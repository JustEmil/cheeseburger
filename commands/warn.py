import discord
from discord.ext import commands
import json
import time
import errorcodes
class WarnCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def warn(self, ctx, user: discord.Member=None, *, reason:str=None):
    if not ctx.author.guild_permissions.kick_members:
      embed=discord.Embed(colour=errorcodes.Colour)
      embed.add_field(name='Restricted Access', value=f'{errorcodes.Restricted}\n`kick_members`')
      await ctx.send(embed=embed)
      return
    if not user:
      embed = discord.Embed(colour=0xff8080)
      embed.add_field(name='Error', Value='Please specify a member')
      await ctx.send(embed=embed)
      return
    if user.bot:
      await ctx.send('You can\'t warn bots.')
      return
    if user.guild_permissions.kick_members:
      if ctx.author.top_role.position <= user.top_role.position:
        embed=discord.Embed(colour=errorcodes.Colour)
        embed.add_field(name='Restricted', value='You cannot ban another moderator with the same permission')
        await ctx.send(embed=embed)
        return
    if not reason:
      reason = 'Unspecified Reason'
    with open('data/warnings.json') as rfile:
      data = json.load(rfile)
      try:
        cases = len(data[str(ctx.guild.id)])
      except Exception:
        cases=0
    isdocumented=False
    newdata = {
      "User": user.id,
      "Reason": reason,
      "CaseId": cases+1,
      "Date": time.asctime(time.localtime(time.time())),
      "Moderator": format(ctx.author),
    }
    for x in data:
      print(x)
      if str(ctx.guild.id) == x:
        isdocumented = True
        print('adding')
        # subdict=data[str(ctx.guild.id)]
        # templist = []
        # for i,v in temp.iteritems():
        #   new=[i,v]
        #   templist.append(new)
        data[str(ctx.guild.id)].append(newdata)
        # data[str(ctx.guild.id)] = templist
        print('added')
    if not isdocumented:
      data[str(ctx.guild.id)] = [newdata]
      print('adding2')
    with open('data/warnings.json', 'w') as wfile:
      json.dump(data, wfile, indent=4)
      print('dump')
    embed = discord.Embed(colour=0xff8080)
    embed.add_field(name='Warned {}!'.format(user), value='Reason: **{}**\nCaseId: **{}**\n\nDate: **{}**'.format(reason, newdata["CaseId"], time.asctime(time.localtime(time.time()))))
    embed.set_footer(text='Moderator actions are stored on the players profile card')
    await ctx.send(embed=embed)
  @commands.command()
  async def rwarn(self, ctx, caseid:int=None):
    embed=discord.Embed(colour=errorcodes.Colour)
    if not ctx.author.guild_permissions.kick_members:
      embed.add_field(name='Restricted Access', value=f'{errorcodes.Restricted}\n`kick_members``')
      await ctx.send(embed=embed) 
      return
    if not caseid:
      embed.add_field(name='Invalid Input', value=f'-rwarn <CaseId>')
      await ctx.send(embed=embed)
      return
    couldfind=False
    with open('data/warnings.json') as rfile:
      data = json.load(rfile)
    pres = None
    for x in data:
      print(x)
      if int(x) == ctx.guild.id:
        for q in data[x]:
          if q['CaseId'] == caseid:
            couldfind=True
            pres = q
            data[x].remove(q)
    if couldfind:
      with open('data/warnings.json', 'w') as wfile:
        json.dump(data, wfile, indent=4)
      embed.add_field(name='Warning', value=f'Removed:\nUser: {self.bot.get_user(pres["User"])}\nReason: {pres["Reason"]}\nCaseId: {pres["CaseId"]}')
      await ctx.send(embed=embed)
    else:
      embed.add_field(name='Warning', value=f'Could not find warning associated with CaseId: {caseid}')
      await ctx.send(embed=embed)
  @commands.command()
  async def ewarn(self, ctx, caseid:int=None, *, reason:str=None):
    embed=discord.Embed(colour=errorcodes.Colour)
    if not ctx.author.guild_permissions.kick_members:
      embed.add_field(name='Restricted Access', value=f'{errorcodes.Restricted}\n`kick_members`')
      await ctx.send(embed=embed)
      return
    if not caseid:
      embed.add_field(name='Invalid Input', value=f'-ewarn <caseid> <NewReason>')
      await ctx.send(embed=embed)
      return
    if not reason:
      embed.add_field(name='Invalid Input', value='-ewarn <caseid> <NewReason>')
      await ctx.send(embed=embed)
      return
    with open('data/warnings.json') as rfile:
      data =json.load(rfile)
    couldfind=False
    pres = None
    for x in data:
      if int(x) == ctx.guild.id:
        for q in data[x]:
          if q['CaseId'] == caseid:
            couldfind = True
            q['Reason'] = reason
            pres = q
    if not couldfind:
      embed.add_field(name='Warnings', value='Could not find warning associated with caseid: {}'.format(caseid))
      await ctx.send(embed=embed)
      return
    else:
      with open('data/warnings.json', 'w') as wfile:
        json.dump(data, wfile, indent=4)
      embed.add_field(name=format(self.bot.get_user(pres['User'])), value=f'Reason: {pres["Reason"]}\nCaseId: {pres["CaseId"]}\nDate: {pres["Date"]}\nModerator: {pres["Moderator"]}')
      await ctx.send(embed=embed)
      return

      

def setup(bot):
  bot.add_cog(WarnCog(bot))
