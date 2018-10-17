from header import *
async def setbday(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_about)
    return
  msg = None
  embed = None
  args = args.upper()
  args = args.split()
  if len(args) != 2:
    embed = help_about
  elif args[1][:3] not in months:
    msg = 'That is not a valid month'
    embed = help_about
  elif int(args[0]) < 1 or int(args[0]) > days[months.index(args[1][:3])]:
    msg = 'That is not a valid day'
    embed = help_about
  else:
    user = message.author.id
    month = months.index(args[1][:3])
    day = int(args[0])
    cursor.execute(bday_select_str, (user,))
    result = cursor.fetchone()
    if result == None:
      cursor.execute(bday_insert_str, (user, month, day))
    else:
      cursor.execute(bday_update_str, (month, day, user))
    connection.commit()
    msg = 'Bday set'
  await client.send_message(message.channel, content=msg, embed=embed)
