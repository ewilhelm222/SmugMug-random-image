#!/bin/bash

# Calculate random delay within the time window (11 hours * 60 minutes/hour = 660 minutes)
RANDOM_DELAY=$((RANDOM % 300))

# Print the delay to the screen
echo "Delaying (seconds): $RANDOM_DELAY"

# Calculate and print the approximate end time of the first delay
END_TIME=$(date -v +${RANDOM_DELAY}S +"%Y-%m-%d %H:%M:%S")
echo "Approximate end time of first delay: $END_TIME"

# Wait for the calculated delay
sleep "${RANDOM_DELAY}"

# Execute the Python script
# Uncomment the next line to execute the Python script
python3 /Users/username/Pictures/SmugMug_Random.py

# Calculate delay before answer
RANDOM_DELAY2=$((RANDOM % 300))

echo "Delaying (seconds): $((300 + RANDOM_DELAY2))"

# Wait for the calculated delay
sleep "$((300 + RANDOM_DELAY2))"

# Execute the Python reading script
# Uncomment the next line to execute the Python reading script
python3 /Users/username/Pictures/Read_SmugMug_log.py
