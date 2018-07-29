from header import *
async def help(message, args):
  user = getmention(message)
  if user == None:
    user = message.author
  if haspermission(user):
    await client.send_message(user, embed=help_message)
    await client.send_message(user, embed=help_message_mod)
  else:
    await client.send_message(user, embed=help_message)
