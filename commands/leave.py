import discord
from discord.ext import commands
import errorcodes
import json
import random

class leavecog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_member_remove(self, member):
    embed=discord.Embed(colour=errorcodes.Colour)
    with open('data/leave.json') as rfile:
      data = json.load(rfile)
    guild = member.guild
    for x in data:
      if int(x) == guild.id:
        if not data[x]['Channel']:
          return
        channel = self.bot.get_channel(data[x]['Channel'])
        await channel.send(f'{member} has left')
        return

  @commands.command()
  async def setleave(self, ctx, channel:discord.TextChannel=None):
    embed=discord.Embed(colour=errorcodes.Colour)
    if not ctx.author.guild_permissions.manage_guild:
      embed.add_field(name='Restricted Access', value=f'{errorcodes.Restricted}\n`manage_guild`')
      await ctx.send(embed=embed)
      return
    if not channel:
      embed.add_field(name='Invalid Input', value='-setleave <ChannelMention>')
      await ctx.send(embed=embed)
      return
    with open('data/leave.json') as rfile:
      data = json.load(rfile)
    documented =True
    if channel:
      channel = channel.id
    for x in data:
      if int(x) == ctx.guild.id:
        documented=False
        data[x]["Channel"] = channel
    if documented:
      newdata ={
        "Channel": channel
      }
      data[str(ctx.guild.id)] = newdata
    with open('data/leave.json', 'w') as wfile:
      json.dump(data, wfile, indent=4)
    embed.add_field(name='Set leave channel', value=f'Set leave channel to {channel.mention}')
    await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(leavecog(bot))