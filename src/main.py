# Creation of a basic model by using Glove

from preprocessing import preprocess, tokenization
from gensim.models import Word2Vec
import pandas as pd
import predict_unk
import nltk
import evaluation
from lstm_pos_prediction import assign_POS_tag, create_neural_network, convert_int_data, compute_accuracy
nltk.download('conll2000')
nltk.download('brown')
nltk.download('averaged_perceptron_tagger')

file = open('../word_vectors/sample.txt')

document = file.read()

lines = preprocess(document)
lines = tokenization(lines)
test = lines[:1000]


model = Word2Vec(test, size=100, window=5, min_count=1, workers=4)
print("Training of the Word2Vec is finished.")

model.save("word2vec.model")


word2vec_model = Word2Vec.load("word2vec.model")

# First of all we will do the replacement with UNK.

unk_test, real_words = predict_unk.replace_with_unknown(test)

# We have now the train set.

# Let's try it with the Nearest-Neighbor

predicted_words = predict_unk.prediction_neighbor_similarities(unk_test, word2vec_model)

df = pd.DataFrame()

df['Real Words'] = real_words
df['Nearest Neighbours'] = predicted_words

df['Similarity'] = df.apply(lambda row: word2vec_model.wv.similarity(row['Real Words'], row['Nearest Neighbours']),
                            axis=1)


# We are now doing it this the Part of Speech enhancement

# First we need to create a list of all the POS tags

lines_POS = assign_POS_tag(test)

# We use a neural network (with Keras)

NN_model = create_neural_network()

train_set = test[5:10]
test_set = test[10:13]

X_train, Y_train = convert_int_data(train_set)
X_test, Y_test = convert_int_data(test_set)

NN_model.fit(X_train, Y_train)
print("Training of the Neural Network is finished.")

Y_pred = NN_model.predict(X_test)

accuracy = compute_accuracy(Y_test, Y_pred)

df['LSTM enhancement'] = predict_unk.prediction_neighbor_with_pos(unk_test, word2vec_model, NN_model)


df_sim = evaluation.spearman(word2vec_model)

df_analogy = evaluation.analogy(word2vec_model)