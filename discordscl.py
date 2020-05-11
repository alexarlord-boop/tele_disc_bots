import pymorphy2
from discord.ext import commands

TOKEN = "NzA5MDkyOTUyODczNjMxNzQ0.XrmKyA.NuzKhMblBFhhr580p0savfN_AEA"
morph = pymorphy2.MorphAnalyzer()


class MorphBotClient(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help_bot')
    async def help(self, ctx):
        await ctx.send(f"Команды:"
                       f"\n!numerals для согласования слов с числительными"
                       f"\n!alive для определения одушевленности"
                       f"\n!noun для склонения"
                       f"\n!inf для образования начальной формы слова"
                       f"\n!morph для полного морфологического анализа")

    @commands.command(name='numerals')
    async def numerals(self, ctx, word, num):
        word = morph.parse(word)[0]
        word = word.make_agree_with_number(int(num)).word
        await ctx.send(f"{num} {word}")

    @commands.command(name='alive')
    async def alive(self, ctx, noun):
        word = morph.parse(noun)[0]
        if word.tag.POS == 'NOUN':
            if word.tag.animacy == 'anim':
                await ctx.send('одушевленнное')
                return
            await ctx.send('неодушевленнное')
        else:
            await ctx.send('Ваш запрос не содержит существительное.')

    @commands.command(name='noun')
    async def noun(self, ctx, noun, case, state):
        cases = {'и': 'nomn', 'р': 'gent', 'д': 'datv', 'в': 'accs', 'т': 'ablt', 'п': 'loct'}
        states = {'е': 'sing', 'м': 'plur'}
        word = morph.parse(noun)[0]
        word = word.inflect({cases[case], states[state]})[0]
        await ctx.send(word)

    @commands.command(name='inf')
    async def inf(self, ctx, noun):
        word = morph.parse(noun)[0].normal_form
        await ctx.send(word)

    @commands.command(name='morph')
    async def morph(self, ctx, noun):
        word_data = morph.parse(noun)[0]
        inf = word_data.normal_form
        await ctx.send(f"{inf}\n{word_data.tag}")


bot = commands.Bot(command_prefix='!')
bot.add_cog(MorphBotClient(bot))
bot.run(TOKEN)
