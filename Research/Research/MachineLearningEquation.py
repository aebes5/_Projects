import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.optimize import differential_evolution
import warnings


def func(x, a, b, Offset):  # from the zunzun.com "function finder"
    return a * np.exp(b/x) + Offset


x = []
y = []


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

            x_ = line[3:14]  # split string for x,y values
            y_ = line[16:30]

            x_coord.append(x_)  # append x, y
            y_coord.append(y_)

        x_coord.pop(0)  # remove first line which holds description of column
        y_coord.pop(0)

        for i in range(len(x_coord)):  # remove " " if in string
            if (x_coord[i][0] == " "):
                x_coord[i] = x_coord[i][1:]

        for x_coordinate in x_coord:
            x.append(float(x_coordinate))
        for y_coordinate in y_coord:
            y.append(float(y_coordinate))

        print(x)

        max_x = x[0]  # current maxes set to first element
        max_y = y[0]

        for i in range(len(y)):  # algorithm to grab max y value(with corresponding x value)
            if (y[i] > max_y):
                max_y = y[i]
                max_x = x[i]

        max_y_values.append(max_y)  # append max value
        corresponding_x_values.append(max_x)

        # plt.plot(x,y) for graphs, plt.scatter(max_x, max_y) for max points
        plt.plot(x, y)

    for i in range(len(max_y_values)):
        print(corresponding_x_values[i])
        print(max_y_values[i])
        print("\n")

    # plt.show() # show plot


main()  # run function

print(x)


# function for genetic algorithm to minimize (sum of squared error)
def sumOfSquaredError(parameterTuple):
    # do not print warnings by genetic algorithm
    warnings.filterwarnings("ignore")
    val = func(x, *parameterTuple)
    return np.sum((y - val) ** 2.0)


def generate_Initial_Parameters():
    # min and max used for bounds

    maxX = max(x, default=0)
    minX = min(x, default=0)
    maxY = max(y, default=0)
    minY = min(y, default=0)

    minData = min(minX, minY)
    maxData = max(maxX, maxY)

    parameterBounds = []
    parameterBounds.append([minData, maxData])  # search bounds for a
    parameterBounds.append([minData, maxData])  # search bounds for b
    parameterBounds.append([minData, maxData])  # search bounds for Offset

    # "seed" the numpy random number generator for repeatable results
    result = differential_evolution(sumOfSquaredError, parameterBounds, seed=3)
    return result.x


# by default, differential_evolution completes by calling curve_fit() using parameter bounds
geneticParameters = generate_Initial_Parameters()

# now call curve_fit without passing bounds from the genetic algorithm,
# just in case the best fit parameters are aoutside those bounds
fittedParameters, pcov = curve_fit(func, x, y, geneticParameters)
print('Fitted parameters:', fittedParameters)
print()

modelPredictions = func(x, *fittedParameters)

absError = modelPredictions - y

SE = np.square(absError)  # squared errors
MSE = np.mean(SE)  # mean squared errors
RMSE = np.sqrt(MSE)  # Root Mean Squared Error, RMSE
Rsquared = 1.0 - (np.var(absError) / np.var(y))

print()
print('RMSE:', RMSE)
print('R-squared:', Rsquared)

print()


##########################################################
# graphics output section
def ModelAndScatterPlot(graphWidth, graphHeight):
    f = plt.figure(figsize=(graphWidth/100.0, graphHeight/100.0), dpi=100)
    axes = f.add_subplot(111)

    # first the raw data as a scatter plot
    axes.plot(x, y,  'D')

    # create data for the fitted equation plot
    xModel = np.linspace(min(x), max(x))
    yModel = func(xModel, *fittedParameters)

    # now the model as a line plot
    axes.plot(xModel, yModel)

    axes.set_xlabel('X Data')  # X axis data label
    axes.set_ylabel('Y Data')  # Y axis data label

    plt.show()
    plt.close('all')  # clean up after using pyplot


graphWidth = 800
graphHeight = 600
ModelAndScatterPlot(graphWidth, graphHeight)
