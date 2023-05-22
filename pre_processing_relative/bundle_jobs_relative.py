import os
import json
import random
import numpy as np
import matplotlib.pyplot as plt


def process_txt_file_relative_jobs(filename, population, n_tasks, bundle_size, iterations):
    """
    Process the txt file and create job bundles with unique IDs for the relative evaluation campaigns.

    Args:
        filename (str): The name of the original txt file.
        population (int): The number of polygons to select from original file.
        n_tasks (int): The number of tasks (=task bundles) in a single job. Ususally 5.
        bundle_size (int): The size of each task bundle. Usually 3.
        iterations (int): The number of iterations of random polygon draws.
    """

    # Create output folder and subfolder with the original data dependent name
    output_folder_name = os.path.splitext(os.path.basename(filename))[0]
    output_folder_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'output', output_folder_name)
    os.makedirs(output_folder_path, exist_ok=True)

    # variable to store the indexed data
    indexed_data = []
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
                        indexed_data.append(indexed_json_data)
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
    # From the initial file we take a set of N (=population) polygons (e.g. N=25) as our population, i.e. the data sets to be processed. From this we randomly draw n_tasks*bundle_size polygons, which are then evaluated in a campaign by a user. We do this K (=iterations) times, so that we end up with K*n_tasks*bundle_size polygons. We just have to make sure that each of the N polygons was captured about the same number of times to remain meaningful.

    # Create a list of polygon IDs that will be used as the population
    # in the future might want to select random ids or get some specific ones, rather than just the N first ones, but will do for now
    population_ids = list(range(1, population+1))
    print('Population IDs:', population_ids)

    # each job file will have n_tasks*bundle_size polygons (usually 5*3=15)
    polygons_in_file = n_tasks*bundle_size

    # for eachg iteration we will randomly draw polygons_in_file polygons from the population
    final_amount_of_files = polygons_in_file*iterations
    print('Final amount of job files with used parameters:', final_amount_of_files)

    # variable for indexing job files
    job_id = 1
    # variable for storing the polygons before writing in a job file
    job_bundle = []

    # variable to store all selection IDs for analyzing the distribution later
    selection_ids = []

    for i in range(iterations):
        # draw bundle_size random polygons n_tasks times from the population
        # so we draw 3 polygons from the population 5 times and then add them to single list
        random_polygon_ids = []
        for j in range(n_tasks):
            random_polygon_ids.extend(
                random.sample(population_ids, bundle_size))
        print('Random polygon IDs:', random_polygon_ids)

        # find the polygons with the drawn IDs in the indexed data in the same order as they are in the random_polygon_ids list and add them to the job_bundle list
        for polygon_id in random_polygon_ids:
            for polygon in indexed_data:
                if polygon[0]['ID'] == str(polygon_id):
                    job_bundle.append(polygon)
                    selection_ids.append(polygon_id)
                    break
            # if the job_bundle has enough polygons in it, save it to the job file and empty the list
            if len(job_bundle) == polygons_in_file:
                # Write job bundle to separate txt file
                job_filename = os.path.join(
                    output_folder_path, 'job_{}.txt'.format(job_id))
                with open(job_filename, 'w') as job_file:
                    job_file.writelines('\n'.join(str(item)
                                                  for item in job_bundle))
                job_id += 1
                job_bundle = []

    # if the job_bundle has polygons in it, print the message
    if len(job_bundle) > 0:
        print('Job bundle with {} polygons was not saved to a job file, because it is not full.'.format(
            len(job_bundle)))

    # if the job_bundle is empty, print the message
    if len(job_bundle) == 0:
        print('{} Job bundles created in: {}'.format(
            job_id-1, output_folder_path))

    # analyze the distribution of the selected polygons for now by simply computing their histogram
    # Count occurrences of each item in the dataset
    item_counts = np.bincount(selection_ids)

    # Plotting the histogram
    plt.bar(population_ids, item_counts[1:])
    plt.xlabel('Polygon ID')
    plt.ylabel('Frequency')
    plt.title('Polygon occurrences in the created dataset')
    plt.show()


# Example usage
process_txt_file_relative_jobs('data/70_155.txt', 25, 5, 3, 50)
