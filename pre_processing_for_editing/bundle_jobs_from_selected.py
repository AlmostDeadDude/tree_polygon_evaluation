import os
import json


def process_txt_file(folder, first_X_from_file, tasks_per_job):
    """
    Process the txt files and create job bundles with unique IDs.
    It takes multiple source files and selects first X polygons from them.
    The output is a set (size = total_size/tasks_per_job) of jobs each
    one of them containing polygons from different source files.

    Args:
        folder (string): Path to the folder with txt files to select from.
        first_X_from_file (int): The number of first polygons to select from each file.
        tasks_per_job (int): The amount of tasks in a single job.
    """

    # Create output folder and subfolder with the original data dependent name
    folder = os.path.normpath(folder)
    parent_dir, folder_name = os.path.split(folder)
    _, parent_folder_name = os.path.split(parent_dir)
    output_folder_name = 'output_' + parent_folder_name
    print(os.path.dirname(os.path.abspath(__file__)))

    output_folder_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'output', output_folder_name)
    os.makedirs(output_folder_path, exist_ok=True)

    # get all the .txt files in the folder
    filenames = []
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            filenames.append(os.path.join(folder, file))

    # Copy the original txt files to the output folder with indexed lines, make ID counter global
    # Skip first x valid lines in each file but increase the ID counter
    skip_first_valid_lines = 0
    i = 0  # Initialize counter for IDs, here we skip x lines in each of 125 files because we had them already in the previous run, if you start fresh just set both to 0
    global_object = []
    for filename in filenames:
        indexed_filename = os.path.join(
            output_folder_path, 'indexed_{}'.format(filename.split('\\')[-1]))
        with open(filename, 'r') as file:
            with open(indexed_filename, 'w') as indexed_file:
                lines = file.readlines()
                j = 0
                k = 0
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
                            # Skip first x valid lines in each file
                            if k < skip_first_valid_lines:
                                k += 1
                                continue
                            # Calculate max and min values for x and y in points
                            points = json_data[0]['points']
                            x_values = [point['x'] for point in points]
                            y_values = [point['y'] for point in points]
                            max_x = max(x_values)
                            min_x = min(x_values)
                            max_y = max(y_values)
                            min_y = min(y_values)

                            # Add ID, filename, max, and min fields to top-level JSON object
                            indexed_json_data = [{'ID': str(i+1), 'filename': filename.split('\\')[-1].split('_')[0], 'number': json_data[0]['number'], 'number_points': json_data[0]['number_points'],
                                                  'points': json_data[0]['points'], 'max_x': max_x, 'min_x': min_x, 'max_y': max_y, 'min_y': min_y}]
                            global_object.append(indexed_json_data)
                            indexed_file.write(json.dumps(
                                indexed_json_data) + '\n')
                            i += 1  # Increment counters
                            j += 1
                            if j == first_X_from_file:
                                break
                        else:
                            # Skip lines with invalid JSON data
                            continue
                    except json.JSONDecodeError:
                        # Skip lines with invalid JSON data
                        continue

    # Create jobs by selecting polygons from tasks_per_job different files and putting them together in one job
    # we go in steps of tasks_per_job through the global_object items using their IDs
    job_id = 1
    # job_id = 251  # Initialize job ID counter, here we start with n+1 because we had n files already in the previous run, if you start fresh just set it to 1 as in the line above
    indices = []  # Store arrays of indices
    # first create the indices array where we take the range from 0 to the number of items in global_object and divide it in chunks of size len(global_object)/tasks_per_job
    indices = list(range(len(global_object)))
    chunk_size = len(global_object) / tasks_per_job
    indices_chunks = [indices[i:i + int(chunk_size)]
                      for i in range(0, len(indices), int(chunk_size))]
    # now we iterate through the chunks and create the job bundles with 1 item from each chunk
    for i in range(int(chunk_size)):
        job_bundle = []
        for j in range(tasks_per_job):
            # add the entry from the global_object to the job_bundle
            job_bundle.append(global_object[indices_chunks[j][i]])
        # Write job bundle to file
        job_bundle_filename = os.path.join(
            output_folder_path, 'job_{}.txt'.format(job_id))
        with open(job_bundle_filename, 'w') as job_bundle_file:
            job_bundle_file.writelines(json.dumps(job_bundle))
        # Increment job ID
        job_id += 1

    print('Job bundles created in:', output_folder_path)


# process_txt_file('./data/dataset_erlig1_125/txt', 10, 5)
process_txt_file('./data/ottmarsheim/acquisitions', 30, 5)
