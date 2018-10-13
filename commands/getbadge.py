from header import *
async def getbadge(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_info)
    return
  if args[:2] == 'my':
    await client.send_message(message.channel, 'User is me')
    return
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
