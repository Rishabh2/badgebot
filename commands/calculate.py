from header import *
async def calculate(message, args):
  allowed_chars = ['+','-','*','/','^','0','1','2','3','4','5','6','7','8','9','.']
  if all([c in allowed_chars for c in args]):
    try:
      args = eval(args)
    except:
      await client.send_message(message.channel, "Please check your syntax and try again")
      return
    await client.send_message(message.channel, args)
  else:
    await client.send_message(message.channel, "Please only include numbers and mathematical operations")
