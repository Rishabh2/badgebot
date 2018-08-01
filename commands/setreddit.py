from header import *
async def setreddit(message, args):
  if len(args) == 0:
    msg = "Please provde your reddit username"
  else:
    user = message.author.id
    cursor.execute(reddit_select_str, (user,))
    result = cursor.fetchone()
    if result == None:
      cursor.execute(reddit_insert_str, (user, args))
    else:
      cursor.execute(reddit_update_str, (args, user))
    connection.commit()
    msg = 'Reddit username set to ' + args
  await client.send_message(message.channel, msg)
