from header import *
async def setbday(message, args):
  months = 'JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'.split()
  days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  args = args.split()
  if len(args) != 2:
    msg = 'Usage: `!setbday 01 JAN`'
  elif args[1][:3] not in months:
    msg = 'That is not a valid month'
  elif int(args[0]) < 1 or int(args[0]) > days[months.index(args[1][:3])]:
    msg = 'That is not a valid day'
  else:
    user = message.author.id
    month = months.index(args[1][:3])
    day = int(args[0])
    cursor.execute('SELECT bdayday FROM userinfo WHERE id=?', (user,))
    result = cursor.fetchone()
    if result == None:
      cursor.execute('INSERT INTO userinfo (id, bdaymonth, bdayday) VALUES (?,?,?)', (user, month, day))
    else:
      cursor.execute('UPDATE userinfo SET bdaymonth=?, bdayday=? WHERE id=?', (month, day, user))
    connection.commit()
    msg = 'Bday set'
  await client.send_message(message.channel, msg)
