import matplotlib.pyplot as plt , mpld3
import mpld3
import pandas as pd
import numpy as np
import gensim
import pyLDAvis
import textblob


backgnd = "C:\\Users\\17742\\Desktop\\win_art_writing\\art_writing\\text_cleaned\\text_cleaned_all\\"
#"~/home/erik/Desktop/Datasets/art/art_writing/text_cleaned/"

def entity_cross_sub(artist):
    artist['polarity'], artist['subjectivity'] = "",""
    for file in artist.filename.unique():
        filename = backgnd + file
        with open(filename, "r", encoding="utf8") as json_data:
            data = json.load(json_data)
            para = data['para']
            pol = TextBlob(para).sentiment.polarity
            sub = TextBlob(para).sentiment.subjectivity
            entries = artist.loc[artist['filename'] == file]
            entries['polarity'], entries['subjectivity'] = pol, sub
            entries['title'] = str(data['title'])
            artist.loc[artist['filename'] == file] = entries
            print(f"'{data['title']}...'\n\t\t pol: {pol} ,\t sub: {sub}")
    artist_save(artist)
    return artist


def artist_save(artist):
    name = artist.iloc[0].entity
    name = name.replace(" ", "_")
    file = f"artists_save/{name}.pkl"
    pd.to_pickle(artist, file)
    print("success: ", file)

def pol_subj_plot(artist, name=False):
    if name:
        pass
    else:
        name = (artist.iloc[0].entity)
    if artist.shape[0] > 1000:
        dsize=3
    else:
        dsize=8

    css = """
    table
    {
      border-collapse: collapse;
    }
    th
    {
      color: #000000;
      background-color: #77777;
      opacity: 0.7;
    }
    td
    {
      background-color: #ffffff;
      opacity: 0.7;
    }
    table, th, td
    {
      font-family: "Lucida Console", "Courier New", monospace;
      font-size: 14px;
      border: 1px solid black;
      text-align: right;
    }
    """
    plt.rcParams['figure.figsize'] = [10, 8]
    fig, ax = plt.subplots()

    points =  ax.scatter(x=artist['pubtime'], y=artist['subjectivity'], color="Orange", s=dsize, label="subjectivity")
    points1 = ax.scatter(x=artist['pubtime'], y=artist['polarity'], color="LightBlue", label="polarity", s=dsize)


    ###trump specific #import datetime as dt
    ymax = ax.get_ylim()
    ###import matplotlib.dates
    dates = [matplotlib.dates.date2num(dt.datetime(2015, 6, 17)) ,
             matplotlib.dates.date2num(dt.datetime(2016, 11, 8)) ,
             matplotlib.dates.date2num(dt.datetime(2020, 11, 1))]
    ax.plot([dates[0], dates[0]], [-.3, ymax[1]], color="Black", lw=1, alpha=0.3, linestyle="--")
    ax.plot([dates[1], dates[1]], [-.3, ymax[1]], color="Black", lw=1.2, alpha=0.3, linestyle="--")
    ax.plot([dates[2], dates[2]], [-.3, ymax[1]], color="Black", lw=1.2, alpha=0.3, linestyle="--")

    ax.text((dates[0] - ((dates[1] - dates[0])/2)), ymax[0], "2015 Run Announced", ha='left', style='italic',
            fontsize=8,
            rotation="vertical", alpha=.6)

    ax.text((dates[1] + ((dates[1] - dates[0])/2)), ymax[0], "2016 Won Election",  ha='left', style='italic',
            fontsize=8,
            rotation="vertical", alpha=.6)

    ax.text((dates[2] + ((dates[1] - dates[0])/2)), ymax[0], "2020 Lost Election", ha='left', style='italic',
            fontsize=8,
            rotation="vertical", alpha=.6)
    ###trump over

    xmax = ax.get_xlim()
    ax.plot(xmax, [0, 0], color="DarkBlue", alpha=0.3, linestyle="--")
    ax.text(xmax[0], -0.02, "Neutral Tone, Not Subjective",  horizontalalignment='left', style='italic', fontsize=8, alpha=.6)

    ax.set_title(f"{name} pol/subj vs. time".title())
    ax.set_ylabel("Less Subjective, Less Positive,         More Subjective, More Positive")
    ax.set_xlabel("Time")

    plt.show()
    labels_s, labels_p = [],[]
    #labela , labelb = artist.title, artist.source
    for i in range(artist.shape[0]):
        label = artist.iloc[i]
        label = label[["title", "entity", "source", "pubtime", "subjectivity", "polarity"]]
        if label.source == "Nytimes_Arts":
            label.title = str(label.title)[:-17]
        label.pubtime = str(label.pubtime)[:-9]
        #print(label)
        label_p = label[["title", "entity","source", "pubtime",  "polarity"]]
        label_s = label[["title", "entity","source", "pubtime", "subjectivity"]]

        label_s = label_s.to_frame()
        label_p = label_p.to_frame()

        label_s.columns = [f'Mention {i}']
        label_p.columns = [f'Mention {i}']

        labels_p.append(str(label_p.to_html()))
        labels_s.append(str(label_s.to_html()))
    #labels = labels.tolist()

    tooltip = plugins.PointHTMLTooltip(points, labels_s, voffset=10, hoffset=10, css=css)
    tooltip1 = plugins.PointHTMLTooltip(points1, labels_p, voffset=10, hoffset=10, css=css)
    plugins.connect(fig, tooltip, tooltip1)
    mpld3.fig_to_html(fig)
    mpld3.save_html(fig, f"sub_pol_{name}.html")


from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'also'])
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

def sent_to_words(sentence):
    return(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations

def remove_stopwords(doc):
    return [word for word in simple_preprocess(str(doc)) if word not in stop_words]

def make_bigrams(doc, bigram_mod):
    return bigram_mod[doc]

def make_trigrams(doc, bigram_mod, trigram_mod):
    return trigram_mod[bigram_mod[doc]]

def lemmatization(text, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    doc = nlp(" ".join(text))
    texts_out = [token.lemma_ for token in doc if token.pos_ in allowed_postags]
    return texts_out


def topic_find_indiv(artist):
    artist['topics'] = ""
    for file in artist.filename.unique():
        filename = backgnd + file
        with open(filename, "r", encoding="utf8") as json_data:
            data = json.load(json_data)
            para = data['para']
            para = para_split(para)

            para_words = list(sent_to_words(para))
            print(para_words)

            bigram = gensim.models.Phrases(para_words, min_count=5, threshold=100)  # higher threshold fewer phrases.
            trigram = gensim.models.Phrases(bigram[para_words], threshold=100)
            bigram_mod = gensim.models.phrases.Phraser(bigram)
            trigram_mod = gensim.models.phrases.Phraser(trigram)

            para_words_nostops = remove_stopwords(para_words)
            #print("para_words_nostops ", para_words_nostops)
            # Form Bigrams
            para_words_bigrams = make_bigrams(para_words_nostops, bigram_mod)
            #print("para_words_bigram ",para_words_bigrams)


            para_lemmatized = lemmatization(para_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
            print("para_words_lemma ",para_lemmatized)

            id2word = corpora.Dictionary(para_lemmatized)
            texts = para_lemmatized
            corpus = [id2word.doc2bow(text) for text in texts]
            # Build LDA model
            lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                        id2word=id2word,
                                                        num_topics=5,
                                                        random_state=100,
                                                        update_every=1,
                                                        chunksize=100,
                                                        passes=10,
                                                        alpha='auto',
                                                        per_word_topics=True)
            # Print the Keyword in the 10 topics
            pprint(lda_model.print_topics())
            doc_lda = lda_model[corpus]

def topic_find_cumu(artist):
    #artist['topics'] = ""
    para = []
    for file in artist.filename.unique():
        filename = backgnd + file
        with open(filename, "r", encoding="utf8") as json_data:
            data = json.load(json_data)
            para_i = data['para']
            para.append(para_i)

    para_words = list(sent_to_words(para))
    #print(para_words)

    bigram = gensim.models.Phrases(para_words, min_count=5, threshold=100)  # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[para_words], threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    para_words_nostops = remove_stopwords(para_words)
    #print("para_words_nostops ", para_words_nostops)
    # Form Bigrams
    para_words_bigrams = make_bigrams(para_words_nostops, bigram_mod)
    #print("para_words_bigram ",para_words_bigrams)
    para_lemmatized = lemmatization(para_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
    #print("para_words_lemma ",para_lemmatized)

    id2word = corpora.Dictionary(para_lemmatized)
    texts = para_lemmatized
    corpus = [id2word.doc2bow(text) for text in texts]

    # Build LDA model
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=5,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=20,
                                                alpha='auto',
                                                per_word_topics=True)
    # Print the Keyword in the 10 topics
    pprint(lda_model.print_topics())
    doc_lda = lda_model[corpus]

    return lda_model,corpus, id2word

def lda_html(name, lda_model,corpus, id2word):
    vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, id2word)
    name = name.replace(" ", "_")
    pyLDAvis.save_html(vis, f"article_topics_{name}.html")


lda_model,corpus, id2word  = topic_find_cumu(artist)

#attempt 2
def para_split(para):
    para = para.replace(".","|").replace("!","|").replace("?","|").replace(";","|").replace(":","|")
    list_para = para.split("|")
    return list_para

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts, bigram_mod):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts, bigram_mod, trigram_mod):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

df1 = pd.DataFrame()
for artist in whitney:
    artistf = df[df["entity"] == artist]
    df1 = pd.concat([artistf, df1])

"""
###whitney specific #import datetime as dt
    ymax = ax.get_ylim()
    ###import matplotlib.dates
    dates = [matplotlib.dates.date2num(dt.datetime(2017, 4, 17)) , matplotlib.dates.date2num(dt.datetime(2017, 6, 11))] # Mar 17–June 11, 2017
    points1 = ax.scatter(x=artist['pubtime'], y=artist['polarity'], color="LightBlue", label="polarity", s=dsize)


    #ax.add_patch(Rectangle((dates[0],ymax[0]), (dates[1]-dates[0]),ymax[1], edgecolor="Black", alpha=.5, lw=1))
    ax.plot([dates[0],dates[0]],[-.02, ymax[1]], color="Black", lw=1, alpha=0.3, linestyle="--")
    ax.plot([dates[1], dates[1]], [-.02, ymax[1]], color="Black", lw=1, alpha=0.3, linestyle="--")
    ax.text((dates[1]+(dates[1]-dates[0])), ymax[0]+.005, "2017 Whitney Biennial",  ha='center', style='italic', fontsize=8,
            rotation="vertical", alpha=.6)
    ###whitney over


"""