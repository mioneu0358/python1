import os
from datetime import datetime, timedelta
import discord
import openai
from googletrans import Translator
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI
import random

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
OPENAI_KEY = os.getenv('OPENAI_KEY')

client = OpenAI(api_key=OPENAI_KEY)

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

@bot.command(name="질문")
async def Q2Gpt(ctx, *query):
    print(' '.join(query))
    completion = client.chat.completions.create(
        model= "gpt-4o",  #"gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": ' '.join(query)
            }

        ]
    )
    await ctx.send(f"질문: {' '.join(query)}\n답변: {completion.choices[0].message.content}")



number_baseball_games = {}

def generate_number():
    digits = random.sample(range(10), 3)
    return ''.join(map(str, digits))

def calculate_score(secret, guess):
    strikes = sum(1 for s, g in zip(secret, guess) if s == g)
    balls = sum(1 for g in guess if g in secret) - strikes
    return strikes, balls

class NumberGuessModal(discord.ui.Modal):
    def __init__(self, user_id):
        super().__init__(title="숫자 야구 게임")
        self.user_id = user_id
        self.input = discord.ui.TextInput(label="3자리 숫자를 입력하세요.", min_length=3, max_length=3)
        self.add_item(self.input)

    async def on_submit(self, interaction: discord.Interaction):
        guess = self.input.value
        secret_number = number_baseball_games.get(self.user_id)

        if not guess.isdigit() or len(set(guess)) != 3:
            await interaction.response.send_message("서로 다른 3자리 숫자를 입력하세요!", ephemeral=True)
            return

        if not secret_number:
            await interaction.response.send_message("먼저 게임을 시작해주세요!", ephemeral=True)
            return

        strikes, balls = calculate_score(secret_number, guess)
        if strikes == 3:
            await interaction.response.send_message(f"정답입니다! {secret_number}를 맞추셨습니다!")
            del number_baseball_games[self.user_id]  # 게임 종료 후 제거
        else:
            await interaction.response.send_message(f"{strikes} 스트라이크, {balls} 볼입니다. 다시 시도해보세요!", ephemeral=True)

@bot.command(name="숫자야구시작")
async def start_game(ctx):
    secret_number = generate_number()
    number_baseball_games[ctx.author.id] = secret_number
    await ctx.send(f"{ctx.author.name}님, 개인 숫자 야구 게임을 시작합니다! 버튼을 눌러 숫자를 입력하세요.",
                   view=NumberInputView(ctx.author.id))

class NumberInputView(discord.ui.View):
    def __init__(self, secret_number):
        super().__init__()
        self.secret_number = secret_number

    @discord.ui.button(label="숫자 입력", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NumberGuessModal(self.secret_number))


bot.run(TOKEN)
