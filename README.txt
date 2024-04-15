README

2024-03-16 

This sends a random image from our family picture archive on SmugMug to our family group chat. A few minutes later, it responds with the random image's album. The intention is to make a game of who can figure out/recognize the image first.

This was built using ChatGPT and Gemini. When code or a strategy from one didn't work, I bounced to the other, iterating back and forth until it all worked. I think ChatGPT 4.0 typically provided code that worked better or with few iterations. 

SmugMug_Random.py

Uses the SmugMug API to get all of the folders. Makes a random choice among the folders, then a random choice among the images in the folders. Logs the choice to smugmug_log.txt. Saves the image as a temporary file, because I don't want to send a link since the whole point is for the group to guess the place/event of the image and the URL gives that away. Calls the Apple Script: send_to_twinkle_turtles.scpt

send_to_twinkle_turtles.scpt

Sends the image and text note to the group iMessage thread named, in my case, The Twinkly Turtles. Doing it this way because one of the members of the group only has an iCloud address, not a phone number. Services such as Twilio only target phone numbers for sending messages, not iCloud addresses via iMessage. This wrinkle causes major strategy implications, such as needing to run this whole process from my laptop, not from a cloud service, as I would prefer. 

Sending the file only works if the image is within the /Users/username/Pictures folder. To keep things together, I put all the files into this folder, except the .plist. I don't know why this is a requirement, but found the information here: https://apple.stackexchange.com/questions/429586/cannot-send-image-files-from-messages-using-applescript-on-monterey

Read_SmugMug_log.py

Reads the log file smugmug_log.txt and pulls out the album name and URL of the most recent log entry. Sends the album name and URL to the iMessage group chat by sending the command directly to Apple Script. Sending the name of the album as a clickable link with the name as anchor text and the URL as the link appears not be something Apple Script can do? This seems dumb, but so far I didn't push on it.

wrapper_SmugMug_Random.sh

This is a bash script that runs on days when the random image should be sent out. It chooses a random time to send the image (SmugMug_Random.py), and then follows up at a random time between 5 and 10 minutes later with the answer (Read_SmugMug_log.py).

com.user.smugmug_random.plist


This .plist file defines scheduled tasks for launchd, macOS's system-level manager, to automatically execute scripts or applications based on specified timing or conditions. It is set to run on Saturdays and Sundays at 8 AM. The timing in wrapper_SmugMug_Random.sh makes it such that a random image is sent out at a random time between 8 AM and 7 PM on Saturday and Sunday. This file is in ~/Library/LaunchAgents/ (unlike the rest of the files, which I put in /Users/username/Pictures).

Setup

Various things need to happen to make this all work. I did many of these while building it.

- API keys and Tokens from SmugMug

- Permissions for Apple Script to access files and Messenger - this can be frustrating because at least in my version of MacOS (13.4 (22F66)) this permission is only granted when the programs first try to access something. 

-  load the .plist with launchctl load ~/Library/LaunchAgents/com.user.smugmug_random.plist -- I think this now will launch every time I restart the computer, but am not yet sure.

- Getting the chat group ID. This was painful and required lots of trial and error. Using the following Apple Script: 

tell application "Messages"
	repeat with aChat in text chats
		if (id of aChat) is equal to "iMessage;+;chat___CHATID____" then
			send "Test message to The Twinkly Turtles" to aChat
			exit repeat
		end if
	end repeat
end tell

Gave me a bunch of errors with actual chat IDs that I tested by trial and error to figure out which was the correct one for my desired group thread. People on my various group threads may have been annoyed by my testing...
 
- SmugMug authentication: The major issue was using oauth = OAuth1Session(API_KEY, client_secret=API_SECRET, resource_owner_key=ACCESS_TOKEN, resource_owner_secret=ACCESS_TOKEN_SECRET)
and 
response = oauth.get

As the ImageSizeDetails API endpoint didn't work with the following even though the albums endpoint worked with it:
auth = OAuth1(api_key, client_secret=None, resource_owner_key=access_token, resource_owner_secret=access_token_secret)
and
response = requests.get(url, auth=auth, headers=headers).json()

- Got the Apple Script to trigger and work by placing the image, Python, and Apple Scripts in the /Users/ewilhelm/Pictures/ folder and explicitly calling the Apple Script with its extension:
result = subprocess.run(["osascript", "/Users/username/Pictures/send_to_twinkle_turtles.scpt"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)


