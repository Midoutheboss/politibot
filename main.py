### message lro7i, matgl3ch les commentaire bach matnsach kol command w cha ydir

import discord
import random
import sqlite3
import os
from discord import app_commands
from discord.ext import commands as cdm

intents = discord.Intents.all()
token = os.getenv("TOKEN")

bot = cdm.Bot(command_prefix=">", intents=intents)

# region DATABASE
conn = sqlite3.connect("economy.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    coins INTEGER
)
""")

# BALLS DATABASE

cursor.execute("""
CREATE TABLE IF NOT EXISTS guild_settings (
    guild_id INTEGER PRIMARY KEY,
    channel_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS collections (
    user_id INTEGER,
    ball_name TEXT,
    PRIMARY KEY (user_id, ball_name)
)
""")

#money and tax database
cursor.execute("""
CREATE TABLE IF NOT EXISTS guild_economy (
    guild_id INTEGER PRIMARY KEY,
    treasury INTEGER DEFAULT 0,
    tax_rate REAL DEFAULT 0
)
""")

# Ensure warning_limits table exists at startup
cursor.execute("""
CREATE TABLE IF NOT EXISTS warning_limits (
    guild_id INTEGER PRIMARY KEY,
    term_limit INTEGER
)
""")

conn.commit()
# warnings table (for moderation)
cursor.execute("""
CREATE TABLE IF NOT EXISTS warnings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    guild_id INTEGER,
    reason TEXT
)
""")
conn.commit()
#endregion

#region vote view
class VoteView(discord.ui.View):
    def __init__(self, question, author):
        super().__init__(timeout=300)  # vote duration
        self.question = question
        self.author = author

        self.aye = 0
        self.nay = 0
        self.abstain = 0

        self.voters = set()

    def get_embed(self):
        embed = discord.Embed(
            title="🗳️ Vote",
            description=self.question,
            color=discord.Color.blurple()
        )

        embed.add_field(name="🟢 Aye", value=str(self.aye))
        embed.add_field(name="🔴 Nay", value=str(self.nay))
        embed.add_field(name="⚪ Abstain", value=str(self.abstain))

        embed.set_footer(text=f"Started by {self.author}")
        return embed

    async def update_message(self, interaction):
        await interaction.message.edit(embed=self.get_embed(), view=self)

    #buttonss

    @discord.ui.button(label="Aye", style=discord.ButtonStyle.green)
    async def aye_button(self, interaction: discord.Interaction, _button: discord.ui.Button):
        if interaction.user.id in self.voters:
            await interaction.response.send_message("You already voted!", ephemeral=True)
            return

        self.voters.add(interaction.user.id)
        self.aye += 1

        await interaction.response.defer()
        await self.update_message(interaction)

    @discord.ui.button(label="Nay", style=discord.ButtonStyle.red)
    async def nay_button(self, interaction: discord.Interaction, _button: discord.ui.Button):
        if interaction.user.id in self.voters:
            await interaction.response.send_message("You already voted!", ephemeral=True)
            return

        self.voters.add(interaction.user.id)
        self.nay += 1

        await interaction.response.defer()
        await self.update_message(interaction)

    @discord.ui.button(label="Abstain", style=discord.ButtonStyle.gray)
    async def abstain_button(self, interaction: discord.Interaction, _button: discord.ui.Button):
        if interaction.user.id in self.voters:
            await interaction.response.send_message("You already voted!", ephemeral=True)
            return

        self.voters.add(interaction.user.id)
        self.abstain += 1

        await interaction.response.defer()
        await self.update_message(interaction)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        result = "PASSED ✅" if self.aye > self.nay else "REJECTED ❌"

        embed = self.get_embed()
        embed.add_field(name="Result", value=result, inline=False)

        self.message = getattr(self, "message", None)
        if self.message:
            await self.message.edit(embed=embed, view=self)
#endregion

#region like button (for twitter command color is red and it adds a like count to the embed)
class LikeButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Like", style=discord.ButtonStyle.red)
        self.likes = 0

    async def callback(self, interaction: discord.Interaction):
        self.likes += 1
        self.label = f"Like ({self.likes})"
        await interaction.response.edit_message(view=self.view)
#endregion

#region punches
punches = [
    "https://media1.tenor.com/m/54vXJe6Jj3kAAAAd/spy-family-spy-x-family.gif",
    "https://media1.tenor.com/m/b0ZXAm867pYAAAAd/jujutsu-kaisen-season-3.gif",
    "https://media1.tenor.com/m/ markiplier-gif-25538262",
    "https://media1.tenor.com/m/terminator-gut-punch-gif-10746852"
]
#endregion

#region balls
balls = {
    "the authority":"https://cdn.discordapp.com/attachments/1428200557964824586/1428206923102031965/Flag_of_The_Authority.svg.png?ex=69cfcd99&is=69ce7c19&hm=ff01b0fde493bd412f244e2da89fc4017010bf64fb39fdd8cd4e845a5a5d47b8&",
    "Algeria": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Flag_of_Algeria.svg/800px-Flag_of_Algeria.png",
    "France": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c3/Flag_of_France.svg/800px-Flag_of_France.png",
    "Germany": "https://upload.wikimedia.org/wikipedia/en/thumb/b/ba/Flag_of_Germany.svg/800px-Flag_of_Germany.png",
    "RBS":"https://cdn.discordapp.com/attachments/1203785283112276078/1489270094801404078/0007d35a805f67afa28576247f542864.png?ex=69cfce5b&is=69ce7cdb&hm=bbb8c942535eadff3d90fe702a390c5feab4a21bfbb139ca358a4addc1379adb&",
    "parthenope":"https://cdn.discordapp.com/attachments/1203785283112276078/1489276829297807533/Senza_titolo_1062_20260216002948.png?ex=69cfd4a1&is=69ce8321&hm=78eeeb9ff537a5703f7a0337c0edd77457fc1735a4bf3ef6ecdeedb93ff1123c&",
    "OMSK":"https://cdn.discordapp.com/attachments/1203785283112276078/1489276650213347349/Balls.png?ex=69cfd476&is=69ce82f6&hm=bd0806cb745e2cc665547670aadbc5fd89650f6cb93a78b8d72c2a30c3d80bf5&",
    "malaysia":"https://cdn.discordapp.com/attachments/1489273816827039804/1489276568885919865/WhatsApp_Image_2026-02-18_at_20.54.06.jpeg?ex=69cfd463&is=69ce82e3&hm=21467ff7f64e82feb3a660448698682c1fa0c35d2ae3a367fdcd60f87412095a&",
    "christmass Authority":"https://cdn.discordapp.com/attachments/1203785283112276078/1489270200783208479/The_Authority.png?ex=69cfce75&is=69ce7cf5&hm=4d5fb1860d654adce9b503848d5b90ec250508b612a7e95150e6977e28051d30&"
}
#endregion

def roulette_number():
    return random.randint(0, 36)

def roulette_color():
    col = random.choice(["red", "black"])
    return col



#================================================================================================================================

@bot.event
async def on_ready():
    print("online")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
        print([cmd.name for cmd in bot.tree.get_commands()])
    except Exception as e:
        print(e)



#info command
@bot.tree.command(name="info", description="information about the bot")
async def info(interaction: discord.Interaction):
    await interaction.response.send_message(
        "this bot was made by Midou, it is still in development, it aims to be a standard mock government bot."
    )

#region number guess command
@bot.tree.command(name="number_guess", description="guess a number between 1 and 50")
@app_commands.describe(guess="Your guess (1-50)")
async def number_guess(interaction: discord.Interaction, guess: int):
    number = random.randint(1, 50)

    if guess == number:
        await interaction.response.send_message("🎉 Congratulations! You guessed correctly!")
    else:
        await interaction.response.send_message(f"❌ Wrong! The number was {number}")

#endregion

#region work command
@bot.tree.command(name="work", description="Earn coins")
async def work(interaction: discord.Interaction):
    user_id = interaction.user.id

    cursor.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result is None:
        coins = 0
        cursor.execute("INSERT INTO users (user_id, coins) VALUES (?, ?)", (user_id, coins))
    else:
        coins = result[0]

    earnings = random.randint(10, 50)

    guild_id = interaction.guild.id

    cursor.execute("SELECT tax_rate, treasury FROM guild_economy WHERE guild_id = ?", (guild_id,))
    result_tax = cursor.fetchone()

    if result_tax:
        tax_rate, treasury = result_tax
    else:
        tax_rate = 0
        treasury = 0
        cursor.execute("INSERT INTO guild_economy (guild_id, treasury, tax_rate) VALUES (?, 0, 0)", (guild_id,))

    tax_amount = int(earnings * (tax_rate / 100))
    final_earnings = earnings - tax_amount

    coins += final_earnings

    # update treasury
    treasury += tax_amount

    cursor.execute("UPDATE guild_economy SET treasury = ? WHERE guild_id = ?", (treasury, guild_id))

    cursor.execute("UPDATE users SET coins = ? WHERE user_id = ?", (coins, user_id))
    conn.commit()

    embed = discord.Embed(
        title="💼 Work",
        description=f"You earned **{earnings} coins**!",
        color=discord.Color.green()
    )

    embed.add_field(name="Total Coins", value=str(coins))

    await interaction.response.send_message(embed=embed)
#endregion


#region profile command
@bot.tree.command(name="profile", description="View your profile")
async def profile(interaction: discord.Interaction):
    user = interaction.user
    user_id = user.id

    cursor.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    coins = result[0] if result else 0

    #njib rank ml database
    cursor.execute("SELECT COUNT(*) FROM users WHERE coins > ?", (coins,))
    rank = cursor.fetchone()[0] + 1

    
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    
    embed = discord.Embed(
        title=f"{user.name}'s Profile",
        color=discord.Color.blue()
    )

    embed.set_thumbnail(url=user.display_avatar.url)

    embed.add_field(name="💰 Coins", value=str(coins), inline=True)
    embed.add_field(name="🏆 Rank", value=f"#{rank} / {total_users}", inline=True)

    await interaction.response.send_message(embed=embed)
#endregion

#region mockgov wiki command
@bot.tree.command(name="mockgov-wiki", description="gives you a link to the mock government wiki")
async def mockgov_wiki(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Here is the link to the Mock Government Wiki: https://mockgovernments.com/wiki/Main_Page"
    )

#leaderboard command
@bot.tree.command(name="leaderboard", description="View top richest users")
async def leaderboard(interaction: discord.Interaction):
    cursor.execute("SELECT user_id, coins FROM users ORDER BY coins DESC LIMIT 10")
    results = cursor.fetchall()

    embed = discord.Embed(
        title="🏆 Leaderboard",
        description="Top 10 richest users",
        color=discord.Color.gold()
    )

    if not results:
        embed.description = "No data yet."
        await interaction.response.send_message(embed=embed)
        return

    leaderboard_text = ""

    for i, (user_id, coins) in enumerate(results, start=1):
        user = bot.get_user(user_id) or await bot.fetch_user(user_id)

        leaderboard_text += f"**{i}. {user.name}** — {coins} coins\n"

    embed.description = leaderboard_text

    await interaction.response.send_message(embed=embed)


#region punch command
@bot.tree.command(name="punch", description="punch someone")
@app_commands.describe(target="The user you want to target")
async def action(interaction: discord.Interaction, target: discord.Member):

    embed = discord.Embed(
        title=f"{target.name}",
        description=f"{interaction.user.mention} punched {target.mention}",
        color=discord.Color.purple()
    )

    embed.set_image(url=random.choice(punches))

    await interaction.response.send_message(embed=embed)

#vote command
@bot.tree.command(name="vote", description="Start a vote")
@app_commands.describe(question="The question to vote on")
async def vote(interaction: discord.Interaction, question: str):

    view = VoteView(question, interaction.user.name)
    embed = view.get_embed()

    await interaction.response.send_message(embed=embed, view=view)
    msg = await interaction.original_response()
    view.message = msg


# region ball spawn setup command
@bot.tree.command(name="mockgovball-setup", description="Set spawn channel")
async def setup(interaction: discord.Interaction, channel: discord.TextChannel):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need admin permissions", ephemeral=True)
        return

    guild_id = interaction.guild.id

    cursor.execute("""
    INSERT OR REPLACE INTO guild_settings (guild_id, channel_id)
    VALUES (?, ?)
    """, (guild_id, channel.id))

    conn.commit()

    await interaction.response.send_message(f"Spawn channel set to {channel.mention}")




# region message counter for ball spawn
message_count = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    guild_id = message.guild.id

    message_count[guild_id] = message_count.get(guild_id, 0) + 1

    if message_count[guild_id] >= 5:
        message_count[guild_id] = 0
        await spawn_ball(message.channel, guild_id)

    await bot.process_commands(message)


#region ball spawn function
async def spawn_ball(_channel, guild_id):

    cursor.execute("SELECT channel_id FROM guild_settings WHERE guild_id = ?", (guild_id,))
    result = cursor.fetchone()

    if not result:
        return

    channel_id = result[0]
    spawn_channel = bot.get_channel(channel_id)

    if not spawn_channel:
        return

    name, image = random.choice(list(balls.items()))

    view = GuessView(name)

    embed = discord.Embed(
        title="🌍 A wild MockGovBall appeared!",
        description="Click the button and guess its name!",
        color=discord.Color.random()
    )

    embed.set_image(url=image)

    msg = await spawn_channel.send(embed=embed, view=view)
    view.message = msg


# region guess model for balls
class GuessModal(discord.ui.Modal, title="Guess the Ball"):
    answer = discord.ui.TextInput(label="Your guess")

    def __init__(self, correct_name, view):
        super().__init__()
        self.correct_name = correct_name.lower()
        self.view = view

    async def on_submit(self, interaction: discord.Interaction):
        guess = self.answer.value.lower()

        if guess == self.correct_name:
            user_id = interaction.user.id

            cursor.execute("""
            INSERT OR IGNORE INTO collections (user_id, ball_name)
            VALUES (?, ?)
            """, (user_id, self.correct_name))

            conn.commit()

            await interaction.response.send_message(f"Correct! {interaction.user.mention} collected it")

            for item in self.view.children:
                item.disabled = True

            await self.view.message.edit(view=self.view)

        else:
            await interaction.response.send_message("❌ Wrong guess!", ephemeral=True)


class GuessView(discord.ui.View):
    def __init__(self, correct_name):
        super().__init__(timeout=120)
        self.correct_name = correct_name
        self.message = None

    @discord.ui.button(label="Guess", style=discord.ButtonStyle.primary)
    async def guess_button(self, interaction: discord.Interaction, _button: discord.ui.Button):
        modal = GuessModal(self.correct_name, self)
        await interaction.response.send_modal(modal)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        if self.message:
            await self.message.edit(view=self)


@bot.tree.command(name="collection", description="View your collection")
async def collection(interaction: discord.Interaction):

    user_id = interaction.user.id

    cursor.execute("SELECT ball_name FROM collections WHERE user_id = ?", (user_id,))
    results = cursor.fetchall()

    if not results:
        await interaction.response.send_message("You have no balls yet!")
        return

    names = [r[0] for r in results]

    embed = discord.Embed(
        title=f"{interaction.user.name}'s Collection",
        description="\n".join(names),
        color=discord.Color.blue()
    )

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="set-tax", description="Set server tax rate (percentage)")
@app_commands.describe(rate="Tax rate (0-100)")
async def set_tax(interaction: discord.Interaction, rate: float):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need admin permissions!", ephemeral=True)
        return

    if rate < 0 or rate > 25:
        await interaction.response.send_message("Tax must be between 0 and 25.", ephemeral=True)
        return

    guild_id = interaction.guild.id

    cursor.execute("""
    INSERT OR IGNORE INTO guild_economy (guild_id, treasury, tax_rate)
    VALUES (?, 0, 0)
    """, (guild_id,))

    cursor.execute("""
    UPDATE guild_economy SET tax_rate = ? WHERE guild_id = ?
    """, (rate, guild_id))

    conn.commit()

    await interaction.response.send_message(f"Tax rate set to {rate}%")

#region treasury command
@bot.tree.command(name="treasury", description="View server treasury")
async def treasury(interaction: discord.Interaction):

    guild_id = interaction.guild.id

    cursor.execute("SELECT treasury, tax_rate FROM guild_economy WHERE guild_id = ?", (guild_id,))
    result = cursor.fetchone()

    if not result:
        treasury = 0
        tax_rate = 0
    else:
        treasury, tax_rate = result

    embed = discord.Embed(
        title="🏦 Server Treasury",
        color=discord.Color.gold()
    )

    embed.add_field(name="💰 Treasury", value=str(treasury))
    embed.add_field(name="📊 Tax Rate", value=f"{tax_rate}%")

    await interaction.response.send_message(embed=embed)


#region roulette command
@bot.tree.command(name="roulette", description="Play roulette")
@app_commands.describe(amount="Gamble an amount of coins")
@app_commands.describe(color="Bet on a color (red or black)")
@app_commands.choices(color=[
    app_commands.Choice(name="Red", value="red"),
    app_commands.Choice(name="Black", value="black")
])
@app_commands.describe(number="Bet on a number (0-36)")
@app_commands.checks.cooldown(1, 30, key=lambda i: (i.guild_id, i.user.id))
async def roulette(interaction: discord.Interaction, amount: int, color: str, number: int):
    correct_number = roulette_number()
    correct_color = roulette_color()
    if amount <= 0:
        await interaction.response.send_message("Amount must be greater than 0.", ephemeral=True)
        return
    user_id = interaction.user.id
    cursor.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    coins = result[0] if result else 0
    if amount > coins:
        await interaction.response.send_message("You don't have enough coins!", ephemeral=True)
        return
    
    #remove coins
    coins -= amount
    cursor.execute("UPDATE users SET coins = ? WHERE user_id = ?", (coins, user_id))
    conn.commit()
    
    winnings = 0
    if color == correct_color:
        winnings += amount * 2
    if number == correct_number:
        winnings += amount * 4
    
    #add winnings
    coins += winnings
    cursor.execute("UPDATE users SET coins = ? WHERE user_id = ?", (coins, user_id))
    conn.commit()

    embed = discord.Embed(
        title="🎰 Roulette Result",
        description=f"The ball landed on **{correct_number}** ({correct_color})! You {'won' if winnings > 0 else 'lost'} **{winnings} coins**.",
        color=discord.Color.random()

    )

    await interaction.response.send_message(embed=embed)

# region server info command
@bot.tree.command(name="server_info", description="View server information")
async def server_info(interaction: discord.Interaction):
    guild = interaction.guild

    embed = discord.Embed(
        title=f"{guild.name} Information",
        color=discord.Color.blue()
    )

    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

    embed.add_field(name="Created On", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
    embed.add_field(name="Members", value=str(guild.member_count), inline=True)

    await interaction.response.send_message(embed=embed)

#region daily server message count command
@bot.tree.command(name="message_count", description="View daily message count")
async def message_count_command(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    count = message_count.get(guild_id, 0)

    embed = discord.Embed(
        title="📊 Daily Message Count",
        description=f"Messages sent today: **{count}**",
        color=discord.Color.orange()
    )

    await interaction.response.send_message(embed=embed)



#region about us command
@bot.tree.command(name="about_us", description="learn about the bot")
async def about(interaction: discord.Interaction):
    await interaction.response.send_message(
        """This bot was created by Midou, a passionate developer and a mock government member.
          this bot aims to bring a unique and entertaining experience to every mock government server.
          our support server: https://discord.gg/3q5UBuwN9R"""
    )

#region warn command (needs admin permissions, saves the warning in the database, if a user gets set amount of warnings they get kicked)
@bot.tree.command(name="warn", description="Warn a user")
@app_commands.describe(target="The user to warn")
async def warn(interaction: discord.Interaction, target: discord.Member):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need admin permissions!", ephemeral=True)
        return

    cursor.execute("""
    INSERT INTO warnings (user_id, guild_id, reason)
    VALUES (?, ?, ?)
    """, (target.id, interaction.guild.id, "No reason provided"))
    conn.commit()
    #check if user has reached warning term_limit
    cursor.execute("SELECT COUNT(*) FROM warnings WHERE user_id = ? AND guild_id = ?", (target.id, interaction.guild.id))
    warning_count = cursor.fetchone()[0]
    cursor.execute("SELECT term_limit FROM warning_limits WHERE guild_id = ?", (interaction.guild.id,))
    result = cursor.fetchone()
    warning_term_limit = result[0] if result else 3
    await interaction.response.send_message(f"Warning issued to {target.mention}.")
    if warning_count >= warning_term_limit:
        try:
            await interaction.guild.kick(target, reason="Reached warning term_limit")
            cursor.execute("DELETE FROM warnings WHERE user_id = ? AND guild_id = ?", (target.id, interaction.guild.id))
            conn.commit()
            await interaction.channel.send(f"{target.mention} has been kicked for reaching the warning term_limit.")
        except discord.Forbidden:
            await interaction.response.send_message(f"Failed to kick {target.mention}: insufficient permissions.", ephemeral=True)
    if warning_count >= warning_term_limit:
        try:
            await interaction.guild.kick(target, reason="Reached warning term_limit")
            kicked = True
        except discord.Forbidden:
            kicked = False
            await interaction.response.send_message(f"Failed to kick {target.mention}: insufficient permissions.", ephemeral=True)
        except discord.HTTPException as e:
            kicked = False
            await interaction.response.send_message(f"Failed to kick {target.mention}: {e}", ephemeral=True)
        if kicked:
            cursor.execute("DELETE FROM warnings WHERE user_id = ? AND guild_id = ?", (target.id, interaction.guild.id))
            conn.commit()
            await interaction.channel.send(f"{target.mention} has been kicked for reaching the warning term_limit.")
            await interaction.channel.send(f"An error occurred while trying to kick {target.mention}: {e}")
        await interaction.guild.kick(target, reason="Reached warning term_limit")
        cursor.execute("DELETE FROM warnings WHERE user_id = ? AND guild_id = ?", (target.id, interaction.guild.id))
        conn.commit()
        await interaction.channel.send(f"{target.mention} has been kicked for reaching the warning term_limit.")


#region set warnings term_limit command
@bot.tree.command(name="set_warning_term_limit", description="Set the warning term_limit for kicking")
@app_commands.describe(term_limit="Number of warnings before kick")
async def set_warning_term_limit(interaction: discord.Interaction, term_limit: int):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need admin permissions!", ephemeral=True)
        return

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warning_term_limits (
        guild_id INTEGER PRIMARY KEY,
        term_limit INTEGER
    )
    """)
    conn.commit()

    cursor.execute("""
    INSERT OR REPLACE INTO warning_term_limits (guild_id, term_limit)
    VALUES (?, ?)
    """, (interaction.guild.id, term_limit))
    conn.commit()

    await interaction.response.send_message(
        f"Warning term_limit set to {term_limit}.\n"
        f"Users will be automatically kicked from the server if they reach this number of warnings."
    )

# region kick command (needs admin permissions, kicks a user and saves the reason in the database)

@bot.tree.command(name="kick", description="Kick a user")
@app_commands.describe(target="The user to kick")
@app_commands.describe(reason="Reason for the kick")
async def kick(interaction: discord.Interaction, target: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need admin permissions!", ephemeral=True)
        return

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kicks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        guild_id INTEGER,
        reason TEXT
    )
    """)
    conn.commit()

    await interaction.response.send_message(f"{target.mention} has been kicked. Reason: {reason}")
    cursor.execute("""
    INSERT INTO kicks (user_id, guild_id, reason)
    VALUES (?, ?, ?)
    """, (target.id, interaction.guild.id, reason))
    conn.commit()
    await target.kick(reason=reason)
@bot.tree.command(name="ban", description="Ban a user")
@app_commands.describe(target="The user to ban")
@app_commands.describe(reason="Reason for the ban")
async def ban(interaction: discord.Interaction, target: discord.Member, reason: str = "No reason provided"):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need admin permissions!", ephemeral=True)
        return

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        guild_id INTEGER,
        reason TEXT
    )
    """)
    conn.commit()

    await interaction.response.send_message(f"{target.mention} has been banned. Reason: {reason}")
    cursor.execute("""
    INSERT INTO bans (user_id, guild_id, reason)
    VALUES (?, ?, ?)
    """, (target.id, interaction.guild.id, reason))
    conn.commit()
    await target.ban(reason=reason)
@bot.tree.command(name="mute", description="Mute a user")
@app_commands.describe(target="The user to mute")
@app_commands.describe(duration="Duration of the mute in minutes")
async def mute(interaction: discord.Interaction, target: discord.Member, duration: int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need admin permissions!", ephemeral=True)
        return

    mute_role = discord.utils.get(interaction.guild.roles, name="Muted")
    if not mute_role:
        mute_role = await interaction.guild.create_role(name="Muted")

        for channel in interaction.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False, speak=False)

    await target.add_roles(mute_role, reason="Muted by admin")
    await interaction.response.send_message(f"{target.mention} has been muted for {duration} minutes.")

#region set mute role command (allows admins to set a specific role as the mute role)
@bot.tree.command(name="set_mute_role", description="Set the mute role")
@app_commands.describe(role="The role to use for muting")
async def set_mute_role(interaction: discord.Interaction, role: discord.Role):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need admin permissions!", ephemeral=True)
        return

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mute_roles (
        guild_id INTEGER PRIMARY KEY,
        role_id INTEGER
    )
    """)
    conn.commit()

    cursor.execute("""
    INSERT OR REPLACE INTO mute_roles (guild_id, role_id)
    VALUES (?, ?)
    """, (interaction.guild.id, role.id))
    conn.commit()

    await interaction.response.send_message(f"Mute role set to {role.mention}.")



#region logs command (logs moderation actions like warns and kicks in a channel, needs admin permissions)
@bot.tree.command(name="logs", description="View moderation logs")
async def logs(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need admin permissions!", ephemeral=True)
        return

    cursor.execute("""
    SELECT user_id, reason FROM kicks WHERE guild_id = ?
    """, (interaction.guild.id,))
    kicks = cursor.fetchall()

    cursor.execute("""
    SELECT user_id, reason FROM bans WHERE guild_id = ?
    """, (interaction.guild.id,))
    bans = cursor.fetchall()
    cursor.execute("""
    SELECT user_id, reason FROM warnings WHERE guild_id = ?
    """, (interaction.guild.id,))
    warnings = cursor.fetchall()
    embed = discord.Embed(
        title="Moderation Logs",
        color=discord.Color.red()
    )
    if not kicks and not bans and not warnings:
        embed.description = "No moderation actions logged yet."
        await interaction.response.send_message(embed=embed)
        return
    log_text = ""
    user_cache = {}

    async def get_user_cached(user_id):
        if user_id in user_cache:
            return user_cache[user_id]
        user = bot.get_user(user_id)
        if user is None:
            try:
                user = await bot.fetch_user(user_id)
            except Exception:
                user = None
        user_cache[user_id] = user
        return user

    for user_id, reason in kicks:
        user = await get_user_cached(user_id)
        user_name = user.name if user else f"User({user_id})"
        log_text += f"**Kick:** {user_name} - Reason: {reason}\n"
    for user_id, reason in bans:
        user = await get_user_cached(user_id)
        user_name = user.name if user else f"User({user_id})"
        log_text += f"**Ban:** {user_name} - Reason: {reason}\n"
    for user_id, reason in warnings:
        user = await get_user_cached(user_id)
        user_name = user.name if user else f"User({user_id})"
        log_text += f"**Warning:** {user_name} - Reason: {reason}\n"
    embed.description = log_text
    await interaction.response.send_message(embed=embed)
    user_name = user.name if user else f"User({user_id})"
    log_text += f"**Warning:** {user_name} - Reason: {reason}\n"
    embed.description = log_text
    await interaction.response.send_message(embed=embed)

#set up twitter channel command
@bot.tree.command(name="set_twitter_channel", description="Set the channel for twitter command")
@app_commands.describe(channel="The channel to use for twitter command")
async def set_twitter_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need admin permissions!", ephemeral=True)
        return

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS twitter_channels (
        guild_id INTEGER PRIMARY KEY,
        channel_id INTEGER
    )
    """)
    conn.commit()

    cursor.execute("""
    INSERT OR REPLACE INTO twitter_channels (guild_id, channel_id)
    VALUES (?, ?)
    """, (interaction.guild.id, channel.id))
    conn.commit()

    await interaction.response.send_message(f"Twitter channel set to {channel.mention}")

#twitter command (turns every message into a tweet Title: user Description: message with a gray background content Footer: timestamp + server name Thumbnail: avatar Color: dark theme (X-like) cooldown 10 seconds and ignores messages that are not in the specified channel and adds a like button that adds a like count to the embed)
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    guild_id = message.guild.id

    cursor.execute("SELECT channel_id FROM twitter_channels WHERE guild_id = ?", (guild_id,))
    result = cursor.fetchone()

    if not result:
        await bot.process_commands(message)
        return

    channel_id = result[0]

    if message.channel.id != channel_id:
        await bot.process_commands(message)
        return

    embed = discord.Embed(
        title=f"{message.author.name} tweeted:",
        description= message.content or "No content",
        color=discord.Color.blue(),
        timestamp=message.created_at
    )

    embed.set_footer(text=message.guild.name)
    embed.set_thumbnail(url=message.author.display_avatar.url)

    like_button = LikeButton()
    view = discord.ui.View()
    view.add_item(like_button)

    await message.channel.send(embed=embed, view=view)
    await message.delete()

#coin flip
@bot.tree.command(name="coin_flip", description="flip a coin")
async def coin_flip(interaction: discord.Interaction):
    result = random.choice(["Heads", "Tails"])
    await interaction.response.send_message(f"The coin landed on **{result}**!")


#blackjack command
@bot.tree.command(name="blackjack", description="Play a game of blackjack")
async def blackjack(interaction: discord.Interaction):
    await interaction.response.send_message("Blackjack is not implemented yet. im still testing it")

#coin flip pvp (two users bet on a coin flip)
@bot.tree.command(name="coin_flip_pvp", description="Challenge another user to a coin flip")
@app_commands.checks.cooldown(1, 60, key=lambda i: (i.guild_id, i.user.id))
@app_commands.describe(target="The user to challenge")
@app_commands.describe(amount="The amount of coins to bet")
async def coin_flip_pvp(interaction: discord.Interaction, target: discord.Member, amount: int):
    if target.bot:
        await interaction.response.send_message("You cannot challenge a bot!", ephemeral=True)
        return

    user_id = interaction.user.id
    target_id = target.id

    cursor.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    coins = result[0] if result else 0

    if amount <= 0:
        await interaction.response.send_message("Amount must be greater than 0.", ephemeral=True)
        return

    if amount > coins:
        await interaction.response.send_message("You don't have enough coins!", ephemeral=True)
        return

    cursor.execute("SELECT coins FROM users WHERE user_id = ?", (target_id,))
    result = cursor.fetchone()
    target_coins = result[0] if result else 0

    if amount > target_coins:
        await interaction.response.send_message(f"{target.mention} doesn't have enough coins!", ephemeral=True)
        return

    await interaction.response.send_message(f"{interaction.user.mention} has challenged {target.mention} to a coin flip for {amount} coins! Waiting for {target.mention} to accept...")


#confess command (allows users to confess something anonymously, the confession is sent to a specific channel that can be set up by admins)
@bot.tree.command(name="confess", description="Confess something anonymously")
@app_commands.describe(message="Your confession")
async def confess(interaction: discord.Interaction, message: str):
    guild_id = interaction.guild.id

    cursor.execute("SELECT channel_id FROM confession_channels WHERE guild_id = ?", (guild_id,))
    result = cursor.fetchone()

    if not result:
        await interaction.response.send_message("Confession channel is not set up yet.", ephemeral=True)
        return

    channel_id = result[0]
    confession_channel = bot.get_channel(channel_id)

    if not confession_channel:
        await interaction.response.send_message("Confession channel not found. Please ask an admin to set it up again.", ephemeral=True)
        return

    embed = discord.Embed(
        title="New Confession",
        description=message,
        color=discord.Color.dark_gray(),
        timestamp=interaction.created_at
    )

    embed.set_footer(text=f"Confession from {interaction.guild.name}")

    await confession_channel.send(embed=embed)
    await interaction.response.send_message("Your confession has been sent!", ephemeral=True)

#confession channel setup command
@bot.tree.command(name="confession_channel_setup", description="Set up the confession channel")
async def confession_channel_setup(interaction: discord.Interaction, channel: discord.TextChannel):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need admin permissions!", ephemeral=True)
        return

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS confession_channels (
        guild_id INTEGER PRIMARY KEY,
        channel_id INTEGER
    )
    """)
    conn.commit()

    cursor.execute("""
    INSERT OR REPLACE INTO confession_channels (guild_id, channel_id)
    VALUES (?, ?)
    """, (interaction.guild.id, channel.id))
    conn.commit()

    await interaction.response.send_message(f"Confession channel set to {channel.mention}.")



#region ping
@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    latency = bot.latency * 1000
    await interaction.response.send_message(f"Pong! Latency: {latency:.2f} ms")



bot.run(token)
