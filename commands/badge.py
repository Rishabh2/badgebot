from header import *
async def badge(message, args):
  if haspermission(message.author):
    user = getmention(message)
    badge = args.split(maxsplit=1)[1].lower()
    cursor.execute(open_challenge_badge_select_str, (user.id, badge))
    result = cursor.fetchone()
    if result == None:
      msg = 'User does not have a matching challenge'
    else:
      cursor.execute(challenge_win_str, (int(message.timestamp.timestamp()), user.id, badge))
      connection.commit()
      msg = 'Assigned ' + badge + ' badge to ' + discorduser_to_discordname(user)
  else:
    msg = no_permissions_message
  await client.send_message(message.channel, msg)
