from header import *
async def wipe(message, args):
  redditn = discorduser_to_redditname(message.author)
  channel = message.channel.id
  try:
    count=int(args)
  except:
    count=100
  if (channel == singles_e4_channel and redditn in singles_e4) or (channel == doubles_e4_channel and redditn in doubles_e4) or (channel in singles_channels and redditn in singles_leaders and singles_channels.index(channel) == singles_leaders.index(redditn)) or (channel in doubles_channels and redditn in doubles_leaders and doubles_channels.index(channel) == doubles_leaders.index(redditn)) or (channel == arcade_channel and coinpermission(message.author)):
    await client.purge_from(message.channel, limit=count, check=lambda x: not x.pinned)
  else:
    await client.send_message(message.channel, no_permissions_message)
