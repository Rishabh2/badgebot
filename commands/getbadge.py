from header import *
async def getbadge(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_info)
    return
  if args[:2] == 'my':
    await client.send_message(message.channel, 'User is me')
    return
  user = getmention(message, args, message.server)
  if user == None:
    await client.send_message(message.channel, 'There is no one on this server named ' + args)
    return
  cursor.execute(lp_select_str, (user.id,))
  result = cursor.fetchone()
  if result == None:
    msg = discorduser_to_discordname(user) + ' does not have an lp'
  else:
    msg = user_badges(user.id)
  await client.send_message(message.channel, msg)
