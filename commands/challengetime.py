from header import *
async def challengetime(message, args):
  userid = message.author.id
  cursor.execute(lp_select_str, (userid,))
  result = cursor.fetchone()
  if result == None:
    msg = 'You do not have a league pass. Set up one with !setlp'
  else:
    cursor.execute(recent_challenge_select_str, (userid,))
    recent_time = cursor.fetchone()
    recent_time = recent_time[0] if recent_time != None else 0
    current_time = int(message.timestamp.timestamp())
    time_dif = current_time - recent_time
    time_remaining = challenge_time_limit - time_dif
    hours = time_remaining / (60 * 60)
    if time_remaining > 0:
      msg = 'You have {:01.1f} hours remaining'.format(hours)
    else:
      msg = 'You are ready to submit a challenge'
  await client.send_message(message.channel, msg)

