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
      mons = result[1]
      m1 = newmons[0]
      m2 = newmons[1]
      if m1 not in mons or m2 not in mons:
        msg = 'One or more of those is not a Pokemon on your LP'
        embed=help_lp
      else:
        salt = ''.join(random.choice(ALPHABET) for i in range(16))
        newlp = mons.replace(m1,'PLACEHOLDER').replace(m2,m1).replace('PLACEHOLDER',m2)
        cursor.execute(lp_update_str, (newlp, salt, userid))
        connection.commit()
        await client.send_message(message.channel, 'Saving...')
        newlp = newlp.split(',')
        roster_sprites(newlp, userid, salt)
        msg='Done'
    else:
      embed = help_lp
  await client.send_message(message.channel, content=msg, embed=embed)

