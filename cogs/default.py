from discord.ext.commands import Bot, Cog, command, Context
from util.embed import WattsdownEmbed as Embed


class DefaultCog(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        print('Loaded default cog')
    
    @command(name='hi')
    async def hello(self, ctx: Context):
        hello_embed = Embed(title='Hi', description='Hello!')
        await hello_embed.send(ctx, as_reply=True)
