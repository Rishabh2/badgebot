from header import *
async def time(message, args):
  currentDT = datetime.datetime.now()
  gmt = (currentDT.strftime("%H:%M"))
  Hour = currentDT.hour
  Min = currentDT.minute
  if message.content.lower().endswith('gmt'):
    await client.send_message(message.channel, gmt)
  elif message.content.lower().endswith('cst'):
    Hour = Hour - 6 + 1
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('est') or message.content.lower().endswith('iet'):
    Hour = Hour - 5 + 1
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('prt'):
    Hour = currentDT.hour - 4
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('agt') or message.content.lower().endswith('bet'):
    currentDT = datetime.datetime.now()
    Min = currentDT.minute
    Hour = currentDT.hour - 3
    if Hour < 0:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('cat'):
    Hour = currentDT.hour - 1
    if Hour < 0:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('gmt'):
    Hour = currentDT.hour
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('mst'):
    Hour = currentDT.hour - 7 + 1
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('pnt'):
    Hour = currentDT.hour - 7
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('pst'):
    Hour = currentDT.hour - 8 + 1
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('ast'):
    Hour = currentDT.hour - 9 + 1
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('hst'):
    Hour = currentDT.hour - 10
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('mit'):
    Hour = currentDT.hour - 10
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('nst'):
    Hour = currentDT.hour - 12
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('sst'):
    Hour = currentDT.hour - 13
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('aet'):
    Hour = currentDT.hour - 14
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('jst'):
    Hour = currentDT.hour + 9
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('ctt'):
    Hour = currentDT.hour + 8
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('vst'):
    Hour = currentDT.hour + 7
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('bst'):
    Hour = currentDT.hour + 6
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('plt'):
    Hour = currentDT.hour + 5
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('net'):
    Hour = currentDT.hour + 4
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('eat'):
    Hour = currentDT.hour + 3
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('art') or message.content.lower().endswith('eet'):
    Hour = currentDT.hour + 2
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('ect'):
    Hour = currentDT.hour + 1 + 1
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('eet'):
    Hour = currentDT.hour + 2 + 1
    if Hour > 23:
      Hour = Hour - 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
  elif message.content.lower().endswith('utc'):
    if Hour < 0:
      Hour = Hour + 24
    if Min >= 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str(Min))
    if Min < 10:
      await client.send_message(message.channel, str(Hour) + str(":") + str("0") + str(Min))
