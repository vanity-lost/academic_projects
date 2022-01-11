from parseData_spam import create_dataset, create_dataset_skewed
import numpy as np
import os

def cal_relevance(prior_knowledge, prior_knowledge_transfer):
    # calculate the relevance
    positive_common_prob = 0  
    positive_common_prob_transfer = 0
    negative_common_prob = 0
    negative_common_prob_transfer = 0
    positive_common_max_prob = 0  
    positive_common_max_prob_transfer = 0
    negative_common_max_prob = 0
    negative_common_max_prob_transfer = 0

    for word in prior_knowledge.keys():
        if word in prior_knowledge_transfer.keys():
            positive_common_prob += prior_knowledge[word][0]
            positive_common_prob_transfer += prior_knowledge_transfer[word][0]
            negative_common_prob += prior_knowledge[word][1]
            negative_common_prob_transfer += prior_knowledge_transfer[word][1]
            if prior_knowledge[word][0] > positive_common_max_prob:
                positive_common_max_prob = prior_knowledge[word][0]
            if prior_knowledge_transfer[word][0] > positive_common_max_prob_transfer:
                positive_common_max_prob_transfer = prior_knowledge_transfer[word][0]
            if prior_knowledge[word][1] > negative_common_max_prob:
                negative_common_max_prob = prior_knowledge[word][1]
            if prior_knowledge_transfer[word][1] > negative_common_max_prob_transfer:
                negative_common_max_prob_transfer = prior_knowledge_transfer[word][1]
    
    positive_max_prob = 0
    negative_max_prob = 0
    positive_sum_prob = 0
    negative_sum_prob = 0

    for word in prior_knowledge.keys():
        positive_sum_prob += prior_knowledge[word][0]
        negative_sum_prob += prior_knowledge[word][1]
        if prior_knowledge[word][0] > positive_max_prob:
            positive_max_prob = prior_knowledge[word][0]
        if prior_knowledge[word][1] > negative_max_prob:
            negative_max_prob = prior_knowledge[word][1]

    positive_max_prob_transfer = 0
    negative_max_prob_transfer = 0
    positive_sum_prob_transfer = 0
    negative_sum_prob_transfer = 0

    for word in prior_knowledge_transfer.keys():
        positive_sum_prob_transfer += prior_knowledge_transfer[word][0]
        negative_sum_prob_transfer += prior_knowledge_transfer[word][1]
        if prior_knowledge_transfer[word][0] > positive_max_prob_transfer:
            positive_max_prob_transfer = prior_knowledge_transfer[word][0]
        if prior_knowledge_transfer[word][1] > negative_max_prob_transfer:
            negative_max_prob_transfer = prior_knowledge_transfer[word][1]
    
    positive_relevance = (positive_common_prob/positive_common_max_prob * positive_common_prob_transfer/positive_common_max_prob_transfer)/(positive_sum_prob/positive_max_prob * positive_sum_prob_transfer/positive_max_prob_transfer)
    negative_relevance = (negative_common_prob/negative_common_max_prob * negative_common_prob_transfer/negative_common_max_prob_transfer)/(negative_sum_prob/negative_max_prob * negative_sum_prob_transfer/negative_max_prob_transfer)

    overall_common_prob = positive_common_prob + negative_common_prob
    overall_common_prob_transfer = positive_common_prob_transfer + negative_common_prob_transfer
    overall_common_max_prob = max([positive_common_max_prob, negative_common_max_prob])
    overall_common_max_prob_transfer = max([positive_common_max_prob_transfer, negative_common_max_prob_transfer])
    overall_max_prob = max([positive_max_prob, negative_max_prob])
    overall_max_prob_transfer = max([positive_max_prob_transfer, negative_max_prob_transfer])
    overall_sum_prob = positive_sum_prob + negative_sum_prob
    overall_sum_prob_transfer = positive_sum_prob_transfer + negative_sum_prob_transfer

    overall_relevance = (overall_common_prob/overall_common_max_prob * overall_common_prob_transfer/overall_common_max_prob_transfer)/(overall_sum_prob/overall_max_prob * overall_sum_prob_transfer/overall_max_prob_transfer)
    
    return positive_relevance, negative_relevance, overall_relevance

def cal_relevance_v2(prior_knowledge, prior_knowledge_transfer):
    # apply KL algorithm
    
    positive_relevance = 0
    negative_relevance = 0
    totall_positive_prob = sum([pair[1][0] for pair in prior_knowledge.items()])
    totall_negative_prob = sum([pair[1][1] for pair in prior_knowledge.items()])
    totall_positive_prob_transfer = sum([pair[1][0] for pair in prior_knowledge_transfer.items()])
    totall_negative_prob_transfer = sum([pair[1][1] for pair in prior_knowledge_transfer.items()])
    for word in prior_knowledge_transfer:
        positive_relevance += prior_knowledge[word][0] / totall_positive_prob * np.log2((prior_knowledge[word][0] / totall_positive_prob)/(prior_knowledge_transfer[word][0] / totall_positive_prob_transfer))
        negative_relevance += prior_knowledge[word][1] / totall_negative_prob * np.log2((prior_knowledge[word][1] / totall_positive_prob)/(prior_knowledge_transfer[word][1] / totall_positive_prob_transfer))
    return (positive_relevance+negative_relevance)

def cal_model(file_name, training_size, testing_size):
    training_data_table, testing_data_table = create_dataset(file_name, training_size, testing_size)
    y1_count = 0
    y0_count = 0
    for i in range(len(training_data_table)-1):
        if training_data_table[i + 1][-1] == 1:
            y1_count += 1
        else:
            y0_count += 1
    if len(training_data_table) != 1:
        y1_prob = y1_count/(len(training_data_table)-1)
        y0_prob = y0_count/(len(training_data_table)-1)
    else:
        y1_prob = 0.5
        y0_prob = 0.5

    prior_knowledge = dict()
    vocabulary = len(training_data_table[0])
    word_num_y1 = 0
    word_num_y0 = 0
    for i in range(len(training_data_table)-1):
        if training_data_table[i+1][-1] == 1:
            word_num_y1 += sum(training_data_table[i+1])-1
        else:
            word_num_y0 += sum(training_data_table[i+1])


    for i in range(len(training_data_table[0])):
        x1_count = 0
        x0_count = 0
        for j in range(len(training_data_table)-1):
            if training_data_table[j+1][-1] == 1:
                x1_count += training_data_table[j+1][i]
            else:
                x0_count += training_data_table[j+1][i]
        prob_x = [(x1_count+1)/(word_num_y1+vocabulary), (x0_count+1)/(word_num_y0+vocabulary)]
        prior_knowledge[training_data_table[0][i]] = prob_x
    return y1_prob, y0_prob, prior_knowledge, training_data_table, testing_data_table

def cal_direct_accuracy(testing_data_table_transfer, y1_prob, y0_prob, prior_knowledge):
    correct_count = 0
    for i in range(1, len(testing_data_table_transfer)):
        prob_Y1 = np.log(y1_prob)
        prob_Y0 = np.log(y0_prob)
        for j in range(len(testing_data_table_transfer[0])):
            if testing_data_table_transfer[0][j] in prior_knowledge.keys():
                [probX_Y1, probX_Y0] = prior_knowledge[testing_data_table_transfer[0][j]]
                prob_Y1 += np.log(probX_Y1) * testing_data_table_transfer[i][j]
                prob_Y0 += np.log(probX_Y0) * testing_data_table_transfer[i][j]
        predicted_class_label = 1 if prob_Y1 >= prob_Y0 else 0
        if predicted_class_label == testing_data_table_transfer[i][-1]:
            correct_count += 1
    accuracy = correct_count / (len(testing_data_table_transfer)-1)
    return accuracy

def NB_relevant_NB_retraining(postive_folder_path, negative_folder_path, training_size, testing_size, postive_folder_path_transfer, negative_folder_path_transfer, training_size_transfer, testing_size_transfer):
    # pre-trained model
    y1_prob, y0_prob, prior_knowledge, training_data_table, testing_data_table = cal_model(postive_folder_path, negative_folder_path, training_size, testing_size)
    print('Pre-model is built')
    
    # the current small model
    y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer, training_data_table_transfer, testing_data_table_transfer = cal_model(postive_folder_path_transfer, negative_folder_path_transfer, training_size_transfer, testing_size_transfer)
    print('Target-model is built')
    
    accuracy_original = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer)
    print('accuracy(no_transfer): ', accuracy_original)
    
    accuracy_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    print('accuracy(directly_transfer): ', accuracy_transfer)
    
    positive_relevance, negative_relevance, prior_overall_relevance = cal_relevance(prior_knowledge, prior_knowledge_transfer)
    print('overall_relevance: ', prior_overall_relevance)
    
    # merge new words of current model into pre-model
    for word in prior_knowledge_transfer.keys():
        if word not in prior_knowledge.keys():
            prior_knowledge[word] = prior_knowledge_transfer[word]
    
    positive_relevance, negative_relevance, overall_relevance = cal_relevance(prior_knowledge, prior_knowledge_transfer)
    print('overall_relevance: ', overall_relevance)
    
    if overall_relevance - prior_overall_relevance >= 0.1:
        print('Retraining (step 1) start...')
        common_pair = [[pair[0], pair[1][0], pair[1][1]] for pair in prior_knowledge.items() if pair[0] in prior_knowledge_transfer.keys()]
        common_pair.sort(key = lambda x:x[1], reverse=True)
        top_positive_words = [pair[0] for pair in common_pair[0:int(len(common_pair)/10)]]
        common_pair.sort(key = lambda x:x[2], reverse=True)
        top_negative_words = [pair[0] for pair in common_pair[0:int(len(common_pair)/10)]]
        for word in prior_knowledge.keys():
            if word in top_positive_words or word in top_negative_words:
                if word in prior_knowledge_transfer.keys():
                    [probX_Y1, probX_Y0] = prior_knowledge[word]
                    [probX_Y1_transfer, probX_Y0_transfer] = prior_knowledge_transfer[word]
                    probX_Y1 += (probX_Y1_transfer - probX_Y1) * 0.01
                    probX_Y0 += (probX_Y0_transfer - probX_Y0) * 0.01
                    prior_knowledge[word] = [probX_Y1, probX_Y0]
                else:
                    [probX_Y1, probX_Y0] = prior_knowledge[word]
                    probX_Y1 += (0.5 - probX_Y1) * 0.01
                    probX_Y0 += (0.5 - probX_Y0) * 0.01
                    prior_knowledge[word] = [probX_Y1, probX_Y0]
        print('Retraining (step 1) end...')
    positive_relevance, negative_relevance, overall_relevance = cal_relevance(prior_knowledge, prior_knowledge_transfer)
    print('overall_relevance: ', overall_relevance)
    
    prior_overall_relevance = 1
    
    if positive_relevance > overall_relevance:
        negative_learning_rate = 0.05
        positive_learning_rate = 0.01
    if negative_relevance > overall_relevance:
        positive_learning_rate = 0.05
        negative_learning_rate = 0.01
    
    print('Retraining (step 2) start...')
    while abs(prior_overall_relevance - overall_relevance) >= 0.00001:        
        for word in prior_knowledge.keys():
            if word in prior_knowledge_transfer.keys():
                [probX_Y1, probX_Y0] = prior_knowledge[word]
                [probX_Y1_transfer, probX_Y0_transfer] = prior_knowledge_transfer[word]
                probX_Y1 += (probX_Y1_transfer - probX_Y1) * positive_learning_rate
                probX_Y0 += (probX_Y0_transfer - probX_Y0) * negative_learning_rate
                prior_knowledge[word] = [probX_Y1, probX_Y0]
        
        prior_overall_relevance = overall_relevance
        positive_relevance, negative_relevance, overall_relevance = cal_relevance(prior_knowledge, prior_knowledge_transfer)
        print('overall_relevance: ', overall_relevance)
        if positive_relevance > overall_relevance:
            negative_learning_rate = 0.05
            positive_learning_rate = 0.01
        if negative_relevance > overall_relevance:
            positive_learning_rate = 0.05
            negative_learning_rate = 0.01
    print('Retraining (step 2) end...')
    
    accuracy_relevant_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    print('accuracy_relevant_transfer: ', accuracy_relevant_transfer)
    return accuracy_original, accuracy_transfer, accuracy_relevant_transfer

def cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer):
    positive_chi2 = (probX_Y1/(probX_Y1+probX_Y0)-probX_Y1_transfer/(probX_Y1_transfer+probX_Y0_transfer)) ** 2 / (probX_Y1_transfer/(probX_Y1_transfer+probX_Y0_transfer))
    negative_chi2 = (probX_Y0/(probX_Y1+probX_Y0)-probX_Y0_transfer/(probX_Y1_transfer+probX_Y0_transfer)) ** 2 / (probX_Y0_transfer/(probX_Y1_transfer+probX_Y0_transfer))
    return positive_chi2, negative_chi2

def NB_relevant_NB_retraining_v2(postive_folder_path, negative_folder_path, training_size, testing_size, postive_folder_path_transfer, negative_folder_path_transfer, training_size_transfer, testing_size_transfer):
    # pre-trained model
    y1_prob, y0_prob, prior_knowledge, training_data_table, testing_data_table = cal_model(postive_folder_path, negative_folder_path, training_size, testing_size)
    print('Pre-model is built')
    
    # the current small model
    y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer, training_data_table_transfer, testing_data_table_transfer = cal_model(postive_folder_path_transfer, negative_folder_path_transfer, training_size_transfer, testing_size_transfer)
    print('Target-model is built')
    
    accuracy_original = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer)
    print('accuracy(no_transfer): ', accuracy_original)
    
    accuracy_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    print('accuracy(directly_transfer): ', accuracy_transfer)
    
    # prior_relevance = 1
    # relevance = cal_relevance_v2(prior_knowledge, prior_knowledge_transfer)
    
    print('Retraining start...')
    # while abs(prior_relevance - relevance) >= 0.0000001:
    #     for word in prior_knowledge.keys():
    #         if word in prior_knowledge_transfer.keys():
    #             [probX_Y1, probX_Y0] = prior_knowledge[word]
    #             [probX_Y1_transfer, probX_Y0_transfer] = prior_knowledge_transfer[word]
    #             positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
    #             positive_learning_rate = 0.05 if positive_chi2 > negative_chi2 else 0.01
    #             negative_learning_rate = 0.05 if positive_chi2 < negative_chi2 else 0.01
    #             overall_chi2 = max([positive_chi2, negative_chi2])
    #             prior_overall_chi2 = 0
    #             while abs(prior_overall_chi2 - overall_chi2) >= 0.0000001: 
    #                 probX_Y1 += (probX_Y1_transfer - probX_Y1) * positive_learning_rate
    #                 probX_Y0 += (probX_Y0_transfer - probX_Y0) * negative_learning_rate
    #                 prior_knowledge[word] = [probX_Y1, probX_Y0]
    #                 positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
    #                 prior_overall_chi2 = overall_chi2
    #                 overall_chi2 = max([positive_chi2, negative_chi2])
    for word in prior_knowledge.keys():
        if word in prior_knowledge_transfer.keys():
            prior_overall_chi2 = 0
            [probX_Y1, probX_Y0] = prior_knowledge[word]
            [probX_Y1_transfer, probX_Y0_transfer] = prior_knowledge_transfer[word]
            positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
            positive_learning_rate = 0.05 if positive_chi2 > negative_chi2 else 0.01
            negative_learning_rate = 0.05 if positive_chi2 < negative_chi2 else 0.01
            overall_chi2 = max([positive_chi2, negative_chi2])
            while abs(prior_overall_chi2 - overall_chi2) >= 0.0000001: 
                probX_Y1 += (probX_Y1_transfer - probX_Y1) * positive_learning_rate
                probX_Y0 += (probX_Y0_transfer - probX_Y0) * negative_learning_rate
                prior_knowledge[word] = [probX_Y1, probX_Y0]
                positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                prior_overall_chi2 = overall_chi2
                overall_chi2 = max([positive_chi2, negative_chi2])
            # print('overall_chi2: ', overall_chi2)
        else:
            [probX_Y1, probX_Y0] = prior_knowledge[word]
            prior_knowledge[word] = [probX_Y1 * 0.9, probX_Y0 * 0.9]
        # prior_relevance = relevance
        # relevance = cal_relevance_v2(prior_knowledge, prior_knowledge_transfer)
        # print(relevance)
    print('Retraining end...')
    
    # merge new words of current model into pre-model
    for word in prior_knowledge_transfer.keys():
        if word not in prior_knowledge.keys():
            prior_knowledge[word] = prior_knowledge_transfer[word]
    
    accuracy_relevant_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    print('accuracy_relevant_transfer: ', accuracy_relevant_transfer)
    return accuracy_original, accuracy_transfer, accuracy_relevant_transfer

def cal_model_skewed(training_filename_transfer, training_size_transfer, testing_size_transfer):
    training_data_table, testing_data_table = create_dataset_skewed(training_filename_transfer, training_size_transfer, testing_size_transfer)
    y1_count = 0
    y0_count = 0
    for i in range(len(training_data_table)-1):
        if training_data_table[i + 1][-1] == 1:
            y1_count += 1
        else:
            y0_count += 1
    y1_prob = y1_count/(len(training_data_table)-1)
    y0_prob = y0_count/(len(training_data_table)-1)

    prior_knowledge = dict()
    vocabulary = len(training_data_table[0])
    word_num_y1 = 0
    word_num_y0 = 0
    for i in range(len(training_data_table)-1):
        if training_data_table[i+1][-1] == 1:
            word_num_y1 += sum(training_data_table[i+1])-1
        else:
            word_num_y0 += sum(training_data_table[i+1])


    for i in range(len(training_data_table[0])):
        x1_count = 0
        x0_count = 0
        for j in range(len(training_data_table)-1):
            if training_data_table[j+1][-1] == 1:
                x1_count += training_data_table[j+1][i]
            else:
                x0_count += training_data_table[j+1][i]
        prob_x = [(x1_count+1)/(word_num_y1+vocabulary), (x0_count+1)/(word_num_y0+vocabulary)]
        prior_knowledge[training_data_table[0][i]] = prob_x
    return y1_prob, y0_prob, prior_knowledge, training_data_table, testing_data_table

def NB_relevant_NB_retraining_v2_progress(training_filename, training_size, testing_size, training_filename_transfer, training_size_transfer, testing_size_transfer):
    # pre-trained model
    y1_prob, y0_prob, prior_knowledge, training_data_table, testing_data_table = cal_model(training_filename, training_size, testing_size)
    # print('Pre-model is built')
    
    # the current small model
    y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer, training_data_table_transfer, testing_data_table_transfer = cal_model(training_filename_transfer, training_size_transfer, testing_size_transfer)
    # print('Target-model is built')
    
    accuracy_original = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer)
    # print('accuracy(no_transfer): ', accuracy_original)
    
    accuracy_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    # print('accuracy(directly_transfer): ', accuracy_transfer)
    
    accuracy_progress_list = [accuracy_transfer]
    
    # merge new words of current model into pre-model
    for word in prior_knowledge_transfer.keys():
        if word not in prior_knowledge.keys():
            prior_knowledge[word] = prior_knowledge_transfer[word]
    
    accuracy_transfer_merged = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    accuracy_progress_list.append(accuracy_transfer_merged)
    
    count = 0
    
    print('Retraining start...')
    for word in prior_knowledge.keys():
        count += 1
        if word in prior_knowledge_transfer.keys():
            prior_overall_chi2 = 0
            [probX_Y1, probX_Y0] = prior_knowledge[word]
            [probX_Y1_transfer, probX_Y0_transfer] = prior_knowledge_transfer[word]
            positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
            positive_learning_rate = 0.05 if positive_chi2 > negative_chi2 else 0.01
            negative_learning_rate = 0.05 if positive_chi2 < negative_chi2 else 0.01
            overall_chi2 = max([positive_chi2, negative_chi2])
            while abs(prior_overall_chi2 - overall_chi2) >= 0.0001: 
                probX_Y1 += (probX_Y1_transfer - probX_Y1) * positive_learning_rate
                probX_Y0 += (probX_Y0_transfer - probX_Y0) * negative_learning_rate
                prior_knowledge[word] = [probX_Y1, probX_Y0]
                positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                prior_overall_chi2 = overall_chi2
                overall_chi2 = max([positive_chi2, negative_chi2])
                # print('overall_chi2: ', overall_chi2)
        else:
            [probX_Y1, probX_Y0] = prior_knowledge[word]
            positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
            prior_relevance = 1
            positive_relevance, negative_relevance, overall_relevance = cal_relevance(prior_knowledge, prior_knowledge_transfer)
            while abs(prior_relevance - overall_relevance) >= 0.0000001: 
                probX_Y1 += (0 - probX_Y1) * 0.01
                probX_Y0 += (0 - probX_Y0) * 0.01
                prior_knowledge[word] = [probX_Y1, probX_Y0]
                prior_relevance = overall_relevance
                positive_relevance, negative_relevance, overall_relevance = cal_relevance(prior_knowledge, prior_knowledge_transfer)
        if count % 1000 == 0:
            accuracy_relevant_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
            accuracy_progress_list.append(accuracy_relevant_transfer)
            # print('accuracy_relevant_transfer: ', accuracy_relevant_transfer)
            count = 0
    # print('Retraining end...')
    
    accuracy_relevant_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    print('accuracy_relevant_transfer: ', accuracy_relevant_transfer)
    
    accuracy_original_list = [accuracy_original] * len(accuracy_progress_list)
    accuracy_transfer_list = [accuracy_transfer] * len(accuracy_progress_list)
    return accuracy_original_list, accuracy_transfer_list, accuracy_progress_list

def NB_relevant_NB_retraining_v2_model(postive_folder_path, negative_folder_path, training_paths, testing_paths):
    # pre-trained model
    y1_prob, y0_prob, prior_knowledge, training_data_table, testing_data_table = cal_model(postive_folder_path, negative_folder_path, 1200, 0)
    # print('Pre-model is built')
    
    i = 0
    while i < len(training_paths):
        # the current small model
        y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer, training_data_table_transfer, testing_data_table_transfer = cal_model(training_paths[i], training_paths[i+1], 1200, 0)
        # print('Target-model is built')
        
        # merge new words of current model into pre-model
        for word in prior_knowledge_transfer.keys():
            if word not in prior_knowledge.keys():
                prior_knowledge[word] = prior_knowledge_transfer[word]
        
        # print('Retraining start...')
        for word in prior_knowledge.keys():
            if word in prior_knowledge_transfer.keys():
                prior_overall_chi2 = 0
                [probX_Y1, probX_Y0] = prior_knowledge[word]
                [probX_Y1_transfer, probX_Y0_transfer] = prior_knowledge_transfer[word]
                positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                positive_learning_rate = 0.05 if positive_chi2 > negative_chi2 else 0.01
                negative_learning_rate = 0.05 if positive_chi2 < negative_chi2 else 0.01
                overall_chi2 = max([positive_chi2, negative_chi2])
                while abs(prior_overall_chi2 - overall_chi2) >= 0.0001: 
                    probX_Y1 += (probX_Y1_transfer - probX_Y1) * positive_learning_rate
                    probX_Y0 += (probX_Y0_transfer - probX_Y0) * negative_learning_rate
                    prior_knowledge[word] = [probX_Y1, probX_Y0]
                    positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                    prior_overall_chi2 = overall_chi2
                    overall_chi2 = max([positive_chi2, negative_chi2])
                    # print('overall_chi2: ', overall_chi2)
            else:
                [probX_Y1, probX_Y0] = prior_knowledge[word]
                prior_relevance = 1
                positive_relevance, negative_relevance, overall_relevance = cal_relevance(prior_knowledge, prior_knowledge_transfer)
                while abs(prior_relevance - overall_relevance) >= 0.0001: 
                    probX_Y1 += (0 - probX_Y1) * 0.01
                    probX_Y0 += (0 - probX_Y0) * 0.01
                    prior_knowledge[word] = [probX_Y1, probX_Y0]
                    prior_relevance = overall_relevance
                    positive_relevance, negative_relevance, overall_relevance = cal_relevance(prior_knowledge, prior_knowledge_transfer)
            # print('Retraining end...')
        i += 2
    
    accuracy_original_list = []
    accuracy_transfer_list = []
    accuracy_relevant_transfer_list = []
    
    i = 0
    while i < len(testing_paths):        
        print('Round ', i/2)
        # the current small model
        y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer, training_data_table_transfer, testing_data_table_transfer = cal_model(testing_paths[i], testing_paths[i+1], 50, 1000)
        # print('Target-model is built')
        
        accuracy_original = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer)
        # print('accuracy(no_transfer): ', accuracy_original)
        
        accuracy_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
        # print('accuracy(directly_transfer): ', accuracy_transfer)
        
        # merge new words of current model into pre-model
        for word in prior_knowledge_transfer.keys():
            if word not in prior_knowledge.keys():
                prior_knowledge[word] = prior_knowledge_transfer[word]
        
        # print('Retraining start...')
        for word in prior_knowledge.keys():
            if word in prior_knowledge_transfer.keys():
                prior_overall_chi2 = 0
                [probX_Y1, probX_Y0] = prior_knowledge[word]
                [probX_Y1_transfer, probX_Y0_transfer] = prior_knowledge_transfer[word]
                positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                positive_learning_rate = 0.05 if positive_chi2 > negative_chi2 else 0.01
                negative_learning_rate = 0.05 if positive_chi2 < negative_chi2 else 0.01
                overall_chi2 = max([positive_chi2, negative_chi2])
                while abs(prior_overall_chi2 - overall_chi2) >= 0.0001: 
                    probX_Y1 += (probX_Y1_transfer - probX_Y1) * positive_learning_rate
                    probX_Y0 += (probX_Y0_transfer - probX_Y0) * negative_learning_rate
                    prior_knowledge[word] = [probX_Y1, probX_Y0]
                    positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                    prior_overall_chi2 = overall_chi2
                    overall_chi2 = max([positive_chi2, negative_chi2])
                    # print('overall_chi2: ', overall_chi2)
            else:
                [probX_Y1, probX_Y0] = prior_knowledge[word]
                positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                prior_relevance = 1
                positive_relevance, negative_relevance, overall_relevance = cal_relevance(prior_knowledge, prior_knowledge_transfer)
                while abs(prior_relevance - overall_relevance) >= 0.0001: 
                    probX_Y1 += (0 - probX_Y1) * 0.01
                    probX_Y0 += (0 - probX_Y0) * 0.01
                    prior_knowledge[word] = [probX_Y1, probX_Y0]
                    prior_relevance = overall_relevance
                    positive_relevance, negative_relevance, overall_relevance = cal_relevance(prior_knowledge, prior_knowledge_transfer)
        # print('Retraining end...')
        
        accuracy_relevant_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
        # print('accuracy_relevant_transfer: ', accuracy_relevant_transfer)
        accuracy_original_list.append(accuracy_original)
        accuracy_transfer_list.append(accuracy_transfer)
        accuracy_relevant_transfer_list.append(accuracy_relevant_transfer)
        i += 2
    
    return accuracy_original_list, accuracy_transfer_list, accuracy_relevant_transfer_list


def NB_relevant_NB_retraining_v3(training_filename, training_size, testing_size, training_filename_transfer, training_size_transfer, testing_size_transfer):
    # pre-trained model
    y1_prob, y0_prob, prior_knowledge, training_data_table, testing_data_table = cal_model(training_filename, training_size, testing_size)
    print('Pre-model is built')
    
    # the current small model
    y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer, training_data_table_transfer, testing_data_table_transfer = cal_model(training_filename_transfer, training_size_transfer, testing_size_transfer)
    print('Target-model is built')
    
    count = 0
    count2 = 0
    for word in prior_knowledge.keys():
        if word in prior_knowledge_transfer.keys():
            count += 1
        else:
            count2 += 1
    for word in prior_knowledge_transfer.keys():
        if word not in prior_knowledge.keys():
            count2 += 1
    
    print(count)
    print(count2)
    
    accuracy_original = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer)
    print('accuracy(no_transfer): ', accuracy_original)
    
    accuracy_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    print('accuracy(directly_transfer): ', accuracy_transfer)
    
    print('Retraining start...')
    for word in prior_knowledge.keys():
        if word in prior_knowledge_transfer.keys():
            prior_overall_chi2 = 0
            [probX_Y1, probX_Y0] = prior_knowledge[word]
            [probX_Y1_transfer, probX_Y0_transfer] = prior_knowledge_transfer[word]
            positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
            positive_learning_rate = 0.05 if positive_chi2 > negative_chi2 else 0.01
            negative_learning_rate = 0.05 if positive_chi2 < negative_chi2 else 0.01
            overall_chi2 = max([positive_chi2, negative_chi2])
            while abs(prior_overall_chi2 - overall_chi2) >= 0.0000001: 
                probX_Y1 += (probX_Y1_transfer - probX_Y1) * positive_learning_rate
                probX_Y0 += (probX_Y0_transfer - probX_Y0) * negative_learning_rate
                prior_knowledge[word] = [probX_Y1, probX_Y0]
                positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                prior_overall_chi2 = overall_chi2
                overall_chi2 = max([positive_chi2, negative_chi2])
        else:
            [probX_Y1, probX_Y0] = prior_knowledge[word]
            prior_knowledge[word] = [probX_Y1 * 0.9, probX_Y0 * 0.9]
    print('Retraining end...')
    
    # merge new words of current model into pre-model
    for word in prior_knowledge_transfer.keys():
        if word not in prior_knowledge.keys():
            prior_knowledge[word] = prior_knowledge_transfer[word]
    
    accuracy_relevant_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    print('accuracy_relevant_transfer: ', accuracy_relevant_transfer)
    return accuracy_original, accuracy_transfer, accuracy_relevant_transfer

def NB_relevant_NB_retraining_v3_progress(training_filename, training_size, testing_size, training_filename_transfer, training_size_transfer, testing_size_transfer):
    # pre-trained model
    y1_prob, y0_prob, prior_knowledge, training_data_table, testing_data_table = cal_model(training_filename, training_size, testing_size)
    print('Pre-model is built')
    
    # the current small model
    y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer, training_data_table_transfer, testing_data_table_transfer = cal_model(training_filename_transfer, training_size_transfer, testing_size_transfer)
    print('Target-model is built')
    
    error_rate_list = []
    accuracy_relevant_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    error_rate_list.append(1-accuracy_relevant_transfer)
    count = 0
    
    # merge new words of current model into pre-model
    for word in prior_knowledge_transfer.keys():
        if word not in prior_knowledge.keys():
            prior_knowledge[word] = prior_knowledge_transfer[word]
    
    accuracy_relevant_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    error_rate_list.append(1-accuracy_relevant_transfer)
    
    print('Retraining start...')
    for word in prior_knowledge.keys():
        count += 1
        if word in prior_knowledge_transfer.keys():
            prior_overall_chi2 = 0
            [probX_Y1, probX_Y0] = prior_knowledge[word]
            [probX_Y1_transfer, probX_Y0_transfer] = prior_knowledge_transfer[word]
            positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
            positive_learning_rate = 0.05 if positive_chi2 > negative_chi2 else 0.01
            negative_learning_rate = 0.05 if positive_chi2 < negative_chi2 else 0.01
            overall_chi2 = max([positive_chi2, negative_chi2])
            while abs(prior_overall_chi2 - overall_chi2) >= 0.0000001: 
                probX_Y1 += (probX_Y1_transfer - probX_Y1) * positive_learning_rate
                probX_Y0 += (probX_Y0_transfer - probX_Y0) * negative_learning_rate
                prior_knowledge[word] = [probX_Y1, probX_Y0]
                positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                prior_overall_chi2 = overall_chi2
                overall_chi2 = max([positive_chi2, negative_chi2])
        else:
            [probX_Y1, probX_Y0] = prior_knowledge[word]
            prior_knowledge[word] = [probX_Y1 * 0.9, probX_Y0 * 0.9]
        if count % 2000 == 0:
            accuracy_relevant_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
            error_rate_list.append(1-accuracy_relevant_transfer)
            count = 0
            print(1-accuracy_relevant_transfer)
    print('Retraining end...')
    return error_rate_list

def cal_model_v2(training_filename, training_size, testing_size):
    training_data_table, testing_data_table = create_dataset(training_filename, training_size, testing_size)
    y1_count = 0
    y0_count = 0
    for i in range(len(training_data_table)-1):
        if training_data_table[i + 1][-1] == 1:
            y1_count += 1
        else:
            y0_count += 1
    y1_prob = y1_count/(len(training_data_table)-1)
    y0_prob = y0_count/(len(training_data_table)-1)

    prior_knowledge = dict()
    vocabulary = len(training_data_table[0])
    word_num_y1 = 0
    word_num_y0 = 0
    for i in range(len(training_data_table)-1):
        if training_data_table[i+1][-1] == 1:
            word_num_y1 += sum(training_data_table[i+1])-1
        else:
            word_num_y0 += sum(training_data_table[i+1])


    for i in range(len(training_data_table[0])):
        x1_count = 0
        x0_count = 0
        for j in range(len(training_data_table)-1):
            if training_data_table[j+1][-1] == 1:
                x1_count += training_data_table[j+1][i]
            else:
                x0_count += training_data_table[j+1][i]
        prob_x = [(x1_count+1)/(word_num_y1+vocabulary), (x0_count+1)/(word_num_y0+vocabulary)]
        prior_knowledge[training_data_table[0][i]] = prob_x
        
    score_list = []
    for i in range(len(training_data_table[0])):
        # count x y
        count00 = 0
        count01 = 0
        count10 = 0
        count11 = 0
        for j in range(len(training_data_table)-1):
            if training_data_table[j+1][-1] == 1:
                if training_data_table[j+1][i] == 0:
                    count01 += 1
                else:
                    count11 += training_data_table[j+1][i]
            else:
                if training_data_table[j+1][i] == 0:
                    count00 += 1
                else:
                    count10 += training_data_table[j+1][i]
        count_sum = count00 + count01 + count10 + count11
        expected_11 = (count11+count10)/count_sum * (count11+count01)
        expected_01 = (count01+count11)/count_sum * (count01+count00)
        expected_10 = (count10+count11)/count_sum * (count10+count00)
        expected_00 = (count00+count01)/count_sum * (count00+count10)
        chi2 = (count00-expected_00) ** 2 + (count01-expected_01) ** 2 + (count10-expected_10) ** 2 + (count11-expected_11) ** 2
        score_list.append([training_data_table[0][i], chi2])
    
    # score_list.sort(key = lambda x:x[1], reverse=True)
    # print(score_list[0:100])
    for i in range(int(len(score_list))):
        if score_list[i][1] < 10.83:
            del prior_knowledge[score_list[i][0]]
    return y1_prob, y0_prob, prior_knowledge, training_data_table, testing_data_table

def NB_relevant_NB_retraining_v3_analysis(training_filename, training_size, testing_size, training_filename_transfer, training_size_transfer, testing_size_transfer):
    # pre-trained model
    y1_prob, y0_prob, prior_knowledge, training_data_table, testing_data_table = cal_model_v2(training_filename, training_size, testing_size)
    print('Pre-model is built')
    
    # the current small model
    y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer, training_data_table_transfer, testing_data_table_transfer = cal_model(training_filename_transfer, training_size_transfer, testing_size_transfer)
    print('Target-model is built')
    
    count = 0
    count2 = 0
    for word in prior_knowledge.keys():
        if word in prior_knowledge_transfer.keys():
            count += 1
        else:
            count2 += 1
    print(count)
    print(count2)
    
    accuracy_original = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer)
    print('accuracy(no_transfer): ', accuracy_original)
    
    accuracy_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    print('accuracy(directly_transfer): ', accuracy_transfer)
    
    print('Retraining start...')
    for word in prior_knowledge.keys():
        if word in prior_knowledge_transfer.keys():
            prior_overall_chi2 = 0
            [probX_Y1, probX_Y0] = prior_knowledge[word]
            [probX_Y1_transfer, probX_Y0_transfer] = prior_knowledge_transfer[word]
            positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
            positive_learning_rate = 0.05 if positive_chi2 > negative_chi2 else 0.01
            negative_learning_rate = 0.05 if positive_chi2 < negative_chi2 else 0.01
            overall_chi2 = max([positive_chi2, negative_chi2])
            while abs(prior_overall_chi2 - overall_chi2) >= 0.0000001: 
                probX_Y1 += (probX_Y1_transfer - probX_Y1) * positive_learning_rate
                probX_Y0 += (probX_Y0_transfer - probX_Y0) * negative_learning_rate
                prior_knowledge[word] = [probX_Y1, probX_Y0]
                positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                prior_overall_chi2 = overall_chi2
                overall_chi2 = max([positive_chi2, negative_chi2])
        else:
            [probX_Y1, probX_Y0] = prior_knowledge[word]
            prior_knowledge[word] = [probX_Y1 * 0.9, probX_Y0 * 0.9]
    print('Retraining end...')
    
    # merge new words of current model into pre-model
    for word in prior_knowledge_transfer.keys():
        if word not in prior_knowledge.keys():
            prior_knowledge[word] = prior_knowledge_transfer[word]
    
    accuracy_relevant_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    print('accuracy_relevant_transfer: ', accuracy_relevant_transfer)
    return accuracy_original, accuracy_transfer, accuracy_relevant_transfer

def NB_relevant_NB_retraining_v3_model(postive_folder_path, negative_folder_path, training_paths, testing_paths):
    # pre-trained model
    y1_prob, y0_prob, prior_knowledge, training_data_table, testing_data_table = cal_model(postive_folder_path, negative_folder_path, 1200, 0)
    # print('Pre-model is built')
    
    i = 0
    while i < len(training_paths):
        # the current small model
        y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer, training_data_table_transfer, testing_data_table_transfer = cal_model(training_paths[i], training_paths[i+1], 1200, 0)
        # print('Target-model is built')
        
        # merge new words of current model into pre-model
        for word in prior_knowledge_transfer.keys():
            if word not in prior_knowledge.keys():
                prior_knowledge[word] = prior_knowledge_transfer[word]
        
        # print('Retraining start...')
        for word in prior_knowledge.keys():
            if word in prior_knowledge_transfer.keys():
                prior_overall_chi2 = 0
                [probX_Y1, probX_Y0] = prior_knowledge[word]
                [probX_Y1_transfer, probX_Y0_transfer] = prior_knowledge_transfer[word]
                positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                positive_learning_rate = 0.05 if positive_chi2 > negative_chi2 else 0.01
                negative_learning_rate = 0.05 if positive_chi2 < negative_chi2 else 0.01
                overall_chi2 = max([positive_chi2, negative_chi2])
                while abs(prior_overall_chi2 - overall_chi2) >= 0.0000001: 
                    probX_Y1 += (probX_Y1_transfer - probX_Y1) * positive_learning_rate
                    probX_Y0 += (probX_Y0_transfer - probX_Y0) * negative_learning_rate
                    prior_knowledge[word] = [probX_Y1, probX_Y0]
                    positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                    prior_overall_chi2 = overall_chi2
                    overall_chi2 = max([positive_chi2, negative_chi2])
            else:
                [probX_Y1, probX_Y0] = prior_knowledge[word]
                prior_knowledge[word] = [probX_Y1 * 0.9, probX_Y0 * 0.9]
            # print('Retraining end...')
        i += 2
    
    accuracy_original_list = []
    accuracy_transfer_list = []
    accuracy_relevant_transfer_list = []
    
    i = 0
    while i < len(testing_paths):        
        print('Round ', i/2)
        # the current small model
        y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer, training_data_table_transfer, testing_data_table_transfer = cal_model(testing_paths[i], testing_paths[i+1], 50, 1000)
        # print('Target-model is built')
        
        accuracy_original = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer)
        # print('accuracy(no_transfer): ', accuracy_original)
        
        accuracy_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
        # print('accuracy(directly_transfer): ', accuracy_transfer)
        
        # merge new words of current model into pre-model
        for word in prior_knowledge_transfer.keys():
            if word not in prior_knowledge.keys():
                prior_knowledge[word] = prior_knowledge_transfer[word]
        
        # print('Retraining start...')
        for word in prior_knowledge.keys():
            if word in prior_knowledge_transfer.keys():
                prior_overall_chi2 = 0
                [probX_Y1, probX_Y0] = prior_knowledge[word]
                [probX_Y1_transfer, probX_Y0_transfer] = prior_knowledge_transfer[word]
                positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                positive_learning_rate = 0.05 if positive_chi2 > negative_chi2 else 0.01
                negative_learning_rate = 0.05 if positive_chi2 < negative_chi2 else 0.01
                overall_chi2 = max([positive_chi2, negative_chi2])
                while abs(prior_overall_chi2 - overall_chi2) >= 0.0000001: 
                    probX_Y1 += (probX_Y1_transfer - probX_Y1) * positive_learning_rate
                    probX_Y0 += (probX_Y0_transfer - probX_Y0) * negative_learning_rate
                    prior_knowledge[word] = [probX_Y1, probX_Y0]
                    positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                    prior_overall_chi2 = overall_chi2
                    overall_chi2 = max([positive_chi2, negative_chi2])
            else:
                [probX_Y1, probX_Y0] = prior_knowledge[word]
                prior_knowledge[word] = [probX_Y1 * 0.9, probX_Y0 * 0.9]
        # print('Retraining end...')
        
        accuracy_relevant_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
        # print('accuracy_relevant_transfer: ', accuracy_relevant_transfer)
        accuracy_original_list.append(accuracy_original)
        accuracy_transfer_list.append(accuracy_transfer)
        accuracy_relevant_transfer_list.append(accuracy_relevant_transfer)
        i += 2
    
    return accuracy_original_list, accuracy_transfer_list, accuracy_relevant_transfer_list

def NB_relevant_NB_retraining_v5(training_filename, training_size, testing_size, training_filename_transfer, training_size_transfer, testing_size_transfer):
    # pre-trained model
    y1_prob, y0_prob, prior_knowledge, training_data_table, testing_data_table = cal_model(training_filename, training_size, testing_size)
    print('Pre-model is built')
    
    # the current small model
    y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer, training_data_table_transfer, testing_data_table_transfer = cal_model(training_filename_transfer, training_size_transfer, testing_size_transfer)
    print('Target-model is built')
    
    count = 0
    count2 = 0
    for word in prior_knowledge.keys():
        if word in prior_knowledge_transfer.keys():
            count += 1
        else:
            count2 += 1
    for word in prior_knowledge_transfer.keys():
        if word not in prior_knowledge.keys():
            count2 += 1
    
    print(count)
    print(count2)
    
    prob_rank = []
    for word in prior_knowledge.keys():
        row = []
        [probX_Y1, probX_Y0] = prior_knowledge[word]
        probX_Y1 = probX_Y1/(probX_Y1+probX_Y0)
        prob_rank.append([probX_Y1, word])
    prob_rank.sort(key = lambda x:x[0], reverse=True)
    positive_table = [pair[1] for pair in prob_rank[:int(len(prob_rank)/10)]]
    negative_table = [pair[1] for pair in prob_rank[int(9*len(prob_rank)/10):]]
    
    accuracy_original = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer)
    print('accuracy(no_transfer): ', accuracy_original)
    
    accuracy_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    print('accuracy(directly_transfer): ', accuracy_transfer)
    
    print('Retraining start...')
    for word in prior_knowledge.keys():
        if word in positive_table or word in negative_table:
            if word in prior_knowledge_transfer.keys():
                prior_overall_chi2 = 0
                [probX_Y1, probX_Y0] = prior_knowledge[word]
                [probX_Y1_transfer, probX_Y0_transfer] = prior_knowledge_transfer[word]
                positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                positive_learning_rate = 0.05 if positive_chi2 > negative_chi2 else 0.01
                negative_learning_rate = 0.05 if positive_chi2 < negative_chi2 else 0.01
                overall_chi2 = max([positive_chi2, negative_chi2])
                original_probX_Y1 = probX_Y1
                original_probX_Y0 = probX_Y1
                while abs(prior_overall_chi2 - overall_chi2) >= 0.0000001: 
                    probX_Y1 += (probX_Y1_transfer - probX_Y1) * positive_learning_rate
                    probX_Y0 += (probX_Y0_transfer - probX_Y0) * negative_learning_rate
                    prior_knowledge[word] = [probX_Y1, probX_Y0]
                    
                    positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                    prior_overall_chi2 = overall_chi2
                    overall_chi2 = max([positive_chi2, negative_chi2])
            else:
                [probX_Y1, probX_Y0] = prior_knowledge[word]
                prior_knowledge[word] = [probX_Y1 * 0.9, probX_Y0 * 0.9]
    print('Retraining end...')
    
    # merge new words of current model into pre-model
    for word in prior_knowledge_transfer.keys():
        if word not in prior_knowledge.keys():
            prior_knowledge[word] = prior_knowledge_transfer[word]
    
    accuracy_relevant_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    print('accuracy_relevant_transfer: ', accuracy_relevant_transfer)
    return accuracy_original, accuracy_transfer, accuracy_relevant_transfer

def NB_relevant_NB_retraining_v5_progress(training_filename, training_size, testing_size, training_filename_transfer, training_size_transfer, testing_size_transfer):
    # pre-trained model
    y1_prob, y0_prob, prior_knowledge, training_data_table, testing_data_table = cal_model_skewed(training_filename, training_size, testing_size)
    print('Pre-model is built')
    
    # the current small model
    y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer, training_data_table_transfer, testing_data_table_transfer = cal_model(training_filename_transfer, training_size_transfer, testing_size_transfer)
    print('Target-model is built')
    
    error_rate_list = []
    accuracy_relevant_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    error_rate_list.append(1-accuracy_relevant_transfer)
    count = 0
    
    prob_rank = []
    for word in prior_knowledge.keys():
        row = []
        [probX_Y1, probX_Y0] = prior_knowledge[word]
        probX_Y1 = probX_Y1/(probX_Y1+probX_Y0)
        prob_rank.append([probX_Y1, word])
    prob_rank.sort(key = lambda x:x[0], reverse=True)
    positive_table = [pair[1] for pair in prob_rank[:int(len(prob_rank)/10)]]
    negative_table = [pair[1] for pair in prob_rank[int(9*len(prob_rank)/10):]]
    
    # merge new words of current model into pre-model
    for word in prior_knowledge_transfer.keys():
        if word not in prior_knowledge.keys():
            prior_knowledge[word] = prior_knowledge_transfer[word]
    
    accuracy_relevant_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    error_rate_list.append(1-accuracy_relevant_transfer)
    
    print('Retraining start...')
    for word in prior_knowledge.keys():
        count += 1
        if word in positive_table or word in negative_table:
            if word in prior_knowledge_transfer.keys():
                prior_overall_chi2 = 0
                [probX_Y1, probX_Y0] = prior_knowledge[word]
                [probX_Y1_transfer, probX_Y0_transfer] = prior_knowledge_transfer[word]
                positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                positive_learning_rate = 0.05 if positive_chi2 > negative_chi2 else 0.01
                negative_learning_rate = 0.05 if positive_chi2 < negative_chi2 else 0.01
                overall_chi2 = max([positive_chi2, negative_chi2])
                while abs(prior_overall_chi2 - overall_chi2) >= 0.0000001: 
                    probX_Y1 += (probX_Y1_transfer - probX_Y1) * positive_learning_rate
                    probX_Y0 += (probX_Y0_transfer - probX_Y0) * negative_learning_rate
                    prior_knowledge[word] = [probX_Y1, probX_Y0]
                    positive_chi2, negative_chi2 = cal_chi2(probX_Y1, probX_Y0, probX_Y1_transfer, probX_Y0_transfer)
                    prior_overall_chi2 = overall_chi2
                    overall_chi2 = max([positive_chi2, negative_chi2])
            else:
                [probX_Y1, probX_Y0] = prior_knowledge[word]
                prior_knowledge[word] = [probX_Y1 * 0.9, probX_Y0 * 0.9]
        if count % 2000 == 0:
            accuracy_relevant_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
            error_rate_list.append(1-accuracy_relevant_transfer)
            count = 0
            print(1-accuracy_relevant_transfer)
    print('Retraining end...')
    return error_rate_list

def NB_relevant_NB_retraining_v4(training_filename, training_size, testing_size, training_filename_transfer, training_size_transfer, testing_size_transfer):
    # pre-trained model
    y1_prob, y0_prob, prior_knowledge, training_data_table, testing_data_table = cal_model(training_filename, training_size, testing_size)
    print('Pre-model is built')
    
    # the current small model
    y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer, training_data_table_transfer, testing_data_table_transfer = cal_model(training_filename_transfer, training_size_transfer, testing_size_transfer)
    print('Target-model is built')
    
    count = 0
    count2 = 0
    for word in prior_knowledge.keys():
        if word in prior_knowledge_transfer.keys():
            count += 1
        else:
            count2 += 1
    print(count)
    print(count2)
    
    accuracy_original = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer)
    print('accuracy(no_transfer): ', accuracy_original)
    
    accuracy_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    print('accuracy(directly_transfer): ', accuracy_transfer)
    
    # merge new words of current model into pre-model
    for word in prior_knowledge_transfer.keys():
        if word not in prior_knowledge.keys():
            prior_knowledge[word] = prior_knowledge_transfer[word]
    
    print('Retraining start...')
    similarity = cal_relevance_v2(prior_knowledge, prior_knowledge_transfer)
    prior_similarity = 1
    while abs(prior_similarity - similarity) >= 0.000001:
        for word in prior_knowledge.keys():
            if word in prior_knowledge_transfer.keys():
                [probX_Y1, probX_Y0] = prior_knowledge[word]
                [probX_Y1_transfer, probX_Y0_transfer] = prior_knowledge_transfer[word]
                probX_Y1 += (probX_Y1_transfer - probX_Y1) * 0.01
                probX_Y0 += (probX_Y0_transfer - probX_Y0) * 0.01
                prior_knowledge[word] = [probX_Y1, probX_Y0]
                prior_similarity = similarity
                similarity = cal_relevance_v2(prior_knowledge, prior_knowledge_transfer)
    print('Retraining end...')
    
    accuracy_relevant_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    print('accuracy_relevant_transfer: ', accuracy_relevant_transfer)
    return accuracy_original, accuracy_transfer, accuracy_relevant_transfer

def NB_relevant_NB_model(top_folder_path):
    # pre-trained model
    y1_prob, y0_prob, prior_knowledge, training_data_table, testing_data_table = cal_model(postive_folder_path, negative_folder_path, training_size, testing_size)
    # print('Pre-model is built')
    
    # the current small model
    y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer, training_data_table_transfer, testing_data_table_transfer = cal_model(postive_folder_path_transfer, negative_folder_path_transfer, training_size_transfer, testing_size_transfer)
    # print('Target-model is built')
    
    # merge new words of current model into pre-model
    for word in prior_knowledge_transfer.keys():
        if word not in prior_knowledge.keys():
            prior_knowledge[word] = prior_knowledge_transfer[word]
    
    prior_overall_relevance = 1
    
    positive_relevance, negative_relevance, overall_relevance = cal_relevance(prior_knowledge, prior_knowledge_transfer)
    # print('overall_relevance: ', overall_relevance)
    if positive_relevance > overall_relevance:
        negative_learning_rate = 0.05
        positive_learning_rate = 0.01
    if negative_relevance > overall_relevance:
        positive_learning_rate = 0.05
        negative_learning_rate = 0.01
    
    # print('Retraining start...')
    while abs(prior_overall_relevance - overall_relevance) >= 0.00001:        
        for word in prior_knowledge.keys():
            if word in prior_knowledge_transfer.keys():
                [probX_Y1, probX_Y0] = prior_knowledge[word]
                [probX_Y1_transfer, probX_Y0_transfer] = prior_knowledge_transfer[word]
                probX_Y1 += (probX_Y1_transfer - probX_Y1) * positive_learning_rate
                probX_Y0 += (probX_Y0_transfer - probX_Y0) * negative_learning_rate
                prior_knowledge[word] = [probX_Y1, probX_Y0]
        
        prior_overall_relevance = overall_relevance
        positive_relevance, negative_relevance, overall_relevance = cal_relevance(prior_knowledge, prior_knowledge_transfer)
        if positive_relevance > overall_relevance:
            negative_learning_rate = 0.05
            positive_learning_rate = 0.01
        if negative_relevance > overall_relevance:
            positive_learning_rate = 0.05
            negative_learning_rate = 0.01
    # print('Retraining end...')
    
    accuracy_relevant_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    # print('accuracy_relevant_transfer: ', accuracy_relevant_transfer)
    return y1_prob, y0_prob, prior_knowledge

def NB_relevant_NB(case_id, y1_prob, y0_prob, prior_knowledge, y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer, testing_data_table_transfer):
    # merge new words of current model into pre-model
    for word in prior_knowledge_transfer.keys():
        if word not in prior_knowledge.keys():
            prior_knowledge[word] = prior_knowledge_transfer[word]
    
    common_pair = [[pair[0], pair[1][0], pair[1][1]] for pair in prior_knowledge.items() if pair[0] in prior_knowledge_transfer.keys()]
    common_pair.sort(key = lambda x:x[1], reverse=True)
    top_positive_words = [pair[0] for pair in common_pair[0:int(len(common_pair)/4)]]
    common_pair.sort(key = lambda x:x[2], reverse=True)
    top_negative_words = [pair[0] for pair in common_pair[0:int(len(common_pair)/4)]]
    for word in top_positive_words:
        prior_knowledge[word][0] = prior_knowledge_transfer[word][0]
    for word in top_negative_words:
        prior_knowledge[word][1] = prior_knowledge_transfer[word][1]
    
    correct_count_transfer = 0
    for i in range(1, len(testing_data_table_transfer)):
        prob_Y1 = np.log((y1_prob+y1_prob_transfer)/2)
        prob_Y0 = np.log((y0_prob+y0_prob_transfer)/2)
        for j in range(len(testing_data_table_transfer[0])):
            if testing_data_table_transfer[0][j] in prior_knowledge.keys():
                [probX_Y1, probX_Y0] = prior_knowledge[testing_data_table_transfer[0][j]]              
                prob_Y1 += np.log(probX_Y1) * testing_data_table_transfer[i][j]
                prob_Y0 += np.log(probX_Y0) * testing_data_table_transfer[i][j]
        predicted_class_label = 1 if prob_Y1 >= prob_Y0 else 0
        if predicted_class_label == testing_data_table_transfer[i][-1]:
            correct_count_transfer += 1
    accuracy_relevant_transfer = correct_count_transfer / (len(testing_data_table_transfer)-1)
    return accuracy_relevant_transfer

def NB_relevance_accuracy(postive_folder_path, negative_folder_path, training_size, testing_size, postive_folder_path_transfer, negative_folder_path_transfer, training_size_transfer, testing_size_transfer):
    # pre-trained model
    y1_prob, y0_prob, prior_knowledge, training_data_table, testing_data_table = cal_model(postive_folder_path, negative_folder_path, training_size, testing_size)
    
    # the current small model
    y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer, training_data_table_transfer, testing_data_table_transfer = cal_model(postive_folder_path_transfer, negative_folder_path_transfer, training_size_transfer, testing_size_transfer)
    
    positive_relevance, negative_relevance, overall_relevance = cal_relevance(prior_knowledge, prior_knowledge_transfer)
    print('positive_relevance: ', positive_relevance)
    print('negative_relevance: ', negative_relevance)
    print('overall_relevance: ', overall_relevance)
    
    case_id = 0
    
    if overall_relevance > 0.8:
        case_id = 1
    elif positive_relevance < 0.5:
        case_id = 2
    elif negative_relevance < 0.5:
        case_id = 3
    
    accuracy_original = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge_transfer)
    print('accuracy(no_transfer): ', accuracy_original)
    
    accuracy_transfer = cal_direct_accuracy(testing_data_table_transfer, y1_prob_transfer, y0_prob_transfer, prior_knowledge)
    print('accuracy(directly_transfer): ', accuracy_transfer)

    accuracy_relevant_transfer = NB_relevant_NB(case_id, y1_prob, y0_prob, prior_knowledge, y1_prob_transfer, y0_prob_transfer,prior_knowledge_transfer, testing_data_table_transfer)
    print('accuracy(relevant_transfer): ', accuracy_relevant_transfer)
