import discord
from discord.ext import commands

import json

class prefix(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def setprefix(self, ctx, *, pre: str=None):

    if not ctx.author == ctx.guild.owner:
      await ctx.send('You dont have permission to use this command')

    else:
    
      if not pre:
        await ctx.send('Please specify a prefix')

      else:
        with open(r"data/prefixes.json", 'r') as f:
          prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = pre
        await ctx.send(f"New prefix is `{pre}`")
        guild = ctx.guild
        channel = self.bot.get_channel(592420327837925387)
        embed = discord.Embed(color=0xff6f6f)
        embed.add_field(name=':bell: New Prefix Change :bell:', value=f'Guild: {guild.name} ({guild.id})\nChanged By: {ctx.message.author} ({ctx.message.author.id})\nNew Prefix: {pre}', inline=False)
        await channel.send(embed=embed)


        with open(r"data/prefixes.json", 'w') as f:
          json.dump(prefixes, f, indent=4)
      

def setup(bot):
  bot.add_cog(prefix(bot))