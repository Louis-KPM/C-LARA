
from .clara_phonetic_lexicon_repository import PhoneticLexiconRepository
from .clara_classes import InternalCLARAError
from .clara_utils import local_file_exists, read_local_json_file, post_task_update, merge_dicts

### Temporary
##def grapheme_phoneme_alignment_available(l2):
##    return l2 in _plain_lexicon_files and l2 in _aligned_lexicon_files
##
### Temporary
##def load_grapheme_phoneme_lexical_resources(l2):
##    load_plain_grapheme_phoneme_lexicon(l2)
##    load_aligned_grapheme_phoneme_lexicon(l2)
##
### Temporary
##_plain_grapheme_phoneme_dicts = {}
##
### Temporary
##_aligned_grapheme_phoneme_dicts = {}
##
### Temporary
##_internalised_aligned_grapheme_phoneme_dicts = {}
##
### Temporary
##_plain_lexicon_files = { 'english': '$CLARA/linguistic_data/english/en_UK_pronunciation_dict.json',
##                         'french': '$CLARA/linguistic_data/french/fr_FR_pronunciation_dict.json' }
##
### Temporary
##_aligned_lexicon_files = { 'english': '$CLARA/linguistic_data/english/en_UK_pronunciation_dict_aligned.json',
##                           'french': '$CLARA/linguistic_data/french/fr_FR_pronunciation_dict_aligned.json' }
##
### Temporary
##def load_plain_grapheme_phoneme_lexicon(l2):
##    if l2 in _plain_grapheme_phoneme_dicts:
##        return
##    
##    _plain_grapheme_phoneme_dicts[l2] = read_local_json_file(_plain_lexicon_files[l2])
##
### Temporary
##def load_aligned_grapheme_phoneme_lexicon(l2):
##    if l2 in _internalised_aligned_grapheme_phoneme_dicts:
##        return
##    
##    _aligned_grapheme_phoneme_dicts[l2] = read_local_json_file(_aligned_lexicon_files[l2])
##    Data =  _aligned_grapheme_phoneme_dicts[l2]
##    internalised_aligned_lexicon, count = internalise_aligned_grapheme_phoneme_lexicon(Data, l2)
##    _internalised_aligned_grapheme_phoneme_dicts[l2] = internalised_aligned_lexicon
##    print(f'--- Loaded internalised aligned {l2} lexicon, {count} different letter/phoneme correspondences')
##
### Temporary
##def get_phonetic_representation_for_word(word, l2):
##    if l2 in _plain_grapheme_phoneme_dicts and word in _plain_grapheme_phoneme_dicts[l2]:
##        return remove_accents_from_phonetic_string(_plain_grapheme_phoneme_dicts[l2][word])
##    else:
##        return None
##
### Temporary
##def grapheme_phoneme_alignments_for_key(key, l2):
##    if l2 in _internalised_aligned_grapheme_phoneme_dicts and key in _internalised_aligned_grapheme_phoneme_dicts[l2]:
##        return _internalised_aligned_grapheme_phoneme_dicts[l2][key]
##    else:
##        return []

def grapheme_phoneme_resources_available(l2):
    repository = PhoneticLexiconRepository()
    return repository.aligned_entries_exist_for_language(l2)

def get_phonetic_lexicon_resources_for_words_and_l2(words, l2, callback=None):
    plain_entries = get_plain_entries_for_words(words, l2, callback=callback)
    aligned_entries = get_aligned_entries_for_words(words, l2, callback=callback)
    internalised_aligned_lexicon = get_internalised_aligned_grapheme_phoneme_lexicon(l2, callback=callback)
    return { 'plain_lexicon_entries': plain_entries,
             'aligned_lexicon_entries': aligned_entries,
             'internalised_aligned_lexicon': internalised_aligned_lexicon }

def add_plain_entries_to_resources(resources, new_plain_entries):
    return { 'plain_lexicon_entries': merge_dicts(resources['plain_lexicon_entries'], new_plain_entries),
             'aligned_lexicon_entries': resources['aligned_lexicon_entries'],
             'internalised_aligned_lexicon': resources['internalised_aligned_lexicon'] }

def get_plain_entries_for_words(words, l2, callback=None):
    repository = PhoneticLexiconRepository()
    plain_entries = repository.get_plain_entries_batch(words, l2, callback=callback)
    data = { plain_entry['word']: plain_entry['phonemes']
             for plain_entry in plain_entries
             if plain_entry['status'] != 'generated' }
    post_task_update(callback, f'--- Found {len(data)} plain {l2} lexicon entries ({len(words)} words submitted)')
    return data

def get_aligned_entries_for_words(words, l2, callback=None):
    repository = PhoneticLexiconRepository()
    aligned_entries = repository.get_aligned_entries_batch(words, l2, callback=callback)
    data = { aligned_entry['word']: ( aligned_entry['aligned_graphemes'], aligned_entry['aligned_phonemes'] )
             for aligned_entry in aligned_entries
             if aligned_entry['status'] != 'generated' }
    post_task_update(callback, f'--- Found {len(data)} aligned {l2} lexicon entries ({len(words)} words submitted)')
    return data

def get_internalised_aligned_grapheme_phoneme_lexicon(l2, callback=None):
    repository = PhoneticLexiconRepository()
    aligned_entries = repository.get_all_aligned_entries_for_language(l2, callback=callback)
    data = { aligned_entry['word']: ( aligned_entry['aligned_graphemes'], aligned_entry['aligned_phonemes'] )
             for aligned_entry in aligned_entries
             if aligned_entry['status'] != 'generated' }
    internalised_lexicon, count = internalise_aligned_grapheme_phoneme_lexicon(data, l2)
    post_task_update(callback, f'--- Created internalised aligned {l2} lexicon, {count} different letter/phoneme correspondences')
    return internalised_lexicon

def get_phonetic_representation_for_word_and_resources(word, resources):
    if 'plain_lexicon_entries' in resources and word in resources['plain_lexicon_entries']:
        return remove_accents_from_phonetic_string(resources['plain_lexicon_entries'][word])
    else:
        return None

def get_aligned_entry_for_word_and_resources(word, resources):
    if 'aligned_lexicon_entries' in resources and word in resources['aligned_lexicon_entries']:
        return resources['aligned_lexicon_entries'][word]
    else:
        return None

def get_grapheme_phoneme_alignments_for_key_and_resources(key, resources):
    if 'internalised_aligned_lexicon' in resources and key in resources['internalised_aligned_lexicon']:
        return resources['internalised_aligned_lexicon'][key]
    else:
        return []

def internalise_aligned_grapheme_phoneme_lexicon(Data, l2):
    internalised_aligned_lexicon = {}
    Count = 0
    for Word in Data:
        Value = Data[Word]
        if not isinstance(Value, ( list, tuple )) or not len(Value) == 2 or not isinstance(Value[0], str) or not isinstance(Value[1], str):
            print(f'*** Warning: bad entry for "{Word}" in aligned {l2} lexicon, not a pair')
        ( Letters, Phonemes0 ) = Value
        Phonemes = remove_accents_from_phonetic_string(Phonemes0)
        ( LetterComponents, PhonemeComponents ) = ( Letters.split('|'), Phonemes.split('|') )
        if not len(LetterComponents) == len(PhonemeComponents):
            print(f'*** Warning: bad entry for "{Word}" in aligned {l2} lexicon, not aligned')
        for ( LetterGroup, PhonemeGroup ) in zip( LetterComponents, PhonemeComponents ):
            Key = ( '' if LetterGroup == '' else LetterGroup[0], '' if PhonemeGroup == '' else PhonemeGroup[0] )
            Current = internalised_aligned_lexicon[Key] if Key in internalised_aligned_lexicon else []
            Correspondence = ( LetterGroup, PhonemeGroup )
            if not Correspondence in Current:
                internalised_aligned_lexicon[Key] = Current + [ Correspondence ]
                Count += 1
    return ( internalised_aligned_lexicon, Count )
    

def remove_accents_from_phonetic_string(Str):
    return Str.replace('ˈ', '').replace('ˌ', '').replace('.', '').replace('\u200d', '')
