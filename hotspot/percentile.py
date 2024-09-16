import numpy as np
def calculate_90th_percentile(grid, file_90th):         
    # Extract cell counts from cells
    cell_counts = [cell.count for row in grid.cells for col in row for cell in col if cell.count != 0]
    
    # Calculate the 90th percentile
    percentile_90 = np.percentile(cell_counts, 90)

    # Write the 90th percentile in text file
    #file_90th.write(f"90th-percentile: {percentile_90}\n")
    print("\n90th-percentile calculated successfully")
    
    # Find hotspots based on the 90th percentile
    flag = False
    for x in range(grid.m):
        for y in range(grid.n):
            for t in range(grid.v):
                cell = grid.cells[x][y][t]
                if cell.count > percentile_90:
                    grid.hotspots_90th.append((x, y, t, cell.count))
                    file_90th.write(f'({x},{y},{t}) = {cell.count}\n')
                    flag = True
    if not flag:
        print('Did not find any hotspots')  
