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

class KickCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def kick(self, ctx, user: discord.Member=None):
      if not ctx.author.guild_permissions.kick_members:
        await ctx.send('You dont have permission to use this command')
        return
      if not user:
        await ctx.send(f'Please specify a member - `{str(getprefix(ctx.guild))}kick <member> <reason>`')
        return
      if user.mention == ctx.message.author.mention:
        await ctx.send('You can\'t kick yourself')
        return
      if user.guild_permissions.kick_members:
        if ctx.author.top_role.position <= user.top_role.position:
          await ctx.send('You can\'t kick another moderator')
          return
      if user.bot:
        await ctx.send('You can\'t kick a bot')
        return
      print('starting')
      with open('data/setmodlog.json') as rfile:
        data = json.load(rfile)
        print('modlog')
        print('thispart')
        for x in data:
          print('startingfor')
          print(x)
          if int(x) == ctx.guild.id:
            if data[x][0]["ChannelId"]:
              channel = self.bot.get_channel(data[x][0]['ChannelId'])
              with open('data/moderation.json') as rfile:
                print('warning')
                data = json.load(rfile)
                global case
                try: 
                  case = len(data[x])
                  print(case)
                except Exception:
                  case = 0 # this is why
                documented = False
                embed=discord.Embed(color=0xffffa2)
                embed.set_author(name=f'Kick | Case #{case+1}')
                embed.set_footer(text=time.asctime(time.localtime(time.time())))
                embed.add_field(name='Member', value=f'{user.name} ({user.mention})')
                embed.add_field(name='Moderator', value=ctx.message.author)
                embed.add_field(name='Reason', value=f'`{str(getprefix(ctx.guild))}reason <CaseID> <reason>`')
                print('embed made')
                msg= await channel.send(embed=embed)
                print('setting')
                udata = {
                  "User": user.id,
                  "Reason": None,
                  "CaseId": case+1,
                  "Date": time.asctime(time.localtime(time.time())),
                  "Moderator": format(ctx.author),
                  "MessageId": msg.id
                }
                print('data')
                await ctx.message.delete()
                await user.kick()
                for x in data:
                  if str(ctx.guild.id) == x:
                    documented = True
                    data[str(ctx.guild.id)].append(udata)
                if not documented:
                  data[str(ctx.guild.id)] = [udata]
                with open('data/moderation.json', 'w') as wfile:
                  json.dump(data, wfile, indent=4)
            else:
              await user.kick()
              await ctx.send(f'Kicked {user}, if you want mod logs do `{str(getprefix(ctx.guild))}setmodlog <channel>`')

    @commands.command()
    async def reason(self, ctx, CaseId:int=None, *, reason:str=None):
      if not ctx.author.guild_permissions.kick_members:
        await ctx.send('You dont have permission to use this command')
        return
      if not CaseId:
        return
      if not reason:
        return
      with open('data/moderation.json') as rfile:
        data =json.load(rfile)
      couldfind=False
      pres = None
      for x in data:
        if int(x) == ctx.guild.id:
          for q in data[x]:
            if q['CaseId'] == CaseId:
              couldfind = True
              q['Reason'] = reason
              pres = q
      if not couldfind:
        await ctx.send(f"Could not find Case associated with CaseId: #{CaseId}")
      else:
        await ctx.message.delete()
        with open('data/moderation.json', 'w') as wfile:
          json.dump(data, wfile, indent=4)
        with open('data/setmodlog.json') as rfile:
          data = json.load(rfile)
        for x in data:
          if int(x) == ctx.guild.id:
            if data[x][0]['ChannelId']:
              channel = self.bot.get_channel(data[x][0]['ChannelId'])
          embed=discord.Embed(color=0xffffa2)
          embed.set_author(name=f'Kick | Case #{pres["CaseId"]}')
          embed.set_footer(text=pres["Date"])
          embed.add_field(name='Member', value=f'{self.bot.get_user(pres["User"]).name} ({self.bot.get_user(pres["User"]).mention})')
          embed.add_field(name='Moderator', value=f'{self.bot.get_user(pres["User"])}')
          embed.add_field(name='Reason', value=f'{pres["Reason"]}')
          themsg= await channel.fetch_message(pres["MessageId"])
          print(themsg)
          await themsg.edit(embed=embed)
        return

def setup(bot):
    bot.add_cog(KickCog(bot))