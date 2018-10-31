from header import *
async def sideboard(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_lp)
    return
  msg = None
  embed = None
  userid = message.author.id
  cursor.execute(lp_select_str, (userid,))
  result = cursor.fetchone()
  cursor.execute(badge_select_str, (userid,))
  badges = len(cursor.fetchall())
  if result == None:
    msg = 'You do not have a league pass. Register one with !setlp'
  elif args not in pokemon_list[0]:
    msg = 'That is not a Pokemon I recognize'
  else:
    salt = ''.join(random.choice(ALPHABET) for i in range(16))
    newlp = result[1]+','+args
    newlplist = newlp.split(',')
    if (len(newlplist) - 6)*2 > badges:
      msg = 'You do not have enough badges to add a sideboard pokemon'
    else:
      cursor.execute(lp_update_str, (newlp, salt, userid))
      connection.commit()
      await client.send_message(message.channel, 'Saving...')
      roster_sprites(newlplist, userid, salt)
      msg = 'Done'

  await client.send_message(message.channel, content=msg, embed=embed)
