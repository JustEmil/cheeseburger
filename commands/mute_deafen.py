import discord
from discord.ext import commands
import errorcodes

class voicecog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def mute(self, ctx, member:discord.Member=None):
    embed=discord.Embed(colour=errorcodes.Colour)
    if not ctx.author.guild_permissions.mute_members:
      embed.add_field(name='Restricted Access', value=f'{errorcodes.Restricted}\n`Mute_Members`')
      await ctx.send(embed=embed)
      return
    if not member:
      embed.add_field(name='Invalid Input', value='`-mute <Mention>`\nVoice mute')
      await ctx.send(embed=embed)
      return
    embed.add_field(name='Mute', value=f'User: {member}\nModerator: {ctx.author}')
    await member.edit(mute=True)
    await ctx.send(embed=embed)
  @commands.command()
  async def unmute(self, ctx, member:discord.Member=None):
    embed=discord.Embed(colour=errorcodes.Colour)
    if not ctx.author.guild_permissions.mute_members:
      embed.add_field(name='Restricted Access', value=f'{errorcodes.Restricted}\n`Mute_Members`')
      await ctx.send(embed=embed)
      return
    if not member:
      embed.add_field(name='Invalid Input', value='`-unmute <Mention>`\nVoice mute')
      await ctx.send(embed=embed)
      return
    embed.add_field(name='Unmute', value=f'User: {member}\nModerator: {ctx.author}')
    await member.edit(mute=False)
    await ctx.send(embed=embed)
  @commands.command()
  async def deafen(self, ctx, member:discord.Member=None):
    embed=discord.Embed(colour=errorcodes.Colour)
    if not ctx.author.guild_permissions.deafen_members:
      embed.add_field(name='Restricted Access', value=f'{errorcodes.Restricted}\n`Mute_Members`')
      await ctx.send(embed=embed)
      return
    if not member:
      embed.add_field(name='Invalid Input', value='`-deafen <Mention>`\nVoice mute')
      await ctx.send(embed=embed)
      return
    embed.add_field(name='Deafen', value=f'User: {member}\nModerator: {ctx.author}')
    await member.edit(deafen=True)
    await ctx.send(embed=embed)
  @commands.command()
  async def undeafen(self, ctx, member:discord.Member=None):
    embed=discord.Embed(colour=errorcodes.Colour)
    if not ctx.author.guild_permissions.deafen_members:
      embed.add_field(name='Restricted Access', value=f'{errorcodes.Restricted}\n`Mute_Members`')
      await ctx.send(embed=embed)
      return
    if not member:
      embed.add_field(name='Invalid Input', value='`-undeafen <Mention>`\nVoice mute')
      await ctx.send(embed=embed)
      return
    embed.add_field(name='Undeafen', value=f'User: {member}\nModerator: {ctx.author}')
    await member.edit(deafen=False)
    await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(voicecog(bot))