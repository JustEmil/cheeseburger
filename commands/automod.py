import discord
from discord.ext import commands
import json

# moderates channels, automatically deletes any
# messages containing swears or links that are in the self. lists
# command to enable and disable it under @commands.command

# TOTAL
# 4 commands in the Cog
# 1 listener

class automodcog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.swearlist = ['fuck', 'fuk', 'fuc', 'bitch', 'cunt', 'ass', 'dick', 'shit', 'pussy', 'slut', 'puta', 'fag', 'nigg', 'chink']
    self.linklist = ['http', 'www.', '.com', '.io', '.org', '.net']
  
  # ===========
  # LISTENERS
  # (Catches messages, checks and verifies them)
  # users with manage messages bypass the check
  # (they can send swears and links)
  # ===========
  @commands.Cog.listener()
  async def on_message(self, message):
    guild = message.guild
    content = message.content
    author = message.author
    swears = False
    links = False
    with open('data/settings.json') as rfile:
      data = json.load(rfile)
    for x in data:
      if int(x) == guild.id:
        if data[x]["SwearEnabled"]:
          swears = True
        if data[x]["LinkEnabled"]:
          links = True
    if swears:
      if not author.guild_permissions.manage_messages:
        for x in self.swearlist: #checks if any of the swears are in the message
          if x in content:
            await message.delete()
            await message.channel.send(f'Please do not use swears in your messages\n{author.mention} | {author}')
            return
    if links:
      if not author.guild_permissions.manage_messages:
        for x in self.linklist: # checks if any of the links are in the message
          if x in content:
            await message.delete()
            await message.channel.send(f'Please do not use links in your messages\n{author.mention} | {author}')
            return
    





  # ===========
  # COMMANDS
  # ===========
  @commands.command() # automoderation for swearing
  async def enableautoswears(self, ctx):
    if not ctx.author.guild_permissions.manage_guild:
      await ctx.send('you do not have the required permissions to perform this task\n`manage_guild`')
      return
    with open('data/settings.json') as rfile:
      data = json.load(rfile)
    documented = False
    for x in data:
      if int(x) == ctx.guild.id:
        documented = True
        data[x]["SwearEnabled"] = True
    if not documented:
      newdata = {
        "SwearEnabled": True,
        "LinkEnabled": False
      }
      data[str(ctx.guild.id)] = newdata
    with open('data/settings.json', 'w') as wfile:
      json.dump(data, wfile, indent=4)
    await ctx.send('enabled automod for Swears')
    return
  @commands.command()
  async def disableautoswears(self, ctx):
    if not ctx.author.guild_permissions.manage_guild:
      await ctx.send('you do not have the required permissions to perform this task\n`manage_guild`')
      return
    with open('data/settings.json') as rfile:
      data = json.load(rfile)
    documented=False
    for x in data:
      if int(x) == ctx.guild.id:
        documented = True
        data[x]["SwearEnabled"] = False
    if not documented:
      newdata={
        "SwearEnabled": False,
        "LinkEnabled": False
      }
      data[str(ctx.guild.id)] = newdata
    with open('data/settings.json', 'w') as wfile:
      json.dump(data, wfile, indent=4)
    await ctx.send("disabled automod for Swears")
    return
  @commands.command() # automoderation for links
  async def enableautolinks(self, ctx):
    if not ctx.author.guild_permissions.manage_guild:
      await ctx.send("You do not have the required permissions to perform this task\n`manage_guild`")
      return
    with open("data/settings.json") as rfile:
      data = json.load(rfile)
    documented = False
    for x in data:
      if int(x) == ctx.guild.id:
        documented = True
        data[x]['LinkEnabled'] = True
    if not documented:
      newdata= {
        "SwearEnabled": False,
        "LinkEnabled": True
      }
      data[str(ctx.guild.id)] = newdata
    with open('data/settings.json', 'w') as wfile:
      json.dump(data, wfile, indent=4)
    await ctx.send("enabled automod for Links")
    return
  @commands.command()
  async def disableautolinks(self, ctx):
    if not ctx.author.guild_permissions.manage_guild:
      await ctx.send('you do not have the required permissions to perform this task\n`manage_guild`')
      return
    with open('data/settings.json') as rfile:
      data = json.load(rfile)
    documented=False
    for x in data:
      if int(x) == ctx.guild.id:
        documented = True
        data[x]["LinkEnabled"] = False
    if not documented:
      newdata={
        "SwearEnabled": False,
        "LinkEnabled": False
      }
      data[str(ctx.guild.id)] = newdata
    with open('data/settings.json', 'w') as wfile:
      json.dump(data, wfile, indent=4)
    await ctx.send("disabled automod for Links")
    return
    


def setup(bot):
  bot.add_cog(automodcog(bot))