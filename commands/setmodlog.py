import discord
from discord.ext import commands

import json

def getprefix(guild):
  with open('data/prefixes.json') as rfile:
    prefixes = json.load(rfile)
    if str(guild.id) in prefixes:
      return prefixes[str(guild.id)]
    else:
      return "-"

modlog = {}

async def on_ready(self):
  global modlog
  try:
    with open('data/setmodlog.json') as f:
      modlog = json.load(f)
  except:
    modlog = {}

def getjson():
  with open('data/setmodlog.json') as rfile:
    data = json.load(rfile)
  return data

class SetModLogCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_bulk_message_delete(self, msgs):
    data = getjson()
    for x in data:
      print(x)
      if int(x) == msgs[0].guild.id:
        if data[x]['ChannelId']:
          print('sending')
          channel = self.bot.get_channel(data[x]['ChannelId'])
          await channel.send(f'Bulk message deletion\n[{len(msgs)}] Messages deleted')
  @commands.Cog.listener()
  async def on_message_edit(self, before, after):
    if before.author.bot:
      return
    data = getjson()
    for x in data:
      if int(x) == before.guild.id:
        if data[x]['ChannelId']:
          channel = self.bot.get_channel(data[x]['ChannelId'])
          embed = discord.Embed(color=0xff8080)

          embed = discord.Embed(color=0xff8080)
          embed.add_field(name='Message Edited', value=f'Member: {before.author}\nBefore: {before.content}\nAfter: {after.content}\nMessage Channel: {before.channel.mention}\n\n[Click here to jump to message](https://discordapp.com/channels/{before.guild.id}/{before.channel.id}/{before.id})')
          await channel.send(embed=embed)
  @commands.command()
  async def setmodlog(self, ctx,  mlog: discord.TextChannel=None):
    channel = ctx.message.channel.id
    if not mlog:
      newdata = {
        "ChannelId": mlog
      }
    else:
      newdata = {
        "ChannelId": mlog.id
      }
    modlog[ctx.message.guild.id] = [newdata]
    if not mlog:
      await ctx.send(f"Mod log removed")
    else:
      await ctx.send(f"Mod Log channel set to {mlog.mention}")
    with open('data/setmodlog.json', 'w') as f:
      json.dump(modlog, f, indent=4)


def setup(bot):
  bot.add_cog(SetModLogCog(bot))