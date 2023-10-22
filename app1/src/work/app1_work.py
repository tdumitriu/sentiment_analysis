import requests
import logging
import config
import time


#
# Call the service that returns the sentence sentiment
#
def get_sentiment_for_sentence(sentence):
    st = time.time()
    logging.debug("call app2")
    try:
        session = requests.Session()
        # If security is required then an access token will be provided
        session.headers.update({'Authorization': 'Bearer {access_token}'})
        session.headers.update({'Content-Type': 'text/html'})
        url = build_app2_url()
        logging.debug("url server2 = [" + url + "]")

        response = session.post(url=url, data=sentence)
        if response.status_code == 200:
            logging.debug("ok")
        elif response.status_code == 404:
            logging.warning("not found")

        et = time.time()
        elapsed_time = et - st
        logging.debug('execution time = [' + format(elapsed_time, '.5f') + '] seconds')

        return response.json()
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


def build_app2_url():
    url = 'http://' + config.HOSTNAME_APP2 + ':' + format(config.PORT_APP2) + '/' + config.PATH_APP2
    return url


#
# Build the final list of sentences sentiments
#
def get_sentiment_list(sentences):
    sentence_sentiment_list = []
    index = 0
    for sentence in sentences:
        # Skip empty sentences
        if sentence.strip():
            sentiment_analysis = get_sentiment_for_sentence(sentence)
            logging.debug(sentiment_analysis)
            if sentiment_analysis is not None:
                index = index + 1
                sentence_sentiment_list.append(
                    {
                        "id": index,
                        "sentence": sentence,
                        "sentiment": sentiment_analysis['sentiment']
                    }
                )
    return sentence_sentiment_list


#
# Build the final list of sentences sentiments
#
# def get_sentiment_list(s_sentiment_list):
#     for sentence in s_sentiment_list:

