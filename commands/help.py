from header import *
async def help(message, args):
  user = getmention(message)
  if user == None:
    user = message.author
  await client.send_message(user, embed=help_message)
  if haspermission(user):
    await client.send_message(user, embed=help_message_mod)
