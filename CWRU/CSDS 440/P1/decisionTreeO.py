import numpy as np
from operator import itemgetter
from mldata import *
import random

count = 1     # keep track of the number of nodes
maxdepth = 0    # keep track of the max depth of the tree

class decisionTree():
    '''''
    decisionTree class contains all data needed to develop a decision tree.
    DataTable contains the training set. 
    When first pass in depth, decisionTree will contain the information about the maximum depth of the tree. 
    After the tree is formed, the depth will get updated where it represents the actual depth of the tree. 
    useGainRatio represents whether to use information gain or gain ration to develop the tree. 
    attributeData contains information of a given attribute. attributeData[attributeName][isContinuous?][used?]
    Tree data is included in node. The node contains the information of the first split. 
    '''''

    def __init__(self, data, maxDepthLimit, useGainRatio, attributeData):
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

        self.maxOfdepth = 0         # reset maxOfdepth
        self.size = 1        # reset size

    def buildTree(self):
        buildTree(self.dataTable, self.depthLimit, self.useGainRatio,
                  self.attributeData, self.node, -1)
    
    def updateMaxDepthAndSize(self):
        self.maxOfdepth = maxdepth
        self.size = count
    
def buildTree(data, maxDepthLimit, useGainRatio, attributeData, node, depth):
    # buildTree will be call recursively
    depth += 1
    global maxdepth
    maxdepth = max(maxdepth, depth)

    if maxDepthLimit <= 0:           # reach the leaves
        classLabel = calClassLabel(data)
        node.updateClassLabel(classLabel)
        return
    
    if len(data) == 0:            # random assgin a class label for this leaf
        random.seed(12345)
        node.classLabel = random.randint(0, 1)
        return

    splitAttributeIndex = -1
    if useGainRatio:
        splitAttributeIndex = max_gain_ratio(data, attributeData)
    else:
        splitAttributeIndex = max_information_gain(data, attributeData)

    if (information_gain(data, splitAttributeIndex, attributeData) == 0):
        classLabel = calClassLabel(data)
        node.classLabel = classLabel
        return

    node.attributeIndex = splitAttributeIndex

    # if attribute is discrete, label it as used
    if not attributeData[splitAttributeIndex][1]:
        attributeData[splitAttributeIndex][2] = 1   

    if attributeData[splitAttributeIndex][1]:   # is continuouse
        continuousValue = findBestContinuousValue(data, splitAttributeIndex)
        node.isContinuous = True
        node.continuousValue = continuousValue
        node.classLabel = -1
        global count
        count += 2
        boxsmall = list()
        boxlarge = list()
        for example in data:
            if example[splitAttributeIndex] <= continuousValue:
                boxsmall.append(example)
            else:
                boxlarge.append(example)
        # 0 represents datasets that are smaller than the best continuous value
        # 1 represents dataset that are bigger than the best continuous value
        node.addChildNode(0, Root_Node(None, None, None, None))
        node.addChildNode(1, Root_Node(None, None, None, None))
        buildTree(boxsmall, maxDepthLimit-1, useGainRatio,
                  attributeData, node.childNodes[0], depth)
        buildTree(boxlarge, maxDepthLimit-1, useGainRatio,
                  attributeData, node.childNodes[1], depth)
    else:   # is discrete
        node.isContinuous = False
        node.classLabel = -1
        attributeValues = attributeData[splitAttributeIndex][3]
        count += len(attributeValues)
        for value in attributeValues:
            attributeValueSet = list()
            for example in data:
                if example[splitAttributeIndex] == value:
                    attributeValueSet.append(example)
            node.addChildNode(value, Root_Node(None, None, None, None))
            buildTree(attributeValueSet, maxDepthLimit-1,
                      useGainRatio, attributeData, node.childNodes[value], depth)


def extractAllDiscreteAttributeValues(data, attributeIndex):
    # extract all values of this attribute
    uniqueAttribute = set()
    for example in data:
        uniqueAttribute.add(example[attributeIndex])
    attributeLabels = list(uniqueAttribute)
    return attributeLabels


def max_information_gain(data, attributeData):
    # find the max information gain and attribute
    
    max_information_gain = 0
    max_information_gain_index = 0
    numberOfAttributes = len(attributeData)
    for i in range(numberOfAttributes):
        if attributeData[i][2] != 1 and information_gain(data, i, attributeData) > max_information_gain:
            max_information_gain = information_gain(data, i, attributeData)
            max_information_gain_index = i
    return max_information_gain_index



def max_gain_ratio(data, attributeData):
    # find the max gain ratio and max attribute
    
    max_gain_ratio = -1
    max_gain_ratio_index = 0
    numberOfAttributes = len(attributeData)
    for i in range(numberOfAttributes):
        if attributeData[i][2] != 1 and gain_ratio(data, i, attributeData) > max_gain_ratio:
            max_gain_ratio = gain_ratio(data, i, attributeData)
            max_gain_ratio_index = i
    return max_gain_ratio_index


def gain_ratio(data, attributeIndex, attributeData):
    # calculate the information gain ratio
    
    attribute_entropy = entropy_attribute(
        data, attributeIndex, attributeData[attributeIndex][1])
    IG = information_gain(data, attributeIndex, attributeData)
    gain_ratio = IG / attribute_entropy if attribute_entropy != 0 else 0
    return gain_ratio


def information_gain(data, attributeIndex, attributeData):
    # calculate the informaion gain
    attribute_entropy = entropy_attribute(data, attributeIndex, attributeData[attributeIndex][1])
    class_entropy = entropy_label(data)
    return class_entropy - attribute_entropy


def calClassLabel(dataTable):
    # find out the most possible class label in this situation
    true_counter = 0
    false_counter = 0
    for row in dataTable:
        if row[-1] == 0.0:
            false_counter += 1
        else:
            true_counter += 1
    if (true_counter >= false_counter):
        return 1
    else:
        return 0


def entropy_label(data):
    # return the entropy for all class label, H(Y)
    
    subset0 = list()
    subset1 = list()
    for example in data:
        if example[-1] == 1:
            subset1.append(example)
        else:
            subset0.append(example)
    fraction0 = len(subset0) / len(data) if len(data) != 0 else 0
    fraction1 = len(subset1) / len(data) if len(data) != 0 else 0
    log_faction0 = np.log2(fraction0) if fraction0 != 0 else 0
    log_faction1 = np.log2(fraction1) if fraction1 != 0 else 0
    entropy = -fraction0*log_faction0 - fraction1*log_faction1
    return entropy


def findContinuousLines(data, attributeIndex):
    # find all the cutoff line for a continuous attribute
    
    sortData = data
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


def entropy_attribute(data, attributeIndex, continuous):
    # return the entropy value for a given attribute
    
    entropy = 0.0
    if (continuous):
        maxEntropy = 0.0
        attributeLabel = list(findContinuousLines(data, attributeIndex))
        for label in attributeLabel:
            # binxy represents the bin of class label x = 1/0 given an attribute value y
            bin11 = list()
            bin01 = list()
            bin10 = list()
            bin00 = list()
            for example in data:
                if example[-1] == 1:
                    if example[attributeIndex] <= label:
                        bin11.append(example)
                    else:
                        bin10.append(example)
                else:
                    if example[attributeIndex] <= label:
                        bin01.append(example)
                    else:
                        bin00.append(example)
            entropy1 = 0
            size1 = len(bin11) + len(bin01)
            if size1 != 0:
                fraction11 = len(bin11) / size1
                fraction01 = len(bin01) / size1
                log_faction11 = np.log2(fraction11) if fraction11 != 0 else 0
                log_faction01 = np.log2(fraction01) if fraction01 != 0 else 0
                entropy1 = size1/len(data) * (-fraction11 *
                                              log_faction11 - fraction01*log_faction01)
            entropy0 = 0
            size0 = len(bin10) + len(bin00)
            if size0 != 0:
                fraction10 = len(bin10) / size0
                fraction00 = len(bin00) / size0
                log_faction10 = np.log2(fraction10) if fraction10 != 0 else 0
                log_faction00 = np.log2(fraction00) if fraction00 != 0 else 0
                entropy0 = size0/len(data) * (-fraction10 * log_faction10 - fraction00*log_faction00)

            if maxEntropy < entropy0+entropy1:
                maxEntropy = entropy0+entropy1
        entropy = maxEntropy
    else:
        attributeLabels = extractAllDiscreteAttributeValues(data, attributeIndex)
        
        for attributeLabel in attributeLabels:
            # binxy represents the bin of class label x = 1/0 given an attribute value y
            bin11 = list()
            bin01 = list()

            for example in data:
                if example[-1] == 1:
                    if example[attributeIndex] == attributeLabel:
                        bin11.append(example)
                else:
                    if example[attributeIndex] == attributeLabel:
                        bin01.append(example)
            
            entropy1 = 0.0
            size1 = len(bin11) + len(bin01)
            
            fraction11 = len(bin11) / size1
            fraction01 = len(bin01) / size1
            log_faction11 = np.log2(fraction11) if fraction11 != 0 else 0
            log_faction01 = np.log2(fraction01) if fraction01 != 0 else 0
            
            entropy1 = size1/len(data) * (-fraction11 * log_faction11 - fraction01*log_faction01)
            entropy += entropy1

    return entropy


def findBestContinuousValue(data, attributeIndex):
    # find the continuous cutoff line for a given attribute based on each IG score
    
    HY = entropy_label(data)
    IG = 0
    value = 0

    attributeLabel = list(findContinuousLines(data, attributeIndex))
    for label in attributeLabel:
        # binxy represents the bin of class label x = 1/0 given an attribute value y
        bin11 = list()
        bin01 = list()
        bin10 = list()
        bin00 = list()
        for example in data:
            if example[-1] == 1:
                if example[attributeIndex] <= label:
                    bin11.append(example)
                else:
                    bin10.append(example)
            else:
                if example[attributeIndex] <= label:
                    bin01.append(example)
                else:
                    bin00.append(example)

        size1 = len(bin11) + len(bin01)
        fraction11 = len(bin11) / size1 if size1 != 0 else 0
        fraction01 = len(bin01) / size1 if size1 != 0 else 0
        log_faction11 = np.log2(fraction11) if fraction11 != 0 else 0
        log_faction01 = np.log2(fraction01) if fraction01 != 0 else 0
        entropy1 = size1/len(data) * (-fraction11 *
                                      log_faction11 - fraction01*log_faction01)

        size0 = len(bin10) + len(bin00)
        fraction10 = len(bin10) / size0 if size0 != 0 else 0
        fraction00 = len(bin00) / size0 if size0 != 0 else 0
        log_faction10 = np.log2(fraction10) if fraction10 != 0 else 0
        log_faction00 = np.log2(fraction00) if fraction00 != 0 else 0
        entropy0 = size0/len(data) * (-fraction10 *
                                      log_faction10 - fraction00*log_faction00)
        
        entropy = entropy0 + entropy1
        if ((HY-entropy) > IG):
            IG = HY-entropy
            value = label
    return value


class Root_Node(object):
    """"
    Root Node represents a node in decision tree or a leaf node. Each node stores information about this node and
    its child nodes with respect to its attribute values. ClassLabel variable indicates whether the node is a attribute
    node(-1) or a leaf node(0, 1).
    If it is a node of discrete attribute, it has an attribute index, boolean value of false for isContinuous.
    The key values for the childNodes will be attribute Name
    If it is a node of continuous attribute, it has an attribute index, boolean value true for isContinuous,
    and a continuousValue indicating its cutoff line. The key values for the childNodes is 0, indicating smaller than
    cutoff line or greater if it is bigger than cutoff line.
    It it is a leaf node, it will only contains the classLabel with value 0 or 1.
    """""

    def __init__(self, attributeIndex, isContinuous, continuousValue, classLabel):
        self.attributeIndex = attributeIndex
        self.isContinuous = isContinuous
        self.continuousValue = continuousValue
        self.classLabel = classLabel
        self.childNodes = dict()

    # add a child node to the Root Nodes
    # continuous attribute value should be dealt before input
    def addChildNode(self, attributeValue, childNode):
        self.childNodes[attributeValue] = childNode

    # find the child node that contains a given attribute value
    # check whether the node is continuous and make decision to move on to the next child node
    def findChildNode(self, attValue):
        if(self.isContinuous):
            if(attValue > self.continuousValue):
                return self.childNodes.get(1)
            else:
                return self.childNodes.get(0)
        else:
            if self.childNodes.get(attValue) is None:
                random.seed(12345)
                return Root_Node(None, None, None, random.randint(0, 1))
            return self.childNodes.get(attValue)

    def updateClassLabel(self, updatedClassLabel):
        self.classLabel = updatedClassLabel

    def isNone(self):
        return (self.attributeIndex == None) and (self.isContinuous == None) and (self.continuousValue == None) and (self.classLabel == None)
