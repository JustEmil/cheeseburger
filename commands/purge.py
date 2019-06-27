import discord
from discord.ext import commands
import errorcodes

class purgecog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command()
  async def purge(self, ctx, amt:int=10):
    # default is 10 messages if left blank
    embed=discord.Embed(colour=errorcodes.Colour)
    if not ctx.author.guild_permissions.manage_messages:
      embed.add_field(name='Restricted Access', value=f'{errorcodes.Restricted}\n`Manage_messages`')
      await ctx.send(embed=embed)
      return
    await ctx.channel.purge(limit=amt+1, check=None)
    return


def setup(bot):
  bot.add_cog(purgecog(bot))