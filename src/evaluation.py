# Here we are going to evaluate our model on the test files.
import pandas as pd
from scipy.stats import spearmanr

# We will now compute the similarity of two words


def spearman(model):
    """
    Calculate the similarities between each words and perform the Spearman ranking.
    """
    df_sim = pd.read_csv('../word_vectors/wordsim353.csv')

    # Apply the similarity function to each row
    df_test = df_sim.copy()  # Test dataframe
    df_test = df_test.iloc[:3, :]
    df_test['Similarity'] = df_test.apply(lambda row: model.wv.similarity(row['Word 1'], row['Word 2']),
                                          axis=1)

    spearman_rank = spearmanr(df_test['Human (mean)'], df_test['Similarity']).correlation
    df_test['Spearman'] = spearman_rank
    print("Spearman ranking between similarities is finished. Value is " + str(spearman_rank))

    return df_test


def analogy(model):
    """
    Get the analogy for each phrase.
    :param model: The Word2Vec model which has been trained.
    :return:
    """

    df_analogy = pd.read_csv('../word_vectors/questions-words.txt', sep=" ", header=None, skiprows=1)
    df_analogy = df_analogy.dropna()  # Drop rows with NaN
    df_analogy.columns = ['Word 1', 'Analogy 1', 'Word 2', 'Analogy 2']
    df_analogy = df_analogy.applymap(lambda s: s.lower() if type(s) == str else s)  # Convert to lowercase

    df_test = df_analogy.copy()  # Get the test dataframe
    df_test = df_test.iloc[19529:19531, :]

    # For each line, we find the analogy and we write in the column prediction.
    df_test['Prediction'] = df_test.apply(lambda row: model.most_similar(positive=[row['Word 2'], row['Analogy 1']],
                                                                         negative=[row['Word 1']])[0][0], axis=1)
    print("Computation of the analogies is finished.")

    return df_test