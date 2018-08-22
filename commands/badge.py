from header import *
async def badge(message, args):
  if haspermission(message.author):
    user = getmention(message)
    badge = args.split(maxsplit=1)[1]
    cursor.execute('SELECT * FROM betachallenge WHERE id=? AND badge=? AND status="O"', (user.id, badge))
    result = cursor.fetchone()
    if result == None:
      await client.send_message(message.channel, 'User does not have a matching challenge')
      return
    cursor.execute('UPDATE betachallenge SET status="W" WHERE id=? AND badge=? AND status="O"', (user.id, badge))
    cursor.execute('SELECT * FROM betabadges WHERE id=?', (user.id,))
    result = cursor.fetchone()
    if result == None:
      cursor.execute('INSERT INTO betabadges (id, badges) VALUES (?,?)', (user.id, badge))
    else:
      cursor.execute('UPDATE betabadges SET badges=? WHERE id=?', (result[1]+'\n'+badge, user.id))
    connection.commit()
    await client.send_message(message.channel, 'Assigned ' + badge + ' badge to ' + discorduser_to_discordname(user))
  else:
    await client.send_message(message.channel, no_permissions_message)

#async def badge(message, args):
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
#     elif flair_post(name, badge, 'Victory'):
#       badges = add_badge(name, badge)
#       print('Badges: ' + str(badges))
#       user = redditname_to_discorduser(name, message.server)
#       if badges == 8: #Badgesheet and 8 badges
#         await client.send_message(user, embed=singles_embed)
#       if badges == 9: #E4singles is 10th comment
#         await client.send_message(user, embed=singles_e4_embed)
#         roles = message.server.roles
#         for role in roles:
#           if role.name=='Hall of Fame':
#             fame_role=role

#         if not any([role == fame_role for role in user.roles]):
#           await client.add_roles(user, leak_role)
#         await client.send_message(client.get_channel('451570995417972751'), 'Congratulations ' + user.mention + '!')
#       msg = 'Assigned badge ' + badge + ' to ' + name
#     else:
#       msg = name + ' does not have a matching challenge'
#   else:
#     msg = no_permissions_message
#   await client.send_message(message.channel, msg)
