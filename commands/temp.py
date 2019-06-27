import discord
from discord.ext import commands
import json
import time as timeee

# 2 commands

class tempcog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.Cog.listener()
  async def on_member_unban(self, guild, member):
    with open('data/temp.json', 'r') as rwfile:
      data = json.load(rwfile)
    for x in data:
      if int(x) == guild.id:
        for q in data[x]:
          if q["User"] == member.id:
            data[x].remove(q)
    with open('data/temp.json', 'w') as wfile:
      json.dump(data, wfile, indent=4) 

  @commands.command(aliases=['softban'])
  async def tempban(self, ctx, member:discord.Member=None, time:int=1, typee:str="d", *, reason:str="Unspecified Reason"):
    if not ctx.author.guild_permissions.ban_members:
      await ctx.send("You do not have the required permissions to perform this task.")
      return
    if member.guild_permissions.ban_members:
      await ctx.send('You can not ban another moderator')
      return
    if not member:
      await ctx.send('please specify a user')
      return
    with open("data/temp.json") as rfile:
      data = json.load(rfile)
    typees = ['day', 'hour', 'minute', 'second']
    if typee == "d":
      typee = "day"
    elif typee == "h":
      typee = "hour"
    elif typee == "m":
      typee = "minute"
    elif typee == "s":
      typee = "second"
    for x in typees:
      if x in typee:
        typee = x
    newdata = {
      "User": member.id,
      "Time": time,
      "Type": typee,
      "Date": timeee.time()
    }
    documented = False
    for x in data:
      if x == str(ctx.guild.id):
        documented = True
        print('adding')
        data[x].append(newdata)
    if not documented:
      print('adding2')
      data[str(ctx.guild.id)] = [newdata]
    ready=newdata["Date"]
    if newdata['Type'] == 'minute':
      ready = ready + (newdata['Time']*60)
    elif newdata['Type'] == 'hour':
      ready = ready + ((newdata['Time']*60)*60)
    elif newdata['Type'] == 'day':
      ready = ready + ((newdata['Time']*60)*60) * 24
    elif newdata['Type'] == 'second':
      ready = ready + (newdata['Time'])
    embed=discord.Embed(colour=discord.Color.red())
    embed.add_field(name='Ban', value='User: {}\nModerator: {}\nTime: {}{}(s)\nReason: {}\n\nUnbanned: {}'.format(member, ctx.author, time, typee, reason, timeee.asctime(timeee.localtime(ready))))
    await member.send(embed=embed)
    await member.ban()
    await ctx.send(embed=embed)
    with open('data/temp.json', 'w') as wfile:
      json.dump(data, wfile, indent=4)
    return
  # @commands.command()
  # async def softbans(self, ctx):
  #   embed=discord.Embed(colour=errorcodes.Colour)
  #   if not ctx.author.guild_permissions.ban_members:
  #     embed.add_field(name='Restricted Access', value=f'{errorcodes.Restricted}\n`ban_members`')
  #     await ctx.send(embed=embed)
  #   with open('data/temp.json') as rfile:
  #     data = json.load(rfile)
  #   documented=False
  #   for x in data:
  #     if int(x) == ctx.guild.id:
  #       for q in 
    

def setup(bot):
  bot.add_cog(tempcog(bot))