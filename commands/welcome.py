import discord
from discord.ext import commands
import errorcodes
import json
import random

    # embed.add_field(name=f'Welcome {member}', value=f'Welcome {member.mention} to {member.guild}!')
    # embed.add_field(name='Account Creation Date', value=f'**{member.created_at}**')

# TOTAL
# 3 commands
# 1 listener


class welcomecog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #welcomes player while showing everyone the accounts creation date
  ############
  # Listener
  ############
  @commands.Cog.listener()
  async def on_member_join(self, member):
    embed=discord.Embed(colour=errorcodes.Colour)
    with open('data/welcomes.json') as rfile:
      data = json.load(rfile)
    guild = member.guild
    for x in data:
      if int(x) == guild.id:
        if not data[x]['Channel']:
          return
        channel = self.bot.get_channel(data[x]['Channel'])
        messages = ['{} just joined the server - glhf!', '{} just joined. Everyone, look busy!', '{} just joined. Can I get a heal?', '{} joined your party.', '{} joined. You must construct additional pylons.', '{} is here.', '{}. Stay awhile and listen.', '{}. We were expecting you ( ͡° ͜ʖ ͡°)', '{}. We hope you brought pizza.']
        embed.add_field(name=f'Welcome {member}', value=f'{random.SystemRandom().choice(messages).format(member.mention)}')
        embed.add_field(name='Account Creation Date', value=f'**{member.created_at}**', inline=False)
        await channel.send(embed=embed)
        return
  
  #############
  # commands
  #############
  @commands.command()
  async def setwelcome(self, ctx, channel:discord.TextChannel=None):
    embed=discord.Embed(colour=errorcodes.Colour)
    print('1')
    if not ctx.author.guild_permissions.manage_guild:
      embed.add_field(name='Restricted Access', value=f'{errorcodes.Restricted}\n`manage_guild`')
      await ctx.send(embed=embed)
      return
    if not channel:
      embed.add_field(name='Invalid Input', value='-setwelcome <ChannelMention>')
      await ctx.send(embed=embed)
      return
    print('2')
    with open('data/welcomes.json') as rfile:
      data = json.load(rfile)
    documented =True
    if channel:
      channel = channel.id
    for x in data:
      if int(x) == ctx.guild.id:
        documented=False
        data[x]["Channel"] = channel
    if documented:
      print('3')
      newdata ={
        "Channel": channel
      }
      data[str(ctx.guild.id)] = newdata
    print('5')
    with open('data/welcomes.json', 'w') as wfile:
      json.dump(data, wfile, indent=4)
    embed.add_field(name='Set welcome channel', value=f'Set welcome channel to {channel.mention}')
    await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(welcomecog(bot))