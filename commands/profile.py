import discord
from discord.ext import commands
import json

class profilecmd(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def profile(self, ctx, user:discord.Member=None):
    if not user:
      user = ctx.message.author
    with open('data/warnings.json') as rfile:
      data = json.load(rfile)
    cm='' # what to display for the users
    userdata =[]
    val=False
    amt2 = 0
    for x in data:
      if x == str(ctx.guild.id):
        val=True
    if val:
      for x in data[str(ctx.guild.id)][::-1]:
        if x['User'] == user.id:
          userdata.append(x)
          amt2 = amt2 + 1
          if amt2 <=4:
            cm = cm + f'Reason: {x["Reason"]}\nDate: {x["Date"]}\nModerator: {x["Moderator"]}\nCaseId: {x["CaseId"]}\n\n' # gets reason and date
    else:
      cm = 'None'
    userprofile = discord.Embed(colour=discord.Color.red())
    userprofile.add_field(name='Account', value="Name: {}\nId: {}".format(user, user.id))
    userprofile.add_field(name='Creation Date', value=user.created_at)
    userprofile.set_thumbnail(url=user.avatar_url)
    if len(userdata) == 0: #if 0, then user has no warns
      userprofile.add_field(name='Warnings', value='None') #
      await ctx.send(embed=userprofile)
      return
    if len(userdata) >= 4:
      amt = len(userdata)-4
      userprofile.add_field(name='Warnings', value=cm + f'\n**{amt}+**')
      await ctx.send(embed=userprofile)
      return
    else:
      userprofile.add_field(name='Warnings', value=cm) # shows warns
      await ctx.send(embed=userprofile)
      return
      
      

def setup(bot):
  bot.add_cog(profilecmd(bot))