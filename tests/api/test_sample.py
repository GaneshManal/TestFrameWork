from lib.sample import Math


class TestSample:

    def __init__(self):
        pass

    def setUp(self):
        global f
        f = open("output.txt", 'a')
        f.write("\nTest Setup Run")

    def tearDown(self):
        global f
        f.write("\nTest Setup teardown")
        f.close()

    def test_sum(self):
        global f
        f.write("\nTest Addition")
        result = Math.sum(2, 2)
        assert result == 4

    def test_mul(self):
        global f
        f.write("\nTest Multiplication")
        result = Math.mul(2, 2)
        assert result == 4
