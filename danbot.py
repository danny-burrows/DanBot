#!/usr/bin/env python3

import asyncio
import io
import logging
import os
import random
import re
from urllib.parse import quote

import discord
import imgkit
from discord.ext import commands
from jinja2 import Environment, FileSystemLoader
from chat import DanBotChat

logging.basicConfig(level=logging.INFO)
logging.debug("[DanBot] - Initializing...")

version = "v0.2"
intents = discord.Intents.default()
intents.members = True  # Gotta subscribe to the privileged members intent.
bot = commands.Bot(
    command_prefix='>',
    description=f"DanBot {version}",
    intents=intents
)

# Initialize Imgkit & Jinja2
config = imgkit.config()
file_loader = FileSystemLoader('templates')
jinja_env = Environment(loader=file_loader)

danbot_re = re.compile('(?m)(?i)DanBot')


@bot.event
async def on_ready():
    logging.debug(f"[DanBot] - We have logged in as {bot.user}")

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"for >help"
        )
    )


@bot.command(
    name="ping",
    aliases=["ping!"],
    help="Check if DanBot is alive. \nHe will only answer if he is awake...",
)
async def ping(ctx):
    await ctx.send("pong!")


@bot.command(
    name="card",
    aliases=["Card"],
    help="Get your user card.",
)
async def card(ctx, arg=""):
    if len(arg) and arg.startswith("<@") and arg.endswith(">"):
        user_id = arg[2:][:-1]
        if user_id.startswith("!"):
            user_id = user_id[1:]
        user = await bot.fetch_user(user_id)
    else:
        user = ctx.author

    template = jinja_env.get_template('temp01.html')

    guild = nick = "Private"
    colour = "fff"
    roles = []
    if ctx.guild:
        guild = ctx.guild.name
        mem = ctx.guild.get_member(user.id)
        nick = mem.nick.replace(
            "  ", " ") if mem.nick else user.name.replace("  ", " ")
        roles = [mem.top_role]
        colour = mem.colour if str(mem.colour) != "#000000" else "#b9bbbe"

    output = template.render(
        id=user.id,
        name=user.name.replace("  ", " "),
        tag=f"#{user.discriminator}",
        avatar=user.avatar,
        guild=guild,
        nick=nick,
        roles=roles,
        colour=colour
    )

    options = {
        'quiet': '',
        'format': 'png',
        'quality': '69',
        'encoding': "UTF-8",
        'width': '815'
    }

    img = imgkit.from_string(output, False, config=config, options=options)
    img_data = io.BytesIO(img)

    await ctx.send(file=discord.File(img_data, 'user_card.png'))


@bot.command(
    name="dmslide",
    aliases=["DMslide", "DMSlide"],
    help="DanBot slides into them DM's...",
)
async def dmslide(ctx):
    await ctx.author.send("Oh hey, did your humanoid father steal the stars from the cosmos and put them in your eyes?")


@bot.command(
    name="google",
    help="DanBot can google things for ya...",
)
async def google(ctx, *args):
    if not len(args):
        return await ctx.send("I can't google nothing. :/")

    # Sanitize input for links...
    sanitized_link_parts = [quote(arg) for arg in args]

    results = discord.Embed(
        title=f"Google Results For \"{' '.join(args)}\"",
        url=f"http://www.justgoogleitup.com/?q={'+'.join(sanitized_link_parts)}",
        description="Did my best to find these results...",
        colour=discord.Colour.red()
    )
    results.set_thumbnail(
        url="https://lh3.googleusercontent.com/COxitqgJr1sJnIDe8-jiKhxDx1FrYbtRHKJ9z_hELisAlapwE9LUPh6fcXIfb5vwpbMl4xl9H9TRFPc5NOO8Sb3VSgIBrfRYvW6cUA")
    await ctx.send(f"Here ya go, this is what I've found...", embed=results)


@bot.command(
    name="roll",
    aliases=['Roll'],
    help="DanBot will roll a dice for you. \ne.g. >roll (d2|d3|d4|d6|d10|d100)"
)
async def roll(ctx, arg):
    dice_types = {
        "d2": (1, 2),
        "d3": (1, 3),
        "d4": (1, 4),
        "d6": (1, 6),
        "d10": (1, 10),
        "d100": (1, 100)
    }

    if arg.lower() not in dice_types.keys():
        await ctx.send("Sorry, I don't know that type of dice. :(")
        return

    await ctx.send(f"{ctx.message.author.mention} rolled a {arg} and got {random.randint(*dice_types[arg])}")


@bot.command(
    name="timer",
    aliases=['Timer'],
    help="DanBot can set a timer for you. \ne.g. >timer 2h 30m 25s"
)
async def timer(ctx, *args):
    h = m = s = 0

    # Future note: Update to regex.
    for i in args:
        if i[-1].lower() == "h":
            h = int(i[:-1])
        elif i[-1].lower() == "m":
            m = int(i[:-1])
        elif i[-1].lower() == "s":
            s = int(i[:-1])
        elif i.isnumeric():
            s = int(i)

    await ctx.send(f'Setting a {" ".join(args)} timer for {ctx.author.mention}.')

    time = (h*60*60)+(m*60)+s
    await asyncio.sleep(time)

    await ctx.reply(f'BEEP BEEP! {ctx.author.mention} your timer just finished!', mention_author=True)


@bot.command(
    name="livetimer",
    aliases=['LiveTimer', 'countdown', 'Countdown'],
    help="DanBot can set live timer that counts down. \ne.g. >livetimer 2h 30m 25s"
)
async def live_timer(ctx, *args):
    h = m = s = 0

    # Future note: Update to regex.
    for i in args:
        if i[-1].lower() == "h":
            h = int(i[:-1])
        elif i[-1].lower() == "m":
            m = int(i[:-1])
        elif i[-1].lower() == "s":
            s = int(i[:-1])
        elif i.isnumeric():
            s = int(i)

    time = (h*60*60)+(m*60)+s

    await ctx.send(f'Setting a {" ".join(args)} second timer for {ctx.author.mention}.')

    msg = await ctx.send(content=f"`{time} seconds left`")

    for i in range(time, 0, -1):
        await msg.edit(content=f"`{i} seconds left`")
        await asyncio.sleep(1)

    await msg.edit(content=f'`BEEP BEEP!`')


@bot.command(name="serverinfo")
async def server_info(ctx):
    # Some lines are commented as they require the members intent.

    role_count = len(ctx.guild.roles)
    list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]

    embed2 = discord.Embed(
        timestamp=ctx.message.created_at, colour=ctx.author.colour)
    embed2.add_field(name='Name', value=f"{ctx.guild.name}", inline=False)
    # embed2.add_field(name='Owner', value=f"{ctx.guild.owner}", inline=False)
    embed2.add_field(name='Highest Role',
                     value=ctx.guild.roles[-2], inline=False)

    # for role in ctx.guild.roles:
    #     members = '\n'.join([member.name for member in role.members]) or "None"
    #     embed2.add_field(name=role.name, value=members)

    embed2.add_field(name='Number of Roles',
                     value=str(role_count), inline=False)
    embed2.add_field(name='Number of Members',
                     value=ctx.guild.member_count, inline=False)
    embed2.add_field(name='Bots:', value=(', '.join(list_of_bots)))
    embed2.add_field(name='Created At', value=ctx.guild.created_at.__format__(
        '%A, %d. %B %Y @ %H:%M:%S'), inline=False)
    embed2.set_thumbnail(url=ctx.guild.icon_url)
    embed2.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed2.set_footer(text=ctx.bot.user.name, icon_url=ctx.bot.user.avatar_url)

    await ctx.send(embed=embed2)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if danbot_re.search(message.content):
        await message.channel.send('Hewwo UwU?')

    if message.content == "load phas":
        loading_txt = f"              Loading... 0%"
        loading_bar = "|                                               |"

        msg = await message.channel.send(f"```\n{loading_txt}\n{loading_bar}\n```")

        segments = 10
        seg_length = len(loading_bar) // segments
        for i in range(segments):
            loading_txt = f"              Loading... {(100//segments)*i}%"
            loading_bar = f"|{'='*(seg_length*i)}{' '*(seg_length*(segments-i))}|"
            await msg.edit(content=f"```\n{loading_txt}\n{loading_bar}\n```")


if __name__ == "__main__":
    bot_token = os.environ.get("DANBOTTOKEN")

    if not bot_token:
        raise ValueError("Couldn't retrieve bot token!")

    logging.debug("[DanBot] - Got bot token!")

    bot.add_cog(DanBotChat(bot))

    bot.run(bot_token)
