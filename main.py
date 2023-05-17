import os
import shutil
from datetime import datetime

# Define the source directory and the destination directory
source_dir = "files"
destination_dir = "exports"

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Iterate over each file in the source directory
for filename in os.listdir(source_dir):
    file_path = os.path.join(source_dir, filename)

    timestamp1 = ('IMG_', 'VID_', 'MVIMG_', 'SAVE_')
    timestamp2 = ('IMG-', 'AUD-', 'PTT-', 'VID-', 'null-')
    timestamp3 = ('2020-', '2021-', '2022-','2023-')
    timestamp4 = ('Screenshot_',)
    timestamp5 = ('Screenrecorder-',)

    # Skip directories and non-files
    if not os.path.isfile(file_path):
        continue

    if not filename.startswith(timestamp1 + timestamp2 + timestamp3 + timestamp4 + timestamp5):
        continue

    if filename.startswith(timestamp1):
        timestamp = filename.split('_')[1]

    elif filename.startswith(timestamp2):
        timestamp = filename.split('-')[1]

    elif filename.startswith(timestamp3):
        pre = str(filename.split('.')[0]).split('-')
        timestamp = f"{pre[0]}{pre[1]}{pre[2]}"

    elif filename.startswith(timestamp4):
        pre = str(filename.split('_')[1]).split('-')
        timestamp = f"{pre[0]}{pre[1]}{pre[2]}"

    elif filename.startswith(timestamp5):
        pre = filename.split('-')
        timestamp = f"{pre[1]}{pre[2]}{pre[3]}"

    date = datetime.strptime(timestamp, '%Y%m%d')

    # Create the year and month folders in the destination directory
    year_folder = os.path.join(destination_dir, str(date.year))
    month_folder = os.path.join(year_folder, date.strftime("%B"))

    os.makedirs(month_folder, exist_ok=True)

    # # Move the file to the month folder
    destination_path = os.path.join(month_folder, filename)
    shutil.move(file_path, destination_path)

    print(f"Moved {filename} to {destination_path}")
