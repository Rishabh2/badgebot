from header import *
async def getfc(message, args):
  user = getmention(message)
  if user == None:
    user = message.author
  userid = discorduser_to_id(user)
  cursor.execute(fc_select_str, (userid,))
  result = cursor.fetchone()
  if result == None:
    await client.send_message(message.channel, id_to_discordname(userid) + " does not have a registered friend code.")
  elif result[1] == None:
    await client.send_message(message.channel, result[0])
  else:
    await client.send_message(message.channel, embed=make_embed(result[0], result[1], user))

