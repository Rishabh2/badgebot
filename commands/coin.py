from header import *
async def coin(message, args):
  if len(args) == 0:
    cursor.execute(coins_dump_str)
    results = cursor.fetchall()
    results = list(filter(lambda x: id_to_discordname(x[0]) != None, results))
    dump = ''
    for result in results:
      dump += str(result[1]) + ' - ' + id_to_discordname(result[0]) + '\n'
    msg = dump
  else:
    splt = args.split(maxsplit=1)
    if len(splt) == 2:
      (name, change) = splt
    else:
      name = splt[0]
      change = None
    try:
      change = int(change)
    except:
      change = None
    user = getmention(message)
    if user == None:
      user = redditname_to_discorduser(name)
    if user == None:
      msg = 'There is no once on the server with the reddit name ' + name
    else:
      userid = discorduser_to_id(user)
      cursor.execute(coins_select_str, (userid,))
      result = cursor.fetchone()
      if change == None and result != None:
        msg = result[0]
      elif haspermission(message.author):
        if result == None:
          change = 0 if change == None else change
          cursor.execute(coins_insert_str, (userid, change))
        else:
          cursor.execute(coins_update_str, (change+result[0], userid))
        connection.commit()
        cursor.execute(coins_dump_str)
        results = cursor.fetchall()
        results = list(filter(lambda x: id_to_discordname(x[0]) != None, results))
        dump = ''
        for result in results:
          dump += str(result[1]) + ' - ' + id_to_discordname(result[0]) + '\n'
        msg = dump
      else:
        msg = no_permissions_message
  await client.send_message(message.channel, msg)

