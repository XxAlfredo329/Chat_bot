import discord
from discord.ext import commands
import random
import asyncio
import os
import requests

print('Para enviar comandos usa "//" - NuevoBot.py:8')

def gen_pass(pass_length):
    elements = "1234567890abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNŇOPQRSTUVWXYZ+-/*!&$#?=@<>"
    password = ""
    for i in range(pass_length):
        password += random.choice(elements)
    return password

# 1. Clase de Bot que hereda de commands.Bot
class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        # Inicia la tarea en segundo plano
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id}) - NuevoBot.py:27')
        print('')

    async def my_background_task(self):
        await self.wait_until_ready()
        counter = 0
        # Reemplaza '1544458069029953658' por la ID de tu canal
        channel = self.get_channel(1544458069029953658)  
        
        while not self.is_closed():
            counter += 1
            if channel:
                await channel.send(counter)
            await asyncio.sleep(60)

# 2. Configuración de intents e instancia del bot
intents = discord.Intents.default()
intents.message_content = True

bot = MyBot(command_prefix='//', intents=intents)

# Diccionario de desafíos
Desafios = {
    1: "Reciclar 10 botellas de plástico",
    2: "No uses botellas de plástico innecesariamente",
    3: "Encontrar 3 botellas de plástico tiradas",
    4: "Haz una manualidad usando botellas de plástico!",
    5: "Empezar a usar bolsas biodegradables",
    6: "Convertir una botella en una maceta",
    7: "Crea una hoja de papel usando materiales naturales"
}

# Función para obtener imágenes de Openverse (sin API Key necesaria)
def get_pollution_image():
    url = "https://api.openverse.org/v1/images/"
    params = {
        "q": "plastic pollution landscape",
        "page_size": 20
    }
    headers = {
        "User-Agent": "DiscordBotContaminacion/1.0"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                image = random.choice(results)
                return image["url"]
    except Exception as e:
        print(f"Error con Openverse API: {e}")
    
    # Imágenes de respaldo por si falla la conexión a la API
    fallback_images = [
        "https://images.unsplash.com/photo-1621451537084-482243006244?w=1200",
        "https://images.unsplash.com/photo-1618477461853-cf6ed80faba5?w=1200",
        "https://images.unsplash.com/photo-1530587191325-3db32d826c18?w=1200"
    ]
    return random.choice(fallback_images)

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

# 3. Comandos del Bot

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
    if num2 == 0:
        await ctx.send("No se puede dividir por 0")
    else:
        resultado = num1 / num2
        await ctx.send(f"La division es {resultado}")

@bot.command()
async def resta(ctx, num1: int, num2: int):
    resultado = num1 - num2
    await ctx.send(f"La resta es {resultado}")

@bot.command()
async def meme1(ctx):    
    with open("imagenes/meme 1.jpeg" , "rb") as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command()
async def memes(ctx): 
    img_name = random.choice(os.listdir("imagenes"))
    with open(f"imagenes/{img_name}", "rb") as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(f"Resultados: {result}")

@bot.command('duck')
async def duck(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command()
async def animal(ctx):
    with open("animales/animal.png", "rb") as f:
        picture = discord.File(f)
    await ctx.send(file=picture)

@bot.command('CalculateBlock')
async def CalculateBlock(ctx, Volume):
    try:
        bloques = int(Volume) / 9
        await ctx.send(f"La cantidad de bloques que puedes crear con {Volume} m³ son: {bloques}")
    except ValueError:
        await ctx.send("Por favor, ingresa un número válido para el volumen.")

@bot.command("Reto")
async def Reto(ctx):
    seleccionado = Desafios[random.randint(1, 7)]
    await ctx.send(f"Tu desafío de hoy es: {seleccionado}")

@bot.command("contaminacion")
async def contaminacion(ctx):
    image_url = get_pollution_image()
    await ctx.send(image_url)

@bot.command()
async def comandos(ctx):
    lista = (
        "**Lista de comandos:**\n"
        "`//hello` - Saludo inicial\n"
        "`//saludo` - Bienvenida\n"
        "`//contraseña <longitud>` - Genera una contraseña\n"
        "`//suma <n1> <n2>` | `//resta <n1> <n2>` | `//division <n1> <n2>`\n"
        "`//roll <NdN>` - Tirar dados\n"
        "`//duck` - Imagen de pato\n"
        "`//CalculateBlock <volumen>` - Calcula bloques por m³\n"
        "`//Reto` - Desafío ecológico diario\n"
        "`//contaminacion` - Imagen sobre contaminación"
    )
    await ctx.send(lista)

# 4. Iniciar bot
bot.run("TU_TOKEN_AQUI")
