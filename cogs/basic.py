import discord
from discord.ext import commands
import math

import sqlite3
sqlite_file = "C:/Users/d3win/Documents/Discord Bot/Discord-Python-Example/discatchi.db"


# discord.py calls groups of commands cogs
# cogs can also be handlers for different types of events
# and respond to changes in data as they happen

user_list = []

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
        if addUser(ctx.author):
            await ctx.send("...")

        else:
            await ctx.send("You've already started")

def createConnection (sqlite_file):
    try:
        conn = sqlite3.connect(sqlite_file)
        return conn
    except Error as e:
        print(e)

    return none

def addUser(author):
    user_list.append(author)

    #conn = sqlite3.connect(sqlite_file)
    conn = createConnection (sqlite_file)
    c = conn.cursor()

    #print(author.guild)

    try:
        c.execute("INSERT INTO SERVER (guild_id) VALUES (" + str(author.guild.id) + ")")
    except sqlite3.IntegrityError:
        print('ERROR: ID already exists in SERVER guild_id column {}')

    try:
        params = (str(author.id), str(author.name), author.discriminator, str(author.guild.id))
        c.execute("INSERT INTO USER VALUES (?, ?, ?, ?)", params)
    except sqlite3.IntegrityError:
        print('ERROR: ID already exists in USER member_id column {}')
        return False
    
    conn.commit()
    conn.close()
    return True
    
"""
def initUsers():
    conn = sqlite3.connect(sqlite_file)
    #this needs to initialize the list of users from
    # what is pulled from the backend
    conn.commit()
    conn.close()
"""

# add this cog to the bot
def setup(bot):
    bot.add_cog(ResponseCog(bot))
    bot.add_cog(TestCog(bot))
    bot.add_cog(StartCog(bot))
    bot.add_cog(ListCog(bot))
