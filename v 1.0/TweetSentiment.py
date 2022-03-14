from textblob import TextBlob
import sys
import tweepy
import pandas as pd
import numpy as np
import os
import nltk
import pycountry
import re
import string
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from IPython.display import display
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pandasgui import show
import tkinter as tk
from tkinter import simpledialog

nltk.download('vader_lexicon')

# Authentication
consumer_key = 'K3PCazIaerCRxhhnonBwgPtla'
consumer_secret = 'xUHhL7WHolpwVonQpOONfWCd6XjulxO71rDFF4L1Ty2ubt5mVs'
access_token = '1495603708045844482-lVmoLmBvY7iEyIkNNbMyp1sQf8KNwk'
access_token_secret = 'zURZHZFRWR4rycrAmiKE9M4kayCTt4MlON5jW5iNf8bNO'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def rs_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Sentiment Analysis
def percentage(part, whole):
    return 100 * float(part) / float(whole)


ROOT = tk.Tk()

ROOT.withdraw()
# the input dialog
keyword = simpledialog.askstring(title="Quick Tweet Sentiment Analysis",
                                 prompt="Please enter keyword or hashtag to search: ")
noOfTweet = int(simpledialog.askstring(title="Quick Tweet Sentiment Analysis",
                                       prompt="Please enter an integer to indicate how many tweets to analyze: "))

# keyword = input("Please enter keyword or hashtag to search: ")
# noOfTweet = int(input("Please enter how many tweets to analyze: "))

tweets = tweepy.Cursor(api.search_tweets, q=keyword).items(noOfTweet)
positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []

for tweet in tweets:

    # print(tweet.text)
    tweet_list.append(tweet.text)
    analysis = TextBlob(tweet.text)
    score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
    neg = score['neg']
    neu = score['neu']
    pos: float = score['pos']
    comp = score['compound']
    polarity += analysis.sentiment.polarity

    if neg > pos:
        negative_list.append(tweet.text)
        negative += 1

    elif pos > neg:
        positive_list.append(tweet.text)
        positive += 1

    elif pos == neg:
        neutral_list.append(tweet.text)
        neutral += 1

positive = percentage(positive, noOfTweet)
negative = percentage(negative, noOfTweet)
neutral = percentage(neutral, noOfTweet)
polarity = percentage(polarity, noOfTweet)
positive = format(positive, '.1f')
negative = format(negative, '.1f')
neutral = format(neutral, '.1f')

# Number of Tweets (Total, Positive, Negative, Neutral)
tweet_list = pd.DataFrame(tweet_list)
neutral_list = pd.DataFrame(neutral_list)
negative_list = pd.DataFrame(negative_list)
positive_list = pd.DataFrame(positive_list)
print("total number: ", len(tweet_list))
print("positive number: ", len(positive_list))
print("negative number: ", len(negative_list))
print("neutral number: ", len(neutral_list))

# Creating PieCart
labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]', 'Negative [' + str(negative) + '%]']
sizes = [positive, neutral, negative]
colors = ['yellowgreen', 'blue', 'red']
patches, texts = plt.pie(sizes, colors=colors, startangle=90)
plt.style.use('default')
plt.legend(labels)
plt.title("Sentiment Analysis Result for keyword= " + keyword + "")
plt.axis("equal")
plt.show()

tweet_list

tweet_list.drop_duplicates(inplace=True)

# Cleaning Text (RT, Punctuation etc)
# Creating new dataframe and new features
tw_list = pd.DataFrame(tweet_list)
tw_list["text"] = tw_list[0]
# Removing RT, Punctuation etc
remove_rt = lambda x: re.sub('RT @\w+: ', " ", x)
rt = lambda x: re.sub("(@[A-Za-z0–9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", x)
tw_list["text"] = tw_list.text.map(remove_rt).map(rt)
tw_list["text"] = tw_list.text.str.lower()
tw_list.head(10)

# Calculating Negative, Positive, Neutral and Compound values
tw_list[['polarity', 'subjectivity']] = tw_list['text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
for index, row in tw_list['text'].iteritems():
    score = SentimentIntensityAnalyzer().polarity_scores(row)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    comp = score['compound']
    if neg > pos:
        tw_list.loc[index, 'sentiment'] = "negative"
    elif pos > neg:
        tw_list.loc[index, 'sentiment'] = "positive"
    else:
        tw_list.loc[index, 'sentiment'] = "neutral"
        tw_list.loc[index, 'neg'] = neg
        tw_list.loc[index, 'neu'] = neu
        tw_list.loc[index, 'pos'] = pos
        tw_list.loc[index, 'compound'] = comp


# Creating new data frames for all sentiments (positive, negative and neutral)
tw_list_negative = tw_list[tw_list["sentiment"] == "negative"]
tw_list_positive = tw_list[tw_list["sentiment"] == "positive"]
tw_list_neutral = tw_list[tw_list["sentiment"] == "neutral"]


def count_values_in_column(data, feature):
    total = data.loc[:, feature].value_counts(dropna=False)
    percentage = round(data.loc[:, feature].value_counts(dropna=False, normalize=True) * 100, 2)
    return pd.concat([total, percentage], axis=1, keys=['Total', 'Percentage'])


# Count_values for sentiment
count_values_in_column(tw_list, "sentiment")

# create data for Pie Chart
pichart = count_values_in_column(tw_list, "sentiment")
names = pichart.index
size = pichart["Percentage"]

# Create a circle for the center of the plot
my_circle = plt.Circle((0, 0), 0.7, color='white')
plt.pie(size, labels=names, colors=['green', 'blue', 'red'])
p = plt.gcf()
p.gca().add_artist(my_circle)
plt.show()


# Function to Create Wordcloud
def create_wordcloud(text, filename):
    mask = np.array(Image.open(rs_path("cloud.png")))
    stopwords = set(STOPWORDS)
    wc = WordCloud(background_color="white", mask=mask, max_words=3000, stopwords=stopwords, repeat=True)
    wc.generate(str(text))
    wc.to_file(rs_path(filename+".png"))
    print("Word Cloud Saved Successfully")
    path = rs_path(filename+".png")
    img = mpimg.imread(path)
    plt.imshow(img)
    plt.axis('off')
    plt.show()


# Creating wordcloud for all tweets
create_wordcloud(tw_list["text"].values, 'wc_all')

# Creating wordcloud for positive sentiment
create_wordcloud(tw_list_positive["text"].values, 'wc_pos')

# Creating wordcloud for negative sentiment
create_wordcloud(tw_list_negative["text"].values, 'wc_neg')

# Calculating tweet’s lenght and word count
tw_list['text_len'] = tw_list['text'].astype(str).apply(len)
tw_list['text_word_count'] = tw_list['text'].apply(lambda x: len(str(x).split()))
round(pd.DataFrame(tw_list.groupby("sentiment").text_len.mean()), 2)

round(pd.DataFrame(tw_list.groupby("sentiment").text_word_count.mean()), 2)


# Removing Punctuation
def remove_punct(text):
    text = "".join([char for char in text if char not in string.punctuation])
    text = re.sub('[0–9]+', '', text)
    return text


tw_list['punct'] = tw_list['text'].apply(lambda x: remove_punct(x))


# Applying tokenization
def tokenization(text):
    text = re.split('\W+', text)
    return text


tw_list['tokenized'] = tw_list['punct'].apply(lambda x: tokenization(x.lower()))
# Removing stopwords
custom_stop_words = ["0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "A", "a1", "a2", "a3", "a4", "ab",
                     "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly",
                     "across", "act", "actually", "ad", "added", "adj", "ae", "af", "affected",
                     "affecting", "after", "afterwards", "ag", "again", "against", "ah", "ain", "aj",
                     "al", "all", "allow", "allows", "almost", "alone", "along", "already", "also",
                     "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and",
                     "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anyway",
                     "anyways", "anywhere", "ao", "ap", "apart", "apparently", "appreciate",
                     "approximately", "ar", "are", "aren", "arent", "arise", "around", "as", "aside",
                     "ask", "asking", "at", "au", "auth", "av", "available", "aw", "away", "awfully",
                     "ax", "ay", "az", "b", "B", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be",
                     "became", "been", "before", "beforehand", "beginnings", "behind", "below",
                     "beside", "besides", "best", "between", "beyond", "bi", "bill", "biol", "bj",
                     "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt",
                     "bu", "but", "bx", "by", "c", "C", "c1", "c2", "c3", "ca", "call", "came", "can",
                     "cannot", "cant", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch",
                     "ci", "cit", "cj", "cl", "clearly", "cm", "cn", "co", "com", "come", "comes",
                     "con", "concerning", "consequently", "consider", "considering", "could", "couldn",
                     "couldnt", "course", "cp", "cq", "cr", "cry", "cs", "ct", "cu", "cv", "cx", "cy",
                     "cz", "d", "D", "d2", "da", "date", "dc", "dd", "de", "definitely", "describe",
                     "described", "despite", "detail", "df", "di", "did", "didn", "dj", "dk", "dl",
                     "do", "does", "doesn", "doing", "don", "done", "down", "downwards", "dp", "dr",
                     "ds", "dt", "du", "due", "during", "dx", "dy", "e", "E", "e2", "e3", "ea", "each",
                     "ec", "ed", "edu", "ee", "ef", "eg", "ei", "eight", "eighty", "either", "ej",
                     "el", "eleven", "else", "elsewhere", "em", "en", "end", "ending", "enough",
                     "entirely", "eo", "ep", "eq", "er", "es", "especially", "est", "et", "et-al",
                     "etc", "eu", "ev", "even", "ever", "every", "everybody", "everyone", "everything",
                     "everywhere", "ex", "exactly", "example", "except", "ey", "f", "F", "f2", "fa",
                     "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find",
                     "fire", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows",
                     "for", "former", "formerly", "forth", "forty", "found", "four", "fr", "from",
                     "front", "fs", "ft", "fu", "full", "further", "furthermore", "fy", "g", "G", "ga",
                     "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving",
                     "gj", "gl", "go", "goes", "going", "gone", "got", "gotten", "gr", "greetings",
                     "gs", "gy", "h", "H", "h2", "h3", "had", "hadn", "happens", "hardly", "has",
                     "hasn", "hasnt", "have", "haven", "having", "he", "hed", "hello", "help", "hence",
                     "here", "hereafter", "hereby", "herein", "heres", "hereupon", "hes", "hh", "hi",
                     "hid", "hither", "hj", "ho", "hopefully", "how", "howbeit", "however", "hr", "hs",
                     "http", "hu", "hundred", "hy", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib",
                     "ibid", "ic", "id", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "im",
                     "immediately", "in", "inasmuch", "inc", "indeed", "index", "indicate",
                     "indicated", "indicates", "information", "inner", "insofar", "instead",
                     "interest", "into", "inward", "io", "ip", "iq", "ir", "is", "isn", "it", "itd",
                     "its", "iv", "ix", "iy", "iz", "j", "J", "jj", "jr", "js", "jt", "ju", "just",
                     "k", "K", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "ko", "l", "L", "l2",
                     "la", "largely", "last", "lately", "later", "latter", "latterly", "lb", "lc",
                     "le", "least", "les", "less", "lest", "let", "lets", "lf", "like", "liked",
                     "likely", "line", "little", "lj", "ll", "ln", "lo", "look", "looking", "looks",
                     "los", "lr", "ls", "lt", "ltd", "m", "M", "m2", "ma", "made", "mainly", "make",
                     "makes", "many", "may", "maybe", "me", "meantime", "meanwhile", "merely", "mg",
                     "might", "mightn", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more",
                     "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much",
                     "mug", "must", "mustn", "my", "n", "N", "n2", "na", "name", "namely", "nay", "nc",
                     "nd", "ne", "near", "nearly", "necessarily", "neither", "nevertheless", "new",
                     "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody", "non",
                     "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "novel",
                     "now", "nowhere", "nr", "ns", "nt", "ny", "o", "O", "oa", "ob", "obtain",
                     "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj",
                     "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only",
                     "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "otherwise", "ou", "ought",
                     "our", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p",
                     "P", "p1", "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular",
                     "particularly", "pas", "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph",
                     "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly",
                     "pp", "pq", "pr", "predominantly", "presumably", "previously", "primarily",
                     "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q",
                     "Q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "R", "r2", "ra", "ran",
                     "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent",
                     "recently", "ref", "refs", "regarding", "regardless", "regards", "related",
                     "relatively", "research-articl", "respectively", "resulted", "resulting",
                     "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr",
                     "rs", "rt", "ru", "run", "rv", "ry", "s", "S", "s2", "sa", "said", "saw", "say",
                     "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section",
                     "seem", "seemed", "seeming", "seems", "seen", "sent", "seven", "several", "sf",
                     "shall", "shan", "shed", "shes", "show", "showed", "shown", "showns", "shows",
                     "si", "side", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm",
                     "sn", "so", "some", "somehow", "somethan", "sometime", "sometimes", "somewhat",
                     "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify",
                     "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub",
                     "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure",
                     "sy", "sz", "t", "T", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc",
                     "td", "te", "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks",
                     "thanx", "that", "thats", "the", "their", "theirs", "them", "themselves", "then",
                     "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein",
                     "thereof", "therere", "theres", "thereto", "thereupon", "these", "they", "theyd",
                     "theyre", "thickv", "thin", "think", "third", "this", "thorough", "thoroughly",
                     "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through",
                     "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to",
                     "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried",
                     "tries", "truly", "try", "trying", "ts", "tt", "tv", "twelve", "twenty", "twice",
                     "two", "tx", "u", "U", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under",
                     "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up",
                     "upon", "ups", "ur", "us", "used", "useful", "usefully", "usefulness", "using",
                     "usually", "ut", "v", "V", "va", "various", "vd", "ve", "very", "via", "viz",
                     "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w", "W", "wa",
                     "was", "wasn", "wasnt", "way", "we", "wed", "welcome", "well", "well-b", "went",
                     "were", "weren", "werent", "what", "whatever", "whats", "when", "whence",
                     "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "wheres",
                     "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who",
                     "whod", "whoever", "whole", "whom", "whomever", "whos", "whose", "why", "wi",
                     "widely", "with", "within", "without", "wo", "won", "wonder", "wont", "would",
                     "wouldn", "wouldnt", "www", "x", "X", "x1", "x2", "x3", "xf", "xi", "xj", "xk",
                     "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "Y", "y2", "yes", "yet", "yj",
                     "yl", "you", "youd", "your", "youre", "yours", "yr", "ys", "yt", "z", "Z", "zero",
                     "zi", "zz"]
stop_words = set(nltk.corpus.stopwords.words('english') + custom_stop_words)


def remove_stopwords(text):
    text = [word for word in text if word not in stop_words]
    return text


tw_list['nonstop'] = tw_list['tokenized'].apply(lambda x: remove_stopwords(x))
# Applying Stemmer
ps = nltk.PorterStemmer()


def stemming(text):
    text = [ps.stem(word) for word in text]
    return text


tw_list['stemmed'] = tw_list['nonstop'].apply(lambda x: stemming(x))

# Cleaning Text
def clean_text(text):
    text_lc = "".join([word.lower() for word in text if word not in string.punctuation])  # remove puntuation
    text_rc = re.sub('[0-9]+', '', text_lc)
    tokens = re.split('\W+', text_rc)  # tokenization
    text = [ps.stem(word) for word in tokens if word not in stop_words]  # remove stopwords and stemming
    return text


# Appliyng Countvectorizer
countVectorizer = CountVectorizer(analyzer=clean_text)
countVector = countVectorizer.fit_transform(tw_list['text'])
print('{} Number of reviews has {} words'.format(countVector.shape[0], countVector.shape[1]))
print(countVectorizer.get_feature_names())

count_vect_df = pd.DataFrame(countVector.toarray(), columns=countVectorizer.get_feature_names())
count_vect_df.head()

# Most Used Words
count = pd.DataFrame(count_vect_df.sum())
countdf = count.sort_values(0, ascending=False).head(20)
countdf = countdf.reset_index()
countdf.columns = ['words', 'count']
countdf = countdf.drop(labels=range(0, 2), axis=0)
plt.style.use('fivethirtyeight')
color = plt.cm.gist_earth(np.linspace(0, 1, 25))
countdf.sort_values(by='count').plot(x='words', y='count', kind='barh', figsize=(15, 6), color=color)
plt.title("Most Frequently Words in this Tweet Search - Top 20")
plt.xlabel('Word')
plt.ylabel('Frequency')
plt.show()
show(countdf)


# Function to ngram
def get_top_n_gram(corpus, ngram_range, n=None):
    vec = CountVectorizer(ngram_range=ngram_range, stop_words='english').fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:n]


# n2_bigram
n2_bigrams = get_top_n_gram(tw_list['text'], (2, 2), 20)
show(n2_bigrams)

# n3_trigram
n3_trigrams = get_top_n_gram(tw_list['text'], (3, 3), 20)
show(n3_trigrams)
