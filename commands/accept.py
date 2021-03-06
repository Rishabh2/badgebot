from header import *
async def accept(message, args):
  if badgepermission(message.author):
    user = getmention(message)
    badge = args.split(maxsplit=1)
    if len(badge) < 2:
      await client.send_message(message.channel, 'Usage: `!accept @Tag type`')
      return
    badge = badge[1].lower()
    cursor.execute(open_challenge_badge_select_str, (user.id, badge))
    result = cursor.fetchone()
    if result == None:
      await client.send_message(message.channel, 'User does not have a matching challenge')
      await client.send_message(message.channel, 'Are you overriding the timer? (y/n)')
      resp = await client.wait_for_message(timeout=60, author=message.author, channel=message.channel)
      if resp != None and resp.content.lower()[0] == 'y':
        cursor.execute(challenge_override_str, (user.id, badge, int(message.timestamp.timestamp()), int(message.timestamp.timestamp())))
        connection.commit()
        msg = 'Accepted challenge of ' + discorduser_to_discordname(user)
      else:
        msg = 'Bye'
    else:
      cursor.execute(challenge_accept_str, (int(message.timestamp.timestamp()), user.id, badge))
      connection.commit()
      msg = 'Accepted challenge of ' + discorduser_to_discordname(user)
    await client.send_message(message.channel, msg)
  else:
    await client.send_message(message.channel, no_permissions_message)
