from header import *
async def remindme(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_misc)
    return
  c = message.channel
  if c.id != '481721487569453076':
    await client.send_message(c, 'Please only use this command in <#481721487569453076>')
    return
  await client.send_message(c, 'Type `cancel` to cancel')
  await client.send_message(c, 'What channel do you want to me be reminded in? If you do not respond with a valid channel, you will be reminded in this channel')
  resp = await client.wait_for_message(timeout=60, author=message.author, channel=c)
  if resp == None or resp.content.lower() == 'cancel':
    await client.send_message(c, 'Bye')
    return
  target = resp.channel_mentions
  target = target[0].id if len(target) > 0 else c.id
  await client.send_message(c, 'Got it. What am I reminding you of?')
  resp = await client.wait_for_message(timeout=60, author=message.author, channel=c)
  if resp == None or resp.content.lower() == 'None':
    await client.send_message(c, 'Bye')
    return
  msg = resp.content
  await client.send_message(c, 'Got it. Finally, how long until the reminder? Enter an amount of time\nExamples: 20s, 10m, 2h, 7d')
  resp = await client.wait_for_message(timeout=60, author=message.author, channel=c)
  if resp == None or resp.content.lower() == None:
    await client.send_message(c, 'Bye')
    return
  time = time_parse_sec(resp.content.lower())
  if time == None:
    await client.send_message(c, 'I could not parse a valid time. Please start over')
    return
  else:
    await client.send_message(c, 'Reminder set')
    now = datetime.datetime.utcnow()
    diff = datetime.timedelta(seconds=time)
    finish = int((now + diff).timestamp())
    salt = ''.join(random.choice(ALPHABET) for i in range(16))
    cursor.execute('INSERT INTO reminders (id, message, end, target, salt) VALUES (?,?,?,?,?)', (message.author.id, msg, finish, target, salt))
    connection.commit()
    await asyncio.sleep(time)
    await client.send_message(discord.Object(id=target), '<@{}>: '.format(message.author.id) + msg)
    cursor.execute('DELETE FROM reminders WHERE salt=?', (salt,))
    connection.commit()

