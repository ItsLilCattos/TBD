import discord
from discord.ext import commands
import math
import sqlite3
import aiosqlite
from discord.ext.commands import BucketType, cooldown
from discord.ext.commands import Context, Paginator



#the discord blue color 
THEME1 = 0x7289da

#the discord gray color 
THEME2 = 0x99aab5

#the discord black color
THEME3 = 0x23272a


xpdb = aiosqlite.connect("level.sqlite3")
# xpdb = sqlite3.connect('level.sqlite3')
# cursor = xpdb.cursor()
# cursor.execute("""CREATE TABLE IF NOT EXISTS levels(
#     unique_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     guild_id BIGINT,
#     user_id BIGINT,
#     lvl INTEGER NOT NULL,
#     exp INTEGER NOT NULL
# )""")




class XP(commands.Cog):
    '''Xp here you can set the xp see level , leaderboard .. '''
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
      await xpdb

      cursor = await xpdb.cursor()
      await cursor.execute("""CREATE TABLE IF NOT EXISTS levels(
        unique_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id BIGINT,
        lvl INTEGER NOT NULL,
        exp INTEGER NOT NULL
)""")
      await xpdb.commit()


    @commands.Cog.listener()
    async def on_message(self, message):
        cursor = await xpdb.cursor()


        if message.author.bot:
            return
        

        await cursor.execute(f"SELECT user_id FROM levels WHERE user_id = {message.author.id}")
        result = await cursor.fetchone()
        if result is None:
            await cursor.execute("INSERT INTO levels(user_id,lvl,exp) VALUES(?,?,?)", (message.author.id, 1, 5))
            await xpdb.commit()
        else:
            await cursor.execute(f"SELECT * FROM levels WHERE user_id = {message.author.id}")
            info = await cursor.fetchone()

            exp = int(info[3])

            await cursor.execute(f"UPDATE levels SET exp = {exp+5} WHERE  user_id = {message.author.id}")
            
            await cursor.execute(f"SELECT user_id, lvl, exp FROM levels WHERE  user_id = {message.author.id}")
            result2 = await cursor.fetchone()

            exp +=5
            lvl_start = int(info[2])
            

            xp_end = math.floor((5 * (lvl_start^2) + (50 * lvl_start) + 100)-10)


            if exp >= xp_end:
            
                await message.channel.send(f"{message.author.mention} has leveled up to level {lvl_start+1}.")

                await cursor.execute(f"UPDATE levels SET exp=0, lvl=? WHERE user_id=?", (int(lvl_start+1), str(message.author.id)))
                val = await cursor.fetchone()

            await xpdb.commit()
            
                
                
    
    
    @commands.command()
    async def rank(self, ctx, user: discord.Member = None):
        print('mmmm')
        USER_ID = ctx.author.id
        cursor = await xpdb.cursor()
        if user is None:
          await cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE user_id = {USER_ID}")
          result = await cursor.fetchone()
          print(result)
          if not result:
            await cursor.execute("INSERT INTO levels(user_id,lvl,exp) VALUES(?,?,?)",(USER_ID, 1, 5))
            await xpdb.commit()

          await cursor.execute(
              f"SELECT user_id, lvl, exp FROM levels WHERE user_id = {USER_ID}")
          result2 = await cursor.fetchone()
          print(result2)

          if result2:
              print('uhhhh')

              exp = int(result2[2])
              lvl_start = int(result2[1])
              xp_end = math.floor(5 * (lvl_start ** 2) + 50 * lvl_start + 100)
              boxes = int((exp / (200 * ((1 / 2) * lvl_start))) * 20)

              lvl_start = int(result2[1])
              xp_end = math.floor(5 * (lvl_start ** 2) + 50 * lvl_start + 100)

              if result is None:
                  await ctx.send("That user is not yet ranked.")
              else:
                  print('yo')
                  em = discord.Embed(color=THEME1)
                  em.add_field(name=f"{ctx.author.name} Level's Table",
                              value=f"{ctx.author.name} is currently level `{lvl_start}` and has `{exp}/{int(xp_end)}XP!`")
                  em.add_field(name="Progress Bar", value=boxes * ":blue_square:" + (20 - boxes) * ":white_large_square:",
                              inline=False)
                  em.set_author(icon_url=ctx.author.avatar_url, name=ctx.author.name)
                  await ctx.send(embed=em)
        else:
          OTHER_ID = user.id
          await cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE user_id = {OTHER_ID}")
          result = await cursor.fetchone()
          print(result)
          if not result:
            await cursor.execute("INSERT INTO levels(user_id,lvl,exp) VALUES(?,?,?)",(OTHER_ID, 1, 5))
            await xpdb.commit()

          await cursor.execute(
              f"SELECT user_id, lvl, exp FROM levels WHERE user_id = {OTHER_ID}")
          result2 = await cursor.fetchone()
          print(result2)

          if result2:
              print('uhhhh')

              exp = int(result2[2])
              lvl_start = int(result2[1])
              xp_end = math.floor(5 * (lvl_start ** 2) + 50 * lvl_start + 100)
              boxes = int((exp / (200 * ((1 / 2) * lvl_start))) * 20)

              lvl_start = int(result2[1])
              xp_end = math.floor(5 * (lvl_start ** 2) + 50 * lvl_start + 100)

              if result is None:
                  await ctx.send("That user is not yet ranked.")
              else:
                  print('yo')
                  em = discord.Embed(color=THEME1)
                  em.add_field(name=f"{user.name} Level's Table",
                              value=f"{user.name} is currently level `{lvl_start}` and has `{exp}/{int(xp_end)}XP!`")
                  em.add_field(name="Progress Bar", value=boxes * ":blue_square:" + (20 - boxes) * ":white_large_square:",
                              inline=False)
                  em.set_author(icon_url=user.avatar_url, name=ctx.author.name)
                  await ctx.send(embed=em)


    @commands.command()
    async def top(self, ctx):
      cursor = await xpdb.cursor()

      await cursor.execute(
            f"SELECT user_id, lvl, exp from levels ORDER BY lvl + 0 DESC LIMIT 5")
      end = await cursor.fetchall()

      em = discord.Embed(title=":speech_left: Most active users :speech_left:", color=THEME1)

      
      for i, x in enumerate(end, 1):
        print(x)
        em.add_field(name=f"#{i}", value=f"<@{x[0]}> on level {x[1]} with {x[2]} total exp", inline=False)
      await ctx.send(embed=em)
       
        
        
        
    
    
def setup(bot):
    bot.add_cog(XP(bot))
    print("-----( Levels is ready! )-----")