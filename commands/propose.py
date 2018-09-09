from header import *
async def propose(message, args):
  numbers = 'ZERO ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE'.split()
  lines = args.split('\n')[1:]
  for line in lines:
    await client.add_reaction(message, line.split()[0])
  await client.pin_message(message)
  await client.send_message(message.channel, '<@&384724202613112843>')
