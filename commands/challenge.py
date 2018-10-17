from header import *
async def challenge(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, help_gym)
    return
  userid = message.author.id
  cursor.execute(lp_select_str, (userid,))
  result = cursor.fetchone()
  if result == None:
    msg = 'You do not have a league pass. Create one with !setlp'
  else:
    cursor.execute(open_challenge_select_str, (userid,))
    result = cursor.fetchone()
    if result != None:
      msg = 'You have an open ' + result[1] + ' challenge'
    elif len(args) == 0:
      msg = 'You do not have an active challenge'
    elif isbadge(args):
      cursor.execute(challenge_str, (userid, int(message.timestamp.timestamp()), args))
      connection.commit()
      msg = 'Challenge Submitted!'
    else:
      msg = args + ' is not a valid badge'
  await client.send_message(message.channel, msg)
