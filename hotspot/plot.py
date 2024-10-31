import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D

def plot_90th_hotspots(grid):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    cells = grid.cells
    hotspots_90th = grid.hotspots_90th
    
    # Initialize the lists for batch plotting
    x_vals_90th, y_vals_90th, t_vals_90th = [], [], []
    dx_vals_90th, dy_vals_90th, dt_vals_90th = [], [], []
    
    x_vals_normal, y_vals_normal, t_vals_normal = [], [], []
    dx_vals_normal, dy_vals_normal, dt_vals_normal = [], [], []
    
    x_vals_empty, y_vals_empty, t_vals_empty = [], [], []
    dx_vals_empty, dy_vals_empty, dt_vals_empty = [], [], []

    # Collect bar data for 90th percentile hotspots, regular cells, and empty cells
    for x in range(grid.m):
        for y in range(grid.n):
            for t in range(grid.v):
                cell = cells[x][y][t]
                
                # Collect the cell dimensions and coordinates
                min_x, min_y, min_t = cell.min_x, cell.min_y, cell.min_t
                max_x, max_y, max_t = cell.max_x, cell.max_y, cell.max_t
                dx, dy, dt = max_x - min_x, max_y - min_y, max_t - min_t

                if cell.count == 0:
                    # Collect data for empty cells (gray)
                    x_vals_empty.append(min_x)
                    y_vals_empty.append(min_y)
                    t_vals_empty.append(min_t)
                    dx_vals_empty.append(dx)
                    dy_vals_empty.append(dy)
                    dt_vals_empty.append(dt)
                elif (x, y, t, cell.count) in hotspots_90th:
                    # Collect data for 90th percentile hotspots (red)
                    x_vals_90th.append(min_x)
                    y_vals_90th.append(min_y)
                    t_vals_90th.append(min_t)
                    dx_vals_90th.append(dx)
                    dy_vals_90th.append(dy)
                    dt_vals_90th.append(dt)
                else:
                    # Collect data for normal cells (light blue)
                    x_vals_normal.append(min_x)
                    y_vals_normal.append(min_y)
                    t_vals_normal.append(min_t)
                    dx_vals_normal.append(dx)
                    dy_vals_normal.append(dy)
                    dt_vals_normal.append(dt)

    # Batch plot all the empty cells (grey) in one call
    ax.bar3d(x_vals_empty, y_vals_empty, t_vals_empty, 
             dx_vals_empty, dy_vals_empty, dt_vals_empty, 
             color='grey', alpha=0)

    # Batch plot all the 90th percentile hotspots (red) in one call
    ax.bar3d(x_vals_90th, y_vals_90th, t_vals_90th, 
             dx_vals_90th, dy_vals_90th, dt_vals_90th, 
             color='red', alpha=0.7)

    # Batch plot all the normal cells (light blue) in one call
    ax.bar3d(x_vals_normal, y_vals_normal, t_vals_normal, 
             dx_vals_normal, dy_vals_normal, dt_vals_normal, 
             color='lightblue', alpha=0.05)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('T')
    ax.set_title('Hotspots based on 90th Percentile')
    
    plt.show()


def plot_getis_ord_hotspots(grid):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    cells = grid.cells
    hotspots_getis_ord = grid.hotspots_getis_ord
    
    # Initialize the lists for batch plotting
    x_vals_getis_ord, y_vals_getis_ord, t_vals_getis_ord = [], [], []
    dx_vals_getis_ord, dy_vals_getis_ord, dt_vals_getis_ord = [], [], []
    
    x_vals_normal, y_vals_normal, t_vals_normal = [], [], []
    dx_vals_normal, dy_vals_normal, dt_vals_normal = [], [], []
    
    x_vals_empty, y_vals_empty, t_vals_empty = [], [], []
    dx_vals_empty, dy_vals_empty, dt_vals_empty = [], [], []

    # Collect bar data for Getis-Ord hotspots, regular cells, and empty cells
    for x in range(grid.m):
        for y in range(grid.n):
            for t in range(grid.v):
                cell = cells[x][y][t]
                
                # Collect the cell dimensions and coordinates
                min_x, min_y, min_t = cell.min_x, cell.min_y, cell.min_t
                max_x, max_y, max_t = cell.max_x, cell.max_y, cell.max_t
                dx, dy, dt = max_x - min_x, max_y - min_y, max_t - min_t

                if cell.count == 0:
                    # Collect data for empty cells (gray)
                    x_vals_empty.append(min_x)
                    y_vals_empty.append(min_y)
                    t_vals_empty.append(min_t)
                    dx_vals_empty.append(dx)
                    dy_vals_empty.append(dy)
                    dt_vals_empty.append(dt)
                elif (x, y, t, cell.getis_ord) in hotspots_getis_ord:
                    # Collect data for Getis-Ord hotspots (green)
                    x_vals_getis_ord.append(min_x)
                    y_vals_getis_ord.append(min_y)
                    t_vals_getis_ord.append(min_t)
                    dx_vals_getis_ord.append(dx)
                    dy_vals_getis_ord.append(dy)
                    dt_vals_getis_ord.append(dt)
                else:
                    # Collect data for normal cells (light blue)
                    x_vals_normal.append(min_x)
                    y_vals_normal.append(min_y)
                    t_vals_normal.append(min_t)
                    dx_vals_normal.append(dx)
                    dy_vals_normal.append(dy)
                    dt_vals_normal.append(dt)

    # Batch plot all the empty cells (grey) in one call
    ax.bar3d(x_vals_empty, y_vals_empty, t_vals_empty, 
             dx_vals_empty, dy_vals_empty, dt_vals_empty, 
             color='grey', alpha=0)

    # Batch plot all the Getis-Ord hotspots (green) in one call
    ax.bar3d(x_vals_getis_ord, y_vals_getis_ord, t_vals_getis_ord, 
             dx_vals_getis_ord, dy_vals_getis_ord, dt_vals_getis_ord, 
             color='green', alpha=0.7)

    # Batch plot all the normal cells (light blue) in one call
    ax.bar3d(x_vals_normal, y_vals_normal, t_vals_normal, 
             dx_vals_normal, dy_vals_normal, dt_vals_normal, 
             color='lightblue', alpha=0.05)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('T')
    ax.set_title('Hotspots based on Getis-Ord Statistic')
    
    plt.show()


def plot_overlap(grid):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    cells = grid.cells
    hotspots_getis_ord = grid.hotspots_getis_ord
    hotspots_90th = grid.hotspots_90th
    
    # Initialize the lists for batch plotting
    x_vals_overlap, y_vals_overlap, t_vals_overlap = [], [], []
    dx_vals_overlap, dy_vals_overlap, dt_vals_overlap = [], [], []
    
    x_vals_90th, y_vals_90th, t_vals_90th = [], [], []
    dx_vals_90th, dy_vals_90th, dt_vals_90th = [], [], []
    
    x_vals_getis_ord, y_vals_getis_ord, t_vals_getis_ord = [], [], []
    dx_vals_getis_ord, dy_vals_getis_ord, dt_vals_getis_ord = [], [], []
    
    x_vals_normal, y_vals_normal, t_vals_normal = [], [], []
    dx_vals_normal, dy_vals_normal, dt_vals_normal = [], [], []
    
    x_vals_empty, y_vals_empty, t_vals_empty = [], [], []
    dx_vals_empty, dy_vals_empty, dt_vals_empty = [], [], []

    # Collect bar data for overlapping, 90th percentile, Getis-Ord, regular cells, and empty cells
    for x in range(grid.m):
        for y in range(grid.n):
            for t in range(grid.v):
                cell = cells[x][y][t]
                
                # Collect the cell dimensions and coordinates
                min_x, min_y, min_t = cell.min_x, cell.min_y, cell.min_t
                max_x, max_y, max_t = cell.max_x, cell.max_y, cell.max_t
                dx, dy, dt = max_x - min_x, max_y - min_y, max_t - min_t

                if cell.count == 0:
                    # Collect data for empty cells (gray)
                    x_vals_empty.append(min_x)
                    y_vals_empty.append(min_y)
                    t_vals_empty.append(min_t)
                    dx_vals_empty.append(dx)
                    dy_vals_empty.append(dy)
                    dt_vals_empty.append(dt)
                elif (x, y, t, cell.count) in hotspots_90th and (x, y, t, cell.getis_ord) in hotspots_getis_ord:
                    # Collect data for overlap (orange)
                    x_vals_overlap.append(min_x)
                    y_vals_overlap.append(min_y)
                    t_vals_overlap.append(min_t)
                    dx_vals_overlap.append(dx)
                    dy_vals_overlap.append(dy)
                    dt_vals_overlap.append(dt)
                elif (x, y, t, cell.count) in hotspots_90th:
                    # Collect data for 90th percentile hotspots (red)
                    x_vals_90th.append(min_x)
                    y_vals_90th.append(min_y)
                    t_vals_90th.append(min_t)
                    dx_vals_90th.append(dx)
                    dy_vals_90th.append(dy)
                    dt_vals_90th.append(dt)
                elif (x, y, t, cell.getis_ord) in hotspots_getis_ord:
                    # Collect data for Getis-Ord hotspots (green)
                    x_vals_getis_ord.append(min_x)
                    y_vals_getis_ord.append(min_y)
                    t_vals_getis_ord.append(min_t)
                    dx_vals_getis_ord.append(dx)
                    dy_vals_getis_ord.append(dy)
                    dt_vals_getis_ord.append(dt)
                else:
                    # Collect data for normal cells (light blue)
                    x_vals_normal.append(min_x)
                    y_vals_normal.append(min_y)
                    t_vals_normal.append(min_t)
                    dx_vals_normal.append(dx)
                    dy_vals_normal.append(dy)
                    dt_vals_normal.append(dt)

    # Batch plot all the empty cells (grey) in one call
    ax.bar3d(x_vals_empty, y_vals_empty, t_vals_empty, 
             dx_vals_empty, dy_vals_empty, dt_vals_empty, 
             color='grey', alpha=0)

    # Batch plot all the overlapping hotspots (orange) in one call
    ax.bar3d(x_vals_overlap, y_vals_overlap, t_vals_overlap, 
             dx_vals_overlap, dy_vals_overlap, dt_vals_overlap, 
             color='orange', alpha=0.7)

    # Batch plot all the 90th percentile hotspots (red) in one call
    ax.bar3d(x_vals_90th, y_vals_90th, t_vals_90th, 
             dx_vals_90th, dy_vals_90th, dt_vals_90th, 
             color='red', alpha=0.7)

    # Batch plot all the Getis-Ord hotspots (green) in one call
    ax.bar3d(x_vals_getis_ord, y_vals_getis_ord, t_vals_getis_ord, 
             dx_vals_getis_ord, dy_vals_getis_ord, dt_vals_getis_ord, 
             color='green', alpha=0.7)

    # Batch plot all the normal cells (light blue) in one call
    ax.bar3d(x_vals_normal, y_vals_normal, t_vals_normal, 
             dx_vals_normal, dy_vals_normal, dt_vals_normal, 
             color='lightblue', alpha=0.05)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('T')
    ax.set_title('Hot Spots Overlap')
    
    plt.show()


def plot_all_hotspots(grid):
    plot_90th_hotspots(grid)  #Plot 90th percentile hotspots
    plot_getis_ord_hotspots(grid)  #Plot Getis-Ord hotspots
    plot_overlap(grid)  #Plot overlap

