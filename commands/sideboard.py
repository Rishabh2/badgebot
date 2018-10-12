from header import *
async def sideboard(message, args):
  msg = None
  embed = None
  userid = message.author.id
  cursor.execute('SELECT * from betalp WHERE id=?', (userid,))
  result = cursor.fetchone()
  if result == None:
    msg = 'You do not have a league pass. Register one with !setlp'
  elif args not in pokemon_list[0]:
    msg = 'That is not a Pokemon I recognize'
  else:
    for i, mon in enumerate(result):
      if mon == None:
        salt = ''.join(random.choice(ALPHABET) for i in range(16))
        cursor.execute('UPDATE betalp SET mon'+str(i)+'=?, salt=? WHERE id=?', (args, salt, userid))
        connection.commit()
        newlp = list(result[1:11])
        newlp[i-1] = args
        await client.send_message(message.channel, 'Saving...')
        roster_sprites(newlp, userid, salt)
        msg = 'Done'
        break

  await client.send_message(message.channel, content=msg, embed=embed)
