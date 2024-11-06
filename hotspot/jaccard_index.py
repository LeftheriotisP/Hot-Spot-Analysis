def clean_coordinate_format(coordinate):
    return coordinate.replace(" ", "")

def read_coordinates_from_file(filename, start_line):
    coordinates = set()
    with open(filename, 'r') as file:
        lines = file.readlines()[start_line:]  #skip header lines
        for line in lines:
            if "=" in line:
                parts = line.split("=")
                coordinate = clean_coordinate_format(parts[0].strip())
                coordinates.add(coordinate)
    return coordinates

def calculate_j(set_a, set_b):
    intersection = set_a.intersection(set_b)
    union = set_a.union(set_b)
    jaccard_index = len(intersection) / len(union) if union else 0
    return jaccard_index, intersection, union

def save_jaccard_results_to_file(filename, jaccard_index, intersection, union):
    with open(filename, 'w', encoding='utf-8') as file:  
        file.write(f"Jaccard Index: {jaccard_index:.4f}\n")
        file.write(f"Number of common cells (A ∩ B): {len(intersection)}\n")
        file.write(f"Number of cells in union (A ∪ B): {len(union)}\n")
        file.write("\nCommon cells:\n")
        for cell in intersection:
            file.write(f"{cell}\n")


def calculate_jaccard_index():
    #read coordinates from both files
    set_90th = read_coordinates_from_file('sorted_90th_percentile_results.txt', start_line=1)
    set_getis_ord = read_coordinates_from_file('sorted_getis_ord_results.txt', start_line=3)
    
    #calculate Jaccard index, intersection, and union
    jaccard_index, intersection, union = calculate_j(set_90th, set_getis_ord)
    
    #save results to a file
    save_jaccard_results_to_file("jaccard_results.txt", jaccard_index, intersection, union)
    
    print(f"Jaccard Index: {jaccard_index:.4f}")
    print(f"Number of common cells: {len(intersection)}")
    print(f"Number of cells in union: {len(union)}")

