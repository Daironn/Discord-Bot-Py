from __future__ import unicode_literals
import discord
import requests
import bs4
import re
import os
from pytube import YouTube
from discord.ext import commands

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

queue = []

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}



commandList = {
            '.help:': 'Shows command list',
            '.ping:': 'Shows current state of bot\'s ping.  Aliases: [Ping, ping, checkping, p]',
            '.join:': 'Bot joins to your voice chat.  Aliases: [j]',
            '.leave:': 'Bot leaves your voice chat \\\\\\TODO\\\\\\',
            '.meme:': 'Gives you a smile. Aliases: [jbzd]',
            '.play:': ' \'URL\' :Plays music \\\\\\TODO\\\\\\',
            '.stop:': 'Jazz music stops\\\\\\TODO\\\\\\',
            '.skip:': 'Skips current song\\\\\\TODO\\\\\\',
            '.queue:': 'Shows queue \\\\\\TODO\\\\\\',
            '.unmute': ' @username: Annoys user.  Aliases: [rzuc, rzuć, odmutuj]',
            '.kick': ' @username: Kicks user from channel.  Aliases: [wypad]'
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~EVENTS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


@bot.event
async def on_ready():

    newActivity = discord.Activity(name='Music | .help for more info', type=discord.ActivityType.listening)

    embed = discord.Embed(
        title="ACTIVATED",
        description='Bot\'s been enabled. Type \".help\" for more informations.',
        colour=discord.Colour.dark_blue()
    )

    embed.set_thumbnail(url=bot.user.avatar_url)

    for channels in bot.get_all_channels():
        if channels.name == 'muzyka':
            # emoji = discord.utils.get(bot.emojis, name='OO') #Fajne warto pamiętać
                await channels.send(embed=embed)

    await bot.change_presence(activity=newActivity)

@bot.event
async def on_member_join(member):

    print(f'{member} has joined a server')


@bot.event
async def on_member_remove(member):

    print(f'{member} has left a server')


@bot.event
async def on_message(Message):

    embed = discord.Embed(
        title="Wrong channel",
        description='Try again on #muzyka <:tsun:616843907724083200>',
        colour=discord.Colour.dark_blue()
    )

    embed.set_thumbnail(url=bot.user.avatar_url)

    if Message.channel.name != 'muzyka' \
            and Message.author != bot.user \
            and Message.content[0] == '.' \
            and re.search(r'\.meme \d*', Message.content) \
            and re.search(r'\.jbzd \d*', Message.content):

         await Message.channel.send(embed=embed)
    else:
         await bot.process_commands(Message)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~COMMANDS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~PING
@bot.command(aliases=['Ping', 'ping', 'checkping', 'p']) #aliasy do komendy
async def _ping(ctx):

    embed = discord.Embed(
        title="Ping test",
        description=f'My ping is: {round(bot.latency * 1000)}MS',
        colour=discord.Colour.dark_blue()
    )

    embed.set_thumbnail(url=bot.user.avatar_url)
    await ctx.send(embed=embed)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~JOIN
@bot.command(aliases=['j', 'join'])
async def _join(ctx):
    if ctx.author.voice is None:
        await ctx.send("U have to be connected to a voice channel")
    elif ctx.voice_client is not None:
        await ctx.voice_client.move_to(ctx.author.voice.channel)
    else:
        await ctx.author.voice.channel.connect()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LEAVE~~~~TODO
@bot.command(aliases=['disconnect', 'leave'])
async def _disconnect(ctx):
    if ctx.voice_client is None:
       await ctx.send("I have to be connected first")
    else:
       await ctx.voice_client.disconnect()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~UNMUTE
@bot.command(aliases=['rzuc', 'rzuć', 'odmutuj', 'unmute'])
async def _unmute(ctx, member: discord.Member):

    for i in range(3):
        for channels in bot.get_all_channels():
            if channels.name == 'Channel1':
                await member.move_to(channels)
            elif channels.name == 'Channel2':
                await member.move_to(channels)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~KICK
@bot.command(aliases=['wypad', 'kick'])
async def _kick(ctx, member: discord.Member):

    await member.move_to(None)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~HELP
@bot.command(aliases=['help'])
async def _help(ctx):

    embed = discord.Embed(
        title='Here\'s your command list:',
        colour=discord.Colour.dark_blue()
    )

    for key in commandList.keys():
        embed.add_field(name=key, value=commandList[key], inline=False)

    embed.set_thumbnail(url=bot.user.avatar_url)

    await ctx.send(embed=embed)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MEME
@bot.command(aliases=['meme', 'jbzd'])
async def _meme(ctx, arg=1):

    embedWarning = discord.Embed(
        title="Wrong channel",
        description='Try again on #depression <:tsun:616843907724083200>',
        colour=discord.Colour.dark_blue()
    )

    embedWarning.set_thumbnail(url=bot.user.avatar_url)

    embedTooMuch = discord.Embed(
        title="Hold your horses",
        description='10 is max, take it or leave it <:tsun:616843907724083200>',
        colour=discord.Colour.dark_blue()
    )

    embedTooMuch.set_thumbnail(url=bot.user.avatar_url)

    embedMeme = discord.Embed(
        colour=discord.Colour.dark_blue()
    )

    if ctx.channel.name != 'depression':
        await ctx.send(embed=embedWarning)
    elif arg >= 10:
        await ctx.send(embed=embedTooMuch)
    else:
        for i in range(0, arg):
            url = 'https://jbzdy.cc/losowe'
            res = requests.get(url)
            res.raise_for_status()

            soup = bs4.BeautifulSoup(res.text, features="html.parser")
            jbzdElem = soup.select('img')

            if jbzdElem == []:
                print('error')
            else:
                embedMeme.set_image(url=jbzdElem[2].get('src'))
                channel = discord.utils.get(bot.get_all_channels(), name='depression')
                await channel.send(embed=embedMeme)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~CLEAR~~~~~~~~~~~~~~TODO
@bot.command(aliases=[''])
async def _clear(ctx):
    pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~PLAY!~~~~~~~~~~~~~~TODO


@bot.command(aliases=["play"])
async def _play(ctx, url):
    if ctx.author.voice is None:
        await ctx.send("U have to be connected to a voice channel")
    elif ctx.voice_client is not None:
        await ctx.voice_client.move_to(ctx.author.voice.channel)
    elif ctx.voice_client is None:
        await ctx.author.voice.channel.connect()

    await ctx.send('going good')

    yt = YouTube(url)
    await ctx.send('going good')
    stream = yt.streams.filter(only_audio=True).first()
    await ctx.send('going good')
    stream.download('/home/dairon/Downloads/PyTube')
    await ctx.send('going good')
    #
    # for filename in os.listdir('/home/dairon/Downloads/PyTube'):
    #     queue.append(filename)
    # source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('/home/dairon/Downloads/PyTube/'+queue[0]))
    # source.volume = 1.0
    #
    # ctx.voice_client.play(source)
    # queue.pop(0)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TOKEN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
bot.run('NjE2NzQyNzY2NjI1NTU0NDMy.XXjdcA.6pN2Xq0bf3STyF-WOMtOCJiW6HM')