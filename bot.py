#pip install PyNaCl
import os
import time
import random
import json
from datetime import datetime #pip install DateTime
import discord #pip install discord
import aiocron #pip install aiocron
from discord.ext import commands #pip install discord-ext-bot
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_API=os.getenv("DISCORD_API")
statistics={}
save_on=False
guild_id=834134184486371339


class cronjobs():
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        @aiocron.crontab('37 21 * * *')
        async def alert():
            global statistics
            channel=bot.get_channel(834134184917729309)
            await channel.send("21:37")
            channel=bot.get_channel(834134184917729304)
            members=len(channel.voice_states)
            if members>0:
                await channel.connect()
                voice=discord.utils.get(bot.voice_clients)
                voice.play(discord.FFmpegPCMAudio("audio/Alert2137.mp3"))
                time.sleep(8)
                await voice.disconnect()
                if "alert" not in statistics:
                    statistics["alert"]=1
                else:
                    statistics["alert"]+=1
        @aiocron.crontab('*/1 * * * *')
        async def save():
            global statistics
            global save_on
            if save_on:
                with open('data.json', 'w') as json_file:
                    json.dump(statistics, json_file, indent=4, sort_keys=True)
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{now} INFO     bot.py saved")
                #print(statistics)

class Bot(commands.Bot):
    def __init__(self):
        intents=discord.Intents.all()
        intents.message_content=True
        intents.members=True
        super().__init__(command_prefix="`",intents=intents,help_command=None)

    async def setup_hook(self):

        cron=cronjobs(self)
        global statistics
        global save_on
        dict1={"alert":0,
                "help":0,
                "hulp":0,
                "jasny":0,
                "kurwa":{},
                "pong":0,
                "error_404":0,}
        with open('data.json', 'r') as f:
            dict2=json.load(f)
        statistics=dict1|dict2
        print(statistics)
        print("We have logged in as {0.user}".format(self))
        save_on=True

        await self.tree.sync(guild=discord.Object(id=guild_id))
        print(f"Synced slash commands for {self.user}.")

    async def on_command_error(self,ctx,error):
        global statistics
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Error 404")
            statistics["error_404"]+=1
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"{round(error.retry_after, 2)} seconds left :)")

    async def on_voice_state_update(self,member,before, after):
        #uno function
        member_id=981651571442069625
        guild=self.get_guild(834134184486371339)
        if member.id==member_id:
            #mute
            if not (before.mute) and after.mute:
                async for entry in guild.audit_logs(limit=1,action=discord.AuditLogAction.member_update):
                    print('{0.user} did {0.action}: mute to {0.target}'.format(entry))
                    if not entry.user==member:
                        await member.edit(mute=False)
                        await entry.user.edit(mute=True)
            #deaf    
            if not (before.deaf) and after.deaf:
                async for entry in guild.audit_logs(limit=1,action=discord.AuditLogAction.member_update):
                    print('{0.user} did {0.action}: deaf to {0.target}'.format(entry))
                    if not entry.user==member:
                        await member.edit(deafen=False)
                        await entry.user.edit(deafen=True)

bot=Bot()

#events
@bot.event
async def on_ready():
    activity=discord.Game(name="2.0.0.1")
    await bot.change_presence(status=discord.Status.online, activity=activity)


#commands
@bot.hybrid_command(name="ping",with_app_command=True,description="pong!")
@app_commands.guilds(discord.Object(id=guild_id))
async def ping(ctx):
    await ctx.send("pong!")
    if "pong" not in statistics:
        statistics["pong"]=1
    else:
        statistics["pong"]+=1
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now} INFO     bot.py {ctx.message.author} use /ping")

@bot.hybrid_command(name="jojn",with_app_command=True,description="jojn na kanał :D")
@app_commands.guilds(discord.Object(id=guild_id))
async def jojn(ctx,channel_id=834134184917729304):
    await ctx.defer(ephemeral = True)
    await ctx.send("Starting jojning procedure")
    channel=bot.get_channel(channel_id)
    await channel.connect()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now} INFO     bot.py {ctx.message.author} use /jojn to {channel_id}")

@bot.hybrid_command(name="sio",with_app_command=True,description="waćpan się oddal")
@app_commands.guilds(discord.Object(id=guild_id))
async def sio(ctx):
    await ctx.defer(ephemeral = True)
    voice=discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await voice.disconnect(force=True)
    await ctx.send("Roger Roger")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now} INFO     bot.py {ctx.message.author} use /sio")

@bot.hybrid_command(name="jasny",with_app_command=True,description="jasny, bardzo jasny")
@app_commands.guilds(discord.Object(id=guild_id))
async def jasny(ctx, seed=0):
    global statistics
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{now} INFO     bot.py {ctx.message.author} use /jasny {seed}")
        if seed>=0 and seed<=4:
            if seed==0:
                seed= random.randint(1,4)
            await channel.connect()
            await ctx.send(f'playing file jasnychuj_{seed}, Enjoy :D')
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            if voice.is_connected():
                if seed==1:
                    voice.play(discord.FFmpegPCMAudio("audio/JasnyChuj/Jasnychuj.mp3"))
                    time.sleep(2)
                elif seed==2:
                    voice.play(discord.FFmpegPCMAudio("audio/JasnyChuj/Jasnychujv2.mp3"))
                    time.sleep(9)
                elif seed==3:
                    voice.play(discord.FFmpegPCMAudio("audio/JasnyChuj/jasnychujv3.mp3"))
                    time.sleep(2)
                elif seed==4:
                    voice.play(discord.FFmpegPCMAudio("audio/JasnyChuj/Jasnychujv4.mp3"))
                    time.sleep(3)
            await voice.disconnect()

            if "jasny" not in statistics:
                statistics["jasny"]=1
            else:
                statistics["jasny"]+=1

        else:
            await ctx.send("invalid parameter")
    else:
        await ctx.send("join to voice channel first")

@bot.hybrid_command(name="hulp",with_app_command=True,description="więcej pomocy")
@app_commands.guilds(discord.Object(id=guild_id))
async def hulp(ctx):
    await ctx.defer(ephemeral = True)
    await ctx.send("https://pacjent.gov.pl/aktualnosc/jak-pomoc-sobie-i-innym-w-depresji")

    if "hulp" not in statistics:
        statistics["hulp"]=1
    else:
        statistics["hulp"]+=1

@bot.hybrid_command(name="kurwa",with_app_command=True,description="używać w przypadku głuchoty jakiegoś uczestnika rozmowy")
@app_commands.guilds(discord.Object(id=guild_id))
@commands.cooldown(1, 60, commands.BucketType.guild)
async def kurwa(ctx,user: discord.Member=None):
    global statistics
    if user is None:
        user=bot.get_guild(834134184486371339).get_member(689167522859188294)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now} INFO     bot.py {ctx.message.author} use /kurwa on {user}")

    if user.voice is None:
        return await ctx.send(f"{user.mention} is not present on any voice channel")

    if user==bot.get_guild(834134184486371339).get_member(328112220712075265):
        if ctx.message.author.id==328112220712075265:
            await ctx.send("Man WTF!?")
            return
        user=ctx.message.author

    if "kurwa" not in statistics:
        statistics["kurwa"]={}
    if str(user) not in statistics["kurwa"]:
        statistics["kurwa"][str(user)]=1
    else:
        statistics["kurwa"][str(user)]+=1

    await ctx.send(f"KURWA {user.mention}!!!")

    channels=(834134184917729302,
                834134184917729304,
                834134184917729305,
                834134184917729306,
                834134184917729307)
    index = channels.index(user.voice.channel.id)
    
    for i in range(index,len(channels)):
        channel=bot.get_channel(channels[i])
        await user.move_to(channel)
    for i in range(len(channels)-1,0,-1):
        channel=bot.get_channel(channels[i])
        await user.move_to(channel)
    for i in range(0,index+1):
        channel=bot.get_channel(channels[i])
        await user.move_to(channel)

@bot.hybrid_command(name="stats",with_app_command=True,description="wyświetla efekty inwigilacji :)")
@app_commands.guilds(discord.Object(id=guild_id))
async def stats(ctx):
    global statistics
    text="""
Alert 2137: {alert} 
help: {help} 
hulp: {hulp}
jasny: {jasny}
pong!: {pong}
Error 404: {error_404}
kurwa:
""".format(**statistics)
    for k,v in statistics["kurwa"].items():
        text+=f"""   {k}: {v}\n"""
    await ctx.send(text)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now} INFO     bot.py {ctx.message.author} use /stats")

@bot.hybrid_command(name="help",with_app_command=True,description="pomoc")
@app_commands.guilds(discord.Object(id=guild_id))
async def help(ctx):
    global statistics
    await ctx.defer(ephemeral = True)
    text="""```
Wszystkie znane komendy:

  /help - TO
  /hulp - więcej pomocy
  /jasny - bardo jasny
  /jojn - na kanał
  /kurwa - używać w przypadku głuchoty jakiegoś uczestnika rozmowy
  /ping - pong
  /sio - waćpan się oddal
  /stats - raport z inwigilacji :)```"""
    await ctx.send(text)
    if "help" not in statistics:
        statistics["help"]=1
    else:
        statistics["help"]+=1  


#developer commands
@bot.hybrid_command(name="test",with_app_command=True,description="test")
@app_commands.guilds(discord.Object(id=guild_id))
@commands.is_owner()
async def test(ctx,user: discord.Member):
    await ctx.send(f"{datetime.now()}")


bot.run(DISCORD_API)

#Patryś 1
#Toster 1

#ps -ef | grep python3