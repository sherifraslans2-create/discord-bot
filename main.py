import discord
import re
import datetime
import random
import os

intents = discord.Intents.all()
bot = discord.Client(intents=intents)

warnings_db = {}

def parse_time(text):
    match = re.match(r"(\d+)([mhd])", text)
    if not match: return None
    num = int(match.group(1))
    unit = match.group(2)
    if unit == "m": return num * 60
    if unit == "h": return num * 3600
    if unit == "d": return num * 86400

@bot.event
async def on_ready():
    print("البوت اونلاين!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.strip()
    parts = content.split()
    if not parts: return
    cmd = parts[0]
    low = content.lower()

    if low == "السلام عليكم" or low == "سلام عليكم":
        await message.channel.send(f"وعليكم السلام ورحمة الله وبركاته نورت الشات يا عسل 😚 {message.author.mention}")
        return
    if low == "باك" or low == "back":
        await message.channel.send(f"ولكم باك منور يا غالي ♥ {message.author.mention}")
        return
    if low == "برب" or low == "brb":
        await message.channel.send(f"تيييت 🥳 لا تطول علينا الشات ينتظرك ❤ {message.author.mention}")
        return

    if cmd == "تايم":
        if not message.author.guild_permissions.moderate_members:
            await message.channel.send("انت مش ادمن"); return
        if len(message.mentions) == 0 or len(parts) < 3:
            await message.channel.send("اكتب: تايم @الشخص 10m السبب"); return
        member = message.mentions[0]
        seconds = parse_time(parts[2])
        if not seconds:
            await message.channel.send("اكتب المدة صح: 10m او 1h او 1d"); return
        reason = " ".join(parts[3:]) if len(parts) > 3 else "مفيش سبب"
        await member.timeout(discord.utils.utcnow() + datetime.timedelta(seconds=seconds), reason=reason)
        await message.channel.send(f"🔇 {member.mention} خد تايم لمدة {parts[2]} السبب: {reason}")

    if cmd == "تف":
        if not message
