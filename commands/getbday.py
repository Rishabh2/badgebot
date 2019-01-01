from header import *
async def getbday(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_info)
    return
  user = getmention(message, args, message.server)
  if user == None:
    await client.send_message(message.channel, 'There is no one on this server named ' + args)
    return

  userid = user.id
  cursor.execute(bday_select_str, (userid,))
  result = cursor.fetchone()
  if result == None or result[0] == None:
    msg = 'User does not have a saved Bday'
  else:
    msg = str(result[0]) + ' ' + months[result[1]]
  await client.send_message(message.channel, msg)
