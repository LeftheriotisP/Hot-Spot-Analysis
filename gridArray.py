import numpy as np
import time

class Cell: #Cell class consists of the borders of the cell and the number of points inside the cell
    def __init__(self, min_x, max_x, min_y, max_y, min_t, max_t, count=0):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_t = min_t
        self.max_t = max_t
        self.count = count 
        self.getis_ord = None  # Initialize Getis-Ord statistic

class Grid: 
    """
    Grid class represents a 3D Array divided into cells

   'm, n, k' is the number of splits on each axis
    m for x , n for y and k for t axis

    'data' is a list of points in the form of (x, y, t)
    """
    def __init__(self, min_x, max_x, min_y, max_y, min_t, max_t, m, n, k, data):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_t = min_t
        self.max_t = max_t
        self.m = m
        self.n = n
        self.k = k

        # Calculate the step size for each axis
        x_step = (max_x - min_x) / m
        y_step = (max_y - min_y) / n
        t_step = (max_t - min_t) / k
        print(f"x_step: {x_step}, y_step: {y_step}, t_step: {t_step}")
        
        # Cell(min_x, max_x, min_y, max_y, min_t, max_t)
        self.cells = [
            [
                [
                    Cell(
                        min_x + x * x_step, min_x + (x + 1) * x_step,   #Cell size
                        min_y + y * y_step, min_y + (y + 1) * y_step,
                        min_t + t * t_step, min_t + (t + 1) * t_step
                    )
                    for t in range(k)
                ]
                for y in range(n)
            ]
            for x in range(m)
        ]
        
        self.find_points(data)  # Calls the find_points method
        print("\nProcessing grid")
        
        '''
        #Printing cells for testing
        for x in range(self.m):
            for y in range(self.n):
                for t in range(self.k):
                    cell = self.cells[x][y][t]
                    print(f"Cell[{x}][{y}][{t}]: (xmin={cell.min_x}, xmax={cell.max_x}, ymin={cell.min_y}, ymax={cell.max_y}, tmin={cell.min_t}, tmax={cell.max_t}, count={cell.count})")
        '''         
            
    def find_points(self, data):    # Finds the points based on the data and adds them to the count of the cell they are in
        for x, y, t in data:
            # print(f"Processing point ({x}, {y}, {t})")
            cell = self.findCell(x, y, t) # Calls the findCell method
            if cell:
                cell.count += 1
            else:
                print("Couldn't update count")

    def findCell(self, x, y, t):   # findCell returns the cell that x, y, t belongs to
        col = int((x - self.min_x) / (self.max_x - self.min_x) * self.m) # (x-x_min)/x_step
        row = int((y - self.min_y) / (self.max_y - self.min_y) * self.n) # (y-y_min)/y_step
        layer = int((t - self.min_t) / (self.max_t - self.min_t) * self.k)  # (t-t_min)/t_step

        if x == self.max_x: # If x, y or t = max values 
            col = self.m - 1  
        if y == self.max_y: 
            row = self.n - 1
        if t == self.max_t:  
            layer = self.k - 1
            
        if 0 <= col < self.m and 0 <= row < self.n and 0 <= layer < self.k: 
            return self.cells[col][row][layer]
        else:
            print("Couldn't find cell")
        
    
    #----Calculate hot-spot with 90-th percentile----     
    def find_hotspot(self, file):         
        # Extract cell counts from cells
        cell_counts = [cell.count for row in self.cells for col in row for cell in col if cell.count != 0]
        
        #Print cell counts in ascending order 
        #print("Cell Counts in ascending order:", sorted(cell_counts))
        
        # Calculate the 90th percentile
        percentile_90 = np.percentile(cell_counts, 90)

        #Write the 90th percentile in text file
        file.write(f"90th-percentile: {percentile_90}\n")

        #print("90th-percentile:", percentile_90)
        print("\n90th-percentile calculated succefully")
        
        # Find hotspots based on the 90th percentile
        flag = False
        for x in range(self.m):
            for y in range(self.n):
                for t in range(self.k):
                    cell = self.cells[x][y][t]
                    if cell.count > percentile_90:
                        #print(f'Concentration found at Cell[{x}][{y}][{t}]: count={cell.count}') #Print for testing

                        #Write hot spots from 90th percentile on text file
                        file.write(f'Hot spot at ({x},{y},{t}): count={cell.count}\n')

                        flag = True
        if not flag:
            print('Did not find any hotspots')  

    #----Calculate getis-ord statistic for each cell----
    def calculate_getis_ord(self, file):

        a = int(input("\nEnter the value of parameter a: "))

        # Calculate mean and standard deviation
        total_cells = self.m * self.n * self.k
        #print(f"total cells: {total_cells}")
        counts_sum = 0
        squared_counts_sum = 0
    
        # Loop through all cells
        for x in range(self.m):
            for y in range(self.n):
                for t in range(self.k):
                    cell = self.cells[x][y][t]
                    counts_sum += cell.count
                    squared_counts_sum += cell.count ** 2

        #print(f"counts_sum: {counts_sum}") #Prints for testing
        #print(f"squared_counts_sum: {squared_counts_sum}")

        # Calculate mean
        mean = counts_sum / total_cells
    
        # Calculate standard deviation
        standard_deviation = np.sqrt((squared_counts_sum / total_cells) - (mean ** 2))
 
        # Writing a header in the text file
        file.write('\nCell Coordinates\tGetis-Ord Statistic\n')

        #Loop for cell i
        for x in range(self.m):
            for y in range(self.n):
                for t in range(self.k):
                    cell_i = self.cells[x][y][t]

                    #Initializing sums
                    weight_sum = 0 
                    squared_weight_sum = 0
                    weighted_count_sum = 0
                    counts_sum = 0 
                    squared_counts_sum = 0

                    #Loop for cell j
                    for b in range(self.m):
                        for c in range(self.n):
                            for d in range(self.k):
                                    cell_j = self.cells[b][c][d]

                                    #Calculate the distance cell i from cell j

                                    distance_x = abs(x - b)
                                    distance_y = abs(y - c)
                                    distance_t = abs(t - d)

                                    #Calculate the maximum distance
                                    max_distance = max(distance_x, distance_y, distance_t)

                                    #Calculating weight i,j (w=a^1-r, a>1 , r=distance i,j)
                                    weight = a ** (1 - max_distance)

                                    #Calculating sum of weights 
                                    weight_sum += weight

                                    #Calculating sum of squared weights 
                                    squared_weight_sum += weight ** 2

                                    # Multiply the weight by the count score of cell j
                                    weighted_count = weight * cell_j.count

                                    # Add the weighted count to the sum for cell i
                                    weighted_count_sum += weighted_count

                    #Loop end                                   
                    #Final calculation of getis-ord
                    cell_i.getis_ord = (weighted_count_sum - (mean * weight_sum)) / (standard_deviation * np.sqrt(((total_cells * squared_weight_sum) - (weight_sum ** 2)) /(total_cells - 1)) )

                    print(f"Getis-Ord statistic for Cell[{x}][{y}][{t}]: {cell_i.getis_ord}") #Print for testing
                    file.write(f"({x},{y},{t})\t{cell_i.getis_ord}\n")
        print("\nGetis-Ord calculated succefully")


        
def find_min_max(data): # Finds the min and max values for x, y and t in the dataset
    if not data:
        return print("Data is empty")

    min_x = float('inf')  # Initializing min and max values
    max_x = float('-inf') 
    min_y = float('inf')
    max_y = float('-inf') 
    min_t = float('inf')
    max_t = float('-inf')

    for x, y, t in data:
        # Update minimum and maximum values 
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        min_t = min(min_t, t)
        max_t = max(max_t, t)


    print(f"Minimum X: {min_x}, Maximum X: {max_x}")
    print(f"Minimum Y: {min_y}, Maximum Y: {max_y}")  
    print(f"Minimum T: {min_t}, Maximum T: {max_t}")  
    return min_x, max_x, min_y, max_y, min_t, max_t

def read_data_from_file(filename):
    data = []
    with open(filename, 'r') as file: # open filename in read mode
        for line in file:
            # Parse each line as a tuple 
            point = eval(line.strip()) 
            data.append(point)
    return data



filename = 'GeoDataS.txt'   # file that contains the dataset
point_data = read_data_from_file(filename)

# Calculate the number of entries
num_entries = len(point_data)


min_x, max_x, min_y, max_y, min_t, max_t = find_min_max(point_data)
  


# Ask user for the number of splits
m = int(input("\nEnter the number of columns: "))

n = int(input("\nEnter the number of rows: "))

k = int(input("\nEnter the number of layers: "))

# Define the path to the output file
output_file_path = 'hot_spot_results.txt'

# Create the Grid
grid = Grid(min_x, max_x, min_y, max_y, min_t, max_t, m, n, k, point_data)  
if grid:
    print("\nGrid created succesfully")
    with open(output_file_path, 'w') as file:
        start_time = time.time() #starting timer to time 90th percentile and getis ord
        
        grid.find_hotspot(file)
        grid.calculate_getis_ord(file)

    end_time = time.time()  #end timer
    execution_time = end_time - start_time
    #convert time to hours, minutes, and seconds
    hours = int(execution_time // 3600)
    minutes = int((execution_time % 3600) // 60)
    seconds = execution_time % 60

    # Print execution time in a human-readable format
    print(f"Execution time: {hours} hours, {minutes} minutes, {seconds:.2f} seconds")   
else:
    print("Grid creation failed.")
    end_time = time.time()