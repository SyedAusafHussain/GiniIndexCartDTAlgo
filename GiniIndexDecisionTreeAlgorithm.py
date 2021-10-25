'''
Created on OCTOBER 10, 2021

@author: Syed.Ausaf.Hussain
'''

# Calculate the Gini index using cart for a split dataset
import pandas


def gini_index(groups, classes):
    # count all samples at split point
    n_instances = float(sum([len(group) for group in groups]))
    # sum weighted Gini index for each group
    gini = 0.0
    for group in groups:
        size = float(len(group))
        # avoid divide by zero
        if size == 0:
            continue
        score = 0.0
        # score the group based on the score for each class
        for class_val in classes:
            p = [row[-1] for row in group].count(class_val) / size
            score += p * p
        # weight the group score by its relative size
        gini += (1.0 - score) * (size / n_instances)
    return gini


def spilitingCriteria(attributes, data):
    print(data)
    dict = {}
    if data[attributes[-1]].nunique() < 2:
        print( str(data[attributes[-1]].unique())+" leafNode")
        return str(data[attributes[-1]].unique())+" leafNode"

    for attr in attributes[:-1]:
        for uniqueValue in data[attr].unique():
            d1 = data[data[attr] == uniqueValue].values.tolist()
            d2 = data[data[attr] != uniqueValue].values.tolist()
            if (data[attr].nunique() < 3):
                dict[attr + "-" + uniqueValue] = gini_index([d1, d2], classes)
                break
            dict[attr + "-" + uniqueValue] = gini_index([d1, d2], classes)
    return  list(dict.keys()) if  len(dict) < 2 else min(dict, key=dict.get)


def spiliting(attributes, data, array):
    if(data.shape[0] < 1):
        return array
    temp = spilitingCriteria(attributes, data)
    print("spilitingCriteria: ", temp)
    array.append(temp)
    if "-" not in temp:
        return array
    value = temp.split("-")
    # attributes.remove(value[0])
    array = spiliting(attributes, data[data[value[0]] == value[1]], array)
    array = spiliting(attributes, data[data[value[0]] != value[1]], array)
    return array


data = pandas.read_csv('dataset1.csv')
print("Data\n", data)
attributes = data.columns.values.tolist()  # class attribute is the last column
classes = data[attributes[-1]].unique().tolist()


print(spiliting(attributes, data, array=[]))
# print("splitting criteria on root", min(dict, key=dict.get))
