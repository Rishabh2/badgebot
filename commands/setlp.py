from header import *
async def setlp(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_lp)
    return
  c = message.channel
  if c.id != '481721487569453076':
    await client.send_message(c, 'Please only use !setlp in the <#481721487569453076> channel')
    return
  await client.send_message(c,'Time to set up your league pass!\nYou start with 6 main pokemon, and will unlock 4 sideboard slots as you continue.\nAs a reminder, legendary pokemon are not allowed in our format.\nAs well as this please ensure pokemon are spelt correctly with a capital letter, also specify the form, for example Alolan Ninetales would be: Ninetales (Alola).\nWhen entering a Mega Pokemon, please only enter the base form.\nThe full details can be found on the subreddit wiki.')
  retry = False
  while not retry:
    await client.send_message(c, 'Type "cancel" to cancel')
    await client.send_message(c, 'Now, enter the names of your first 6 pokemon, one at a time:')
    mons = []
    while len(mons) < 6:
      resp = await client.wait_for_message(timeout=60, author=message.author, channel=c)
      if resp == None or resp.content.lower() == 'cancel':
        await client.send_message(c, 'Bye')
        return
      if resp.content in pokemon_list[0]:
        mons.append(resp.content)
        await client.send_message(c, 'Added ' + resp.content)
      else:
        await client.send_message(c, resp.content + ' is not a Pokemon I know. Double check spelling and capitalization, and you may need to specfiy form')
    await client.send_message(c, 'Alright, your pokemon are: ' + ', '.join(mons))
    await client.send_message(c, 'Is this correct? (y/n)')
    resp = await client.wait_for_message(timeout=60, author=message.author, channel=c)
    if resp == None:
      await client.send_message(c, 'Bye')
      return
    retry = resp.content.lower()[0] == 'y'
  cursor.execute('SELECT * FROM betalp WHERE id=?', (message.author.id,))
  result = cursor.fetchone()
  if result != None:
    cursor.execute('DELETE FROM betalp WHERE id=?', (message.author.id,))
  salt = ''.join(random.choice(ALPHABET) for i in range(16))
  cursor.execute('INSERT INTO betalp (id, mon1, mon2, mon3, mon4, mon5, mon6, salt) VALUES (?,?,?,?,?,?,?,?)', (message.author.id, *mons, salt))
  cursor.execute('DELETE FROM betabadges WHERE id=?', (message.author.id,))
  connection.commit()
  await client.send_message(c, 'Saving...')
  roster_sprites(mons, message.author.id, salt)
  ch = list(filter(lambda x: x.id == '482742805639331841', message.server.roles))[0]
  await client.add_roles(message.author, ch)
  await client.send_message(c, 'All Done!')
