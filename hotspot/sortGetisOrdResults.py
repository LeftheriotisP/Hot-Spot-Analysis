def sort_getis_ord_file(input_filename, output_filename, limit=200):
    
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    
    header_lines = lines[:3]
    getis_ord_lines = lines[3:] 

    
    getis_ord_stats = []
    for line in getis_ord_lines:
        if '=' in line:  
            parts = line.strip().split(' = ')
            coordinates = parts[0].strip()  
            value = float(parts[1])  
            getis_ord_stats.append((coordinates, value))

    #sort Getis-Ord statistics by value in descending order
    sorted_getis_ord_stats = sorted(getis_ord_stats, key=lambda x: x[1], reverse=True)

    #limit results to top-k hotspots
    limited_getis_ord_stats = sorted_getis_ord_stats[:limit]

    
    with open(output_filename, 'w') as file:
        file.writelines(header_lines) 
        for stat in limited_getis_ord_stats:
            file.write(f'{stat[0]} = {stat[1]}\n')

    print(f"File '{output_filename}' created with sorted Getis-Ord statistics.")