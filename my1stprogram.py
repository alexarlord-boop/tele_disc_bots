import discord
import random
import schedule
import datetime
from discord.ext import commands, timers



bot = commands.Bot(command_prefix="!")
bot.timer_manager = timers.TimerManager(bot)


@bot.command(name="remind")
async def remind(ctx, time, *, text):
    time = datetime.datetime(*map(int, time.split("/")))

    bot.timer_manager.create_timer("reminder", time, args=(ctx.channel.id, ctx.author.id, text))
    # or without the manager
    timers.Timer(bot, "reminder", time, args=(ctx.channel.id, ctx.author.id, text)).start()


@bot.event
async def on_reminder(channel_id, author_id, text):
    channel = bot.get_channel(channel_id)

    await channel.send("Hey, <@{0}>, remember to: {1}".format(author_id, text))


bot.run(TOKEN)
