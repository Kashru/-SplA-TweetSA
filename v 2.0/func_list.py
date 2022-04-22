import tweepy as tw
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import collections
import nltk
import numpy as np
from nltk.corpus import stopwords
import re
import networkx as nx
from textblob import TextBlob
import tkinter.messagebox

import warnings

warnings.filterwarnings("ignore")

sns.set(font_scale=1.5)
sns.set_style("whitegrid")
color = plt.cm.gist_earth(np.linspace(0, 1, 25))

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


def TweetsSearch(keyword, start_date, end_date, min_retweets=100, min_faves=100, item_num=300):
    consumer_key = 'K3PCazIaerCRxhhnonBwgPtla'
    consumer_secret = 'xUHhL7WHolpwVonQpOONfWCd6XjulxO71rDFF4L1Ty2ubt5mVs'
    access_token = '1495603708045844482-lVmoLmBvY7iEyIkNNbMyp1sQf8KNwk'
    access_token_secret = 'zURZHZFRWR4rycrAmiKE9M4kayCTt4MlON5jW5iNf8bNO'

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    # Define the search term and the date_since date as variables
    search_words = keyword + " min_retweets:" + str(min_retweets) + " min_faves:" + str(
        min_faves) + " since:" + start_date + " until:" + end_date

    print(search_words)

    # Collect tweets
    tweets_by_tag = tw.Cursor(api.search_tweets, q=search_words, lang="en").items(item_num)

    all_tweets_by_tag = []
    all_tweets_by_tag.extend(tweets_by_tag)

    # Transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.text.encode("utf-8").decode("utf-8"),
                  tweet.created_at,
                  tweet.user.screen_name,
                  tweet.user.name,
                  "https://twitter.com/" + tweet.user.screen_name,
                  tweet.user.url,
                  tweet.favorite_count,
                  tweet.retweet_count,
                  "https://twitter.com/twitter/statuses/" + str(tweet.id)]
                 for idx, tweet in enumerate(all_tweets_by_tag)]
    tbt = pd.DataFrame(outtweets, columns=["Content", "Created_at", "Twitter_id", "Name", "Twitter Home",
                                           "Official website (if it exists)", "Favorite", "Retweet",
                                           "Tweet_link"])

    return tbt


# print(TweetsSearch('bitcoin', '2022-03-07', '2022-3-21', 300, 300))


def TweetUserRelevant(keyword, start_date, end_date, min_retweets=100, min_faves=100, item_num=300):
    consumer_key = 'K3PCazIaerCRxhhnonBwgPtla'
    consumer_secret = 'xUHhL7WHolpwVonQpOONfWCd6XjulxO71rDFF4L1Ty2ubt5mVs'
    access_token = '1495603708045844482-lVmoLmBvY7iEyIkNNbMyp1sQf8KNwk'
    access_token_secret = 'zURZHZFRWR4rycrAmiKE9M4kayCTt4MlON5jW5iNf8bNO'

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    # Define the search term and the date_since date as variables
    search_words = keyword + " min_retweets:" + str(min_retweets) + " min_faves:" + str(
        min_faves) + " since:" + start_date + " until:" + end_date + " -RT"

    # Collect tweets
    tweets_by_tag = tw.Cursor(api.search_tweets, q=search_words, lang="en").items(item_num)

    all_tweets_by_tag = []
    all_tweets_by_tag.extend(tweets_by_tag)

    # Transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.text.encode("utf-8").decode("utf-8"),
                  tweet.created_at,
                  tweet.user.screen_name,
                  tweet.user.name,
                  "https://twitter.com/" + tweet.user.screen_name,
                  tweet.user.url,
                  tweet.favorite_count,
                  tweet.retweet_count,
                  "https://twitter.com/twitter/statuses/" + str(tweet.id)]
                 for idx, tweet in enumerate(all_tweets_by_tag)]
    tbt = pd.DataFrame(outtweets, columns=["Content", "Created_at", "Twitter_id", "Name", "Twitter Home",
                                           "Official website (if it exists)", "Favorite", "Retweet",
                                           "Tweet_link"])
    tbt_user = tbt["Name"].value_counts().rename_axis('User').reset_index(name='Counts')
    tbt_user = tbt_user.sort_values(by="Counts", ascending=False)
    tbt_user = tbt_user.head(20)

    fig, ax = plt.subplots(figsize=(16, 12))

    try:
        # Plot horizontal bar graph
        tbt_user.sort_values(by='Counts').plot.barh(x='User', y='Counts', ax=ax, color=color)

        ax.set_title("Most Relevant Users")

        plt.show()
    except IndexError:
        tkinter.messagebox.showwarning(title='App System Warning', message='Nothing to display. Please try again after '
                                                                           'changing the current parameter setting.')


# TweetUserRelevant('bitcoin', '2022-3-7', '2022-3-21', 100, 100, 300)


def remove_url(txt):
    """Replace URLs found in a text string with nothing
    (i.e. it will remove the URL from the string).

    Parameters
    ----------
    txt : string
        A text string that you want to parse and remove urls.

    Returns
    -------
    The same txt string with url's removed.
    """

    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())


def TweetAnalyze(collection_word1, collection_word2, keyword, start_date, end_date, min_retweets=100, min_faves=100, item_num=300):
    consumer_key = 'K3PCazIaerCRxhhnonBwgPtla'
    consumer_secret = 'xUHhL7WHolpwVonQpOONfWCd6XjulxO71rDFF4L1Ty2ubt5mVs'
    access_token = '1495603708045844482-lVmoLmBvY7iEyIkNNbMyp1sQf8KNwk'
    access_token_secret = 'zURZHZFRWR4rycrAmiKE9M4kayCTt4MlON5jW5iNf8bNO'

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    # Define the search term and the date_since date as variables
    search_words = keyword + " min_retweets:" + str(min_retweets) + " min_faves:" + str(
        min_faves) + " since:" + start_date + " until:" + end_date

    # Collect tweets
    tweets_by_tag = tw.Cursor(api.search_tweets, q=search_words, lang="en").items(item_num)

    all_tweets_by_tag = [tweet.text for tweet in tweets_by_tag]
    all_tweets_no_urls = [remove_url(tweet) for tweet in all_tweets_by_tag]

    # Create a list of lists containing lowercase words for each tweet
    words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_urls]

    # List of all words across tweets
    all_words_no_urls = list(itertools.chain(*words_in_tweet))

    # Create counter
    counts_no_urls = collections.Counter(all_words_no_urls)

    clean_tweets_no_urls = pd.DataFrame(counts_no_urls.most_common(15),
                                        columns=['words', 'count'])

    # Remove Stopwords With nltk
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english') + custom_stop_words)

    # Remove stop words from each tweet list of words
    tweets_nsw = [[word for word in tweet_words if not word in stop_words]
                  for tweet_words in words_in_tweet]

    all_words_nsw = list(itertools.chain(*tweets_nsw))

    counts_nsw = collections.Counter(all_words_nsw)

    clean_tweets_nsw = pd.DataFrame(counts_nsw.most_common(15),
                                    columns=['words', 'count'])

    # Remove collection words
    collection_words = [collection_word1, collection_word2]

    tweets_nsw_nc = [[w for w in word if not w in collection_words]
                     for word in tweets_nsw]

    # Flatten list of words in clean tweets
    all_words_nsw_nc = list(itertools.chain(*tweets_nsw_nc))

    # Create counter of words in clean tweets
    counts_nsw_nc = collections.Counter(all_words_nsw_nc)

    clean_tweets_ncw = pd.DataFrame(counts_nsw_nc.most_common(15),
                                    columns=['words', 'count'])

    fig, ax = plt.subplots(figsize=(15, 15))

    try:
        # Plot horizontal bar graph
        clean_tweets_ncw.sort_values(by='count').plot.barh(x='words',
                                                           y='count',
                                                           ax=ax,
                                                           color=color)

        ax.set_title("Common Words Found in Tweets")

        plt.show()
    except TypeError:
        tkinter.messagebox.showwarning(title='App System Warning', message='Nothing to display. Please try again after '
                                                                           'changing the current parameter setting.')


def TweetCo_occurrence(collection_word, keyword, start_date, end_date, min_retweets=100, min_faves=100, item_num=300):
    consumer_key = 'K3PCazIaerCRxhhnonBwgPtla'
    consumer_secret = 'xUHhL7WHolpwVonQpOONfWCd6XjulxO71rDFF4L1Ty2ubt5mVs'
    access_token = '1495603708045844482-lVmoLmBvY7iEyIkNNbMyp1sQf8KNwk'
    access_token_secret = 'zURZHZFRWR4rycrAmiKE9M4kayCTt4MlON5jW5iNf8bNO'

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    # Define the search term and the date_since date as variables
    search_words = keyword + " min_retweets:" + str(min_retweets) + " min_faves:" + str(
        min_faves) + " since:" + start_date + " until:" + end_date + " -RT"

    # Collect tweets
    tweets_by_tag = tw.Cursor(api.search_tweets, q=search_words, lang="en").items(item_num)

    all_tweets_by_tag = [tweet.text for tweet in tweets_by_tag]
    all_tweets_no_urls = [remove_url(tweet) for tweet in all_tweets_by_tag]

    # Create a list of lists containing lowercase words for each tweet
    words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_urls]

    # List of all words across tweets
    all_words_no_urls = list(itertools.chain(*words_in_tweet))

    # Create counter
    counts_no_urls = collections.Counter(all_words_no_urls)

    clean_tweets_no_urls = pd.DataFrame(counts_no_urls.most_common(15),
                                        columns=['words', 'count'])

    # Remove Stopwords With nltk
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english') + custom_stop_words)

    # Remove stop words from each tweet list of words
    tweets_nsw = [[word for word in tweet_words if not word in stop_words]
                  for tweet_words in words_in_tweet]

    all_words_nsw = list(itertools.chain(*tweets_nsw))

    counts_nsw = collections.Counter(all_words_nsw)

    clean_tweets_nsw = pd.DataFrame(counts_nsw.most_common(15),
                                    columns=['words', 'count'])

    # Remove collection words
    collection_words = [collection_word]

    tweets_nsw_nc = [[w for w in word if not w in collection_words]
                     for word in tweets_nsw]

    # Create list of lists containing bigrams in tweets
    terms_bigram = [list(nltk.bigrams(tweet)) for tweet in tweets_nsw_nc]

    # Flatten list of bigrams in clean tweets
    bigrams = list(itertools.chain(*terms_bigram))

    # Create counter of words in clean bigrams
    bigram_counts = collections.Counter(bigrams)

    bigram_counts.most_common(20)

    bigram_df = pd.DataFrame(bigram_counts.most_common(20),
                             columns=['bigram', 'count'])

    # Create dictionary of bigrams and their counts
    d = bigram_df.set_index('bigram').T.to_dict('records')

    # Create network plot
    G = nx.Graph()

    try:
        # Create connections between nodes
        for k, v in d[0].items():
            G.add_edge(k[0], k[1], weight=(v * 10))

        G.add_node("china", weight=100)

        fig, ax = plt.subplots(figsize=(10, 8))

        pos = nx.spring_layout(G, k=2)

        # Plot networks
        nx.draw_networkx(G, pos,
                         font_size=16,
                         width=4,
                         edge_color='grey',
                         node_color='#1DA1F2',
                         with_labels=False,
                         ax=ax)

        # Create offset labels
        for key, value in pos.items():
            x, y = value[0] + .135, value[1] + .045
            ax.text(x, y,
                    s=key,
                    bbox=dict(facecolor='red', alpha=0.25),
                    horizontalalignment='center', fontsize=13)

        plt.show()
    except IndexError:
        tkinter.messagebox.showwarning(title='App System Warning', message='Nothing to display. Please try again after '
                                                                           'changing the current parameter setting.')
    return bigram_df


def TweetSentiment(keyword, start_date, end_date, min_retweets=100, min_faves=100, item_num=300):
    consumer_key = 'K3PCazIaerCRxhhnonBwgPtla'
    consumer_secret = 'xUHhL7WHolpwVonQpOONfWCd6XjulxO71rDFF4L1Ty2ubt5mVs'
    access_token = '1495603708045844482-lVmoLmBvY7iEyIkNNbMyp1sQf8KNwk'
    access_token_secret = 'zURZHZFRWR4rycrAmiKE9M4kayCTt4MlON5jW5iNf8bNO'

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    # Define the search term and the date_since date as variables
    search_words = keyword + " min_retweets:" + str(min_retweets) + " min_faves:" + str(
        min_faves) + " since:" + start_date + " until:" + end_date + " -RT"

    # Collect tweets
    tweets_by_tag = tw.Cursor(api.search_tweets, q=search_words, lang="en").items(item_num)

    all_tweets_by_tag = [tweet.text for tweet in tweets_by_tag]
    all_tweets_no_urls = [remove_url(tweet) for tweet in all_tweets_by_tag]

    # Create textblob objects of the tweets
    sentiment_objects = [TextBlob(tweet) for tweet in all_tweets_no_urls]

    # Create list of polarity valuesx and tweet text
    sentiment_values = [[tweet.sentiment.polarity, str(tweet)] for tweet in sentiment_objects]

    # Create dataframe containing the polarity value and tweet text
    sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity", "tweet"])

    # Remove polarity values equal to zero
    # sentiment_df = sentiment_df[sentiment_df.polarity != 0]

    fig, ax = plt.subplots(figsize=(12, 8))

    try:
        # Plot histogram with break at zero
        sentiment_df.hist(
            bins=[-1, -0.875, -0.75, -0.625, -0.5, -0.375, -0.25, -0.125, 0.0, 0.125, 0.25, 0.375, 0.5, 0.625,
                  0.75, 0.875, 1],
            ax=ax,
            color='#1DA1F2')

        plt.title("Sentiments from Retrieved Tweets")
        plt.xlabel('Sentiment Score')
        plt.ylabel('Count')
        plt.show()
    except ValueError:
        tkinter.messagebox.showwarning(title='App System Warning', message='Nothing to display. Please try again after '
                                                                           'changing the current parameter setting.')

    return sentiment_df
