'''
Developed with <3 and for the sake of doing so by AlwaysLivid.

@author: AlwaysLivid
'''

if __name__ == "__main__":
	exit()

import discord
from discord.ext import commands
import logging
import config

class Owner:

	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='disablebot', hidden=True)
	@commands.is_owner()
	async def disablebot(self, ctx):
		logging.info("Disablebot command issued by {} (ID: {}).".format(ctx.author, str(ctx.author.id)))
		embed = discord.Embed(title="Goodbye!", color=0x551a8b, description="Alright, see ya! :wave:")
		embed.set_author(icon_url=ctx.author.avatar_url, name=str(ctx.author))
		logging.critical("Logging out per {}'s request!".format(ctx.author))
		await ctx.send(embed=embed)
		self.bot.logout()
		exit()
	
	'''
	Part taken from EvieePy's example and adapted to my own needs.
	https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
	'''

	@commands.command(name='cogmgmt', hidden=True)
	@commands.is_owner()
	async def cogmgmt(self, ctx, load: str, file: str):
		# Syntax: "m!manualcogloader <enable/disable> <cogname>"

		class OperationError(Exception):
			pass

		logging.info("Cogmgmt command issued by {} (ID: {}).".format(ctx.author, str(ctx.author.id)))
		load = load.lower()

		embed = discord.Embed(title="Cog Management", color=config.admin_color)
		embed.set_author(icon_url=ctx.author.avatar_url, name=str(ctx.author))
		logging.info("Cogmgmt command issued by {}.".format(ctx.author))

		try:
			if load == "enable":
				try:
					logging.info("Loading {}...".format(file))
					self.bot.load_extension(file)
					config.extensions.append(file)
					embed.add_field(name="Status", value="Operation Succeeded!", inline=False)
					logging.info("Loaded {}...".format(file))
					await ctx.send(embed=embed)
				except Exception:
					logging.critical("FAILED TO LOAD {}".format(file))
					raise OperationError
			elif load == "disable":
				try:
					logging.info("Unloading {}...".format(file))
					if file == __name__:
						logging.critical("Can't unload {}! (You'd unload the core parts of the bot, you silly goose!)".format(__name__))
						raise OperationError
					else:
						try:
							self.bot.unload_extension(file)
							config.extensions.remove(file) # Temporarily removes 'file' from the config.extensions list, just in case the user decides to reload the bot after removing the 'file' cog.
							embed.add_field(name="Status", value="Operation Succeeded!", inline=False)
							logging.info("Unloaded {}...".format(file))
							await ctx.send(embed=embed)
						except Exception:
							logging.critical("FAILED TO UNLOAD {}".format(file))
							raise OperationError
				except Exception:
					raise OperationError
			else:
				raise OperationError
		except OperationError:
			embed.add_field(name="Status", value="Operation Failed! (Check the console for more info!)", inline=False)
			embed.add_field(name="Syntax", value="`m!manualcogloader <enable/disable> <cogname>`", inline=False)
			await ctx.send(embed=embed)
	
	@commands.command(name='reload', hidden=True)
	@commands.is_owner()
	async def reload(self, ctx):
		logging.info("Reload command issued by {} (ID: {}).".format(ctx.author, str(ctx.author.id)))
		embed = discord.Embed(title="Reload", color=config.admin_color)
		embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author)
		try:
			for file in config.extensions:
				self.bot.unload_extension(file)
				logging.critical("Unloaded {}!".format(file))
				self.bot.load_extension(file)
				logging.critical("Reloaded {}!".format(file))
			logging.critical("Reloaded!")
			embed.add_field(title="\u200B", value="Operation Succeeded!", inline=False)
			await ctx.send(embed=embed)
		except:
			embed.add_field(name="FAILURE!", value="Operation Failed!", inline=False)

def setup(bot):
	bot.add_cog(Owner(bot))
