from header import *
async def getlp(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_info)
    return
  user = getmention(message, args, message.server)

  if user == None:
    await client.send_message(message.channel, 'There is no one on this server named ' + args)
    return

  embed = discord.Embed(title=discorduser_to_discordname(user)+"'s League Pass",color=badgebot_color)
  embed.set_footer(text="Contact @DePVLoper in #committee-contact for any questions.")

  cursor.execute(lp_select_str, (user.id,))
  result = cursor.fetchone()

  if result == None:
    msg = no_lp_message.format(discorduser_to_discordname(user))
    embed.add_field(name="No LP found",value=msg)
    await client.send_message(message.channel, embed=embed)
  else:
    embed.set_image(url=roster_url.format(user.id+'-'+result[-1])) #Get salted LP
    embed.add_field(name='Badges',value=user_badges(user.id))

    mons = result[1].split(',')
    msg = ', '.join([x for x in mons[:6]])
    embed.add_field(name="Main Roster",value=msg, inline=False)
    msg = ', '.join([x for x in mons[6:]])
    if msg != '':
      embed.add_field(name="Sideboard",value=msg, inline=False)

    await client.send_message(message.channel, embed=embed)
