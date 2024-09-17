import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def main():
    path = input("Enter directory path: ")  # directory path

    file_path = os.chdir(path)
    fileList = os.listdir(file_path)  # all files in directory

    corresponding_x_values = []

    max_y_values = []

    for file in fileList:  # for each file
        x_coord = []  # x, y lists
        y_coord = []

        result = open(file, 'r')  # open and read lines
        read_file = result.readlines()

        for line in read_file:

            x = line[3:14]  # split string for x,y values
            y = line[16:30]

            x_coord.append(x)  # append x, y
            y_coord.append(y)

        x_coord.pop(0)  # remove first line which holds description of column
        y_coord.pop(0)

        for i in range(len(x_coord)):  # remove " " if in string
            if (x_coord[i][0] == " "):
                x_coord[i] = x_coord[i][1:]

        x = [float(x_coordinate) for x_coordinate in x_coord]  # convert string to float
        y = [float(y_coordinate) for y_coordinate in y_coord]

        print(np.polyfit(x,y,...))

        max_x = x[0]  # current maxes set to first element
        max_y = y[0]

        for i in range(len(y)):  # algorithm to grab max y value(with corresponding x value)
            if (y[i] > max_y):
                max_y = y[i]
                max_x = x[i]

        max_y_values.append(max_y)  # append max value
        corresponding_x_values.append(max_x)

    categories = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 4,
                  4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 8, 8, 8, 8, 9, 9, 9]
    
    corresponding_x_values = pd.Series(corresponding_x_values)
    max_y_values = pd.Series(max_y_values)

    #df = pd.DataFrame(corresponding_x_values, max_y_values) #just numbers
    '''
    blue1x = pd.Series(corresponding_x_values[0:4])
    green1x = pd.Series(corresponding_x_values[4:8])
    purple1x = pd.Series(corresponding_x_values[8:10])
    pink1x = pd.Series(corresponding_x_values[10:14])
    yellow1x = pd.Series(corresponding_x_values[14:18])
    pink2x = pd.Series(corresponding_x_values[18:21])
    darkblue2x = pd.Series(corresponding_x_values[21:25])
    lightblue2x = pd.Series(corresponding_x_values[25:27])
    green2x = pd.Series(corresponding_x_values[27:31])
    yellow2x = pd.Series(corresponding_x_values[31:34])

    blue1y = pd.Series(max_y_values[0:4])
    green1y = pd.Series(max_y_values[4:8])
    purple1y = pd.Series(max_y_values[8:10])
    pink1y = pd.Series(max_y_values[10:14])
    yellow1y = pd.Series(max_y_values[14:18])
    pink2y = pd.Series(max_y_values[18:21])
    darkblue2y = pd.Series(max_y_values[21:25])
    lightblue2y = pd.Series(max_y_values[25:27])
    green2y = pd.Series(max_y_values[27:31])
    yellow2y = pd.Series(max_y_values[31:34])

    DFx = pd.DataFrame(data = {'blue1': blue1x, 'green1' : green1x, 'purple1' : purple1x, 'pink1' : pink1x, 
                              'yellow1' : yellow1x, 'pink2' : pink2x, 'darkblue2' : darkblue2x, 'lightblue2' : lightblue2x,
                              'green2' : green2x, 'yellow2' : yellow2x}) #x values

    DFy = pd.DataFrame(data = {'blue1': blue1y, 'green1' : green1y, 'purple1' : purple1y, 'pink1' : pink1y, 
                              'yellow1' : yellow1y, 'pink2' : pink2y, 'darkblue2' : darkblue2y, 'lightblue2' : lightblue2y,
                              'green2' : green2y, 'yellow2' : yellow2y})
    #df = pd.DataFrame(data = {corresponding_x_values, max_y_values}) #y values

    

    print(DFx)
    print(DFy)


    '''



#X_train, X_test, y_train, y_test = train_test_split()

'''
    AF1x = pd.Series(corresponding_x_values[0:3])
    AF1x.append(pd.Series(corresponding_x_values[10:13]))
    AC1x = pd.Series(corresponding_x_values[3])
    AC1x.append(pd.Series(corresponding_x_values[13]))
    FF1x = pd.Series(corresponding_x_values[4:7])
    FF1x.append(pd.Series(corresponding_x_values[8:10]))
    FF1x.append(pd.Series(corresponding_x_values[14:17]))
    FC1x = pd.Series(corresponding_x_values[7])
    FC1x.append(pd.Series(corresponding_x_values[17]))
    AF2x = pd.Series(corresponding_x_values[24])
    AC2x = pd.Series(corresponding_x_values[21:24])
    AC2x.append(pd.Series(corresponding_x_values[25:27]))
    AC2x.append(pd.Series(corresponding_x_values[31:34]))
    FF2x = pd.Series(corresponding_x_values[20])
    FF2x.append(pd.Series(corresponding_x_values[30]))
    FC2x = pd.Series(corresponding_x_values[18:20])
    FC2x.append(pd.Series(corresponding_x_values[27:30]))

    AF1y = pd.Series(max_y_values[0:3])
    AF1y.append(pd.Series(max_y_values[10:13]))
    AC1y = pd.Series(max_y_values[3])
    AC1y.append(pd.Series(max_y_values[13]))
    FF1y = pd.Series(max_y_values[4:7])
    FF1y.append(pd.Series(max_y_values[8:10]))
    FF1y.append(pd.Series(max_y_values[14:17]))
    FC1y = pd.Series(max_y_values[7])
    FC1y.append(pd.Series(max_y_values[17]))
    AF2y = pd.Series(max_y_values[24])
    AC2y = pd.Series(max_y_values[21:24])
    AC2y.append(pd.Series(max_y_values[25:27]))
    AC2y.append(pd.Series(max_y_values[31:34]))
    FF2y = pd.Series(max_y_values[20])
    FF2y.append(pd.Series(max_y_values[30]))
    FC2y = pd.Series(max_y_values[18:20])
    FC2y.append(pd.Series(max_y_values[27:30]))

    DFx = pd.DataFrame(data = {'AF1': AF1x, 'AC1' : AC1x, 'FF1' : FF1x, 
                            'FC1' : FC1x, 
                              'AF2' : AF2x, 'AC2' : AC2x, 'FF2' : FF2x, 
                              'FC2' : FC2x}) #x values

    DFy = pd.DataFrame(data = {'AF1': AF1y, 'AC1' : AC1y, 'FF1' : FF1y, 
                            'FC1' : FC1y, 
                              'AF2' : AF2y, 'AC2' : AC2y, 'FF2' : FF2y, 
                              'FC2' : FC2y}) #x values

    print(DFx)

    print(DFy)

    '''

main()  # run function


'''
Do every 4 indexes, each index set to a variable
Doesn't reach an index out of bounds
Sort numbers
If index 1 - 0 > index 3 - 2 (flip/conserve is first element)
Print the index of number
'''
'''
Keep going through indexes until number is found that is outlier
Split that group of data into new array[final element is flip/conserve]
Outlier could be anywhere between 10 - 20 percent
Continue separating(if only one piece of data exists when an outlier is found throw an exception for group
until a seemingly normal group of data arises)
'''
