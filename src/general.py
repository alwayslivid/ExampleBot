'''
Developed with <3 and for the sake of doing so by AlwaysLivid.

@author: AlwaysLivid
'''

from discord.ext import commands
if __name__ == "__main__":
	exit()

import discord
import logging
import config

class General:

	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="ping", description="Ping the bot!")
	async def ping(self, ctx):

		logging.info("Ping command issued by {} (ID: {}).".format(ctx.author, str(ctx.author.id)))
		embed = discord.Embed(title="Ping", color=config.neutral_green)
		embed.set_author(icon_url=ctx.author.avatar_url, name=str(ctx.author))
		embed.add_field(name="Pong!", value="Latency: {}".format(self.bot.latency), inline=False)

		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(General(bot))
