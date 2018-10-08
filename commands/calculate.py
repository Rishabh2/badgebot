from header import *
async def calculate(message, args):
  allowed_chars = '+-*/^0123456789.() '
  if all([c in allowed_chars for c in args]):
    try:
      args = eval(args.replace('^', '**'))
    except:
      await client.send_message(message.channel, "Please check your syntax and try again")
      return
    await client.send_message(message.channel, args)
  else:
    await client.send_message(message.channel, "Please only include numbers and mathematical operations")
