from discord import Color
from discord.ext.commands import Bot, Cog, command, Context
from scraper.scraper import WattsdownScraper
from util.embed import WattsdownEmbed as Embed


class DefaultCog(Cog):
    def __init__(self, bot: Bot, scraper: WattsdownScraper):
        self.bot = bot
        self.scraper = scraper
        print('Loaded default cog')
    
    @command(name='hi')
    async def hello(self, ctx: Context):
        hello_embed = Embed(title='Hi', description='Hello!')
        await hello_embed.send(ctx, as_reply=True)
    
    @command(name='list')
    async def list_outages(self, ctx: Context):
        async with ctx.typing():
            # Check if the scraper's scraped anything yet
            if self.scraper.meralco_outages.size == 0:
                # Scrape first and perform OCR
                self.scraper.scrape_meralco_outages()
                self.scraper.ocr_meralco_outages()
            
            # Iterate through each row in the outages dataframe
            for _, outage in self.scraper.meralco_outages.iterrows():
                # Create embed
                outage_embed = Embed(
                    title='Outage on {}'.format(outage['Outage Date']),
                    fields=[
                        ('Outage time', outage['Outage Time']),
                        ('Affected areas', outage['Affected Areas']),
                        ('Announcement link', 'https://twitter.com/meralco/status/{0}'.format(outage['Tweet ID']))
                    ],
                    color=Color.from_rgb(235, 120, 54)
                )
                await outage_embed.send(ctx, as_reply=False)
