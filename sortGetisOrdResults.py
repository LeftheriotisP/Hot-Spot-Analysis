def sort_getis_ord_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
    
    # Extract data and convert Getis-Ord values to floats
    data = []
    for line in lines:
        if '=' in line:
            coordinate, value = line.split('=')
            value = float(value.strip())
            data.append((coordinate.strip(), value))
    
    # Sort data by Getis-Ord values in descending order
    sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
    
    # Write sorted data to a new file with commas instead of dots
    with open(output_file_path, 'w') as file:
        for coordinate, value in sorted_data:
            # Convert value to string and replace dot with comma
            value_str = f"{value:.6f}".replace('.', ',')  # Adjust precision as needed
            file.write(f"{coordinate} = {value_str}\n")
    
    print(f"Sorted data written to {output_file_path}")

# Paths to the input and output files
input_file_path = 'getis_ord_results.txt'
output_file_path = 'sorted_getis_ord_results.txt'

# Sort the file
sort_getis_ord_file(input_file_path, output_file_path)


def sort_90th_percentile_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
    
    # Extract data and convert percentile values to integers
    data = []
    for line in lines:
        if '=' in line:
            coordinate, value = line.split('=')
            value = int(value.strip())  # Assuming values are integers
            data.append((coordinate.strip(), value))
    
    # Sort data by percentile values in descending order
    sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
    
    # Write sorted data to a new file
    with open(output_file_path, 'w') as file:
        for coordinate, value in sorted_data:
            file.write(f"{coordinate} = {value}\n")
    
    print(f"Sorted data written to {output_file_path}")

# Paths to the input and output files
input_file_path = '90th_percentile_results.txt'
output_file_path = 'sorted_90th_percentile_results.txt'

# Sort the file
sort_90th_percentile_file(input_file_path, output_file_path)
