from header import *
async def read(message, args):
  if message.channel.id not in ['577960539016396830', '577960497580867594']:
    await client.send_message(message.channel, 'Only to be used in public draft channels')
    return
  user = getmention(message, args, message.server)
  if user == None:
    await client.send_message(message.channel, 'There is no one on this server named ' + args)
    return
  target = user.id
  cursor.execute(text_select_str, (user.id,))
  result = cursor.fetchone()
  if result is None:
    msg = 'User did not have any text saved'
  else:
    msg = result[0]
  await client.send_message(message.author, msg)
  await client.send_message(message.channel, discorduser_to_discordname(message.author) + ' has read the info of ' + discorduser_to_discordname(user))
