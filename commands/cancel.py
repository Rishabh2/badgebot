from header import *
async def cancel(message, args):
  cursor.execute(challenge_cancel_str, (int(message.timestamp.timestamp()),message.author.id))
  await client.send_message(message.channel, 'Challenge Canceled')
