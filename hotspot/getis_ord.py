import numpy as np

def calculate_getis_ord(self, file_GetisOrd):
    a = int(input("\nEnter the value of parameter a: "))
    # Calculate mean and standard deviation
    total_cells = self.m * self.n * self.k
    counts_sum = 0
    squared_counts_sum = 0

    # Loop through all cells
    for x in range(self.m):
        for y in range(self.n):
            for t in range(self.k):
                cell = self.cells[x][y][t]
                counts_sum += cell.count
                squared_counts_sum += cell.count ** 2

    # Calculate mean
    mean = counts_sum / total_cells

    # Calculate standard deviation
    if (squared_counts_sum / total_cells) - (mean ** 2) > 0:
        standard_deviation = np.sqrt((squared_counts_sum / total_cells) - (mean ** 2))
    else:
        standard_deviation = 1

    #file_GetisOrd.write(f'Getis-Ord Statistic with a={a}\n')
    #file_GetisOrd.write('\nCell Coordinates\tGetis-Ord Statistic\n')

    # Loop for cell i
    for x in range(self.m):
        for y in range(self.n):
            for t in range(self.k):
                cell_i = self.cells[x][y][t]

                # Initializing sums
                weight_sum = 0 
                squared_weight_sum = 0
                weighted_count_sum = 0

                # Loop for cell j
                for b in range(max(0, x - 2), min(self.m, x + 2)):
                    for c in range(max(0, y - 2), min(self.n, y + 2)):
                        for d in range(max(0, t - 2), min(self.k, t + 2)):
                            cell_j = self.cells[b][c][d]

                            # Calculate the distance cell i from cell j
                            distance_x = abs(x - b)
                            distance_y = abs(y - c)
                            distance_t = abs(t - d)

                            # Calculate the maximum distance
                            max_distance = max(distance_x, distance_y, distance_t)

                            # Calculating weight i,j (w=a^1-r, a>1 , r=distance i,j)
                            
                            if max_distance <= 2:    #Limiting the influence of further neighbours to gain computational efficiency
                                weight = a ** (1 - max_distance)
                            else:
                                weight = 0 

                            # Calculating sum of weights 
                            weight_sum += weight

                            # Calculating sum of squared weights 
                            squared_weight_sum += weight ** 2

                            # Add the weighted count to the sum for cell i
                            weighted_count_sum += weight * cell_j.count

                # Avoiding case were denominator = 0
                denominator = (standard_deviation * np.sqrt(((total_cells * squared_weight_sum) - (weight_sum ** 2)) / (total_cells - 1)))
                if denominator == 0:
                    cell_i.getis_ord = 0
                else:
                    # Final calculation of Getis-Ord
                    cell_i.getis_ord = (weighted_count_sum - (mean * weight_sum)) / denominator

                print(f"[{x}][{y}][{t}] = {cell_i.getis_ord}")
                file_GetisOrd.write(f"({x},{y},{t}) = {cell_i.getis_ord}\n")
                
                # Add to Getis-Ord hotspots if above threshold
                threshold = 2.0  # Define a threshold for Getis-Ord statistic
                if cell_i.getis_ord > threshold:
                    self.hotspots_getis_ord.append((x, y, t, cell_i.getis_ord))
    
    print("\nGetis-Ord calculated successfully")
