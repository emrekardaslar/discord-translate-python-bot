import os
import re
import urllib.parse
import urllib.request

import speech_recognition as sr
from gtts import gTTS

from bot_features.city import City
from bot_features.corona import Corona
from video import *
from yaml import safe_load

bot = commands.Bot(command_prefix="!")
bot.remove_command('help')
bot.add_cog(Music(bot))


@bot.event
async def on_ready():
    print("Bot is online")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))


@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(
        colour=discord.Colour.orange()
    )
    embed.set_author(name='List of Commands')
    embed.add_field(name='!join', value='Joins voice channel', inline=False)
    embed.add_field(name='!leave', value='Leaves voice channel', inline=False)
    embed.add_field(name='!t <language> <sentence>', value='Reads a sentence in desired language', inline=False)
    embed.add_field(name='!w <city>', value='Shows the weather and temperature', inline=False)
    embed.add_field(name='!f <language> <city>', value='Reads weather forecast to the voice channel', inline=False)
    embed.add_field(name='!play songname', value='Plays a song', inline=False)
    embed.add_field(name='!resume', value='Resumes the song', inline=False)
    embed.add_field(name='!pause', value='Pauses the song', inline=False)
    embed.add_field(name='!skip', value='Skips the song', inline=False)
    embed.add_field(name='!stop', value='Clears the queue', inline=False)
    embed.add_field(name='!queue', value='Shows the queue', inline=False)
    await ctx.send(author, embed=embed)


async def text2Speech(language, text, ctx, channel):
    myText = text
    language = language
    output = gTTS(text=myText, lang=language, slow=False)
    output.save("output.mp3")
    # if not connected
    if ctx.voice_client is None:
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio('output.mp3'))
    else:
        ctx.voice_client.play(discord.FFmpegPCMAudio('output.mp3'))


@bot.command(name='t')
async def t2s(ctx, *argv):
    channel = ctx.author.voice.channel
    text = ""
    for i in range(1, len(argv)):
        text += argv[i]
    language = argv[0]
    await text2Speech(language, text, ctx, channel)
    # await ctx.send("Lang is {} and the sentence is:  {} ".format(arg1,arg2))


@bot.command(name='w')
async def weather(ctx, city):
    city = City(city)
    strCity = city.getData()
    await ctx.send(strCity)


@bot.command(name='f')
async def weather(ctx, language, name):
    channel = ctx.author.voice.channel
    city = City(name)
    data = city.getData()
    if language == "en":
        await text2Speech(language, data, ctx, channel)
    elif language == "tr":
        data = city.getName() + " şehrinde hava " + str(city.convert(city.getTemp())) + "derece."
        await text2Speech(language, data, ctx, channel)


@bot.command(name='l')
async def speech2Text(ctx):
    language = 'tr'
    channel = ctx.author.voice.channel
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Anything :")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, key=None, language=language)
            # print("You said : {}".format(text))
            print(text)
            await ctx.send("You said : {}".format(text))

            if (text == 'hava kaç derece'):
                await weather(ctx, language, name='Ankara')
            else:
                await text2Speech(language, text, ctx, channel)
        except:
            await ctx.send("Sorry could not recognize what you said")
            # print("Sorry could not recognize what you said")


async def speech2Text(ctx, language):
    channel = ctx.author.voice.channel
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Anything :")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, key=None, language=language)
            print("You said : {}".format(text))
            await ctx.send("You said : {}".format(text))
            await text2Speech(language, text, ctx, channel)
        except:
            print("Sorry could not recognize what you said")


@bot.command(name='p')
async def youtube(ctx, *, search):
    query_string = urllib.parse.urlencode({
        'search_query': search
    })

    htm_content = urllib.request.urlopen(
        'http://www.youtube.com/results?' + query_string
    )
    search_results = re.findall('href=\"\\/watch\\?v=(.{11})', htm_content.read().decode())
    url = 'http://www.youtube.com/watch?v=' + search_results[0]
    await ctx.send(url)
    await play(ctx, url)


@bot.command(name='covid')
async def corona(ctx, *argv):
    if argv[0] == 'help':
        corona = Corona()
        countriesList = corona.listCountries()
        res = ''
        for country in countriesList:
            res += country + '\n'
            if len(res) >= 180:
                await ctx.send(res)
                res = ''
    else:
        corona = Corona()
        corona.listCountries()
        info = corona.getData(argv[0])
        await ctx.send(info)


async def play(ctx, url):
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


with open("env.yaml", encoding="utf-8") as env:
    config = safe_load(env)
    bot.run(config["DISCORD_TOKEN"])
