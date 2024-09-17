import os
import matplotlib.pyplot as plt


def main():
    path = input("Enter directory path: ")  # directory path

    file_path = os.chdir(path)
    fileList = os.listdir(file_path)  # all files in directory

    corresponding_x_values = []  # store data
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

        x = [float(x_coordinate)
             for x_coordinate in x_coord]  # convert string to float
        y = [float(y_coordinate) for y_coordinate in y_coord]

        max_x = x[0]  # current maxes set to first element
        max_y = y[0]

        for i in range(len(y)):  # algorithm to grab max y value(with corresponding x value)
            if (y[i] > max_y):
                max_y = y[i]
                max_x = x[i]

        max_y_values.append(max_y)  # append max value
        corresponding_x_values.append(max_x)

        # plt.plot(x,y) for graphs, plt.scatter(max_x, max_y) for max points
        plt.scatter(max_x, max_y)
        #plt.plot(x, y)

    plt.show()  # show plot


main()  # run function
