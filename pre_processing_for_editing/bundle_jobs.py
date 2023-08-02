import os
import json


def process_txt_file(filenames, indices, sample_size):
    """
    Process the txt files and create job bundles with unique IDs.
    It takes multiple source files and selects polygons with the given indices.
    The output is a set (size = sample_size) of jobs each one of them containing one polygon from each source file.

    Args:
        filenames (array of strings): The names of the original txt files.
        indices (array of arrays of ints): The indices of the polygons to select from each file.
        sample_size (int): The amount of jobs to create - actually the length of indices subarrays.
    """

    # Create output folder and subfolder with the original data dependent name
    output_folder_names = []
    for filename in filenames:
        output_folder_names.append(
            os.path.splitext(os.path.basename(filename))[0])

    output_folder_name = '-'.join(output_folder_names)

    output_folder_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'output', output_folder_name)
    os.makedirs(output_folder_path, exist_ok=True)

    # Copy the original txt files to the output folder with indexed lines
    for filename in filenames:
        indexed_filename = os.path.join(
            output_folder_path, 'indexed_{}'.format(filename.split('/')[-1]))
        with open(filename, 'r') as file:
            with open(indexed_filename, 'w') as indexed_file:
                lines = file.readlines()
                i = 0  # Initialize counter
                for line in lines:
                    # Skip empty lines
                    if not line.strip():
                        continue
                    # Check if line contains only a single number
                    if line.strip().isdigit():
                        continue
                    try:
                        json_data = json.loads(line)
                        if isinstance(json_data, list) and len(json_data) > 0 and isinstance(json_data[0], dict) and 'number' in json_data[0] and 'number_points' in json_data[0] and 'points' in json_data[0]:
                            # Calculate max and min values for x and y in points
                            points = json_data[0]['points']
                            x_values = [point['x'] for point in points]
                            y_values = [point['y'] for point in points]
                            max_x = max(x_values)
                            min_x = min(x_values)
                            max_y = max(y_values)
                            min_y = min(y_values)

                            # Add ID, filename, max, and min fields to top-level JSON object
                            indexed_json_data = [{'ID': str(i+1), 'filename': filename.split('/')[-1].split('_')[0], 'number': json_data[0]['number'], 'number_points': json_data[0]['number_points'],
                                                  'points': json_data[0]['points'], 'max_x': max_x, 'min_x': min_x, 'max_y': max_y, 'min_y': min_y}]
                            indexed_file.write(json.dumps(
                                indexed_json_data) + '\n')
                            i += 1  # Increment counter
                        else:
                            # Skip lines with invalid JSON data
                            continue
                    except json.JSONDecodeError:
                        # Skip lines with invalid JSON data
                        continue

    # Create jobs by selecting polygons from each file and putting them together in one job
    job_id = 1
    job_bundle = []
    for i in range(sample_size):
        for j in range(len(filenames)):
            indexed_filename = os.path.join(
                output_folder_path, 'indexed_{}'.format(filenames[j].split('/')[-1]))
            with open(indexed_filename, 'r') as indexed_file:
                for line in indexed_file:
                    json_data = json.loads(line)
                    if json_data[0]['ID'] == str(indices[j][i]):
                        job_bundle.append(line)
                        break
        # Write job bundle to file
        job_bundle_filename = os.path.join(
            output_folder_path, 'job_{}.txt'.format(job_id))
        with open(job_bundle_filename, 'w') as job_bundle_file:
            job_bundle_file.writelines(job_bundle)
        # Increment job ID
        job_id += 1
        # Reset job bundle
        job_bundle = []

    print('Job bundles created in:', output_folder_path)


# Example usage
process_txt_file(['data/70_155.txt', 'data/71_155.txt', 'data/72_155.txt'], [[121, 102, 16, 75, 17, 14, 61,
                                                                              151, 41, 45], [53, 113, 19, 10, 13, 101, 11, 44, 111, 140], [47, 82, 70, 22, 83, 147, 13, 95, 80, 44]], 10)
