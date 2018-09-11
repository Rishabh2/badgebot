from header import *
async def getbday(message, args):
  months = 'JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'.split()
  days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
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
