import discord, ffmpeg, requests, sys, youtube_dl, os
import urllib.parse, urllib.request, re
from gtts import gTTS
from discord.ext import commands
from city import City

bot = commands.Bot(command_prefix="!")
bot.remove_command('help')
@bot.event
async def on_ready():
    print("Bot is online")

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour = discord.Colour.orange()
    )
    embed.set_author(name='List of Commands')
    embed.add_field(name='!join',value='joins voice channel',inline=False)
    embed.add_field(name='!leave',value='leaves voice channel',inline=False)
    embed.add_field(name='!t <language> <sentence>', value='reads a sentence in desired language',inline=False)
    embed.add_field(name='!w <city>',value='shows the weather and temperature',inline=False)
    embed.add_field(name='!f <language> <city>', value='reads weather forecast to the voice channel',inline=False)
    await ctx.send(author,embed=embed)

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

@bot.command(name='f')
async def weather(ctx,language,name):
    channel = ctx.author.voice.channel
    city = City(name)
    data = city.getData()
    if language == "en":
        await text2Speech(language,data,ctx,channel)
    elif language == "tr":
        data = city.getName() + " şehrinde hava " + str(city.convert(city.getTemp())) + "derece."
        await text2Speech(language,data,ctx,channel)

@bot.command(name='p')
async def youtube(ctx,*,search):
    query_string = urllib.parse.urlencode( {
        'search_query':search
    })

    htm_content = urllib.request.urlopen (
        'http://www.youtube.com/results?' + query_string
    )
    search_results = re.findall('href=\"\\/watch\\?v=(.{11})',htm_content.read().decode())
    url = 'http://www.youtube.com/watch?v='+search_results[0]
    await ctx.send(url)
    await play(ctx,url)
    
async def play(ctx,url):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music end or use the 'stop' command")
        return
    await ctx.send("Getting everything ready, playing audio soon")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3") and not file.startswith("output"):
            os.rename(file, 'song.mp3')

    if ctx.voice_client is None:
        vc = await ctx.author.voice.channel.connect()
        vc.play(discord.FFmpegPCMAudio("song.mp3"))
    else:
        ctx.voice_client.play(discord.FFmpegPCMAudio("song.mp3"))


bot.run("NjgyMjk3MDEzMTczNDg1NTgx.Xla8pA.ZEVEqEPM6qSPr8weYy8HG7LgAdo")
