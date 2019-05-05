from header import *
async def setlp(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_lp)
    return

  c = message.channel
  if c.id != bot_spam_channel_id:
    await client.send_message(c, 'Please only use this command in <#{}>'.format(bot_spam_channel_id))
    return
  lp_message = '''Time to set up your league pass!
You start with 6 main pokemon, and will unlock 2 sideboard slots as you continue.
If you haven't already, use the command `!rules` to read the rules for the challenge.
As well as this please ensure pokemon are spelt correctly with a capital letter, also specify the form, for example Alolan Ninetales would be: Ninetales (Alola).
If you need any help, please contact H2owsome'''

  await client.send_message(c,lp_message)
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
      #Normalize Pokemon name
      mon = resp.content
      if mon not in pokemon_list[0]:
        await client.send_message(c, mon + ' is not a Pokemon I know. Double check spelling and capitalization, and you may need to specfiy form')
      elif mon in mons:
        await client.send_message(c, 'You cannot draft duplicate Pokemon')
      else:
        mons.append(mon)
        embed = discord.Embed(title = 'Added ' + mon, color=badgebot_color)
        embed.set_image(url=sprite_url.format(pokemon_list[1][pokemon_list[0].index(mon)]))
        await client.send_message(c, embed=embed)
        if mon in ubers:
          await client.send_message(c, 'Note: This pokemon cannot be mega evolved as per the challenge rules')
    await client.send_message(c, 'Alright, your pokemon are: ' + ', '.join(mons))
    await client.send_message(c, 'Is this correct? (y/n)')
    resp = await client.wait_for_message(timeout=60, author=message.author, channel=c)
    if resp == None:
      await client.send_message(c, 'Bye')
      return
    retry = resp.content.lower()[0] == 'y'

  cursor.execute(lp_select_str, (message.author.id,))
  result = cursor.fetchone()
  if result != None:
    cursor.execute(lp_delete_str, (message.author.id,))

  salt = ''.join(random.choice(ALPHABET) for i in range(16))
  monstext = ','.join(mons)
  cursor.execute(lp_insert_str, (message.author.id, monstext, salt))
  cursor.execute(badge_reset_str, (message.author.id,))
  connection.commit()
  await client.send_message(c, 'Saving...')
  roster_sprites(mons, message.author.id, salt)
  ch = list(filter(lambda x: x.id == '572978328215224344', message.server.roles))[0]
  await client.add_roles(message.author, ch)
  await client.send_message(c, 'All Done!')
