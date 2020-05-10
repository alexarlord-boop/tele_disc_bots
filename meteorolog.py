import discord
import requests
from discord.ext import commands
import geocoder



bot = commands.Bot(command_prefix="!")

current_latlng = [39.7837304, -100.4458825]
def get_latlng(place):
    latlng = geocoder.location(place).latlng
    return latlng


def get_weather(latlng, days=1): # no parsing yet + no weather-api access
    url = 'https://api.weather.yandex.ru/v1/forecast/'
    apikey = '68cff375-4aab-4f83-85fc-3886b4d93c24'
    lat, lng = latlng
    params = {
        'X-Yandex-API-Key': apikey,
        'lat': lat,
        'lon': lng,  # < долгота >
        'lang': 'ru_RU',
        'limit': days
    }
    try:
        response = requests.get(url, params)
        response = response.json()
    except Exception:

        response = 'ошиб0чка'

    return response


class Weather(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help_bot')
    async def help(self, ctx):
        await ctx.send('Я бот-метеоролог.'
                       '\nКоманда !place задает место прогноза.'
                       '\nКоманда !current присылает сообщение о текущей погоде.'
                       '\nКоманда !forecast {days} сообщает прогноз дневной температуры и осадков'
                       ' на указанное количество дней.')

    @commands.command(name='place')
    async def place(self, ctx, new_place):
        global current_latlng
        current_latlng = get_latlng(new_place)
        await ctx.send(f'Место изменено на {new_place}\n{current_latlng}')

    @commands.command(name='current')
    async def current(self, ctx):
        global current_latlng
        res = get_weather(current_latlng)
        await ctx.send(res)

    @commands.command(name='forecast'):
    async def forecast(self, ctx, days):
        global current_latlng
        res = get_weather(current_latlng, days)
        await ctx.send(res)

bot.add_cog(Weather(bot))

bot.run(TOKEN)
