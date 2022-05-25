from kare.functions import cfilter, cmap, creduce


class TestCurriedFunctions:
    def test_cmap(self):
        assert list(cmap(lambda x: x + 1)([1, 2, 3, 4])) == [2, 3, 4, 5]

    def test_cfilter(self):
        assert list(cfilter(lambda x: x % 2)([1, 2, 3, 4])) == [1, 3]

    def test_creduce(self):
        assert creduce(0)(lambda acc, val: acc + val)([1, 2, 3, 4]) == 10
