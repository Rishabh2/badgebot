from header import *
async def cancel(message, args):
  if haspermission(message.author):
    (name, badge) = args.split(maxsplit=1)
    user = getmention(message)
    if user != None:
      name = discorduser_to_redditname(user)
    badge = badge.lower()
    if name == None:
      msg = no_reddit_message.format(discorduser_to_discordname(user))
    elif not isbadge(badge):
      msg = badge + ' is not a valid badge'
    elif cancel_challenge(name, badge):
      msg = 'Canceled challenge for ' + name
    else:
      msg = name + ' does not have an open challenge'
  else:
    msg = no_permissions_message
  await client.send_message(message.channel, msg)
