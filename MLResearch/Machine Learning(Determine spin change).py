import os

# input should be 4 files, looking for the change in spin


def main():
    path = input("Enter directory path: ")  # directory path

    file_path = os.chdir(path)
    fileList = os.listdir(file_path)  # all files in directory

    corresponding_x_values = [] # store data
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

    sorted_x_values = corresponding_x_values.sort()

    running_total = 0
    times = 0

    for i in range(len(sorted_x_values)):
        if (i == 0 or i == (len(sorted_x_values)) - 1):
            continue
        else:
            running_total += sorted_x_values[i]
            times += 1

    average = running_total / times


    if((sorted_x_values[len(sorted_x_values)] - average) < (average - sorted_x_values[0])):
        outlier = sorted_x_values[len(sorted_x_values)]
    else:
        outlier = sorted_x_values[0]

    for i in range(len(sorted_x_values)):
        if(corresponding_x_values[i] == outlier):
            print(f"Spin change is file number {i + 1} in the directory")




main()  # run function