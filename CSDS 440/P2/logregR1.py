import re
import random
import sys
import numpy as np

# divide the dataset to five folds using stratified cross validation
from mldata import parse_c45, _find_file, _parse_values

classLabels = list()

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

#normalize discrete and continuous attribute
def redefine(data, attributeData):
    '''
    This method normalizes all the attributes.
    :param data: the original data
    :param attributeData: the list that contains all information about the attribute
    :return: the updated data
    '''
    for i in range(len(attributeData)):
        attributeValue = [data[j][i] for j in range(len(data))]
        mean = np.mean(attributeValue)
        std = np.std(attributeValue, ddof=1)
        for example in data:
            example[i] = (example[i]-mean)/std
    return data

def retrieveAttributeValues(file_base, rootdir='.'):
    '''
    This method uses the .name file to extract the feature information.
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
                else:
                    attribute.append(False)
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

def sigmoid(scores):
    '''
    This method calculates the sigmoid function based on wx + b
    :param scores: the value of wx + b
    :return: the value of the calculation
    '''
    return 1 / (1 + np.exp(-scores))

def updateWeights(attributeValues, y, weights, b, learningRate, length, lambdaConstant):
    '''
    This method updates the weight of each attribute using gradient descent
    :param attributeValues: the attribute values of one example
    :param y: class labels
    :param weights: weights
    :param b: bias term
    :param learningRate: the learning rate
    :param length: the number of data
    :param lambdaConstant: lambda from the penalty term
    :return: the updated weight, bias term, the derivative dw and db
    '''
    # backpropagation for w, b
    scores = np.dot(attributeValues, weights)+b
    sigma = sigmoid(scores)
    dw = lambdaConstant * weights/length + np.dot(attributeValues.T, (sigma - y))/length
    db = np.sum(sigma - y)/length
    weights -= learningRate * dw
    b -= learningRate * db
    
    # grad desc for equation
    return weights, b, min(dw), db


def buildModel(trainingSet, attributeData, lambdaConstant, learningRate = 0.1, converge_changeW = 0.0001, converge_changeB = 0.01):
    '''
    This method checks when to stop the weight update based on the converge difference for w and b
    :param trainingSet: the training data
    :param attributeData: the feature information list
    :param lambdaConstant: lambda from the penalty term
    :param learningRate: the learning rate
    :param converge_changeW: the converge difference for w
    :param converge_changeB: the converge difference for b
    :return: the updated weight and bias term
    '''
    weights = list(np.zeros(len(attributeData)))
    b = 0
    changeForw = 1
    changeForb = 1
    attributes = list()
    classy = list()
    for ex in trainingSet:
        attributes.extend(ex[:-1])
        classy.append(ex[-1])
    attributes = np.reshape(attributes, (len(trainingSet), len(attributeData)))
    classy = np.reshape(classy, (len(trainingSet), 1))
    weights = np.reshape(weights, (len(weights), 1))

    # gradient descent for equation: argmin 0.5 * w^2 * lambdaConstant + Cost Function
    while abs(changeForw) >= converge_changeW or abs(changeForb) >= converge_changeB:
        weights, b, changeForw, changeForb = updateWeights(attributes, classy, weights, b, learningRate, len(trainingSet), lambdaConstant)
    return weights, b

def evalution(testingSet, weights, b):
    '''
    This method evaluate the testing set based on the calculated weights and bias term.
    :param testingSet: the testing set of the data
    :param weights: the weights
    :param b: the bias term
    :return: the accuracy, precision, recall
    '''
    countTP = 0
    countTN = 0
    countFP = 0
    countFN = 0
    global classLabels
    for example in testingSet:
        prediValue = b
        for i in range(len(weights)):
            prediValue += weights[i]*example[i]
        classLabel = 1 if prediValue > 0 else 0
        classLabels.append([example[-1], 1/(1+np.exp(-prediValue+2*b))])
        if classLabel == 1 and example[-1] == 1:
            countTP += 1
        if classLabel == 0 and example[-1] == 0:
            countTN += 1
        if classLabel == 1 and example[-1] == 0:
            countFP += 1
        if classLabel == 0 and example[-1] == 1:
            countFN += 1
    return (countTP + countTN) / (countTP + countTN + countFP + countFN), countTP / (countTP + countFP), countTP / (countTP + countFN)

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

def Logregression(path, useFullSample, lambdaConstant, k):
    '''
    This method is the main method to take in all options and compute the logistic regression model.
    :param path: the path name of the file
    :param useFullSample: 1 for full sample, 0 for validation
    :param lambdaConstant: lambda constant for the penalty term
    :param k: the number of best k attributes
    :return: accuracy, precision, recall, and AUC of ROC curve
    '''
    import os
    rootdir, file_base = os.path.split(path)
    rootdir = rootdir[1:] if rootdir[1:] != '' else '.'
    attributeData = retrieveAttributeValues(file_base, rootdir)
    # convert to list of list here
    data = (parse_c45(file_base, rootdir)).to_float()
    for example in data:
        example.pop(0)

    data, attributeData = chi2selection(data, attributeData, k)

    data = redefine(data, attributeData)    

    if useFullSample == 0:
        folds = make_folds(data, 5)
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

            weights, b = buildModel(trainingSet, attributeData, lambdaConstant)
            accuracy, precision, recall = evalution(testingSet, weights, b)
            accuracyList.append(accuracy)
            precisionList.append(precision)
            recallList.append(recall)
        areaUnderROC = calcAUC(classLabels)
        return np.mean(accuracyList), calSD(accuracyList), np.mean(precisionList), calSD(precisionList), np.mean(recallList), calSD(recallList), areaUnderROC
    else:
        weights, b = buildModel(data, attributeData, lambdaConstant)
        accuracy, precision, recall = evalution(data, weights, b)
        areaUnderROC = calcAUC(classLabels)
        return accuracy, 0, precision, 0, recall, 0, areaUnderROC

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
    lambdaConstant = float(sys.argv[3])
    accuracy, accuracySTD, precision, precisionSTD, recall, recallSTD, areaUnderROC = Logregression(path, useFullSample, lambdaConstant)

    print('Accuracy: %.03f %.03f' % (accuracy, accuracySTD))
    print('Precision: %.03f %.03f' % (precision, precisionSTD))
    print('Recall: %.03f %.03f' % (recall, recallSTD))
    print('Area Under ROC: %.03f' % (areaUnderROC))
