import os
import numpy as np
import pickle


class WordEmbedding:
    def __init__(self):
        self.embedding = np.zeros((0, 0))
        self.dimension = 0
        self.vocabulary = dict()
        self.vocabulary_size = 1
        self.vocabulary_index = []

    def dump(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(os.path.join(folder, 'embedding.pkl'), 'wb') as handle:
            obj = {'dimension': self.dimension,
                   'vocabulary': self.vocabulary,
                   'vocabulary_index': self.vocabulary_index,
                   'vocabulary_size': self.vocabulary_size}
            pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)

            glove_map = np.memmap(os.path.join(folder, 'embedding.np'),
                                  dtype=np.float16, mode='w+',
                                  shape=(self.vocabulary_size, self.dimension))
            glove_map[:] = self.embedding

    def load(self, folder):
        with open(os.path.join(folder, 'embedding.pkl'), 'rb') as handle:
            obj = pickle.load(handle)
            self.dimension = obj['dimension']
            self.vocabulary = obj['vocabulary']
            self.vocabulary_size = obj['vocabulary_size']
            self.vocabulary_index = obj['vocabulary_index']

        self.embedding = np.memmap(os.path.join(folder, 'embedding.np'),
                                   dtype=np.float16, mode='r',
                                   shape=(self.vocabulary_size, self.dimension))


class Glove(WordEmbedding):
    def __init__(self):
        super().__init__()

    def parse(self, glove_file):

        self.vocabulary_size = 1
        with open(glove_file, encoding='latin-1') as f:
            for line in f:
                self.vocabulary_size += 1
                if self.dimension == 0:
                    items = line.strip().split(' ')
                    self.dimension = len(items) - 1

        self.embedding = np.zeros((self.vocabulary_size, self.dimension), dtype=float)
        self.vocabulary['<unk>'] = 0
        self.vocabulary_index.append('<unk>')
        with open(glove_file, encoding='latin-1') as f:
            count = 0
            for line in f:
                count += 1
                if count % 10000 == 0:
                    print(count)
                items = line.strip().split(' ')
                self.embedding[count, :] = items[1:]
                self.vocabulary[items[0]] = count
                self.vocabulary_index.append(items[0])
