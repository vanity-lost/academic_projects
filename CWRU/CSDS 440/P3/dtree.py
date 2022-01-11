import numpy as np
from operator import itemgetter
from mldata import parse_c45, _parse_c45, _find_file, _parse_values
import random
import sys
import re

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
            randIndex = random.randint(0, len(classLabel1) - 1)
            folds[j].append(classLabel1[randIndex])
            classLabel1.pop(randIndex)
    folds[-1].extend(classLabel1)

    for j in range(fold_number - 1):
        for rIndex in range(count0):
            randIndex = random.randint(0, len(classLabel0) - 1)
            folds[j].append(classLabel0[randIndex])
            classLabel0.pop(randIndex)
    folds[-1].extend(classLabel0)

    return folds


# build the decision tree model and return the evaluation of the model based on the input
# path specifies the name of the file
# crossValidation should be inpt as an int, 0 indicates cross validation, 1 indicates full sample
# maxDepthLimit should be input as an int, 0 is no depth limit, any other positive integer is the model's max depth
# gainRatio should be input as an int, 0 is information gain, 1 is gain ratio
def dtree(path, crossValidation, iterationNums, maxDepthLimit=1, gainRatio=0):
    '''
    This method builds the decision tree model and return the evaluation of the model based on the input
    :param path: name of the file
    :param crossValidation: 0 indicates cross validation, 1 indicates full sample
    :param iterationNums: number of iteratiosn for boosting
    :param maxDepthLimit: 0 is no depth limit, any other positive integer is the model's max depth
    :param gainRatio: 0 is no depth limit, any other positive integer is the model's max depth
    :return: accuracy, accuracy std, precision, precision std, recall, recall std, auc, auc std
    '''
    import os
    rootdir, file_base = os.path.split(path)
    rootdir = rootdir[1:] if rootdir[1:] != '' else '.'
    # convert to list of list here
    data = (parse_c45(file_base, rootdir)).to_float()  # 0.0 is -, 1.0 is 0, 2.0 is +
    for example in data:
        example.pop(0)

    if crossValidation == 0:
        folds = make_folds(data, 5)
        accuracyList = []
        precisionList = []
        recallList = []
        aucList = []
        for i in range(len(folds)):
            print('Cross Validation: %3d / 5' % (i+1))
            trainingSet = list()
            testingSet = list()
            attributeData = retrieveAttributeType(file_base, rootdir)
            for j in range(len(folds)):
                if i != j:
                    for example in folds[j]:
                        trainingSet.append(example)
                else:
                    for example in folds[j]:
                        testingSet.append(example)
            dataWeights = [1 / len(trainingSet)] * len(trainingSet)
            alphaWeights = []
            tree = []
            for m in range(iterationNums):
                print('Boosting... %3d / %3d' % (m+1, iterationNums))
                attributeData = retrieveAttributeType(file_base, rootdir)
                dTree = decisionTree(trainingSet, maxDepthLimit, gainRatio, attributeData, dataWeights)
                dTree.buildTree()
                dTree.updateMaxDepthAndSize()
                error = 0.0
                prediction = []
                for i in range(len(trainingSet)):
                    node = dTree.node
                    while node.classLabel == -1:
                        node = node.findChildNode(trainingSet[i][node.attributeIndex])

                    classLabel = 1 if node.classLabel == 1 else -1
                    prediction.append(classLabel)
                    trueLabel = 1 if trainingSet[i][-1] == 1 else -1
                    #trueClassLabel.append([trueLabel, classLabel])
                    if classLabel != trueLabel:
                        error += dataWeights[i]
                if error == 0 or error >= 0.5:
                    print('Error: ', error)
                    break

                alpha = 0.5 * np.log((1 - error) / error)
                alphaWeights.append(alpha)
                tree.append(dTree)

                # update sample weight
                for i in range(len(dataWeights)):
                    trueLabel = 1 if trainingSet[i][-1] == 1 else -1
                    classLabel = prediction[i]
                    dataWeights[i] = dataWeights[i] * np.exp(-alpha * trueLabel * classLabel)
                dataWeights = dataWeights / sum(dataWeights)
                accuracy, precision, recall, aucList = evaluateTree(data, tree, alphaWeights)
                print('Accuracy: ', accuracy)
                print('Precision:', precision)
                print('Recall: ', recall)
            accuracy, precision, recall, auc = evaluateTree(testingSet, tree, alphaWeights)
            accuracyList.append(accuracy)
            precisionList.append(precision)
            aucList.append(auc)
            recallList.append(recall)
            print()
        return sum(accuracyList)/5, calSD(accuracyList), sum(precisionList)/5, calSD((precisionList)), sum(recallList)/5, calSD(recallList), sum(aucList)/5, calSD(aucList)
    else:
        dataWeights = [1 / len(data)] * len(data)
        alphaWeights = []
        tree = []
        for m in range(iterationNums):
            print('Boosting... %3d / %3d' % (m+1, iterationNums))
            attributeData = retrieveAttributeType(file_base, rootdir)
            dTree = decisionTree(data, maxDepthLimit, gainRatio, attributeData, dataWeights)
            dTree.buildTree()
            dTree.updateMaxDepthAndSize()
            error = 0.0
            prediction = []
            #print(dTree.node.attributeIndex, dTree.node.childNodes[0].classLabel, dTree.node.childNodes[1].classLabel, dTree.node.continuousValue)
            for i in range(len(data)):
                node = dTree.node
                while node.classLabel == -1:
                    node = node.findChildNode(data[i][node.attributeIndex])

                classLabel = 1 if node.classLabel == 1 else -1
                prediction.append(classLabel)
                trueLabel = 1 if data[i][-1] == 1 else -1
                if classLabel != trueLabel:
                    error += dataWeights[i]
            print('Error: ', error)
            if error == 0 or error >= 0.5:
                print()
                break
            alpha = 0.5 * np.log((1 - error) / error)
            alphaWeights.append(alpha)
            tree.append(dTree)

            #update sample weight
            for i in range(len(dataWeights)):
                trueLabel = 1 if data[i][-1] == 1 else -1
                classLabel = prediction[i]
                dataWeights[i] = dataWeights[i] * np.exp(-alpha * trueLabel * classLabel)
            dataWeights = dataWeights/sum(dataWeights)

            accuracy, precision, recall, aucList= evaluateTree(data, tree, alphaWeights)
            #print('Accuracy: ', accuracy)
            #print('Precision:', precision)
            #print('Recall: ', recall)
            print()
        accuracy, precision, recall, auc = evaluateTree(data, tree, alphaWeights)
        return accuracy, 0, precision, 0, recall, 0, auc, 0


# evaluation phase of the model based on the dataset
# testingSet should be a 2D list
# dTree is Root_Node
def evaluateTree(testingSet, tree, alphaWeight):
    '''
    This method evaluates the testing set with alpha weight.
    :param testingSet: testing set
    :param tree: trees from past iteration
    :param alphaWeight: alpha from past iterations
    :return: accuracy, precision, recall, auc
    '''
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    classLabels = []
    alphaSum = sum(alphaWeight)
    prediction = []
    for i in range(len(testingSet)):
        weightLabel = 0
        trueLabel = 1 if testingSet[i][-1] == 1 else -1
        for t in range(len(tree)):
            dTree = tree[t]
            node = dTree.node
            while node.classLabel == -1:
                node = node.findChildNode(testingSet[i][node.attributeIndex])
            classLabel = 1 if node.classLabel == 1 else -1
            weightLabel += alphaWeight[t] / alphaSum * classLabel
        if weightLabel >= 0 and trueLabel == 1:
            TP += 1
            classLabels.append([1, trueLabel])
        if weightLabel >= 0 and trueLabel == -1:
            FP += 1
            classLabels.append([1, trueLabel])
        if weightLabel < 0 and trueLabel == 1:
            FN += 1
            classLabels.append([-1, trueLabel])
        if weightLabel < 0 and trueLabel == -1:
            TN += 1
            classLabels.append([-1, trueLabel])
    accuracy = (TP+TN) / (TP+TN+FP+FN)
    precision = TP / (FP+TP) if (FP+TP) != 0 else 0
    recall = TP / (TP+FN) if (TP+FN) != 0 else 0
    auc, fpr, tpr = calcAUC(classLabels)
    return accuracy, precision, recall, auc

def calSD(listOfValues):
    '''
    This method calculates the standard deviation of the input
    :param listOfValues: a list of values
    :return: the standard deviation of the list
    '''
    return np.std(listOfValues, ddof=1)


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
        if classLabels[i][0] == -1:
            countTN += 1
        if classLabels[i][0] == 1:
            countFN += 1

    listFPRtoTPR = list()

    FPR = 0
    TPR = 0
    listFPRtoTPR.append([FPR, TPR])
    for i in range(len(classLabels)):
        if classLabels[i][0] == -1:
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

    return np.trapz(TPRs, FPRs), FPRs, TPRs




# return a list of attributes name and its feature type(bool), list of attribute values for discrete attribute(list), used(int 1 or 0)
# the method runs the .names file to find the information
def retrieveAttributeType(file_base, rootdir='.'):
    '''
    This method iterates through the .names file and gather information about the attributes.
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
                attribute.append(name)
                remainder = line[colon + 1:]
                values = _parse_values(remainder)
                if (len(values) == 1 and values[0].startswith('continuous')) or len(values) > 10:
                    attribute.append(True)
                    attribute.append([])
                else:
                    attribute.append(False)
                    valueList = to_float(values)
                    attribute.append(valueList)
                attribute.insert(2, 0)
                attributeList.append(attribute)

    return attributeList


# turn the attribute value name into float information
def to_float(values):
    '''
    This method updates the categorical attribute to int.
    :param values: values of one categorical attribute
    :return: changed categorial attribute
    '''
    list = []
    for i in range(len(values)):
        list.append(i)
    return list


count = 1  # keep track of the number of nodes
maxdepth = 0  # keep track of the max depth of the tree


class decisionTree():
    '''
    decisionTree class contains all data needed to develop a decision tree.
    DataTable contains the training set. 
    When first pass in depth, decisionTree will contain the information about the maximum depth of the tree. 
    After the tree is formed, the depth will get updated where it represents the actual depth of the tree. 
    useGainRatio represents whether to use information gain or gain ration to develop the tree. 
    attributeData contains information of a given attribute. attributeData[attributeName][isContinuous?][used?]
    Tree data is included in node. The node contains the information of the first split. 
    '''

    def __init__(self, data, maxDepthLimit, useGainRatio, attributeData, dataWeights):
        '''
        Initialization for decision tree
        :param X: training attributes
        :param y: training labels
        :param maxDepthLimit: maximum depth limit
        :param useGainRatio: 0 is information gain, 1 is gain ratio
        :param attributeData: information list of the attributes
        :param dataWeights: example weight
        '''
        # initialize
        global count
        count = 1
        global maxdepth
        maxdepth = 0
        self.dataTable = data  # list
        if maxDepthLimit == 0:
            self.depthLimit = len(attributeData)
        else:
            self.depthLimit = maxDepthLimit

        if useGainRatio == 0:
            self.useGainRatio = False
        else:
            self.useGainRatio = True
        # data(attributeIndex, isContinuous, continuousValue, classLabel)
        self.node = Root_Node(None, None, None, None)
        # list[attributeName][isContinuous][used]
        self.attributeData = attributeData

        self.maxOfdepth = 0  # reset maxOfdepth
        self.size = 1  # reset size
        self.dataWeights = dataWeights

    def buildTree(self):
        buildTree(self.dataTable, self.depthLimit, self.useGainRatio,
                  self.attributeData, self.node, -1, self.dataWeights)

    def updateMaxDepthAndSize(self):
        self.maxOfdepth = maxdepth
        self.size = count


def buildTree(data, maxDepthLimit, useGainRatio, attributeData, node, depth, dataWeights):
    '''
    This method will build the classifier based on the given inputs.
    :param X: training attributes
    :param y: training labels
    :param maxDepthLimit: maximum depth limit
    :param useGainRatio: 0 is information gain, 1 is gain ratio
    :param attributeData: information list of the attribute
    :param node: root node of the tree
    :param depth: current depth
    :param dataWeights: example weight
    '''

    depth += 1
    global maxdepth
    maxdepth = max(maxdepth, depth)

    if maxDepthLimit <= 0:  # reach the leaves
        classLabel = calClassLabel(data, dataWeights)
        node.updateClassLabel(classLabel)
        return

    if len(data) == 0:  # random assgin a class label for this leaf
        random.seed(12345)
        node.classLabel = random.randint(0, 1)
        return

    splitAttributeIndex = -1
    if useGainRatio:
        splitAttributeIndex = max_gain_ratio(data, attributeData, dataWeights)
    else:
        splitAttributeIndex = max_information_gain(data, attributeData, dataWeights)

    if information_gain(data, splitAttributeIndex, attributeData, dataWeights) == 0:
        classLabel = calClassLabel(data)
        node.classLabel = classLabel
        return

    node.attributeIndex = splitAttributeIndex

    # if attribute is discrete, label it as used
    if not attributeData[splitAttributeIndex][1]:
        attributeData[splitAttributeIndex][2] = 1

    if attributeData[splitAttributeIndex][1]:  # is continuouse
        continuousValue = findBestContinuousValue(data, splitAttributeIndex, dataWeights)
        node.isContinuous = True
        node.continuousValue = continuousValue
        node.classLabel = -1
        global count
        count += 2
        boxsmall = list()
        boxlarge = list()
        weightsmall = []
        weightbig = []
        for i in range(len(data)):
            if data[i][splitAttributeIndex] <= continuousValue:
                boxsmall.append(data[i])
                weightsmall.append(dataWeights[i])
            else:
                boxlarge.append(data[i])
                weightbig.append(dataWeights[i])
        # 0 represents datasets that are smaller than the best continuous value
        # 1 represents dataset that are bigger than the best continuous value
        node.addChildNode(0, Root_Node(None, None, None, None))
        node.addChildNode(1, Root_Node(None, None, None, None))
        buildTree(boxsmall, maxDepthLimit - 1, useGainRatio,
                  attributeData, node.childNodes[0], depth, weightsmall)
        buildTree(boxlarge, maxDepthLimit - 1, useGainRatio,
                  attributeData, node.childNodes[1], depth, weightbig)
    else:  # is discrete
        node.isContinuous = False
        node.classLabel = -1
        attributeValues = attributeData[splitAttributeIndex][3]
        count += len(attributeValues)
        for value in attributeValues:
            attributeValueSet = list()
            weight = []
            for i in range(len(data)):
                if data[i][splitAttributeIndex] == value:
                    attributeValueSet.append(data[i])
                    weight.append(dataWeights[i])
            node.addChildNode(value, Root_Node(None, None, None, None))
            buildTree(attributeValueSet, maxDepthLimit - 1,
                      useGainRatio, attributeData, node.childNodes[value], depth, weight)


def extractAllDiscreteAttributeValues(data, attributeIndex):
    '''
    This method extracts all the discrete attribute value given the attribute index
    :param data: training attributes
    :param attributeIndex: attribute index
    :return: a list of discrete attribute values available at the list
    '''
    uniqueAttribute = set()
    for example in data:
        uniqueAttribute.add(example[attributeIndex])
    attributeLabels = list(uniqueAttribute)
    return attributeLabels


def max_information_gain(data, attributeData, dataWeights):
    '''
    This method returns the attribute index that has the maximum information gain
    :param data: training data
    :param attributeData: information about the attribute
    :param dataWeights: example weight
    :return: attribute index that has the maximum information gain
    '''

    max_information_gain = 0
    max_information_gain_index = 0
    numberOfAttributes = len(attributeData)
    for i in range(numberOfAttributes):
        temp = information_gain(data, i, attributeData, dataWeights)
        if attributeData[i][2] != 1 and temp > max_information_gain:
            max_information_gain = temp
            max_information_gain_index = i
    return max_information_gain_index


def max_gain_ratio(data, attributeData, dataWeights):
    '''
    This method returns the attribute index that has the maximum gain ratio
    :param data: training data
    :param attributeData: information about the attribute
    :param dataWeights: example weight
    :return: attribute index that has the maximum gain ratio
    '''
    # find the max gain ratio and max attribute
    max_gain_ratio = -1
    max_gain_ratio_index = 0
    numberOfAttributes = len(attributeData)
    for i in range(numberOfAttributes):
        temp = gain_ratio(data, i, attributeData, dataWeights)
        if attributeData[i][2] != 1 and temp > max_gain_ratio:
            max_gain_ratio = temp
            max_gain_ratio_index = i
    return max_gain_ratio_index


def gain_ratio(data, attributeIndex, attributeData, dataWeights):
    '''
    This method returns the gain ratio of an attribute
    :param data: training data
    :param attributeIndex: attribute index
    :param attributeData: information about the attribute
    :param dataWeights: example weight
    :return: the gain ratio of the attribute
    '''
    # calculate the information gain ratio
    attribute_entropy = entropy_X(data, attributeIndex, attributeData[attributeIndex][1], dataWeights)
    IG = information_gain(data, attributeIndex, attributeData, dataWeights)
    gain_ratio = IG / attribute_entropy if attribute_entropy != 0 else 0
    return gain_ratio


def information_gain(data, attributeIndex, attributeData, dataWeights):
    '''
    This method returns the information gain of an attribute
    :param data: training data
    :param attributeIndex: attribute index
    :param attributeData: information about the attribute
    :param dataWeights: example weight
    :return: the information gain of the attribute
    '''
    # calculate the informaion gain
    attribute_entropy = entropy_attribute(data, attributeIndex, attributeData[attributeIndex][1], dataWeights)
    class_entropy = entropy_label(data, dataWeights)
    return class_entropy - attribute_entropy


def calClassLabel(dataTable, dataWeight):
    '''
    This method calculates the most possible class label
    :param dataTable: classification data
    :param dataWeight: example weight
    :return: the majority class label based on weight
    '''
    # find out the most possible class label in this situation
    true_counter = 0
    false_counter = 0
    for i in range(len(dataTable)):
        if dataTable[i][-1] == 0.0:
            false_counter += dataWeight[i]
        else:
            true_counter += dataWeight[i]
    if (true_counter >= false_counter):
        return 1
    else:
        return 0

def entropy_label(data, dataWeights):
    '''
    This method calculates the label entropy H(Y)
    :param data: training data
    :param dataWeights: example weight
    :return:entropy of the class label
    '''

    weight0 = 0
    weight1 = 0
    for i in range(len(data)):
        if data[i][-1] == 1:
            weight1 += dataWeights[i]
        else:
            weight0 += dataWeights[i]
    fraction0 = weight0 / sum(dataWeights) if sum(dataWeights) != 0 else 0
    fraction1 = weight1 / sum(dataWeights) if sum(dataWeights) != 0 else 0
    log_faction0 = np.log2(fraction0) if fraction0 != 0 else 0
    log_faction1 = np.log2(fraction1) if fraction1 != 0 else 0
    entropy = -fraction0 * log_faction0 - fraction1 * log_faction1
    return entropy

def findContinuousLines(data, attributeIndex):
    '''
    This method finds all the cutoff line for a continuous attribute
    :param data: training data
    :param attributeIndex: attribute index
    :return: a list of possible cutoff lines
    :return:
    '''
    # find all the cutoff line for a continuous attribute
    sortData = data.copy()
    sorted(sortData, key=lambda x: (x[attributeIndex]))
    classLabel = list()
    classLabel.append([sortData[0][-1]])
    # previousValue refers to the last different value
    previousValue = sortData[0][attributeIndex]
    # lastValue refers to last visited value
    lastValue = 0
    attributeLabel = set()
    for row in sortData:
        # if the previous is non-repeated, it has a different class label with current, and holds a different value
        # add the midpoint to the attribute label
        if (len(classLabel) == 1 and row[-1] != classLabel[0] and lastValue != row[attributeIndex]):
            attributeLabel.add((lastValue + row[attributeIndex]) / 2)
            previousValue = lastValue
            lastValue = row[attributeIndex]
            classLabel.clear()
            classLabel.append(row[-1])
        # if the previous and current value are the same number but with different label
        # add the midpoint of previous value and current value to the attribute label
        elif (row[-1] != classLabel[0] and lastValue == row[attributeIndex]):
            attributeLabel.add((previousValue + row[attributeIndex]) / 2)
            classLabel.append(row[-1])
        # if the previous and current value are not the same and the previous value is repeated
        # add the midpoint of previous value and current value to the attribute label
        elif (lastValue != row[attributeIndex] and len(classLabel) > 1):
            attributeLabel.add((lastValue + row[attributeIndex]) / 2)
            previousValue = lastValue
            lastValue = row[attributeIndex]
            classLabel.clear()
            classLabel.append(row[-1])
        else:
            if (lastValue != row[attributeIndex]):
                previousValue = lastValue
            lastValue = row[attributeIndex]
    return attributeLabel  # return a set


def entropy_X(data, attributeIndex, continuous, dataWeights):
    '''
    This method calculates the attribute entropy H(X)
    :param data: training data
    :param attributeIndex: attribute index
    :param continuous: boolean is continuous?
    :param dataWeights: example weight
    :return: H(X)
    '''
    entropy = 0.0
    if (continuous):
        maxEntropy = 0.0
        attributeLabel = list(findContinuousLines(data, attributeIndex))
        for label in attributeLabel:
            # binxy represents the bin of class label x = 1/0 given an attribute value y
            weight1 = 0
            weight0 = 0
            for i in range(len(data)):
                if data[i][attributeIndex] <= label:
                    weight1 += dataWeights[i]
                else:
                    weight0 += dataWeights[i]
            entropy1 = 0
            size = weight1 + weight0
            if size != 0:
                fraction1 = weight1 / size
                fraction0 = weight0 / size
                log_faction1 = np.log2(fraction1) if fraction1 != 0 else 0
                log_faction0 = np.log2(fraction0) if fraction0 != 0 else 0
                entropy1 = -fraction1 * log_faction1 - fraction0 * log_faction0

            if maxEntropy < entropy1:
                maxEntropy = entropy1
        entropy = maxEntropy
    else:
        attributeLabels = extractAllDiscreteAttributeValues(data, attributeIndex)

        for attributeLabel in attributeLabels:
            weight = 0
            for i in range(len(data)):
                if data[i][attributeIndex] == attributeLabel:
                    weight += dataWeights[i]

            entropy1 = -weight * np.log2(weight) if weight != 0 else 0
            entropy += entropy1
    return entropy


def entropy_attribute(data, attributeIndex, continuous, dataWeights):
    '''
    This method calculates the attribute entropy
    :param data: training data
    :param attributeIndex: attribute index
    :param continuous: bool to check if the attribute is continuous
    :param dataWeights: example weights
    :return: entropy of the attribute
    '''

    entropy = 0.0
    if (continuous):
        maxEntropy = 0.0
        attributeLabel = list(findContinuousLines(data, attributeIndex))
        for label in attributeLabel:
            # binxy represents the bin of class label x = 1/0 given an attribute value y
            weight11 = 0
            weight10 = 0
            weight01 = 0
            weight00 = 0
            for i in range(len(data)):
                if data[i][-1] == 1:
                    if data[i][attributeIndex] <= label:
                        weight11 += dataWeights[i]
                    else:
                        weight10 += dataWeights[i]
                else:
                    if data[i][attributeIndex] <= label:
                        weight01 += dataWeights[i]
                    else:
                        weight00 += dataWeights[i]
            entropy1 = 0
            size1 = weight11 + weight01
            entropy0 = 0
            size0 = weight10 + weight00
            if size1 != 0:
                fraction11 = weight11 / size1
                fraction01 = weight01 / size1
                log_faction11 = np.log2(fraction11) if fraction11 != 0 else 0
                log_faction01 = np.log2(fraction01) if fraction01 != 0 else 0
                entropy1 = size1 / (size1 + size0) * (-fraction11 *
                                                      log_faction11 - fraction01 * log_faction01)
            if size0 != 0:
                fraction10 = weight10 / size0
                fraction00 = weight00 / size0
                log_faction10 = np.log2(fraction10) if fraction10 != 0 else 0
                log_faction00 = np.log2(fraction00) if fraction00 != 0 else 0
                entropy0 = size0 / (size1 + size0) * (-fraction10 * log_faction10 - fraction00 * log_faction00)

            if maxEntropy < entropy0 + entropy1:
                maxEntropy = entropy0 + entropy1
        entropy = maxEntropy
    else:
        attributeLabels = extractAllDiscreteAttributeValues(data, attributeIndex)

        for attributeLabel in attributeLabels:
            # binxy represents the bin of class label x = 1/0 given an attribute value y
            weight11 = 0
            weight01 = 0

            for i in range(len(data)):
                if data[i][-1] == 1:
                    if data[i][attributeIndex] == attributeLabel:
                        weight11 += dataWeights[i]
                else:
                    if data[i][attributeIndex] == attributeLabel:
                        weight01 += dataWeights[i]

            entropy1 = 0.0
            size1 = weight11 + weight01

            fraction11 = weight11 / size1
            fraction01 = weight01 / size1
            log_faction11 = np.log2(fraction11) if fraction11 != 0 else 0
            log_faction01 = np.log2(fraction01) if fraction01 != 0 else 0

            entropy1 = size1 / sum(dataWeights) * (-fraction11 * log_faction11 - fraction01 * log_faction01)
            entropy += entropy1

    return entropy


def findBestContinuousValue(data, attributeIndex, dataWeights):
    '''
    This method finds the continuous cutoff line for a given attribute based on each IG score
    :param data: training data
    :param attributeIndex: attribute index
    :param dataWeights: example weights
    :return: the cutoff line with the highest IG
    '''

    HY = entropy_label(data, dataWeights)
    IG = 0
    value = 0

    attributeLabel = list(findContinuousLines(data, attributeIndex))
    for label in attributeLabel:
        # binxy represents the bin of class label x = 1/0 given an attribute value y
        weight11 = 0
        weight10 = 0
        weight01 = 0
        weight00 = 0
        for i in range(len(data)):
            if data[i][-1] == 1:
                if data[i][attributeIndex] <= label:
                    weight11 += dataWeights[i]
                else:
                    weight10 += dataWeights[i]
            else:
                if data[i][attributeIndex] <= label:
                    weight01 += dataWeights[i]
                else:
                    weight00 += dataWeights[i]
        entropy1 = 0
        size1 = weight11 + weight01
        entropy0 = 0
        size0 = weight10 + weight00
        if size1 != 0:
            fraction11 = weight11 / size1
            fraction01 = weight01 / size1
            log_faction11 = np.log2(fraction11) if fraction11 != 0 else 0
            log_faction01 = np.log2(fraction01) if fraction01 != 0 else 0
            entropy1 = size1 / (size1 + size0) * (-fraction11 *
                                                  log_faction11 - fraction01 * log_faction01)
        if size0 != 0:
            fraction10 = weight10 / size0
            fraction00 = weight00 / size0
            log_faction10 = np.log2(fraction10) if fraction10 != 0 else 0
            log_faction00 = np.log2(fraction00) if fraction00 != 0 else 0
            entropy0 = size0 / (size1 + size0) * (-fraction10 * log_faction10 - fraction00 * log_faction00)

        entropy = entropy0 + entropy1
        if ((HY - entropy) > IG):
            IG = HY - entropy
            value = label
    return value


class Root_Node(object):
    '''
    Root Node represents a node in decision tree or a leaf node. Each node stores information about this node and
    its child nodes with respect to its attribute values. ClassLabel variable indicates whether the node is a attribute
    node(-1) or a leaf node(0, 1).
    If it is a node of discrete attribute, it has an attribute index, boolean value of false for isContinuous.
    The key values for the childNodes will be attribute Name
    If it is a node of continuous attribute, it has an attribute index, boolean value true for isContinuous,
    and a continuousValue indicating its cutoff line. The key values for the childNodes is 0, indicating smaller than
    cutoff line or greater if it is bigger than cutoff line.
    It it is a leaf node, it will only contains the classLabel with value 0 or 1.
    '''

    def __init__(self, attributeIndex, isContinuous, continuousValue, classLabel):
        self.attributeIndex = attributeIndex
        self.isContinuous = isContinuous
        self.continuousValue = continuousValue
        self.classLabel = classLabel
        self.childNodes = dict()

    # add a child node to the Root Nodes
    # continuous attribute value should be dealt before input
    def addChildNode(self, attributeValue, childNode):
        '''
        This method adds a child node to the parent node.
        :param attributeValue: attribute value v where X = v
        :param childNode: empty child node
        '''
        self.childNodes[attributeValue] = childNode

    # find the child node that contains a given attribute value
    # check whether the node is continuous and make decision to move on to the next child node
    def findChildNode(self, attValue):
        '''
        This method finds the child node based on the attribute value v
        :param attValue: attribute value v
        :return: the child node that has the attribute value v
        '''
        if (self.isContinuous):
            if (attValue > self.continuousValue):
                return self.childNodes.get(1)
            else:
                return self.childNodes.get(0)
        else:
            if self.childNodes.get(attValue) is None:
                random.seed(12345)
                return Root_Node(None, None, None, random.randint(0, 1))
            return self.childNodes.get(attValue)

    def updateClassLabel(self, updatedClassLabel):
        '''
        This method updates class label for a node
        :param updatedClassLabel: the updated class label
        '''
        self.classLabel = updatedClassLabel

    def isNone(self):
        return (self.attributeIndex == None) and (self.isContinuous == None) and (self.continuousValue == None) and (
                    self.classLabel == None)
