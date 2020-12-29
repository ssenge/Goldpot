from goldpot.Utils import Splitter


class Tests:

    short_list = ['abc', 'def', 'ghi']
    long_list = 10000 * short_list

    def test_1(self):
        assert Splitter.len_chunk_split([]) == []
        assert Splitter.len_chunk_split(self.short_list)[0][0] == self.short_list
        assert Splitter.len_chunk_split(self.long_list)[0][0] == self.long_list


    def test_2(self):
        assert Splitter.len_chunk_split(self.short_list, max_len=6) == [[['abc', 'def']], [['ghi']]]


    def test_3(self):
        assert Splitter.len_chunk_split(self.short_list, max_len=6, max_chunks=1) == [[['abc'], ['def']], [['ghi']]]


    def test_4(self):
        r = Splitter.len_chunk_split(self.long_list, max_len=7500, max_chunks=2000)
        assert len(r) == 12  # len(long_list) == 90000, len(r) == 12 == 90000/7500
        for i in range(0, 11):
            assert len(r[i]) == 2
            assert len(r[i][0]) == 2000
            assert len(r[i][1]) == 500
