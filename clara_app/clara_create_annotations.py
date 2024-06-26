"""
This module contains functions to generate segmented, glossed, and tagged versions of a given text using ChatGPT4.
These functions are used to annotate the text with various annotations, such as pages, segments, glosses, and tags.

The main functions are:

1. generate_segmented_version(text, l2_language):
   Takes a text and target language, and returns a tuple where the first element
   is a segmented version of the text and the second element is a list of APICall instances related to the operation.

2. improve_segmented_version(segmented_text, l2_language):
   Similar to (1), but takes an already segmented text and tries to improve the segmentation.

3. generate_glossed_version(segmented_text, l1_language, l2_language):
   Takes a segmented text, source language, and target language, and returns a tuple where the first element
   is a glossed version of the text and the second element is a list of APICall instances related to the operation.

4. improve_glossed_version(glossed_text, l1_language, l2_language):
   Similar to (3), but takes an already glossed text and tries to improve the glossing.

5. generate_tagged_version(segmented_text, l2_language):
   Takes a segmented text and target language, and returns a tuple where the first element
   is a tagged version of the text and the second element is a list of APICall instances related to the operation.

6. improve_tagged_version(tagged_text, l1_language, l2_language):
   Similar to (3), but takes an already tagged text and tries to improve the tagging.

There are also several utility functions to help with the annotation process.
"""

from . import clara_prompt_templates
from . import clara_chatgpt4
from . import clara_internalise
#from . import clara_test

from .clara_utils import get_config, post_task_update
from .clara_classes import *

import json
import regex
import difflib
import traceback
import copy
import pprint

config = get_config()

# Try invoking the template-based prompt generation with trivial text to see if we get an error
def invoke_templates_on_trivial_text(annotate_or_improve, version, l1_language, l2_language):
    if not version in ( 'segmented', 'gloss', 'lemma', 'pinyin', 'lemma_and_gloss' ):
        return True
    if version == 'segmented':
        text = ''
        return segmentation_prompt(annotate_or_improve, text, l2_language)
    if version == 'gloss':
        simplified_elements_json = []
        return glossing_prompt(annotate_or_improve, simplified_elements_json, l1_language, l2_language)
    if version == 'lemma':
        simplified_elements_json = []
        return tagging_prompt(annotate_or_improve, simplified_elements_json, l2_language)
    if version == 'mwe':
        simplified_elements_json = []
        return mwe_prompt(annotate_or_improve, simplified_elements_json, l2_language)
    if version == 'pinyin':
        simplified_elements_json = []
        return pinyin_tagging_prompt(annotate_or_improve, simplified_elements_json, l2_language)
    if version == 'lemma_and_gloss':
        simplified_elements_json = []
        return joint_tagging_and_glossing_prompt(simplified_elements_json, l1_language, l2_language)
    
# Annotate the text with pages and segments
def generate_segmented_version(text, l2_language, config_info={}, callback=None):
    return generate_or_improve_segmented_version('annotate', text, l2_language, config_info=config_info, callback=callback)

# Improve annotation of the text with pages and segments
def improve_segmented_version(text, l2_language, config_info={}, callback=None):
    return generate_or_improve_segmented_version('improve', text, l2_language, config_info=config_info, callback=callback)

# Annotate the text with glosses
def generate_glossed_version(segmented_text, l1_language, l2_language, mwe=False,
                             current_glossed_text=None, config_info={}, callback=None):
    return generate_or_improve_annotated_version('annotate', 'gloss', segmented_text, l1_language, l2_language,
                                                 mwe=mwe, current_annotated_text=current_glossed_text,
                                                 config_info=config_info, callback=callback)

# Improve annotation of the text with glosses
def improve_glossed_version(glossed_text, l1_language, l2_language, config_info={}, callback=None):
    return generate_or_improve_annotated_version('improve', 'gloss', glossed_text, l1_language, l2_language, config_info=config_info, callback=callback)

# Annotate the text with pinyin
def generate_pinyin_tagged_version(segmented_text, l2_language, config_info={}, callback=None):
    l1_language = 'irrelevant'
    return generate_or_improve_annotated_version('annotate', 'pinyin', segmented_text, l1_language, l2_language, config_info=config_info, callback=callback)

# Improve annotation of the text with pinyin
def improve_pinyin_tagged_version(pinyin_tagged_text, l2_language, config_info={}, callback=None):
    l1_language = 'irrelevant'
    return generate_or_improve_annotated_version('improve', 'pinyin', tagged_text, l1_language, l2_language, config_info=config_info, callback=callback)

# Annotate the text with lemmas
def generate_tagged_version(segmented_text, l2_language, mwe=False,
                            current_lemma_tagged_text=None, config_info={}, callback=None):
    l1_language = 'irrelevant'
    return generate_or_improve_annotated_version('annotate', 'lemma', segmented_text, l1_language, l2_language,
                                                 mwe=mwe, current_annotated_text=current_lemma_tagged_text,
                                                 config_info=config_info, callback=callback)

# Improve annotation of the text with lemmas
def improve_tagged_version(tagged_text, l2_language, config_info={}, callback=None):
    l1_language = 'irrelevant'
    return generate_or_improve_annotated_version('improve', 'lemma', tagged_text, l1_language, l2_language, config_info=config_info, callback=callback)

# Annotate the text with MWEs
def generate_mwe_tagged_version(segmented_text, l2_language,
                                current_mwe_tagged_text=None, config_info={}, callback=None):
    l1_language = 'irrelevant'
    return generate_or_improve_annotated_version('annotate', 'mwe', segmented_text, l1_language, l2_language,
                                                 current_annotated_text=current_mwe_tagged_text, config_info=config_info, callback=callback)


# Improve annotation of the text with lemmas and glosses
def improve_lemma_and_gloss_tagged_version(tagged_text, l1_language, l2_language, config_info={}, callback=None):
    return generate_or_improve_annotated_version('improve', 'lemma_and_gloss', tagged_text, l1_language, l2_language, config_info=config_info, callback=callback)

def generate_or_improve_segmented_version(annotate_or_improve, text, l2_language, config_info={}, callback=None):
    l2_language = l2_language.capitalize()
    annotate_prompt =  segmentation_prompt(annotate_or_improve, text, l2_language)
    api_call = clara_chatgpt4.call_chat_gpt4(annotate_prompt, config_info=config_info, callback=callback)
    return ( api_call.response, [ api_call ] )

def generate_or_improve_annotated_version(annotate_or_improve, processing_phase, annotated_text, l1_language, l2_language,
                                          mwe=False, current_annotated_text=None,
                                          config_info={}, callback=None):

    if mwe:
        source_version = 'mwe'
    elif annotate_or_improve == 'annotate':
        source_version = 'segmented'
    else:
        source_version = processing_phase
    l1_language = l1_language.capitalize()
    l2_language = l2_language.capitalize()
    internalised_annotated_text = clara_internalise.internalize_text(annotated_text, l2_language, l1_language, source_version)
    if current_annotated_text and annotate_or_improve == 'annotate' and processing_phase == 'gloss':
        internalised_current_annotated_text = clara_internalise.internalize_text(current_annotated_text, l2_language, l1_language, 'gloss')
    elif current_annotated_text and annotate_or_improve == 'annotate' and processing_phase == 'lemma':
        internalised_current_annotated_text = clara_internalise.internalize_text(current_annotated_text, l2_language, l1_language, 'lemma')
    elif current_annotated_text and annotate_or_improve == 'annotate' and processing_phase == 'mwe':
        internalised_current_annotated_text = clara_internalise.internalize_text(current_annotated_text, l2_language, l1_language, 'mwe')
    else:
        internalised_current_annotated_text = None

    # Use max_annotation_words from config_info if available, otherwise default to a preset value
    if 'max_annotation_words' in config_info:
        max_elements = config_info['max_annotation_words']
    else:
        max_elements = int(config.get('chatgpt4_annotation', 'max_elements_to_annotate'))

    # segmented_elements is a list of lists of elements, each one corresponding to a segment in the internalised text
    segmented_elements = internalised_annotated_text.segmented_elements()

    # Annotate each chunk separately and store the results in the annotated_elements list
    annotated_elements = []
    # If we are doing MWE tagging, we are returning MWEs for each segment
    analyses_and_mwes_for_segments = []
    all_api_calls = []

    if mwe:
        segments = internalised_annotated_text.segments()
        segmented_elements_mwe_dict = segments_to_segmented_elements_mwe_dict(segments)
    else:
        segmented_elements_mwe_dict = None

    print(f'segmented_elements_mwe_dict: {segmented_elements_mwe_dict}')

    if internalised_current_annotated_text:
        if mwe or processing_phase == 'mwe':
            current_segments = internalised_current_annotated_text.segments()
            current_segmented_elements_dict = segments_to_annotations_dict(current_segments)
        else:
            current_segmented_elements = internalised_current_annotated_text.segmented_elements() if internalised_current_annotated_text else None
            current_segmented_elements_dict = segmented_elements_to_dict(current_segmented_elements)
            
    else:
        current_segmented_elements_dict = None

    #print(f'current_segmented_elements_dict:')
    #pprint.pprint(current_segmented_elements_dict)
    
    if few_enough_segments_changed_to_use_saved_annotations(segmented_elements, current_segmented_elements_dict, processing_phase, mwe, config_info):
        # We're reusing the saved annotations and only redoing the new segments
        print(f'--- Redoing {processing_phase}, trying to reuse material from previous version')
        for elements in segmented_elements:
            key = key_for_segment_elements(elements)
            if key in current_segmented_elements_dict:
                if processing_phase != 'mwe':
                    #print(f'--- Found material for {key} in previous version')
                    old_annotated_segment = current_segmented_elements_dict[key]
                    annotated_elements += old_annotated_segment
                else:
                    old_annotations_and_mwes = current_segmented_elements_dict[key]
                    analyses_and_mwes_for_segments.append(old_annotations_and_mwes)
            else:
                # In the worst case, the segment is too long and needs to be split up
                # Usually, chunks is the same as [ elements ]
                #print(f'--- Annotating material for {key}')
                chunks = split_elements_by_segments([ elements ], max_elements) if not mwe and processing_phase != 'mwe' else [ elements ]
                for chunk in chunks:
                    key = key_for_segment_elements(chunk)
                    mwes_for_segment = segmented_elements_mwe_dict[key] if segmented_elements_mwe_dict and key in segmented_elements_mwe_dict else []
                    print(f'key: {key}, mwes_for_segment: {mwes_for_segment}')
                    annotated_chunk_or_analysis_and_mwes, api_calls = call_chatgpt4_to_annotate_or_improve_elements(annotate_or_improve, processing_phase, chunk,
                                                                                                       l1_language, l2_language, mwe=mwe, mwes=mwes_for_segment,
                                                                                                       config_info=config_info, callback=callback)
                    if processing_phase != 'mwe':
                        annotated_elements += annotated_chunk_or_analysis_and_mwes
                    else:
                        analyses_and_mwes_for_segments.append(annotated_chunk_or_analysis_and_mwes)
                    all_api_calls += api_calls

    else:
        # We're doing everything from scratch
        #print(f'--- Doing {processing_phase} element by element')
        if processing_phase == 'mwe' or mwe:
            # Do tagging involving MWEs one segment at a time
            chunks = segmented_elements
        else:
            chunks = split_elements_by_segments(segmented_elements, max_elements)
        
        for chunk in chunks:
            key = key_for_segment_elements(chunk)
            mwes_for_segment = segmented_elements_mwe_dict[key] if segmented_elements_mwe_dict and key in segmented_elements_mwe_dict else []
            print(f'key: {key}, mwes_for_segment: {mwes_for_segment}')
            annotated_chunk_or_analysis_and_mwes, api_calls = call_chatgpt4_to_annotate_or_improve_elements(annotate_or_improve, processing_phase, chunk,
                                                                                                            l1_language, l2_language, mwe=mwe, mwes=mwes_for_segment,
                                                                                                            config_info=config_info, callback=callback)
            if processing_phase != 'mwe':
                annotated_elements += annotated_chunk_or_analysis_and_mwes
            else:
                analyses_and_mwes_for_segments.append(annotated_chunk_or_analysis_and_mwes)
            all_api_calls += api_calls

    # Reassemble the annotated elements back into the segmented_text structure
    index = 0
    for page in internalised_annotated_text.pages:
        for segment in page.segments:
            # If we are not doing MWE, we replace elements with annotated elements
            if processing_phase != 'mwe':
                n_elements_in_segment = len(segment.content_elements)
                segment.content_elements = annotated_elements[index:index+n_elements_in_segment]
                index += n_elements_in_segment
            # If we are doing MWE, we add the MWEs to the segment
            else:
                segment.annotations = analyses_and_mwes_for_segments[index]
                index += 1
    #print(f'internalised_annotated_text: {internalised_annotated_text}')        
    human_readable_text = internalised_annotated_text.to_text(processing_phase)
    return ( human_readable_text, all_api_calls )

# We index on tuples consisting of the content of each element.
# Typically we have not more than a hundred segments in a text and a few dozen content elements in a segment, so this is acceptably efficient
def key_for_segment_elements(elements):
    return tuple([ element.content for element in elements ])

# Index MWEs on the key given above
def segments_to_segmented_elements_mwe_dict(segments):
    return { key_for_segment_elements(segment.content_elements): ( segment.annotations['mwes'] if 'mwes' in segment.annotations else [] )
             for segment in segments }

# Index a list of segmented elements on the key given above
def segmented_elements_to_dict(segmented_elements):
    if not segmented_elements:
        return None
    
    return { key_for_segment_elements(elements): elements for elements in segmented_elements }

# Index annotations for segmented elements on the key given above
def segments_to_annotations_dict(segments):
    if not segments:
        return None
    
    return { key_for_segment_elements(segment.content_elements): segment.annotations for segment in segments }

# Find how many segments aren't in the previous version and compare with the limit
def few_enough_segments_changed_to_use_saved_annotations(segmented_elements, current_segmented_elements_dict, processing_phase, mwe, config_info):
    if not current_segmented_elements_dict:
        return False

    # If MWE tagging is involved, we do it one segment at a time, so always reuse saved annotations if possible
    if processing_phase == 'mwe' or mwe:
        return True
    
    limit = int(config.get('chatgpt4_annotation', 'max_segments_to_reannotate_separately'))
    new_segments = [ key_for_segment_elements(elements) for elements in segmented_elements
                     if not key_for_segment_elements(elements) in current_segmented_elements_dict \
                     and len(word_items_in_element_list(elements)) > 0 ]
    #print(f'--- Limit = {limit}. {len(new_segments)} new segments:')
    #pprint.pprint(new_segments)
    return len(new_segments) <= limit

def word_and_non_word_text_items_in_element_list(elements):
    return [ element for element in elements if element.type in ( 'Word', 'NonWordText' ) ]

def word_items_in_element_list(elements):
    return [ element for element in elements if element.type in ( 'Word' ) ]

def split_elements_by_segments(segmented_elements, max_elements):
    chunks = []
    current_chunk = []
    current_count = 0

    for segment0 in segmented_elements:
        segment = copy.copy(segment0)   # Copy the segment, since we don't want to modify it in the 'extend' line
        segment_length = len(segment)
        if current_count + segment_length > max_elements:
            if current_chunk:  # if the current chunk is not empty, push it to chunks
                chunks.append(current_chunk)
                current_chunk = []
                current_count = 0
            # If a single segment is larger than max_elements, split it using the stupid method
            # Keeping it unsplit can easily confuse GPT-4
            if segment_length > max_elements:
                #chunks.append(segment)
                split_segment = [segment[i:i + max_elements] for i in range(0, segment_length, max_elements)]
                chunks += split_segment
            else:
                current_chunk = segment
                current_count = segment_length
        else:
            current_chunk.extend(segment)
            current_count += segment_length

    if current_chunk:  # Don't forget to add the last chunk if it exists
        chunks.append(current_chunk)

    return chunks

def call_chatgpt4_to_annotate_or_improve_elements(annotate_or_improve, processing_phase, elements,
                                                  l1_language, l2_language, mwe=False, mwes=[], config_info={}, callback=None):
    word_elements = word_items_in_element_list(elements)
    if len(word_elements) == 0:
        # If we're not doing MWE, return the elements unchanged
        if processing_phase != 'mwe':
            return ( elements, [] )
        # If we're doing MWE, return empty list of MWEs
        else:
            return ( [], [] )

    # Remove markup from the elements before passing to GPT-4 to make things easier for the AI
    word_and_non_word_text_elements = word_and_non_word_text_items_in_element_list(elements)
    
    if annotate_or_improve == 'annotate':
        simplified_elements0 = [ simplify_element_to_string(element) for element in word_and_non_word_text_elements ]
    else:
        simplified_elements0 = [ simplify_element_to_list(element, processing_phase) for element in word_and_non_word_text_elements ]
    simplified_elements = [ element for element in simplified_elements0 if element != False ]
    text_to_annotate = simplified_element_list_to_text(simplified_elements) 
    simplified_elements_json = json.dumps(simplified_elements)
    n_words = len(simplified_elements)
    l1_language = l1_language.capitalize()
    l2_language = l2_language.capitalize()
    if processing_phase == 'gloss':
        annotation_prompt = glossing_prompt(annotate_or_improve, simplified_elements_json, l1_language, l2_language, mwe=mwe, mwes=mwes)
    elif processing_phase == 'lemma':
        annotation_prompt = tagging_prompt(annotate_or_improve, simplified_elements_json, l2_language, mwe=mwe, mwes=mwes)
    elif processing_phase == 'mwe':
        annotation_prompt = mwe_tagging_prompt(annotate_or_improve, simplified_elements_json, l2_language)
    elif processing_phase == 'pinyin':
        annotation_prompt = pinyin_tagging_prompt(annotate_or_improve, simplified_elements_json, l2_language)
    elif processing_phase == 'lemma_and_gloss' and annotate_or_improve == 'improve':
        annotation_prompt = joint_tagging_and_glossing_prompt(simplified_elements_json, l1_language, l2_language)
    else:
        raise InternalCLARAError(message = f'Unsupported combination processing_phase = {processing_phase} and annotate_or_improve = {annotate_or_improve} in create_annotation' )
    api_calls = []
    n_attempts = 0
    limit = int(config.get('chatgpt4_annotation', 'retry_limit'))
    while True:
        if n_attempts >= limit:
            raise ChatGPTError( message=f'*** Giving up, have tried sending this to ChatGPT-4 {limit} times' )
        n_attempts += 1
        post_task_update(callback, f'--- Calling ChatGPT-4 (attempt #{n_attempts}) to {annotate_or_improve} text ({n_words} words and punctuation marks): "{text_to_annotate}"')
        try:
            api_call = clara_chatgpt4.call_chat_gpt4(annotation_prompt, config_info=config_info, callback=callback)
            api_calls += [ api_call ]
            if processing_phase != 'mwe':
                annotated_simplified_elements = parse_chatgpt_annotation_response(api_call.response, simplified_elements, processing_phase, callback=callback)
                nontrivial_annotated_elements = [ unsimplify_element(element, processing_phase) for element in annotated_simplified_elements ]
                annotated_elements = merge_elements_and_annotated_elements(elements, nontrivial_annotated_elements, processing_phase)
                return ( annotated_elements, api_calls )
            else:
                mwes = parse_chatgpt_annotation_response(api_call.response, simplified_elements, 'mwe', callback=callback)
                return ( mwes, api_calls )
        except ChatGPTError as e:
            post_task_update(callback, f'*** Warning: unable to parse response from ChatGPT-4')
            post_task_update(callback, e.message)
        except Exception as e:
            post_task_update(callback, f'*** Warning: error when sending request to ChatGPT-4')
            error_message = f'"{str(e)}"\n{traceback.format_exc()}'
            post_task_update(callback, error_message)

def merge_elements_and_annotated_elements(elements, annotated_elements, processing_phase):
    matcher = difflib.SequenceMatcher(None, 
        [element.content.strip() for element in elements], 
        [element.content.strip() for element in annotated_elements])

    # Add a placeholder annotation to all Word elements initially
    for element in elements:
        if element.type == "Word" and processing_phase not in element.annotations:
            element.annotations[processing_phase] = 'NO_ANNOTATION'

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            # If the contents match, we merge the annotations
            for i, j in zip(range(i1, i2), range(j1, j2)):
                elements[i].annotations.update(annotated_elements[j].annotations)
        elif tag == 'insert':
            # Handle insertions if necessary
            pass
        elif tag == 'delete':
            # Handle deletions if necessary
            pass
        elif tag == 'replace':
            # Handle replacements if necessary
            pass
    return elements

def segmentation_prompt(annotate_or_improve, text, l2_language):
    template, annotated_example_list = get_template_and_annotated_example_list(annotate_or_improve, 'segmented', l2_language)
    examples = segmentation_examples_to_text(annotated_example_list)
    return template.format( l2_language=l2_language,
                            examples=examples,
                            text=text )

def glossing_prompt(annotate_or_improve, simplified_elements_json, l1_language, l2_language, mwe=False, mwes=[]):
    template, annotated_example_list = get_template_and_annotated_example_list(annotate_or_improve,
                                                                               ( 'gloss' if not mwe else 'gloss_with_mwe' ),
                                                                               l2_language)
    if annotate_or_improve == 'annotate':
        examples = glossing_examples_to_examples_text(annotated_example_list, l1_language, l2_language, mwe=mwe, mwes=mwes)
    else:
        examples = reglossing_examples_to_examples_text(annotated_example_list, l1_language, l2_language, mwe=mwe, mwes=mwe)
    return template.format( l1_language=l1_language,
                            l2_language=l2_language,
                            examples=examples,
                            simplified_elements_json=simplified_elements_json
                            )

# We only have 'improvement' for 'lemma_and_gloss'
def joint_tagging_and_glossing_prompt(simplified_elements_json, l1_language, l2_language):
    template, annotated_example_list = get_template_and_annotated_example_list('improve', 'lemma_and_gloss', l2_language)
    examples = re_lemma_and_glossing_examples_to_examples_text(annotated_example_list, l1_language, l2_language)
    return template.format( l1_language=l1_language,
                            l2_language=l2_language,
                            examples=examples,
                            simplified_elements_json=simplified_elements_json
                            )

def tagging_prompt(annotate_or_improve, simplified_elements_json, l2_language, mwe=False, mwes=[]):
    l1_language = 'irrelevant'
    template, annotated_example_list = get_template_and_annotated_example_list(annotate_or_improve,
                                                                               ( 'lemma' if not mwe else 'lemma_with_mwe' ),
                                                                               l2_language)
    if annotate_or_improve == 'annotate':
        examples = tagging_examples_to_examples_text(annotated_example_list, l2_language, mwe=mwe, mwes=mwes)
    else:
        examples = retagging_examples_to_examples_text(annotated_example_list, l2_language, mwe=mwe, mwes=mwes)
    return template.format( l2_language=l2_language,
                            examples=examples,
                            simplified_elements_json=simplified_elements_json
                            )

def mwe_tagging_prompt(annotate_or_improve, simplified_elements_json, l2_language):
    l1_language = 'irrelevant'
    template, annotated_example_list = get_template_and_annotated_example_list(annotate_or_improve, 'mwe', l2_language)
    if annotate_or_improve == 'annotate':
        examples = mwe_tagging_examples_to_examples_text(annotated_example_list, l1_language, l2_language)
    else:
        examples = mwe_retagging_examples_to_examples_text(annotated_example_list, l1_language, l2_language)
    return template.format( l2_language=l2_language,
                            examples=examples,
                            simplified_elements_json=simplified_elements_json
                            )

def pinyin_tagging_prompt(annotate_or_improve, simplified_elements_json, l2_language):
    l1_language = 'irrelevant'
    template, annotated_example_list = get_template_and_annotated_example_list(annotate_or_improve, 'pinyin', l2_language)
    if annotate_or_improve == 'annotate':
        examples = pinyin_tagging_examples_to_examples_text(annotated_example_list, l1_language, l2_language)
    else:
        examples = pinyin_retagging_examples_to_examples_text(annotated_example_list, l1_language, l2_language)
    return template.format( l2_language=l2_language,
                            examples=examples,
                            simplified_elements_json=simplified_elements_json
                            )

def get_template_and_annotated_example_list(annotate_or_improve, annotation_type, l2_language):
    l2_language = l2_language.lower()
    try:
        return get_template_and_annotated_example_list_for_language(annotate_or_improve, annotation_type, l2_language)
    except TemplateError as e:
        if l2_language != 'default':
            print(f'--- Unable to find valid prompt template data for "{annotate_or_improve}", "{annotation_type}", "{l2_language}", using default')
            return get_template_and_annotated_example_list_for_language(annotate_or_improve, annotation_type, 'default')
        else:
            raise e

def get_template_and_annotated_example_list_for_language(annotate_or_improve, annotation_type, l2_language):
    prompt_repo = clara_prompt_templates.PromptTemplateRepository(l2_language)
    template = prompt_repo.load_template_or_examples('template', annotation_type, annotate_or_improve)
    annotated_example_list = prompt_repo.load_template_or_examples('examples', annotation_type, annotate_or_improve)
    clara_prompt_templates.check_validity_of_template_and_annotated_example_list(template, annotated_example_list, annotation_type)
    return ( template, annotated_example_list )

def segmentation_examples_to_text(examples):
    return '\n\n'.join([ segmentation_example_to_text(example) for example in examples ])

def segmentation_example_to_text(example):
    example_internalised = clara_internalise.internalize_text(example, 'l2_language', 'l1_language', 'segmented')
    elements = example_internalised.content_elements()
    plain_example = ''.join([ element.content for element in elements ])
    return f'{plain_example} ->\n{example}'

def glossing_examples_to_examples_text(examples_structure, l2_language, l1_language, mwe=False, mwes=[]):
    print(f'--- glossing_examples_to_examples_text({examples_structure}, {l2_language}, {l1_language}, mwe={mwe}, mwes={mwes})')
    # We aren't using MWEs at all
    if not mwe:
        return '\n\n'.join([ glossing_example_to_example_text(example, l2_language, l1_language) for example in examples_structure ])
    # We are using MWEs, but this particular text doesn't have any, so we use only examples with no MWEs
    elif not mwes:
        examples_to_use = [ example for example in examples_structure
                            if example[1].strip() == '' ]
        intro = 'Here are some examples:'
        examples_text = '\n\n'.join([ glossing_example_with_mwes_to_example_text(example, l2_language, l1_language) for example in examples_to_use ])
        return f'{intro}\n\n{examples_text}'
    # We are using MWEs, and this particular text has MWEs, so we use only examples with MWEs
    else:
        examples_to_use = [ example for example in examples_structure
                            if example[1].strip() != '' ]
        mwes_text = mwes_to_json_string(mwes)
        if len(mwes) == 1:
            intro1 = f'The following sequence of words should be treated as a single multi-word expression (MWE)'
        else:
            intro1 = f'The following sequences of words should be treated as single multi-word expressions (MWEs)'
        intro2 = f'This means that each of the component words in the MWE should be glossed in the same way. Here are some examples of how to gloss:'
        examples_text = '\n\n'.join([ glossing_example_with_mwes_to_example_text(example, l2_language, l1_language) for example in examples_to_use ])
        return f'{intro1}\n\n{mwes_text}\n\n{intro2}\n\n{examples_text}'

def tagging_examples_to_examples_text(examples_structure, l2_language, mwe=False, mwes=[]):
    print(f'--- tagging_examples_to_examples_text({examples_structure}, {l2_language}, mwe={mwe}, mwes={mwes})')
    # We aren't using MWEs at all
    if not mwe:
        return '\n\n'.join([ tagging_example_to_example_text(example, l2_language) for example in examples_structure ])
    # We are using MWEs, but this particular text doesn't have any, so we use only examples with no MWEs
    elif not mwes:
        examples_to_use = [ example for example in examples_structure
                            if example[1].strip() == '' ]
        intro = 'Here are some examples:'
        examples_text = '\n\n'.join([ tagging_example_with_mwes_to_example_text(example, l2_language) for example in examples_to_use ])
        return f'{intro}\n\n{examples_text}'
    # We are using MWEs, and this particular text has MWEs, so we use only examples with MWEs
    else:
        examples_to_use = [ example for example in examples_structure
                            if example[1].strip() != '' ]
        mwes_text = mwes_to_json_string(mwes)
        if len(mwes) == 1:
            intro1 = f'The following sequence of words should be treated as a single multi-word expression (MWE)'
        else:
            intro1 = f'The following sequences of words should be treated as single multi-word expressions (MWEs)'
        intro2 = f'This means that each of the component words in the MWE should be tagged in the same way. Here are some examples of how to gloss:'
        examples_text = '\n\n'.join([ tagging_example_with_mwes_to_example_text(example, l2_language) for example in examples_to_use ])
        return f'{intro1}\n\n{mwes_text}\n\n{intro2}\n\n{examples_text}'

##def tagging_examples_to_examples_text(examples_structure, l2_language, l1_language):
##    return '\nor\n'.join([ tagging_example_to_example_text(example, l2_language, l1_language) for example in examples_structure ])

def reglossing_examples_to_examples_text(examples_structure, l2_language, l1_language):
    return '\nor\n'.join([ reglossing_example_to_example_text(example, l2_language, l1_language) for example in examples_structure ])

def re_lemma_and_glossing_examples_to_examples_text(examples_structure, l1_language, l2_language):
    return '\nor\n'.join([ re_lemma_and_glossing_example_to_example_text(example, l2_language, l1_language) for example in examples_structure ])

def glossing_example_to_example_text(example, l2_language, l1_language):
    simplified_internalised_example = annotated_string_to_simplified_internalised_form(example, l2_language, l1_language, 'gloss')
    simplified_internalised_example_words = [ pair[0] for pair in simplified_internalised_example ]
    return f'Input: {json.dumps(simplified_internalised_example_words)}\nOutput: {json.dumps(simplified_internalised_example)}'

def glossing_example_with_mwes_to_example_text(example_pair, l2_language, l1_language):
    example, mwes = example_pair
    simplified_internalised_example = annotated_string_to_simplified_internalised_form(example, l2_language, l1_language, 'gloss')
    simplified_internalised_example_words = [ pair[0] for pair in simplified_internalised_example ]
    if not mwes.strip():
        return f'Input: {json.dumps(simplified_internalised_example_words)}\nOutput: {json.dumps(simplified_internalised_example)}'
    else:
        return f'Input: {json.dumps(simplified_internalised_example_words)}\nMWES:{json.dumps(mwes)}\nOutput: {json.dumps(simplified_internalised_example)}'

def tagging_example_with_mwes_to_example_text(example_pair, l2_language):
    example, mwes = example_pair
    l1_language = 'irrelevant'
    simplified_internalised_example = annotated_string_to_simplified_internalised_form(example, l2_language, l1_language, 'lemma')
    simplified_internalised_example_words = [ pair[0] for pair in simplified_internalised_example ]
    if not mwes.strip():
        return f'Input: {json.dumps(simplified_internalised_example_words)}\nOutput: {json.dumps(simplified_internalised_example)}'
    else:
        return f'Input: {json.dumps(simplified_internalised_example_words)}\nMWES:{json.dumps(mwes)}\nOutput: {json.dumps(simplified_internalised_example)}'

def mwes_to_json_string(mwes):
    return json.dumps(mwes)

def reglossing_example_to_example_text(example, l2_language, l1_language):
    ( first, second ) = example
    simplified_internalised_example1 = annotated_string_to_simplified_internalised_form(first, l2_language, l1_language, 'gloss')
    simplified_internalised_example2 = annotated_string_to_simplified_internalised_form(second, l2_language, l1_language, 'gloss')
    return f'{json.dumps(simplified_internalised_example1)} to {json.dumps(simplified_internalised_example2)}'

def re_lemma_and_glossing_example_to_example_text(example, l2_language, l1_language):
    ( first, second ) = example
    simplified_internalised_example1 = annotated_string_to_simplified_internalised_form(first, l2_language, l1_language, 'lemma_and_gloss')
    simplified_internalised_example2 = annotated_string_to_simplified_internalised_form(second, l2_language, l1_language, 'lemma_and_gloss')
    return f'{json.dumps(simplified_internalised_example1)} to {json.dumps(simplified_internalised_example2)}'

def mwe_tagging_examples_to_examples_text(examples_structure, l2_language, l1_language):
    print(f'MWE examples: {examples_structure}')
    return '\n\n'.join([ mwe_tagging_example_to_example_text(example, l2_language, l1_language) for example in examples_structure ])

def retagging_examples_to_examples_text(examples_structure, l2_language, l1_language):
    return '\nor\n'.join([ retagging_example_to_example_text(example, l2_language, l1_language) for example in examples_structure ])

def pinyin_tagging_examples_to_examples_text(examples_structure, l2_language, l1_language):
    return '\nor\n'.join([ pinyin_tagging_example_to_example_text(example, l2_language, l1_language) for example in examples_structure ])

def pinyin_retagging_examples_to_examples_text(examples_structure, l2_language, l1_language):
    return '\nor\n'.join([ pinyin_retagging_example_to_example_text(example, l2_language, l1_language) for example in examples_structure ])

def tagging_example_to_example_text(example, l2_language):
    l1_language = 'irrelevant'
    simplified_internalised_example = annotated_string_to_simplified_internalised_form(example, l2_language, l1_language, 'lemma')
    simplified_internalised_example_words = [ pair[0] for pair in simplified_internalised_example ]
    return f'{json.dumps(simplified_internalised_example_words)} as {json.dumps(simplified_internalised_example)}'

def mwe_tagging_example_to_example_text(mwe_example, l2_language, l1_language):
    # example_text is a string with the example
    # mwes_text is a comma-separated list of MWEs
    #
    # example_text =  "She must have thrown it out on Boxing Day morning.",
    # mwes_text = "thrown out, Boxing Day"
    # analysis = "- 'thrown out' is a form of a phrasal verb hence an MWE.
    #             'Boxing Day' is a set expression whose meaning is not deducible from its component words, hence an MWE'"
    example_text, mwes_text, analysis = mwe_example
    simplified_internalised_example_words = annotated_string_to_simplified_internalised_form(example_text, l2_language, l1_language, 'segmented')
    mwes = [ mwe.strip() for mwe in mwes_text.split(',') ]
    return f'Input: {json.dumps(simplified_internalised_example_words)}\nAnalysis: {analysis}\nOutput: {json.dumps(mwes)}'

def retagging_example_to_example_text(example, l2_language, l1_language):
    ( first, second ) = example
    simplified_internalised_example1 = annotated_string_to_simplified_internalised_form(first, l2_language, l1_language, 'lemma')
    simplified_internalised_example2 = annotated_string_to_simplified_internalised_form(second, l2_language, l1_language, 'lemma')
    return f'{json.dumps(simplified_internalised_example1)} to {json.dumps(simplified_internalised_example2)}'

def pinyin_tagging_example_to_example_text(example, l2_language, l1_language):
    simplified_internalised_example = annotated_string_to_simplified_internalised_form(example, l2_language, l1_language, 'pinyin')
    simplified_internalised_example_words = [ pair[0] for pair in simplified_internalised_example ]
    return f'{json.dumps(simplified_internalised_example_words)} as {json.dumps(simplified_internalised_example)}'

def pinyin_retagging_example_to_example_text(example, l2_language, l1_language):
    ( first, second ) = example
    simplified_internalised_example1 = annotated_string_to_simplified_internalised_form(first, l2_language, l1_language, 'pinyin')
    simplified_internalised_example2 = annotated_string_to_simplified_internalised_form(second, l2_language, l1_language, 'pinyin')
    return f'{json.dumps(simplified_internalised_example1)} to {json.dumps(simplified_internalised_example2)}'

def annotated_string_to_simplified_internalised_form(example, l2_language, l1_language, processing_phase):
    internalised_example = clara_internalise.internalize_text(example, l2_language, l1_language, processing_phase)
    elements = internalised_example.content_elements()
    if processing_phase == 'segmented':
        return [ element.content.strip() for element in elements
                 if element.type in ( 'Word', 'NonWordText' ) and element.content.strip() ]
    else:
        simplified_elements0 = [ simplify_element_to_list(element, processing_phase) for element in elements ]
        return [ element for element in simplified_elements0 if element != False ]

def simplify_element_to_string(element):
    content = element.content
    # Return Words as they are
    if element.type == 'Word':
        return content
    # Return NonWordText with the whitespace stripped off, if it's not all whitespace
    elif not content.isspace():
        return content.strip()
    # Discard whitespace strings
    else:
        return False

def simplify_element_to_list(element, processing_phase):
    content = element.content
    annotation = element.annotations[processing_phase] if processing_phase in element.annotations else 'NO_ANNOTATION'
    gloss = element.annotations['gloss'] if 'gloss' in element.annotations else 'NO_GLOSS'
    lemma = element.annotations['lemma'] if 'lemma' in element.annotations else 'NO_LEMMA'
    pos = element.annotations['pos'] if 'pos' in element.annotations else 'NO_POS'
    pinyin = element.annotations['pinyin'] if 'pinyin' in element.annotations else 'NO_PINYIN'
    # Return Words as they are
    if element.type == 'Word':
        if processing_phase == 'gloss':
            return [ content, gloss ]
        elif processing_phase == 'lemma':
            return [ content, lemma, pos ]
        elif processing_phase == 'pinyin':
            return [ content, pinyin ]
        else:
            return [ content, lemma, pos, gloss ]
            
    # Return NonWordText with the whitespace stripped off, if it's not all whitespace
    elif not content.isspace():
        content = content.strip()
        if processing_phase == 'gloss':
            return [ content, content ]
        elif processing_phase == 'pinyin':
            return [ content, content ]
        elif processing_phase == 'lemma':
            return [ content, content, 'PUNC' ]
        else:
            return [ content, content, 'PUNC', content ]
    # Discard whitespace strings
    else:
        return False

# element is
#     a two-item list consisting of content and annotation (gloss)
#     a three-item list consisting of content, annotation and pos (lemma)
#     a four-item list consisting of content, lemma, pos and gloss (lemma_and_gloss)
# Return a ContentElement object with the content and annotation in the right places.
def unsimplify_element(element, processing_phase):
    if processing_phase in ( 'gloss', 'pinyin' ) and len(element) == 2:
        content, annotation = element
        # String only consists of punctuation marks
        if all(regex.match(r"\p{P}", c) for c in content):
            return ContentElement("NonWordText", content)
        # String is an HTML tag
        elif regex.match(r"<\/?\w+>", content):
            return ContentElement("Markup", content)
        else:
            return ContentElement("Word", content, annotations={ processing_phase: annotation })
    elif processing_phase == 'lemma' and len(element) == 3:
        content, lemma, pos = element
        # String only consists of punctuation marks
        if all(regex.match(r"\p{P}", c) for c in content):
            return ContentElement("NonWordText", content)
        # String is an HTML tag
        elif regex.match(r"<\/?\w+>", content):
            return ContentElement("Markup", content)
        else:
            return ContentElement("Word", content, annotations={ 'lemma': lemma, 'pos': pos })
    elif processing_phase == 'lemma_and_gloss' and len(element) == 4:
        content, lemma, pos, gloss = element
        # String only consists of punctuation marks
        if all(regex.match(r"\p{P}", c) for c in content):
            return ContentElement("NonWordText", content)
        # String is an HTML tag
        elif regex.match(r"<\/?\w+>", content):
            return ContentElement("Markup", content)
        else:
            return ContentElement("Word", content, annotations={ 'lemma': lemma, 'pos': pos, 'gloss': gloss })
    else:
        raise InternalCLARAError(message = f'Bad call: unsimplify_element({element}, {processing_phase})')

##def parse_chatgpt_annotation_response(response, simplified_elements, processing_phase, callback=None):
##    response_object = clara_chatgpt4.interpret_chat_gpt4_response_as_json(response, object_type='list', callback=callback)
##    if not isinstance(response_object, list):
##        raise ChatGPTError(message = f'Response is not a list: {response}')
##    
##    usable_response_object = []
##    for element in response_object:
##        if not well_formed_element_in_annotation_response(element, processing_phase):
##            post_task_update(callback, f'*** Warning: bad element {element} in annotation response, discarding')
##        else:
##            usable_response_object += [ element ]
##    if processing_phase != 'mwe':
##        original_text = ' '.join([ element if isinstance(element, str) else element[0] for element in simplified_elements ])
##        annotated_text = ' '.join([ element[0] for element in usable_response_object ])
##        if not original_text == annotated_text:
##            warning = f"""*** Warning: original text and annotated text are different.
##     Original text: {original_text}
##    Annotated text: {annotated_text}"""
##            post_task_update(callback, warning)
##        return usable_response_object
##    else:
##        return [ element.split() for element in usable_response_object ]

def parse_chatgpt_annotation_response(response, simplified_elements, processing_phase, callback=None):
    analysis = ""
    mwes = []

    if processing_phase == 'mwe':
        # Extract the analysis text and the JSON list separately
        analysis_marker = "Analysis:"
        json_marker = "Output"

        analysis_start = response.find(analysis_marker)
        json_start = response.find(json_marker)

        if analysis_start != -1 and json_start != -1:
            analysis = response[analysis_start + len(analysis_marker):json_start].strip()
            json_str = response[json_start + len(json_marker):].strip()

            # Extract the JSON content
            response_object = clara_chatgpt4.interpret_chat_gpt4_response_as_json(json_str, object_type='list', callback=callback)
            if isinstance(response_object, list):
                mwes = [element.split() for element in response_object]
            else:
                raise ChatGPTError(message=f'Response is not a list: {response}')
        else:
            raise ChatGPTError(message="Could not find the markers for analysis and JSON output in the response.")
        
        # Return a structure containing both the analysis and the list of MWEs
        return {'analysis': analysis, 'mwes': mwes}

    else:
        # Handle other processing phases (non-MWE)
        response_object = clara_chatgpt4.interpret_chat_gpt4_response_as_json(response, object_type='list', callback=callback)
        if not isinstance(response_object, list):
            raise ChatGPTError(message=f'Response is not a list: {response}')

        usable_response_object = []
        for element in response_object:
            if not well_formed_element_in_annotation_response(element, processing_phase):
                post_task_update(callback, f'*** Warning: bad element {element} in annotation response, discarding')
            else:
                usable_response_object.append(element)

        original_text = ' '.join([element if isinstance(element, str) else element[0] for element in simplified_elements])
        annotated_text = ' '.join([element[0] for element in usable_response_object])
        if original_text != annotated_text:
            warning = f"""*** Warning: original text and annotated text are different.
     Original text: {original_text}
    Annotated text: {annotated_text}"""
            post_task_update(callback, warning)

        return usable_response_object


def simplified_element_list_to_text(simplified_elements):
    return ' '.join([ element if isinstance(element, str) else element[0]
                      for element in simplified_elements ])

def well_formed_element_in_annotation_response(element, processing_phase):
    if processing_phase in ( 'gloss', 'pinyin' ):
        return isinstance(element, list) and len(element) == 2
    elif processing_phase == 'lemma':
        return isinstance(element, list) and len(element) == 3
    elif processing_phase == 'lemma_and_gloss':
        return isinstance(element, list) and len(element) == 4
    elif processing_phase == 'mwe':
        return isinstance(element, str) 

