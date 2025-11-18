import os
import json

#one polygon per input file, only the polygon points are given, one point pair in format: x,y per line
#the file name is also the name of the corresponding picture so we also use it as ID
def transform_data(input_data):
    transformed_data = []
    for item in input_data:
        transformed_item = {
            "ID": item.split(".")[0],
            "filename": item.split(".")[0],
            "number": 1,  # irrelevant constant, was in legacy format
            "number_points": len(input_data[item]),
            "points": [{"number": i, "x": point["x"], "y": point["y"]} for i, point in enumerate(input_data[item])],
            "max_x": max(point["x"] for point in input_data[item]),
            "min_x": min(point["x"] for point in input_data[item]),
            "max_y": max(point["y"] for point in input_data[item]),
            "min_y": min(point["y"] for point in input_data[item])
        }
        transformed_data.append(transformed_item)
    return transformed_data


def process_files(input_folder, output_folder, files_per_job):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else:
        # clear the folder
        for filename in os.listdir(output_folder):
            file_path = os.path.join(output_folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

    #we pack files_per_job filex into one job
    job_number = 0
    data = {}
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_filepath = os.path.join(input_folder, filename)
            with open(input_filepath, "r") as file:
                #if the filename has something after the number and the underscore, we use the number only for the ID
                if len(filename.split("_")) > 1:
                    filename = filename.split("_")[0]
                #read line by line and split by comma to get x and y
                data[filename] = []
                for line in file:
                    data[filename].append({"x": int(line.split(",")[0]), "y": int(line.split(",")[1])})
                if len(data) == files_per_job:
                    transformed_data = transform_data(data)

                    # Extracting job number from the input filename
                    job_number += 1
                    output_filename = f"job_{job_number}.txt"
                    output_filepath = os.path.join(output_folder, output_filename)

                    with open(output_filepath, "w") as output_file:
                        output_file.write("[")
                        # Serialize the transformed data to JSON without new lines or indentation
                        json_data = json.dumps(
                            transformed_data, separators=(',', ':'))
                        # Manually add square brackets for each polygon without new lines or indentation
                        for i, polygon_data in enumerate(json.loads(json_data)):
                            if i > 0:
                                # Add comma between polygons
                                output_file.write(",")
                            output_file.write("[")
                            output_file.write(json.dumps(polygon_data))
                            output_file.write("]")
                        output_file.write("]")
                        print(
                            f"Files from '{list(data.keys())[0]}' to '{list(data.keys())[-1]}' were processed into job '{output_filename}'")
                    data = {}
    #if there are still files left, we optput a warning
    if len(data) > 0:
        print(f"WARNING: There are {len(data)} files left that were not processed because they did not fit into a job. Please check if this is intended.")


# Example usage:
input_folder = "./data/data_2023_11_29_NOTFORMATTED_reduced"
output_folder = "./pre_processing_for_editing/output_convert_notformatted_to_jobs"
files_per_job = 5
process_files(input_folder, output_folder, files_per_job)
