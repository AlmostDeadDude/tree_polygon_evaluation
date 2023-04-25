#PREPROCESSING
bundle_jobs.py uses the provided one big .txt file from data folder and creates the jobs in desired format in the output subfolder

those can be used in jobs subfolder in the web part

#WEB PART
the user starts the task on microworkers (note that internal timer is 20 min, so the microworkers timer should be <= 20 min)

the task description contains the link as follows:Go to ...task_folder/about.php?firstTime=true&campaign={{CAMP_ID}}&worker={{MW_ID}}&rand_key={{RAND_KEY}}

then user gets to the about page with the firstTime = true, so after the instructions he sees the button, which starts the task

while in the task, user can open the about page in a new tab, but there will be no button to start the task anymore

after user gets to the index.php the job assignment algorithm provides him the job and iteration number to start the task

then user does the actual task and finally is able to submit it

the submission is handled by the saveResults.php, that writes the results to files in results and user_info folders, using job and iteration number in the file name

if submission was successful, the user is then redirected to the results.php?vcode=... page, where he can see and copy the vcode 

#POSTPROCESSING
for the postprocessing the results are read from the results folder and the user_info folder, which can be copied from web folder into post precessing folder

then the final_results.txt file is created by aggregate_results.py script. This file contains the results in the json format. The file contains the scores of each iteration for each task and the average score for each task.

this file can be used for further analysis or visualisation

#RESULTS VISUALISATION
the visualisation/visu.php uses jobs from web/jobs and image from web/pics and the final_results.txt file from post-processing dir to create the visualisation of the results

it is showing the selection and their average scores, it is sorted from low to high and can be filtered by the score. The total and shown amounts are also displayed.