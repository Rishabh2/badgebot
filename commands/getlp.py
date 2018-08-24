from header import *
async def getlp(message, args):
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
  else:
    msg = ', '.join([x for x in result[1:7] if x!=None])
    embed.add_field(name="Main Roster",value=msg)
    msg = ', '.join([x for x in result[7:] if x!=None])
    if msg != '':
      embed.add_field(name="Sideboard",value=msg)
    embed.set_image(url=roster_url.format(user.id))

  await client.send_message(message.channel, embed=embed)
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
