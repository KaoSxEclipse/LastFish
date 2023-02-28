import discord, logging
from discord.ext import *
from discord import *
from discord.ext import commands
from discord.ext.commands import *
from typing import Optional, Literal
import json





# bot intents / privileges
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix='l!', intents=intents, case_insensitive=True, Activity="Playing LastFish")


# Set up Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("bot.log"),logging.StreamHandler()]
)
logger = logging.getLogger()
class help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.hybrid_command(name="help", description="Need some help?", aliases=["LH"])
    async def Help(self,ctx):
        embed = discord.Embed(title=f"**__Need a Hand?__**", description="Please use /Rulebook!", color=0xff91a4)
        embed.add_field(name="Find a bug or error?", value=f"dm [KaoSxEclipseYT](https://twitter.com/KaoSxEclipseYT) on Twitter, or KaoSxEclipse#0111 on Discord.")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="credits", description="Card Art Credits")
    async def Credits(self,ctx):
        embed = discord.Embed(title="**Credits and Notable Mentions**", description="")
        embed.add_field(name="Artists", value="[Cliff Elivert](https://twitter.com/cliffBallin), [Zwistillus](https://twitter.com/Zwistillus), [Winnie Liu](https://twitter.com/winniestudio), [CheeryBee](https://twitter.com/HanhTran1112)")
        embed.add_field(name="Game Testers", value="[Mackinac](https://twitter.com/_mackinac) and __Rey Romo__!", inline=False)
        await ctx.send(embed=embed, ephemeral=True)






rulebook_pages = {
            "Keywords & Card Types": {
                "title": "Keywords and Card Types!",
                "description": "There are **12** Total Keywords and **7** Card Types\n   ",
                "information": "Each card uses different keywords, follow the instructions on the sheet below for the keyword specified. \n __Card types__ are also listed below."
                               "\n <:5:1069133378890244106> **Instants** can be used anytime the effect is applicable *and* the  Encounter Card Resolves.\n"
                               "<:1:1069133377099280414> **Spells** can be played both *Before* and/or *After* Item/Attack cards, you may play as many Spell cards as you want on your turn. \n"
                               "<:2:1069133382170198068> **Curses** are similar to spells but only *1* may be played. They have two abilities and to use the 'Secondary' ability you must sacrifice HP. Players may not use *Attack* or *Curse* cards on their first turn\n"
                               "<:3:1069133380635070494> **Encounter** card are random events that a **CHAMPION** might face. They are able to affect a myriad of players at once and effects may vary."
                               ,
                "image": "https://i.imgur.com/rFiUSD0.png"
            },
            "Turn Actions": {
                "title": "Turn Actions",
                "description": "What to do and when.",
                "information": "What can I do on my turn and when do I do it?\n"
                               "**__Turn Actions__**\n"
                               "**1.** **DRAW** a card from the *Draw* deck and add it to your hand.\n"
                               "**2.** **DISCOVER** a card from the *Encounter* deck and follow it's effect then discard it to the Encounter Discard Pile.\n"
                               "**3.** Perform *Any* or *All* of the following actions.\n"
                               "    i. Use as many *Spells* as you want\n"
                               "    ii. Use as many *Instants* as you want\n"
                               "    iii. Play One *Curse* Card\n"
                               "    iiii. **EQUIP** an *Item* to your Champion OR *Attack* an opposing player.\n"
                               "OR **DRAW** until you have 5 cards. If you already have 5 or more, draw 1.\n"
                               "    *Play Continues Clockwise.*",

                "image": "https://i.imgur.com/ibbehYA.png"
            },
            "SetUp": {
                "title": "Setup and Cards",
                "description": "What do I do with all these cards?",
                "information": "**__Player Cards__**\n"
                               "From Left to Right -> Champion Card, HP Cards stacked together, Equiptment/Item Cards.\n"
                               "\n **__Table Cards__**\n"
                               "Draw and Encounter Decks in the middle, respective discard piles on the *outside* of each deck.\n"
                               ,




                "image": "https://i.imgur.com/M2QBvG5.png"
            } ,
            "Card Notation": {
                "title": "Card Notation",
                "description": "**__What do these things mean?__**",
                "information": "**Card Type** refers to whether it's an: *Instant, Item, Spell, Curse, Encounter, Champion,* or *Attack* (Affetcs Border Color)\n"
                               "**Ability Text** explains card effects and when to perform them.\n"
                               "**Flavor Text** Short blurb of lore\n"
                               "**Artist's Stamp** refers to the artist who made the card art -> See /Credits.",
                "image": "https://i.imgur.com/wyM4gEW.png"

            } ,
            "Misc": {
                "title": "Misc.",
                "description": "**__Additional Rulings__**",
                "information": "**1.** All forms of damage can be blocked by *Item* cards, **except** for *direct* damage or damage that bypasses items and attacks HP directly.\n"
                               "--> All *Items* block **1** damage point.\n"
                               "**2.** The *Spell* 'Duplication' plays an additional copy of the card it's paired with when played.\n"
                               "--> Even if one copy is **NEGATED** the other copy will still exist and peform the effect.\n"
                               "**3.** Any card that says *you may...* means the effect is optional if you choose to use it.\n"
                               "**4. **Whenever a card has you draw from the *discard pile* you **must** reveal the chosen card to the other players\n"
                               "**5.** When a player must **GIFT** another player a card, they are not required to reveal it.\n"
                               "**6.** __Chaining__\n"
                               "A chain determines the order in which to resolve card conflicts. A general rule is cards in a chain resolve one by one starting with the last one played.\n"
                               "--> EX: An *Instant* played after an *Attack* card nullifes the *Attack* card.\n"
                               "**7.** Players may look through either discard pile at any time."
    ,
                "image": None
            },
            "Remaining Card Types": {
                "title": "**__Remaining Card Types__**",
                "description": "",

                "information": "<:5:1069133378890244106> *Instants* are spells, skills, or items that can be used at *almost* any moment, whether it is your turn or not as long as the effect is applicable.\n"
                               "--> **Instants** can not be used until **after** each turn's *Encounter* card has resolved.\n"
                               "<:4:1069133383545925663> **Champion** cards are used to represent your character in the game.\n"
                               "--> Each Champion has a *Signature* card(s) in the *Draw* deck, if you draw your Champions signature card you may apply the bonus effect listed on your champions **Ability Text** when you play the signature card.\n"
                               "<:7:1069134744392060928> **Attack** cards are the primary way to deal damage. Only one *Attack* card may be used on your turn so long as you have not played an *Item* card\n"
                               "--> Some cards may allow for multple *Attack* cards to be played, or even an *Item* card and an *Attack* card on the same turn.",
                "image": "https://i.imgur.com/j4ZGYuy.png",
},
            "Card-Based Combat": {
                "title": "Attack",
                "description": "**__How do I attack?__**",
                "information": "__Example__:\n"
                               "Kaos uses **Frozen Spear** a *1* damage **ATTACK** card on Rico. Rico may now, use an *Instant* card, and/or **DESTORY** one of Kaos' items (unless a card states otherwise or specifies which item) per point of damage taken.\n"
                               "If Rico has no more *Instants* or more *Items* to protect himself with. He takes the non-negated damage points to his **HP** and flips that many *Heart* cards face down.\n"
                               "--> Once all of a players *Heart* cards are face down they have been eliminated. Send all of the cards in their hand to the *Discard* pile.",
                "image": "https://i.imgur.com/FucD2kb.png"

            }
        }
# Emojis
with open("CustomEmoji", "r") as f:
    emojis = json.load(f)
    for key, value in emojis.items():
        exec(f"{key} = '{value}'")
class Rulebook(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="rulebook", description="Load an Interactive LastFish! Rulebook and Guide!")
    async def rulebook(self, interaction: discord.Interaction):
        """An interactive rulebook and guide!"""

        class Dropdown(discord.ui.Select):
            def __init__(self):



                options = [
                  discord.SelectOption(label="Keywords & Card Types",description="Need help with the keyterms and card types?",  ),
                  discord.SelectOption(label="Remaining Card Types", description="Champions, HP cards, Items, etc."),
                  discord.SelectOption(label="SetUp", description="What do I do with all these cards?"),
                  discord.SelectOption(label="Turn Actions", description="What to do and When."),
                  discord.SelectOption(label="Misc", description="Additional Rulings and Information."),
                  discord.SelectOption(label="Card-Based Combat", description="Attacking How-To's"),
                  discord.SelectOption(label="Card Notation", description="Understanding what's on the card.")]

                super().__init__(placeholder='Please Select a Page', min_values=1, max_values=1,options=options)

            async def callback(self, interaction: discord.Interaction):
                selected_option = self.values[0]
                information = rulebook_pages[selected_option]['information']
                for option in self.options:
                    if option.label == selected_option:
                        embed = discord.Embed(title=option.label, description=option.description, color=6750182)
                        embed.add_field(name="", value=information)
                        embed.set_image(url=rulebook_pages.get(option.label, {}).get('image', None))
                await interaction.response.send_message(embed=embed, ephemeral=True)


        class DropdownView(discord.ui.View):
            def __init__(self):
                super().__init__()

                # Adds the dropdown to our view object.
                self.add_item(Dropdown(),)

        logger.info("Command Invoked")
        pages = list(rulebook_pages.keys())
        current_page = 0
        welcome_embed = discord.Embed(title="Welcome to the Rulebook", description=(f"{players}2-6 Players \n {clock}Gametime: 10-60 minutes"),
                                      color=discord.Color.teal())
        welcome_embed.add_field(name=f"__**Getting Started**__\n",
                                value=f"First, separate all the cards by their differing backs and hand each player a *Rule  Reference* card\n"
                                      f"Next, shuffle the 'Draw' and 'Encounter' Decks Separately, use the areas next to each deck respectively as discard piles.", inline=False)
        welcome_embed.add_field(name="**__Who Goes First?__**",
                                value=(f"Play Rock, Paper, Scissors or your own fun game to decide who goes first! The winner picks their Champion first. Play continues to the left."))
        welcome_embed.set_footer(text="Box Contains: 1 Draw Deck, 1 Encounter Deck, 8 Champion Cards, 18 Heart Cards, and 6 Rule Reference Cards")

        view = DropdownView()
        await interaction.response.send_message(embed=welcome_embed, view=view, ephemeral=True)




class syncCog(commands.Cog):
    @commands.command(description='Syncs all commands globally. Only accessible to developers.')
    async def sync(self, ctx: Context, guilds: Greedy[discord.Object],
                   spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        if ctx.author.id != 301494278901989378:
            return

        embed = discord.Embed(description="Syncing...", color=discord.Color.red())
        await ctx.send(embed=embed)
        print("Syncing...")
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(embed=discord.Embed(
                description=f"Synced `{len(synced)}` commands {'globally' if spec is None else 'to the current guild.'}.",
                color=discord.Color.green()))
            print("Synced.")
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(embed=discord.Embed(description=f"Synced the tree to {ret}/{len(guilds)}.", color=self.color))
        print("Synced.")


