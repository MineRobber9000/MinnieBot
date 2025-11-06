import os, sys, asyncio
from discord.ext import commands
from discord import Intents
import config
# add this directory to the python module path
sys.path.insert(1,os.path.dirname(os.path.realpath(__file__)))

class IgnoreBotsBot(commands.Bot):
	async def on_message(self,message):
		if message.author.bot: return
		await self.process_commands(message)
	async def setup_hook(self):
		for module in os.listdir("cogs"):
			# if it's a python file, load it as an extension
			if module.endswith(".py"):
				await bot.load_extension("cogs."+module[:-3])

bot = IgnoreBotsBot("%",intents=Intents.all())

bot.run(config.token)
