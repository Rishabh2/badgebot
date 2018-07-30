from header import *
async def swearlist(message, args):
  user = getmention(message)
  try:
    limit = int(args)
  except:
    limit = 0
  if user == None:
    cursor.execute(swear_dump_str, (limit,))
    results = cursor.fetchall()
    results = list(filter(lambda x: id_to_discordname(x[0], client.get_server('372042060913442818')) != None, results))
    dump = ''
    for result in results:
      dump += str(result[1]) + ' - ' + id_to_discordname(result[0], client.get_server('372042060913442818')) + '\n'
  else:
    cursor.execute(swear_select_str, (discorduser_to_id(user),))
    result = cursor.fetchone()
    if result == None or result[0] == None:
      dump = '0'
    else:
      dump = str(result[0])
  await client.send_message(message.channel, dump)
