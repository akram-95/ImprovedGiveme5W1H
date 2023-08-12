import logging
import os
import socket

from flask import Flask, request, jsonify
from jinja2 import Environment, PackageLoader, select_autoescape

from Giveme5W1H.extractor.document import Document
from Giveme5W1H.extractor.extractor import MasterExtractor
from Giveme5W1H.extractor.tools.file.reader import Reader
from Giveme5W1H.extractor.tools.file.writer import Writer

"""
This is a simple example on how to use flask to create a rest api for our extractor.

Please update the CoreNLP address to match your host and check the flask settings.
"""


# helper to find own ip address
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


# Flask setup
app = Flask(__name__)
log = logging.getLogger(__name__)
host = get_ip()
port = 9099
debug = False

# Template engine
env = Environment(
    loader=PackageLoader('Giveme5W1H.examples', 'extracting'),
    autoescape=select_autoescape(['html', 'xml'])
)

template_index = env.from_string(open(os.path.join(os.path.dirname(__file__), 'index.html')).read())
template_index_doubled = env.from_string(open(os.path.join(os.path.dirname(__file__), 'index_doubled.html')).read())
extractor = MasterExtractor()
reader = Reader()
writer = Writer()


def get_mainpage():
    return template_index.render()


@app.route('/', methods=['GET'])
def root():
    return get_mainpage()


def request_to_document():
    document = None
    if request.method == 'POST':
        data = request.get_json(force=True)
        document = reader.parse_newsplease(data, 'Server')
    elif request.method == 'GET':
        # either
        full_text = request.args.get('fulltext', '')
        # or
        title = request.args.get('title', '')
        description = request.args.get('description', '')
        text = request.args.get('text', '')
        # and always
        date = request.args.get('date', None)

        if full_text:
            document = Document.from_text(full_text, date=date)
        elif title:
            log.debug("retrieved raw article for extraction: %s", title)
            document = Document(title, description, text, date=date)
        else:
            log.error("Retrieved data does not contain title or full_text. One of them is required.")
            return None

    return document


def request_to_document_doubled():
    document = None
    if request.method == 'POST':
        body = request.get_json()
        data = body["data"]
        date = body["publish_date"]

        if data:
            document = Document(data, data, '', date=date)
        else:
            log.error("Retrieved data does not contain data. it is required.")
            return None
    return document


@app.route('/extract', methods=['POST'])
def extract():
    document = request_to_document()
    if document:
        document = extractor.parse(document)
        top_who = ''
        top_why = ''
        top_what = ''
        top_where = ''
        top_when = ''
        top_how = ''
        try:
            top_who = document.get_top_answer('who').get_parts_as_text()
        except:
            pass
        try:
            top_why = document.get_top_answer('why').get_parts_as_text()
        except:
            pass
        try:
            top_what = document.get_top_answer('what').get_parts_as_text()
        except:
            pass
        try:
            top_where = document.get_top_answer('where').get_parts_as_text()
        except:
            pass
        try:
            top_when = document.get_top_answer('when').get_parts_as_text()
        except:
            pass

        try:
            top_how = document.get_top_answer('how').get_parts_as_text()
        except:
            pass

        return {'who': top_who, 'where': top_where, 'why': top_why, 'when': top_when, 'what': top_what, 'how': top_how}
    else:
        return "Record not found", 400


@app.route('/extract-doubled', methods=['GET'])
def extract_doubled():
    return get_mainPageDoubled()


def get_mainPageDoubled():
    return template_index_doubled.render()


@app.route('/extract-doubled', methods=['POST'])
def extract_doubled_post():
    document = request_to_document_doubled()
    if document:
        document = extractor.parse(document)
        top_who = ''
        top_why = ''
        top_what = ''
        top_where = ''
        top_when = ''
        top_how = ''
        try:
            top_who = document.get_top_answer('who').get_parts_as_text()
        except:
            pass
        try:
            top_why = document.get_top_answer('why').get_parts_as_text()
        except:
            pass
        try:
            top_what = document.get_top_answer('what').get_parts_as_text()
        except:
            pass
        try:
            top_where = document.get_top_answer('where').get_parts_as_text()
        except:
            pass
        try:
            top_when = document.get_top_answer('when').get_parts_as_text()
        except:
            pass

        try:
            top_how = document.get_top_answer('how').get_parts_as_text()
        except:
            pass

        return {'who': top_who, 'where': top_where, 'why': top_why, 'when': top_when, 'what': top_what, 'how': top_how}
    else:
        return "Record not found", 400


def main():
    log.info("starting server on port %i", port)
    app.run(host, port, debug)

    log.info("server has stopped")


if __name__ == "__main__":
    main()
