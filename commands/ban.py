import discord
import time
from discord.ext import commands

import json

def getprefix(guild):
  with open('data/prefixes.json') as rfile:
    prefixes = json.load(rfile)
    if str(guild.id) in prefixes:
      return prefixes[str(guild.id)]
    else:
      return "!"

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

class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ban(self, ctx, member: discord.Member=None, *, reason='Unspecified Reason'):
      if not ctx.author.guild_permissions.ban_members:
        await ctx.send('You dont have permission to use this command')
        return
      if not member:
        await ctx.send(f'Please specify a member - `{str(getprefix(ctx.guild))}ban <member> <reason>`')
        return
      if member.mention == ctx.message.author.mention:
        await ctx.send('You can\'t ban yourself')
        return
      if member.guild_permissions.ban_members:
        if ctx.author.top_role.position <= member.top_role.position:
          await ctx.send('You can\'t kick another moderator')
          return
      if member.bot:
        await ctx.send('You can\'t ban a bot')
        return
      else:
        with open('data/setmodlog.json') as rfile:
          data = json.load(rfile)
        for x in data:
          if int(x) == member.guild.id:
            if data[x]['ChannelId']:
              channel = self.bot.get_channel(data[x]['ChannelId'])
              embed=discord.Embed(color=0xffffa2)
              embed.set_author(name='Member banned')
              embed.add_field(name='Member', value=member)
              embed.add_field(name='Moderator', value=ctx.message.author)
              embed.add_field(name='Reason', value=reason)
              await channel.send(embed=embed)
              await ctx.message.delete()
              await member.ban()
            else:
              await member.ban()

def setup(bot):
    bot.add_cog(BanCog(bot))
    print('Loaded commands.Moderation.ban')