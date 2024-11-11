import os
import shutil
from datetime import datetime, timezone

# Define the source directory and the destination directory
SOURCE_DIR = "files"
DESTINATION_DIR = "exports"

MOVED = 0
EXISTING = 0
moved_months = []
moved_types = []

timestamp1 = ("IMG_", "VID_", "MVIMG_", "SAVE_", "MVIMG_")
timestamp2 = ("IMG-", "AUD-", "PTT-", "VID-", "null-", "DOC")
timestamp3 = ("2017-", "2018-", "2019-", "2020-", "2021-", "2022-", "2023-", "2024-")
timestamp4 = ("2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024")
timestamp5 = ("Screenshot_",)
timestamp6 = ("Screenrecorder-",)
timestamp7 = ("IMG20",)
timestamp8 = (")_", "call_")
timestamp9 = ("WhatsApp ", "Screen Recording")
timestamp10 = ("Screenshot ",)
timestamp11 = ("VID",)


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
    if raw_name.endswith(".opus"):
        return "Voice Notes"
    if "record" in raw_name.lower():
        return "Screen Records"
    if raw_name.startswith("Screenshot"):
        return "Screenshots"
    if raw_name.endswith((".mp4", ".MP4")):
        return "Videos"
    if any_in([")_", "call"], raw_name.lower()):
        return "Call Records"
    if raw_name.startswith("DOC") or raw_name.endswith((".pdf", ".csv")):
        return "Documents"
    return "Other" if other else "main"


def chat_sorter(raw_chat_file):
    with open(raw_chat_file, "r", encoding="utf-8") as file:
        lines = [line.replace("[", "").replace("]", " -") for line in file.readlines()]
    chat_dates = []
    chats = []
    for line in lines:
        day = line.split(",")[0]
        if day not in chat_dates:
            try:
                if eval_date(day):
                    chat_dates.append(day)
            except:
                pass
    for chat_date in chat_dates:
        chat = []
        for line in lines:
            if chat_date == line.split(",")[0]:
                chat.append(line)
        chats.append(chat)
    for chat in chats:
        chat_date = fmt_date(chat[0].split(",")[0])
        file_name = os.path.join(
            DESTINATION_DIR, f"{chat_date.year}/{chat_date.strftime('%B')}/Chats/{chat_date.strftime('%d-%B-%Y')}.txt"
        )
        chat_file = os.path.dirname(file_name)
        if not os.path.exists(chat_file):
            os.makedirs(chat_file, exist_ok=True)
            with open(file_name, "w", encoding="utf-8") as file:
                file.writelines(chat)
                file.close()
        else:
            with open(file_name, "+a", encoding="utf-8") as file:
                file.writelines(chat)
                file.close()
    print(f"Chat is backed up from the date {chat_dates[0]} to {chat_dates[-1]} .")
    os.remove(raw_chat_file)


# Create the destination directory if it doesn't exist
if not os.path.exists(DESTINATION_DIR):
    os.makedirs(DESTINATION_DIR)
# Iterate over each file in the source directory
for filename in os.listdir(SOURCE_DIR):
    try:
        IS_OTHER = False
        file_path = os.path.join(SOURCE_DIR, filename)
        try:
            IS_RAW = bool(datetime.fromtimestamp(float(filename.split(".")[0]), timezone.utc))
        except:
            IS_RAW = False
        if filename.startswith("."):
            continue
        # Skip directories and non-files
        if not os.path.isfile(file_path):
            continue
        if filename.endswith(".txt"):
            chat_sorter(file_path)
            MOVED += 1
            continue
        if (
            not filename.startswith(
                timestamp1
                + timestamp2
                + timestamp3
                + timestamp4
                + timestamp5
                + timestamp6
                + timestamp7
                + timestamp9
                + timestamp10
                + timestamp11
            )
            and not any_in(timestamp8, filename)
        ) and not IS_RAW:
            IS_OTHER = True
            TIMESTAMP = str(datetime.today().strftime(r"%Y%m%d"))
        elif filename.startswith(timestamp1):
            TIMESTAMP = filename.split("_")[1]
        elif filename.startswith(timestamp2):
            TIMESTAMP = filename.split("-")[1]
        elif filename.startswith(timestamp3):
            pre = str(filename.split(".")[0]).split("-")
            TIMESTAMP = f"{pre[0]}{pre[1]}{pre[2]}"
        elif filename.startswith(timestamp4):
            TIMESTAMP = filename.split("_")[0]
        elif filename.startswith(timestamp5):
            if "com." in filename:
                pre = str(filename.split("_")[1]).split("-")
                TIMESTAMP = f"{pre[0]}{pre[1]}{pre[2]}"
            else:
                TIMESTAMP = str(filename.split("_")[1]).split("-", maxsplit=1)[0]
        elif filename.startswith(timestamp6):
            pre = filename.split("-")
            TIMESTAMP = f"{pre[1]}{pre[2]}{pre[3]}"
        elif filename.startswith(timestamp7):
            TIMESTAMP = filename.split(".")[0][3:11]
        elif any_in(timestamp8, filename):
            TIMESTAMP = f"{filename.split('_')[1].split('.')[0]}"[:8]
        elif filename.startswith(timestamp9):
            TIMESTAMP = f"{filename.split(' ')[2].replace('-', '')}"
        elif filename.startswith(timestamp10):
            TIMESTAMP = f"{filename.split(' ')[1].replace('-', '')}"
        elif filename.startswith(timestamp11):
            TIMESTAMP = f"{filename[3:11]}"
            print(TIMESTAMP)
        elif IS_RAW:
            TIMESTAMP = datetime.fromtimestamp(float(filename.split(".")[0]), timezone.utc).strftime("%Y%m%d")
        else:
            print("unknown error occurred")
            break
        try:
            date = datetime.strptime(TIMESTAMP, "%Y%m%d")
        except:
            TIMESTAMP = str(datetime.today().strftime(r"%Y%m%d"))
            date = datetime.strptime(TIMESTAMP, "%Y%m%d")
        month_name = date.strftime("%B")
        year_folder = os.path.join(DESTINATION_DIR, str(date.year))
        month_folder = os.path.join(year_folder, date.strftime("%B"))
        os.makedirs(f"{month_folder}/.p", exist_ok=True)
        FILE_TYPE = check_type(filename, IS_OTHER)
        if FILE_TYPE == "main":
            destination_path = os.path.join(month_folder, filename)
        else:
            os.makedirs(f"{month_folder}/{FILE_TYPE}", exist_ok=True)
            destination_path = os.path.join(f"{month_folder}/{FILE_TYPE}", filename)
        if os.path.exists(destination_path):
            EXISTING += 1
            print(f"{filename} already exists in {destination_path}")
            continue
        month_log = f"{date.year}-{month_name}"
        if month_log not in moved_months:
            moved_months.append(month_log)
        if FILE_TYPE not in moved_types:
            moved_types.append(FILE_TYPE)
        shutil.move(file_path, destination_path)
        # print(f'{filename} moved to {destination_path} from {file_path}')
        MOVED += 1
    except IndexError as e:
        print(", ".join(e.args), f" - {filename}")
    except:
        print(f"Error at file - {filename}")

print(f"Moved files - {MOVED}")
print(f"Already existing files - {EXISTING}")
print(f"Types sorted - {', '.join(moved_types) if moved_types else 'None'}")
print(f"Moved months - {', '.join(moved_months) if moved_months else 'None'}")
