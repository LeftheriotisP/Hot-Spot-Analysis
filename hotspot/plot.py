import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D

def plot_90th_hotspots(ax, grid):
    cells = grid.cells
    hotspots_90th = grid.hotspots_90th

    # Plot the 90th percentile hotspots
    for x in range(grid.m):
        for y in range(grid.n):
            for t in range(grid.k):
                cell = cells[x][y][t]
                if cell.count == 0:
                    color = 'grey'
                    alpha = 0
                else:
                    color = 'lightblue'
                    alpha = 0.1
                    if (x, y, t, cell.count) in hotspots_90th:
                        color = 'red'
                        alpha = 0.7

                ax.bar3d(cell.min_x, cell.min_y, cell.min_t, 
                         cell.max_x - cell.min_x, 
                         cell.max_y - cell.min_y, 
                         cell.max_t - cell.min_t, 
                         color=color, alpha=alpha)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('T')
    ax.set_title('Hotspots based on 90th Percentile')
    ax.legend(handles=[
        mpatches.Patch(color='grey', alpha=0.05, label='Empty Cell'),
        mpatches.Patch(color='lightblue', alpha=0.5, label='Regular Cell'),
        mpatches.Patch(color='red', alpha=0.7, label='Hotspot (90th Percentile)')
    ], loc='upper left', bbox_to_anchor=(1.05, 1), fontsize='small', frameon=False)

def plot_getis_ord_hotspots(ax, grid):
    cells = grid.cells
    hotspots_getis_ord = grid.hotspots_getis_ord

    # Plot the Getis-Ord hotspots
    for x in range(grid.m):
        for y in range(grid.n):
            for t in range(grid.k):
                cell = cells[x][y][t]
                if cell.count == 0:
                    color = 'grey'
                    alpha = 0
                else:
                    color = 'lightblue'
                    alpha = 0.1
                    if (x, y, t, cell.getis_ord) in hotspots_getis_ord:
                        color = 'green'
                        alpha = 0.7

                ax.bar3d(cell.min_x, cell.min_y, cell.min_t, 
                         cell.max_x - cell.min_x, 
                         cell.max_y - cell.min_y, 
                         cell.max_t - cell.min_t, 
                         color=color, alpha=alpha)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('T')
    ax.set_title('Hotspots based on Getis-Ord Statistic')
    ax.legend(handles=[
        mpatches.Patch(color='grey', alpha=0.05, label='Empty Cell'),
        mpatches.Patch(color='lightblue', alpha=0.5, label='Regular Cell'),
        mpatches.Patch(color='green', alpha=0.7, label='Hotspot (Getis-Ord)')
    ], loc='upper left', bbox_to_anchor=(1.05, 1), fontsize='small', frameon=False)

def plot_overlap(ax, grid):
    cells = grid.cells
    hotspots_getis_ord = grid.hotspots_getis_ord
    hotspots_90th = grid.hotspots_90th

    # Plot overlap
    for x in range(grid.m):
        for y in range(grid.n):
            for t in range(grid.k):
                cell = cells[x][y][t]
                if cell.count == 0:
                    color = 'grey'
                    alpha = 0
                else:
                    color = 'lightblue'
                    alpha = 0.1
                    if (x, y, t, cell.count) in hotspots_90th and (x, y, t, cell.getis_ord) in hotspots_getis_ord:
                        color = 'orange'
                        alpha = 0.7
                    elif (x, y, t, cell.count) in hotspots_90th:
                        color = 'red'
                        alpha = 0.7
                    elif (x, y, t, cell.getis_ord) in hotspots_getis_ord:
                        color = 'green'
                        alpha = 0.7

                ax.bar3d(cell.min_x, cell.min_y, cell.min_t, 
                         cell.max_x - cell.min_x, 
                         cell.max_y - cell.min_y, 
                         cell.max_t - cell.min_t, 
                         color=color, alpha=alpha)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('T')
    ax.set_title('Hot Spots Overlap')
    ax.legend(handles=[
        mpatches.Patch(color='grey', alpha=0.05, label='Empty Cell'),
        mpatches.Patch(color='lightblue', alpha=0.5, label='Regular Cell'),
        mpatches.Patch(color='orange', alpha=0.7, label='Hotspot (90th & Getis-Ord)'),
        mpatches.Patch(color='red', alpha=0.7, label='Hotspot (90th Percentile)'),
        mpatches.Patch(color='green', alpha=0.7, label='Hotspot (Getis-Ord)')
    ], loc='upper left', bbox_to_anchor=(1.05, 1), fontsize='small', frameon=False)

def plot_all_hotspots(grid, min_x, max_x, min_y, max_y, min_t, max_t):
    fig = plt.figure(figsize=(18, 12))
    
    # Create 3D subplot grid
    ax1 = fig.add_subplot(221, projection='3d')  # First plot
    ax2 = fig.add_subplot(222, projection='3d')  # Second plot
    ax3 = fig.add_subplot(212, projection='3d')  # Third plot (spans both columns)
    
    # Plot each subplot
    plot_90th_hotspots(ax1, grid)
    plot_getis_ord_hotspots(ax2, grid)
    plot_overlap(ax3, grid)
    
    plt.tight_layout()
    plt.show()
