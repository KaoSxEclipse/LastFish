from discord.ext import commands
from dotenv import load_dotenv
import os,sys, discord, logging
from Cogs import *
from discord import *




logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("bot.log"),logging.StreamHandler()]
)

logger = logging.getLogger()
bot.help_command = None
load_dotenv()
TOKEN = os.getenv("LastFish")

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    await bot.add_cog(Rulebook(bot))
    await bot.add_cog(syncCog(bot))
    await bot.add_cog(about(bot))
    await bot.add_cog(help(bot))

@bot.command()
async def terminate(ctx):
    if ctx.author.id != 301494278901989378:
        return
    else:
        await ctx.send("Terminating the bot")
        logger.info(f" {ctx.message.author} has terminated {bot.user.name}")
        await bot.close()
class about(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.hybrid_command(name="about", description="Information about the Bot")
    async def about(self, ctx):
        embed = discord.Embed(title=f"{bot.user} | About",
                              description=f"{bot.user.mention} was made to explain and guide Last Fish! players through the game",
                              color=6750182)
        KaoSxEclipse = bot.get_user(301494278901989378)
        version = "3.2.2"
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
        embed.set_thumbnail(url=bot.user.avatar)
        await ctx.send(embed=embed)



bot.run(TOKEN)