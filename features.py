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

    @staticmethod
    def root_auto(token):
        if token.find('auto') != -1:
            return True
        return False

    @staticmethod
    def root_pete(token):
        if token.find('pete') != -1:
            return True
        return False

    @staticmethod
    def root_mobile(token):
        if token.find('mobile') != -1:
            return True
        return False

    @staticmethod
    def root_man(token):
        if token.find('man') != -1:
            return True
        return False

    @staticmethod
    def root_super(token):
        if token.find('super') != -1:
            return True
        return False

    @staticmethod
    def root_ble(token):
        if token.find('ble') != -1:
            return True
        return False

    @staticmethod
    def root_tion(token):
        if token.find('tion') != -1:
            return True
        return False

    @staticmethod
    def root_s(token):
        if token.find('s') != -1:
            return True
        return False

    @staticmethod
    def root_male(token):
        if token.find('male') != -1:
            return True
        return False

    @staticmethod
    def root_sub(token):
        if token.find('sub') != -1:
            return True
        return False

    @staticmethod
    def root_over(token):
        if token.find('over') != -1:
            return True
        return False

    @staticmethod
    def root_am(token):
        if token.find('am') != -1:
            return True
        return False

    @staticmethod
    def root_pm(token):
        if token.find('pm') != -1:
            return True
        return False

    @staticmethod
    def root_bc(token):
        if token.find('bc') != -1:
            return True
        return False

    @staticmethod
    def root_before(token):
        if token.find('before') != -1:
            return True
        return False

    @staticmethod
    def root_after(token):
        if token.find('after') != -1:
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
