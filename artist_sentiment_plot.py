import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



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
            artist.loc[artist['filename'] == file] = entries
            print(f"'{data['title'][:30]}...'\t pol: {pol} , sub: {sub}")
    artist_save(artist)
    return artist


def artist_save(artist):
    name = artist.iloc[0].entity
    name = name.replace(" ", "_")
    file = f"artists_save/{name}.pkl"
    pd.to_pickle(artist, file)
    print("success: ", file)

def pol_subj_plot(artist):
    name = artist.iloc[0].entity
    if artist.shape[0] > 1000:
        dsize=1
    else:
        dsize=2
    ax = artist.plot(kind='scatter', x='pubtime', y='subjectivity',
                     color="Orange", s=dsize, label="subjectivity")
    artist.plot(kind='scatter', x='pubtime', y='polarity', color="Blue",
                label="polarity", title=f"{name} pol/subj vs. time".title(), s=dsize, ax=ax)
    plt.show()



