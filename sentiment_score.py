from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


def quick_score(text):
    analyzer_pa = TextBlob(text)
    # analyzer_nb = TextBlob(text, analyzer=NaiveBayesAnalyzer())
    print(analyzer_pa.sentiment)
    # print(analyzer_nb.sentiment)
    sentiments = {
            "pa_polarity":analyzer_pa.sentiment.polarity,
            "pa_subjectivity":analyzer_pa.sentiment.subjectivity,
            "score":analyzer_pa.sentiment.polarity*analyzer_pa.sentiment.subjectivity
            # "nb_classification":analyzer_nb.sentiment.classification,
            # "nb_p_pos":analyzer_nb.sentiment.p_pos,
            # "nb-p_neg":analyzer_nb.sentiment.p_neg
    }
    return sentiments