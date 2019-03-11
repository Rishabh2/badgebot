from header import *
async def loss(message, args):
  if haspermission(message.author):
    user = getmention(message)
    badge = args.split(maxsplit=1)
    if len(badge) == 1:
      await client.send_message(message.channel, 'Usage: `!loss @Tag type`')
      return
    badge = badge[1].lower()
    cursor.execute(open_challenge_badge_select_str, (user.id, badge))
    result = cursor.fetchone()
    if result == None:
      await client.send_message(message.channel, 'User does not have a matching challenge')
      return
    if badge != 'e4champ':
      cursor.execute(challenge_loss_str, (int(message.timestamp.timestamp()), user.id, badge))
      await client.send_message(message.channel, 'Assigned loss to ' + discorduser_to_discordname(getmention(message)))
    else:
      losses = result[-1] + 1
      if losses == 3:
        cursor.execute(challenge_loss_str, (int(message.timestamp.timestamp()), user.id, badge))
      else:
        cursor.execute(e4_loss_str, (user.id,))
      await client.send_message(message.channel, 'Assigned ' + ['1st','2nd','3rd'][losses-1] + ' loss to ' + discorduser_to_discordname(getmention(message)))
    connection.commit()
  else:
    await client.send_message(message.channel, no_permissions_message)
