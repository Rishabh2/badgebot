from header import *
async def getbadge(message, args):
  if args[:2] == 'my':
    await client.send_message(message.channel, 'User is me')
  user = getmention(message)
  if user == None:
    user = message.author
  cursor.execute('SELECT badge FROM betabadges WHERE id=?', (user.id,))
  result = cursor.fetchall()
  if len(result) == 0:
    msg = discorduser_to_discordname(user) + ' has no badges'
  else:
    msg = ' '.join([badge_ids[r[0]] for r in result])
  await client.send_message(message.channel, msg)
# async def getbadge(message, args):
#   user = getmention(message)
#   if user == None:
#     if len(args) == 0:
#       user = message.author
#       name = discorduser_to_redditname(message.author)
#     else:
#       name = args
#   else:
#     name = discorduser_to_redditname(user)
#   if name == None:
#     msg = no_reddit_message.format(discorduser_to_discordname(user, client.get_server('372042060913442818')
# ))
#   else:
#     msg = get_badges(name)
#   await client.send_message(message.channel, msg)
