from header import *
async def getbadge(message, args):
  user = getmention(message)
  if user == None:
    if len(args) == 0:
      user = message.author
      name = discorduser_to_redditname(message.author)
    else:
      name = args
  else:
    name = discorduser_to_redditname(user)
  if name == None:
    msg = no_reddit_message.format(discorduser_to_discordname(user))
  else:
    msg = get_badges(name)
  await client.send_message(message.channel, msg)
