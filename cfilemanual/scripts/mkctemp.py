import csv
import os
import time

def get_valid_num_input(prompt):
    """Checks to make sure that user puts in a valid numerical value (interger,
    greater than 0). If they do, it returns the inputted number. If not, continue
    to ask until a valid value is given.

    INPUT: prompt (str)
    OUTPUT: val (int)"""
    while True:
        print(prompt)
        try:
            val = int(input(">"))
            if val > 0:
                return val
            print("Please input an interger greater than 0.")
        except ValueError as e:
          print(e)
          print("Please input an interger greater than zero.")

def get_valid_dir_name(prompt):
    """Checks to make sure that user puts in valid textual value (not empty, no
    numbers). If they do, function returns the valid input. If not, continues to
    ask until a valid value is given.

    INPUT: prompt (str)
    OUTPUT: val (str)"""

    while True:
      if prompt == "Input a name for the directory you want to export to.":
          print(prompt)
          val = input(">")
          if not os.path.exists(f"{os.getcwd()}/{val}"):
              try:
                  os.mkdir(f"{os.getcwd()}/{val}")
                  return f"{os.getcwd()}/{val}"
              except:
                  print("That is not a valid directory name. Try again.")
          else:
              print(f"Directory already exists! Will export to: {val}")
              return f"{os.getcwd()}/{val}"

# The use of while loops throughout this program is to check to make sure
# that the user input a valid data type in the field.
while True:
    print("-" * 80)
    print("MIND LAB CONDITIONS FILE TEMPLATE CREATOR.")
    print("-" * 80)

    print("""In order to create properly format the files, please answer a
few questions about the experiment.""")

# Get number of participants run.
    prompt = "How many participants do you need to make conditions files for?: "
    participant_number = get_valid_num_input(prompt)

# Get number of sessions in experiment.
    prompt = "How many sessions were there in the experiment?: "
    total_sessions = get_valid_num_input(prompt)

# Get number of sensors used in experiment.
    prompt = "How many sensors were used on each participant?: "
    cond_per_participant = get_valid_num_input(prompt)

# Get valid sensor types used in experiment.
    while True:
# If you do not see your sensor in this list, add it and make a pull request.
# Please try to keep sensor names 4 chars or less.
        proper_sensors = ["FNIRS", "EDA", "ECG",
                          "EEG", "RESP", "GSR",
                          "EYET"]
        print("Please enter the sensor types separated by a space:")
        sensor_list = input(">")
        # Splits input into list of inputs, and checks them against current
        # valid inputs.
        sensor_list = sensor_list.split(" ")
        sensor_list = [s.upper() for s in sensor_list]
        not_proper = [s for s in sensor_list if s not in proper_sensors]
        if not not_proper and len(sensor_list) == cond_per_participant:
            break
        print("-" * 80)
        print("That is not proper input. Please try again.")
        print(f"Acceptable values: {proper_sensors}")
        print("-" * 80)

# Gets valid two digit experiment ID. Should eventually include checking current
# experiments in the dataset to make sure no conflicting filenames are created.
    while True:
        print("Please enter the experient ID number: ")
        experiment_id = input(">")
        if len(experiment_id) == 2 and experiment_id.isnumeric():
            break
        print("-" * 80)
        print("That is not proper input. Please try again.")
        print(f"Acceptable values must be a two digit interger.")
        print("-" * 80)

# Gets number of tasks per session.
    task_num_per_session = []
    for i, session in enumerate(range(0, total_sessions)):
        if total_sessions == 1:
            prompt = "How many tasks were in the experiment?"
        else:
            prompt = f"How many tasks were in session {i + 1}?: "
        task_num = get_valid_num_input(prompt)
        task_num_per_session.append(task_num)

# Based on user input, this is the total amount of files that need to be
# generated.
    total_files = participant_number * cond_per_participant * total_sessions

# Make directory "exports" if it doesn't already exist, and move into it.
    if not os.path.exists(f"{os.getcwd()}/exports/"):
        os.mkdir(f"{os.getcwd()}/exports/")
    os.chdir(f"{os.getcwd()}/exports/")

    prompt = "Input a name for the directory you want to export to."
    export_dir = get_valid_dir_name(prompt)

# Prints out a list of filenames, and file information for the user to review
# before generating the files.
    fnames = []
    for i_session, session in enumerate(range(0, total_sessions)):
        for i_cond, cond in enumerate(range(0, cond_per_participant)):
            for i, fname in enumerate(range(0, participant_number)):
                i = i + 1
                str_i = str(i)
                if len(str_i) < 2:
                    str_i = f"0{str_i}"
                fname = f"{experiment_id}{str_i}_{sensor_list[i_cond]}_conditions_s{i_session + 1}.csv"
                print(fname)
                fnames.append(fname)

    print("Above are the file names that will be generated by this script.")
    for i, task_num in enumerate(task_num_per_session):
        print(f"Session {i + 1} has {task_num} tasks.")
    print(f"Files will be exported to: {export_dir}")
    print("Does the above information appear to be correct?: ")
    ans = input("(Y/n)")
    if ans[0].upper() == "Y":
        os.chdir(export_dir)
        break
    print("Okay, lets try again then.")
    time.sleep(2)
    os.system("clear")

for fname in fnames:
    for i, task_num in enumerate(task_num_per_session):
        if int(fname[-5]) == i + 1:
            task_row = [f"Task{x + 1}" for x in range(0, task_num)]
            task_row.insert(0, "")
            onset_row = ["" for x in range(0, task_num)]
            onset_row.insert(0, "onset")
            duration_row = ["" for x in range(0, task_num)]
            duration_row.insert(0, "duration")
            stim_row = ["" for x in range(0, task_num)]
            stim_row.insert(0, "stim")
            tlxm_row = ["" for x in range(0, task_num)]
            tlxm_row.insert(0, "TLX_Mental")
            tlxph_row = ["" for x in range(0, task_num)]
            tlxph_row.insert(0, "TLX_Physical")
            tlxt_row = ["" for x in range(0, task_num)]
            tlxt_row.insert(0, "TLX_Temporal")
            tlxp_row = ["" for x in range(0, task_num)]
            tlxp_row.insert(0, "TLX_Performance")
            tlxe_row = ["" for x in range(0, task_num)]
            tlxe_row.insert(0, "TLX_Effort")
            tlxf_row = ["" for x in range(0, task_num)]
            tlxf_row.insert(0, "TLX_Frustration")
            print(fname)
            print(task_row)

            # file_rows = [task_row, onset_row, duraction_row]

            file_rows = [task_row, onset_row, duration_row,
                         stim_row, tlxm_row, tlxph_row,
                         tlxt_row, tlxp_row, tlxe_row, tlxf_row]

            with open(f"{fname}", "w") as out_csv:
                 writer = csv.writer(out_csv, delimiter=",")

                 for row in file_rows:
                     writer.writerow(row)
