from stanza.server import CoreNLPClient

from Giveme5W1H.extractor.document import Document


class NamedEntityRecognition:
    cnlClient: CoreNLPClient = None
    document: Document = None

    def __init__(self, client: CoreNLPClient):
        self.cnlClient = client
        self.document = Document()

    def setDocument(self, document: Document):
        self.document = document

    def getMoney(self):
        money_pattern = '[{ner:"MONEY"}]+'
        matches = self.cnlClient.tokensregex(self.document.get_raw()['title'],
                                             money_pattern)
        sentences = matches['sentences']
        result = []

        for sentence in enumerate(sentences):
            for key in sentence[1]:
                if key != 'length':
                    text = sentence[1][str(key)]['text']
                    result.append(text)

        return result

    def getMoney_raw(self):
        money_pattern = '[{ner:"MONEY"}]+'
        matches = self.cnlClient.tokensregex(self.document.get_raw()['title'],
                                             money_pattern)
        sentences = matches['sentences']
        return sentences

    def getLocation(self):
        location_pattern = '[{ner:"CITY"} | {ner:"STATE_OR_PROVINCE"} | {ner:"LOCATION"} | {ner:"COUNTRY"}]+'
        matches = self.cnlClient.tokensregex(self.document.get_raw()['title'],
                                             location_pattern)
        sentences = matches['sentences']
        result = []
        for sentence in enumerate(sentences):
            for key in sentence[1]:
                if key != 'length':
                    text = sentence[1][str(key)]['text']
                    result.append(text)

        return result

    def getLocation_raw(self):
        location_pattern = '[{ner:"CITY"} | {ner:"STATE_OR_PROVINCE"} | {ner:"LOCATION"} | {ner:"COUNTRY"}]+'
        matches = self.cnlClient.tokensregex(self.document.get_raw()['title'],
                                             location_pattern)
        sentences = matches['sentences']
        return sentences

    def getNERByPattern(self, pattern):
        matches = self.cnlClient.tokensregex(self.document.get_raw()['title'],
                                             pattern)
        sentences = matches['sentences']
        result = []

        for sentence in enumerate(sentences):
            for key in sentence[1]:
                if key != 'length':
                    text = sentence[1][str(key)]['text']
                    result.append(text)

        return result

    def getNERByPattern_raw(self, pattern):
        matches = self.cnlClient.tokensregex(self.document.get_raw()['title'],
                                             pattern)
        sentences = matches['sentences']
        return sentences
