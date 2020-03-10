import discord, ffmpeg, requests, sys
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
async def t2s(ctx,*argv):
    channel = ctx.author.voice.channel
    text = ""
    for i in range(1,len(argv)):
        text += argv[i]
    language = argv[0]
    await text2Speech(language,text,ctx,channel)
    #await ctx.send("Lang is {} and the sentence is:  {} ".format(arg1,arg2))

@bot.command(name='w')
async def weather(ctx,city):
    city = City(city)
    strCity = city.getData()
    await ctx.send(strCity)

@bot.command(name='fcast')
async def weather(ctx,language,name):
    channel = ctx.author.voice.channel
    city = City(name)
    data = city.getData()
    if language == "en":
        await text2Speech(language,data,ctx,channel)
    elif language == "tr":
        data = city.getName() + " şehrinde hava " + str(city.convert(city.getTemp())) + "derece."
        await text2Speech(language,data,ctx,channel)

bot.run("NjgyMjk3MDEzMTczNDg1NTgx.Xla8pA.ZEVEqEPM6qSPr8weYy8HG7LgAdo")
