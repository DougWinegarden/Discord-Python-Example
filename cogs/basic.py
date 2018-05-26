import discord
from discord.ext import commands
import math

import sqlite3
sqlite_file = "C:/Users/d3win/Documents/Discord Bot/Discord-Python-Example/discatchi.db"

img_file = "C:/Users/d3win/Documents/Discord Bot/Discord-Python-Example/img/"
boop_img = img_file + "cat_grey_boop.png"
walk_img = img_file + "cat_grey_walk.png"
cat_img = img_file + "cat_grey.png"


from datetime import datetime  
from datetime import timedelta  


# discord.py calls groups of commands cogs
# cogs can also be handlers for different types of events
# and respond to changes in data as they happen

#user_list = []
start_money = 75

#cooldowns are in seconds
walk_cd = 5 * 60
boop_cd = 30

"""
# setup
class BasicCog:
    def __init__(self, bot):
        self.bot = bot

    # ping command
    @commands.command()
    async def ping(self, ctx):
        # replies back to the command context with the
        # text "Pong!"
        await ctx.send("Pong!")
        
class TestCog:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def test(self, ctx):
        await ctx.send(user_list)
        

class ResponseCog:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def respond(self, ctx):
        await ctx.send("hey " + ctx.author.mention + "!")
"""

#list users
class ListCog:
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def list(self, ctx, arg):
        if arg == "users":
            conn = createConnection (sqlite_file)
            c = conn.cursor()
            """
            msg = "Users: "
            for i in range(len(user_list)):
                if user_list[i].guild == ctx.author.guild:
                    msg += user_list[i].name + ", "
                    """
            #query database for users in the same guild as author
            #SELECT username from USER u where u.guild_id = author.guild.id
            c.execute("SELECT username from USER where user_guild_id = '" + str(ctx.author.guild.id) + "'")
            query = c.fetchall()
            msg = "Users: "
            for i in range(len(query)):
                a = str(query[i])
                b = a[2:len(a) - 3]
                msg += b
                if i < len(query) - 1:
                    msg += ", "
            await ctx.send(msg)

            
            conn.commit()
            conn.close()
        else:
            await ctx.send("invalid argument");

#list users
class StartCog:
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def start(self, ctx):
        if addUser(ctx):
            await ctx.send("Welcome to Discatchi! What kind of pet would you like to adopt today? " +
                           "Type !help to get started.")

        else:
            await ctx.send("You've already started")



def createConnection (sqlite_file):
    try:
        conn = sqlite3.connect(sqlite_file)
        return conn
    except Error as e:
        print(e)

    return none

def addUser(ctx):
    author = ctx.author
    #user_list.append(author)

    #conn = sqlite3.connect(sqlite_file)
    conn = createConnection (sqlite_file)
    c = conn.cursor()

    #print(author.guild)

    try:
        c.execute("INSERT INTO SERVER (guild_id) VALUES (" + str(author.guild.id) + ")")
    except sqlite3.IntegrityError:
        print('ERROR: ID already exists in SERVER guild_id column {}')

    try:
        params = (str(author.id), str(author.name), author.discriminator, str(author.guild.id), start_money)
        c.execute("INSERT INTO USER VALUES (?, ?, ?, ?, ?)", params)
    except sqlite3.IntegrityError:
        print('ERROR: ID already exists in USER member_id column {}')
        return False

    conn.commit()
    conn.close()
    
    addPet("Kyle", "cat", "calico", ctx)
    
    
    return True


def addPet(name, species, color, ctx):
    author = ctx.author
    
    conn = createConnection (sqlite_file)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) from PET where pet_owner_id = '" + str(author.id) + "'")
    petcount = c.fetchall()[0]
    
    params = (
        str(author.id) + "_" + str(petcount),
        str(name),
        str(species),
        str(color),
        1, #lvl
        0, #exp
        
        0, #hap
        0, #enr
        0, #app
        0, #full

        5,
        5,
        5,
        5,

        '2007-01-01 10:00:00.00',
        '2007-01-01 10:00:00.00',
        '2007-01-01 10:00:00.00',
        '2007-01-01 10:00:00.00',
        '2007-01-01 10:00:00.00',
        '2007-01-01 10:00:00.00',

        str(author.id)
        )

    s = "INSERT INTO PET VALUES ("
    for i in range(20):
        s += "?, "
    s += "?)"

    print(s)
    c.execute(s, params)

    conn.commit()
    conn.close()
    
    #try:
       # c.execute(s, params)
    #except:
     #   print('I tried to enter a new pet but Im too stupid')
    
"""
def initUsers():
    conn = sqlite3.connect(sqlite_file)
    #this needs to initialize the list of users from
    # what is pulled from the backend
    conn.commit()
    conn.close()
"""

class WalkCog:
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def walk(self, ctx, *arg):
        #arg is pet name
        #try:
        conn = createConnection (sqlite_file)
        c = conn.cursor()

        
        now = datetime.now()
        c.execute("SELECT last_walk from PET where pet_owner_id = '" + str(ctx.author.id) + "' " +
                      "AND pet_name = '" + str(arg[0]) + "'")
        last_walk = str(c.fetchall()[0])
        lw = last_walk[2:len(last_walk) - 6]
        print("last walk: " + lw)

        lw_t = datetime.strptime(lw, "%Y-%m-%d %H:%M:%S")
        
        if now - timedelta(seconds=walk_cd) > lw_t:
            await ctx.send("walking " + str(arg[0]) + "!")

            with open(walk_img, 'rb') as f:
                await ctx.channel.send("", file=discord.File(f,walk_img))
            
            #update walk in pet attribute to date.now
            
            snow = str(now)
            s = snow[:len(snow) - 4]
            #print(str(now))
            print("current time: " + s)

            c.execute("UPDATE PET SET last_walk = '" + s + "' where pet_owner_id = '" + str(ctx.author.id) + "' " +
                      "AND pet_name = '" + str(arg[0]) + "'")
            

            
        else:
            await ctx.send("Couldn't walk " + str(arg[0]) + " because it hasn't been 5 minutes")

        conn.commit()
        conn.close()
        #except:
            #await ctx.send("Please specify a valid pet. ex: \"!walk Kyle\"")

        
class BoopCog:
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def boop(self, ctx, *arg):
        #arg is pet name
        #try:
        conn = createConnection (sqlite_file)
        c = conn.cursor()

        
        now = datetime.now()
        c.execute("SELECT last_boop from PET where pet_owner_id = '" + str(ctx.author.id) + "' " +
                      "AND pet_name = '" + str(arg[0]) + "'")
        last_boop = str(c.fetchall()[0])
        lb = last_boop[2:len(last_boop) - 6]
        #print("last walk: " + lw)

        lb_t = datetime.strptime(lb, "%Y-%m-%d %H:%M:%S")
        
        if now - timedelta(seconds=boop_cd) > lb_t:
            await ctx.send("booping " + str(arg[0]) + "!")

            with open(cat_img, 'rb') as f:
                await ctx.channel.send("", file=discord.File(f,cat_img))
            
            #update walk in pet attribute to date.now
            
            snow = str(now)
            s = snow[:len(snow) - 4]
            #print(str(now))
            #print("current time: " + s)

            c.execute("UPDATE PET SET last_boop = '" + s + "' where pet_owner_id = '" + str(ctx.author.id) + "' " +
                      "AND pet_name = '" + str(arg[0]) + "'")
            

            
        else:
            await ctx.send("Couldn't boop " + str(arg[0]) + " because it hasn't been 30 seconds")

        conn.commit()
        conn.close()

# add this cog to the bot
def setup(bot):
    #bot.add_cog(ResponseCog(bot))
    #bot.add_cog(TestCog(bot))
    bot.add_cog(StartCog(bot))
    bot.add_cog(ListCog(bot))
    bot.add_cog(WalkCog(bot))
    bot.add_cog(BoopCog(bot))
