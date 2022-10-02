from discord.ext import commands, tasks
import discord
from dataclasses import dataclass
import datetime
import os
from dotenv import load_dotenv


MAX_SESSION_TIME_MINUTES = 30

# This example requires the 'message_content' intent.

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = os.getenv("CHANNEL_ID")


@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
session = Session()

@bot.event
async def on_ready():
    print("Hello! Bot is ready!")
    channel = bot.get_channel(int(CHANNEL_ID))
    await channel.send('Hello! Study bot is ready!')
    
@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2)
async def break_reminder():
    
    # ignore the first loop
    if break_reminder.current_loop == 0:
        return
    
    channel = bot.get_channel(int(CHANNEL_ID))
    await channel.send(f"***Take a break! *** You've been studying for {MAX_SESSION_TIME_MINUTES} minutes.")
    
@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")
    
@bot.command()
async def info(ctx):
    await ctx.send("This is a discord for networking and studying/learning/building together!")
    
@bot.command()
async def add(ctx, *arr):
    result = 0
    for i in arr:
        result += int(i)
    await ctx.send(f"Result: {result}")
    
@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return
    
    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    break_reminder.start()
    
    await ctx.send(f"New session started at {human_readable_time}")
    
@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session is active!")
        return
    
    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    break_reminder.stop()
    await ctx.send(f"Session ended after {human_readable_duration} seconds")
    
bot.run(BOT_TOKEN)