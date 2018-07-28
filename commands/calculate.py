from header import *
async def calculate(message, args):
  args = eval(args)
  await client.send_message(message.channel, args)
