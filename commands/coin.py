from header import *
async def coin(message, args):
	embed = discord.Embed(colour=discord.Colour(0xbc614e))
	embed.set_footer(text="Contact @DePVLoper in #committee-contact for any questions.")

  if len(args) == 0:
    cursor.execute(coins_dump_str)
    results = cursor.fetchall()
    results = list(filter(lambda x: id_to_discordname(x[0], client.get_server('372042060913442818')) != None and x[1] != 0, results))
    dump = ''
    for result in results:
      dump += str(result[1]) + ' - ' + id_to_discordname(result[0], client.get_server('372042060913442818')) + '\n'
    msg = dump
	
	embed.add_field(name="Coins Leaderboard", value=msg)
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
      user = redditname_to_discorduser(name, message.server)
    if user == None:
      msg = 'There is no one on the server with the reddit name ' + name
    else:
      userid = discorduser_to_id(user)
      cursor.execute(coins_select_str, (userid,))
      result = cursor.fetchone()
      if change == None and result != None and result[0] != None:
        msg = result[0]
		embed.add_field(name="Coins for"+discorduser_to_discordname(user),value=msg)
      elif coinpermission(message.author):
        if result == None:
          change = 0 if change == None else change
          cursor.execute(coins_insert_str, (userid, change))
          msg = change
        else:
          value = 0 if result[0] == None else result[0]
          cursor.execute(coins_update_str, (change+value, userid))
          msg = value + " => " + (change+value)
		  embed.add_field("Coins for"+discorduser_to_discordname(user),value=msg)
      elif change==None:
        embed.add_field("Coins for"+discorduser_to_discordname(user),value="0")
      else:
        msg = no_permissions_message
		embed.add_field(name="Error!",value=msg)
  await client.send_message(message.channel, embed=embed)

