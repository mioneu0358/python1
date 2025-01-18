import os
import discord
from discord.ext import commands
from discord.ui import View, Button, TextInput
from dotenv import load_dotenv
from datetime import datetime, timedelta

# 환경 변수 로드
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# 디스코드 봇 설정
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# 투표 데이터 저장
active_polls = {}

class PollCreationView(View):
    """투표 생성 창 - 항목 추가 및 투표 시작"""
    def __init__(self, creator_id):
        super().__init__()
        self.creator_id = creator_id
        self.topic = None
        self.options = []

    @discord.ui.button(label="투표 주제 입력", style=discord.ButtonStyle.primary)
    async def enter_topic(self, interaction: discord.Interaction, button: discord.ui.Button):
        """투표 주제 입력"""
        modal = TopicInputModal(self.creator_id, self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="항목 추가하기", style=discord.ButtonStyle.secondary)
    async def add_option(self, interaction: discord.Interaction, button: discord.ui.Button):
        """투표 항목 추가"""
        modal = OptionInputModal(self.creator_id, self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="투표 시작하기", style=discord.ButtonStyle.success)
    async def start_poll(self, interaction: discord.Interaction, button: discord.ui.Button):
        """투표 시작"""
        if interaction.user.id != self.creator_id:
            await interaction.response.send_message("🚫 이 버튼은 투표 생성자만 사용할 수 있습니다.", ephemeral=True)
            return

        if not self.topic or len(self.options) < 1:
            await interaction.response.send_message("❌ 투표 주제와 최소 1개의 항목이 필요합니다.", ephemeral=True)
            return

        active_polls[self.creator_id] = {
            "topic": self.topic,
            "options": self.options,
            "votes": {opt: [] for opt in self.options},
            "creator": self.creator_id,
            "is_active": False,
            "end_time": None,
            "user_votes": {},
            "custom_votes": {}
        }

        await interaction.response.send_message(
            "⏳ 마감 시간을 설정해주세요!",
            view=SetPollDurationView(self.creator_id),
            ephemeral=True
        )

    def generate_embed(self):
        """투표 UI Embed 생성"""
        embed = discord.Embed(title="🗳️ 투표 생성", color=discord.Color.blue())
        embed.add_field(name="**투표 주제**", value=self.topic if self.topic else "아직 입력되지 않음", inline=False)
        if self.options:
            options_text = "\n".join([f"- {opt}" for opt in self.options])
            embed.add_field(name="**투표 항목**", value=options_text, inline=False)
        else:
            embed.add_field(name="**투표 항목**", value="아직 추가되지 않음", inline=False)
        return embed


class TopicInputModal(discord.ui.Modal):
    """투표 주제 입력 Modal"""
    def __init__(self, creator_id, view: PollCreationView):
        super().__init__(title="📝 투표 주제 입력")
        self.creator_id = creator_id
        self.view = view
        self.topic_input = TextInput(label="투표 주제", placeholder="투표할 주제를 입력하세요")
        self.add_item(self.topic_input)

    async def on_submit(self, interaction: discord.Interaction):
        """주제 입력 후 Embed 업데이트"""
        self.view.topic = self.topic_input.value.strip()
        await interaction.response.edit_message(embed=self.view.generate_embed(), view=self.view)


class OptionInputModal(discord.ui.Modal):
    """투표 항목 추가 Modal"""
    def __init__(self, creator_id, view: PollCreationView):
        super().__init__(title="➕ 투표 항목 추가")
        self.creator_id = creator_id
        self.view = view
        self.option_input = TextInput(label="새 항목", placeholder="추가할 항목을 입력하세요")
        self.add_item(self.option_input)

    async def on_submit(self, interaction: discord.Interaction):
        """항목 입력 후 Embed 업데이트"""
        new_option = self.option_input.value.strip()
        if new_option in self.view.options:
            await interaction.response.send_message("❌ 이미 존재하는 항목입니다.", ephemeral=True)
            return
        self.view.options.append(new_option)
        await interaction.response.edit_message(embed=self.view.generate_embed(), view=self.view)


class SetPollDurationView(View):
    """투표 마감 시간 설정 UI"""
    def __init__(self, creator_id):
        super().__init__()
        self.creator_id = creator_id
        self.date = None
        self.time = None

    @discord.ui.button(label="날짜 입력", style=discord.ButtonStyle.primary)
    async def enter_date(self, interaction: discord.Interaction, button: discord.ui.Button):
        """마감 날짜 입력"""
        modal = DateInputModal(self.creator_id, self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="시간 입력", style=discord.ButtonStyle.primary)
    async def enter_time(self, interaction: discord.Interaction, button: discord.ui.Button):
        """마감 시간 입력"""
        modal = TimeInputModal(self.creator_id, self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="투표 시작", style=discord.ButtonStyle.success)
    async def confirm_poll(self, interaction: discord.Interaction, button: discord.ui.Button):
        """투표 시작"""
        if not self.date or not self.time:
            await interaction.response.send_message("❌ 날짜와 시간을 모두 입력해주세요.", ephemeral=True)
            return

        end_time = datetime.strptime(f"{self.date} {self.time}", "%Y-%m-%d %H:%M")
        active_polls[self.creator_id]["is_active"] = True
        active_polls[self.creator_id]["end_time"] = end_time

        await interaction.response.send_message(
            f"✅ 투표가 시작되었습니다! ⏳ 마감: {end_time.strftime('%Y-%m-%d %H:%M')}",
            ephemeral=True
        )


class DateInputModal(discord.ui.Modal):
    """투표 마감 날짜 입력 Modal"""
    def __init__(self, creator_id, view: SetPollDurationView):
        super().__init__(title="📅 마감 날짜 입력")
        self.creator_id = creator_id
        self.view = view
        self.date_input = TextInput(label="마감 날짜 (YYYY-MM-DD)", placeholder="예: 2025-01-20")
        self.add_item(self.date_input)

    async def on_submit(self, interaction: discord.Interaction):
        """날짜 저장"""
        self.view.date = self.date_input.value.strip()
        await interaction.response.send_message("✅ 날짜가 설정되었습니다.", ephemeral=True)


class TimeInputModal(discord.ui.Modal):
    """투표 마감 시간 입력 Modal"""
    def __init__(self, creator_id, view: SetPollDurationView):
        super().__init__(title="⏰ 마감 시간 입력")
        self.creator_id = creator_id
        self.view = view
        self.time_input = TextInput(label="마감 시간 (HH:MM)", placeholder="예: 18:30")
        self.add_item(self.time_input)

    async def on_submit(self, interaction: discord.Interaction):
        """시간 저장"""
        self.view.time = self.time_input.value.strip()
        await interaction.response.send_message("✅ 시간이 설정되었습니다.", ephemeral=True)


@bot.command(name="투표만들기")
async def create_poll(ctx):
    """투표 생성"""
    await ctx.author.send(f"{ctx.author.mention}, 🗳️ 투표를 생성하려면 아래 버튼을 클릭하세요.", view=PollCreationView(ctx.author.id), ephemeral=True)


bot.run(TOKEN)
