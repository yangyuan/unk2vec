import re


class RawFeatures:

    @staticmethod
    def digits_only(token):
        if re.match('[0-9]+$', token):
            return True
        return False

    @staticmethod
    def digits_and_dot_1(token):
        if re.match('\.[0-9]+$', token):
            return True
        return False

    @staticmethod
    def digits_and_dot_2(token):
        if re.match('[0-9]+\.$', token):
            return True
        return False

    @staticmethod
    def digits_and_dot_3(token):
        if re.match('[0-9]+\.[0-9]+$', token):
            return True
        return False

    @staticmethod
    def year_like_1(token):
        if re.match('[1-9][0-9]{0,3}$', token):
            return True
        return False

    @staticmethod
    def year_like_2(token):
        if re.match('[1-9][0-9]{1,3}$', token):
            return True
        return False

    @staticmethod
    def year_like_3(token):
        if re.match('[1-9][0-9]{2,3}$', token):
            return True
        return False

    @staticmethod
    def year_like_4(token):
        if re.match('[1-2][0-9]{3}$', token):
            return True
        return False


class Features:
    def __init__(self):
        self._features = [getattr(RawFeatures, func) for func in dir(RawFeatures)
                     if callable(getattr(RawFeatures, func)) and not func.startswith('__')]
        self._size = len(self._features)

    def get_size(self):
        return len(self._features)

    def get_vector(self, token):
        tmp = [0.] * self._size
        for i in range(self._size):
            if self._features[i](token):
                tmp[i] = 1.
        return tmp

    def get_vectors(self, tokens):
        tmp = []
        for token in tokens:
            tmp.append(self.get_vector(token))
        return tmp
