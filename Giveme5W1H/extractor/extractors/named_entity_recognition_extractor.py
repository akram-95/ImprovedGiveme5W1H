from stanza.server import CoreNLPClient

from Giveme5W1H.extractor.document import Document
from Giveme5W1H.extractor.extractors.abs_extractor import AbsExtractor


class NamedEntityRecognitionExtractor(AbsExtractor):
    def _evaluate_candidates(self, document):
        pass

    def _extract_candidates(self, document):
        document.set_answer('money', self.getMoney(document))
        document.set_answer('location', self.getLocation(document))
        pass

    cnlClient: CoreNLPClient = None
    document: Document = None

    def __init__(self, client: CoreNLPClient):
        self.cnlClient = client
        self.document = Document()

    def setDocument(self, document: Document):
        self.document = document

    def getMoney(self, document):
        money_pattern = '[{ner:"MONEY"}]+'
        matches = self.cnlClient.tokensregex(document.get_raw()['title'],
                                             money_pattern)
        sentences = matches['sentences']
        result = []

        for sentence in enumerate(sentences):
            for key in sentence[1]:
                if key != 'length':
                    text = sentence[1][str(key)]['text']
                    result.append(text)

        return result

    def getMoney_raw(self, document):
        money_pattern = '[{ner:"MONEY"}]+'
        matches = self.cnlClient.tokensregex(document.get_raw()['title'],
                                             money_pattern)
        sentences = matches['sentences']
        return sentences

    def getLocation(self, document):
        location_pattern = '[{ner:"CITY"} | {ner:"STATE_OR_PROVINCE"} | {ner:"LOCATION"} | {ner:"COUNTRY"}]+'
        matches = self.cnlClient.tokensregex(document.get_raw()['title'],
                                             location_pattern)
        sentences = matches['sentences']
        result = []
        for sentence in enumerate(sentences):
            for key in sentence[1]:
                if key != 'length':
                    text = sentence[1][str(key)]['text']
                    result.append(text)

        return result

    def getLocation_raw(self, document):
        location_pattern = '[{ner:"CITY"} | {ner:"STATE_OR_PROVINCE"} | {ner:"LOCATION"} | {ner:"COUNTRY"}]+'
        matches = self.cnlClient.tokensregex(document.get_raw()['title'],
                                             location_pattern)
        sentences = matches['sentences']
        return sentences

    def getNERByPattern(self, document, pattern):
        matches = self.cnlClient.tokensregex(document.get_raw()['title'],
                                             pattern)
        sentences = matches['sentences']
        result = []

        for sentence in enumerate(sentences):
            for key in sentence[1]:
                if key != 'length':
                    text = sentence[1][str(key)]['text']
                    result.append(text)

        return result

    def getNERByPattern_raw(self, document, pattern):
        matches = self.cnlClient.tokensregex(document.get_raw()['title'],
                                             pattern)
        sentences = matches['sentences']
        return sentences
