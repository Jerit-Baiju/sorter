import os
import shutil
from datetime import datetime, timezone

# Define the source directory and the destination directory
source_dir = "files"
destination_dir = ".."

moved = 0
existing = 0
moved_months = []
moved_types = []

timestamp1 = ('IMG_', 'VID_', 'MVIMG_', 'SAVE_', 'MVIMG_')
timestamp2 = ('IMG-', 'AUD-', 'PTT-', 'VID-', 'null-', 'DOC')
timestamp3 = ('2017-', '2018-','2019-','2020-', '2021-', '2022-', '2023-', '2024-')
timestamp4 = ('2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024')
timestamp5 = ('Screenshot_',)
timestamp6 = ('Screenrecorder-',)
timestamp7 = ('IMG20',)
timestamp8 = (')_', 'call_')
timestamp9 = ('WhatsApp ', 'Screen Recording')
timestamp10 = ('Screenshot ',)
timestamp11 = ('VID',)


def fmt_date(fmt):
    return datetime.strptime(fmt, "%d/%m/%y")


def eval_date(content):
    try:
        fmt_date(content)
        return True
    except:
        return False


def any_in(checks, target):
    for check in checks:
        if check in target:
            return True
    return False


def check_type(raw_name, other=False):
    if raw_name.endswith('.opus'):
        return 'Voice Notes'
    if 'record' in raw_name.lower():
        return 'Screen Records'
    if raw_name.startswith('Screenshot'):
        return 'Screenshots'
    if raw_name.endswith(('.mp4', '.MP4')):
        return 'Videos'
    if any_in ([')_', 'call'], raw_name.lower()):
        return 'Call Records'
    if raw_name.startswith('DOC') or raw_name.endswith(('.pdf', '.csv')):
        return 'Documents'
    return 'Other' if other else 'main'

def chat_sorter(raw_chat_file):
    with open(raw_chat_file, 'r') as file:
        lines = [line.replace('[', '').replace(']', ' -') for line in file.readlines()]
    chat_dates = []
    chats = []
    for line in lines:
        day = line.split(',')[0]
        if day not in chat_dates:
            try:
                if eval_date(day):
                    chat_dates.append(day)
            except:
                pass
    for chat_date in chat_dates:
        chat = []
        for line in lines:
            if chat_date == line.split(',')[0]:
                chat.append(line)
        chats.append(chat)
    for chat in chats:
        chat_date = fmt_date(chat[0].split(',')[0])
        file_name = os.path.join(
            destination_dir, f"{chat_date.year}/{chat_date.strftime('%B')}/Chats/{chat_date.strftime('%d-%B-%Y')}.txt")
        chat_file = os.path.dirname(file_name)
        if not os.path.exists(chat_file):
            os.makedirs(chat_file, exist_ok=True)
            with open(file_name, 'w') as file:
                file.writelines(chat)
                file.close()
        else:
            with open(file_name, '+a') as file:
                file.writelines(chat)
                file.close()
    print(f"Chat is backed up from the date {chat_dates[0]} to {chat_dates[-1]} .")
    os.remove(raw_chat_file)


# Create the destination directory if it doesn't exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)
# Iterate over each file in the source directory
for filename in os.listdir(source_dir):
    try:
        is_other = False
        file_path = os.path.join(source_dir, filename)
        try:
            is_raw = bool(datetime.fromtimestamp(float(filename.split('.')[0]), timezone.utc))
        except:
            is_raw = False
        if filename.startswith('.'):
            continue
        # Skip directories and non-files
        if not os.path.isfile(file_path):
            continue
        if filename.endswith('.txt'):
            chat_sorter(file_path)
            moved += 1
            continue
        if (not filename.startswith(timestamp1 + timestamp2 + timestamp3 + timestamp4 + timestamp5 + timestamp6 + timestamp7 + timestamp9 + timestamp10 + timestamp11 ) and not any_in(timestamp8, filename)) and not is_raw:
            is_other = True
            timestamp = str(datetime.today().strftime(r'%Y%m%d'))
        elif filename.startswith(timestamp1):
            timestamp = filename.split('_')[1]
        elif filename.startswith(timestamp2):
            timestamp = filename.split('-')[1]
        elif filename.startswith(timestamp3):
            pre = str(filename.split('.')[0]).split('-')
            timestamp = f"{pre[0]}{pre[1]}{pre[2]}"
        elif filename.startswith(timestamp4):
            timestamp = filename.split('_')[0]
        elif filename.startswith(timestamp5):
            if 'com.' in filename:
                pre = str(filename.split('_')[1]).split('-')
                timestamp = f"{pre[0]}{pre[1]}{pre[2]}"
            else:
                timestamp = str(filename.split('_')[1]).split('-', maxsplit=1)[0]
        elif filename.startswith(timestamp6):
            pre = filename.split('-')
            timestamp = f"{pre[1]}{pre[2]}{pre[3]}"
        elif filename.startswith(timestamp7):
            timestamp = filename.split('.')[0][3:11]
        elif any_in(timestamp8, filename):
            timestamp = f"{filename.split('_')[1].split('.')[0]}"[:8]
        elif filename.startswith(timestamp9):
            timestamp = f"{filename.split(' ')[2].replace('-', '')}"
        elif filename.startswith(timestamp10):
            timestamp = f"{filename.split(' ')[1].replace('-', '')}"
        elif filename.startswith(timestamp11):
            timestamp = f"{filename[3:11]}"
            print(timestamp)
        elif is_raw:
            timestamp = datetime.fromtimestamp(float(filename.split('.')[0]), timezone.utc).strftime('%Y%m%d')
        else:
            print('unknown error occurred')
            break
        try:
            date = datetime.strptime(timestamp, '%Y%m%d')
        except:
            timestamp = str(datetime.today().strftime(r'%Y%m%d'))
            date = datetime.strptime(timestamp, '%Y%m%d')
        month_name = date.strftime('%B')
        year_folder = os.path.join(destination_dir, str(date.year))
        month_folder = os.path.join(year_folder, date.strftime("%B"))
        os.makedirs(f'{month_folder}/.p', exist_ok=True)
        file_type = check_type(filename, is_other)
        if file_type == 'main':
            destination_path = os.path.join(month_folder, filename)
        else:
            os.makedirs(f"{month_folder}/{file_type}", exist_ok=True)
            destination_path = os.path.join(f"{month_folder}/{file_type}", filename)
        if os.path.exists(destination_path):
            existing += 1
            print(f'{filename} already exists in {destination_path}')
            continue
        month_log = f'{date.year}-{month_name}'
        if month_log not in moved_months:
            moved_months.append(month_log)
        if file_type not in moved_types:
            moved_types.append(file_type)
        shutil.move(file_path, destination_path)
        # print(f'{filename} moved to {destination_path} from {file_path}')
        moved += 1
    except IndexError as e:
        print(', '.join(e.args),f' - {filename}')
    except :
        print(f"Error at file - {filename}")

print(f"Moved files - {moved}")
print(f"Already existing files - {existing}")
print(f"Types sorted - {', '.join(moved_types) if moved_types else 'None'}")
print(f"Moved months - {', '.join(moved_months) if moved_months else 'None'}")
