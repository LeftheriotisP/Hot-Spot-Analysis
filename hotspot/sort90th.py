def sort_90th_file(input_filename, output_filename, limit=200):
    
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    #Extract the 90th percentile value and the hotspot lines
    percentile_line = lines[0]  
    hotspot_lines = lines[1:]   

    hotspots = []
    for line in hotspot_lines:
        parts = line.strip().split(' = ')
        coordinates = eval(parts[0])  
        count = int(parts[1])  
        hotspots.append((coordinates, count))

    sorted_hotspots = sorted(hotspots, key=lambda x: x[1], reverse=True)
    
    #limit to top-k hotspots
    limited_hotspots = sorted_hotspots[:limit]
    
    
    with open(output_filename, 'w') as file:
        file.write(percentile_line)  # Write the 90th percentile value
        for hotspot in limited_hotspots:
            file.write(f'{hotspot[0]} = {hotspot[1]}\n')

    print(f"File '{output_filename}' created with sorted hotspots.")
