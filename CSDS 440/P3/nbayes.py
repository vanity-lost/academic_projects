import re
import random
import sys
import numpy as np

# divide the dataset to five folds using stratified cross validation
from mldata import parse_c45, _find_file, _parse_values

classLabels = list()


def nbayes(path, useFullSample, iterationNums, numBins=16, mEstimateNum=-1):
    '''
    This method is the main method to take in all options and compute the naive bayes model with Adaboost.
    :param path: the path name of the file
    :param useFullSample: 1 for full sample, 0 for validation
    :param iterationNums: the number of iterations
    :param numBins: the number of bins = 16
    :param mEstimateNum: negative, so use laplace smoothing
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
    
    if useFullSample == 0:
        folds = make_folds(data, 5)
        accuracyList = list()
        precisionList = list()
        recallList = list()
        sumOfAreaUnderROC = 0.0
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
                probY0, probY1 = calLabelProb(trainingSet, data_weight)
                knowledgeTable = calKnowledge(trainingSet, attributeData, probY0, probY1, mEstimateNum, data_weight)
                
                trainingData[0][m] = [knowledgeTable, probY0, probY1]
                error = 0.0
                classLabelArr = [0] * len(trainingSet)
                for i in range(len(trainingSet)):
                    guessY0 = np.log(probY0)
                    guessY1 = np.log(probY1)
                    for attributeIndex in range(len(trainingSet[i]) - 1):
                        probXi = knowledgeTable[attributeIndex].get(trainingSet[i][attributeIndex])
                        guessY0 += np.log(probXi[0])
                        guessY1 += np.log(probXi[1])
                    classLabelArr[i] = 1 if guessY0 < guessY1 else -1
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

            accuracy, precision, recall = checkExample(
                testingSet, trainingData)
            accuracyList.append(accuracy)
            precisionList.append(precision)
            recallList.append(recall)
        areaUnderROC = calcAUC(classLabels)
        return np.mean(accuracyList), calSD(accuracyList), np.mean(precisionList), calSD(precisionList), np.mean(recallList), calSD(recallList), areaUnderROC
    else:
        data_weight = [1/len(data)] * len(data)
        trainingData = list()
        for i in range(2):
            row = [0] * iterationNums
            trainingData.append(row)
        for m in range(iterationNums):
            probY0, probY1 = calLabelProb(data, data_weight)
            knowledgeTable = calKnowledge(data, attributeData, probY0, probY1, mEstimateNum, data_weight)
            
            trainingData[0][m] = [knowledgeTable, probY0, probY1]
            error = 0.0
            classLabelArr = [0] * len(data)
            for i in range(len(data)):
                guessY0 = np.log(probY0)
                guessY1 = np.log(probY1)
                for attributeIndex in range(len(data[i]) - 1):
                    probXi = knowledgeTable[attributeIndex].get(data[i][attributeIndex])
                    guessY0 += np.log(probXi[0])
                    guessY1 += np.log(probXi[1])
                classLabelArr[i] = 1 if guessY0 < guessY1 else -1
                trueLabel = 1 if data[i][-1] == 1 else -1
                if classLabelArr[i] != trueLabel:
                    error += data_weight[i]
            # print('error: ', error) 
            if error == 0 or error >= 0.5:
                break
            alpha = 0.5 * np.log((1-error)/(error))  
            trainingData[-1][m] = alpha
            for i in range(len(data_weight)):
                trueLabel = 1 if data[i][-1] == 1 else -1
                data_weight[i] = data_weight[i] * np.exp(-alpha * trueLabel * classLabelArr[i])
            data_weight = data_weight / sum(data_weight)   

        accuracy, precision, recall = checkExample(data, trainingData)
        areaUnderROC = calcAUC(classLabels)
        return accuracy, 0, precision, 0, recall, 0, areaUnderROC

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
                example[i] = (value - min) // binSize + \
                    1 if value != max else binNumber
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

def calLabelProb(trainingSet, dataWeights):
    '''
    This method calculates the the class label probability with data weight.
    :param trainingSet: the training data
    :param dataWeights: the weight for each row of the dataset
    :return: the number of each class label and the probability of each class label
    '''
    # calculate the P(y=0) and P(y=1)
    probY0 = 0
    probY1 = 0

    for i in range(len(trainingSet)):
        if trainingSet[i][-1] == 1:
            probY1 += dataWeights[i]
        else:
            probY0 += dataWeights[i]
    return probY0, probY1


def calKnowledge(trainingSet, attributeData, probY0, probY1, m, dataWeights):
    '''
    This method calculates the knowledge of each attribute with data weight.
    :param trainingSet: the training data
    :param attributeData: the list containing feature information
    :param y0Num: the number of class label = 0 in the training data
    :param y1Num: the number of class label = 1 in the training data
    :param m: negative, so use laplace smoothing
    :param dataWeights: the weight for each row of the dataset
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
            xiGiveny0Num = 0
            xiGiveny1Num = 0
            for i in range(len(trainingSet)):
                if (trainingSet[i][attributeIndex] == value and trainingSet[i][-1] == 0):
                    xiGiveny0Num += dataWeights[i]
                if (trainingSet[i][attributeIndex] == value and trainingSet[i][-1] == 1):
                    xiGiveny1Num += dataWeights[i]
            if m >= 0:
                probX[value] = [(xiGiveny0Num + m * p) / (probY0 + m),
                                (xiGiveny1Num + m * p) / (probY1 + m)]
            else:
                probX[value] = [(xiGiveny0Num * len(trainingSet) + 1) / (probY0 * len(trainingSet) + v),
                                (xiGiveny1Num * len(trainingSet) + 1) / (probY1 * len(trainingSet) + v)]
        knowledgeTable.append(probX)
        # print(knowledgeTable)
    return knowledgeTable


def checkExample(testingSet, trainingData):
    '''
    This method tests the model using the testing data.
    :param testingSet: the testing data
    :param trainingData: first row is all classifier,  e.g. we have trainingData[0][m] = [knowledgeTable, probY0, probY1]
        second row is the classifier weight, coloumn is the i'th iteration
    :return: accuracy, recall, precision
    '''
    countTP = 0
    countTN = 0
    countFP = 0
    countFN = 0
    global classLabels
    alphaSum = sum(trainingData[-1])
    for j in range(len(testingSet)): # for every row
        f = 0
        for i in range(len(trainingData[-1])):  # for every iteration
            if (trainingData[0][i] == 0):
                break
            guessY0 = np.log(trainingData[0][i][1])
            guessY1 = np.log(trainingData[0][i][2])
            for attributeIndex in range(len(testingSet[j]) - 1):
                probXi = trainingData[0][i][0][attributeIndex].get(testingSet[j][attributeIndex])
                guessY0 = guessY0 + np.log(probXi[0])
                guessY1 = guessY1 + np.log(probXi[1])
            classLabel = 1 if guessY0 < guessY1 else -1
            f += classLabel * trainingData[1][i] / alphaSum
        classLabel = 1 if f > 0 else 0
        classLabels.append([testingSet[j][-1], f])
        if classLabel == 1 and testingSet[j][-1] == 1:
            countTP += 1
        if classLabel == 0 and testingSet[j][-1] == 0:
            countTN += 1
        if classLabel == 1 and testingSet[j][-1] == 0:
            countFP += 1
        if classLabel == 0 and testingSet[j][-1] == 1:
            countFN += 1
    # print('TP: ', countTP)
    # print('TN: ', countTN)
    # print('FP: ', countFP)
    # print('FN: ', countFN)
    return (countTP + countTN) / (countTP + countTN + countFP + countFN), countTP / (countTP + countFP), countTP / (countTP + countFN)


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
    # print(classLabels)
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
    # listFPRtoTPR.sort()
    listFPRtoTPR = sorted(listFPRtoTPR, key=lambda x: (x[1]))
    FPRs = list()
    TPRs = list()
    for row in listFPRtoTPR:
        FPRs.append(row[0])
        TPRs.append(row[1])
    # print(FPRs)
    # print(TPRs)
    return np.trapz(TPRs, FPRs)
