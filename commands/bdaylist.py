from header import *
async def bdaylist(message, args):
  #await client.send_message(message.channel, '<@293853774982938625> is gonna write this method')
  months = 'JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'.split()
  cursor.execute('SELECT bdaymonth, bdayday, id FROM userinfo WHERE bdaymonth IS NOT NULL ORDER BY bdaymonth, bdayday ASC')
  bdays = cursor.fetchall()
  current = datetime.date.today()
  current = (current.month-1, current.day)
  pivot = -1
  for i, bday in enumerate(bdays):
    if pivot == -1 and bday[0] >= current[0] and bday[1] >= current[1]:
      pivot = i
  if pivot > 0: # We found a pivot bday
    bdays = bdays[pivot:] + bdays[:pivot]
  bdays = bdays[:5]
  msg = 'Upcoming Birthdays:\n' + '\n'.join([str(b[1]) + ' ' + months[b[0]] + ' - ' + id_to_discordname(b[2], message.server) for b in bdays])
  await client.send_message(message.channel, msg)
