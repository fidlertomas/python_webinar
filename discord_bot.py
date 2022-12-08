import discord
import discord_responses

# https://discord.com/oauth2/authorize?client_id=CLIENT_ID&scope=bot


def run_discord_bot():
    TOKEN = "tady byl token, ale neukladejte jej přímo do skriptu"
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username = str(message.author)
        zprava = str(message.content)
        channel = str(message.channel)

        print(f'{username} napsal "{zprava}"')
        if zprava[0] == "?":
            zprava = zprava[1:]
            await discord_responses.send_message(message, zprava, is_private=True)
        else:
            if zprava.split()[0] != "bote":
                return
            zprava = zprava.replace("bote", "")
            await discord_responses.send_message(message, zprava, is_private=False)

    client.run(TOKEN)


if __name__ == "__main__":
    run_discord_bot()
