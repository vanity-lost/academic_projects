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

def updateWeights(attributeValues, y, weights, b, learningRate, length, lambdaConstant, data_weights):
    '''
    This method updates the weight of each attribute using gradient descent
    :param attributeValues: the attribute values of one example
    :param y: class labels
    :param weights: weights
    :param b: bias term
    :param learningRate: the learning rate
    :param length: the number of data
    :param lambdaConstant: lambda from the penalty term
    :param data_weights: data weight
    :return: the updated weight, bias term, the derivative dw and db
    '''
    # backpropagation for w, b
    scores = np.dot(attributeValues, weights)+b
    loss = sigmoid(scores) - y
    for i in range(len(data_weights)):
        loss[i] *= data_weights[i]
    dw = lambdaConstant * weights/length + np.dot(attributeValues.T, loss)/length
    db = np.sum(loss)/length
    weights -= learningRate * dw
    b -= learningRate * db
    
    # grad desc for equation
    return weights, b, np.mean(dw), db


def buildModel(trainingSet, attributeData, data_weights, lambdaConstant = 0.5, learningRate = 0.05, converge_changeW = 0.05, converge_changeB = 1):
    '''
    This method checks when to stop the weight update based on the converge difference for w and b
    :param trainingSet: the training data
    :param attributeData: the feature information list
    :param data_weights: data weight
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
    data_weights = np.reshape(data_weights, (len(trainingSet), 1))

    # gradient descent for equation: argmin 0.5 * w^2 * lambdaConstant + Cost Function
    while abs(changeForw) >= converge_changeW/len(trainingSet) or abs(changeForb) >= converge_changeB/len(trainingSet):
        weights, b, changeForw, changeForb = updateWeights(attributes, classy, weights, b, learningRate, len(trainingSet), lambdaConstant, data_weights)  
        # print([changeForw, changeForb])  
    return weights, b, data_weights            

def evalution(trainingData, testingSet):
    '''
    This method evaluate the testing set based on the calculated weights and bias term.
    :param traningData: information regarding the previous trained models and alpha weight
    :param testingSet: the testing set of the data
    :return: the accuracy, precision, recall
    '''
    countTP = 0
    countTN = 0
    countFP = 0
    countFN = 0
    global classLabels
    alphaSum = sum(trainingData[-1])
    for j in range(len(testingSet)-1): # for every row
        f = 0
        for i in range(len(trainingData[-1])):  # for every iteration
            if trainingData[0][i] == 0:
                break
            prediValue = trainingData[0][i][1]
            for p in range(len(trainingData[0][i][0])):
                prediValue += trainingData[0][i][0][p] * testingSet[j][p]
            classLabel = 1 if prediValue > 0 else -1
            f += classLabel * trainingData[1][i] / alphaSum
        classLabel = 1 if f > 0 else 0
        classLabels.append([testingSet[j][-1], f])
        if classLabel == 1 and testingSet[j][-1] == 1:
            countTP += 1
        if classLabel == 0 and testingSet[j][-1] == 0:
            countTN += 1
        if classLabel == 1 and testingSet[j][-1] == 0:
            countFP += 1
            # print(j)
        if classLabel == 0 and testingSet[j][-1] == 1:
            countFN += 1
            # print(j)
    # print('TP: ', countTP)
    # print('TN: ', countTN)
    # print('FP: ', countFP)
    # print('FN: ', countFN)
    return (countTP + countTN) / (countTP + countTN + countFP + countFN), countTP / (countTP + countFP), countTP / (countTP + countFN)

def calSD(listOfValues):
    '''
    This method calculates the standard deviation of the input
    :param listOfValues: a list of values
    :return: the standard deviation of the list
    '''
    return np.std(listOfValues, ddof=1)

def logreg(path, useFullSample, iterationNums):
    '''
    This method is the main method to take in all options and compute the logistic regression model.
    :param path: the path name of the file
    :param useFullSample: 1 for full sample, 0 for validation
    :param iterationNums: the number of iteration for boosting
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
    data = redefine(data, attributeData)

    if useFullSample == 0:
        folds = make_folds(data, 5)
        accuracyList = list()
        precisionList = list()
        recallList = list()
        for fold in range(len(folds)):
            trainingSet = list()
            testingSet = list()
            for j in range(len(folds)):
                if fold != j:
                    for example in folds[j]:
                        trainingSet.append(example)
                else:
                    for example in folds[j]:
                        testingSet.append(example)

            data_weight = [1/len(trainingSet)] * len(trainingSet)
            trainingData = list()
            for i in range(2):
                row = [0] * iterationNums
                trainingData.append(row)
            for m in range(iterationNums):
                weights, b, data_weight = buildModel(trainingSet, attributeData, data_weight)
                trainingData[0][m] = [weights, b]
                error = 0.0
                classLabelArr = [0] * len(trainingSet)
                for i in range(len(trainingSet)):
                    prediValue = b
                    for j in range(len(weights)):
                        prediValue += weights[j]*trainingSet[i][j]
                    classLabelArr[i] = 1 if prediValue > 0 else -1
                    trueLabel = 1 if trainingSet[i][-1] == 1 else -1
                    if classLabelArr[i] != trueLabel:
                        error += data_weight[i]
                # print('error: ', error) 
                if error == 0 or error >= 0.5:
                    break
                alpha = 0.5 * np.log((1-error)/(error))  
                trainingData[-1][m] = alpha
                for i in range(len(data_weight)):
                    trueLabel = 1 if trainingSet[i][-1] == 1 else -1
                    data_weight[i] = data_weight[i] * np.exp(-alpha * trueLabel * classLabelArr[i])
                data_weight = data_weight / sum(data_weight)
                
            accuracy, precision, recall = evalution(trainingData, testingSet)
            accuracyList.append(accuracy)
            precisionList.append(precision)
            recallList.append(recall)
        areaUnderROC, FPRs, TPRs = calcAUC(classLabels)
        return np.mean(accuracyList), calSD(accuracyList), np.mean(precisionList), calSD(precisionList), np.mean(recallList), calSD(recallList), areaUnderROC
    else:
        data_weight = [1/len(data)] * len(data)
        trainingData = list()
        for i in range(2):
            row = [0] * iterationNums
            trainingData.append(row)
        for m in range(iterationNums):
            print('Boosting... %1d / %1d' % (m+1, iterationNums))
            weights, b, data_weight = buildModel(data, attributeData, data_weight)
            trainingData[0][m] = [weights, b]
            error = 0.0
            classLabelArr = [0] * len(data)
            for i in range(len(data)):
                prediValue = b
                for j in range(len(weights)):
                    prediValue += weights[j] * data[i][j]
                classLabelArr[i] = 1 if prediValue > 0 else -1
                trueLabel = 1 if data[i][-1] == 1 else -1
                if classLabelArr[i] != trueLabel:
                    error += data_weight[i]
            print('error: ', error)
            
            if error == 0 or error >= 0.5:
                break
            alpha = 0.5 * np.log((1-error)/(error))  
            trainingData[-1][m] = alpha
            for i in range(len(data_weight)):
                trueLabel = 1 if data[i][-1] == 1 else -1
                data_weight[i] = data_weight[i] * np.exp(-alpha * trueLabel * classLabelArr[i])
            data_weight = data_weight / sum(data_weight)   
            
        accuracy, precision, recall = evalution(trainingData, data)
        areaUnderROC, FPRs, TPRs  = calcAUC(classLabels)
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
    
    return np.trapz(TPRs, FPRs), FPRs, TPRs

