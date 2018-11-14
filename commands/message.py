from header import *
async def message(message, args):
  if message.author.id == '242558859300831232' or message.author.id == '159118090519445514':
    (userid, messagetext) = args.split(maxsplit=1)
    target = client.get_channel(userid)
    msg = (target, messagetext)
  else:
    msg = (message.channel, no_permissions_message)
  await client.send_message(*msg)
