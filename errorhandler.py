import discord
from discord.ext import commands
import asyncio
import traceback

class errorhandler(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if hasattr(ctx.command, 'on_error'):
      return
    ignored = (commands.CommandNotFound, commands.UserInputError, asyncio.TimeoutError, discord.NotFound)
    error = getattr(error, 'original', error)
    if isinstance(error, ignored):
      return
    if isinstance(error, commands.BotMissingPermissions):
      embed = discord.Embed(
        colour=discord.Color.red()
      )
      embed.add_field(name='Error', value=format(error))
      await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(errorhandler(bot))