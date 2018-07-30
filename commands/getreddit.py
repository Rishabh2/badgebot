from header import *
async def getreddit(message, args):
  user = getmention(message)
  if user == None:
    if len(args) > 0:
      cursor.execute(reddit_select_name_str, (args.lower(),))
      result = cursor.fetchone()
      if result == None or result[0] == None:
        msg = 'There is no one on this server with the reddit username ' + args
      else:
        msg = id_to_discordname( result[0], message.server )
      await client.send_message(message.channel, msg)
      return
    user = message.author.id
  else:
    user = user.id
  cursor.execute(reddit_select_str, (user,))
  result = cursor.fetchone()
  if result == None or result[0] == None:
    msg = no_reddit_message.format(id_to_discordname(user, message.server))
  else:
    msg = result[0]
  await client.send_message(message.channel, msg)

