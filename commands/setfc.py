from header import *
async def setfc(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_about)
    return
  url=None
  if len(message.mentions) > 0 or len(message.raw_mentions) > 0:
    msg = 'Please do not include user tags in your FC'
    await client.send_message(message.channel, msg)
    return
  elif len(args) == 0:
    msg = 'Please provide a friend code'
  else:
    user = message.author.id
    url = None
    if len(message.attachments) > 0:
      url = message.attachments[0]['url']
    cursor.execute(fc_select_str, (user,))
    result = cursor.fetchone()
    if result == None:
      cursor.execute(fc_insert_str, (user, args, url))
    else:
      cursor.execute(fc_update_str, (args, url, user))
    connection.commit()
    msg = 'Friend code set to '
  if url != None:
    embed = discord.Embed(color=badgebot_color, title=args)
    embed.set_thumbnail(url=url)
    await client.send_message(message.channel, content=msg, embed=embed)
  else:
    await client.send_message(message.channel, msg+args)
