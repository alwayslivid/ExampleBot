'''
Developed with <3 and for the sake of doing so by AlwaysLivid.

@author: AlwaysLivid
'''

# IMPORTATION OF MODULES

try:
    import discord # I don't think that I have to explain this one.
    from discord.ext import commands # I don't think that I have to explain this one either.
    import logging # Module necessary, for well, uh, logging. 
    import smtplib
    import config, private # Modules necessary for the initialization of the bot.
except (AttributeError, ImportError):
    try:
        import logging # At this point my program prays that the user has the logging module installed and warns him accordingly.
        logging.basicConfig(level=logging.DEBUG)
        logging.critical("Failed to load some modules, exiting in 5 seconds.")
    except (AttributeError, ImportError):
        # Just in case the user *somehow* doesn't have the logging module installed.
        print("Failed to import some libs, exiting in 5 seconds.")
    import time # I've spent way too much time in this part, so I won't even have my program check whether the user has the 'time' module.
    time.sleep(5)
    exit()

# FUNCTION DEFINITION

bot = commands.Bot(command_prefix=config.prefix, description=config.description)

async def CogLoader(): # Loads cogs.
    for file in config.extensions: # file = list item in config.extensions
        try:
            logging.info("Loading %s...", file)
            bot.load_extension(file)
            logging.info("Loaded %s...", file)
        except Exception as e:
            logging.critical("FAILED TO LOAD %s", file)
            logging.critical("Exception: %s", e)
            logging.critical(traceback.print_exc())

@bot.event
async def on_ready():
    logging.info("Ready!")
    logging.info("Signed in as %s (ID: %s)", bot.user.name, bot.user.id)
    logging.info("Discord Version: %s", discord.__version__)
    await CogLoader()
    if config.debug_mode == True:
        activity = config.debug_status
        await bot.change.presence(activity=discord.Game(name=activity))
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