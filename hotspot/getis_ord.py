import numpy as np

def calculate_getis_ord(self, file_GetisOrd):
    while True:
        try:
            a = int(input("\nEnter the value of parameter a (a > 1): "))
            if a <= 1:
                print("The parameter 'a' must be greater than 1. Please enter a correct value.")
            else:
                break
        except ValueError:
            print("Invalid input, please enter a numeric value for parameter a.")

    while True:
        try:
            k = int(input("\nEnter the distance for counting neighbours: "))
            if k <= 0:
                print("The distance for counting neighbours must be a positive integer. Please enter a correct value.")
            elif k >= min(self.m, self.n, self.v):
                print(f"The distance for counting neighbours is larger than the grid dimensions. Adjusting k to fit within grid boundaries.")
                k = min(self.m, self.n, self.v) - 1  
                break
            else:
                break
        except ValueError:
            print("Invalid input, please enter an integer value for distance k.")

    while True:
        try:
            h = float(input("\nEnter the threshold for Getis-Ord (1.65, 1.96, 2.58): "))
            if h == 1.65:
                print("Threshold set to 90% confidence level (1.65).")
                break
            elif h == 1.96:
                print("Threshold set to 95% confidence level (1.96).")
                break
            elif h == 2.58:
                print("Threshold set to 99% confidence level (2.58).")
                break
            else:
                print("Invalid threshold. Please enter one of the following values: 1.65, 1.96, or 2.58.")
        except ValueError:
            print("Invalid input. Please enter a valid numeric value (1.65, 1.96, or 2.58).")
    
    #Calculate mean and standard deviation
    total_cells = self.m * self.n * self.v
    counts_sum = 0
    squared_counts_sum = 0

    # Loop through all cells
    for x in range(self.m):
        for y in range(self.n):
            for t in range(self.v):
                cell = self.cells[x][y][t]
                counts_sum += cell.count
                squared_counts_sum += cell.count ** 2

    #Calculate mean
    mean = counts_sum / total_cells

    #Calculate standard deviation
    if (squared_counts_sum / total_cells) - (mean ** 2) > 0:
        standard_deviation = np.sqrt((squared_counts_sum / total_cells) - (mean ** 2))
    else:
        standard_deviation = 1

    #file_GetisOrd.write(f'Getis-Ord Statistic with a={a} and threshold={h}\n')
    file_GetisOrd.write(f'Counting up to {k} neighbours\n')
    file_GetisOrd.write('\nCell Coordinates\tGetis-Ord Statistic\n')
    
    # Loop for cell i
    for x in range(self.m):
        for y in range(self.n):
            for t in range(self.v):
                cell_i = self.cells[x][y][t]

                # Initializing sums
                weight_sum = 0 
                squared_weight_sum = 0
                weighted_count_sum = 0

                # Loop for cell j
                for b in range(max(0, x - k), min(self.m, x + k)):
                    for c in range(max(0, y - k), min(self.n, y + k)):
                        for d in range(max(0, t - k), min(self.v, t + k)):
                            cell_j = self.cells[b][c][d]

                            # calculate the distance cell i from cell j
                            distance_x = abs(x - b)
                            distance_y = abs(y - c)
                            distance_t = abs(t - d)

                            # calculate the maximum distance
                            max_distance = max(distance_x, distance_y, distance_t)

                            # calculating weight i,j (w=a^1-r, a>1 , r=distance i,j)
                            
                            if max_distance <= k:    #Limiting the influence of further neighbours to gain computational efficiency
                                weight = a ** (1 - max_distance)
                            else:
                                weight = 0 

                            # calculating sum of weights 
                            weight_sum += weight

                            # calculating sum of squared weights 
                            squared_weight_sum += weight ** 2

                            # add the weighted count to the sum for cell i
                            weighted_count_sum += weight * cell_j.count

                #check for denominator = 0
                denominator = (standard_deviation * np.sqrt(((total_cells * squared_weight_sum) - (weight_sum ** 2)) / (total_cells - 1)))
                if denominator == 0:
                    cell_i.getis_ord = 0
                else:
                    #Final Calculation of Getis-Ord
                    cell_i.getis_ord = (weighted_count_sum - (mean * weight_sum)) / denominator

                #print(f"[{x}][{y}][{t}] = {cell_i.getis_ord}")
                #file_GetisOrd.write(f"({x},{y},{t}) = {cell_i.getis_ord}\n")
                
                #if above threshold add to hotspots
                threshold = 1.96

                if cell_i.getis_ord > threshold:
                    file_GetisOrd.write(f"({x},{y},{t}) = {cell_i.getis_ord}\n")
                    self.hotspots_getis_ord.append((x, y, t, cell_i.getis_ord))
    
    #prints to detect errors
    #print(f"this is mean: {mean}")
    #print(f"this is standard dev:{standard_deviation}")
    
    print("\nGetis-Ord calculated successfully")
