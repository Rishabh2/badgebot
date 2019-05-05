from header import *
async def message(message, args):
  if mutepermission(message.author) or message.author.id in ['159118090519445514', '242558859300831232', '245963462952484864']:
    (userid, messagetext) = args.split(maxsplit=1)
    target = getmention(message, userid, message.server)
    if target is None:
      target = client.get_channel(userid)
    if target is None:
      target = id_to_discorduser(userid, message.server)
    msg = (target, messagetext)
  else:
    msg = (message.channel, no_permissions_message)
  await client.send_message(*msg)
