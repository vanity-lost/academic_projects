import sys
from dtree import dtree
from nbayes import nbayes
from logreg import logreg

def main(**Option):
    # the format of input: python boost.py /folder/filename 0/1 algorithm_name iteration_number
    # Option 1 is the path, Option 2 is cross validation/full example, Option 3 is algorithm name, Option 4 is the number of iterations.
    path = sys.argv[1]
    useFullSample = int(sys.argv[2])
    algorithm = sys.argv[3]
    iterationNums = int(sys.argv[4])
    
    if algorithm == "dtree":
        accuracy, accuracySD, precision, precisionSD, recall, recallSD, areaUnderROC = dtree(
            path, useFullSample, iterationNums)
    elif algorithm == "nbayes":
        accuracy, accuracySD, precision, precisionSD, recall, recallSD, areaUnderROC = nbayes(
            path, useFullSample, iterationNums)
    elif algorithm == "logreg":
        accuracy, accuracySD, precision, precisionSD, recall, recallSD, areaUnderROC = logreg(
            path, useFullSample, iterationNums)
    else:
        print("Wrong input format of the choice of algorithms")
        return

    print('Accuracy: %.03f %.03f' % (accuracy, accuracySD))
    print('Precision: %.03f %.03f' % (precision, precisionSD))
    print('Recall: %.03f %.03f' % (recall, recallSD))
    print('Area Under ROC: %.03f' % (areaUnderROC))
    
main()