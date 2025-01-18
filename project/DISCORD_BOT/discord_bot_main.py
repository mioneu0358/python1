import os
from datetime import datetime, timedelta
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI  # OpenAI API를 사용하여 GPT 호출

# 환경 변수 로드 (TOKEN, OPENAI_KEY)
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
OPENAI_KEY = os.getenv('OPENAI_KEY')

# OpenAI API 클라이언트 설정
client = OpenAI(api_key=OPENAI_KEY)

# 디스코드 봇 생성 및 설정
intents = discord.Intents.all()  # 모든 인텐트 활성화
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    """봇이 실행되었을 때 콘솔에 출력"""
    print(f"{bot.user}가 접속했습니다.")

@bot.event
async def on_member_join(member):
    """서버에 새로운 멤버가 가입하면 개인 DM으로 환영 메시지 전송"""
    await member.send(f"{member.name}님, 반갑습니다!")

@bot.command(name="관리권한확인")
async def check_manage_permissions(ctx):
    """유저가 가지고 있는 'manage_' 권한 목록을 확인"""
    permissions = ctx.author.guild_permissions  # 유저의 권한 가져오기
    manage_permissions_list = {
        "서버 관리": permissions.manage_guild,
        "역할 관리": permissions.manage_roles,
        "채널 관리": permissions.manage_channels,
        "메시지 관리": permissions.manage_messages,
        "권한 관리": permissions.manage_permissions,
        "웹훅 관리": permissions.manage_webhooks,
        "이모지 관리": permissions.manage_emojis,
        "닉네임 관리": permissions.manage_nicknames,
        "스레드 관리": permissions.manage_threads,
    }

    result = [f"✅ {perm}" if value else f"🚫 {perm}" for perm, value in manage_permissions_list.items()]
    await ctx.send(f"**{ctx.author.mention}님의 'Manage' 관련 권한 상태:**\n" + "\n".join(result))


# 🚨 [기능 1] 채팅 금지 시스템 (금지어 필터 & 경고 시스템)
banned_words = ["비속어", "나쁜말"]  # 금지어 목록
warning_record = {}  # 유저별 경고 기록 저장
mute_list = {}  # 채팅 금지된 유저 목록 (유저 ID : 해제 시간)

@bot.command(name="채팅벤현황")
async def show_mute_list(ctx):
    """현재 채팅이 금지된 유저 목록 출력"""
    ret_str = "현재 채팅 금지된 사용자 목록:\n"
    for key, value in mute_list.items():
        ret_str += f"{key}님은 {value.strftime('%H시 %M분 %S초')}까지 채팅이 금지되었습니다.\n"
    await ctx.send(ret_str)

@bot.event
async def on_message(message):
    """메시지 필터링 및 경고 시스템"""
    if message.author == bot.user:
        return  # 봇의 메시지는 무시

    # 채팅 금지 확인
    if message.author.id in mute_list:
        if datetime.now() < mute_list[message.author.id]:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} 경고 3회 초과로 {mute_list[message.author.id].strftime('%H시 %M분 %S초')}까지 채팅이 금지됩니다."
            )
            return
        else:
            del mute_list[message.author.id]  # 채팅 금지 해제

    # 금지어 확인 및 경고 증가
    if any(word in message.content for word in banned_words):
        await message.delete()
        await message.channel.send(f"{message.author.mention} 금지어를 사용하셨습니다!")

        warning_record[message.author.id] = warning_record.get(message.author.id, 0) + 1

        if warning_record[message.author.id] >= 3:
            mute_list[message.author.id] = datetime.now() + timedelta(minutes=10)  # 10분 금지
            await message.channel.send(f"{message.author.mention} 경고 3회 초과로 10분간 채팅 금지됩니다.")
        else:
            await message.channel.send(f"{message.author.mention} 경고 {warning_record[message.author.id]}회입니다. 3회가 되면 채팅이 10분간 금지됩니다.")

    await bot.process_commands(message)  # 명령어 처리


@bot.command(name="질문")
async def Q2Gpt(ctx, *query):
    """GPT에게 질문을 하고 답변을 받는 기능"""
    question = ' '.join(query)  # 질문을 하나의 문자열로 변환
    await ctx.send("🤖 GPT가 답변을 준비하고 있습니다...")

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",  # GPT 모델 선택
            messages=[{"role": "user", "content": question}]
        )
        response = completion.choices[0].message.content  # GPT 응답 가져오기
        await ctx.send(f"**질문:** {question}\n**답변:** {response}")
    except Exception as e:
        await ctx.send("❌ GPT 응답 중 오류가 발생했습니다. 다시 시도해주세요.")
        print(f"오류 발생: {e}")


# 🎲 [기능 2] 숫자 야구 게임 기능
number_baseball_games = {}  # 플레이어별 게임 데이터 저장

def generate_number():
    """서로 다른 3자리 숫자로 이루어진 정답 생성"""
    digits = random.sample(range(10), 3)
    return ''.join(map(str, digits))


def calculate_score(secret, guess):
    """입력한 숫자와 정답 비교하여 스트라이크 & 볼 개수 계산"""
    strikes = sum(1 for s, g in zip(secret, guess) if s == g)
    balls = sum(1 for g in guess if g in secret) - strikes
    return strikes, balls


class NumberBaseballGame:
    """숫자 야구 게임 상태 관리"""

    def __init__(self, user_id):
        self.user_id = user_id
        self.secret_number = generate_number()  # 정답 생성
        self.attempts = 0
        self.max_attempts = 10  # 최대 10회 시도 가능

    def check_guess(self, guess):
        """입력값을 확인하고 스트라이크 & 볼 개수를 반환"""
        self.attempts += 1
        strikes, balls = calculate_score(self.secret_number, guess)

        if strikes == 3:
            return True, f"🎉 정답입니다! {self.secret_number}를 {self.attempts}번 만에 맞추셨습니다!"

        if self.attempts >= self.max_attempts:
            return False, f"💀 10번의 시도 안에 정답을 맞추지 못했습니다. 정답은 {self.secret_number}였습니다."

        return False, f"⚾ {strikes} 스트라이크, {balls} 볼입니다. ({self.attempts}/{self.max_attempts}회 시도)"


class NumberGuessModal(discord.ui.Modal):
    """숫자 입력을 받기 위한 Modal UI"""

    def __init__(self, user_id):
        super().__init__(title="숫자 야구 게임")
        self.user_id = user_id

        # 3개의 숫자 입력칸 추가
        self.num1 = discord.ui.TextInput(label="첫 번째 숫자", min_length=1, max_length=1)
        self.num2 = discord.ui.TextInput(label="두 번째 숫자", min_length=1, max_length=1)
        self.num3 = discord.ui.TextInput(label="세 번째 숫자", min_length=1, max_length=1)

        self.add_item(self.num1)
        self.add_item(self.num2)
        self.add_item(self.num3)

    async def on_submit(self, interaction: discord.Interaction):
        """사용자가 입력을 제출했을 때 실행"""
        if self.user_id not in number_baseball_games:
            await interaction.response.send_message("먼저 `!숫자야구시작`을 입력하여 게임을 시작하세요!", ephemeral=True)
            return

        game = number_baseball_games[self.user_id]
        guess = self.num1.value + self.num2.value + self.num3.value

        # 유효성 검사 (서로 다른 3자리 숫자)
        if not guess.isdigit() or len(set(guess)) != 3:
            await interaction.response.send_message("서로 다른 3자리 숫자를 입력하세요!", ephemeral=True)
            return

        is_correct, message = game.check_guess(guess)

        if is_correct or "정답은" in message:
            del number_baseball_games[self.user_id]  # 게임 종료 후 삭제
            await interaction.response.send_message(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)


class NumberInputView(discord.ui.View):
    """숫자 입력을 위한 버튼 UI"""

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    @discord.ui.button(label="숫자 입력", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        """숫자 입력 버튼 클릭 시 Modal 창 표시"""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("이 게임은 다른 사람이 진행 중입니다!", ephemeral=True)
            return
        await interaction.response.send_modal(NumberGuessModal(self.user_id))


@bot.command(name="숫자야구시작")
async def start_game(ctx):
    """숫자 야구 게임 시작"""
    if ctx.author.id in number_baseball_games:
        await ctx.send("이미 게임이 진행 중입니다!", ephemeral=True)
        return

    number_baseball_games[ctx.author.id] = NumberBaseballGame(ctx.author.id)
    await ctx.send(f"{ctx.author.name}님, 숫자 야구 게임을 시작합니다! 버튼을 눌러 숫자를 입력하세요.",
                   view=NumberInputView(ctx.author.id), ephemeral=True)


bot.run(TOKEN)
