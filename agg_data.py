import os
import json
import pandas as pd

def load_users():
    """Loads user information from the 'users.json' file.

    Returns:
        dict: A dictionary containing user information including name, email, and time zone.
    """
    with open('users.json') as file:
        users = json.load(file)
        user_data = {user['id']: {'name': user['profile']['first_name'] + ' ' + user['profile']['last_name'], 'email': user['profile']['email'], 'time zone': user['tz']} for user in users}
    return user_data

def load_channel_messages(channel_name):
    """Loads messages from a specific channel.

    Args:
        channel_name (str): The name of the channel (folder) to load messages from.

    Returns:
        dict: A dictionary containing user IDs as keys and a list of messages as values.
    """
    channel_messages = {}
    for filename in os.listdir(channel_name):
        if filename.endswith('.json'):
            with open(os.path.join(channel_name, filename)) as file:
                messages = json.load(file)
                for message in messages:
                    user_id = message['user']
                    text = message['text']
                    if user_id not in channel_messages:
                        channel_messages[user_id] = []
                    channel_messages[user_id].append(text)
    return channel_messages

# Load user information
user_data = load_users()

# Load channel messages
channels = ['help', 'legionella', 'general', 'random']
channel_messages = {channel: load_channel_messages(channel) for channel in channels}

# Create DataFrame
data = []
for user_id, user_info in user_data.items():
    contributions = 0
    for channel in channels:
        count = len(channel_messages[channel].get(user_id, []))
        contributions += count
        row = {
            'name': user_info['name'],
            'contributions': contributions,
            'channel': channel,
            'count': count
        }
        data.append(row)

df = pd.DataFrame(data)
# Save DataFrame to a CSV file
df.to_csv('2023_vsoar_slack_data.tsv', sep='\t', index=False)

print("Data table created and saved as 2023_vsoar_slack_data.tsv")

