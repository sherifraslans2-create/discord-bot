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
        if not message.author.guild_permissions.ban_members:
            await message.channel.send("انت مش ادمن"); return
        if len(message.mentions) == 0:
            await message.channel.send("اكتب: تف @الشخص السبب"); return
        member = message.mentions[0]
        reason = " ".join(parts[2:]) if len(parts) > 2 else "مفيش سبب"
        await member.ban(reason=reason)
        await message.channel.send(f"🔨 {member.mention} خد تف السبب: {reason}")

    if cmd == "برا":
        if not message.author.guild_permissions.kick_members:
            await message.channel.send("انت مش ادمن"); return
        if len(message.mentions) == 0:
            await message.channel.send("اكتب: برا @الشخص السبب"); return
        member = message.mentions[0]
        reason = " ".join(parts[2:]) if len(parts) > 2 else "مفيش سبب"
        await member.kick(reason=reason)
        await message.channel.send(f"👢 {member.mention} اتعملو برا السبب: {reason}")

    if cmd == "انتايم":
        if not message.author.guild_permissions.moderate_members:
            await message.channel.send("انت مش ادمن"); return
        if len(message.mentions) == 0: return
        member = message.mentions[0]
        await member.timeout(None)
        await message.channel.send(f"✅ {member.mention} اتفك التايم بتاعه")

    if cmd == "فك":
        if not message.author.guild_permissions.ban_members:
            await message.channel.send("انت مش ادمن"); return
        if len(parts) < 2:
            await message.channel.send("اكتب: فك @الشخص"); return
        target_id = None
        target_name = None
        if len(message.mentions) > 0:
            target_id = message.mentions[0].id
            target_name = message.mentions[0].name
        else:
            target_name = parts[1].replace("@", "")
        unbanned = False
        async for ban in message.guild.bans():
            user = ban.user
            if (target_id and user.id == target_id) or (target_name and (user.name == target_name or str(user.id) == target_name)):
                await message.guild.unban(user)
                await message.channel.send(f"✅ اتفك التف عن {user.name}")
                unbanned = True
                break
        if not unbanned:
            await message.channel.send("مش لاقي الشخص ده في البان، اتأكد انك كاتب اسمه صح")

    if cmd == "تح":
        if len(message.mentions) == 0: return
        member = message.mentions[0]
        reason = " ".join(parts[2:]) if len(parts) > 2 else "مفيش سبب"
        warnings_db.setdefault(member.id, []).append(reason)
        await message.channel.send(f"⚠️ {member.mention} خد تحذير السبب: {reason} | بقى عنده {len(warnings_db[member.id])} تحذير")

    if cmd == "تحذيرات":
        if len(message.mentions) == 0:
            await message.channel.send("اكتب: تحذيرات @الشخص"); return
        member = message.mentions[0]
        warns = warnings_db.get(member.id, [])
        if not warns:
            await message.channel.send(f"{member.mention} معندوش تحذيرات")
        else:
            await message.channel.send(f"تحذيرات {member.mention} : {len(warns)}\n" + "\n".join([f"{i+1}. {w}" for i, w in enumerate(warns)]))

    if cmd == "شيل":
        if len(message.mentions) == 0: return
        member = message.mentions[0]
        if member.id in warnings_db and warnings_db[member.id]:
            warnings_db[member.id].pop()
            await message.channel.send(f"✅ اتشال تحذير من {member.mention} بقى عنده {len(warnings_db[member.id])}")
        else:
            await message.channel.send("معندوش تحذيرات اصلا")

    if cmd == "مسح":
        if not message.author.guild_permissions.manage_messages:
            await message.channel.send("انت مش ادمن"); return
        num = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 10
        await message.channel.purge(limit=num+1)
        await message.channel.send(f"تم مسح {num} رسالة", delete_after=3)

    if cmd == "قفل":
        if not message.author.guild_permissions.manage_channels:
            await message.channel.send("انت مش ادمن"); return
        await message.channel.set_permissions(message.guild.default_role, send_messages=False)
        await message.channel.send("🔒 الروم اتقفلت")

    if cmd == "فتح":
        if not message.author.guild_permissions.manage_channels:
            await message.channel.send("انت مش ادمن"); return
        await message.channel.set_permissions(message.guild.default_role, send_messages=True)
        await message.channel.send("🔓 الروم اتفتحت")

    if cmd == "بطئ":
        if not message.author.guild_permissions.manage_channels:
            await message.channel.send("انت مش ادمن"); return
        sec = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 5
        await message.channel.edit(slowmode_delay=sec)
        await message.channel.send(f"🐢 الشات بقى بطيء كل {sec} ثانية")

    if cmd == "ر" or cmd == "رول" or cmd == "+rar":
        if not message.author.guild_permissions.manage_roles:
            await message.channel.send("انت مش ادمن"); return
        if len(message.mentions) == 0 or len(parts) < 3:
            await message.channel.send("اكتب: ر @الشخص اسم الرتبة"); return
        member = message.mentions[0]
        role_name = " ".join(parts[2:])
        role = discord.utils.get(message.guild.roles, name=role_name)
        if not role:
            await message.channel.send("مفيش رتبة بالاسم ده"); return
        await member.add_roles(role)
        await message.channel.send(f"✅ {member.mention} خد رتبة {role.name}")

    if cmd == ".roles":
        roles = [r.name for r in message.guild.roles if r.name != "@everyone"]
        await message.channel.send("رولات السيرفر:\n" + "\n".join(roles))

    if cmd == "معلومات":
        if len(message.mentions) > 0:
            m = message.mentions[0]
            await message.channel.send(f"👤 {m.mention}\nالاسم: {m.name}\nدخل: {m.joined_at}\nالايدي: {m.id}")
        else:
            g = message.guild
            await message.channel.send(f"🏠 سيرفر {g.name}\nالاعضاء: {g.member_count}")

    if cmd == "بنج":
        await message.channel.send(f"البوت شغال 🏓 {round(bot.latency*1000)}ms")

    if cmd == "صوره":
        if len(message.mentions) > 0:
            m = message.mentions[0]
            await message.channel.send(m.display_avatar.url)
        else:
            await message.channel.send(message.author.display_avatar.url)

    if cmd == "تك":
        overwrites = {
            message.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            message.author: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        ch = await message.guild.create_text_channel(f"تكت-{message.author.name}", overwrites=overwrites)
        await ch.send(f"{message.author.mention} عمل تكت، اكتب مشكلتك والادمن هيرد عليك")
        await message.channel.send(f"اتعمل تكتك {ch.mention}")

    if cmd == "لوك":
        if "تكت-" in message.channel.name:
            await message.channel.delete()
        else:
            await message.channel.send("دي مش روم تكت")

    if cmd == "نكته":
        jokes = [
            "مرة واحد دخل السيرفر نسي يطلع 😂",
            "ليه الكمبيوتر زعلان؟ عشان حد داس على مشاعره",
            "مرة واحد كان بيحب الشات اوي، اتجوز الادمن",
            "ليه البطريق بيحب البرد؟ عشان بيتلج من الحر"
        ]
        await message.channel.send(random.choice(jokes))

    if cmd == "روليت":
        if len(message.mentions) == 0:
            await message.channel.send("اكتب: روليت @الشخص"); return
        member = message.mentions[0]
        if random.randint(1, 6) == 1:
            await message.channel.send(f"💥 بووووم! {member.mention} خسر في الروليت")
        else:
            await message.channel.send(f"😮‍💨 {member.mention} نجا من الروليت، حظك حلو")

bot.run(os.environ['TOKEN'])
