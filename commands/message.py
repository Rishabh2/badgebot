from header import *
async def message(message, args):
  if haspermission(message.author.id):
    (userid, messagetext) = args.split(maxsplit=1)
    if userid == passwords.modpass:
      user = client.get_channel('372042060913442820')
    else:
      user = id_to_discorduser(userid)
    if user == None or messagetext == None or len(messagetext) == 0:
      msg = (message.channel, 'Usage: !message USER-ID-HERE message text goes here')
    else:
      msg = (user, messagetext)
  else:
    msg = (message.channel, no_permissions_message)
  await client.send_message(*msg)
