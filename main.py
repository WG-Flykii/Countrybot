import discord
import requests
import re
import io
import asyncio
import math
from datetime import datetime, timedelta, timezone

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

image_channel_id =  # Channel where you can set up a new daily challenge
guess_channel_id =    # Channel where the daily challenge will be posted
ping_role_id =     # daily challenge ping role 
winner_role_id =   # winner role


original_lat = None
original_lon = None
challenge_active = False

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the distance between two points on the Earth."""
    R = 6371000  # radius of the earth (in meters)
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance_m = R * c
    return round(distance_m)

def format_distance(distance_m):
    """Format the distance in meters, kilometers, miles, and feet."""
    distance_km = distance_m / 1000
    distance_miles = distance_km * 0.621371  # km to miles
    distance_feet = distance_m * 3.28084      # meters to feet

    if distance_m >= 1000:
        return f"{round(distance_km)}Km ({round(distance_miles)} Miles)"
    else:
        return f"{round(distance_m)}m ({round(distance_feet)} feet)"


async def send_challenge_message(guess_channel):
    global image_url, challenge_active
    embed = discord.Embed(
        title="New 5K Challenge!",
        description="Guess the location using [the ChatGuessr Map](https://chatguessr.com/map/PlonkIt).\nYou can use **any** external tools you want !",
        color=discord.Color.blue()
    )
    await guess_channel.send(embed=embed)
    if image_url:
        await guess_channel.send(image_url)
    challenge_active = True 

async def send_ping_reminder(challenge_channel):
    role_ping = f"<@&{ping_role_id}>"
    await challenge_channel.send(f"{role_ping} Daily Challenge in 2 minutes!")

async def send_reminder_and_challenge(start_time):
    global challenge_active

    now = datetime.now(timezone.utc)
    challenge_channel = client.get_channel(guess_channel_id)
    reminder_time = start_time - timedelta(minutes=2)

    await asyncio.sleep((reminder_time - now).total_seconds())
    await send_ping_reminder(challenge_channel)

    await asyncio.sleep((start_time - reminder_time).total_seconds())
    await send_challenge_message(challenge_channel)

@client.event
async def on_message(message):
    global original_lat, original_lon, image_url, challenge_active

    if message.author == client.user:
        return

    if message.channel.id == image_channel_id:
        match = re.search(r"/w PlonkIt !g (-?\d+\.\d+), (-?\d+\.\d+)", message.content)
        if match and message.attachments:
            original_lat = float(match.group(1))
            original_lon = float(match.group(2))
            image_url = message.attachments[0].url

            now = datetime.now(timezone.utc)
            start_time = now.replace(hour=17, minute=0, second=0, microsecond=0) # 18:00 cet paris time
            if now >= start_time:
                start_time += timedelta(days=1)
            start_time_paris = start_time + timedelta(hours=1)
            formatted_start_time = start_time_paris.strftime("%d/%m/%Y %H:%M:%S")
            await message.channel.send(f"✅ Challenge is set up and will start today at {formatted_start_time} (Paris time).")
            challenge_active = True
            await send_reminder_and_challenge(start_time)


    if message.channel.id == guess_channel_id and challenge_active:
        guess_match = re.fullmatch(r"/w PlonkIt !g (-?\d+\.\d+), (-?\d+\.\d+)", message.content.strip())
        
        if guess_match:
            guess_lat = float(guess_match.group(1))
            guess_lon = float(guess_match.group(2))
            distance = haversine(original_lat, original_lon, guess_lat, guess_lon)
            formatted_distance = format_distance(distance)

            if distance <= 200:
                google_maps_url = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={original_lat},{original_lon}&heading=0&pitch=0"
                winner_role = discord.utils.get(message.guild.roles, id=winner_role_id)
                for member in winner_role.members:
                    await member.remove_roles(winner_role)
                await message.author.add_roles(winner_role)

                embed = discord.Embed(
                    title="🎉 5k Achieved!",
                    description=f"{message.author.mention}, you were {formatted_distance} away!",
                    color=discord.Color.green()
                )
                embed.add_field(name="Exact Location", value=f"[Click here to view on Streetview]({google_maps_url})")
                embed.set_footer(text="Great job!")
                await message.channel.send(embed=embed)
                challenge_active = False
            else:
                await message.channel.send(
                    embed=discord.Embed(
                        title="🚶 Keep Guessing!",
                        description=f"{message.author.mention}, you are {formatted_distance} away.",
                        color=discord.Color.orange()
                    )
                )
            await message.delete()


client.run('')  #bot-token
