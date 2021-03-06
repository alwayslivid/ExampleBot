'''
Developed with <3 and for the sake of doing so by AlwaysLivid.

@author: AlwaysLivid
'''

try:
    import discord
    from discord.ext import commands
    import logging
    import random
    import config, private
except (AttributeError, ImportError):
    try:
    import logging, time
    logging.basicConfig(level=logging.DEBUG)
    logging.critical("Failed to load some modules, exiting in 5 seconds.")
    time.sleep(5)
    exit()

bot = commands.Bot(command_prefix=config.prefix, description=config.description)

async def CogLoader(): # Loads cogs.
    for file in config.extensions: # file = list item in config.extensions
        try:
            logging.info("Loading {}...".format(file))
            bot.load_extension(file)
            logging.info("Loaded {}...".format(file))
        except Exception as e:
            logging.critical("FAILED TO LOAD {}".format(file))
            logging.critical("Exception: {}".format(e))

@bot.event
async def on_ready():
    logging.info("Ready!")
    logging.info("Signed in as {} (ID: {})".format(bot.user.name, bot.user.id))
    logging.info("Discord Version: {}".format(discord.__version__))
    await CogLoader()
    if config.debug_mode == True:
        activity = config.debug_status
        await bot.change_presence(activity=discord.Game(name=activity))
    elif config.debug_mode == False:
        activity = random.choice(config.statuses)
        await bot.change_presence(activity=discord.Game(name=activity))

def main():
    if config.debug_mode == True:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.info("Logging in!")
    is_bot = config.is_bot
    reconnect = config.reconnect
    bot.run(private.token, bot=is_bot, reconnect=reconnect)

if __name__ == "__main__":
    main()
