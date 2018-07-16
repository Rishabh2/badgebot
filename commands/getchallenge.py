from header import *
async def getchallenge(message, args):
  (name, badge) = args.split(maxsplit=1)
  user = getmention(message)
  if user != None:
    name = discorduser_to_redditname(user)
  badge = badge.lower()
  if name == None:
    msg = no_reddit_message.format(discorduser_to_discordname(user, client.get_server('372042060913442818')
))
  elif not wiki_exists(name):
    msg = name + ' does not have a reigstered league pass'
  elif not isbadge(badge):
    msg = badge + ' is not a valid badge'
  else:
    challenges = challenges_list(name, badge)
    if len(challenges) == 0:
      msg = name + ' does not have a matching challenge'
    else:
      msg = challenges[0].url
  await client.send_message(message.channel, msg)
