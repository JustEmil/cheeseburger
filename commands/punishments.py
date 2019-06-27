import discord
from discord.ext import commands
import json

class punishmentscmd(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def punishments(self, ctx, user:discord.Member=None):
    if not ctx.author.guild_permissions.kick_members:
      await ctx.send("you do not have the required permissions\n`kick_members`")
      return
    if not user:
      await ctx.send('please specify a user\n`punishments [@mention]')
      return
    with open('data/warnings.json') as rfile:
      data = json.load(rfile)
    warnings=[]
    for x in data[str(ctx.guild.id)]:
      if x['User'] == user.id:
        warnings.append(x)
    if len(warnings) == 0:
      await ctx.send('User has no warns')
    embed = discord.Embed(colour=discord.Color.blue()) # change to what ever
    cm = ''
    for x in warnings:
      cm = cm + f"Reason: {x['Reason']}\nCaseId: {x['CaseId']}\n"
    embed.add_field(name='Warnings', value=cm)
    embed.add_field(name='Info', value= 'Remove warnings with command `-rwarn [CASEID]`')
    await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(punishmentscmd(bot))