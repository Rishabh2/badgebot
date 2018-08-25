from header import *
async def addtsv(message, args):
  user = message.author.id
  val = args.split(maxsplit=1)
  if len(val) < 2:
    msg = "To assign your tsv, use the command '!addtsv XXXX Game'"
  else:
    tsv = val[0]
    game = val[1]
    if len(tsv) != 4 or not tsv.isdigit():
      msg = "Your tsv must be exactly 4 numbers"
    else:
      cursor.execute(tsv_insert_str, (user, tsv, game))
      connection.commit()
      msg = 'Added ' + tsv + ' for ' + game
  await client.send_message(message.channel, msg)
