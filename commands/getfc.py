from header import *
async def getfc(message, args):
  user = getmention(message)
  if user == None:
    if len(args) == 0:
      userid = discorduser_to_id(message.author)
    else:
      cursor.execute(reddit_select_name_str, (args.lower(),))
      result = cursor.fetchone()
      if result == None or result[0] == None:
        await client.send_message(message.channel, 'There is no one on this server with the reddit username ' + args)
        return
      else:
        userid = result[0]
  else:
    userid = discorduser_to_id(user)
  cursor.execute(fc_select_str, (userid,))
  result = cursor.fetchone()
  if result == None or result[0] == None:
    await client.send_message(message.channel, id_to_discordname(userid,message.server ) + " does not have a registered friend code.")
  elif result[1] == None:
    await client.send_message(message.channel, result[0])
  else:
    await client.send_message(message.channel, embed=make_embed(result[0], result[1], user))

