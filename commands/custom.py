from header import *
async def custom(message, args):
  if args=='e4':
    embed = singles_e4_embed
  else:
    embed = singles_embed
  await client.send_message(message.channel, embed=embed)
