from header import *
async def badge(message, args):
  if badgepermission(message.author):
    user = getmention(message)
    badge = args.split(maxsplit=1)
    if len(badge) < 2:
      await client.send_message(message.channel, 'Usage: `!badge @Tag type`')
      return
    badge = badge[1].lower()
    cursor.execute(open_challenge_badge_select_str, (user.id, badge))
    result = cursor.fetchone()
    if result == None:
      msg = 'User does not have a matching challenge'
    else:
      cursor.execute(challenge_win_str, (int(message.timestamp.timestamp()), user.id, badge))
      connection.commit()
      msg = 'Assigned ' + badge + ' badge to ' + discorduser_to_discordname(user)
      cursor.execute(badge_count_str, (user.id,))
      badges = len(cursor.fetchall())
      if badges == 8:
        await client.send_message(user, embed=singles_embed)
  else:
    msg = no_permissions_message
  await client.send_message(message.channel, msg)
