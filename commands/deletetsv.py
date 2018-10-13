from header import *
async def deletetsv(message, args):
  msg = None
  embed = None
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_tsv)
    return
  user = message.author.id
  if len(args) != 4:
    msg = "The tsv you want to delete must be exactly 4 characters"
    embed = help_tsv
  else:
    cursor.execute(tsv_delete_str, (user, args))
    connection.commit()
    msg = 'Deleted TSV ' + args
  await client.send_message(message.channel, content=msg, embed=embed)
