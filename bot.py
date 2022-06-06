from discord import DiscordException, Message
from discord.ext.commands import Bot, Context
from dotenv import load_dotenv
from os import environ

# Load environment variables
load_dotenv()

# Create Discord client
client = Bot(command_prefix='!')

# Event listeners
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message: Message):
    # Ignore messages from self
    if message.author == client.user:
        return

    # Respond to messages
    if message.content.startswith('!hello'):
        await message.reply('Hello!')

@client.event
async def on_command_error(ctx: Context, error: DiscordException):
    print(error)

# Run client
if __name__ == '__main__':
    client.run(environ['DISCORD_TOKEN'])
