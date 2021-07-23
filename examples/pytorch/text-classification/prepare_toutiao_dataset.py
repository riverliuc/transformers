import os
import random
import sys
import csv
from tqdm import tqdm

class_code_to_labels = {
    100: 0,
    101: 1,
    102: 2,
    103: 3,
    104: 4,
    106: 5,
    107: 6,
    108: 7,
    109: 8,
    110: 9,
    112: 10,
    113: 11,
    114: 12,
    115: 13,
    116: 14
}

def read_toutiao_whole_dataset(data_file_path):
    texts = []
    labels = []
    if not os.path.exists(data_file_path):
        raise ValueError("dataset file %s does not exist!" % data_file_path)
    
    with open(data_file_path, 'r', encoding='UTF-8') as data_file:
        lines = data_file.readlines()
        for line in lines:
            if len(line) == 0:
                continue
            line_split = line.split('_!_')
            if len(line_split) < 4:
                continue
            class_code = int(line_split[1])
            label = class_code_to_labels[class_code]
            news_text = line_split[3]

            texts.append(news_text)
            labels.append(label)

    data_pairs = list(zip(texts, labels))
    random.shuffle(data_pairs)

    texts, labels = zip(*data_pairs)
    return texts, labels

def split_train_val_test(texts, labels, output_dir, train_ratio=0.7, val_ratio=15, test_ratio=0.15):
    num_all_data = len(labels)
    num_train = int(num_all_data * 0.7)
    num_val = int(num_all_data * 0.15)
    num_test = num_all_data - num_train - num_val

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    train_file_path = os.path.join(output_dir, 'train.txt')
    val_file_path = os.path.join(output_dir, 'val.txt')
    test_file_path = os.path.join(output_dir, 'test.txt')

    with open(train_file_path, 'w', encoding='utf-8') as train_file:
        train_writer = csv.writer(train_file)

        for idx in tqdm(range(0, num_train)):
            train_writer.writerow([texts[idx], labels[idx]])
    
    with open(val_file_path, 'w', encoding='utf-8') as val_file:
        val_writer = csv.writer(val_file)

        for idx in tqdm(range(num_train, num_train + num_val)):
            val_writer.writerow([texts[idx], labels[idx]])

    with open(test_file_path, 'w', encoding='utf-8') as test_file:
        test_writer = csv.writer(test_file)

        for idx in tqdm(range(num_train + num_val, num_all_data)):
            test_writer.writerow([texts[idx], labels[idx]])

def check_raw_dataset(dataset_path):
    if not os.path.exists(dataset_path):
        raise ValueError("dataset file %s does not exist!" % dataset_path)

    output_dir = os.path.dirname(dataset_path)
    file_name = os.path.basename(dataset_path).split('.')[0]
    checked_file_name = file_name + '_set.txt'
    checked_file_path = os.path.join(output_dir, checked_file_name)

    checked_file = open(checked_file_path, 'w', encoding='utf-8')
    with open(dataset_path, 'r', encoding='utf-8') as data_file:
        csv_reader = csv.reader(data_file)
        try:
            for row in csv_reader:
                if len(row) > 2:
                    print(row)
                    raise ValueError("csv row should not contain more than 2 elements")
                text = row[0]
                label = int(row[1])
                # print(text, label)
        except:
            print(row)
    checked_file.close()

if __name__ == '__main__':
    file_path = sys.argv[1]
    output_dir = sys.argv[2]
    # print('Load dataset from %s' % file_path)
    # texts, labels = read_toutiao_whole_dataset(file_path)

    # split_train_val_test(texts, labels, output_dir)

    check_raw_dataset(os.path.join(output_dir, 'val.txt'))
