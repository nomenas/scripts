import os
import re

def normalise_name(test_definition):
    returnValue = ""
    inTestName = False
    underscoreBefore = False
    underscoreTwoBefore = False
    isFirst = True
    for ch in test_definition:
        new_ch = ch
        if (not inTestName and ch == ','):
            inTestName = True
        elif (inTestName):
            if (isFirst and ch != ' '):
                new_ch = ch.upper()
                isFirst = False
            elif (underscoreTwoBefore and underscoreBefore and ch != '_'):
                new_ch = ch.upper()
            elif (underscoreBefore and ch != '_'):
                returnValue = returnValue[:len(returnValue) - 1]
                new_ch = ch.upper()

        underscoreTwoBefore = underscoreBefore
        underscoreBefore = ch == '_'
        returnValue = returnValue + new_ch

    return returnValue


def unify_names(filename):
    test_matcher = re.compile("^TEST.*[a-z]_[a-z]")
    misleading_test_name_matcher = re.compile(".*__.*__.*")
    isValid = True
    with open(filename, "r") as file:
        for line in file:
            if (test_matcher.match(line) and misleading_test_name_matcher.match(line)):
                isValid = False

    if (not isValid):
        new_file = open(filename + "_", "w")
        file = open(filename, "r")
        for line in file:
            if (test_matcher.match(line) and misleading_test_name_matcher.match(line)):
                new_file.write(normalise_name(line))
            else:
                new_file.write(line)
        os.remove(filename)
        os.rename(filename + "_", filename)

test_file_matcher = re.compile(".*Test.*cpp$")

for root, dirs, files in os.walk("."):
    for file in files:
        if test_file_matcher.match(file):
            unify_names(os.path.join(root, file))