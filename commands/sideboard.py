from header import *
async def sideboard(message, args):
  if len(args) > 0:
    userid = message.author.id
    cursor.execute('SELECT * from betalp WHERE id=?', (userid,))
    result = cursor.fetchone()
    if result == None:
      msg = 'You do not have a league pass. Register one with !setlp'
    else:
      newmons = args.split('/', maxsplit=1)
      if not all([p in pokemon_list[0] for p in newmons]):
        msg = 'One or more of those is not a Pokemon I recognize.'
      elif len(newmons) == 1: #Add a pokemon to sideboard
        for i, mon in enumerate(result):
          if mon == None:
            salt = ''.join(random.choice(ALPHABET) for i in range(16))
            cursor.execute('UPDATE betalp SET mon'+str(i)+'=?, salt=? WHERE id=?', (newmons[0], salt, userid))
            connection.commit()
            newlp = list(result[1:11])
            newlp[i-1] = newmons[0]
            await client.send_message(message.channel, 'Saving...')
            roster_sprites(newlp, userid, salt)
            msg = 'Done'
            break
      elif len(newmons) == 2: #Swap position of two mons
        if newmons[0] not in result or newmons[1] not in result:
          msg = 'One or more of those is not a Pokemon on your LP'
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
        msg = 'Usage: `!sideboard Pokemon` to add a pokemon, `!sideboard PokemonA/PokemonB` to swap two pokemon on your roster'
  else:
    msg = 'Usage: `!sideboard Pokemon` to add a pokemon, `!sideboard PokemonA/PokemonB` to swap two pokemon on your roster'
  await client.send_message(message.channel, msg)
