from header import *
async def swearlist(message, args):
  cursor.execute(swear_dump_str)
  results = cursor.fetchall()
  results = list(filter(lambda x: id_to_discordname(x[0], pvl) != None, results))
  dump = ''
  for result in results:
    dump += str(result[1]) + ' - ' + id_to_discordname(result[0], pvl) + '\n'
  await client.send_message(message.channel, dump)
