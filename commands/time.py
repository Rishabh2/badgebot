from header import *
async def time(message, args):
  args = args.lower()
  currentDT = datetime.datetime.now()
  if args == 'gmt':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-  0))).strftime('%I:%M%p'))
  elif args == 'cst':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-  (6 - 1)))).strftime('%I:%M%p'))
  elif args == 'est' or args == 'iet':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-  (5 - 1)))).strftime('%I:%M%p'))
  elif args == 'prt':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-  4))).strftime('%I:%M%p'))
  elif args == 'agt' or args == 'bet':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-  3))).strftime('%I:%M%p'))
  elif args == 'cat':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-  1))).strftime('%I:%M%p'))
  elif args == 'bst':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=+  1))).strftime('%I:%M%p'))
  elif args == 'mst':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-  (7-1)))).strftime('%I:%M%p'))
  elif args == 'pnt':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-  7))).strftime('%I:%M%p'))
  elif args == 'pst':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-  (8-1)))).strftime('%I:%M%p'))
  elif args == 'ast':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-  (9-1)))).strftime('%I:%M%p'))
  elif args == 'hst' or args == 'mit':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-  10))).strftime('%I:%M%p'))
  elif args == 'nst':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-  12))).strftime('%I:%M%p'))
  elif args == 'sst':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-  13))).strftime('%I:%M%p'))
  elif args == 'aet':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-  14))).strftime('%I:%M%p'))
  elif args == 'jst' or args == 'kst':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=+  9))).strftime('%I:%M%p'))
  elif args == 'ctt':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=+  8))).strftime('%I:%M%p'))
  elif args == 'vst':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=+  7))).strftime('%I:%M%p'))
  elif args == 'plt':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=+  5))).strftime('%I:%M%p'))
  elif args == 'net':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=+  4))).strftime('%I:%M%p'))
  elif args == 'eat':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=+  3))).strftime('%I:%M%p'))
  elif args == 'art':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=+  (2+1)))).strftime('%I:%M%p'))
  elif args == 'cet':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=+  (1+1)))).strftime('%I:%M%p'))
  elif args == 'eet':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=+  (2+1)))).strftime('%I:%M%p'))
  elif args == 'utc':
    await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-  0))).strftime('%I:%M%p'))
  elif args == 'why':
    await client.send_message(message.channel, 'https://youtu.be/-5wpm-gesOY')
  elif len(args) == 0:
    await client.send_message(message.channel, "Valid timezones include: gmt, cat, agt, bet, est, iet, prt, cst, mst, pst, pnt, ast, hst, mit, nst, sst, aet, jst, kst, ctt, vst, plt, net, eat, art, cet, eet, bst, utc. Please contact Scepti if you would like a timezone added. ^_^")
  else:
    await client.send_message(message.channel, str(args) + " is not a valid timezone, please use `!time` for a list of included timezones.")
