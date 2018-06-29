from header import *
async def wipe(message, args):
  redditn = discorduser_to_redditname(message.author)
  channel = message.channel.id
  try:
    count=int(args)
  except:
    count=100
  if (channel == singles_e4_channel and redditn in singles_e4) or (channel == doubles_e4_channel and redditn in doubles_e4) or (channel in singles_channels and singles_channels.index(channel) == singles_leaders.index(redditn)) or (channel in doubles_channels and doubles_channels.index(channel) == doubles_leaders.index(redditn)):
    ms=[]
    async for m in client.logs_from(client.get_channel(channel), limit=count):
      if not m.pinned:
        ms.append(m)
    await client.delete_messages(ms)
  else:
    await client.send_message(message.channel, no_permissions_message)
