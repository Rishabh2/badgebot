from header import *
async def deletetsv(message, args):
  user = message.author.id
  if len(args) != 4:
    msg = "The tsv you want to delete must be exactly 4 characters"
  else:
    cursor.execute(tsv_delete_str, (user, args))
    connection.commit()
    msg = 'Deleted TSV ' + args
  await client.send_message(message.channel, msg)
