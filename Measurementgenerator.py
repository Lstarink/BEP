
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import csv

class vector_field:
    def __init__(self, u, v):
        self.u = u
        self.v = v
    
    def Sample(self, x_n, y_n):
        expr_u = self.u
        expr_v = self.v
        x = sp.symbols('x')
        y = sp.symbols('y')
        
        u_x = expr_u.subs({x:x_n,y:y_n})               
        u_y = expr_v.subs({x:x_n,y:y_n})
        v = np.array([u_x,u_y])
        return(v)
        
    def Plot(self,L,n):
        x = np.linspace(-L/2,L/2,n)
        y = np.linspace(-L/2,L/2,n)
        X, Y = np.meshgrid(x,y)
        
        u_x_vec = np.zeros([len(x),len(y)])
        u_y_vec = np.zeros([len(x),len(y)])
        
        for i in range(0, len(x)):
            for j in range(0, len(y)):
                v = self.Sample(x[i], y[j])
                
                u_x_vec[i][j] = v[0]
                u_y_vec[i][j] = v[1]
        
        plt.figure()
        plt.quiver(y, x, u_y_vec, u_x_vec)
        plt.show()
        return()

class line:
    def __init__(self, A, B):
        self.A = A
        self.B = B
        self.length = line.Length(self)
        self.unit_vector = line.Unit_vector(self)
        
    def Unit_vector(self):
        unit_vector = np.array([self.B[0]-self.A[0],self.B[1]-self.A[1]])/self.length
        return(unit_vector)
        
    def Length(self):
        dX = self.B[0] - self.A[0]
        dY = self.B[1] - self.A[1]
        
        length = (dX**2 + dY**2)**0.5
        return(length)
    
    def V_average(self, field):
        iteration_steps = 100               #Numerical integration setting
        ds = self.length/iteration_steps
        
        v_sum = 0
        for i in range(0, iteration_steps):
            location_x = self.A[0] + self.unit_vector[0]*ds*i
            location_y = self.A[1] + self.unit_vector[1]*ds*i
            v = field.Sample(location_x, location_y)
            
            v_projected = np.dot(v,self.unit_vector)
            v_sum += v_projected
            
        v_average = v_sum/iteration_steps
    
        return(v_average)
    
class Measurement_setup:
    def __init__(self, file):
        self.file_name = file
        self.lines = Measurement_setup.MakeLines(self)
        
    def MakeLines(self):
        lines = []
        line_count = 0
        
        with open(self.file_name) as setup:
            csv_reader = csv.reader(setup, delimiter=',')
            for row in csv_reader:
                if line_count == 0:
                    print(row)
                else:    
                    lines.append(line([float(row[1]),float(row[2])],[float(row[3]),float(row[4])]))
    
                line_count += 1
                print(line_count)        
        return(lines)
    
    def SaveMeasurements(self,field, outputfile):
        row_count = 0
        with open(self.file_name, 'r') as read_obj, \
             open(outputfile, 'w', newline='') as write_obj:
                 csv_reader = csv.reader(read_obj)
                 csv_writer = csv.writer(write_obj)
                 for row in csv_reader:
                     if row_count == 0:
                         row.append('V_average')
                         row.append('Unit_vector_x')
                     else:
                         row.append(self.lines[row_count-1].V_average(field))
                         row.append(self.lines[row_count-1].unit_vector)
                     csv_writer.writerow(row)
                     row_count += 1
        return()
    
    def plot_setup(self):
        plt.figure()
        for i in range(len(self.lines)):
            plt.plot([self.lines[i].A[0],self.lines[i].B[0]],
                     [self.lines[i].A[1],self.lines[i].B[1]], color = 'b')  
        plt.show()
        return()
    
def instantiate_field1():
    x = sp.symbols('x')
    y = sp.symbols('y')
    
    u = x**2
    v = y   
    return(u,v)


def main():
    #Make a vector field
    field = instantiate_field1()
    field1 = vector_field(field[0],field[1])
    field1.Plot(1, 12)
    
    #Load setup
    measurement_setup = Measurement_setup('setup1.csv')
    #Calculate and save it
    measurement_setup.SaveMeasurements(field1, 'output_setup1.csv')
    #Show setup
    measurement_setup.plot_setup()
    print(measurement_setup.lines[1].unit_vector)

main()
