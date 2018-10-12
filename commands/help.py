from header import *
async def help(message, args):
  user = getmention(message)
  if user == None:
    user = message.author
  for hp in help_embeds:
    await client.send_message(user, embed=hp)
    await asyncio.sleep(0.1)
