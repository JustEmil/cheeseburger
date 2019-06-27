import discord
import os
from discord.ext import commands
import json
import time
import asyncio
import traceback

def get_prefix(bot, message):
  if not message.guild:
    return commands.when_mentioned_or("-")(bot, message)
  
  with open("data/prefixes.json", 'r') as f:
    prefixes = json.load(f)
  
  if str(message.guild.id) not in prefixes:
    return commands.when_mentioned_or("-")(bot, message)

  prefix = prefixes[str(message.guild.id)]
  return commands.when_mentioned_or(prefix)(bot, message)

def getprefix(guild):
  with open('data/prefixes.json') as rfile:
    prefixes = json.load(rfile)
    if str(guild.id) in prefixes:
      return prefixes[str(guild.id)]  
    else:
      return "-"

bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)

@bot.event
async def on_message(msg):
  if msg.author.bot:
    return
  await bot.process_commands(msg)

extension = [
  'commands.warn',
  'commands.punishments',
  'commands.kick',
  'prefix',
  'commands.profile',
  'commands.setmodlog',
  'commands.temp',
  'commands.automod',
  'commands.mute_deafen',
  'commands.nick',
  'errorhandler',
  'commands.purge',
  'commands.ban',
  'commands.welcome',
  'commands.leave',
]
# data2= [
#   {"test"},
#   {'Test2'}
# ]
# for x, i in enumerate(data2):
#   print(x,i)


@bot.event
async def on_ready():
  print('ready')
  await bot.change_presence(activity=discord.Activity(name='Netflix', type = discord.ActivityType.watching))

# =========
# Temporary Bans
# =========
async def tempcheck():
  await bot.wait_until_ready()
  while not bot.is_closed():
    changes = False
    with open('data/temp.json') as rfile:
      data = json.load(rfile)
    if len(data) > 0:
      for x in data:
        if not "comment" in x:
          for q in data[x]:
            print(q)
            print(x)
            ready=q['Date']
            if q['Type'] == 'minute':
              ready = ready + (q['Time']*60)
            elif q['Type'] == 'hour':
              ready = ready + ((q['Time']*60)*60)
            elif q['Type'] == 'day':
              ready = ready + ((q['Time']*60)*60) * 24
            elif q['Type'] == 'second':
              ready = ready + (q['Time'])
            if ready < time.time():
              guild = bot.get_guild(int(x))
              # for i,v in enumerate(data):
              #   if v["User"] == q['User']:
              data[x].remove(q) # i hope this works so i dont have to use the method above
              changes = True
              for banned in await guild.bans():
                if banned.user.id == q['User']:
                  await guild.unban(banned.user, reason=f'Tempban lifted, Time: {q["Time"]}{q["Type"]}(s)')
      if changes:
        with open('data/temp.json', "w") as wfile:
          json.dump(data, wfile, indent=4)
    await asyncio.sleep(10) # slows the script to stop bot lag important

if __name__ == "__main__":
  for extension in extension:
    try:
      bot.load_extension(extension)
    except Exception as error:
      print('{} cannot be loaded. [{}]'.format(extension, error))
  bot.loop.create_task(tempcheck()) # constant loop
  bot.run(os.getenv('token'))
