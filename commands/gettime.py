from header import *
async def gettime(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_info)
    return
  user = getmention(message, args, message.server)
  if user == None:
    await client.send_message(message.channel, 'There is no one on this server named ' + args)
    return
  cursor.execute(time_select_str, (user.id,))
  result = cursor.fetchone()
  if result == None:
    msg = 'There is no offset saved for that user'
  else:
    offset = result[0]
    msg = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=offset))).strftime('%I:%M%p')
  await client.send_message(message.channel, msg)
