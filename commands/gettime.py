from header import *
async def gettime(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_info)
    return
  user = getmention(message)
  if user == None:
    if len(args) == 0:
      name = message.author.id
    else:
      name = args.lower()
  else:
    name = discorduser_to_id(user)
  cursor.execute('SELECT offset FROM time WHERE id=?', (name,))
  result = cursor.fetchone()
  if result == None:
    msg = 'There is no offset saved for that user/place'
  else:
    offset = result[0]
    msg = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=offset))).strftime('%I:%M%p')
  await client.send_message(message.channel, msg)
