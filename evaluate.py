import os


def read_clusters(filename):
    clusters = [set()]
    with open(filename) as file:
        for line in file:
            if line == "\n":
                pass
            elif line == "##########\n":
                clusters.append(set())
            else:
                clusters[-1].add(line)
    return clusters


def precision_recall_f1(correct_clusters, clusters):
    true_positive = 0
    false_positive = 0
    false_negative = 0
    for c1 in correct_clusters:
        best = set()
        for c2 in clusters:
            common = c1 & c2
            if len(common) > len(best):
                best = c2
        success = len(c1 & best)
        true_positive += success
        false_positive += len(best) - success
        false_negative += len(c1) - success

    # print((true_positive, false_positive, false_negative))
    precision = (1.0 * true_positive) / (true_positive + false_positive)
    recall = (1.0 * true_positive) / (true_positive + false_negative)
    f1 = 2 * (1.0 * precision * recall) / (precision + recall)
    return precision, recall, f1


# read data
correct_clusters = read_clusters('data/clusters.txt')
result_filenames = []
for dirname, dirnames, filenames in os.walk('data/results'):
    if filenames:
        result_filenames = [os.path.join(dirname, filename) for filename in filenames]

for filename in result_filenames:
    clusters = read_clusters(filename)
    print(filename)
    print(precision_recall_f1(correct_clusters, clusters))