from header import *
async def time(message, args):
  currentDT = datetime.datetime.now()
  gmt = (currentDT.strftime("%H:%M"))
  Hour = currentDT.hour
  Min = currentDT.minute
  if args == 'gmt':
    await client.send_message(message.channel, gmt)
  elif args == 'cst':
    Hour = Hour - 6 + 1
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'est' or args == 'iet':
    Hour = Hour - 5 + 1
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'prt':
    Hour = currentDT.hour - 4
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'agt' or args == 'bet':
    currentDT = datetime.datetime.now()
    Min = currentDT.minute
    Hour = currentDT.hour - 3
    if Hour < 0:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'cat':
    Hour = currentDT.hour - 1
    if Hour < 0:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'bst':
    Hour = currentDT.hour + 1
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'mst':
    Hour = currentDT.hour - 7 + 1
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'pnt':
    Hour = currentDT.hour - 7
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'pst':
    Hour = currentDT.hour - 8 + 1
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'ast':
    Hour = currentDT.hour - 9 + 1
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'hst':
    Hour = currentDT.hour - 10
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'mit':
    Hour = currentDT.hour - 10
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'nst':
    Hour = currentDT.hour - 12
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'sst':
    Hour = currentDT.hour - 13
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'aet':
    Hour = currentDT.hour - 14
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'jst':
    Hour = currentDT.hour + 9
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'ctt':
    Hour = currentDT.hour + 8
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'kst':
    Hour = currentDT.hour + 9
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'vst':
    Hour = currentDT.hour + 7
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'bst':
    Hour = currentDT.hour + 6
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'plt':
    Hour = currentDT.hour + 5
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'net':
    Hour = currentDT.hour + 4
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'eat':
    Hour = currentDT.hour + 3
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'art':
    Hour = currentDT.hour + 2 + 1
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'cet':
    Hour = currentDT.hour + 1 + 1
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'eet':
    Hour = currentDT.hour + 2
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'utc':
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif args == 'why':
    await client.send_message(message.channel, 'https://youtu.be/-5wpm-gesOY')
  elif len(args) == 0:
    await client.send_message(message.channel, "Valid timezones include: gmt, cat, agt, bet, est, iet, prt, cst, mst, pst, pnt, ast, hst, mit, nst, sst, aet, jst, kst, ctt, vst, plt, net, eat, art, cet, eet, bst, utc. Please contact Scepti if you would like a timezone added. ^_^")
  else:
    await client.send_message(message.channel, str(args) + " is not a valid timezone, please use `!time` for a list of included timezones.")
