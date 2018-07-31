from header import *
async def forcewipe(message, args):
  if haspermission(message.author):
    async for m in client.logs_from(message.channel, limit=int(args)):
      if not m.pinned:
        await client.delete_message(m)
  else:
    await client.send_message(message.channel, no_permissions_message)
