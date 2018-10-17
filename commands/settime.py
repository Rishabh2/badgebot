from header import *
async def settime(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_about)
    return
  msg = None
  embed = None
  argr = args.lower()[::-1]
  args = [x[::-1] for x in argr.split(maxsplit=1)]
  name = message.author.id
  try:
    offset = int(args[0])
    cursor.execute(time_select_str, (name,))
    result = cursor.fetchone()
    if result == None:
      cursor.execute(time_insert_str, (name, offset))
    else:
      cursor.execute(time_update_str, (offset, name))
    connection.commit()
    msg = 'Time offset saved'
  except:
    embed = help_about
  await client.send_message(message.channel, content=msg, embed=embed)
