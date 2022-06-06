from .default import DefaultCog
from discord.ext.commands import Bot
from scraper.scraper import WattsdownScraper


def setup(bot: Bot):
    # Create scraper instance
    scraper = WattsdownScraper()

    # Add default cog
    bot.add_cog(DefaultCog(bot, scraper))
