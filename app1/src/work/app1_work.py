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


#
# Build the URL for calling app2
#
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
# Aggregate the sentence sentiments
#
# There are several methods to aggregate overall sentiment from pre-sentence sentiment scores.
# For the current exercise the "Average Score" ius implemented.
#
# 1. Average Score:
#    - calculate the mean of all sentence sentiment scores.
# 2. Weighted Average
#    - assign weights to sentences based on their length, importance, or other features
#    - calculate the average sentiment score by multiplying each sentence's score  by its
#      weight and then dividing by total weight
# 3. Majority Rule
#    - determine the overall sentiment based on which class has the majority
# 4. Cumulative Score
#    - Sum up all sentiment scores
# 5. Median Score
#    - sort the scores and pick the middle one (used mostly to mitigate the impact of outliers)
# 6. Mode-Based Aggregation
#    - assign each sentence a sentiment class
#    - determine the most frequently occurring sentiment class as the overall sentiment
# 7. Sentiment Density
#    - calculate the proportion of sentences that fall into each sentiment category
#    - get the heat map of sentiments
# 8. Topic-based Aggregation
#    - group sentences by logic or theme
#    - compute sentiment for each logic and then use other sentiment aggregation method to get the overall sentiment
# 9. Hybrid Approach
#    - Combine multiple methods for a more nuanced overall sentiment
# 10. Machine Learning
#    - "deep learning has provided a new standard by which to measure sentiment analysis models and has introduced
#       many common model architectures that can be quickly prototyped and adapted to particular datasets to quickly
#       achieve high accuracy"
#       (https://www.datarobot.com/blog/using-machine-learning-for-sentiment-analysis-a-deep-dive/)
#    - "The Sentiment models are pre-trained classification models for classifying the sentiment of the input text.
#       It can predict the document sentiment, each sentence's sentiment, and each target's sentiment."
#       (https://www.ibm.com/docs/en/watson-libraries?topic=catalog-sentiment-aggregated)
# ... Many other techniques
#
def get_sentiment_aggregation(s_sentiment_list):
    final_sentiment_score = 0.00
    index = 0
    for sentence in s_sentiment_list:
        current_label = sentence['sentiment'][0]['label']
        current_score = sentence['sentiment'][0]['score']
        logging.info("==> score = [" + format(current_score) + "], sentiment = [" + current_label + "]")
        index = index + 1

        current_sign = 1
        if current_label == "NEGATIVE":
            current_sign = -1

        final_sentiment_score = final_sentiment_score + (current_score * current_sign)

    final_score = final_sentiment_score / index
    final_sentiment = get_final_sentiment_label(final_score)

    return {"label": final_sentiment, "score": final_score}


#
# Get final sentiment label
#
def get_final_sentiment_label(final_score):
    final_sentiment = "POSITIVE"
    if final_score < 0:
        final_sentiment = "NEGATIVE"
    elif final_score < 0.1:
        final_sentiment = "NEUTRAL"
    return final_sentiment
