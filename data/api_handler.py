## This file handles API management with Notion so it can keep me updated on what is due today for work and school, as well as clearing out completed tasks for specific boards across different workspaces to keep my to-do list clear and ready to go automatically.

import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import pytz  # Add this import

# Load environment variables
load_dotenv()

# Define Central Time timezone
CENTRAL_TZ = pytz.timezone('America/Chicago')

# Prepare lists for tasks between all relevant dashboards
tasks_1 = []
tasks_2 = []
tasks_3 = []

def tasks1(dashboard, lst):
    
    # Get current day name in Central Time
    today = datetime.now(CENTRAL_TZ).strftime("%A")
    
    # Notion API setup
    token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv(dashboard)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Find the page for today
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    filter_data = {
        "filter": {
            "property": "Name",
            "title": {
                "equals": today
            }
        }
    }
    
    response = requests.post(url, headers=headers, json=filter_data)

    # Request is good!
    if response.status_code == 200:
        results = response.json().get('results', [])
        
        if results:
            page_id = results[0]['id']
            
            # Get the content/blocks from today's page
            blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
            blocks_response = requests.get(blocks_url, headers=headers)
            
            # Request is good!
            if blocks_response.status_code == 200:
                blocks = blocks_response.json().get('results', [])
                
                # Temporary list to collect all tasks before sorting
                temp_tasks = []
                
                for block in blocks:
                    if block.get('type') == 'to_do':
                        checked = block['to_do']['checked']
                        text_content = ""
                        
                        # Extract text from the to-do
                        rich_text = block['to_do']['rich_text']
                        if rich_text:
                            text_content = rich_text[0]['text']['content']
                        
                        # Add to temporary list with status
                        status = "✅" if checked else "⬜"
                        temp_tasks.append((checked, f"{status} {text_content}"))

                # Sort tasks: unchecked (⬜) first, then checked (✅)
                temp_tasks.sort(key=lambda x: x[0])  # False (unchecked) comes before True (checked)
                
                # Add sorted tasks to the main list
                for _, task_text in temp_tasks:
                    lst.append(task_text)

                if not lst:
                    lst.append("No tasks for today! 🎉")
                    
            else:
                print(f"Unable to get tasks due to: {blocks_response.status_code}")
        else:
            print(f"Unable to get tasks due to: No page found for {today}")
    else:
        print(f"Error accessing database: {response.status_code}")
        print(response.text)

    return lst

def tasks2(dashboard, lst):
    
    # Notion API setup
    token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv(dashboard)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Find pages in the "Not started" column
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    filter_data = {
        "filter": {
            "property": "Status",
            "status": {
                "equals": "Not started"
            }
        }
    }
    
    response = requests.post(url, headers=headers, json=filter_data)

    # Request is good!
    if response.status_code == 200:
        results = response.json().get('results', [])
        
        if results:
            for page in results:
                # Extract the page title
                properties = page.get('properties', {})
                
                # Find the title property
                page_title = "N/A"
                for prop_name, prop_data in properties.items():
                    if prop_data.get('type') == 'title':
                        title_array = prop_data.get('title', [])
                        if title_array:
                            page_title = title_array[0].get('text', {}).get('content', 'Untitled')
                        break
                
                # Add page title to the list
                lst.append(f"📌 {page_title}")

            if not lst:
                lst.append("No tasks for today! 🎉")

    else:
        print(f"Error accessing database: {response.status_code}")
        print(response.text)
    
    return lst

def tasks3(dashboard, lst):
        
    # Notion API setup
    token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv(dashboard)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # Find pages in the "To-Do" column
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    filter_data = {
        "filter": {
            "property": "Status",
            "select": {
                "equals": "To-Do"
            }
        }
    }
    
    response = requests.post(url, headers=headers, json=filter_data)

    # Request is good!
    if response.status_code == 200:
        results = response.json().get('results', [])
        
        if results:
            for page in results:
                # Extract the page title
                properties = page.get('properties', {})
                
                # Find the title property
                page_title = "N/A"
                for prop_name, prop_data in properties.items():
                    if prop_data.get('type') == 'title':
                        title_array = prop_data.get('title', [])
                        if title_array:
                            page_title = title_array[0].get('text', {}).get('content', 'Untitled')
                        break
                
                # Add page title to the list
                lst.append(f"📌 {page_title}")

            if not lst:
                lst.append("No tasks for today! 🎉")

    else:
        print(f"Error accessing database: {response.status_code}")
        print(response.text)
    
    return lst

def delete_completed(dashboard):
    
    # Notion API setup
    token = os.getenv('NOTION_TOKEN')
    database_id = os.getenv(dashboard)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    
    # Set up filter based on dashboard type
    if dashboard in ['NOTION_DASHBOARD2', 'NOTION_DASHBOARD3']:
        filter_data = {
            "filter": {
                "property": "Status",
                "status": {
                    "equals": "Done"
                }
            }
        }
    elif dashboard == 'NOTION_DASHBOARD4':
        filter_data = {
            "filter": {
                "property": "Status",
                "select": {
                    "equals": "Completed"
                }
            }
        }
    else:
        return
    
    response = requests.post(url, headers=headers, json=filter_data)

    if response.status_code == 200:
        results = response.json().get('results', [])
        
        if results:
            for page in results:
                page_id = page['id']
                
                # Delete the page
                delete_url = f"https://api.notion.com/v1/blocks/{page_id}"
                requests.delete(delete_url, headers=headers)