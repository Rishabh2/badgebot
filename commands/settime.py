from header import *
async def settime(message, args):
  argr = args.lower()[::-1]
  args = [x[::-1] for x in argr.split(maxsplit=1)]
  if len(args) == 1:
    name = message.author.id
    offset = int(args[0])
  else:
    name = args[0]
    offset = int(args[1])
  cursor.execute('SELECT offset FROM time WHERE id=?', (name,))
  result = cursor.fetchone()
  if result == None:
    cursor.execute('INSERT INTO time (id, offset) VALUES (?,?)', (name, offset))
  else:
    cursor.execute('UPDATE time SET offset=? WHERE id=?', (offset, name))
  connection.commit()
  msg = 'Time offset saved'
  await client.send_message(message.channel, msg)
