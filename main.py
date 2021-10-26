import os
import logging
import disnake
from web import life
from disnake.ext import commands

intents = disnake.Intents.all() 
intents.members = True

# Bot
tokeN = os.environ["token"]
bot = commands.Bot(command_prefix=["darkb ", "Darkb "], help_command=None, intents = intents)



for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

  else:
    print(f'Unable to load {filename[:-3]}')

for backups in os.listdir('./backups'):
  print(f'Backup: {backups}')



logging.basicConfig(level=logging.INFO)
bot.load_extension('jishaku')



@bot.event 
async def on_ready():
  print(f"{bot.user} is online")
  print(f"disnake: {disnake.__version__}")
  activity=disnake.Activity(type=disnake.ActivityType.watching, name="Ur life")
  await bot.change_presence(status=disnake.Status.idle, activity=activity)


  
#universal command not found error
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    embed = disnake.Embed(title = 'error', description = 'command was not found', color = disnake.Color.red())
    await ctx.send(embed = embed)





life()
bot.run(tokeN)