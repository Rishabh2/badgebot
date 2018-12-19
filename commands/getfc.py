from header import *
async def getfc(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_info)
    return
  user = getmention(message, args, message.server)
  if user == None:
    if len(args) == 0:
      userid = discorduser_to_id(message.author)
    else:
        await client.send_message(message.channel, 'There is no one on this server named ' + args)
        return
  else:
    userid = discorduser_to_id(user)
  cursor.execute(fc_select_str, (userid,))
  result = cursor.fetchone()
  if result == None or result[0] == None:
    await client.send_message(message.channel, id_to_discordname(userid,message.server ) + " does not have a registered friend code.")
  elif result[1] == None:
    msg = result[0]
    if userid == '178255522531639296':
      msg = "Scepti's FC: " + result[0]
    await client.send_message(message.channel, msg)
  else:
    embed = discord.Embed(color=badgebot_color, title=result[0])
    embed.set_thumbnail(url=result[1])
    await client.send_message(message.channel, embed=embed)
