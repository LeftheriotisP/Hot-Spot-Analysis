import time
from grid import Grid
from getis_ord import calculate_getis_ord
from percentile import calculate_90th_percentile
from plot import plot_all_hotspots

def read_data_from_file(filename):
    data = []
    with open(filename, 'r') as file:  # open filename in read mode
        for line in file:
            point = eval(line.strip()) 
            data.append(point)
    return data

def find_min_max(data):  # Finds the min and max values for x, y and t in the dataset
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

def main():
    filename = 'NewGeoDataS.txt'
    point_data = read_data_from_file(filename)
    
    min_x, max_x, min_y, max_y, min_t, max_t = find_min_max(point_data)
    
    m = int(input("\nEnter the number of columns: "))
    n = int(input("\nEnter the number of rows: "))
    v = int(input("\nEnter the number of layers: "))
    
    grid = Grid(min_x, max_x, min_y, max_y, min_t, max_t, m, n, v, point_data)
    
    if grid:
        print("\nGrid created successfully")
        output_file_90th = '90th_percentile_results.txt'
        output_file_GetisOrd = 'getis_ord_results.txt'
        
        start_time = time.time()
        
        # Calculate 90th percentile hotspots
        with open(output_file_90th, 'w') as file_90th:
            calculate_90th_percentile(grid, file_90th)
        
        # Calculate Getis-Ord hotspots
        with open(output_file_GetisOrd, 'w') as file_GetisOrd:
            calculate_getis_ord(grid, file_GetisOrd)
        
        end_time = time.time()
        execution_time = end_time - start_time
        hours = int(execution_time // 3600)
        minutes = int((execution_time % 3600) // 60)
        seconds = execution_time % 60

        print(f"Execution time: {hours} hours, {minutes} minutes, {seconds:.2f} seconds")
        
        # Plotting hotspots
        plot_all_hotspots(grid)
    else:
        print("Grid creation failed.")

if __name__ == "__main__":
    main()