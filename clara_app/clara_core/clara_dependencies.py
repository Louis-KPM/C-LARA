

from .clara_utils import absolute_file_name, remove_duplicates_from_list_of_hashable_items, get_file_time
from .clara_classes import InternalCLARAError

from datetime import datetime, timezone

import traceback
import pprint

class CLARADependencies:

    # Initialise with the information needed to calculate whether processing phases are up to date.
    def __init__(self, clara_project_internal, project_id,
                 human_audio_info=None, phonetic_human_audio_info=None,
                 format_preferences=None, content_object=None,
                 callback=None):
        self.clara_project_internal = clara_project_internal
        self.project_id = project_id
        self.human_audio_info = human_audio_info
        self.phonetic_human_audio_info = phonetic_human_audio_info
        self.format_preferences = format_preferences
        self.content_object = content_object

        # The different C-LARA processing phases we will evaluate for being up to date
        self._processing_phases = [
            "plain",                # Plain text
                                    # Accessible from CLARAProjectInternal object
    
            "summary",              # Typically AI-generated summary
                                    # Accessible from CLARAProjectInternal object
            
            "cefr_level",           # Typically AI-generated estimate of CEFR level
                                    # Accessible from CLARAProjectInternal object

            "title",                # Typically AI-generated title for first page of text
                                    # Accessible from CLARAProjectInternal object

            "segmented_title",      # Typically AI-generated segmented version of title for first page of text
                                    # Accessible from CLARAProjectInternal object 
            
            "segmented",            # Typically AI-generated segmented version of text
                                    # Accessible from CLARAProjectInternal object
            
            "images",               # Typically AI-generated images
                                    # Accessible from CLARAProjectInternal object
            
            "phonetic",             # Typically AI-generated phonetic version of text
                                    # Only possible for languages with phonetic lexicon resources
                                    # Accessible from CLARAProjectInternal object
            
            "gloss",                # Typically AI-generated glossed version of text
                                    # Accessible from CLARAProjectInternal object
            
            "lemma",                # Typically AI-generated lemma-tagged version of text
                                    # Accessible from CLARAProjectInternal object
            
            "audio",                # Declarations for how to attach audio to normal text
                                    # If human-recorded audio is specified, the relevant audio files
                                    # Accessible from CLARAProject object

            "audio_phonetic",       # Declarations for how to attach audio to phonetic text
                                    # If human-recorded audio is specified, the relevant audio files
                                    # Accessible from CLARAProject object
            
            "format_preferences",   # Declarations for formatting, e.g. font and text alignment
                                    # Accessible from CLARAProject object
            
            "render",               # Rendered version of normal text
                                    # Accessible from CLARAProjectInternal object

            "render_phonetic",      # Rendered version of phonetic text
                                    # Accessible from CLARAProjectInternal object
            
            "social_network",       # Social network page if text is posted there
                                    # Accessible from CLARAProject object
            ]

        # For each processing phase, list the preceding phases on which it is immediately dependent
        self._immediate_dependencies = {
            "plain": [],
            
            "summary": [ "plain" ],
            
            "cefr_level": [ "plain" ],

            "title": [ "plain" ],

            "segmented_title": [ "title" ],
            
            "segmented": [ "plain" ],
            
            "images": [ "plain" ],
            
            "phonetic": [ "segmented", "segmented_title" ],
            
            "gloss": [ "segmented", "segmented_title" ],
            
            "lemma": [ "segmented", "segmented_title" ],
            
            "audio": [ "segmented" ],

            "audio_phonetic": [ "phonetic" ],
            
            "format_preferences": [ "segmented" ],
            
            "render": [ "title", "gloss", "lemma", "images", "audio", "format_preferences" ],

            "render_phonetic": [ "phonetic", "images", "audio_phonetic", "format_preferences" ],
            
            "social_network": [ "render", "render_phonetic", "summary", "cefr_level" ],
            }

    # Create the transitive closure of _immediate_dependencies to get the full list of dependencies
    def get_dependencies(self, processing_phase_id):
        all_dependencies = []
        
        if not processing_phase_id in self._immediate_dependencies:
            return []
        else:
            immediate_dependencies = self._immediate_dependencies[processing_phase_id]
            all_dependencies += immediate_dependencies
        
        for dependency_processing_phase_id in immediate_dependencies:
            all_dependencies += self.get_dependencies(dependency_processing_phase_id)
            
        return remove_duplicates_from_list_of_hashable_items(all_dependencies)

    # Get the latest timestamp for files and database records associated with a processing phase
    def timestamp_for_phase(self, processing_phase_id):
        if processing_phase_id in [ "plain", "summary", "cefr_level", "title", "segmented_title",
                                    "segmented", "phonetic", "gloss", "lemma" ]:
            try:
                if not self.clara_project_internal.text_versions[processing_phase_id]:
                    return None
                else:
                    file_path = self.clara_project_internal.text_versions[processing_phase_id]
                    return get_file_time(file_path, time_format='timestamp')
            except FileNotFoundError:
                return None
            
        elif processing_phase_id == 'images':
                images = self.clara_project_internal.get_all_project_images()
                timestamps = [ get_file_time(image.image_file_path, time_format='timestamp')
                               for image in images ]
                return latest_timestamp(timestamps)
            
        elif processing_phase_id == 'audio':
            if not self.human_audio_info:
                return None
            human_voice_id = self.human_audio_info.voice_talent_id
            metadata = []
            if self.human_audio_info.use_for_words:
                metadata += self.clara_project_internal.get_audio_metadata(human_voice_id=human_voice_id,
                                                                           audio_type_for_words='human', type='words',
                                                                           format='text_and_full_file')
            if self.human_audio_info.use_for_segments:
                metadata += self.clara_project_internal.get_audio_metadata(human_voice_id=human_voice_id,
                                                                           audio_type_for_segments='human', type='segments',
                                                                           format='text_and_full_file')
            objects_and_timestamps = [ [ item['full_file'], get_file_time(item['full_file'], time_format='timestamp') ]
                                       for item in metadata
                                       # We can have null files for items that haven't been recorded
                                       if item['full_file'] ]

            if self.human_audio_info.updated_at:
                objects_and_timestamps.append([ 'human_audio_info record', self.human_audio_info.updated_at ])

            return latest_timestamp_from_objects_and_timestamps(objects_and_timestamps, label='human_audio', debug=False)
        
        elif processing_phase_id == 'audio_phonetic':
            if not self.phonetic_human_audio_info:
                return None
            human_voice_id = self.phonetic_human_audio_info.voice_talent_id
            metadata = []
            if self.human_audio_info.use_for_words:
                metadata += self.clara_project_internal.get_audio_metadata(phonetic=True, human_voice_id=human_voice_id,
                                                                           audio_type_for_words='human', type='words',
                                                                           format='text_and_full_file')
            objects_and_timestamps = [ [ item['full_file'], get_file_time(item['full_file'], time_format='timestamp') ]
                                       for item in metadata
                                       # We can have null files for items that haven't been recorded
                                       if item['full_file'] ]

            if self.phonetic_human_audio_info.updated_at:
                objects_and_timestamps.append([ 'phonetic_human_audio_info record', self.phonetic_human_audio_info.updated_at ])
            
            return latest_timestamp_from_objects_and_timestamps(objects_and_timestamps, label='phonetic_human_audio', debug=False)
        
        elif processing_phase_id == 'format_preferences':
            if not self.format_preferences:
                return None
            else:
                return self.format_preferences.updated_at
            
        elif processing_phase_id == 'render':
            if not self.clara_project_internal.rendered_html_exists(self.project_id):
                return None
            else:
                return self.clara_project_internal.rendered_html_timestamp(self.project_id, time_format='timestamp')
            
        elif processing_phase_id == 'render_phonetic':
            if not self.clara_project_internal.rendered_phonetic_html_exists(self.project_id):
                return None
            else:
                return self.clara_project_internal.rendered_phonetic_html_timestamp(self.project_id, time_format='timestamp')
            
        elif processing_phase_id == 'social_network':
            if not self.content_object:
                return None
            else:
                return self.content_object.updated_at
            
        else:
            raise InternalCLARAError(message=f'Unknown processing phase id {processing_phase_id}')

    # Get the latest timestamp associated with all the phases
    def timestamps_for_all_phases(self):
        return { processing_phase_id: self.timestamp_for_phase(processing_phase_id)
                 for processing_phase_id in self._processing_phases }

    # Print ages of timestamps for all phases. Use for debugging
    def print_ages_for_all_phase_timestamps(self):
        processing_phase_timestamp_dict = self.timestamps_for_all_phases()
        ages_dict = { processing_phase_id: timestamp_to_age_in_seconds(processing_phase_timestamp_dict[processing_phase_id])
                      for processing_phase_id in self._processing_phases }
        print(f'Ages for processing phases')
        pprint.pprint(ages_dict)        

    # Use timestamps_for_all_phases to get the latest timestamp for all the phases on which each phase depends
    def timestamp_for_all_phase_dependencies(self):
        processing_phase_timestamp_dict = self.timestamps_for_all_phases()
        result = {}
        
        for processing_phase_id in self._processing_phases:
            dependencies = self.get_dependencies(processing_phase_id)
            timestamps = [ processing_phase_timestamp_dict[dependency_processing_phase_id] for
                           dependency_processing_phase_id in dependencies ]
            result[processing_phase_id] = latest_timestamp(timestamps)
            
        return result

    # Use the timestamps for phases and dependencies to determine whether the resources for each phase are up to date
    def up_to_date_dict(self, debug=False):
        processing_phase_timestamp_dict = self.timestamps_for_all_phases()
        processing_phase_dependency_timestamp_dict = self.timestamp_for_all_phase_dependencies()
        result = {}
        
        for processing_phase in self._processing_phases:
            processing_phase_timestamp = processing_phase_timestamp_dict[processing_phase]
            processing_phase_dependency_timestamp = processing_phase_dependency_timestamp_dict[processing_phase]
            
            # If the phase and the dependencies both have a timestamp,
            # and the timestamp for the dependencies is later, then the phase is out of date
            if processing_phase_timestamp and processing_phase_dependency_timestamp and \
               later_timestamp(processing_phase_dependency_timestamp, processing_phase_timestamp):
                result[processing_phase] = False
            # Else if there is no timestamp, then if it's an optional phase, count it as up to date
            # otherwise count it as out of date
            elif not processing_phase_timestamp:
                _optional_phases = ( "audio", "audio_phonetic", "format_preferences" )
                result[processing_phase] = True if processing_phase in _optional_phases else False
            # Otherwise the phase is up to date
            else:
                result[processing_phase] = True

            if debug:
                print(f'---------------------')
                print(f'Processing phase: {processing_phase}:')
                print(f'Timestamp: {processing_phase_timestamp}')
                print(f'Age in seconds: {timestamp_to_age_in_seconds(processing_phase_timestamp)}')
                print(f'Dependencies timestamp: {processing_phase_dependency_timestamp}')
                print(f'Dependencies age in seconds: {timestamp_to_age_in_seconds(processing_phase_dependency_timestamp)}')
                print(f'Up to date: {result[processing_phase]}')

        return result

# Utility functions

# Return the latest in a list of timestamps. If list is empty, return None
def latest_timestamp(timestamps):
    try:
        aware_timestamps = [convert_to_timezone_aware(timestamp)
                            for timestamp in timestamps if timestamp is not None]
        return max(aware_timestamps)
    except ValueError:
        # Return None if the list is empty (i.e., all timestamps are None)
        return None

# Version of latest_timestamp adapted to print more debugging info
def latest_timestamp_from_objects_and_timestamps(objects_and_timestamps, label=None, debug=False):
    if not objects_and_timestamps:
        if debug:
            print(f'latest_timestamp_from_objects_and_timestamps (label={label}): empty list')
        return None

    ( latest_object, latest_timestamp ) = ( None, None )
    for ( x, timestamp ) in objects_and_timestamps:
        if not latest_timestamp or later_timestamp(timestamp, latest_timestamp):
            ( latest_object, latest_timestamp ) = ( x, timestamp)

    if debug:
        print(f'latest_timestamp_from_objects_and_timestamps (label={label})')
        print(f'latest_timestamp: {latest_timestamp}')
        print(f'latest_age: {timestamp_to_age_in_seconds(latest_timestamp)}')
        print(f'latest_object: "{latest_object}"')

    return latest_timestamp

# Returns True if timestamp1 is later than timestamp2, otherwise False
def later_timestamp(timestamp1, timestamp2):
    if timestamp1 is None or timestamp2 is None:
        return False

    aware_timestamp1 = convert_to_timezone_aware(timestamp1)
    aware_timestamp2 = convert_to_timezone_aware(timestamp2)
                                                                               
    return aware_timestamp1 > aware_timestamp2

# Returns the time delta in seconds between the present moment and the timestamp.
# This should be useful for debugging.
def timestamp_to_age_in_seconds(timestamp):
    if timestamp is None:
        return None
    now = datetime.now().timestamp()
    return int(now - timestamp.timestamp())

# Convert naive datetime objects to timezone-aware objects (using UTC)
def convert_to_timezone_aware(timestamp):
    try:
        return timestamp if timestamp.tzinfo else timestamp.replace(tzinfo=timezone.utc)
    except:
        return timestamp
    
