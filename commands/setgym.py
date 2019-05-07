from header import *
async def setgym(message, args):
  gymtype, intro = args.split(maxsplit=1)
  gymtype = gymtype.lower()
  cursor.execute(gym_update_str, (intro, gymtype))
  connection.commit()
  await client.send_message(message.channel, 'Done')
