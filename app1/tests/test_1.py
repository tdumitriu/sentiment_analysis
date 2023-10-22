import unittest

from app1.src.work import app1_work


class MyTestCase(unittest.TestCase):

    def test_sentiment_score_aggregation(self):
        sentence_sentiment_list = [
            {
                "id": 1,
                "sentence": "sentence1",
                "sentiment": [
                    {
                        "label": "POSITIVE",
                        "score": 0.999554455280304
                    }
                ]
            },
            {
                "id": 2,
                "sentence": "sentence2",
                "sentiment": [
                    {
                        "label": "NEGATIVE",
                        "score": 0.9946598410606384
                    }
                ]
            },
            {
                "id": 3,
                "sentence": "sentece3",
                "sentiment": [
                    {
                        "label": "NEGATIVE",
                        "score": 0.9978918433189392
                    }
                ]
            }
        ]
        actual = app1_work.get_sentiment_aggregation(sentence_sentiment_list)
        expected = {
            "label": "NEGATIVE",
            "score": -0.33099907636642456
        }

        self.assertEqual(actual, expected, "The final sentiment value is wrong")

    def test_final_sentiment_label(self):
        self.assertEqual(app1_work.get_final_sentiment_label(0.8), "POSITIVE",
                         "The final sentiment label should be POSITIVE")
        self.assertEqual(app1_work.get_final_sentiment_label(0.01), "NEUTRAL",
                         "The final sentiment label should be NEUTRAL")
        self.assertEqual(app1_work.get_final_sentiment_label(-0.7), "NEGATIVE",
                         "The final sentiment label should be NEGATIVE")


if __name__ == '__main__':
    unittest.main()
