import streamlit as st
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from scipy.spatial.distance import cosine
from sklearn.metrics import pairwise_distances

def getSongRecommendation(text, topK=10):
    """Function returns a 
    
    :args:
        text (str): text of explaining current mood
        topK (int): number of song titles to be returned
        
    :returns:
        top_tracks (list): list containing `topK` number of song titles
    """
    
    bow = st.session_state["bow"]
    model = st.session_state["model"]
    
    X_text = st.session_state["X_text"]
    X_mood = st.session_state["X_mood"]
    
    ## YOUR CODE BELOW AT QUESTION 1.4
    
    x_text = bow.transform([text])
    x_mood = model.predict_proba(x_text)
    sim_mood = calculateSimilarity(x_mood, X_mood)

    x_text = bow.transform([text])
    x_mood = model.predict_proba(x_text)
    sim_text = calculateSimilarity(x_text, X_text)

    mean_scores = []

    for mood_score, text_score in zip(sim_mood, sim_text):
      mean_score = (mood_score + text_score) / 2
      mean_scores.append(mean_score)

    #data
    f = "song_dataset.csv"
    columns = ["song_titles", "song_lyrics"]
    data = pd.read_csv(f, sep="\t", names=columns)


    X_text = bow.transform(data["song_lyrics"])
    X_mood = model.predict_proba(X_text)
    #data

    sorted_scores = dict(sorted(zip(data['song_titles'], mean_scores), key=lambda x: x[1], reverse=True))

    iterator = iter(sorted_scores.items())
    top_tracks = []
    for i in range(topK):
      top_tracks.append(next(iterator))

    return top_tracks
    ## YOUR CODE ABOVE AT QUESTION 1.4
    
    


def calculateSimilarity(document_vector, all_vectors):
    """The function that checks similarity between input and all instance of features of corpus
    
    """
    return (1 - pairwise_distances(all_vectors,document_vector, metric="cosine")).T[0]

if not "X_mood" in st.session_state.keys():
    
    ## COPY YOUR BELOW HERE (Q1.1 TO Q1.3)
    
    #q1.1
    import pandas as panda
    
    file1 = 'train_emotion.csv'
    columns_train = ['sentence', 'label']
    train_data = pd.read_csv(file1, sep='\t', names=columns_train, encoding="utf-8")

    file2 = 'test_emotion.csv'
    columns_test = ['sentence', 'label']
    test_data = pd.read_csv(file2, sep='\t', names=columns_test, encoding="utf-8")


    train_sentences = []
    train_labels = []

    test_sentences = []
    test_labels = []

    label_to_int = { "sadness": 0 , "joy": 1 , "love" : 2 , "anger" : 3, "fear" : 4 , 'surprise': 5 }
    int_to_label = { 0: "sadness", 1: "joy" , 2: "love" , 3: "anger", 4: "fear", 5: 'surprise'}

    train_data['label'] = train_data.label.map(label_to_int)
    test_data['label'] = test_data.label.map(label_to_int)

        #q1.2
    bow = CountVectorizer()
    X_train = bow.fit_transform(train_data["sentence"])
    model = MultinomialNB()
    model.fit(X_train, train_data["label"])

    X_test = bow.transform(test_data["sentence"])
    y_pred = model.predict(X_test)
        #q1.3
    f = "song_dataset.csv"
    columns = ["song_titles", "song_lyrics"]
    data = pd.read_csv(f, sep="\t", names=columns)


    X_text = bow.transform(data["song_lyrics"])
    X_mood = model.predict_proba(X_text)
    print(X_mood)

    ## COPY YOUR ABOVE HERE (Q1.1 TO Q1.3)    
    
    st.session_state["bow"] = bow
    st.session_state["model"] = model
    st.session_state["X_text"] = X_text
    st.session_state["X_mood"] = X_mood
    


######################
# MAIN USER INTERFACE
######################

# Define input_text component
input_text = st.text_input("Enter your current mood")

# Define button here
button = st.button("Calculate")

int_to_label = { 0: "sadness", 1: "joy" , 2: "love" , 3: "anger", 4: "fear", 5: 'surprise'}

if button:
    model = st.session_state["model"]
    
    # Get model prediction and display "You feel `model_prediction`" via `st.write()`
    input_to_vector = st.session_state["bow"].transform([input_text])
    prediction = model.predict(input_to_vector)[0]
    model_prediction = int_to_label[prediction]
    
    st.write("Your emotion is", model_prediction)
    
    recommendations = getSongRecommendation(input_text, topK=10)
    
    # Using for loop, display "Your songs..\n 1. song_title, 2. song_title....." via `st.write()` as in diagram in question.
    st.write("Your songs are:")
    for i, (song_title, _) in enumerate(recommendations):
        st.write(f"{i+1}. {song_title}")
    
    