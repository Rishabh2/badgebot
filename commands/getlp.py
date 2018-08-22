from header import *
async def getlp(message, args):
  user = getmention(message)
  if user == None:
    user = message.author
  cursor.execute('SELECT * FROM betalp WHERE id=?', (user.id,))
  result = cursor.fetchone()
  if result == None:
    msg = no_lp_message.format(discorduser_to_discordname(user))
  else:
    msg = '\n'.join([x for x in result[1:] if x!=None])
  await client.send_message(message.channel, msg)
# async def getlp(message, args):
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
#     msg = no_reddit_message.format(discorduser_to_discordname(user))
#   else:
#     msg = get_league_pass(name)
#     if not isinstance(msg, str):
#       msg=msg.url
#   await client.send_message(message.channel, msg)
