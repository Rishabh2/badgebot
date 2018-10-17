from header import *
async def swap(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_lp)
    return
  msg = None
  embed = None
  userid = message.author.id
  cursor.execute(lp_select_str, (userid,))
  result = cursor.fetchone()
  if result == None:
    msg = 'You do not have a league pass. Register one with !setlp'
    embed=help_lp
  else:
    newmons = [m.strip() for m in args.split('/', maxsplit=1)]
    if not all([p in pokemon_list[0] for p in newmons]):
      msg = 'One or more of those is not a Pokemon I recognize.'
      embed=help_lp
    elif len(newmons) == 2: #Swap position of two mons
      if newmons[0] not in result or newmons[1] not in result:
        msg = 'One or more of those is not a Pokemon on your LP'
        embed=help_lp
      else:
        i1 = result.index(newmons[0]) - 1
        i2 = result.index(newmons[1]) - 1
        newlp = list(result[1:11])
        newlp[i1], newlp[i2] = newlp[i2], newlp[i1]
        salt = ''.join(random.choice(ALPHABET) for i in range(16))
        cursor.execute('UPDATE betalp SET ' + ', '.join(['mon'+str(i)+'=?' for i in range(1,11)]) + ', salt=? WHERE id=?', (*newlp, salt, userid))
        connection.commit()
        await client.send_message(message.channel, 'Saving...')
        roster_sprites(newlp, userid, salt)
        msg='Done'
    else:
      embed = help_lp
  await client.send_message(message.channel, content=msg, embed=embed)

