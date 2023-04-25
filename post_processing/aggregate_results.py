import os
import json


def aggregate_results(results_, user_info_):
    results = {}

    results_dir = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), results_)
    user_info_dir = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), user_info_)

    # Loop over all files in the results directory
    for subdir, _, files in os.walk(results_dir):
        for filename in files:
            filepath = os.path.join(subdir, filename)

            # if file is empty - skip it
            if os.stat(filepath).st_size == 0:
                continue

            # Load the JSON data from the file
            with open(filepath, 'r') as f:
                data = json.load(f)

            # Skip files that don't have task data
            if not any(key.startswith('task_') for key in data.keys()):
                continue

            # Extract the job and iteration numbers from the filename
            job_iteration = os.path.splitext(filename)[0].split('_')[1:]

            # Load the JSON data from the corresponding user_info file
            user_info_filepath = os.path.join(
                user_info_dir, f"{'_'.join(['job'] + job_iteration)}.txt")
            with open(user_info_filepath, 'r') as f:
                user_info_data = json.load(f)

            # Extract the file and image fields from the user_info data
            image = user_info_data.get('image')

            # get the tasks
            task_names = [k for k in data.keys() if k.startswith('task_')]

            # iterate over task names
            for task_name in task_names:
                task_score = data.get(task_name)
                if image not in results:
                    results[image] = {}
                if task_name not in results[image]:
                    results[image][task_name] = {
                        'scores': [], 'average': None}

                results[image][task_name]['scores'].append(
                    int(task_score))

    # compute average scores for each task and assign to results dictionary
        for image_name, task_data in results.items():
            for task_name, task_scores in task_data.items():
                scores = task_scores['scores']
                task_scores['average'] = sum(scores) / len(scores)

    return results


# example usage:
results = aggregate_results('results', 'user_info')

# save to txt file
with open(os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'final_results.txt'), 'w') as f:
    json.dump(results, f)
