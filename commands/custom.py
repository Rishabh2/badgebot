from header import *
async def custom(message, args):
  if haspermission(message.author):
    user = getmention(message)
    if user == None:
      user = message.author
    await client.send_message(user, embed=singles_embed)
