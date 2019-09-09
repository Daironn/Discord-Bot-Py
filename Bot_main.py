import discord
import requests
import bs4
import re
from discord.ext import commands

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

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

    await ctx.author.voice.channel.connect()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~UNMUTE
@bot.command(aliases=['rzuc', 'rzuć', 'odmutuj', 'unmute'])
async def _unmute(ctx, member: discord.Member):

    for i in range(3):
        for channels in bot.get_all_channels():
            if channels.name == 'Dupa mojego starego':
                await member.move_to(channels)
            elif channels.name == 'Dupa mojej starej':
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
            url = ' https://jbzdy.eu/losowe'
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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TOKEN~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
bot.run('NjE2NzQyNzY2NjI1NTU0NDMy.XWhAug.RosTW7Cal5t1u4mOLdUcqgFFHeI')

