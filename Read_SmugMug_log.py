import re
import subprocess

def extract_most_recent_album(log_file_path):
    # Adjusted regex pattern to match multiline entries, properly capturing only the album URL
    album_pattern = re.compile(
        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - INFO - Album: (.+?)\nAlbum URL: (https?://.+?)(?=\n|$)", 
        re.DOTALL
    )

    most_recent_timestamp = None
    most_recent_album = None
    most_recent_url = None

    with open(log_file_path, 'r') as file:
        log_content = file.read()
        matches = album_pattern.findall(log_content)
        for match in matches:
            timestamp, album, url = match
            if most_recent_timestamp is None or timestamp > most_recent_timestamp:
                most_recent_timestamp = timestamp
                most_recent_album = album
                most_recent_url = url

    if most_recent_album and most_recent_url:
        # Construct clickable link (HTML format for web usage)
        clickable_link = f"{most_recent_album}: {most_recent_url}"
        return clickable_link
    else:
        return "No album found."

def send_link_via_applescript(clickable_link):
    apple_script_command = f'''
    tell application "Messages"
        set targetChatID to "iMessage;+;chat____CHATID_________" -- Your actual group chat ID
        set targetService to id of 1st account whose service type = iMessage
        set targetChat to (a reference to chat id targetChatID of account id targetService)
        send "{clickable_link}" to targetChat
    end tell
    '''
    subprocess.run(["osascript", "-e", apple_script_command])

# Example usage
log_file_path = 'smugmug_log.txt'
clickable_link = extract_most_recent_album(log_file_path)
if clickable_link != "No album found.":
    print(f"{clickable_link}")
    send_link_via_applescript(clickable_link)
else:
    print("No album found.")
