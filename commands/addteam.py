async def addteam(message, args):
  cursor.execute(team_insert_str, (message.author.id, args, int(message.timestamp.timestamp())))
  connection.commit()
  await client.send_message('Done')
