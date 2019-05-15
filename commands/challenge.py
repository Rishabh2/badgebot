from header import *
async def challenge(message, args):
  if args.lower().strip() == 'help':
    await client.send_message(message.channel, embed=help_gym)
    return
  args = args.lower()
  userid = message.author.id
  cursor.execute(lp_select_str, (userid,))
  result = cursor.fetchone()
  cursor.execute(recent_challenge_select_str, (userid,))
  recent_time = cursor.fetchone()
  recent_time = recent_time[0] if recent_time != None else 0
  current_time = int(message.timestamp.timestamp())
  if result == None:
    msg = 'You do not have a league pass. Create one with !setlp'
  else:
    cursor.execute(open_challenge_select_str, (userid,))
    result = cursor.fetchone()
    if result != None:
      msg = 'You have an open ' + result[1] + ' challenge'
    elif len(args) == 0:
      msg = 'You do not have an active challenge'
    elif current_time - recent_time < challenge_time_limit:
      msg = 'Your last challenge was too recent. Please wait 20 hours between challenges'
    elif isbadge(args):
      cursor.execute(badge_count_str, (userid,))
      result = cursor.fetchall()
      if args.lower() == 'e4champ' and len(result) != 8:
        msg = 'You need 8 badges to challenge the elite 4'
      else:
        cursor.execute(challenge_str, (userid, current_time, args))
        connection.commit()
        cursor.execute(gym_select_str, (args.lower(),))
        result = cursor.fetchone()
        gym_channel = client.get_channel(result[0])
        embed = discord.Embed(title=gym_channel.name.replace('-',' ').title(), color=badgebot_color, description=result[1])
        embed.set_image(url=result[2])
        await client.send_message(message.author, embed=embed)
        msg = 'Challenge Submitted!\n'+gym_channel.mention
    else:
      msg = args + ' is not a valid badge'
  await client.send_message(message.channel, msg)
