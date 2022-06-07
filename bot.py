from discord import Color, DiscordException, Message
from discord.ext.commands import Bot, Context
from dotenv import load_dotenv
from os import environ
from util.embed import WattsdownEmbed as Embed

# Load environment variables
load_dotenv()

# Create Discord client
client = Bot(command_prefix='!')

# Event listeners
@client.event
async def on_ready():
    print('Logged in as {0}!'.format(client.user))
    client.load_extension('cogs')

@client.event
async def on_message(message: Message):
    # Ignore messages from self
    if message.author == client.user:
        return

    try:
        await client.process_commands(message)
    except Exception as e:
        embed = Embed(color=Color.red(), title=f'Error while processing command', description=e.message)
        await message.reply(embed=embed.get())

@client.event
async def on_command_error(ctx: Context, error: DiscordException):
    print(error)

# Run client
if __name__ == '__main__':
    client.run(environ['DISCORD_TOKEN'])
