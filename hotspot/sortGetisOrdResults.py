def sort_getis_ord_file(input_filename, output_filename, limit=200):
    # Read the file
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    # Extract the header lines (first three lines)
    header_lines = lines[:3]
    getis_ord_lines = lines[3:]  # The rest are the Getis-Ord entries

    # Parse the Getis-Ord lines into tuples (coordinates, value)
    getis_ord_stats = []
    for line in getis_ord_lines:
        if '=' in line:  # Ensure that this is a valid Getis-Ord line
            parts = line.strip().split(' = ')
            coordinates = parts[0].strip()  # Keep the coordinates as a string
            value = float(parts[1])  # Convert the Getis-Ord value to a float
            getis_ord_stats.append((coordinates, value))

    # Sort Getis-Ord statistics by value in descending order
    sorted_getis_ord_stats = sorted(getis_ord_stats, key=lambda x: x[1], reverse=True)

    #limit results to top-k hotspots
    limited_getis_ord_stats = sorted_getis_ord_stats[:limit]

    # Write the sorted result to the output file
    with open(output_filename, 'w') as file:
        file.writelines(header_lines)  # Write the header lines
        for stat in limited_getis_ord_stats:
            file.write(f'{stat[0]} = {stat[1]}\n')

    print(f"File '{output_filename}' created with sorted Getis-Ord statistics.")