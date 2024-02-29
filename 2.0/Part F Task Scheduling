# =============================================================================
# Section F - Test Task Scheduler (Start of CTRL + / here)
# =============================================================================

import datetime

current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

username = 'xavier'

log_filename = "Task_Scheduler.log"

logging.basicConfig(filename=log_filename,
                    level=logging.INFO,
                    format='%(asctime)s, xavier - INFO - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

activities = [
    'Task Scheduler ran successfully'
]

for activity in activities:
    logging.info(activity)

# =============================================================================
# End of Section F (End of CTRL + / here)
# =============================================================================

import win32com.client

def create_task(name, path_to_python, path_to_script, working_directory, start_time="21:18"):
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')

    # Define the task
    task_def = scheduler.NewTask(0)
    task_def.RegistrationInfo.Description = 'Run StorageManager.py at specified timing'
    task_def.RegistrationInfo.Author = 'Billy'

    # Create trigger
    start_boundary = f"2024-02-29T{start_time}:00"  # Start date and time (ISO 8601)
    trigger = task_def.Triggers.Create(2)  # 2 signifies a daily trigger
    trigger.StartBoundary = start_boundary
    trigger.DaysInterval = 1

    # Create action
    action = task_def.Actions.Create(0)  # 0 signifies an exec action
    action.Path = path_to_python
    action.Arguments = f'"{path_to_script}"'
    action.WorkingDirectory = working_directory  # Set the working directory

    # Set principal
    task_def.Principal.RunLevel = 1  # 1 = highest privileges

    # Register the task (create or update, if already exists)
    root_folder.RegisterTaskDefinition(
        name,
        task_def,
        6,  # 6 means CREATE_OR_UPDATE
        None,  # User (None means current user)
        None,  # Password (None means current user's password)
        3,  # 3 means run whether user is logged on or not
        ""  # No sddl (security descriptor)
    )

PATH_TO_PYTHON = "C:\\Users\\Billy\\PycharmProjects\\StorageManagement\\venv\\Scripts\\python.exe"
PATH_TO_SCRIPT = "C:\\Users\\Billy\\PycharmProjects\\StorageManagement\\StorageManager.py"
WORKING_DIRECTORY = "C:\\Users\\Billy\\PycharmProjects\\StorageManagement"

create_task("RunStorageManagerDaily", PATH_TO_PYTHON, PATH_TO_SCRIPT, WORKING_DIRECTORY, "21:18")
