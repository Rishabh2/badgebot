from header import *
async def wipe(message, args):
  try:
    count = int(args)
  except:
    count = 100

  if haspermission(message.author):
    await client.send_message(message.channel, 'Are you sure? (y/n)')
    resp = await client.wait_for_message(timeout=60, author=message.author, channel=message.channel)
    if resp != None and resp.content.lower()[0] == 'y':
      await client.purge_from(message.channel, limit=count, check=lambda x: not x.pinned)
    else:
      await client.send_message(id_to_discorduser('242558859300831232', message.server), 'Wipe attempt in ' + message.channel.name + ' by ' + discorduser_to_discordname(message.author))
  else:
    await client.send_message(message.channel, no_permissions_message)
    await client.send_message(id_to_discorduser('242558859300831232', message.server), 'Wipe attempt in ' + message.channel.name + ' by ' + discorduser_to_discordname(message.author))
