from mldata import *
import random
from decisionTreeO import *
from decisionTreeO import Root_Node
from decisionTreeO import decisionTree
import sys
from mldata import _parse_c45, _find_file, _parse_values

# divide the dataset to folds using stratified cross validation
#data should be a 2D list
#fold_number should be an int
def make_folds(data, fold_number):
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

    for j in range(fold_number - 1):
        choice = random.choices(classLabel1, k = int(len(classLabel1)/5))
        folds[j].extend(choice)
        classLabel1 = [ele for ele in classLabel1 if ele not in choice]
    
    folds[-1].extend(classLabel1)
    
    for j in range(fold_number - 1):
        choice = random.choices(classLabel0, k = int(len(classLabel0)/5))
        folds[j].extend(choice)
        classLabel0 = [ele for ele in classLabel0 if ele not in choice]
        
    folds[-1].extend(classLabel0)
    return folds

#evaluation phase of the model based on the dataset
#testingSet should be a 2D list
#dTree is Root_Node
def evaluateTree(testingSet, dTree):
    true_counter = 0
    row = 0
    for example in testingSet:
        node = dTree.node
        
        while node.classLabel == -1:
            node = node.findChildNode(example[node.attributeIndex])
        if node.classLabel == example[-1]:
            true_counter += 1
        
        row += 1

    accuracyOfFolds = true_counter / (len(testingSet))
    return accuracyOfFolds

# return the average accuracy of five turns
def averageAccuracy(foldsAccuracy):
    return sum(foldsAccuracy) / 5


def main(**Option):
    # the format of input: python main.py /folder/filename 0/1 maxDepth 0/1
    # Option 1 is the path, Option 2 is cross validation/full example, Option 3 is maxDepth, Option 4 is IG/gainRatio
    path = sys.argv[1]
    useFullSample = int(sys.argv[2])
    maxDepthLimit = int(sys.argv[3])
    useGainRatio = int(sys.argv[4])
    accuracy, size, maxDepth, firstFeature = buildModel(path, useFullSample, maxDepthLimit, useGainRatio)

    # accuracy, size, maxDepth, firstFeature = buildModel('/spam/spam', 1, 10, 0)

    print()

    print('Accuracy: %.03f' % (accuracy))
    print('Size: %3d' % (size))
    print('Maximum Depth: %3d' % (maxDepth))
    print('First Feature: %s' % (firstFeature))

#build the decision tree model and return the evaluation of the model based on the input
#path specifies the name of the file
#crossValidation should be inpt as an int, 0 indicates cross validation, 1 indicates full sample
#maxDepthLimit should be input as an int, 0 is no depth limit, any other positive integer is the model's max depth
#gainRatio should be input as an int, 0 is information gain, 1 is gain ratio
def buildModel(path, crossValidation, maxDepthLimit, gainRatio):
    import os
    rootdir, file_base = os.path.split(path)
    rootdir = rootdir[1:] if rootdir[1:] != '' else '.'
    # convert to list of list here
    data = (parse_c45(file_base, rootdir)).to_float()       # 0.0 is -, 1.0 is 0, 2.0 is +
    for example in data:
        example.pop(0)

    if crossValidation == 0:
        folds = make_folds(data, 5)
        foldsAccuracy = list()
        sizeList = list()
        firstFeature = list()
        depthList = list()
        for i in range(len(folds)):
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
            dTree = decisionTree(trainingSet, maxDepthLimit,
                                 gainRatio, attributeData)
            dTree.buildTree()
            dTree.updateMaxDepthAndSize()
            accuracy = evaluateTree(testingSet, dTree)
            foldsAccuracy.append(accuracy)
            sizeList.append(dTree.size)
            depthList.append(dTree.maxOfdepth)
            firstFeature.append(attributeData[dTree.node.attributeIndex][0])
        overallAccuracy = averageAccuracy(foldsAccuracy)
        size = sum(sizeList) / 5
        maxDepth = sum(depthList) / 5
        return overallAccuracy, size, maxDepth, firstFeature
    else:
        attributeData = retrieveAttributeType(file_base, rootdir)
        dTree = decisionTree(data, maxDepthLimit, gainRatio, attributeData)
        dTree.buildTree()
        dTree.updateMaxDepthAndSize()
        accuracy = evaluateTree(data, dTree)
        firstFeature = attributeData[dTree.node.attributeIndex][0]
        return accuracy, dTree.size, dTree.maxOfdepth, firstFeature

# return a list of attributes name and its feature type(bool), list of attribute values for discrete attribute(list), used(int 1 or 0)
# the method runs the .names file to find the information
def retrieveAttributeType(file_base, rootdir='。'):
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

#turn the attribute value name into float information
def to_float(values):
    list = []
    for i in range(len(values)):
        list.append(i)
    return list

#run the model 5 times to get the average time and accuracy of a given model
def getAccuracyAndTime(path, crossValidation, maxDepthLimit, gainRatio):
    import time
    start_time = time.time()
    SumOfAccuracy = 0.0
    SumOfSize = 0
    for i in range(5):
        accuracy, size, maxDepth, firstFeature = buildModel(path, crossValidation, maxDepthLimit, gainRatio)
        SumOfAccuracy += accuracy
        SumOfSize += size
    SumOftime = time.time() - start_time
    return SumOftime/5, SumOfAccuracy/5, SumOfSize/5