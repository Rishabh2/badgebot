from header import *
async def info(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_info)
    return
  user = getmention(message, args, message.server)
  if user == None:
    user = message.author
  userid = discorduser_to_id(user)
  #Id, FC, Url, Reddit, Swear, Coins, Month, Day
  cursor.execute(info_dump_str, (userid,))
  result = cursor.fetchone()
  if result == None:
    await client.send_message(message.channel, 'User has no info')
  else:
    embed = discord.Embed(title="User Info", color=discord.Color(0x85bff8))
    if result[1] != None:
      embed.add_field(name='Friend Code', value=result[1])
    if result[2] != None:
      embed.set_thumbnail(url=result[2])
    if result[4] != None:
      embed.add_field(name='Swear Jar Triggers', value=result[4])
    else:
      embed.add_field(name='Swear Jar Triggers', value=0)
    if result[5] != None:
      embed.add_field(name='PVL Coins', value=result[5])
    else:
      embed.add_field(name='PVL Coins', value=0)
    if result[6] != None:
      embed.add_field(name='Birthday', value=str(result[7]) + ' ' + months[result[6]])
    cursor.execute(tsv_select_str, (userid,))
    result = cursor.fetchall()
    if result != None and len(result) > 0:
      for pair in result:
        embed.add_field(name='TSV: '+pair[0], value=pair[1])

    cursor.execute(lp_select_str, (user.id,))
    result = cursor.fetchone()
    if result != None:
      embed.add_field(name='Badges',value=user_badges(user.id))

      embed.set_image(url=roster_url.format(user.id+'-'+result[-1])) #Get salted LP
      mons = result[1].split(',')
      msg = ', '.join([x for x in mons[:6] if x!=None])
      embed.add_field(name="Main Roster",value=msg)
      msg = ', '.join([x for x in mons[6:] if x!=None])
      if msg != '':
        embed.add_field(name="Sideboard",value=msg)


    await client.send_message(message.channel, embed=embed)
