from asyncio import TimeoutError
from discord import Embed, Member, Message, NotFound, Reaction
from discord.ext.commands import Context
from typing import Callable, List


class Paginator:
    """
    Adapted from @jareddantis/rico-bot
    """
    def __init__(self, ctx: Context):
        self.bot = ctx.bot
        self.ctx = ctx
        self.embeds = []
        self.current = 0
        self.timeout = 60
    
    async def run(self, embeds: List[Embed], start: int = 0, timeout: int = 0, callback: Callable[[int], None] = None):
        # Based on https://github.com/toxicrecker/DiscordUtils/blob/master/DiscordUtils/Pagination.py
        # but with support for custom home page
        control_emojis = ('⏮️', '⏪', '🏠', '⏩', '⏭️')
        timeout = timeout if timeout > 0 else 60
        self.timeout = timeout
        self.embeds = embeds

        # Add footer and timestamp to every embed
        for i in range(len(embeds)):
            embeds[i].timestamp = self.ctx.message.created_at
            embeds[i].set_footer(text=f'Page {i + 1} of {len(embeds)}')

        # Send initial embed and call callback with message ID
        self.current = start
        msg = await self.ctx.send(embed=embeds[start])
        msg: Message = await msg.channel.fetch_message(msg.id)
        if callback is not None:
            callback(msg.id)
        
        # Add reactions
        for emoji in control_emojis:
            try:
                await msg.add_reaction(emoji)
            except Exception as e:
                print(f'Error adding emoji to {msg.id}: {e}')
        
        # Handle reactions
        def check(r: Reaction, u: Member):
            return u == self.ctx.author and str(r.emoji) in control_emojis
        while True:
            # Wait for reaction add until timeout runs out
            try:
                # Remove user reaction
                try:
                    r, u = await self.bot.wait_for('reaction_add', check=check, timeout=self.timeout)
                    await msg.remove_reaction(r.emoji, u)
                except NotFound:
                    # Message has likely been deleted
                    return

                if str(r.emoji) == control_emojis[0]:     # Start
                    self.current = 0
                elif str(r.emoji) == control_emojis[1]:   # Back
                    self.current = 0 if self.current <= 0 else self.current - 1
                elif str(r.emoji) == control_emojis[2]:   # Home
                    self.current = start
                elif str(r.emoji) == control_emojis[3]:   # Next
                    self.current = len(embeds) - 1 if self.current >= len(embeds) - 1 else self.current + 1
                elif str(r.emoji) == control_emojis[4]:   # End
                    self.current = len(embeds) - 1

                await msg.edit(embed=self.embeds[self.current])
            except TimeoutError:
                # Remove all reactions
                self.current = start
                try:
                    await msg.clear_reactions()
                except:
                    pass
                return
