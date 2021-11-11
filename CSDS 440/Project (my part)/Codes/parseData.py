import sys
import os
import re
import random

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

def update_bags(text, bag_of_words):
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

def open_file(filepath):
    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting ...".format(filepath))
        sys.exit()
    
    bag_of_words = {}
    with open(filepath) as fp:
        for line in fp:
            update_bags(line.strip(), bag_of_words)
    
    return bag_of_words

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

def create_dataset(postive_folder_path, negative_folder_path, training_size, testing_size):
    training_bags = [0] * training_size
    testing_bags = [0] * testing_size
    random.seed(12345)
    training_half = int(training_size/2)
    testing_half = int(testing_size/2)
    filenames = random.sample(os.listdir(postive_folder_path), training_half+testing_half)
    for i in range(training_half):
        file_path = os.path.join(postive_folder_path, filenames[i])
        training_bags[i] = open_file(file_path)
    for i in range(testing_half):
        file_path = os.path.join(postive_folder_path, filenames[training_half + i])
        testing_bags[i] = open_file(file_path)
    
    filenames = random.sample(os.listdir(negative_folder_path), training_half+testing_half)
    for i in range(training_half):
        file_path = os.path.join(negative_folder_path, filenames[i])
        training_bags[training_half+i] = open_file(file_path)
    for i in range(testing_half):
        file_path = os.path.join(negative_folder_path, filenames[training_half + i])
        testing_bags[testing_half+i] = open_file(file_path)
    
    training_label = [1] * training_half + [0] * training_half
    testing_label = [1] * testing_half + [0] * testing_half
    
    training_data_table = create_data_table(training_bags, training_label)
    testing_data_table = create_data_table(testing_bags, testing_label)
    
    return training_data_table, testing_data_table

def create_dataset_skewed(postive_folder_path, negative_folder_path, training_size, testing_size):
    training_bags = [0] * training_size
    testing_bags = [0] * testing_size
    random.seed(12345)
    training_half = int(training_size/5)
    testing_half = int(testing_size/5)
    filenames = random.sample(os.listdir(postive_folder_path), training_half+testing_half)
    for i in range(training_half):
        file_path = os.path.join(postive_folder_path, filenames[i])
        training_bags[i] = open_file(file_path)
    for i in range(testing_half):
        file_path = os.path.join(postive_folder_path, filenames[training_half + i])
        testing_bags[i] = open_file(file_path)
    
    filenames = random.sample(os.listdir(negative_folder_path), 4*training_half+4*testing_half)
    for i in range(4*training_half):
        file_path = os.path.join(negative_folder_path, filenames[i])
        training_bags[training_half+i] = open_file(file_path)
    for i in range(4*testing_half):
        file_path = os.path.join(negative_folder_path, filenames[training_half + i])
        testing_bags[testing_half+i] = open_file(file_path)
    
    training_label = [1] * training_half + [0] * 4*training_half
    testing_label = [1] * testing_half + [0] * 4*testing_half
    
    training_data_table = create_data_table(training_bags, training_label)
    testing_data_table = create_data_table(testing_bags, testing_label)
    
    return training_data_table, testing_data_table

# def main():
#     training_data_table, testing_data_table = create_dataset("./20news-18828/comp.os.ms-windows.misc", "./20news-18828/comp.sys.ibm.pc.hardware")
    
# if __name__ == '__main__':
#     main()