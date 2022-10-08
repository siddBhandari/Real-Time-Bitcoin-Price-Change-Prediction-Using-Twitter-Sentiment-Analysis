pickle_in = open("vectorizer.pkl","rb")
vect=pickle.load(pickle_in)

pickle_in = open("MultinomialNB.pkl","rb")
MultinomialNB = pickle.load(pickle_in)