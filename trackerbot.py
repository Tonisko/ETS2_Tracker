import discord
from discord.ext import commands
import sqlite3

bot = commands.Bot(command_prefix='a!')


@bot.command()
async def stats(ctx):
    conn = sqlite3.connect('trackerlog.db')
    c = conn.cursor()
    dist = []
    fuel = []
    weight = []
    avg = []
    for row in c.execute("SELECT * FROM {}".format(ctx.author.name + ctx.author.discriminator)):
        list.append(dist, row[6])
        list.append(fuel, row[7])
        list.append(weight, row[4])
        list.append(avg, row[8])
    totald = sum(dist)
    totalf = sum(fuel)
    totalw = sum(weight) / 1000
    avgc = sum(avg) / len(avg)
    _totald = round(totald, 2)
    _totalw = round(totalw)
    _avgc = round(avgc)
    e = discord.Embed(title=f"{ctx.author.name}'s statistics", description=f"""Total distance: **{_totald} km**
Total weight transported: **{_totalw} tons**
Total fuel burned: **{totalf} litres**
Average delivery consumption: **{_avgc} l/100km**""", color=0xa9181c)
    await ctx.send(embed=e)


@bot.command()
async def logbook(ctx):
    conn = sqlite3.connect('trackerlog.db')
    c = conn.cursor()
    e = discord.Embed(title=f"{ctx.author.name}'s logbook", color=0xa9181c)
    e.set_footer(text='Alpha version, possible improvement soon')
    index = 0
    for row in c.execute("SELECT * FROM {}".format(ctx.author.name + ctx.author.discriminator)):
        index += 1
        dist = round(row[6])
        e.add_field(name=str(index), value='{} \u200b **->** \u200b {} \u200b **|** \u200b {} km \u200b **|** \u200b {} l \u200b **|** \u200b {} hrs, {} min'.format(row[2], row[3], dist, row[7], row[9], row[10]), inline=False)
    await ctx.send(embed=e)


bot.run('token')
