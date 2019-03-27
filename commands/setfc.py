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
    user = message.author.id
    c = message.channel
    await client.send_message(c, 'First, what text do you want to have in your fc?\nYou can include things like IGN, game version, or even multiple FCs')
    resp = await client.wait_for_message(timeout=60, author=message.author, channel=c)
    if resp == None or resp.content.lower()=='cancel':
      await client.send_message(c, 'Bye')
      return
    args = resp.content
    await client.send_message(c, 'Now, what image do you want to include in your fc?\nEither provide a direct link to the image or embed it directly in your message\nIf you don\'t want an image, just say "No thanks"')
    resp = await client.wait_for_message(timeout=60, author=message.author, channel=c)
    if resp == None or resp.content.lower()=='cancel':
      await client.send_message(c, 'Bye')
      return
    cursor.execute(fc_select_str, (user,))
    result = cursor.fetchone()
    if result == None:
      url = None
    else:
      url = result[1] #Get the existing url
    if len(resp.embeds) > 0:
      url = resp.embeds[0]['url']

  else:
    user = message.author.id
    url = None
    if len(message.embeds) > 0:
      url = message.embeds[0]['url']
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
