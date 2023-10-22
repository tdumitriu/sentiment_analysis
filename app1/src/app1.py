from __future__ import unicode_literals, print_function

from flask import Flask, request, jsonify
from spacy.lang.en import English
import requests
import logging
import config
import time

from work import app1_work

logging.basicConfig(filename=config.LOGFILE_APP1,
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)
app.config.from_object(config)
logging.info("app1 has been started")


#######################################################
# SERVER 1
#######################################################

#
# Route that returns info about service
#
@app.route('/', methods=['GET'])
def info():
    app.config.from_object(config)
    app.logger.debug("app1 UP and RUNNING")

    return "APP1 is UP and RUNNING\n"


#
# Route providing status information for heartbeat monitoring
#
@app.route('/status', methods=['GET'])
def status():
    app.logger.debug("STATUS: ok")
    response = jsonify(
        {"status": "ok"}
    )

    response.headers["Content-Type"] = "application/json"
    return response


#
# Main process that implements the following tasks:
# - loads a paragraph from an uploaded json or from an uploaded binary
# - tokenizes the paragraph into a list of sentences
# - for each sentence calls the service that returns the sentiment of sentences
# - builds the final response assembling the sentences and their sentiments
#
@app.route('/process', methods=['POST'])
def process():
    nlp = English()
    nlp.add_pipe("sentencizer")
    content_type = request.headers.get('Content-Type')

    # processes the loaded json
    if content_type == 'application/json':
        data = request.json
        logging.debug(data.get('id'))
        logging.debug(data.get('text'))

        try:
            doc = nlp(data.get('text'))
            sentence_sentiment_list = get_sentence_sentiments(doc)

            return jsonify(sentence_sentiment_list)
        except requests.exceptions.RequestException as err:
            return err
    # processes the loaded binary
    elif content_type == 'text/html':
        data = request.data.decode("utf-8")
        logging.debug(data)

        try:
            doc = nlp(data)
            sentence_sentiment_list = get_sentence_sentiments(doc)

            return jsonify(sentence_sentiment_list)
        except requests.exceptions.RequestException as err:
            return err
    else:
        return "Content type is not supported."


#
# Get the paragraph sentiments
#
def get_sentence_sentiments(doc):
    # tokenize the paragraph
    sentences = [sent.text.strip() for sent in doc.sents]

    st = time.time()

    # get the sentence sentiments
    sentence_sentiment_list = app1_work.get_sentiment_list(sentences)

    et = time.time()
    elapsed_time = et - st
    logging.debug('paragraph tokenization execution time = [' + format(elapsed_time, '.5f') + '] seconds')

    return sentence_sentiment_list


#
# Passthrough route that works as a gateway for calling
# the service that provides sentiment analysis for a sentence
#
@app.route('/sentiment', methods=['POST'])
def sentiment():
    logging.debug("calling app2 for sentiment analysis")
    content_type = request.headers.get('Content-Type')

    # The input is always a simple string
    if content_type == 'text/html':
        try:
            st = time.time()

            data = request.data
            sentence = data.decode("utf-8")
            # Call the sentiment analysis service
            sentiment_analysis = app1_work.get_sentiment_for_sentence(sentence)

            et = time.time()
            # Logs the time it takes to get the sentiment analysis result
            elapsed_time = et - st
            logging.debug('call app2 for sentiment analysis execution time = [' +
                          format(elapsed_time, '.5f') + '] seconds')

            return sentiment_analysis
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
    else:
        return "Content type is not supported."


@app.errorhandler(404)
def not_found(error):
    return 'Bad Request', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT_APP1, debug=config.DEBUG_APP1)
