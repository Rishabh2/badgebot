from header import *
async def getlp(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_info)
    return
  user = getmention(message)

  if user == None:
    user = message.author

  embed = discord.Embed(title=discorduser_to_discordname(user)+"'s League Pass",color=discord.Color(0xbc614e))
  embed.set_footer(text="Contact @DePVLoper in #committee-contact for any questions.")

  cursor.execute('SELECT * FROM betalp WHERE id=?', (user.id,))
  result = cursor.fetchone()

  if result == None:
    msg = no_lp_message.format(discorduser_to_discordname(user))
    embed.add_field(name="No LP found",value=msg)
    await client.send_message(message.channel, embed=embed)
  else:
    embed.set_image(url=roster_url.format(user.id+'-'+result[-1])) #Get salted LP
    cursor.execute('SELECT badge FROM betabadges WHERE id=?', (user.id,))
    badgeresult = cursor.fetchall()
    if len(badgeresult) > 0:
      embed.add_field(name='Badges',value=' '.join([badge_ids[r[0]] for r in badgeresult]), inline=False)

    msg = ', '.join([x for x in result[1:7] if x!=None])
    embed.add_field(name="Main Roster",value=msg, inline=False)
    msg = ', '.join([x for x in result[7:11] if x!=None])
    if msg != '':
      embed.add_field(name="Sideboard",value=msg, inline=False)

    await client.send_message(message.channel, embed=embed)
    #await client.send_file(message.channel, '/root/badgebot/rosters/{}.png'.format(user.id))

# async def getlp(message, args):
#   user = getmention(message)
#   if user == None:
#     if len(args) == 0:
#       user = message.author
#       name = discorduser_to_redditname(message.author)
#     else:
#       name = args
#   else:
#     name = discorduser_to_redditname(user)
#   if name == None:
#     msg = no_reddit_message.format(discorduser_to_discordname(user))
#   else:
#     msg = get_league_pass(name)
#     if not isinstance(msg, str):
#       msg=msg.url
#   await client.send_message(message.channel, msg)
