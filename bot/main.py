import discord
import os
import sys
import datetime
import pytz
from discord.ext import commands, tasks
from dotenv import load_dotenv

# Add the parent directory to Python path to import from run.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run import format_daily_message
from data.api_handler import delete_completed

load_dotenv()

# Define Central Time timezone
CENTRAL_TZ = pytz.timezone('America/Chicago')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
token = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

@bot.event
async def on_ready():
    # Use Central Time for logging
    ct_time = datetime.datetime.now(CENTRAL_TZ)
    print(f"\n[{ct_time.strftime('%Y-%m-%d %H:%M:%S %Z')}] Logged in as {bot.user.name}")
    daily_briefing.start()  # Start the morning briefing task
    nightly_cleanup.start()  # Start the nightly cleanup task

@bot.command()
async def briefing(ctx):
    """Manual command to trigger daily briefing"""
    try:
        message = format_daily_message()
        await ctx.send(message)
        ct_time = datetime.datetime.now(CENTRAL_TZ)
        print(f"\n[{ct_time.strftime('%Y-%m-%d %H:%M:%S %Z')}] Manual Briefing completed")
    except Exception as e:
        await ctx.send(f"Sorry, there was an error generating the briefing: {str(e)}")
        print(f"Error in briefing command: {e}")

@bot.command()
async def cleanup(ctx):
    """Manual command to trigger cleanup"""
    try:
        delete_completed('NOTION_DASHBOARD1')
        delete_completed('NOTION_DASHBOARD2') 
        delete_completed('NOTION_DASHBOARD3')
        ct_time = datetime.datetime.now(CENTRAL_TZ)
        print(f"\n[{ct_time.strftime('%Y-%m-%d %H:%M:%S %Z')}] Manual Cleanup completed")
    except Exception as e:
        await ctx.send(f"Sorry, there was an error during cleanup: {str(e)}")
        print(f"Error in cleanup command: {e}")

# Create time objects in Central Time
CT_6AM = datetime.time(hour=6, minute=0, tzinfo=CENTRAL_TZ)
CT_11_59PM = datetime.time(hour=23, minute=59, tzinfo=CENTRAL_TZ)

@tasks.loop(time=CT_6AM)
async def daily_briefing():
    """Automatically send daily briefing at 6 AM Central Time"""
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            message = format_daily_message()
            await channel.send(message)
            ct_time = datetime.datetime.now(CENTRAL_TZ)
            print(f"\n[{ct_time.strftime('%Y-%m-%d %H:%M:%S %Z')}] Daily automatic briefing sent")
        else:
            print(f"Channel with ID {CHANNEL_ID} not found!")
    except Exception as e:
        print(f"Error in daily briefing: {e}")

@tasks.loop(time=CT_11_59PM)
async def nightly_cleanup():
    """Automatically cleanup completed tasks at 11:59 PM Central Time"""
    try:
        delete_completed('NOTION_DASHBOARD2')
        delete_completed('NOTION_DASHBOARD3') 
        delete_completed('NOTION_DASHBOARD4')
        ct_time = datetime.datetime.now(CENTRAL_TZ)
        print(f"\n[{ct_time.strftime('%Y-%m-%d %H:%M:%S %Z')}] Nightly cleanup completed")
    except Exception as e:
        print(f"Error in nightly cleanup: {e}")

@daily_briefing.before_loop
async def before_daily_briefing():
    await bot.wait_until_ready()

@nightly_cleanup.before_loop
async def before_nightly_cleanup():
    await bot.wait_until_ready()

if __name__ == "__main__":
    if token:
        bot.run(token)
    else:
        print("Error: DISCORD_TOKEN not found in environment variables!")