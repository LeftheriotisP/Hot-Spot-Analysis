import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Plot 90th percentile hotspots for a specific t-value
def plot_90th_hotspots_at_t(grid, t_value):
    fig, ax = plt.subplots(figsize=(8, 8))
    
    cells = grid.cells
    hotspots_90th = grid.hotspots_90th

    #find min and max t of the cells with specific t_value
    min_t = cells[0][0][t_value].min_t
    max_t = cells[0][0][t_value].max_t

    image_path = 'README_nari_dynamic.png'
    img = plt.imread(image_path)
    ax.imshow(img, extent=(grid.min_x, grid.max_x, grid.min_y, grid.max_y), aspect='auto')

    # Collect data for t = t_value
    for x in range(grid.m):
        for y in range(grid.n):
            cell = cells[x][y][t_value]
            min_x, min_y = cell.min_x, cell.min_y
            width = cell.max_x - cell.min_x
            height = cell.max_y - cell.min_y

            if cell.min_t < min_t: 
                min_t = cell.min_t
            if cell.max_t > max_t:
                max_t = cell.max_t
                
            if cell.count == 0:
                color = 'grey'  # Empty cell
            elif (x, y, t_value, cell.count) in hotspots_90th:
                color = 'red'  # 90th percentile hotspot
            else:
                color = 'lightblue'  # Normal cell

            # Create a rectangle for each cell
            ax.add_patch(mpatches.Rectangle((min_x, min_y), width, height, color=color, alpha=0.7))

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(f'Hotspots at t = {t_value} , (t range: {min_t}-{max_t})')
    plt.xlim(grid.min_x, grid.max_x)  # Set x limits if needed
    plt.ylim(grid.min_y, grid.max_y)  # Set y limits if needed
    plt.show()

# Plot Getis-Ord hotspots for a specific t-value
def plot_getis_ord_hotspots_at_t(grid, t_value):
    fig, ax = plt.subplots(figsize=(8, 8))
    
    cells = grid.cells
    hotspots_getis_ord = grid.hotspots_getis_ord

    #find min and max t of the cells with specific t_value
    min_t = cells[0][0][t_value].min_t
    max_t = cells[0][0][t_value].max_t
    
    # Collect data for t = t_value
    for x in range(grid.m):
        for y in range(grid.n):
            cell = cells[x][y][t_value]
            min_x, min_y = cell.min_x, cell.min_y
            width = cell.max_x - cell.min_x
            height = cell.max_y - cell.min_y

            if cell.count == 0:
                color = 'grey'  # Empty cell
            elif (x, y, t_value, cell.getis_ord) in hotspots_getis_ord:
                color = 'green'  # Getis-Ord hotspot
            else:
                color = 'lightblue'  # Normal cell

            # Create a rectangle for each cell
            ax.add_patch(mpatches.Rectangle((min_x, min_y), width, height, color=color, alpha=0.7))

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(f'Hotspots at t = {t_value} , (t range: {min_t}-{max_t})')
    plt.xlim(grid.min_x, grid.max_x)
    plt.ylim(grid.min_y, grid.max_y)
    plt.show()

# Plot overlap of hotspots for a specific t-value
def plot_overlap_at_t(grid, t_value):
    fig, ax = plt.subplots(figsize=(8, 8))
    
    cells = grid.cells
    hotspots_getis_ord = grid.hotspots_getis_ord
    hotspots_90th = grid.hotspots_90th

    #find min and max t of the cells with specific t_value
    min_t = cells[0][0][t_value].min_t
    max_t = cells[0][0][t_value].max_t

    # Collect data for t = t_value
    for x in range(grid.m):
        for y in range(grid.n):
            cell = cells[x][y][t_value]
            min_x, min_y = cell.min_x, cell.min_y
            width = cell.max_x - cell.min_x
            height = cell.max_y - cell.min_y

            if cell.count == 0:
                color = 'grey'  # Empty cell
            elif (x, y, t_value, cell.count) in hotspots_90th and (x, y, t_value, cell.getis_ord) in hotspots_getis_ord:
                color = 'orange'  # Overlapping hotspots
            elif (x, y, t_value, cell.count) in hotspots_90th:
                color = 'red'  # 90th percentile hotspot
            elif (x, y, t_value, cell.getis_ord) in hotspots_getis_ord:
                color = 'green'  # Getis-Ord hotspot
            else:
                color = 'lightblue'  # Normal cell

            # Create a rectangle for each cell
            ax.add_patch(mpatches.Rectangle((min_x, min_y), width, height, color=color, alpha=0.7))

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title(f'Hotspots at t = {t_value} , (t range: {min_t}-{max_t})')
    plt.xlim(grid.min_x, grid.max_x)
    plt.ylim(grid.min_y, grid.max_y)
    plt.show()

# Function to plot all hotspot types at a specific t-value
def plot_all_hotspots_at_t(grid):
    while True:
        try:
            t_value = int(input("\nEnter the value of t: "))
            if t_value < 0:
                print("'t' must be positive or 0. Please enter a correct value.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a numeric value for t.")
    plot_90th_hotspots_at_t(grid, t_value)  # Plot 90th percentile hotspots
    plot_getis_ord_hotspots_at_t(grid, t_value)  # Plot Getis-Ord hotspots
    plot_overlap_at_t(grid, t_value)  # Plot overlap
