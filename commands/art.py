from header import *
async def art(message, args):
  mods = ['Ahri', 'Aqua', 'Boo', 'Dovah', 'H2', 'Helix', 'Lolz', 'RoPr', 'Serk', 'Tort', 'All Might', 'East', 'Raven', 'Feesh', 'Blue']
  userid = message.author.id
  if len(args) == 0:
    cursor.execute('SELECT * FROM art WHERE id=?', (userid,))
    result = cursor.fetchall()
    if result == None or len(result) == 0:
      msg = 'You do not have any submissions'
    else:
      msg = 'Your submissions:\n' + '\n'.join([r[1] + ': ' + r[2] for r in result])
  else:
    try:
      argr = args[::-1]
      art, mod = (x[::-1] for x in argr.split(maxsplit=1))
      if mod in mods:
        if art.lower() in ['remove', 'delete', 'clear', 'cancel']:
          cursor.execute('DELETE FROM art WHERE id=? AND mod=?', (userid, mod))
          connection.commit()
          await client.send_message(message.channel, 'Removed submission of ' + mod + ' art.')
          return
        cursor.execute('SELECT * FROM art WHERE id=?', (userid,))
        result = cursor.fetchall()
        if len(result) == 5 and userid != '103049236525887488':
          await client.send_message(message.channel, 'You cannot have more than 5 submissions. Please use `!art Mod Name delete` to delete a submission')
          return
        cursor.execute('SELECT * FROM art WHERE id=? AND mod=?', (userid, mod))
        result = cursor.fetchone()
        if result == None:
          cursor.execute('INSERT INTO art (id, mod, art) VALUES (?,?,?)', (userid, mod, art))
        else:
          cursor.execute('UPDATE art SET art=? WHERE id=? AND mod=?', (art, userid, mod))
        msg = 'Your art has been submitted!'
      else:
        msg = 'Usage: !art Mod Name link-to-art\nThe PVL mods are:\n' + '\n'.join(mods[:10]) + '\nThe Amino Leaders are:\n' + '\n'.join(mods[10:])
    except:
      msg = 'Usage: !art Mod Name link-to-art\nThe PVL mods are:\n' + '\n'.join(mods[:10]) + '\nThe Amino Leaders are:\n' + '\n'.join(mods[10:])
  connection.commit()
  await client.send_message(message.channel, msg)
