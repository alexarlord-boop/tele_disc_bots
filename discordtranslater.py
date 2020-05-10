import discord
import requests
from discord.ext import commands



bot = commands.Bot(command_prefix="!")

current_langs = 'ru-en'


def translate(lang, text):
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    apikey = 'trnsl.1.1.20200510T132635Z.3a54c096f064164d.35b1734400a3c0bd923eebf52428d50b58a64bfb'

    params = {
        'key': apikey,
        'text': text,
        'lang': lang
    }
    try:
        response = requests.get(url, params)
        response = response.json()['text'][0]
    except Exception:

        response = 'ошиб0чка'

    return response


class TranslateCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help_bot')
    async def help(self, ctx):
        await ctx.send('Я бот-переводчик. Для смены языка введи команду !set_lang и языки(например ru-en)\n'
                       'Для перевода введи команду !text и текст после нее.')

    @commands.command(name='set_lang')
    async def set_lang(self, ctx, languages):
        global current_langs
        current_langs = languages
        await ctx.send(current_langs)

    @commands.command(name='text')
    async def text(self, ctx, *txt):
        global current_langs
        txt = ' '.join(txt)
        res = translate(current_langs, txt)
        await ctx.send(res)


bot.add_cog(TranslateCommands(bot))

bot.run(TOKEN)
