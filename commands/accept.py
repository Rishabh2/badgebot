from header import *
async def accept(message, args):
  if haspermission(message.author):
    user = getmention(message)
    badge = args.split(maxsplit=1)[1]
    cursor.execute(open_challenge_badge_select_str, (user.id, badge))
    result = cursor.fetchone()
    if result == None:
      await client.send_message(message.channel, 'User does not have a matching challenge')
      return
    cursor.execute(challenge_accept_str, (int(message.timestamp.timestamp()), user.id, badge))
    connection.commit()
    await client.send_message(message.channel, 'Accepted challenge of ' + discorduser_to_discordname(getmention(message)))
  else:
    await client.send_message(message.channel, no_permissions_message)
