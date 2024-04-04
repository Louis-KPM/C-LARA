"""
clara_image_repository_orm.py

This module implements an image repository that stores image files and associated metadata. The code is based
on the earlier class AudioRepositoryORM, defined in clara_audio_repository_orm.py.

Classes:
- ImageRepositoryORM: Class for managing the audio repository.

The ImageRepositoryORM class provides methods for adding entries, retrieving entries,
getting the image directory, and storing image files.
"""

from django.core.exceptions import ObjectDoesNotExist

from .models import ImageMetadata

from .clara_image_repository import ImageRepository

from .clara_utils import get_config, absolute_file_name, absolute_local_file_name, file_exists, local_file_exists, copy_local_file, basename
from .clara_utils import make_directory, remove_directory, directory_exists, local_directory_exists, make_local_directory, copy_directory
from .clara_utils import list_files_in_directory, post_task_update, generate_unique_file_name
from .clara_utils import adjust_file_path_for_imported_data, generate_thumbnail_name

from .clara_classes import Image, InternalCLARAError

from pathlib import Path

from PIL import Image as PILImage

import os
import traceback

config = get_config()

class ImageRepositoryORM:
    def __init__(self, initialise_from_non_orm=False, callback=None):
        self.base_dir = absolute_file_name(config.get('image_repository', 'base_dir_orm'))

        if not directory_exists(self.base_dir):
            if initialise_from_non_orm:
                self.initialise_from_non_orm_repository(callback=callback)
            else:
                make_directory(self.base_dir, parents=True, exist_ok=True)
                post_task_update(callback, f'--- Created base directory for image repository, {self.base_dir}')
        elif initialise_from_non_orm:
            post_task_update(callback, f'--- Image repository already initialised, {self.base_dir} exists')

    def initialise_from_non_orm_repository(self, callback=None):
        try:
            non_orm_repository = ImageRepository(callback=callback)
            exported_data = non_orm_repository.export_image_metadata()

            if not exported_data:
                post_task_update(callback, f'--- No data found in non-ORM repository')
                make_directory(self.base_dir, parents=True, exist_ok=True)
                post_task_update(callback, f'--- Created base directory for image repository, {self.base_dir}')
                return

            post_task_update(callback, f'--- Importing {len(exported_data)} items from non-ORM repository')
            
            base_dir_non_orm = absolute_file_name(config.get('image_repository', 'base_dir'))
            base_dir_orm = absolute_file_name(config.get('image_repository', 'base_dir_orm'))
            
            new_objects = []
            for data in exported_data:
                new_file_path = adjust_file_path_for_imported_data(data['file_path'], base_dir_non_orm, base_dir_orm, callback=callback)
                new_objects.append(ImageMetadata(
                    project_id=data['project_id'],
                    image_name=data['image_name'],
                    file_path=new_file_path,
                    associated_text=data['associated_text'],
                    associated_areas=data['associated_areas'],
                    page=data['page'],
                    position=data['position'],
                ))

            ImageMetadata.objects.bulk_create(new_objects)
            copy_directory(base_dir_non_orm, base_dir_orm)

        except Exception as e:
            post_task_update(callback, f'Error initialising from non-ORM repository: "{str(e)}"\n{traceback.format_exc()}')
            return []

    def delete_entries_for_project(self, project_id, callback=None):
        try:
            project_id = str(project_id)
            post_task_update(callback, f'--- Deleting image repository DB entries for {project_id}')
            
            # Delete database entries for the specified project
            entries_deleted = ImageMetadata.objects.filter(project_id=project_id).delete()
            post_task_update(callback, f'--- Deleted {entries_deleted[0]} DB entries for project ID {project_id}')

            # Delete associated image files from the file system
            project_dir = self.get_project_directory(project_id)
            if directory_exists(project_dir):
                remove_directory(project_dir)
                post_task_update(callback, f'--- Image files for project ID {project_id} deleted')
            
            post_task_update(callback, 'Finished deletion process successfully.')

        except Exception as e:
            error_message = f'*** Error when trying to delete image data for project ID {project_id}: "{str(e)}"\n{traceback.format_exc()}'
            post_task_update(callback, error_message)

    def add_entry(self, project_id, image_name, file_path, associated_text='', associated_areas='', page=1, position='bottom', callback=None):
        try:
            # Ensure project_id is a string and page is an integer
            project_id = str(project_id)
            page = int(page)

            # Try to retrieve an existing entry
            obj, created = ImageMetadata.objects.update_or_create(
                project_id=project_id, 
                image_name=image_name,
                defaults={
                    'file_path': file_path, 
                    'associated_text': associated_text, 
                    'associated_areas': associated_areas, 
                    'page': page, 
                    'position': position
                }
            )

            if created:
                post_task_update(callback, f'--- Created new image entry for project_id={project_id} and image_name={image_name}')
            else:
                post_task_update(callback, f'--- Updated existing image entry for project_id={project_id} and image_name={image_name}')

        except Exception as e:
            error_message = f'*** Error when adding/updating image entry "{project_id}/{image_name}" in the database: "{str(e)}"\n{traceback.format_exc()}'
            post_task_update(callback, error_message)
            raise InternalCLARAError(message='Image database inconsistency')

    def store_associated_areas(self, project_id, image_name, associated_areas, callback=None):
        try:
            # Ensure project_id is a string
            project_id = str(project_id)

            # Try to update the existing entry with the new associated_areas
            updated_count = ImageMetadata.objects.filter(project_id=project_id, image_name=image_name).update(associated_areas=associated_areas)

            if updated_count > 0:
                post_task_update(callback, f'--- Updated associated_areas for project_id={project_id} and image_name={image_name}')
            else:
                post_task_update(callback, f'*** No matching entry found to update associated_areas for "{project_id}/{image_name}"')
            
        except Exception as e:
            error_message = f'*** Error when updating associated_areas for "{project_id}/{image_name}": "{str(e)}"\n{traceback.format_exc()}'
            post_task_update(callback, error_message)
            raise InternalCLARAError(message='Image database inconsistency')

    def get_entry(self, project_id, image_name, callback=None):
        try:
            project_id = str(project_id)
            
            # Try to fetch the entry from the database
            entry = ImageMetadata.objects.get(project_id=project_id, image_name=image_name)
            
            # Generate thumbnail name
            thumbnail = generate_thumbnail_name(entry.file_path)
            
            # Construct and return an Image object with all necessary information

            image = Image(entry.file_path,
                          thumbnail,
                          entry.image_name,
                          entry.associated_text,
                          entry.associated_areas,
                          entry.page,
                          entry.position)
            
            return image
                
        except ObjectDoesNotExist:
            post_task_update(callback, f'*** No entry found for "{image_name}" in Image database.')
            return None
        except Exception as e:
            error_message = f'*** Error when looking for "{image_name}" in Image database: "{str(e)}"\n{traceback.format_exc()}'
            post_task_update(callback, error_message)
            raise InternalCLARAError(message='Image database inconsistency')

    def get_all_entries(self, project_id, callback=None):
        try:
            project_id = str(project_id)
            post_task_update(callback, f'--- Retrieving all images for project {project_id}')

            # Fetch all entries for the given project_id from the ORM
            entries = ImageMetadata.objects.filter(project_id=project_id)

            images = []
            for entry in entries:
                # Generate thumbnail name
                thumbnail = generate_thumbnail_name(entry.file_path)
                
                # Construct an Image object for each entry
                image = Image(entry.file_path,
                              thumbnail,
                              entry.image_name,
                              entry.associated_text,
                              entry.associated_areas,
                              entry.page,
                              entry.position)
                images.append(image)

            post_task_update(callback, f'--- Retrieved {len(images)} images for project {project_id}')
            return images
                
        except Exception as e:
            error_message = f'*** Error when retrieving images for project {project_id}: {str(e)}\n{traceback.format_exc()}'
            post_task_update(callback, error_message)
            raise InternalCLARAError(message='Image database inconsistency')

    def store_image(self, project_id, source_file, keep_file_name=True, callback=None):
        try:
            project_id = str(project_id)
            project_dir = self.get_project_directory(project_id)
            make_directory(project_dir, parents=True, exist_ok=True)

            # Use UUID for generating a unique file name if not keeping the original file name
            file_name = basename(source_file) if keep_file_name else generate_unique_file_name(f'project_{project_id}', extension='png')
            destination_path = str(Path(project_dir) / file_name)
            copy_local_file(source_file, destination_path)

            # Generate and store thumbnail
            try:
                original_image = PILImage.open(source_file)
                thumbnail_size = (100, 100)  # Example size, adjust as needed
                original_image.thumbnail(thumbnail_size)
                thumbnail_destination_path = generate_thumbnail_name(destination_path)
                original_image.save(thumbnail_destination_path)

                post_task_update(callback, f'--- Image and thumbnail stored at {destination_path} and {thumbnail_destination_path}')
            except Exception as e:
                error_message = f'*** Error when generating thumbnail for {file_name}: {str(e)}\n{traceback.format_exc()}'
                post_task_update(callback, error_message)
                raise InternalCLARAError(message='Error generating thumbnail')

            return destination_path
        except Exception as e:
            error_message = f'*** Error when storing image "{source_file}" in image repository: "{str(e)}"\n{traceback.format_exc()}'
            post_task_update(callback, error_message)
            raise InternalCLARAError(message='Image repository error')

    def remove_entry(self, project_id, image_name, callback=None):
        try:
            project_id = str(project_id)
            post_task_update(callback, f'--- Attempting to remove entry for image {image_name} in project {project_id}')
            
            # Attempt to fetch and delete the specified entry
            entry = ImageMetadata.objects.get(project_id=project_id, image_name=image_name)
            entry.delete()
            
            post_task_update(callback, f'--- Entry for image {image_name} in project {project_id} removed successfully')
        except ObjectDoesNotExist:
            post_task_update(callback, f'*** No entry found for image {image_name} in project {project_id}')
        except Exception as e:
            error_message = f'*** Error when removing entry for image {image_name} in project {project_id}: {str(e)}\n{traceback.format_exc()}'
            post_task_update(callback, error_message)
            raise InternalCLARAError(message='Image database inconsistency')

    def get_annotated_image_text(self, project_id, callback=None):
        try:
            project_id = str(project_id)
            post_task_update(callback, f'--- Retrieving annotated image text for project {project_id}')
            
            entries = ImageMetadata.objects.filter(project_id=project_id).order_by('page', 'position')
            
            annotated_image_text = ""
            for entry in entries:
                image_name = entry.image_name
                associated_text = entry.associated_text
                page = entry.page
                position = entry.position
                annotated_image_text += f"<page img='{image_name}' page='{page}' position='{position}'>\n{associated_text}\n"

            post_task_update(callback, f'--- Annotated image text for project {project_id} generated')
            return annotated_image_text

        except ObjectDoesNotExist:
            return "" # Return an empty string if no entries found
        except Exception as e:
            error_message = f'*** Error when retrieving annotated image text for project {project_id}: {str(e)}\n{traceback.format_exc()}'
            post_task_update(callback, error_message)
            raise InternalCLARAError(message='Image database inconsistency')

    def get_project_directory(self, project_id):
        # Returns the directory path where images for a specific project are stored
        return absolute_file_name(Path(self.base_dir) / str(project_id))


