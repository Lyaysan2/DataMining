import math


class BloomFilter(object):

    def __init__(self, word_count, fp_prob):
        self.fp_prob = fp_prob
        self.word_count = word_count

        self.size = int(-(word_count * math.log(fp_prob)) / (math.log(2) ** 2))
        self.hash_count = int((self.size / self.word_count) * math.log(2))

        self.bloom_filter = [0] * self.size

    def _hash(self, item, i):
        hash_f = 5381
        for x in item:
            hash_f += (hash_f << 5) + ord(x) * 2 ** i
        return hash_f % self.size

    def add_to_filter(self, item):
        for i in range(self.hash_count):
            self.bloom_filter[self._hash(item, i)] += 1
        # print(*self.bloom_filter)

    def delete_from_filter(self, item):
        for i in range(self.hash_count):
            self.bloom_filter[self._hash(item, i)] -= 1
        # print(*self.bloom_filter)

    def check(self, item):
        for i in range(self.hash_count):
            if self.bloom_filter[self._hash(item, i)] == 0:
                return False  # значит точно нет слова
        return True  # возможно есть


file = open("/Users/lyaysanz/Desktop/HarryPotter.txt", "rt")
words = file.read().split()

word_count = len(words)
fp_prob = 0.1

bloom_filter = BloomFilter(word_count, fp_prob)

print("Count of word:{}".format(bloom_filter.word_count))
print("Size of bit array:{}".format(bloom_filter.size))
print("False positive Probability:{}".format(bloom_filter.fp_prob))
print("Number of hash functions:{}".format(bloom_filter.hash_count))

for item in words:
    # print(item)
    bloom_filter.add_to_filter(item)

# print(*bloom_filter.bloom_filter)

print(bloom_filter.check("фильтр"))  # false
bloom_filter.add_to_filter("фильтр")
print(bloom_filter.check("фильтр"))  # true
bloom_filter.delete_from_filter("фильтр")
print(bloom_filter.check("фильтр"))  # false
