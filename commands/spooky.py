from header import *
async def spooky(message, args):
  userid=message.author.id
  if args == 'help':
    msg = 'Usage:\n`!spooky` - See your submitted art\n`!spooky link-to-art` or `!spooky embed-the-art-directly` - Submit art for the content\n`!spooky delete #` - Delete a submission, replace # with the number of the submission you want to delete'
  elif len(args) == 0 and len(message.attachments)==0:
    cursor.execute('SELECT number, link FROM spooky WHERE id=? ORDER BY number ASC', (userid,))
    result=cursor.fetchall()
    msg = 'Your submissions:\n' + '\n'.join([str(r[0])+': '+r[1] for r in result])
  else:
    args = args.split(maxsplit=1)
    if len(args) == 2 and args[0] == 'delete':
      todel = int(args[1])
      cursor.execute('DELETE FROM spooky WHERE id=? AND number=?', (userid, todel))
      connection.commit()
      msg = 'Done'
    else:
      if len(args) == 1:
        link = args[0]
      if len(message.attachments) > 0:
        link = message.attachments[0]['url']
      cursor.execute('SELECT number, link FROM spooky WHERE id=? ORDER BY number ASC', (userid,))
      result=cursor.fetchall()
      maxnum = result[-1][0] if len(result)>0 else 0
      cursor.execute('INSERT INTO spooky (id, number, link) VALUES (?,?,?)', (userid, maxnum+1, link))
      connection.commit()
      msg = 'Done'
  await client.send_message(message.channel, msg)
