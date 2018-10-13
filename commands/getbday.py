from header import *
async def getbday(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_info)
    return
  months = 'JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'.split()
  user = getmention(message)
  if user == None:
    userid = discorduser_to_id(message.author)
  else:
    userid = discorduser_to_id(user)

  cursor.execute('SELECT bdayday, bdaymonth FROM userinfo WHERE id=?', (userid,))
  result = cursor.fetchone()
  if result == None or result[0] == None:
    msg = 'User does not have a saved Bday'
  else:
    msg = str(result[0]) + ' ' + months[result[1]]
  await client.send_message(message.channel, msg)
