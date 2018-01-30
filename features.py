class CharFeatures:
    chars = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5',
             '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
             'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_',
             '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
             'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']

    @staticmethod
    def _get_letter_grams(_len):
        if _len == 1:
            return CharFeatures.letters.copy()
        else:
            tmp = CharFeatures._get_letter_grams(_len - 1)
            ret = []
            for char in CharFeatures.letters:
                for gram in tmp:
                    ret.append(char + gram)
            return ret

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

        for gram in CharFeatures._get_letter_grams(3):
            gram = _char_to_py_string(gram)
            tmp = 'lambda x: True if x.lower().find(%s) != -1 else False' % gram
            ret.append(eval(tmp))

        return ret


class Features:
    def __init__(self):
        self._features = CharFeatures.get_features()
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
