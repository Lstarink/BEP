import matplotlib.pyplot as plt
import numpy as np
import csv

#A group of lines which are parallel. eg same unit_vector
class line_group:
    def __init__(self, unit_vector):
        self.unit_vector = unit_vector
        self.lines_k = []
        self.group_size = int(0)
        
    def AddLine(self, line):
        self.lines_k.append(line)
        self.group_size += 1
    

    
    
class line:
    def __init__(self, start, end, vAverage, unit_vector):
        self.A = start
        self.B = end
        self.vAverage = vAverage
        self.unit_vector = unit_vector


def Load_data(fileName):
    lines = []
    line_count = 0
    
    with open(fileName) as setup:
        csv_reader = csv.reader(setup, delimiter=',')
        for row in csv_reader:
            if line_count == 0:
                print(row)
            else:    
                lines.append(line([float(row[1]),float(row[2])],[float(row[3]),float(row[4])],float(row[5]),np.array(row[6])))

            line_count += 1      
    return(lines)

def MakeLineGroups(lines):
    
    list_unit_vectors = []
    for i in range(len(lines)):
        if lines[i].unit_vector not in list_unit_vectors:
            list_unit_vectors.append(lines[i].unit_vector)
    
    lineGroups = []
    for k in range(len(list_unit_vectors)):
        lineGroups.append(line_group(list_unit_vectors[k]))
        for i in range(len(lines)):
            if (list_unit_vectors[k] == lines[i].unit_vector):
                lineGroups[k].AddLine(lines[i])
    return(lineGroups)
        

def main():
    lines = Load_data('output_setup1.csv')
    MakeLineGroups(lines)
    
    return(0)

main()