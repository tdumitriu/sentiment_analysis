import requests.exceptions
from flask import Flask, request, jsonify, make_response

from transformers import pipeline
import logging
import config
import time

logging.basicConfig(filename=config.LOGFILE,
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)
app.logger.info("app2 has been started")
app.logger.info(app.config)


#######################################################
# SERVER 2
#######################################################

#
# Route that returns info about service
#
@app.route('/', methods=['GET'])
def info():
    app.config.from_object(config)
    app.logger.debug("app2 UP and RUNNING")

    return "APP2 is UP and RUNNING\n"


#
# Route providing status information for heartbeat monitoring
#
@app.route('/status', methods=['GET'])
def status():
    app.logger.debug("STATUS: ok")
    response = make_response(
        jsonify(
            {"status": "ok"}
        ),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


#
# Main process that returns the sentiment of the sentence
#
@app.route('/sentiment', methods=['POST'])
def get_sentiment():
    content_type = request.headers.get('Content-Type')
    if content_type == 'text/html':
        try:
            data = request.data

            st = time.time()
            classifier = pipeline('sentiment-analysis')
            sentence = data.decode("utf-8")
            sentiment_classification = classifier(sentence)

            logging.debug(sentence)
            logging.debug(sentiment_classification)

            et = time.time()
            elapsed_time = et - st
            logging.debug('sentiment analysis time = [' + format(elapsed_time, '.5f') + '] seconds')

            response = make_response(
                {"sentiment": sentiment_classification},
                200,
            )
            logging.debug(response)
            response.headers["Content-Type"] = "application/json"

            return response
        except requests.exceptions.RequestException as err:
            return err
    else:
        return "Content type [" + content_type + "] is not supported."


@app.errorhandler(404)
def not_found(error):
    return 'Bad Request', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT2, debug=config.DEBUG2)
