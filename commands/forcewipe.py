from header import *
async def forcewipe(message, args):
  if message.author.id == '242558859300831232':
    async for m in client.logs_from(message.channel, limit=int(args)):
      if not m.pinned:
        await client.delete_message(m)
        await asyncio.sleep(0.5)
  else:
    await client.send_message(message.channel, no_permissions_message)
