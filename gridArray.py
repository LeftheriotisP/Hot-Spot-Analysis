import numpy as np


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
        print("Grid after processing data:")
        for x in range(self.m):
            for y in range(self.n):
                for t in range(self.k):
                    cell = self.cells[x][y][t]
                    print(f"Cell[{x}][{y}][{t}]: (xmin={cell.min_x}, xmax={cell.max_x}, ymin={cell.min_y}, ymax={cell.max_y}, tmin={cell.min_t}, tmax={cell.max_t}, count={cell.count})")

        self.find_hotspot() # Calls the find_hotspot method that uses 90%

    def findCell(self, x, y, t):   # findCell is a method that returns the cell that x and y belongs to
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

    def find_points(self, data):    # Finds the points based on the data and adds them to the count of the cell they are in
        for x, y, t in data:
            # print(f"Processing point ({x}, {y}, {t})")

            cell = self.findCell(x, y, t) # Calls the findCell method
            if cell:
                cell.count += 1
            else:
                print("Couldn't update count")
    
    #Calculate hot-spot with 90-th percentile     
    def find_hotspot(self):         
        # Extract cell counts from cells
        cell_counts = [cell.count for row in self.cells for col in row for cell in col if cell.count != 0]
        
        # Print cell counts in ascending order 
        print("Cell Counts in ascending order:", sorted(cell_counts))
        '''
        # Calculate the 90th percentile
        #percentile_90 = np.percentile(cell_counts, 90)

        #print("90th-percentile:", percentile_90)

        
        # Find hotspots based on the 90th percentile
        flag = False
        for x in range(self.m):
            for y in range(self.n):
                for t in range(self.k):
                    cell = self.cells[x][y][t]
                    if cell.count > percentile_90:
                        print(f'Concentration found at Cell[{x}][{y}][{t}]: count={cell.count}')
                        flag = True
        if not flag:
            print('Did not find any hotspots')
        '''
    '''
    #calculate the mean of the dataset
    def calculate_mean(self):
        total_counts = sum(cell.count for row in self.cells for col in row for cell in col)
        total_cells = self.m * self.n * self.k

        #printing total_counts and total_cells for testing
        print('total_counts=', total_counts, 'total_cells=', total_cells)
        
        if total_cells > 0:
            return total_counts / total_cells
        else:
            return 0
        
        #calculate variance for getis-ord
        def calculate_standard_deviation(self):

            #make a list with all the counts
            total_counts = [cell.count for row in self.cells for col in row for cell in col]   
            total_cells = self.m * self.n * self.k

            #mean of all counts
            mean = sum(total_counts) / total_cells
            print("Mean in standard deviation is=", mean)

            #mean of the squares of all counts using the list of counts
            mean_of_squares = sum(count ** 2 for count in total_counts) / total_cells
            print("Square Mean in standard deviation is=", mean_of_squares)
            variance = mean_of_squares - (mean ** 2)
            standard_deviation = np.sqrt(variance)
            return standard_deviation
        '''
    #calculate getis-ord statistic for each cell
    def calculate_getis_ord(self):
        #loop for cell i
        for x in range(self.m):
            for y in range(self.n):
                for t in range(self.k):
                    cell_i = self.cells[x][y][t]
                    #initializing sums
                    weight_sum = 0 
                    squared_weight_sum = 0
                    weighted_count_sum = 0
                    counts_sum = 0 
                    squared_counts_sum = 0
                    
                    #loop for cell j
                    for b in range(self.m):
                        for c in range(self.n):
                            for d in range(self.k):
                                if (b, c, d) != (x, y, t):  #if cell i != cell j
                                    cell_j = self.cells[b][c][d]

                                    # Calculate the distance from the reference cell

                                    distance_x = abs(x - b)
                                    distance_y = abs(y - c)
                                    distance_t = abs(t - d)

                                    # Calculate the maximum distance
                                    max_distance = max(distance_x, distance_y, distance_t)
                                    
                                    #calculating weight i,j
                                    weight = 2 ** (1 - max_distance)
                                    
                                    #calculating sum of weights 
                                    weight_sum += weight
                                    
                                    #calculating sum of squared weights 
                                    squared_weight_sum += weight ** 2
                                    
                                    # Multiply the weight by the count score of cell j
                                    weighted_count = weight * cell_j.count

                                    # Add the weighted count to the sum for cell i
                                    weighted_count_sum += weighted_count

                                    counts_sum += cell_j.count
                                    squared_counts_sum += cell_j.count ** 2
                                    
                    #loop end                
                    total_cells = self.m * self.n * self.k
                    #calculate mean
                    mean = counts_sum / total_cells

                    #calculate standard deviation
                    standard_deviation = np.sqrt((squared_counts_sum/total_cells) - (mean ** 2))
                    getis_ord_numerator = (weighted_count_sum - (mean * weight_sum))
                    getis_ord_denominator = (standard_deviation * np.sqrt(((total_cells * squared_weight_sum) - (weight_sum ** 2)) /(total_cells - 1)) )
                    cell_i.getis_ord = getis_ord_numerator / getis_ord_denominator
                    if (x, y, t) == (0, 0, 0):
                        # Print intermediate calculations
                        print(f"Intermediate calculations for Cell[{x}][{y}][{t}]:")
                        print(f"Weight sum: {weight_sum}")
                        print(f"Squared weight sum: {squared_weight_sum}")
                        print(f"Weighted count sum: {weighted_count_sum}")
                        print(f"Counts sum: {counts_sum}")
                        print(f"Squared counts sum: {squared_counts_sum}")
                        print(f"Mean: {mean}")
                        print(f"Standard deviation: {standard_deviation}")

                    print(f"Getis-Ord statistic for Cell[{x}][{y}][{t}]: {cell_i.getis_ord}")


        
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

    # print("In the find_min_max method:")
    print(f"Minimum X: {min_x}, Maximum X: {max_x}")
    print(f"Minimum Y: {min_y}, Maximum Y: {max_y}")  
    print(f"Minimum T: {min_t}, Maximum T: {max_t}")  
    return min_x, max_x, min_y, max_y, min_t, max_t

def read_data_from_file(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            # Parse each line as a tuple directly
            point = eval(line.strip())  # Safely evaluates a string containing a Python expression
            data.append(point)
    return data


filename = 'GeoDataSmall.txt'   #file that contains the dataset
point_data = read_data_from_file(filename)

# Calculate the number of entries
num_entries = len(point_data)


min_x, max_x, min_y, max_y, min_t, max_t = find_min_max(point_data)
  


# Ask user for the number of splits
m = int(input("Enter the number of columns you want to have: "))

n = int(input("Enter the number of rows you want to have: "))

k = int(input("Enter the number of layers you want to have: "))

# Create the Grid
grid = Grid(min_x, max_x, min_y, max_y, min_t, max_t, m, n, k, point_data)  
if grid:
    grid.calculate_getis_ord()
    """
        print("Grid created successfully.")
        #call the calculate_mean and print result
        mean_value = grid.calculate_mean()
        print("Mean of the dataset:", mean_value)
        standard_deviation = grid.calculate_standard_deviation()
        print("Standard Deviation:", standard_deviation)
    """
else:
    print("Grid creation failed.")