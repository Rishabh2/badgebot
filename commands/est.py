from header import *
async def est(message, args):
  await client.send_message(message.channel, datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-  4))).strftime('%I:%M%p'))
