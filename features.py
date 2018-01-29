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

    @staticmethod
    def length_less_1(token):
        if len(token) < 2:
            return True
        return False

    @staticmethod
    def length_less_2(token):
        if len(token) < 4:
            return True
        return False

    @staticmethod
    def length_less_3(token):
        if len(token) < 8:
            return True
        return False

    @staticmethod
    def length_less_4(token):
        if len(token) < 16:
            return True
        return False

    @staticmethod
    def start_with_upper_1(token):
        if re.match('[A-Z][a-z0-9]*$', token):
            return True
        return False

    @staticmethod
    def start_with_upper_2(token):
        if re.match('[A-Z][a-z]*$', token):
            return True
        return False

    @staticmethod
    def all_upper(token):
        if re.match('[A-Z]*$', token):
            return True
        return False

    @staticmethod
    def all_upper_2(token):
        if re.match('[0-9]*[A-Z]*$', token):
            return True
        return False


class CharFeatures:

    chars = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']

    @staticmethod
    def _get_grams(_len):
        if _len == 1:
            return CharFeatures.chars.copy()
        else:
            tmp = CharFeatures._get_grams(_len - 1)
            ret = []
            for char in CharFeatures.chars:
                for gram in tmp:
                    ret.append(char + gram)
            return ret

    @staticmethod
    def get_features():

        def _char_to_py_string(token):
            token = token.replace("\\", "\\\\")
            token = token.replace("'", "\\'")
            return "'" + token + "'"

        ret = []

        for gram in CharFeatures._get_grams(2):
            gram = _char_to_py_string(gram)
            tmp = 'lambda x: True if x.find(%s) != -1 else False' % gram
            ret.append(eval(tmp))

        for gram in CharFeatures._get_grams(1):
            gram = _char_to_py_string(gram)
            tmp = 'lambda x: x.startswith(%s)' % gram
            ret.append(eval(tmp))
            tmp = 'lambda x: x.endswith(%s)' % gram
            ret.append(eval(tmp))

        return ret


class Features:
    def __init__(self):
        self._features = [getattr(RawFeatures, func) for func in dir(RawFeatures)
                          if callable(getattr(RawFeatures, func)) and not func.startswith('__')]

        # self._features = []

        self._features.extend(CharFeatures.get_features())
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
