def sort_90th_file(input_filename, output_filename, limit=200):
    # Read the file
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    # Extract the 90th percentile value and the hotspot lines
    percentile_line = lines[0]  # The first line contains the 90th percentile value
    hotspot_lines = lines[1:]   # The rest are the hotspot entries

    # Parse the hotspot lines into tuples (x, y, t, count)
    hotspots = []
    for line in hotspot_lines:
        parts = line.strip().split(' = ')
        coordinates = eval(parts[0])  # Convert '(x, y, t)' string to a tuple
        count = int(parts[1])  # Convert the count value to an integer
        hotspots.append((coordinates, count))

    # Sort hotspots by count in descending order
    sorted_hotspots = sorted(hotspots, key=lambda x: x[1], reverse=True)
    
    #limit to top-k hotspots
    limited_hotspots = sorted_hotspots[:limit]
    
    # Write the sorted result to the output file
    with open(output_filename, 'w') as file:
        file.write(percentile_line)  # Write the 90th percentile value
        for hotspot in limited_hotspots:
            file.write(f'{hotspot[0]} = {hotspot[1]}\n')

    print(f"File '{output_filename}' created with sorted hotspots.")
