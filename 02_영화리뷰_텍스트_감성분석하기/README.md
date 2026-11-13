# Sentiment Analysis of Naver Movie Reviews

This project cleans NSMC movie reviews and compares average pooling, CNN, LSTM, and a CNN initialized with Word2Vec embeddings.

[Project notebook](%E1%84%8B%E1%85%A7%E1%86%BC%E1%84%92%E1%85%AA%E1%84%85%E1%85%B5%E1%84%87%E1%85%B2_%E1%84%90%E1%85%A6%E1%86%A8%E1%84%89%E1%85%B3%E1%84%90%E1%85%B3_%E1%84%80%E1%85%A1%E1%86%B7%E1%84%89%E1%85%A5%E1%86%BC%E1%84%87%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%E1%86%A8%E1%84%92%E1%85%A1%E1%84%80%E1%85%B5%5B%E1%84%91%E1%85%B3%E1%84%85%E1%85%A9%E1%84%8C%E1%85%A6%E1%86%A8%E1%84%90%E1%85%B3%5D.ipynb)

## Evaluation Criteria

| Criterion | Evidence |
| --- | --- |
| Use Korean Word2Vec and reach at least 85% accuracy | Section 8: CNN_Word2Vec test accuracy is **86.49%** |
| Compare learned and pretrained embeddings using gensim similar words | Section 7: classifier embeddings; Section 8: custom Word2Vec; Section 9: shared word queries and analysis |
| Successfully train at least three model types | Section 5: training and validation outputs for GlobalAveragePooling, CNN, and LSTM |

The external `word2vec_ko.model` file was not provided, so I adapted the lecturer's code to train Word2Vec myself.
I trained Word2Vec on the NSMC training split, then used its vectors to initialize and fine-tune the CNN.
Here, **pretraining means training Word2Vec before training the sentiment classifier**.
The model uses NSMC text, rather than an external text collection. No extra pretrained model file is needed.

## Saved Results

| Model | Validation Accuracy | Validation Loss | Test Accuracy |
| --- | ---: | ---: | ---: |
| GlobalAveragePooling | 84.60% | 0.358842 | - |
| CNN (random embeddings) | 85.82% | 0.325472 | - |
| LSTM | 86.01% | 0.333235 | 85.49% |
| CNN + NSMC Word2Vec | **86.93%** | **0.310330** | **86.49%** |

Word2Vec improved CNN validation accuracy by **1.12 percentage points**.
The LSTM test score came from an earlier baseline evaluation. The final CNN_Word2Vec model was selected using validation accuracy.
These numbers come from saved notebook outputs. Training was not rerun during this update.

## Data Preparation and Models

1. Remove duplicate and missing reviews, tokenize with MeCab, and remove stopwords.
2. Convert words to integer IDs using a vocabulary of up to 10,000 tokens.
3. Pad or trim sequences at the end to a length of 47. This keeps 95.23% of training reviews without trimming.
4. Split the training file into 80% training and 20% validation data, keeping the label balance (`random_state=42`).
5. Train average pooling, CNN, and LSTM models. Stop early based on validation loss and restore the best weights.
6. Train a 100-dimensional skip-gram Word2Vec model using only the training split, then initialize and fine-tune the CNN.
7. Select the final model using validation accuracy and evaluate it on the test set.

After cleaning, the training file has 146,182 reviews and the test file has 49,157 reviews.
The training and validation splits contain 116,945 and 29,237 reviews.
The vocabulary and maximum sequence length were chosen before the validation split. For stricter validation, choose these using only the training split.

## Embedding Comparison

In the classifier embeddings, the Korean word for "not good" was close to words meaning "worst" and "not fun", showing negative sentiment.
In the custom Word2Vec embeddings, "movie" was close to "work", "horror movie", and "animation", showing related contexts.
Words meaning "fun" and "not fun" can also be close, so similar contexts do not always mean the same sentiment.
Section 9 compares both embeddings with the same Korean query words using gensim's `most_similar()`.

## Running and Submission

1. Use an environment with TensorFlow, gensim, pandas, NumPy, matplotlib, scikit-learn, and MeCab.
2. Use `/content` for the NSMC files on Colab, or the current working folder elsewhere. The setup cell downloads missing files.
3. The MeCab build error in the previous Python 3.13 Linux run was fixed by installing `python-mecab-ko-py313`.
4. Run the cells in order. The custom Word2Vec model is trained and saved as `word2vec_ko_custom.model`.
5. Run the new comparison in Section 9 and the checklist in Section 10. Save the notebook with the outputs. The comparison is also saved as `embedding_neighbours.csv`.

The existing training and final test outputs have been kept. The new comparison and checklist cells have not been run yet.
The local environment does not have TensorFlow or gensim, so full training was not rerun.
Before submitting, run the new cells in the original training environment and check the results.

## Reflection and Peer Review

I adapted the lecturer's code to train Word2Vec because the external model was not available.
Future improvements include checking results with several random seeds and building the vocabulary after splitting the data.
The masked average pooling layer ignores padding and keeps the denominator at least 1 to avoid division by zero for empty reviews.

Add the reviewer's name and screenshots after the actual review.

- [ ] Check the final results and evaluation evidence (Sections 5 and 8-10).
- [ ] Check the comments and behavior of the main code.
- [ ] Check the installation fix and extra Word2Vec experiment.
- [ ] Check the result analysis and reflection (Sections 9 and 11).
- [ ] Check that the code is clear and reusable.
