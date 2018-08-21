from header import *
async def loss(message, args):
  if haspermission(message.author, args):
    await client.send_message(message.channel, 'Assigned loss to ' + discorduser_to_discordname(getmention(message)))
  else:
    await client.send_message(message.channel, no_permissions_message)
# async def loss(message, args):
#   if haspermission(message.author):
#     (name, badge) = args.split(maxsplit=1)
#     user = getmention(message)
#     if user != None:
#       name = discorduser_to_redditname(user)
#     badge = badge.lower()
#     if name == None:
#       msg = no_reddit_message.format(discorduser_to_discordname(user))
#     elif not wiki_exists(name):
#       msg = name + ' does not have a reigstered league pass'
#     elif not isbadge(badge):
#       msg = badge + ' is not a valid badge'
#     elif flair_post(name, badge, 'Defeat'):
#       msg = 'Assigned loss to ' + name
#     else:
#       msg = name + ' does not have a matching challenge'
#   else:
#     msg = no_permissions_message
#   await client.send_message(message.channel, msg)
