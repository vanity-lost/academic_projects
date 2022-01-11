import os
import json
import gzip
import re

def update_bags(line):
    bag_of_word = dict()
    split = line.split(" ")
    for word_count in split[1:]:
        word, count_str = word_count.split(":")
        count = int(count_str)
        bag_of_word[word] = count
    label = int(split[0])
    bool_label = 1 if label == 1 else 0
    return bag_of_word, bool_label

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
    with open(file_name) as fp:
        for line in fp:
            bag_of_words, class_label = update_bags(line)
            if class_label == 1 and positive_num < half_size:
                if positive_num < half_training_size:
                    training_bags_of_words.append(bag_of_words)
                    training_class_labels.append(class_label)
                else:
                    testing_bags_of_words.append(bag_of_words)
                    testing_class_labels.append(class_label)
                positive_num += 1
            if class_label == 0 and negative_num < half_size:
                if negative_num < half_training_size:
                    training_bags_of_words.append(bag_of_words)
                    training_class_labels.append(class_label)
                else:
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

def open_file_skewed(file_name, training_size, testing_size):    
    training_bags_of_words = []
    training_class_labels = []
    testing_bags_of_words = []
    testing_class_labels = []
    half_training_size_positive = int(training_size/5)
    half_training_size_negative = training_size - half_training_size_positive
    half_testing_size_positive = int(testing_size/2)
    half_testing_size_negative = testing_size - half_testing_size_positive
    half_size_positive = half_training_size_positive + half_testing_size_positive
    half_size_negative = half_training_size_negative + half_testing_size_negative
    positive_num = 0
    negative_num = 0
    with open(file_name) as fp:
        for line in fp:
            bag_of_words, class_label = update_bags(line)
            if class_label == 1 and positive_num < half_size_positive:
                if positive_num < half_training_size_positive:
                    training_bags_of_words.append(bag_of_words)
                    training_class_labels.append(class_label)
                else:
                    testing_bags_of_words.append(bag_of_words)
                    testing_class_labels.append(class_label)
                positive_num += 1
            if class_label == 0 and negative_num < half_size_negative:
                if negative_num < half_training_size_negative:
                    training_bags_of_words.append(bag_of_words)
                    training_class_labels.append(class_label)
                else:
                    testing_bags_of_words.append(bag_of_words)
                    testing_class_labels.append(class_label)
                negative_num += 1
            if positive_num >= half_size_positive and negative_num >= half_size_negative:
                break
    return training_bags_of_words, training_class_labels, testing_bags_of_words, testing_class_labels

def create_dataset_skewed(file_name, training_size, testing_size):
    training_bags_of_words, training_class_labels, testing_bags_of_words, testing_class_labels = open_file_skewed(file_name, training_size, testing_size)
    training_data_table = create_data_table(training_bags_of_words, training_class_labels)
    testing_data_table = create_data_table(testing_bags_of_words, testing_class_labels)

    return training_data_table, testing_data_table