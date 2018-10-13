from header import *
async def addtsv(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_tsv)
    return
  msg = None
  embed = None
  user = message.author.id
  val = args.split(maxsplit=1)
  if len(val) < 2:
    embed = help_tsv
  else:
    tsv = val[0]
    game = val[1]
    if len(tsv) != 4 or not tsv.isdigit():
      msg = "Your tsv must be exactly 4 numbers"
      embed = help_tsv
    else:
      cursor.execute(tsv_insert_str, (user, tsv, game))
      connection.commit()
      msg = 'Added ' + tsv + ' for ' + game
  await client.send_message(message.channel, content=msg, embed=embed)
