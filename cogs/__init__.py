from .default import DefaultCog
from discord.ext.commands import Bot


def setup(bot: Bot):
    bot.add_cog(DefaultCog(bot))
