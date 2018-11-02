from header import *
async def cancel(message, args):
  await client.send_message(message.channel, 'Are you sure you want to cancel your challenge? (y/n)')
  resp = await client.wait_for_message(timeout=60, author=message.author, channel=message.channel)
  if resp != None and resp.content.lower()[0] == 'y':
    cursor.execute(challenge_cancel_str, (int(message.timestamp.timestamp()),message.author.id))
    msg = 'Challenge cancelled'
  else:
    msg = 'Challenge not cancelled'
  await client.send_message(message.channel, msg)
