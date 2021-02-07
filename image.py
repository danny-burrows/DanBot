import io

import imageio
import imgkit
import discord
from discord.ext import commands
from jinja2 import Environment, FileSystemLoader

from utils import loading_bar


class DanBotImage(commands.Cog, name="Images"):

    def __init__(self, bot):
        self.bot = bot
        # Initialize Imgkit & Jinja2
        self.imgkit_config = imgkit.config()
        self.imgkit_options = {
            'quiet': '',
            'format': 'png',
            'quality': '69',
            'encoding': "UTF-8",
            'width': '815'
        }

        file_loader = FileSystemLoader('templates')
        self.jinja_env = Environment(loader=file_loader)

    async def get_card_info(self, ctx, arg):
        if len(arg) and arg.startswith("<@") and arg.endswith(">"):
            user_id = arg[2:][:-1]
            if user_id.startswith("!"):
                user_id = user_id[1:]
            user = await self.bot.fetch_user(user_id)
        else:
            user = ctx.author

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

        return user, guild, nick, roles, colour

    def build_card(self, ctx, card_info, template_name="card.html", background_hue=""):
        template = self.jinja_env.get_template(template_name)

        user, guild, nick, roles, colour = card_info

        output = template.render(
            id=user.id,
            name=user.name.replace("  ", " "),
            tag=f"#{user.discriminator}",
            avatar=user.avatar,
            guild=guild,
            nick=nick,
            roles=roles,
            colour=colour,
            background_hue=background_hue
        )

        img = imgkit.from_string(
            output, False, config=self.imgkit_config, options=self.imgkit_options)
        img_data = io.BytesIO(img)

        return img_data

    @commands.command(
        name="card",
        aliases=["Card"],
        help="Get your user card.",
    )
    async def card(self, ctx, arg=""):
        msg = await ctx.send(loading_bar(0))
        card_info = await self.get_card_info(ctx, arg)
        await msg.edit(content=loading_bar(40))
        img_data = self.build_card(ctx, card_info, "card.html")
        await msg.edit(content=loading_bar(80))
        await ctx.send(file=discord.File(img_data, 'user_card.png'))
        await msg.edit(content=loading_bar(90))
        await msg.delete()

    @commands.command(
        name="neoncard",
        aliases=["NeonCard"],
        help="Get a neon user card.",
    )
    async def neon_card(self, ctx, arg=""):
        msg = await ctx.send(loading_bar(0))
        card_info = await self.get_card_info(ctx, arg)
        await msg.edit(content=loading_bar(40))
        img_data = self.build_card(
            ctx, card_info, 'card_neon.html', background_hue=13)
        await msg.edit(content=loading_bar(80))
        await ctx.send(file=discord.File(img_data, 'user_card_neon.png'))
        await msg.edit(content=loading_bar(90))
        await msg.delete()

    @commands.command(
        name="neoncardgif",
        aliases=["NeonCardGif"],
        help="Get an animated neon user card.",
    )
    async def neon_card_gif(self, ctx, arg=""):
        msg = await ctx.send(loading_bar(0))
        card_info = await self.get_card_info(ctx, arg)
        await msg.edit(content=loading_bar(20))

        frames = []
        base_hue = 13
        hues = [0 for i in range(5)] + [i for i in range(5)] + \
            [i for i in range(5, 0, -1)]
        await msg.edit(content=loading_bar(20))
        for perc, hue in enumerate(hues):
            img_data = self.build_card(
                ctx, card_info, "card_neon.html", background_hue=(base_hue + (hue*4)))
            await msg.edit(content=loading_bar(40+perc+1))
            frames.append(imageio.imread(img_data))
            await msg.edit(content=loading_bar(40+perc+2))

        await msg.edit(content=loading_bar(60))
        imageio.mimsave('test.gif', frames, duration=0.2)
        await msg.edit(content=loading_bar(80))

        await ctx.send(file=discord.File('test.gif'))
        await msg.edit(content=loading_bar(90))
        await msg.delete()
        # await ctx.send(file=discord.File(img_data, 'user_card.png'))
