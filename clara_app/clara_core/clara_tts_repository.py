"""
clara_tts_repository.py

This module implements a TTS repository that stores metadata and generated audio files from various TTS engines.

Classes:
- TTSRepository: Class for managing the TTS repository.

The TTSRepository class provides methods for adding entries, retrieving entries, getting the voice directory, and storing mp3 files.

Use clara_database_adapter so that the code works for both sqlite3 and PostgreSQL databases.

SQL templates must be written in PostgreSQL format with %s signifying a parameter placeholder.
The function clara_database_adapter.localise_sql_query converts this to sqlite3 format if necessary.
"""

from .clara_database_adapter import connect, localise_sql_query

from .clara_tts_api import get_tts_engine_types
from .clara_utils import _s3_storage, get_config, absolute_file_name, absolute_local_file_name, file_exists, copy_local_file
from .clara_utils import make_directory, remove_directory, directory_exists, list_files_in_directory, post_task_update

from .clara_classes import InternalCLARAError

from pathlib import Path

import os
import traceback

config = get_config()

class TTSRepository:
    def __init__(self):   
        self.db_file = absolute_local_file_name(config.get('tts_repository', 'db_file_s3' if _s3_storage else 'db_file'))
        self.base_dir = absolute_file_name(config.get('tts_repository', 'base_dir'))
        self._initialize_repository()

    def _initialize_repository(self):
        if not directory_exists(self.base_dir):
            make_directory(self.base_dir)

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

    def delete_entries_for_language(self, language_id):
        connection = connect(self.db_file)
        cursor = connection.cursor()
        cursor.execute(localise_sql_query("DELETE FROM metadata WHERE language_id = %s"), (language_id,))
        connection.commit()
        connection.close()

        for engine_id in get_tts_engine_types():
            remove_directory(self.get_language_directory(engine_id, language_id))

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
            # cursor.execute(localise_sql_query("SELECT file_path FROM metadata WHERE engine_id = %s AND language_id = %s AND voice_id = %s AND text = %s"),
                           # (engine_id, language_id, voice_id, text))
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
            return result[0] if result else None
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
