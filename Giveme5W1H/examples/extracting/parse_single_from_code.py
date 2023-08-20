import logging

from Giveme5W1H.extractor.document import Document
from Giveme5W1H.extractor.extractor import MasterExtractor
from Giveme5W1H.extractor.extractors.named_entity_recognition_extractor import NamedEntityRecognitionExtractor

"""
This is a simple example how to use the extractor in combination with a dict in news-please format.

- Nothing is cached

"""

# don`t forget to start up core_nlp_host
# giveme5w1h-corenlp

titleshort = "The Islamic Republic is shooting at people from inside the Morodesh Mosque"
date_publish = '2016-11-10 07:44:00'

if __name__ == '__main__':
    # logger setup
    log = logging.getLogger('GiveMe5W')
    log.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    log.addHandler(sh)

    # giveme5w setup - with defaults
    extractor = MasterExtractor()

    doc = Document.from_text(titleshort, date_publish)
    doc = Document(titleshort, titleshort, '', date_publish)

    doc = extractor.parse(doc)
    location_pattern = '[{ner:"CITY"} | {ner:"STATE_OR_PROVINCE"} | {ner:"LOCATION"} | {ner:"COUNTRY"}]+'
    named_entity_recognition_extractor = next(
        x for x in extractor.extractors if isinstance(x, NamedEntityRecognitionExtractor))

    top_who_answer = doc.get_top_answer('who').get_parts_as_text()
    top_what_answer = doc.get_top_answer('what').get_parts_as_text()
    # top_when_answer = doc.get_top_answer('when').get_parts_as_text()
    # top_where_answer = doc.get_top_answer('where').get_parts_as_text()
    # top_why_answer = doc.get_top_answer('why').get_parts_as_text()
    # top_how_answer = doc.get_top_answer('how').get_parts_as_text()
    # top_location_answer = doc.get_top_answers('location')

    print(top_who_answer)
    print(top_what_answer)
    # print(top_when_answer)
    # print(top_where_answer)
    # print(top_why_answer)
    # print(top_how_answer)
    # print(top_location_answer)
    # print(named_entity_recognition_extractor.getNERByPattern_raw(doc, location_pattern))
