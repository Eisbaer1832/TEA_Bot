
from inspect import ArgInfo
from typing import Text
import discord
from discord import message
from discord import client
from discord import permissions
from discord.channel import CategoryChannel
from discord.enums import try_enum
from discord.ext import commands
import random
from discord.utils import get
from discord.ext.commands import converter, has_permissions, MissingPermissions
import os
import re
import requests
import json
from jokeapi import Jokes
import random
import pafy
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import urllib
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!',intents = intents)


FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}


#Startbestätigung
@bot.event
async def on_ready():
    print("erfolgreich gestartet")
    bot.get_channel(847452918600040478)



#Wilkommensnachricht
@bot.event
async def on_member_join(member):
    print("erfolgreich gemerkt")
    await bot.get_channel(847452918600040478).send(f"{member.name} ist zu uns gestoßen, setz dich hin und trink einen Tee")
    


#Abschiedsnachricht
@bot.event
async def on_member_remove(member):
    print("erfolgreich gemerkt")
    await bot.get_channel(847452918600040478).send(f"{member.name} ist gegangen :-(")


#Team zuweisen
@bot.command()
async def gib(ctx, arg, arg2):
    try:        
        if arg == "Team":
                print("Rolle zugewiesen")
                guild = ctx.guild
                authour = ctx.message.author
                role = discord.utils.get(authour.guild.roles, name= arg+arg2)
                await authour.add_roles(role)
                await ctx.send ("Wurde dir zugewiesen :dizzy:")
        else:
            await ctx.send ("Hat nicht geklappt. Versuche es nocheinmal!")
    except:
            await ctx.send ("Hat nicht geklappt. Versuche es nocheinmal!")




#Team erstellen
@bot.command()
async def erstellTeam(ctx, arg):

        try:
            print("Rolle Erstellt")
            guild = ctx.guild
            authour = ctx.message.author
            role = await guild.create_role(name='Team'+ arg, permissions=discord.Permissions(0), colour=discord.Colour(0xff550), hoist=True)
            await ctx.send ("wurde erstellt :sunglasses:")
            await authour.add_roles(role)
            roleid = role.id


            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.get_role(roleid): discord.PermissionOverwrite(read_messages=True)
            }
            await ctx.guild.create_text_channel('Team'+ arg, overwrites=overwrites)

        except:
                await ctx.send ("Da hat etwas nicht geklappt. Versuche es nochmal")

#Hilfe Embed
@bot.command()
async def Hilfe(ctx):
    embed = discord.Embed(
        title="**__Command_Hilfe__**", 
        description="Du kennst nicht alle Commands? Hier sind sie! :sunglasses:",
        colour = discord.Colour.gold()
   )

    embed.add_field(name="**!erstellTeam**", value="Erstelle Teams, indem du **'!erstellTeam *dein_Teamname*'** in das Textfeld eingibst.", inline=False)
    embed.add_field(name="**!gibTeam**", value="Weise dir ein Team zu, indem du **'!gib Team *dein_Teamname*'** in das Textfeld eingibst.", inline=False)
    embed.add_field(name="**!meldan**", value=" Melde dich an, indem du **'!meldan *deinName* *deinTeamname* *deineKlasse* *deineSchule*'** in das Textfeld eingibst.", inline=False)
    embed.add_field(name="**!anmeldungen**", value="Sieh alle bisherigen Anmeldungen, indem du ** *!anmeldungen* ** in das Textfeld eingibst. :warning: **Dieses Feature kann nur im Adminchannel genutzt werden!** :warning:", inline=False)
    embed.add_field(name="**!Witz**", value= "Der Bot schreibt einen random Programmier-Witz, indem du **'!Witz'** in das Textfeld eingibst.", inline=False)
    await ctx.send(embed=embed)


#Anmelden 
@bot.command()
async def meldan(ctx, Name, Teamname, Klasse, Schule):
    f = open("Anmeldungen.txt", "a")
    print("wird angemeldet")
    with open("Anmeldungen.txt", "a"):
        f.write("Name: "+Name)
        f.write(", Teamname: "+Teamname)
        f.write(", Klasse: "+ Klasse)
        f.write(", Schule: "+Schule)
        f.write( "\n")
        
        await ctx.send ("Fertig :thumbsup:")
        await ctx.send ("Du wurdes als: "+Name+", im Team: "+Teamname+", aus der Klasse: "+Klasse+", von der Schule: "+ Schule+" angemeldet!")

    f.close()


#Anmeldungen an Admin senden
@bot.command(pass_context = True)
async def anmeldungen(ctx):
        await bot.get_channel(847452960740999198).send("Hier sind alle aktuellen Anmeldungen")
        await bot.get_channel(847452960740999198).send(file=discord.File(r'C:\Users\Tino Brinker\Desktop\Programmierwettbewerb Axoltlanten\Anmeldungen.txt'))
        

#Witz senden
@bot.command(pass_context = True)
async def Witz(ctx):
        j = Jokes()
        joke = j.get_joke(lang = "de", category=['any'],blacklist=['nsfw', 'racist'])
        if joke["type"] == "single": 
            await ctx.send (joke["joke"])
        else:
            await ctx.send (joke["setup"])
            await ctx.send (joke["delivery"])


#mUSIK MACHEN
@bot.command()
async def Musik(ctx, arg):

    search = arg
    
    if ctx.message.author.voice == None:
        await ctx.send ("Du musst in einem Sprachchat sein um den Befehl zu nutzen!")
        return
   

    author = ctx.message.author

    channel = ctx.author.voice.channel
    
    vc = await channel.connect()
    
    voice = discord.utils.get(ctx.guild.voice_channels, name=channel.name)
        
    html = urllib.request.urlopen(search)
    
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    
    embed = discord.Embed(
        title="Es wird nun ein neues Video gespielt!", 
        description= arg,
        colour = discord.Colour.green()
   )
        
    await ctx.send(embed = embed)

    song = pafy.new(video_ids[0])

    audio = song.getbestaudio()

    source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)

    vc.play(source)
        

# Musik beenden
@bot.command(pass_context = True)
async def stop(ctx):
    await ctx.guild.voice_client.disconnect()



#Ort des Tages
@bot.command(pass_context = True)
async def ort(ctx):
    for x in range (1):
        x = random.randint(2,9)
        y = random.randint(2,9)
        converted_num = str(x)
        converted_num1 = str(y)

        ort = "https://www.google.de/maps/@"+converted_num+".2634574,"+converted_num1+".7837054"
        #https://www.google.de/maps/@59.2923265,7.5175231,14z
        await ctx.send (ort)
bot.run("ODA2NTAxMzg1MzkwNjUzNDcw.YBqW8g.7YdmkHrZbYuQ1RsLELGsu_bjIEQ")





# Es wurde der Sv443s-JokeApi-Python-Wrapper verwendet. -> https://github.com/thenamesweretakenalready/Sv443s-JokeAPI-Python-Wrapper#readme-

