# UNK2VEC

## Warning

Not working yet

## Background

Word2vec is a popular way to do word embeddings. Usually the unknown tokens in corpus won't make too much trouble. This
is especially true when you use large Word2vec such as Glove. However in some tasks the unknown tokens sometimes play a
big role. Such as in factoid question answering tasks, unknown tokens are usually included in the answer.

## Intuition

Studies show that most of unknown tokens are numbers (such as `32.21756368%`), time (such as `1081bc`), name entities
(include account names, domain names, emails) and typos. The first three are easy for human to recognize because they
follow some patterns. The idea in here is to use charactor n-grams as features to predict the vector of unknown tokens.

Also for words with lower frequencies (such as typos), the vector from Word2vec might not be precise. I'm hoping that
this project can also be used to adjust those values for lower frequency words.

## Implementation

I'm planning to use existing big Word2vec as data-set and start with relatively simple Neural Network. Considering the
accuracy for the vector of lower frequency words might not precise, the test set will contain the words with all
frequencies.
