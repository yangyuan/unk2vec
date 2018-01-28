from features import Features
from embedding import Glove
from utils import GloveDataSet, GeneralDataSet

'''
glove = Glove()
glove.parse('data/glove.840B.300d.txt')
glove.dump('data/glove.840B.300d')
glove.load('data/glove.840B.300d')

data = GloveDataSet(glove, Features())
data.dump('data/dataset')
'''

data = GeneralDataSet()
data.load('data/dataset')

print(data.all_data())
