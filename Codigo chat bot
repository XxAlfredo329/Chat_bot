import discord
from discord.ext import commands
import random
import asyncio

print('Para enviar comandos usa "//"')

def gen_pass(pass_length):
    elements = "1234567890abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNŇOPQRSTUVWXYZ+-/*!&$#?=@<>"
    password = ""
    for i in range(pass_length):
        password += random.choice(elements)
    return password

# 1. Creamos nuestra propia clase de Bot que hereda de commands.Bot
class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        # Inicia la tarea en segundo plano
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id}) - NuevoBot.py')
        print('------')

    async def my_background_task(self):
        await self.wait_until_ready()
        counter = 0
        # ¡IMPORTANTE! Reemplaza '1234567' por la ID real del canal de Discord
        channel = self.get_channel(1234567)  
        
        while not self.is_closed():
            counter += 1
            if channel:  # Verificamos que el canal exista para evitar errores
                await channel.send(counter)
            await asyncio.sleep(60)  # La tarea se ejecuta cada 60 segundos

# 2. Configuramos los intents y creamos la instancia de nuestro bot
intents = discord.Intents.default()
intents.message_content = True

bot = MyBot(command_prefix='//', intents=intents)

# 3. Añadimos todos los comandos usando @bot.command()
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hola, soy un bot {bot.user}!')

@bot.command()
async def heh(ctx, count_heh: int = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def saludo(ctx):
    await ctx.send("Hola Kenneth bienvenido a discord!")

@bot.command()
async def contraseña(ctx, num: int):
    await ctx.send(f"Tu contraseña es {gen_pass(num)}")

@bot.command()
async def suma(ctx, num1: int, num2: int):
    resultado = num1 + num2
    await ctx.send(f"La suma es {resultado}")

@bot.command()
async def division(ctx, num1: int, num2: int):
    # Corregido: antes restaba
    resultado = num1 / num2
    await ctx.send(f"La division es {resultado}")

@bot.command()
async def resta(ctx, num1: int, num2: int):
    # Corregido: antes dividía
    resultado = num1 - num2
    await ctx.send(f"La resta es {resultado}")

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    # Corregido: Faltaba enviar el mensaje con el resultado
    await ctx.send(f"Resultados: {result}")

@bot.command()
async def comandos(ctx):
    # Corregido: Formato de envío en un solo mensaje de texto
    lista = (
        "**Lista de comandos:**\n"
        "`//hello`\n"
        "`//heh`\n"
        "`//saludo`\n"
        "`//contraseña <numero>`\n"
        "`//suma <num1> <num2>`\n"
        "`//resta <num1> <num2>`\n"
        "`//division <num1> <num2>`\n"
        "`//roll <NdN>`"
    )
    await ctx.send(lista)

# 4. Corremos el bot
bot.run("TU_TOKEN_AQUI")
