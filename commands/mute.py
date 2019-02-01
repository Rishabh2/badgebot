from header import *
async def mute(message, args):
  if mutepermission(message.author):
    target, time, reason = args.split(maxsplit=2)
    target = id_to_discorduser(target, message.server)
    if target == None:
      target = getmention(message)
    if target.id == '242558859300831232':
      await client.send_message(message.channel, no_permissions_message)
    else:
      time = time_parse_sec(time)
      if time == None:
        return
      roles = message.server.roles
      for role in roles:
        if role.name=='Muted':
          mute_role=role
      await client.add_roles(target, mute_role)
      await client.send_message(message.channel, target.mention + ' was muted')

      now = datetime.datetime.utcnow()
      diff = datetime.timedelta(seconds=time)
      finish = int((now + diff).timestamp())
      salt = ''.join(random.choice(ALPHABET) for i in range(16))
      cursor.execute('INSERT INTO mutes (id, reason, end, target, salt) VALUES (?,?,?,?,?)', (message.author.id, reason, finish, target.id, salt))
      connection.commit()
      await asyncio.sleep(time)
      cursor.execute('DELETE FROM mutes WHERE salt=?', (salt,))
      connection.commit()
      await client.remove_roles(target, mute_role)

  else:
    await client.send_message(message.channel, no_permissions_message)
