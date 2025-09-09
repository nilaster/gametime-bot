from datetime import datetime
import json
import os
from typing import List, Tuple
import zoneinfo

import dateparser
import discord
from discord.ext import commands
from discord.utils import get
import dotenv


dotenv.load_dotenv()


description = """Game Time Manager"""

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", description=description, intents=intents)

config_path = "data.json"
if not os.path.exists(config_path):
    members_timezones: dict[str, str] = {}
    next_game: datetime | None = None
else:
    with open(config_path) as f:
        data = json.load(f)
    members_timezones = data["members_timezones"]
    if data["next_game"] is None:
        next_game = None
    else:
        next_game = datetime.fromtimestamp(data["next_game"])
    
    
def save():
    with open(config_path, "w") as f:
        data = {
            "members_timezones": members_timezones,
            "next_game": next_game.timestamp() if next_game is not None else None,
        }
        json.dump(data, f)
    

def dt_string_for_all_timezones(dt: datetime):
    data: List[Tuple[discord.Member, datetime]] = []
    for user_id, tz_name in members_timezones.items():
        member = get(bot.get_all_members(), id=int(user_id))
        if member is None:
            continue
        zone_info = zoneinfo.ZoneInfo(tz_name)
        local_dt = dt.astimezone(zone_info)
        data.append((member, local_dt))
    
    data.sort(key=lambda x: x[1].utcoffset())
    
    result = []
    for member, dt in data:
        tzname = str(dt.tzinfo)
        tzname = tzname.split("/", 1)[1] if "/" in tzname else tzname
        dt_str = dt.strftime("%A %d %B %I:%M %p")
        result.append(f"- {member.display_name}: {dt_str}")
    return "\n".join(result)


@bot.command()
async def timezone(ctx: commands.Context, zone: str):
    available = zoneinfo.available_timezones()
    found = [x for x in available if x.lower() == zone.lower()]
    if found:
        selected = found[0]
    else:
        found = [x for x in zoneinfo.available_timezones() if zone.lower() in x.lower()]
        if not found:
            return await ctx.send(f"Error: Invalid timezone: {zone}")
        selected = found[0]
    members_timezones[str(ctx.author.id)] = selected
    await ctx.send(f"Success: {selected} is set as your timezone.")
    save()


@bot.command()
async def time(ctx: commands.Context, *text: str):
    parsed_text = " ".join(text)
    date = dateparser.parse(parsed_text)
    if date is None:
        return await ctx.send("Invalid date/time string")
    if date.tzinfo is None:
        member_tz = members_timezones.get(str(ctx.author.id))
        if member_tz is None:
            return await ctx.send(
                "Error: Either provide a timezone or set a default one using: `!timezone <timezone>`"
            )
        tzinfo = zoneinfo.ZoneInfo(member_tz)
        date = date.replace(tzinfo=tzinfo)
    data = dt_string_for_all_timezones(date)
    await ctx.send(data)


@bot.command()
async def game(ctx: commands.Context, *text: str):
    global next_game
    if not text:
        if next_game is not None:
            data = dt_string_for_all_timezones(next_game)
            return await ctx.send(f"Next game set for:\n\n{data}")
        else:
            return await ctx.send("No game set. Use `!game <date and time>` to set one")
    parsed_text = " ".join(text)
    date = dateparser.parse(parsed_text)
    if date is None:
        return await ctx.send("Invalid date/time string")
    if date.tzinfo is None:
        member_tz = members_timezones.get(str(ctx.author.id))
        if member_tz is None:
            return await ctx.send(
                "Error: Either provide a timezone or set a default one using: `!timezone <timezone>`"
            )
        tzinfo = zoneinfo.ZoneInfo(member_tz)
        date = date.replace(tzinfo=tzinfo)
    next_game = date
    data = dt_string_for_all_timezones(date)
    await ctx.send(f"Next game is set for:\n\n{data}")
    save()


token = os.getenv("DISCORD_TOKEN")

if token is None:
    print("Error: DISCORD_TOKEN environment variable is not set.")
    exit(1)

bot.run(token)
