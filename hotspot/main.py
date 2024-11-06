import time
from grid import Grid
from getis_ord import calculate_getis_ord
from percentile import calculate_90th_percentile
from plot import plot_all_hotspots_at_t 
from sort90th import sort_90th_file 
from sortGetisOrdResults import sort_getis_ord_file 
from jaccard_index import calculate_jaccard_index 

def read_data_from_file(filename):
    data = []
    with open(filename, 'r') as file:  #open filename in read mode
        for line in file:
            point = eval(line.strip()) 
            data.append(point)
    return data

def find_min_max(data):  #Find the min and max values for x, y and t in the dataset
    if not data:
        return print("Data is empty")

    min_x = float('inf')  #Initializing min and max values
    max_x = float('-inf') 
    min_y = float('inf')
    max_y = float('-inf') 
    min_t = float('inf')
    max_t = float('-inf')

    for x, y, t in data:
        #Update minimum and maximum values 
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
    filename = 'Geodata.txt'
    point_data = read_data_from_file(filename)
    
    min_x, max_x, min_y, max_y, min_t, max_t = find_min_max(point_data)
    
    m = int(input("\nEnter the number of columns: "))
    n = int(input("\nEnter the number of rows: "))
    v = int(input("\nEnter the number of layers: "))

    start_time = time.time()
    start_grid_time = time.time()

    grid = Grid(min_x, max_x, min_y, max_y, min_t, max_t, m, n, v, point_data)
    
    end_grid_time = time.time()
    grid_creation_time = end_grid_time - start_grid_time
    
    if grid:
        print("\nGrid created successfully")
        output_file_90th = '90th_percentile_results.txt'
        output_file_GetisOrd = 'getis_ord_results.txt'
        
        

        #Calculate 90th percentile hotspots
        percentile_start_time = time.time()
        with open(output_file_90th, 'w') as file_90th:
            calculate_90th_percentile(grid, file_90th)
        percentile_end_time = time.time()
        percentile_execution_time = percentile_end_time - percentile_start_time
        
        #Calculate Getis-Ord hotspots
        getis_ord_start_time = time.time()
        with open(output_file_GetisOrd, 'w') as file_GetisOrd:
            calculate_getis_ord(grid, file_GetisOrd)
        getis_ord_end_time = time.time()
        getis_ord_execution_time = getis_ord_end_time - getis_ord_start_time
        
        end_time = time.time()

        #sort 90th results
        input_sort_90th = '90th_percentile_results.txt'
        output_sort_90th = 'sorted_90th_percentile_results.txt'
        sort_90th_file(input_sort_90th, output_sort_90th)

        #sortGi* results
        input_filename = 'getis_ord_results.txt'
        output_filename = 'sorted_getis_ord_results.txt'
        sort_getis_ord_file(input_filename, output_filename)

        #calculate jaccard index for 90th and Gi*
        calculate_jaccard_index()   #output jaccard_results.txt

        execution_time = end_time - start_time

        total_execution_time_ms = execution_time * 1000
        grid_creation_time_ms = grid_creation_time * 1000
        percentile_execution_time_ms = percentile_execution_time * 1000
        getis_ord_execution_time_ms = getis_ord_execution_time * 1000

        print(f"Total execution time: {total_execution_time_ms:.2f} ms")
        print(f"Grid creation time: {grid_creation_time_ms:.2f} ms")
        print(f"90th percentile calculation time: {percentile_execution_time_ms:.2f} ms")
        print(f"Getis-Ord calculation time: {getis_ord_execution_time_ms:.2f} ms")
               
        #plot hotspots
        plot_all_hotspots_at_t(grid)
    else:
        print("Grid creation failed.")

if __name__ == "__main__":
    main()