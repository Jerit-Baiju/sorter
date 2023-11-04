from datetime import datetime
import os


def fmt_date(fmt):
    return datetime.strptime(fmt, "%d/%m/%y")


def eval_date(content):
    try:
        fmt_date(content)
        return True
    except:
        return False

def run(filename, destination_dir):
    with open(filename, 'r') as file:
        lines = file.readlines()

    dates = []
    chats = []

    for line in lines:
        day = line.split(',')[0]
        if day not in dates:
            try:
                if eval_date(day):
                    dates.append(day)
            except:
                pass

    for date in dates:
        chat = []
        for line in lines:
            if date == line.split(',')[0]:
                chat.append(line)
        chats.append(chat)

    for chat in chats:
        date = fmt_date(chat[0].split(',')[0])
        year_folder = os.path.join(destination_dir, str(date.year))
        month_folder = os.path.join(year_folder, date.strftime("%B"))

        file_name = os.path.join(month_folder,f"Chats/{date.strftime('%d-%B-%Y')}.txt")
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
    os.remove(filename)
