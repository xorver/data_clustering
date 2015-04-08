import collections
import math
import re

ignored_chars = {'$', ',', '.', ':', ';', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\\', '`', '\'', '+', '-',
                 '*', '/', '<', '>', '^', '%', '=', '?', '!', '(', ')', '[', ']', '{', '}', '_', '"', '&', '~'}
ignored_patterns = {'ltd', 'inn', 'kpp', 'sp', 'z', 'zo', 'zoo', 'o', 'tel', 'fax', 'sa', 'nip', 'ul', 'spolka',
                    'komandytowa', 'co', 'llc', 'inn', 'company', 'address', 'build', 'building', 'lit', 'a',
                    'h', 'str', 'pom', 'litera', 'office', 'mobile', 'email', 'post', 'postal', 'code', 'street',
                    'pic', 'flat', 'gsm', 'floor', 'eori', 'pl', 'no', 'phone', 'eax', 'lit', 'b', 'litb', 'regon',
                    'no', 'c', 'o', 'city', 'room', 'unit', 'mid', 'zone', 'town', 'district', 'nip', 'lok', 'line',
                    'of', 't', 'r', 'i', 'plc', 'th', 'd', 'a', 'g', 'st', 'bld', 'ui', 'n', 'd', "e-mail", 'roku',
                    'nr', 'm', 'k', 'koff', 'off', 'f', 'bld', 'zip', 'ph'}


def normalize_text(text):
    text = text.lower()
    for pattern in ignored_patterns:
        text = re.sub(r"(?<=[^\w]|\d)%s(?=[^\w]|\d)" % pattern, '', text)
    for pattern in ignored_chars:
        text = re.sub(re.escape(pattern), '', text)
    text = re.sub(r" +", ' ', text)
    return text


def ngram_vector(text, n=2):
    vector = collections.Counter()
    for string in normalize_text(text).split():
        chars = list(string)
        for i in range(len(chars) - n + 1):
            vector.update(tuple(chars[i: i+n]))
    return vector


def norm(x):
    return math.sqrt(dot_product(x, x))


def dot_product(x, y):
    return sum(map(lambda ngram: x[ngram] * y[ngram], list(x | y)))


def dice(x, y):
    return 1 - (2.0 * norm(x & y)) / (norm(x) + norm(y))


def cosine(x, y):
    return 1 - (1.0 * dot_product(x, y)) / (norm(x) * norm(y))


# read input
with open("data/lines.txt") as file:
    lines = file.readlines()
normalized_lines = map(lambda x: normalize_text(x), lines)
ngrams = map(lambda x: ngram_vector(x), normalized_lines)

for x in range(1, 15):
    alpha = (1.0 * x)/100
    all = set()
    clusters = []
    for i in range(len(ngrams)):
        if not (i in all):
            all.add(i)
            clusters.append({i})
            for j in range(i, len(ngrams)):
                if (not (j in all)) and dice(ngrams[i], ngrams[j]) < alpha:
                    all.add(j)
                    clusters[-1].add(j)
    with open("data/result_"+str(x), "wx") as file:
        for cluster in clusters:
            for m in cluster:
                file.write(lines[m])
            file.write("\n##########\n")