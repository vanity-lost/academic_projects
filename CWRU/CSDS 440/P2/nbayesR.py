import re
import random
import sys
import numpy as np

# divide the dataset to five folds using stratified cross validation
from mldata import parse_c45, _find_file, _parse_values

classLabels = list()


def make_bins(data, attributeData, binNumber):
    '''
    This method discretizes continuous values by partition the range of the feature into k bins.
    :param data: the original data
    :param attributeData: the list containing information about each attribute
    :param binNumber: the number of bins we want to partition
    :return: the updated data with discretized continuous values
    '''
    for i in range(len(attributeData)):
        if attributeData[i][0]:
            min = 0
            max = 0
            for example in data:
                if example[i] > max:
                    max = example[i]
                if example[i] < min:
                    min = example[i]
            rangeOfAttribute = max - min
            binSize = rangeOfAttribute / binNumber
            for example in data:
                value = example[i]
                example[i] = (value - min) // binSize + 1 if value != max else binNumber
    return data


def make_folds(data, fold_number):
    '''
    This method partition data into desired number of folds with equal class labels in each fold.
    :param data: the original data
    :param fold_number: the number of fold
    :return: a list containing each fold
    '''
    classLabel0 = list()
    classLabel1 = list()
    for example in data:
        if example[-1] == 1:
            classLabel1.append(example)
        else:
            classLabel0.append(example)
    random.seed(12345)
    folds = []
    for i in range(fold_number):
        folds.append(list())

    count1 = int(len(classLabel1) / 5)
    count0 = int(len(classLabel0) / 5)

    for j in range(fold_number - 1):
        for rIndex in range(count1):
            randIndex = random.randint(0, len(classLabel1)-1)
            folds[j].append(classLabel1[randIndex])
            classLabel1.pop(randIndex)
    folds[-1].extend(classLabel1)

    for j in range(fold_number - 1):
        for rIndex in range(count0):
            randIndex = random.randint(0, len(classLabel0)-1)
            folds[j].append(classLabel0[randIndex])
            classLabel0.pop(randIndex)
    folds[-1].extend(classLabel0)

    return folds


def retrieveAttributeValues(numBins, file_base, rootdir='.'):
    '''
    This method uses the .name file to extract the feature information.
    :param numBins: the number of bins we want to partition for continuous attributes
    :param file_base: name of the file base
    :param rootdir: name of the root directory
    :return: a list containing information about each attribute
    '''
    attributeList = list()
    schema_name = file_base + '.names'
    schema_filename = _find_file(schema_name, rootdir)
    if schema_filename is None:
        raise ValueError('Schema file not found')
        return None
    with open(schema_filename) as schema_file:
        for line in schema_file:
            line = re.sub('//.*', '', line)
            line = line.strip()
            if len(line) > 0 and line[-1] == '.':
                line = line[:-1].strip()
            if len(line) == 0:
                continue
            colon = line.find(':')
            if colon > 0:
                attribute = list()
                name = line[:colon].strip()
                if name == 'index':
                    continue
                remainder = line[colon + 1:]
                values = _parse_values(remainder)
                if (len(values) == 1 and values[0].startswith('continuous')
                    ) or len(values) > 10:
                    attribute.append(True)
                    valueList = list(range(1, numBins + 1))
                    attribute.append(valueList)
                else:
                    attribute.append(False)
                    valueList = to_float(values)
                    attribute.append(valueList)
                attributeList.append(attribute)
    return attributeList

def to_float(values):
    '''
    This method turns the nominal attribute into integer
    :param values: a list of attribute value in string
    :return: a list of attribute value in integer
    '''
    list = []
    for i in range(len(values)):
        list.append(i)
    return list

def calSD(listOfValues):
    '''
    This method calculates the standard deviation of the input
    :param listOfValues: a list of values
    :return: the standard deviation of the list
    '''
    return np.std(listOfValues, ddof=1)

def chi2selection(data, attributeData, k):
    '''
    This method uses chi square test to find the best k attributes and update the data.
    :param data: the original data
    :param attributeData: the original attributeData list containing the feature information
    :param k: the number of attribute we want to keep
    :return: the updated data and attributeData with k best attributes
    '''
    attribute_chisquare = list()
    total_num = len(attributeData) * 2
    for i in range(len(attributeData)):
        attri_num = dict()
        yes_num = 0
        no_num = 0
        for example in data:
            if example[i] not in attri_num:
                if example[-1] == 1:
                    attri_num[example[i]] = [1,0,1]
                    yes_num += 1
                else:
                    attri_num[example[i]] = [0,1,1]
                    no_num += 1
            else:
                attri_num[example[i]][2] += 1
                if example[-1] == 1:
                    attri_num[example[i]][0] += 1
                    yes_num += 1
                else:
                    attri_num[example[i]][1] += 1
                    no_num += 1
        chi2_score = 0.0
        for key in attri_num:
            pair = attri_num[key]
            expected_freq_yes = pair[-1]/total_num * yes_num
            expected_freq_no = pair[-1]/total_num * no_num
            chi2_score += (pair[0]-expected_freq_yes) ** 2 / expected_freq_yes
            chi2_score += (pair[1]-expected_freq_no) ** 2 / expected_freq_no
        
        attribute_chisquare.append([i, chi2_score])
    
    sortedValue = sorted(attribute_chisquare, key=lambda x: x[1])
    attributeIndexes = list()
    for i in range(len(attributeData) - k):
        attributeIndexes.append(sortedValue[i][0])
    attributeIndexes = sorted(attributeIndexes, reverse = True)

    for example in data:  
        for index in attributeIndexes:
            example.pop(index)

    for index in attributeIndexes:  
        attributeData.pop(index)

    return data, attributeData


def NaiveBayes(path, useFullSample, numBins, mEstimateNum, k):
    '''
    This method is the main method to take in all options and compute the naive bayes model.
    :param path: the path name of the file
    :param useFullSample: 1 for full sample, 0 for validation
    :param numBins: the number of bins we want to partition for continuous attributes
    :param mEstimateNum: if negative, laplace smoothing. if 0, MLE. if positive, m-estimate
    :param k: the number of attributes we want to use
    :return: accuracy, precision, recall, and AUC of the model
    '''
    import os
    rootdir, file_base = os.path.split(path)
    rootdir = rootdir[1:] if rootdir[1:] != '' else '.'
    attributeData = retrieveAttributeValues(numBins, file_base, rootdir)
    # convert to list of list here
    data = (parse_c45(file_base, rootdir)).to_float()
    for example in data:
        example.pop(0)
    data = make_bins(data, attributeData, numBins)

    data, attributeData = chi2selection(data, attributeData, k)

    if useFullSample == 0:
        folds = make_folds(data, 5)
        # TODO: track of accuracy, precision, recall, areaUnderROC
        accuracyList = list()
        precisionList = list()
        recallList = list()
        for i in range(len(folds)):
            trainingSet = list()
            testingSet = list()
            for j in range(len(folds)):
                if i != j:
                    for example in folds[j]:
                        trainingSet.append(example)
                else:
                    for example in folds[j]:
                        testingSet.append(example)

            y0Num, y1Num, probY0, probY1 = calLabelProb(trainingSet)
            knowledgeTable = calKnowledge(trainingSet, attributeData, y0Num,
                                          y1Num, mEstimateNum)
            accuracy, precision, recall = checkExample(
                testingSet, knowledgeTable, probY0, probY1)
            accuracyList.append(accuracy)
            precisionList.append(precision)
            recallList.append(recall)
        areaUnderROC = calcAUC(classLabels)
        return np.mean(accuracyList), calSD(accuracyList), np.mean(precisionList), calSD(precisionList), np.mean(recallList), calSD(recallList), areaUnderROC
    else:
        y0Num, y1Num, probY0, probY1 = calLabelProb(data)
        knowledgeTable = calKnowledge(data, attributeData, y0Num, y1Num,
                                      mEstimateNum)
        accuracy, precision, recall = checkExample(
                data, knowledgeTable, probY0, probY1)
        areaUnderROC = calcAUC(classLabels)
        return accuracy, 0, precision, 0, recall, 0, areaUnderROC


def calLabelProb(trainingSet):
    '''
    This method calculates the the class label probability.
    :param trainingSet: the training data
    :return: the number of each class label and the probability of each class label
    '''
    # calculate the P(y=0) and P(y=1)
    y0Num = 0
    y1Num = 0
    for example in trainingSet:
        if example[-1] == 1:
            y1Num = y1Num + 1
        else:
            y0Num = y0Num + 1
    return y0Num, y1Num, y0Num / len(trainingSet), y1Num / len(trainingSet)


def calKnowledge(trainingSet, attributeData, y0Num, y1Num, m):
    '''
    This method calculates the knowledge of each attribute.
    :param trainingSet: the training data
    :param attributeData: the list containing feature information
    :param y0Num: the number of class label = 0 in the training data
    :param y1Num: the number of class label = 1 in the training data
    :param m: if negative, laplace smoothing. if 0, MLE. if positive, m-estimate
    :return: a knowledge table containing all information about each attribute
    '''
    # calculate the knowledge table learned farom trainingSet
    knowledgeTable = list()
    for attributeIndex in range(len(attributeData)):
        # calculate the P(Xi=xi | Y = 0) and P(Xi=xi | Y = 1) with m-estimate
        attributeValues = attributeData[attributeIndex][1]
        v = len(attributeValues)
        p = 1 / v
        probX = dict()
        for value in attributeValues:
            xiGiveny0Num = len([
                ex for ex in trainingSet
                if ex[attributeIndex] == value and ex[-1] == 0
            ])
            xiGiveny1Num = len([
                ex for ex in trainingSet
                if ex[attributeIndex] == value and ex[-1] == 1
            ])
            if m >= 0:
                probX[value] = [(xiGiveny0Num + m * p) / (y0Num + m),
                                (xiGiveny1Num + m * p) / (y1Num + m)]
            else:
                probX[value] = [(xiGiveny0Num + 1) / (y0Num + v),
                                (xiGiveny1Num + 1) / (y1Num + v)]
        knowledgeTable.append(probX)
    return knowledgeTable


def checkExample(testingSet, knowledgeTable, probY0, probY1):
    '''
    This method tests the model using the testing data.
    :param testingSet: the testing data
    :param knowledgeTable: the knowledge table containing all information about each attribute
    :param probY0: the probability of class label = 0
    :param probY1: the probability of class label = 1
    :return: accuracy, recall, precision
    '''
    countTP = 0
    countTN = 0
    countFP = 0
    countFN = 0
    global classLabels
    for example in testingSet:
        guessY0 = np.log2(probY0)
        guessY1 = np.log2(probY1)
        for attributeIndex in range(len(example) - 1):
            probXi = knowledgeTable[attributeIndex].get(
                example[attributeIndex])
            guessY0 = guessY0 + np.log2(probXi[0])
            guessY1 = guessY1 + np.log2(probXi[1])
        classLabel = 1 if guessY0 < guessY1 else 0
        classLabels.append([example[-1], 2 ** (guessY1)/(2 ** (guessY1)+2 ** (guessY0))])
        #print(classLabel)
        if classLabel == 1 and example[-1] == 1:
            countTP += 1
        if classLabel == 0 and example[-1] == 0:
            countTN += 1
        if classLabel == 1 and example[-1] == 0:
            countFP += 1
        if classLabel == 0 and example[-1] == 1:
            countFN += 1
    #print()
    #print(len(classLabels))
    #print(classLabels)
    #print(countTP)
    #print(countTN)
    #print(countFP)
    #print(countFN)
    return (countTP + countTN) / (
        countTP + countTN + countFP + countFN), countTP / (
            countTP + countFP), countTP / (countTP + countFN)


def calcAUC(classLabels):
    '''
    This method calculates the AUC for the ROC curve.
    :param classLabels: the class label of the original data
    :return: AUC of the ROC curve
    '''
    countFP = 0
    countTN = 0

    countTP = 0
    countFN = 0
    classLabels = sorted(classLabels, key=lambda x: (x[1]), reverse=True)
    #print(classLabels)
    for i in range(len(classLabels)):
        if classLabels[i][0] == 0:
            countTN += 1
        if classLabels[i][0] == 1:
            countFN += 1
            
    listFPRtoTPR = list()
    
    FPR = 0
    TPR = 0
    listFPRtoTPR.append([FPR, TPR])
    for i in range(len(classLabels)):
        if classLabels[i][0] == 0:
            countFP += 1
            countTN -= 1
        if classLabels[i][0] == 1:
            countTP += 1
            countFN -= 1
        FPR = countFP / (countFP + countTN) if countFP + countTN != 0 else 0
        TPR = countTP / (countTP + countFN) if countTP + countFN != 0 else 0
        listFPRtoTPR.append([FPR, TPR])
    #listFPRtoTPR.sort()
    listFPRtoTPR = sorted(listFPRtoTPR,key=lambda x: (x[1]))
    FPRs = list()
    TPRs = list()
    for row in listFPRtoTPR:
        FPRs.append(row[0])
        TPRs.append(row[1])
    #print(FPRs)
    #print(TPRs)
    return np.trapz(TPRs, FPRs)

def main(**Option):
    # the format of input: python main.py /folder/filename 0/1 >=2 m
    # Option 1 is the path, Option 2 is cross validation/full example, Option 3 is number of Bins, Option 4 is the value of m fro m-estimate
    path = sys.argv[1]
    useFullSample = int(sys.argv[2])
    numBins = int(sys.argv[3])
    mEstimateNum = float(sys.argv[4])
    accuracy, accuracySD, precision, precisionSD, recall, recallSD, areaUnderROC = NaiveBayes(
        path, useFullSample, numBins, mEstimateNum)

    print('Accuracy: %.03f %.03f' % (accuracy, accuracySD))
    print('Precision: %.03f %.03f' % (precision, precisionSD))
    print('Recall: %.03f %.03f' % (recall, recallSD))
    print('Area Under ROC: %.03f' % (areaUnderROC))
