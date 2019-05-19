from header import *
async def store(message, args):
  cursor.execute(text_insert_str, (message.author.id, args, int(message.timestamp.timestamp())))
  connection.commit()
  await client.send_message(message.channel, 'Done')
