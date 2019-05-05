from header import *
async def propose(message, args):
  if haspermission(message.author):
    lines = args.split('\n')[1:]
    for line in lines:
      await client.add_reaction(message, line.split()[0])
    await client.pin_message(message)
    await client.send_message(message.channel, '<@&569708333943226368>')
