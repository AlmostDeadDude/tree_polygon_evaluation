import os
import json


def process_txt_file(filename, bundle_size):
    """
    Process the txt file and create job bundles with unique IDs.

    Args:
        filename (str): The name of the original txt file.
        bundle_size (int): The size of each job bundle.
    """

    # Create output folder and subfolder with the original data dependent name
    output_folder_name = os.path.splitext(os.path.basename(filename))[0]
    output_folder_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'output', output_folder_name)
    os.makedirs(output_folder_path, exist_ok=True)

    # Copy the original txt file to the output folder with indexed lines
    indexed_filename = os.path.join(
        output_folder_path, 'indexed_{}.txt'.format(output_folder_name))
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

                        # Add ID, max, and min fields to top-level JSON object
                        indexed_json_data = [{'ID': str(i+1), 'number': json_data[0]['number'], 'number_points': json_data[0]['number_points'],
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

    # Create job bundles with unique IDs
    job_id = 1
    job_bundle = []
    with open(indexed_filename, 'r') as indexed_file:
        for line in indexed_file:
            job_bundle.append(line)
            if len(job_bundle) == bundle_size:
                # Write job bundle to separate txt file
                job_filename = os.path.join(
                    output_folder_path, 'job_{}.txt'.format(job_id))
                with open(job_filename, 'w') as job_file:
                    job_file.writelines(job_bundle)
                job_id += 1
                job_bundle = []
        # Write the last job bundle to a separate txt file
        if len(job_bundle) > 0:
            job_filename = os.path.join(
                output_folder_path, 'job_{}.txt'.format(job_id))
            with open(job_filename, 'w') as job_file:
                job_file.writelines(job_bundle)

    print('Job bundles created in:', output_folder_path)


# Example usage
process_txt_file('data/70_155.txt', 5)
