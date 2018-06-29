from header import *
async def dumptsv(message, args):
  cursor.execute(tsv_dump_str)
  results = cursor.fetchall()
  results = list(filter(lambda x: id_to_discordname(x[0]) != None, results))
  results.sort(key=lambda x: x[1])
  dump = ''
  for result in results:
    dump += result[1] + ' ' + result[2] + ' ' + id_to_discordname(result[0]) +  '\n'
  post = requests.post("https://hastebin.com/documents", data=dump.encode('utf- 8'))
  await client.send_message(message.channel, "https://hastebin.com/" + post.json()["key"])
