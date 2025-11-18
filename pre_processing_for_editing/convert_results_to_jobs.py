import os
import json


def transform_data(input_data):
    transformed_data = []
    for item in input_data:
        transformed_item = {
            "ID": item.split("_")[1].split("-")[0],
            "filename": item.split("_")[1].split("-")[1],
            "number": 1,  # irrelevant constant
            "number_points": len(input_data[item]),
            "points": [{"number": i, "x": point["x"], "y": point["y"]} for i, point in enumerate(input_data[item])],
            "max_x": max(point["x"] for point in input_data[item]),
            "min_x": min(point["x"] for point in input_data[item]),
            "max_y": max(point["y"] for point in input_data[item]),
            "min_y": min(point["y"] for point in input_data[item])
        }
        transformed_data.append(transformed_item)
    return transformed_data


def process_files(input_folder, output_folder):
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

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_filepath = os.path.join(input_folder, filename)
            with open(input_filepath, "r") as file:
                data = json.load(file)
                transformed_data = transform_data(data)

                # Extracting job number from the input filename
                job_number = filename.split("_")[1]
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
                        f"File '{filename}' transformed and saved as '{output_filename}'.")


# Example usage:
input_folder = "./data/dataset_erlig1_125/results_first_20_lines_1_iteration"
output_folder = "./pre_processing_for_editing/output_convert_results_to_jobs"
process_files(input_folder, output_folder)
