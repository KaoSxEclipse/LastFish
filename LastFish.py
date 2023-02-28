
from dotenv import load_dotenv
import os,sys
from Cogs import *
from CardCommands import CardSearch
import discord
from discord import *
import logging
from discord.ext import commands
from Modals import PlayerSelect, Suggestion

bot = commands.Bot(command_prefix='l!', intents=intents, case_insensitive=True, Activity="Playing LastFish")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(level    qname)s - %(message)s',
    handlers=[logging.FileHandler("bot.log"),logging.StreamHandler()]
)


logger = logging.getLogger()
bot.help_command = None
load_dotenv()
TOKEN = os.getenv("LastFish")
# Loads Cogs When bot gets initiated
@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    await bot.add_cog(Rulebook(bot))
    await bot.add_cog(syncCog(bot))
    await bot.add_cog(about(bot))
    await bot.add_cog(help(bot))
    await bot.add_cog(CardSearch(bot))
    await bot.add_cog(PlayerSelect(bot))
    await bot.add_cog(Suggestion(bot))

# Dev only, turns off bot in case of double instances or bugs / I can't get to my laptop
@bot.command()
async def terminate(ctx):
    if ctx.author.id != 301494278901989378:
        return
    else:
        await ctx.send("Terminating the bot")
        logger.info(f" {ctx.message.author} has te  rminated {bot.user.name}")
        await bot.close()
    # About Embed Command
class about(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.hybrid_command(name="about", description="Information about the Bot")
    async def about(self, ctx):
        embed = discord.Embed(title=f"{bot.user} | About",
                              description=f"{bot.user.mention} was made to explain and guide Last Fish! players through the game",
                              color=6750182)
        KaoSxEclipse = bot.get_user(301494278901989378)
        version = "3.5.1"
        arrow = "<:KaoArrow:1068047981309345852>"
        discordlogo = "<:discordlogo:1068760141954023505>"
        support = "<:tools:1068752038122504293>"
        pythonlogo = "<:pythonlogo:1068760140389560320>"

        information = f"{arrow} **Developer:** {KaoSxEclipse}\n" \
                      + f"{arrow} **Python:** 3.9.7\n" \
                      + f"{arrow} **Pycharm** 2022.3.2\n" \
                      + f"{arrow} **Latency:** {round(bot.latency * 1000)} ms\n" \
                      + f"{arrow} **Version:** {version}"
        links = f"{arrow} **Library:** {pythonlogo} [discord.py 2.1.0](https://github.com/Rapptz/discord.py)\n" \
                + f"{arrow} **Support:** {support} [Click me](https://twitter.com/KaoSxEclipseYT)\n" \
                + f"{arrow} **Whiskers Discord:** {discordlogo} [Click me](https://discord.gg/thegreatpond)"
        embed.add_field(name="__Information__", value=information, inline=False)
        embed.add_field(name="__Links__", value=links, inline=False)
        await ctx.send(embed=embed)


# Runs the but using the TOKEN variable from os.getenv("LastFish")
bot.run(TOKEN)
