"""
clara_audio_repository.py

This module implements an audio repository that stores metadata and generated audio files from human voices and various TTS engines.

Classes:
- AudioRepository: Class for managing the audio repository.

The AudioRepository class provides methods for adding entries, retrieving entries, getting the voice directory, and storing mp3 files.

Use clara_database_adapter so that the code works for both sqlite3 and PostgreSQL databases.

SQL templates must be written in PostgreSQL format with %s signifying a parameter placeholder.
The function clara_database_adapter.localise_sql_query converts this to sqlite3 format if necessary.
"""

from .clara_database_adapter import connect, localise_sql_query

from .clara_tts_api import get_tts_engine_types
from .clara_utils import _s3_storage, get_config, absolute_file_name, absolute_local_file_name, file_exists, local_file_exists, copy_local_file
from .clara_utils import make_directory, remove_directory, directory_exists, local_directory_exists, make_local_directory, list_files_in_directory, post_task_update

from .clara_classes import InternalCLARAError

from pathlib import Path

import os
import traceback

config = get_config()

class AudioRepository:
    def __init__(self, callback=None):   
        self.db_file = absolute_local_file_name(config.get('audio_repository', ( 'db_file' if _s3_storage else 'db_file_local' )))
        self.base_dir = absolute_file_name(config.get('audio_repository', 'base_dir'))
        self._initialize_repository(callback=callback)

    def _initialize_repository(self, callback=None):
        if not directory_exists(self.base_dir):
            make_directory(self.base_dir, parents=True, exist_ok=True)

        try:
            if os.getenv('DB_TYPE') == 'sqlite':
                # If we're using sqlite, check if db_file exists and if not create it
                db_dir = config.get('audio_repository', 'db_dir')
                if not local_directory_exists(db_dir):
                    post_task_update(callback, f'--- Creating empty DB dir for audio repository, {db_dir}')
                    make_local_directory(db_dir)
                if not local_file_exists(self.db_file):
                    post_task_update(callback, f'--- Creating empty DB file for audio repository, {self.db_file}')
                    open(self.db_file, 'a').close()
                    
            connection = connect(self.db_file)
            cursor = connection.cursor()
        
            if os.getenv('DB_TYPE') == 'sqlite':
                cursor.execute('''CREATE TABLE IF NOT EXISTS metadata
                                  (id INTEGER PRIMARY KEY,
                                   engine_id TEXT,
                                   language_id TEXT,
                                   voice_id TEXT,
                                   text TEXT,
                                   file_path TEXT)''')            
            # Assume Postgres, which does auto-incrementing differently
            # We need a suitable definition for the primary key
            else:
                cursor.execute('''CREATE TABLE IF NOT EXISTS metadata
                                  (id SERIAL PRIMARY KEY,
                                   engine_id TEXT,
                                   language_id TEXT,
                                   voice_id TEXT,
                                   text TEXT,
                                   file_path TEXT)''')
                                   
            connection.commit()
            connection.close()
            post_task_update(callback, f'--- Initialised audio repository')
                                   
        except Exception as e:
            error_message = f'*** Error when trying to initialise TTS database: "{str(e)}"\n{traceback.format_exc()}'
            post_task_update(callback, error_message)
            raise InternalCLARAError(message='TTS database inconsistency')   

    def delete_entries_for_language(self, engine_id, language_id, callback=None):
        try:
            post_task_update(callback, f'--- Deleting tts repository DB entries for {language_id}')
            connection = connect(self.db_file)
            cursor = connection.cursor()
            cursor.execute(localise_sql_query("DELETE FROM metadata WHERE language_id = %s"), (language_id,))
            connection.commit()
            connection.close()
            post_task_update(callback, f'--- DB entries for {language_id} deleted')

            post_task_update(callback, f'--- Deleting audio files for {language_id}')
            language_dir = self.get_language_directory(engine_id, language_id)
            if directory_exists(language_dir):
                remove_directory(language_dir)
            post_task_update(callback, f'--- audio files for {engine_id} and {language_id} deleted')
            post_task_update(callback, f'finished')
        except Exception as e:
            error_message = f'*** Error when trying to delete audio data: "{str(e)}"\n{traceback.format_exc()}'
            post_task_update(callback, error_message)
            post_task_update(callback, f'error')

    def add_entry(self, engine_id, language_id, voice_id, text, file_path, callback=None):
        try:
            connection = connect(self.db_file)
            cursor = connection.cursor()
            cursor.execute(localise_sql_query("INSERT INTO metadata (engine_id, language_id, voice_id, text, file_path) VALUES (%s, %s, %s, %s, %s)"),
                           (engine_id, language_id, voice_id, text, file_path))
            connection.commit()
            connection.close()
        except Exception as e:
            post_task_update(callback, f'*** Error when inserting "{language_id}/{text}/{file_path}" into TTS database: "{str(e)}"')
            raise InternalCLARAError(message='TTS database inconsistency')

    def get_entry(self, engine_id, language_id, voice_id, text, callback=None):
        try:
            connection = connect(self.db_file)
            cursor = connection.cursor()
            if os.getenv('DB_TYPE') == 'sqlite':
                cursor.execute("SELECT file_path FROM metadata WHERE engine_id = ? AND language_id = ? AND voice_id = ? AND text = ?",
                               (engine_id, language_id, voice_id, text))
            else:
                # Assume postgres
                cursor.execute("""SELECT file_path FROM metadata 
                                  WHERE engine_id = %(engine_id)s 
                                  AND language_id = %(language_id)s 
                                  AND voice_id = %(voice_id)s 
                                  AND text = %(text)s""",
                               {
                                  'engine_id': engine_id,
                                  'language_id': language_id,
                                  'voice_id': voice_id,
                                  'text': text
                               })
            result = cursor.fetchone()
            connection.close()
            if os.getenv('DB_TYPE') == 'sqlite':
                return result[0] if result else None
            else:  # Assuming PostgreSQL
                return result['file_path'] if result else None

        except Exception as e:
            error_message = f'*** Error when looking for "{text}" in TTS database: "{str(e)}"\n{traceback.format_exc()}'
            post_task_update(callback, error_message)
            raise InternalCLARAError(message='TTS database inconsistency')

    def get_language_directory(self, engine_id, language_id):
        return absolute_file_name( Path(self.base_dir) / engine_id / language_id )

    def get_voice_directory(self, engine_id, language_id, voice_id):
        return absolute_file_name( Path(self.base_dir) / engine_id / language_id / voice_id )

    def store_mp3(self, engine_id, language_id, voice_id, source_file):
        voice_dir = self.get_voice_directory(engine_id, language_id, voice_id)
        make_directory(voice_dir, parents=True, exist_ok=True)
        file_name = f"{voice_id}_{len(list_files_in_directory(voice_dir)) + 1}.mp3"
        destination_path = str(Path(voice_dir) / file_name)
        copy_local_file(source_file, destination_path)
        return destination_path
    