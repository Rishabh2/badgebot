from header import *
async def loss(message, args):
  if haspermission(message.author):
    user = getmention(message)
    badge = args.split(maxsplit=1)[1]
    cursor.execute('SELECT * FROM betachallenge WHERE id=? AND badge=? AND status="O"', (user.id, badge))
    result = cursor.fetchone()
    if result == None:
      await client.send_message(message.channel, 'User does not have a matching challenge')
      return
    cursor.execute('UPDATE betachallenge SET status="L" WHERE id=? AND badge=? AND STATUS="O"', (user.id, badge))
    connection.commit()
    await client.send_message(message.channel, 'Assigned loss to ' + discorduser_to_discordname(getmention(message)))
  else:
    await client.send_message(message.channel, no_permissions_message)
# async def loss(message, args):
#   if haspermission(message.author):
#     (name, badge) = args.split(maxsplit=1)
#     user = getmention(message)
#     if user != None:
#       name = discorduser_to_redditname(user)
#     badge = badge.lower()
#     if name == None:
#       msg = no_reddit_message.format(discorduser_to_discordname(user))
#     elif not wiki_exists(name):
#       msg = name + ' does not have a reigstered league pass'
#     elif not isbadge(badge):
#       msg = badge + ' is not a valid badge'
#     elif flair_post(name, badge, 'Defeat'):
#       msg = 'Assigned loss to ' + name
#     else:
#       msg = name + ' does not have a matching challenge'
#   else:
#     msg = no_permissions_message
#   await client.send_message(message.channel, msg)
