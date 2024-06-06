import discord
from discord.ext import commands
import random
from restaurants import cities, restaurants, menus
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()


class MyBot(commands.Bot):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        if message.content == '?':
            await message.channel.send('?')
        
        if os.getenv('BOT_USER_ID') in message.content:
            await message.channel.send('Moro')
        await self.process_commands(message)


    
    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Heloust {member}'
            await guild.system_channel.send(to_send)

intents = discord.Intents.all()
intents.members = True        
client = MyBot(intents = intents,command_prefix = commands.when_mentioned_or('!'))

@client.command()
async def ping(ctx):
    await ctx.send(f'Ping {round(client.latency*1000)}ms')

@client.command()
async def roll(ctx):
    await ctx.send(random.randint(1,6))

@client.command()
async def vitsi(ctx):
    jokes = ['Mitä James Bond sanoi grillikioskilla?\n-Hampurilainen, kerroshampurilainen.',
            'Kaksi mummoa meni marjaan, mutta toinen ei mahtunut.',
            'Miksei voi sataa kahta päivää peräkkäin?\n-Yö on välissä.',
            'Mummo ja pappa pelasivat tennistä.\nPappa hävisi.\nEtsinnät jatkuvat yhä.',
            'Tarjoilija, tuokaa lasillinen appelsiinimehua.\n-Jäänkö kanssa?\n-Joo, voit sä jäädäkin.',
            'Pidetäänkö teillä mattoja lattialla?\n-Pidetään.\n-Meillä ne pysyy pitämättäkin.',
            'Kuka on Maija Mehiläisen isä?\nNo faija Mehiläinen',
            'Mikä on kirkasta ja haisee?\nKirkan pieru.']
    await ctx.send(random.choice(jokes))
@client.command()
async def vappu(ctx):
    await ctx.send("Wabu ei lobu :D")

@client.command()
async def ruoka(ctx):
    await ctx.send('Valitse kaupunki:\n' + '\n'.join([f'{i+1}. {city}' for i, city in enumerate(cities)]))
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit() and 0 < int(m.content) < len(cities)+1
    msg = await client.wait_for('message', check=check)
    city = int(msg.content)
    selected_city = restaurants[city-1]
    selected_menus = menus[city-1]
    
    printable_restaurants = '\n'.join([f'{i+1}. {restaurant}' for i, restaurant in enumerate(selected_city)])
    await ctx.send('Valitse ravintola:\n' + printable_restaurants)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit() and 0 < int(m.content) < len(selected_city)+1
    msg = await client.wait_for('message', check=check)
    selected_restaurant = printable_restaurants.split('\n')[int(msg.content) - 1].split('. ')[1]
    menu = selected_menus[int(msg.content) - 1]
    if menu == '':
        await ctx.send(f'Tänään ravontolassa {selected_restaurant} ei ole ruokaa tarjolla :(')
    else:
        await ctx.send(f'{selected_restaurant}\n{menu}')

client.run(os.getenv('BOT_CLIENT_KEY'))