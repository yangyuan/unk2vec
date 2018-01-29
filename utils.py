import numpy as np
import datetime
import pickle
import os


def trace(*args):
    print(' > ' + str(datetime.datetime.now()) + ':', *args)


def create_file_matrix(path, shape, dtype):
    with open(path + '.shape', 'wb') as f:
        pickle.dump({'shape': shape, 'dtype': dtype}, f)
    return np.memmap(path + '.mem', dtype=dtype, mode='w+', shape=shape)


def load_file_matrix(path):
    with open(path + '.shape', 'rb') as f:
        tmp = pickle.load(f)
    return np.memmap(path + '.mem', dtype=tmp['dtype'], mode='r', shape=tmp['shape'])


def dump_object(path, data):
    with open(path + '.pkl', 'wb') as f:
        pickle.dump(data, f)


def load_object(path):
    with open(path + '.pkl', 'rb') as f:
        return pickle.load(f)


def batches(_x, _y, _size):
    i = -1
    for i in range(int(_x.shape[0]/_size)):
        yield _x[i * _size: (i + 1) * _size], _y[i * _size: (i + 1) * _size]
    i += 1
    if i * _size != _x.shape[0]:
        yield _x[i * _size:], _y[i * _size:]


class DataSet:
    def train_data(self):
        raise NotImplemented()

    def validation_data(self):
        raise NotImplemented()

    def all_train_data(self):
        raise NotImplemented()

    def test_data(self):
        raise NotImplemented()

    def all_data(self):
        raise NotImplemented()


class GeneralDataSet(DataSet):
    def __init__(self):
        self.initialized = False

        self._indexes = []
        self._indexes_train = []
        self._indexes_validation = []
        self._indexes_all_train = []
        self._indexes_test = []

        self._y = np.zeros((0, 0))
        self._x = np.zeros((0, 0))

    def initialize(self, x, y):
        assert x.shape[0] == y.shape[0]
        length = x.shape[0]

        indexes = np.arange(length)
        np.random.shuffle(indexes)
        self._indexes = indexes
        self._indexes_train = indexes[0: int(length * 8 / 10)]
        self._indexes_validation = indexes[self._indexes_train.shape[0]: int(length * 9 / 10)]
        self._indexes_all_train = indexes[0: int(length * 9 / 10)]
        self._indexes_test = indexes[self._indexes_train.shape[0] + self._indexes_validation.shape[0]:]

        self._y = y
        self._x = x

        self.initialized = True

    def train_data(self):
        return self._x[self._indexes_train], self._y[self._indexes_train]

    def validation_data(self):
        return self._x[self._indexes_validation], self._y[self._indexes_validation]

    def all_train_data(self):
        return self._x[self._indexes_all_train], self._y[self._indexes_all_train]

    def test_data(self):
        return self._x[self._indexes_test], self._y[self._indexes_test]

    def all_data(self):
        return self._x[self._indexes], self._y[self._indexes]

    def dump(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

        tmp = create_file_matrix(os.path.join(folder, '_x'), self._x.shape, np.float32)
        tmp[:] = self._x

        tmp = create_file_matrix(os.path.join(folder, '_y'), self._y.shape, np.float32)
        tmp[:] = self._y

        dump_object(os.path.join(folder, '_data'),
                    {
                        '_indexes': self._indexes,
                        '_indexes_train': self._indexes_train,
                        '_indexes_validation': self._indexes_validation,
                        '_indexes_all_train': self._indexes_all_train,
                        '_indexes_test': self._indexes_test
                    })

    def load(self, folder):
        self._x = load_file_matrix(os.path.join(folder, '_x'))
        self._y = load_file_matrix(os.path.join(folder, '_y'))

        tmp = load_object(os.path.join(folder, '_data'))
        self._indexes = tmp['_indexes']
        self._indexes_train = tmp['_indexes_train']
        self._indexes_validation = tmp['_indexes_validation']
        self._indexes_all_train = tmp['_indexes_all_train']
        self._indexes_test = tmp['_indexes_test']


class GloveDataSet(GeneralDataSet):
    def __init__(self, _glove, _features):

        y = _glove.embedding[0:1000]
        x = np.asarray(_features.get_vectors(_glove.vocabulary_index[0:1000]))

        super().__init__()
        super().initialize(x, y)

        print(self._x.shape)
        print(self._y.shape)
