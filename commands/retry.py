from header import *
async def retry(message, args):
  if haspermission(message.author):
    user = getmention(message)
    name = args
    if user != None:
      name = discorduser_to_redditname(user)
    if name == None:
      msg = no_reddit_message.format(discorduser_to_discordname(user))
    elif approve_rematch(name):
      msg = 'Retry approved for ' + name
    else:
      msg = name + ' does not have a pending retry'
  else:
    msg = no_permissions_message
  await client.send_message(message.channel, msg)
