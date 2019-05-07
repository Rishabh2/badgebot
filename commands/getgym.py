from header import *
async def getgym(message, args):
  cursor.execute(gym_select_str, (args.lower(),))
  result = cursor.fetchone()
  if result is None:
    await client.send_message(message.channel, 'No Gym Found')
    return
  else:
    embed = discord.Embed(title=(args + ' gym').title(), color=badgebot_color, description=result[1])
    embed.set_image(url=result[2])
    await client.send_message(message.channel, embed=embed)
    return
