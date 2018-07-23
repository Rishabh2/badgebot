from header import *
async def badge(message, args):
  if haspermission(message.author):
    (name, badge) = args.split(maxsplit=1)
    user = getmention(message)
    if user != None:
      name = discorduser_to_redditname(user)
    badge = badge.lower()
    if name == None:
      msg = no_reddit_message.format(discorduser_to_discordname(user))
    elif not wiki_exists(name):
      msg = name + ' does not have a reigstered league pass'
    elif not isbadge(badge):
      msg = badge + ' is not a valid badge'
    elif flair_post(name, badge, 'Victory'):
      badges = add_badge(name, badge)
      print('Badges: ' + str(badges))
      user = redditname_to_discorduser(name, message.server)
      if badges == 8: #Badgesheet and 8 badges
        await client.send_message(user, embed=singles_embed)
      if badges == 9: #E4singles is 10th comment
        await client.send_message(user, embed=singles_e4_embed)
        roles = message.server.roles
        for role in roles:
          if role.name=='Hall of Fame':
            fame_role=role

        if not any([role == fame_role for role in user.roles]):
          await client.add_roles(user, leak_role)
        await client.send_message(client.get_channel('451570995417972751'), 'Congratulations ' + user.mention + '!')
      msg = 'Assigned badge ' + badge + ' to ' + name
    else:
      msg = name + ' does not have a matching challenge'
  else:
    msg = no_permissions_message
  await client.send_message(message.channel, msg)
