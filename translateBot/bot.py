import discord, ffmpeg, requests
from gtts import gTTS
from discord.ext import commands
from city import City

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Bot is online")

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()
    
async def text2Speech(language,text,ctx,channel):
    myText = text
    language = language
    output = gTTS(text=myText,lang=language,slow=False)
    output.save("output.mp3")
    #if not connected
    if ctx.voice_client is None:
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio('output.mp3'))
    else:
        ctx.voice_client.play(discord.FFmpegPCMAudio('output.mp3'))
    
@bot.command(name='t')
async def t2s(ctx,arg1,arg2):
    channel = ctx.author.voice.channel
    await text2Speech(arg1,arg2,ctx,channel)
    #await ctx.send("Lang is {} and the sentence is:  {} ".format(arg1,arg2))

@bot.command(name='w')
async def weather(ctx,city):
    city = City(city)
    strCity = city.getData()
    print(strCity)
    await ctx.send(strCity)

bot.run(token)
