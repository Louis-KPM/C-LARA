"""
This module defines the following classes to represent a text and its components:

1. ContentElement: Represents a single content element, such as a word or a punctuation mark.
2. Segment: Represents a segment of text, containing a list of ContentElements.
3. Page: Represents a page of text, containing a list of Segments.
4. Text: Represents a full text, containing a list of Pages and metadata about the text, such as L1 and L2 languages.

Each class also includes methods to convert the objects to and from JSON and plain text formats.

It also defines the following classes:

5. APICall, which represents an API call to gpt-4
6. DiffElement, which is used when constructing a smart diff of two texts

7. Various kinds of exceptions
"""

import json

class ContentElement:
    def __init__(self, element_type, content, annotations=None):
        self.type = element_type
        self.content = content
        self.annotations = annotations if annotations else {}

    def to_text(self, annotation_type=None):
        def escape_special_chars(text):
            return text.replace("#", r"\#").replace("@", r"\@").replace("<", r"\<").replace(">", r"\>")

        # If a Word element contains spaces, we need to add @ signs around it for the annotated text to be well-formed
        def put_at_signs_around_text_if_necessary(text, annotation_type):
            if ' ' in text and annotation_type in ( 'segmented', 'gloss', 'lemma' ):
                return f'@{text}@'
            else:
                return text
        
        if self.type == "Word":
            escaped_content = escape_special_chars(self.content)
            escaped_content = put_at_signs_around_text_if_necessary(escaped_content, annotation_type)
            annotations = self.annotations
            # For texts tagged with lemma, POS and gloss, we have the special notation Word#Lemma/POS/Gloss#
            if annotation_type == 'lemma_and_gloss':
                gloss = annotations['gloss'] if 'gloss' in annotations else 'NO_GLOSS'
                lemma = annotations['lemma'] if 'lemma' in annotations else 'NO_LEMMA'
                pos = annotations['pos'] if 'pos' in annotations else 'NO_POS'
                escaped_lemma = escape_special_chars(lemma)
                escaped_gloss = escape_special_chars(gloss)
                return f"{escaped_content}#{escaped_lemma}/{pos}/{escaped_gloss}#"
            # For lemma-tagged texts, we have the special notation Word#Lemma/POS# for words with POS tags as well
            elif annotation_type == 'lemma' and 'lemma' in annotations and 'pos' in annotations:
                lemma, pos = ( annotations['lemma'], annotations['pos'] )
                escaped_lemma = escape_special_chars(lemma)
                return f"{escaped_content}#{escaped_lemma}/{pos}#"
            elif annotation_type and annotation_type in annotations:
                escaped_annotation = escape_special_chars(annotations[annotation_type])
                return f"{escaped_content}#{escaped_annotation}#"
            elif annotation_type:
                return f"{escaped_content}#-#"
            else:
                return escaped_content
        else:
            return self.content

    def word_count(self):
        return 1 if self.type == "Word" else 0
        
class Segment:
    def __init__(self, content_elements, annotations=None):
        self.content_elements = content_elements
        self.annotations = annotations or {}

    def to_text(self, annotation_type=None):
        out_text = ''
        last_type = None
        for element in self.content_elements:
            this_type = element.type
            # When producing 'segmented' text, we need to add | markers between continuous Words.
            if annotation_type == 'segmented' and this_type == 'Word' and last_type == 'Word':
                out_text += '|'
            out_text += element.to_text(annotation_type)
            last_type = this_type
        return out_text

    def add_annotation(self, annotation_type, annotation_value):
        self.annotations[annotation_type] = annotation_value

    def word_count(self):
        return sum([ element.word_count() for element in self.content_elements ])

class Page:
    def __init__(self, segments, annotations=None):
        self.segments = segments
        self.annotations = annotations or {}  # This could contain 'img', 'page_number', and 'position'

    def content_elements(self):
        elements = []
        for segment in self.segments:
            elements.extend(segment.content_elements)
        return elements

##    def to_text(self, annotation_type=None):
##        return "||".join([segment.to_text(annotation_type) for segment in self.segments])

    def to_text(self, annotation_type=None):
        segment_texts = "||".join([segment.to_text(annotation_type) for segment in self.segments])
        if self.annotations:
            attributes_str = ' '.join([f"{key}='{value}'" for key, value in self.annotations.items()])
            return f"<page {attributes_str}>\n{segment_texts}"
        else:
            return f"<page>\n{segment_texts}"

    def word_count(self):
        return sum([ segment.word_count() for segment in self.segments ])

    @classmethod
    def from_json(cls, json_str):
        page_dict = json.loads(json_str)
        segments = []
        for segment_dict in page_dict["segments"]:
            content_elements = []
            for element_dict in segment_dict["content_elements"]:
                content_element = ContentElement(
                    element_type=element_dict["type"],
                    content=element_dict["content"],
                    annotations=element_dict["annotations"],
                )
                content_elements.append(content_element)
            segment = Segment(content_elements)
            segments.append(segment)
        return cls(segments)

    def to_json(self):
        page_json = {"segments": []}
        for segment in self.segments:
            segment_json = {"content_elements": []}
            for element in segment.content_elements:
                content_element_json = {
                    "type": element.type,
                    "content": element.content,
                    "annotations": element.annotations,
                }
                segment_json["content_elements"].append(content_element_json)
            page_json["segments"].append(segment_json)
        return json.dumps(page_json)

class Text:
    def __init__(self, pages, l2_language, l1_language, annotations=None, voice=None):
        self.l2_language = l2_language
        self.l1_language = l1_language
        self.pages = pages
        self.annotations = annotations or {}
        self.voice = voice

    def content_elements(self):
        elements = []
        for page in self.pages:
            elements.extend(page.content_elements())
        return elements
    
    def word_count(self):
        return sum([ page.word_count() for page in self.pages ])

    def add_page(self, page):
        self.pages.append(page)

##    def to_text(self, annotation_type=None):
##        return "\n<page>\n".join([page.to_text(annotation_type) for page in self.pages])

    def to_text(self, annotation_type=None):
        return "\n".join([page.to_text(annotation_type) for page in self.pages])

    def to_json(self):
        json_list = [json.loads(page.to_json()) for page in self.pages]
        return json.dumps({
            "l2_language": self.l2_language,
            "l1_language": self.l1_language,
            "pages": json_list
        })

    def add_to_end_of_last_segment(self, content_element):
        if not self.pages:
            # If there are no pages, create a new one with an empty segment
            new_page = Page([Segment([])])
            self.pages.append(new_page)
        
        last_page = self.pages[-1]
        if not last_page.segments:
            # If the last page has no segments, add an empty one
            last_page.segments.append(Segment([]))
        
        last_segment = last_page.segments[-1]
        last_segment.content_elements.append(content_element)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        text = cls(l2_language=data["l2_language"], l1_language=data["l1_language"])
        text.pages = [Page.from_json(page_json) for page_json in data["pages"]]
        return text

class Image:
    def __init__(self, image_file_path, image_name, associated_text, associated_areas, page, position):
        self.image_file_path = image_file_path
        self.image_name = image_name
        self.associated_text = associated_text
        self.associated_areas = associated_areas
        self.page = page
        self.position = position

    def __repr__(self):
        return f"Image(image_file_path={self.image_file_path}, image_name={self.image_name})"

class APICall:
    def __init__(self, prompt, response, cost, duration, timestamp, retries):
        self.prompt = prompt
        self.response = response
        self.cost = cost
        self.duration = duration
        self.timestamp = timestamp
        self.retries = retries

class DiffElement:
    def __init__(self, type, content = '', annotations = {}):
        self.type = type
        self.content = content
        self.annotations = annotations

class InternalCLARAError(Exception):
    def __init__(self, message = 'Internal CLARA error'):
        self.message = message

class InternalisationError(Exception):
    def __init__(self, message = 'Internalisation error'):
        self.message = message

class TemplateError(Exception):
    def __init__(self, message = 'Template error'):
        self.message = message

class ChatGPTError(Exception):
    def __init__(self, message = 'ChatGPT error'):
        self.message = message

class TreeTaggerError(Exception):
    def __init__(self, message = 'TreeTagger error'):
        self.message = message
