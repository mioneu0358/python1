# https://discordpy.readthedocs.io/en/latest/interactions/api.html?highlight=command#interaction    :    discord.py document

import os
from datetime import datetime, timedelta
import discord
from googletrans import Translator
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

banned_words = ["비속어", "나쁜말"]
warning_record = {}
mute_list = {'abc': datetime.now()}

@bot.event
async def on_ready():
    print(f"{bot.user}가 접속했습니다.")

@bot.event
async def on_member_join(member):
    await member.send(f"{member.name}님, 반갑습니다.")


@bot.command(name="채팅벤현황")
async def show_mute_list(ctx):
    ret_str = ""
    for key,value in mute_list.items():
        ret_str += f"{key}님은 {value.strftime('%H시 %M분 %S초')}까지 채팅이 금지되었습니다.\n"
    await ctx.send(ret_str)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # 채팅 금지 상태 확인 및 관리
    if message.author.id in mute_list:
        if datetime.now() < mute_list[message.author.id]:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} 경고 3회 초과로 {mute_list[message.author.id].strftime('%H시 %M분 %S초')}까지 채팅이 금지됩니다.")
            return
        else:
            del mute_list[message.author.id]

    # 금지어 체크 및 경고 누적
    if any(word in message.content for word in banned_words):
        await message.delete()
        await message.channel.send(f"{message.author.mention} 금지어를 사용하셨습니다!")

        warning_record[message.author.id] = warning_record.get(message.author.id, 0) + 1

        if warning_record[message.author.id] >= 3:
            mute_list[message.author.id] = datetime.now() + timedelta(minutes=10)
            await message.channel.send(f"{message.author.mention} 경고 3회 초과로 10분간 채팅 금지됩니다.")
        else:
            await message.channel.send(f"{message.author.mention} 경고 {warning_record[message.author.id]}회입니다. 3회가 되면 채팅이 10분간 금지됩니다.")


    await bot.process_commands(message)


bot.run(TOKEN)
