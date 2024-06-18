import requests
import random
import time
import re
import os

# Global variables
ACCESS_TOKEN = 'EAAQzbxqK9QkBO0tNvNh2B9FiZB5RPW2Qqsv7FiMcsqt1iZCgAQ3a6jAsZBvEoeZALqKuMLP9QGXdaHi9XZCG6ZBO6mZAUbN8KvOiG7oEfFA1vaNfipZBdH23gADl3eBIr3miRZCyZBJpMr4JZA5hpSudPXIGUZCqKjZBcQrmkNK70ZBQ2n0DKNReLKJIOevOb8gBEZCT7bkmubuLaBB6BMFJn3XYcqaJe1GwMLXN0vYa0nDhbqe8G5Pqr0DwqfvZClat0KJ9EmEZD'  # Replace with your access token

# List of Facebook accounts with their credentials
accounts = []

# Base URLs for Graph API endpoints
BASE_URL = 'https://graph.facebook.com/v13.0/'
REACTIONS_URL = BASE_URL + '{}/reactions'
FOLLOW_URL = BASE_URL + '{}/subscribers'
SHARE_URL = BASE_URL + '{}/sharedposts'

# Function to clear the console screen
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to login to Facebook and get session cookie
def facebook_login(email, password):
    url = 'https://www.facebook.com/login.php'
    data = {
        'email': email,
        'pass': password
    }
    session = requests.Session()
    session.post(url, data=data)
    return session

# Function to react to a Facebook post
def auto_react(session, post_id, reaction_type):
    reactions = {
        'like': 1,
        'love': 2,
        'haha': 3,
        'wow': 4,
        'sad': 7,
        'angry': 8
    }
    if reaction_type.lower() in reactions:
        reaction_code = reactions[reaction_type.lower()]
        url = REACTIONS_URL.format(post_id)
        params = {
            'access_token': ACCESS_TOKEN,
            'type': reaction_code
        }
        try:
            response = session.post(url, params=params)
            response_data = response.json()
            if response.status_code == 200:
                print(f"\033[92mSuccessfully reacted '{reaction_type}' to post {post_id}\033[0m")
            else:
                error_message = response_data.get('error', {}).get('message', 'Unknown error')
                print(f"\033[91mFailed to react. Status code: {response.status_code}, Error: {error_message}\033[0m")
        except requests.exceptions.RequestException as e:
            print(f"\033[91mAn error occurred: {str(e)}\033[0m")
    else:
        print("\033[91mInvalid reaction type. Available types: like, love, haha, wow, sad, angry\033[0m")

# Function to follow a Facebook profile or page
def auto_follow(session, target_id):
    url = FOLLOW_URL.format(target_id)
    params = {
        'access_token': ACCESS_TOKEN
    }
    try:
        response = session.post(url, params=params)
        response_data = response.json()
        if response.status_code == 200:
            print(f"\033[92mSuccessfully followed {target_id}\033[0m")
        else:
            error_message = response_data.get('error', {}).get('message', 'Unknown error')
            print(f"\033[91mFailed to follow. Status code: {response.status_code}, Error: {error_message}\033[0m")
    except requests.exceptions.RequestException as e:
        print(f"\033[91mAn error occurred: {str(e)}\033[0m")

# Function to share a Facebook post
def auto_share(session, post_id):
    url = SHARE_URL.format(post_id)
    params = {
        'access_token': ACCESS_TOKEN
    }
    try:
        response = session.post(url, params=params)
        response_data = response.json()
        if response.status_code == 200:
            print(f"\033[92mSuccessfully shared post {post_id}\033[0m")
        else:
            error_message = response_data.get('error', {}).get('message', 'Unknown error')
            print(f"\033[91mFailed to share. Status code: {response.status_code}, Error: {error_message}\033[0m")
    except requests.exceptions.RequestException as e:
        print(f"\033[91mAn error occurred: {str(e)}\033[0m")

# Function to perform actions using a random Facebook account from the accounts list
def perform_actions(post_id, reaction_type, follow_target_id, share_post_id):
    if not accounts:
        print("\033[91mNo accounts added yet. Please add accounts first.\033[0m")
        return
    
    # Select a random account from the accounts list
    account = random.choice(accounts)
    session = facebook_login(account['email'], account['password'])

    # Perform actions based on user selection
    if post_id:
        auto_react(session, post_id, reaction_type)
    if follow_target_id:
        auto_follow(session, follow_target_id)
    if share_post_id:
        auto_share(session, share_post_id)

    session.close()

# Function to extract Facebook post ID from link (example implementation)
def extract_post_id(post_link):
    pattern = r'facebook\.com/.+/posts/(\d+)'
    match = re.search(pattern, post_link)
    if match:
        return match.group(1)
    else:
        print("\033[91mInvalid Facebook post link. Please follow this format: https://www.facebook.com/{username}/posts/{post_id}\033[0m")
        return None

# Function to extract Facebook page ID from link (example implementation)
def extract_page_id(page_link):
    pattern = r'facebook\.com/(pages|page)/(.+?)/?(\?|\Z)'
    match = re.search(pattern, page_link)
    if match:
        return match.group(2)
    else:
        print("\033[91mInvalid Facebook page link. Please follow this format: https://www.facebook.com/pages/{page_name}/{page_id}\033[0m")
        return None

# Function to extract Facebook profile ID from link (example implementation)
def extract_profile_id(profile_link):
    pattern = r'facebook\.com/(.+?)(\?|\Z)'
    match = re.search(pattern, profile_link)
    if match:
        return match.group(1)
    else:
        print("\033[91mInvalid Facebook profile link. Please follow this format: https://www.facebook.com/{username}\033[0m")
        return None

# Example usage
if __name__ == "__main__":
    while True:
        clear_console()
        print("""
    WELCOME TO BESTSMMPH BOOSTING SERVICE
    created by boss Jack For BestSMMph.com 

    1. Boost Now
    2. Add Account
    3. Show All Added Accounts
    4. Exit
        """)
        choice = input("Enter your choice: ")

        if choice == '1':
            clear_console()
            print("""
    1. Boost Reaction
    2. Boost Facebook Page Followers
    3. Boost Facebook Profile Followers
    4. Boost Shares
            """)
            boost_choice = input("Enter your boost choice: ")

            if boost_choice == '1':
                reaction_type = input("Enter reaction type (like, love, haha, wow, sad, angry): ")
                post_link = input("Enter Facebook post link to react: ")
                post_id = extract_post_id(post_link)
                if post_id:
                    interval = int(input("Enter interval (in seconds): "))
                    num_reactions = min(len(accounts), int(input(f"Select how many reactions (max {len(accounts)}): ")))
                    print(f"\033[93mStarting {num_reactions} reactions...\033[0m")
                    for i in range(num_reactions):
                        perform_actions(post_id, reaction_type, None, None)
                        print(f"Remaining accounts that reacted: {num_reactions - i - 1}")
                        time.sleep(interval)
            
            elif boost_choice == '2':
                page_link = input("Enter Facebook page link to boost followers: ")
                page_id = extract_page_id(page_link)
                if page_id:
                    interval = int(input("Enter interval (in seconds): "))
                    num_followers = min(len(accounts), int(input(f"Select how many page followers (max {len(accounts)}): ")))
                    print(f"\033[93mStarting {num_followers} page followers boost...\033[0m")
                    for i in range(num_followers):
                        perform_actions(None, None, page_id, None)
                        print(f"Remaining accounts that followed page: {num_followers - i - 1}")
                        time.sleep(interval)
            
            elif boost_choice == '3':
                profile_link = input("Enter Facebook profile link to boost followers: ")
                profile_id = extract_profile_id(profile_link)
                if profile_id:
                    interval = int(input("Enter interval (in seconds): "))
                    num_followers = min(len(accounts), int(input(f"Select how many profile followers (max {len(accounts)}): ")))
                    print(f"\033[93mStarting {num_followers} profile followers boost...\033[0m")
                    for i in range(num_followers):
                        perform_actions(None, None, profile_id, None)
                        print(f"Remaining accounts that followed profile: {num_followers - i - 1}")
                        time.sleep(interval)
            
            elif boost_choice == '4':
                share_link = input("Enter Facebook post link to share: ")
                share_post_id = extract_post_id(share_link)
                if share_post_id:
                    interval = int(input("Enter interval (in seconds): "))
                    num_shares = min(len(accounts), int(input(f"Select how many shares (max {len(accounts)}): ")))
                    print(f"\033[93mStarting {num_shares} shares...\033[0m")
                    for i in range(num_shares):
                        perform_actions(None, None, None, share_post_id)
                        print(f"Remaining accounts that shared: {num_shares - i - 1}")
                        time.sleep(interval)
            
            else:
                print("\033[91mInvalid choice. Please enter a valid option.\033[0m")
        
        elif choice == '2':
            email = input("Enter email: ")
            password = input("Enter password: ")
            accounts.append({'email': email, 'password': password})
            print(f"\033[92mAccount added successfully.\033[0m")
        
        elif choice == '3':
            if not accounts:
                print("\033[91mNo accounts added yet.\033[0m")
            else:
                print("\033[93mAll added accounts:\033[0m")
                for index, account in enumerate(accounts, start=1):
                    print(f"Account {index}: Email - {account['email']}")
        
        elif choice == '4':
            print("\nExiting program...")
            break
        
        else:
            print("\033[91mInvalid choice. Please enter a valid option.\033[0m")
        
        input("\nPress Enter to continue...")
