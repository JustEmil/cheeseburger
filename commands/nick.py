import discord
from discord.ext import commands
import errorcodes

class nickcog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def nick(self, ctx, member:discord.Member=None, name:str=None):
    embed=discord.Embed(colour=errorcodes.Colour)
    if not ctx.author.guild_permissions.manage_nicknames:
      embed.add_field(name='Restricted Access', value=f'{errorcodes.Restricted}\n`Manage_nicknames`')
      await ctx.send(embed=embed)
      return
    if not member:
      embed.add_field(name='Invalid Input', value='`-nick <Mention> <Nickname>`')
      await ctx.send(embed=embed)
      return
    oldname = member.display_name
    await member.edit(nick=name)
    embed.add_field(name='Nickname', value=f'User: {member}\n\nNew Nickname: {name}\nOld Nickname: {oldname}')
    await ctx.send(embed=embed)
    

def setup(bot):
  bot.add_cog(nickcog(bot))