import discord

import random
from discord.ext import commands, timers

TOKEN = "NzA5MDkyOTUyODczNjMxNzQ0.Xrg4gA.KzZI3St1y0A6DK32ABIxIafiQbw"


class EmojiBotClient(discord.Client):
    def __init__(self):
        super().__init__()
        self.game_emoji = ['☺', '☹', '😈', '😎', '😸', '😺', '🚁', '🚟', '❤', '🌷']
        self.emoji = self.game_emoji.copy()
        self.user_score = 0
        self.bot_score = 0
        print(self.emoji)

    def get_i(self, i):
        if i > len(self.emoji) != 0:
            i = i % len(self.emoji)
        return i - 1

    def delemoji(self, u_i, b_i):
        if u_i < b_i:
            self.emoji.__delitem__(u_i)
            self.emoji.__delitem__(b_i - 1)
        elif u_i > b_i:
            self.emoji.__delitem__(u_i)
            self.emoji.__delitem__(b_i)
        else:
            self.emoji.__delitem__(u_i)

    def gpoints(self, u, b):
        u = ord(u)
        b = ord(b)

        if u > b:
            self.user_score += 1
        elif b > u:
            self.bot_score += 1

    def gemoji(self, u_i, b_i):
        print(u_i, b_i)
        user_c = self.emoji[u_i]
        bot_c = self.emoji[b_i]
        self.delemoji(u_i, b_i)
        self.gpoints(user_c, bot_c)

        print(self.emoji)

        return [user_c, bot_c]

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    async def on_message(self, message):
        if message.author == self.user:
            return
        if "привет" in message.content.lower():
            await message.channel.send("И тебе привет")
        else:  # only int

            if '/stop' in message.content.lower():
                self.user_score = 0
                self.bot_score = 0
                self.emoji = self.game_emoji.copy()
            else:
                u_i = self.get_i(int(message.content))
                seq = [i for i in range(len(self.emoji)) if i != u_i]
                if seq == []:

                    self.emoji = self.game_emoji.copy()

                    if self.user_score > self.bot_score:
                        mess = 'You win!'
                    elif self.user_score < self.bot_score:
                        mess = 'Bot win!'
                    else:
                        mess = 'Draw!'
                    await message.channel.send(f"SCORE: You-{self.user_score} Bot-{self.bot_score}"
                                               f"\n{mess}")  # победа + результаты
                    self.user_score = 0
                    self.bot_score = 0

                else:
                    bot_i = random.choice(seq)
                    game = self.gemoji(u_i, bot_i)

                    await message.channel.send(f"Your emoji: {game[0]}"
                                               f"\nBot emoji: {game[1]}"
                                               f"\nSCORE: You-{self.user_score} Bot-{self.bot_score}")  # смайлы и очки


client = EmojiBotClient()
client.run(TOKEN)
