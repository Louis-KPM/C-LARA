from .clara_classes import InternalCLARAError
from .clara_utils import absolute_local_file_name, file_exists, basename, copy_local_file, copy_to_local_file
from .clara_utils import make_local_directory, copy_directory_to_local_directory, local_directory_exists, remove_local_directory
from .clara_utils import make_tmp_file, write_json_to_local_file, read_json_local_file, make_zipfile, unzip_file, post_task_update
from .clara_audio_annotator import AudioAnnotator
from .clara_audio_repository import AudioRepository
from .clara_image_repository import ImageRepository

import os
import tempfile
import traceback

def create_export_zipfile(project_directory, audio_metadata, image_metadata, zipfile, callback=None):
    try:
        tmp_dir = tempfile.mkdtemp()
        tmp_zipfile = make_tmp_file('project_zip', 'zip')
        
        copy_project_directory_to_tmp_dir(project_directory, tmp_dir)
        copy_audio_data_to_tmp_dir(audio_metadata, tmp_dir)
        copy_image_data_to_tmp_dir(image_metadata, tmp_dir)
        
        make_zipfile(tmp_dir, tmp_zipfile, callback=callback)
        copy_local_file(tmp_zipfile, zipfile)
        return True
    except Exception as e:
        post_task_update(callback, f'*** Error when trying to create zipfile for project')
        error_message = f'"{str(e)}"\n{traceback.format_exc()}'
        post_task_update(callback, error_message)
        return False
    finally:
        # Remove the tmp dir once we've used it
        if local_directory_exists(tmp_dir):
            remove_local_directory(tmp_dir)

def copy_project_directory_to_tmp_dir(project_directory, tmp_dir):
    tmp_project_dir = os.path.join(tmp_dir, 'project_dir')
    
    copy_directory_to_local_directory(project_directory, tmp_project_dir)

## Format looks like this:
##
##  {
##    "words": [
##        {
##            "word": "once",
##            "file": "C:\\cygwin64\\home\\github\\c-lara\\audio\\tts_repository\\google\\en\\default\\default_311.mp3"
##        },
##        ...
##     "segments": [
##        {
##            "segment": "Once upon a time there were four little Rabbits, and their names were\u2014 Flopsy, Mopsy, Cotton-tail, and Peter.",
##            "file": "C:\\cygwin64\\home\\github\\c-lara\\audio\\tts_repository\\google\\en\\default\\default_356.mp3"
##        },
##        ...

def copy_audio_data_to_tmp_dir(audio_metadata, tmp_dir):
    tmp_audio_dir = os.path.join(tmp_dir, 'audio')
    make_local_directory(tmp_audio_dir)
    file = f'{tmp_audio_dir}/metadata.json'

    for words_or_segments in ( 'words', 'segments' ):
        if words_or_segments in audio_metadata:
            for item in audio_metadata[words_or_segments]:
                if 'file' in item and file_exists(item['file']):
                    pathname = item['file']
                    zipfile_pathname = os.path.join(tmp_audio_dir, basename(pathname))
                    copy_to_local_file(pathname, zipfile_pathname)
                    item['file'] = basename(pathname)
    
    write_json_to_local_file(audio_metadata, file)

## Format looks like this:
##
## [
##    {
##        "image_file_path": "C:\\cygwin64\\home\\github\\c-lara\\images\\image_repository\\Peter_Rabbit_small_18\\tmp1i2yu_18.jpg",
##        "thumbnail_file_path": "C:\\cygwin64\\home\\github\\c-lara\\images\\image_repository\\Peter_Rabbit_small_18\\tmp1i2yu_18_thumbnail.jpg",
##        "image_name": "01VeryBigFirTree",
##        "associated_text": "",
##        "associated_areas": "",
##        "page": 1,
##        "position": "bottom"
##    },
    
def copy_image_data_to_tmp_dir(image_metadata, tmp_dir):
    tmp_image_dir = os.path.join(tmp_dir, 'images')
    make_local_directory(tmp_image_dir)
    file = f'{tmp_image_dir}/metadata.json'
    
    image_metadata_as_json = [ image.to_json() for image in image_metadata ]
    for item in image_metadata_as_json:
        for key in ( 'image_file_path', 'thumbnail_file_path' ):
            if key in item:
                pathname = item[key]
                zipfile_pathname = os.path.join(tmp_image_dir, basename(pathname))
                copy_to_local_file(pathname, zipfile_pathname)
                item[key] = basename(pathname)
    
    write_json_to_local_file(image_metadata_as_json, file)
