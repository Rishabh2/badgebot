from header import *
async def help(message, args):
  user = getmention(message)
  if user == None:
    user = message.author
  for hp in help_embeds:
    await client.send_message(user, embed=hp.set_thumbnail(url='https://images-ext-2.discordapp.net/external/8Z0dL7YbZmXqgEYPI06J7m4Ht1jpRb9PxwvlAIy66mU/%3Fsize%3D128/https/cdn.discordapp.com/avatars/368207908258709508/65eec358e20f26f99b3ecfcfd5d1cb5d.png'))
    await asyncio.sleep(0.1)
