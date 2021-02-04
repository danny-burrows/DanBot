import os

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from discord.ext import commands


class DanBotChat(commands.Cog, name="Chat Bot"):

    def __init__(self, bot):
        self.bot = bot
        self.chatty_channels = []

        needs_training = not os.path.isfile('./db.sqlite3')

        self.chatbot = ChatBot(
            'DanBot',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri='sqlite:///db.sqlite3'
        )

        if needs_training:
            trainer = ChatterBotCorpusTrainer(self.chatbot)
            trainer.train(
                "chatterbot.corpus.english",
                "chatterbot.corpus.english.greetings",
                "chatterbot.corpus.english.conversations"
            )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.channel.id in self.chatty_channels:
            response = self.chatbot.get_response(message.content)
            await message.channel.send(response)

    @commands.command(
        name="chat",
        aliases=['Chat'],
        help="Let DanBot try talk to you. (He won't bite, I think :/)"
    )
    async def chat(self, ctx):
        self.chatty_channels += [ctx.channel.id]
        response = self.chatbot.get_response("Hello")
        await ctx.reply(response)

    @commands.command(
        name="stop",
        aliases=['quit'],
        help="Make DanBot stop talking!"
    )
    async def stop_chat(self, ctx):
        if ctx.channel.id in self.chatty_channels:
            self.chatty_channels.remove(ctx.channel.id)
        await ctx.send(f"Ok {ctx.author.mention} I'll stop now, it was nice chatting with you. :-)")
