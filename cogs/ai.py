import disnake
from disnake.ext import commands
from methods.methods import ask
from groq import Groq
import logging

logger = logging.getLogger(__name__)

class Ai(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="askai", description="Спросить AI (BETA)")
    async def askai(
        self,
        inter: disnake.ApplicationCommandInteraction,
        question: str,
        ai: str = commands.Param(
            choices=["llama3-8b-8192", "llama-3.3-70b-versatile"],
            default="llama-3.3-70b-versatile",
            description="Выберите модель AI"),
        role: str = "Вы - полезный помощник.",
    ):
        await inter.response.defer()
        await inter.edit_original_message(await ask(question, ai, role))
    
    async def cog_load(self):
        logger.info("%s loaded", __name__)

def setup(bot):
    bot.add_cog(Ai(bot))
