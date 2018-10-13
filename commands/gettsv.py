from header import *
async def gettsv(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_tsv)
    return
  msg = None
  embed = None
  mentuser = getmention(message)
  if mentuser == None:
    user = message.author.id
  else:
    user = mentuser.id
  if len(args) == 0 or mentuser != None:
    cursor.execute(tsv_select_str, (user,))
    results = cursor.fetchall()
    if results == None or len(results) == 0:
      msg = "User doesn't have any registered tsvs"
    else:
      msg = ''
      for result in results:
        msg += result[0] + ' ' + result[1] + '\n'
  else:
    if len(args) != 4:
      msg = 'The tsv you are searching for must be exactly 4 characters'
      embed = help_tsv
    else:
      cursor.execute(tsv_request_str, (args,))
      results = cursor.fetchall()
      if results == None or len(results) == 0:
        msg = "No one has that tsv"
      else:
        msg = ''
        server = message.server
        for result in results:
          msg += id_to_discordname(result[0], server) + ' has that tsv in the game ' + result[1] + '\n'
  await client.send_message(message.channel, content=msg, embed=embed)
