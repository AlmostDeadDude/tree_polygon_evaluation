import os

# Get a list of all the files in the folder
folder_path = "user_info"
files = os.listdir(folder_path)

# Loop over the files and apply the script to each file
for filename in files:
    file_path = os.path.join(folder_path, filename)

    # Open the input file
    with open(file_path, "r") as f:
        data = f.read()

    # Replace all occurrences of '}{'
    data = data.replace("},{", ",")

    # Write the modified data to the output file (overwrite the input file)
    with open(file_path, "w") as f:
        f.write(data)
