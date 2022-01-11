import os
import json
import gzip
import re
def text_cleaner(text):
    words = re.split(r'\W+', text)
    import string
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in words]
    
    stop_list = []
    with open('C:/Users/rando/OneDrive/Working/transfer learning/terrier-stop.txt') as fp:
        for line in fp:
            word = line.strip().split(' ')[0]
            stop_list.append(word)
    for word in words:
        if word.lower() in stop_list:
            del word
    return words

def update_bags(text):
    bag_of_words = dict()
    words = text_cleaner(text)
    if words is None:
        return
    
    for word in words:
        word = re.sub(r'\W+', '', word)
        if word != ' ':
            if word.lower() in bag_of_words:
                bag_of_words[word.lower()] += 1
            else:
                bag_of_words[word.lower()] = 1
    return bag_of_words

def open_file(file_name, training_size, testing_size):    
    training_bags_of_words = []
    training_class_labels = []
    testing_bags_of_words = []
    testing_class_labels = []
    half_training_size = int(training_size/2)
    half_testing_size = int(testing_size/2)
    half_size = int((training_size+testing_size)/2)
    positive_num = 0
    negative_num = 0
    with gzip.open(file_name) as fp:
        for line in fp:
            data = json.loads(line.strip())
            class_label = 1 if data['overall'] >= 2.5 else 0
            if class_label == 1 and positive_num < half_size:
                if 'reviewText' in data.keys():
                    if positive_num < half_training_size:
                        bag_of_words = update_bags(data['reviewText'].strip())
                        training_bags_of_words.append(bag_of_words)
                        training_class_labels.append(class_label)
                    else:
                        bag_of_words = update_bags(data['reviewText'].strip())
                        testing_bags_of_words.append(bag_of_words)
                        testing_class_labels.append(class_label)
                    positive_num += 1
            if class_label == 0 and negative_num < half_size:
                if 'reviewText' in data.keys():
                    if negative_num < half_training_size:
                        bag_of_words = update_bags(data['reviewText'].strip())
                        training_bags_of_words.append(bag_of_words)
                        training_class_labels.append(class_label)
                    else:
                        bag_of_words = update_bags(data['reviewText'].strip())
                        testing_bags_of_words.append(bag_of_words)
                        testing_class_labels.append(class_label)
                    negative_num += 1
            if positive_num >= half_size and negative_num >= half_size:
                break
    return training_bags_of_words, training_class_labels, testing_bags_of_words, testing_class_labels

def create_data_table(bags, class_labels):
    data_table = list()
    for i in range(len(bags) + 1):
        row = list()
        data_table.append(row)
    
    for i in range(len(bags)):
        for word in bags[i]:
            if word in data_table[0]:
                data_table[i+1][data_table[0].index(word)] += bags[i][word]
            else:
                data_table[0].append(word)
                for j in range(len(bags)):
                    data_table[j+1].append(0)
                data_table[i+1][-1] += 1
    for i in range(len(bags)):
        data_table[i+1].append(class_labels[i])
    return data_table

def create_dataset(file_name, training_size, testing_size):
    training_bags_of_words, training_class_labels, testing_bags_of_words, testing_class_labels = open_file(file_name, training_size, testing_size)
    training_data_table = create_data_table(training_bags_of_words, training_class_labels)
    testing_data_table = create_data_table(testing_bags_of_words, testing_class_labels)

    return training_data_table, testing_data_table