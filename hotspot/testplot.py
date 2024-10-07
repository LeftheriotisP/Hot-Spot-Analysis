from datetime import datetime, timezone
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs  # cartopy
import cartopy.feature as cfeature

def plot_background_map(ax, grid):
    # Set up Mercator projection and add map features
    ax.set_extent([grid.min_x, grid.max_x, grid.min_y, grid.max_y], crs=ccrs.PlateCarree())
    ax.coastlines(resolution='10m')
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Add gridlines and labels
    gl = ax.gridlines(draw_labels=True, crs=ccrs.PlateCarree(),
                      color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {'size': 12, 'color': 'black'}
    gl.ylabel_style = {'size': 12, 'color': 'black'}

# Function to convert Unix epoch to timezone-aware UTC time
def convert_unix_to_utc(epoch):
    return datetime.fromtimestamp(epoch, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

# Plot 90th percentile hotspots for a specific t-value
def plot_90th_hotspots_at_t(grid, t_value):
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    
    plot_background_map(ax, grid)  # Add map background

    cells = grid.cells
    hotspots_90th = grid.hotspots_90th

    # Find min and max t of the cells with specific t_value
    min_t = cells[0][0][t_value].min_t
    max_t = cells[0][0][t_value].max_t

    # Collect data for t_value and update min/max t range
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
                color = 'grey'  # Empty cells
            elif (x, y, t_value, cell.count) in hotspots_90th:
                color = 'red'  # 90th percentile hotspots
            else:
                color = 'lightblue'  # Normal cells

            # Create rectangle for cells with explicit borders
            ax.add_patch(mpatches.Rectangle(
                (min_x, min_y), width, height, transform=ccrs.PlateCarree(), 
                edgecolor='black', linewidth=0.5, facecolor=color, alpha=0.7))
    #Test print
    #print(f"Minimum T: {min_t}, Maximum T: {max_t}")
    
    # Convert min_t and max_t to UTC time strings
    min_t_str = convert_unix_to_utc(min_t)
    max_t_str = convert_unix_to_utc(max_t)

    # Set title with the converted t range
    ax.set_title(f'Hotspots at t = {t_value} , (t range: {min_t_str} - {max_t_str} UTC)')
    plt.show()

# Plot Getis-Ord hotspots for a specific t-value
def plot_getis_ord_hotspots_at_t(grid, t_value):
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    
    plot_background_map(ax, grid)  # Add map background

    cells = grid.cells
    hotspots_getis_ord = grid.hotspots_getis_ord

    # Find min and max t of the cells with specific t_value
    min_t = cells[0][0][t_value].min_t
    max_t = cells[0][0][t_value].max_t

    # Collect data for t_value and update min/max t range
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
                color = 'grey'  # Empty cells
            elif (x, y, t_value, cell.getis_ord) in hotspots_getis_ord:
                color = 'green'  # Getis-Ord hotspots
            else:
                color = 'lightblue'  # Normal cells

            # Create rectangle for cells with explicit borders
            ax.add_patch(mpatches.Rectangle(
                (min_x, min_y), width, height, transform=ccrs.PlateCarree(), 
                edgecolor='black', linewidth=0.5, facecolor=color, alpha=0.7))

    # Convert min_t and max_t to UTC time strings
    min_t_str = convert_unix_to_utc(min_t)
    max_t_str = convert_unix_to_utc(max_t)

    # Set title with the converted t range
    ax.set_title(f'Hotspots at t = {t_value} , (t range: {min_t_str} - {max_t_str} UTC)')
    plt.show()

# Plot overlap of hotspots for a specific t-value
def plot_overlap_at_t(grid, t_value):
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    
    plot_background_map(ax, grid) 

    cells = grid.cells
    hotspots_getis_ord = grid.hotspots_getis_ord
    hotspots_90th = grid.hotspots_90th

    # Find min and max t of the cells with specific t_value
    min_t = cells[0][0][t_value].min_t
    max_t = cells[0][0][t_value].max_t

    # Collect data for t_value and update min/max t range
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
                color = 'grey'  # Empty cells
            elif (x, y, t_value, cell.count) in hotspots_90th and (x, y, t_value, cell.getis_ord) in hotspots_getis_ord:
                color = 'orange'  # Overlapping hotspots
            elif (x, y, t_value, cell.count) in hotspots_90th:
                color = 'red'  # 90th percentile hotspots
            elif (x, y, t_value, cell.getis_ord) in hotspots_getis_ord:
                color = 'green'  # Getis-Ord hotspots
            else:
                color = 'lightblue'  # Normal cells

            # Create rectangle for cells with explicit borders
            ax.add_patch(mpatches.Rectangle(
                (min_x, min_y), width, height, transform=ccrs.PlateCarree(), 
                edgecolor='black', linewidth=0.5, facecolor=color, alpha=0.7))

    # Convert min_t and max_t to UTC time strings
    min_t_str = convert_unix_to_utc(min_t)
    max_t_str = convert_unix_to_utc(max_t)

    # Set title with the converted t range
    ax.set_title(f'Hotspots at t = {t_value} , (t range: {min_t_str} - {max_t_str} UTC)')
    plt.show()


#plot all hotspot types at a specific t-value
def plot_all_hotspots_at_t(grid):
    while True:
        #ask if the user wants to see a plot
        plot_choice = input("Do you want to see a plot? (Y/N): ").strip().upper()
        
        if plot_choice == 'Y':
            # If yes plot
            while True:
                try:
                    t_value = int(input(f"Enter the value of t (0 to {grid.v - 1}): "))
                    if t_value < 0 or t_value >= grid.v:
                        print(f"'t' must be between 0 and {grid.v - 1}, please enter a valid value.")
                    else:
                        break
                except ValueError:
                    print("Invalid input, please enter a valid value for t.")
                    
            plot_90th_hotspots_at_t(grid, t_value)       #plot 90th percentile hotspots
            plot_getis_ord_hotspots_at_t(grid, t_value)  #plot Getis-Ord hotspots
            plot_overlap_at_t(grid, t_value)             #plot overlap
        elif plot_choice == 'N':
            # If no exit
            print("Exiting the plot viewer.")
            break
        else:
            print("Invalid input, please enter 'Y' or 'N'.")
