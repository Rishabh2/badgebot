from header import *
def pyramid(message, args):
  result = ''
  floor = random.randint(1,20)
  if floor == 1:
    result += '''''I see a shower of sparks…
…And in it, I see your POKéMON struggling with paralysis…'''
  elif floor == 2:
    result += '''I see poison…
…And, I see your POKéMON suffering
from the effects of poison…'''
  elif floor == 3:
    result += '''I see bright red flames…
…And, I see your POKéMON suffering
from burns…'''
  elif floor == 4:
    result += '''I sense the tremendous pressure of
unrequited anger…
It is a curse…
…And, I see your POKéMON drained of
Power Points and having no recourse
but to use STRUGGLE…'''
  elif floor == 5:
    result += '''I see POKéMON loftily airborne…
…And, I see your POKéMON frustrated
by powerless GROUND-type moves…'''
  elif floor == 6:
    result += '''I sense terrific energy rising from
the ground below…
…And, I see your POKéMON unable to
escape the power's clutches…'''
  elif floor == 7:
    result += '''I see ICE-type POKéMON…
…And, I see your POKéMON fighting
the freezing effects of ice…'''
  elif floor == 8:
    result += '''I see a flurry of moves that imperil
the user…
…And, I see your POKéMON falling
to them…'''
  elif floor == 9:
    result += '''I see PSYCHIC-type POKéMON…
…And, I see your POKéMON in torment
from PSYCHIC moves…'''
  elif floor == 10:
    result += '''I see ROCK-type POKéMON…
…And, I see your POKéMON suffering
from ROCK moves…'''
  elif floor == 11:
    result += '''I see FIGHTING-type POKéMON…
…And, I see your POKéMON pummeled
by FIGHTING moves…'''
  elif floor == 12:
    result += '''RAIN DANCE… SUNNY DAY…
SANDSTORM… HAIL…
I see POKéMON that become stronger
with the weather…
…And, I see your POKéMON confounded
by different types of moves…'''
  elif floor == 13:
    result += '''I see BUG-type POKéMON…
…And, I see your POKéMON suffering
from different kinds of attacks…'''
  elif floor == 14:
    result += '''I see DARK-type POKéMON…
…And, I see your POKéMON suffering
from DARK-type moves…'''
  elif floor == 15:
    result += '''I see WATER-type POKéMON…
…And, I see your POKéMON suffering
from WATER-type moves…'''
  elif floor == 16:
    result += '''I see GHOST-type POKéMON…
…And, I see your POKéMON suffering
from GHOST-type moves…'''
  elif floor == 17:
    result += '''I see STEEL-type POKéMON…
…And, I see your POKéMON suffering
from enormously powerful moves…'''
  elif floor == 18:
    result += '''I see flying POKéMON…
…And, I see your POKéMON suffering
from enormously powerful moves…'''
  elif floor == 19:
    result += '''I see those that have evolved from
the power of stones…
…And, I see your POKéMON suffering
from those powers…'''
  elif floor == 20:
    result += '''I see NORMAL-type POKéMON…
…And, I see your POKéMON suffering
from enormously powerful moves…'''

  result += '\n And your item is... '
  item = random.randint(1,31)
  if item == 1 or item == 2:
    result += 'Assault Vest'
  elif item == 3 or item == 4:
    result += 'Choice Band'
  elif item == 5 or item == 6:
    result += 'Choice Scarf'
  elif item == 7 or item == 8:
    result += 'Choice Specs'
  elif item == 9 or item == 10:
    result += 'Eviolite'
  elif item == 11 or item == 12:
    result += 'Focus Sash'
  elif item == 13 or item == 14:
    result += 'Leftovers'
  elif item == 15 or item == 16:
    result += 'Life Orb'
  elif item == 17 or item == 18:
    result += 'Power Herb'
  elif item == 19 or item == 20:
    result += 'White Herb'
  elif item == 21 or item == 22:
    result += 'Rocky Helmet'
  elif item == 23 or item == 24:
    result += 'Lum Berry'
  elif item == 25 or item == 26:
    result += 'Sitrus Berry'
  elif item == 27 or item == 28:
    result += 'Mega Stone'
  elif item == 29 or item == 30:
    result += 'Z-Crystal'
  elif item == 31:
    result += 'Sacred Ash'

  return result

def flair_post( username, badge, flair ):
  author = reddit.redditor(username)
  challenges = challenges_list(author, badge)
  if len(challenges) > 0:
    challenges[0].mod.flair(text=flair, css_class=flair_to_css(badge, flair))
    return True
  return False

def approve_rematch( username ):
  for submission in subreddit.mod.modqueue(only='submissions'):
    if submission.author.name.lower() == username.lower():
      submission.mod.approve()
      for i, tf in enumerate(title_flairs):
        if tf in submission.title.lower():
          submission.mod.flair(text=challenge_flairs[i], css_class=challenge_css[i])
      return True
  return False

def cancel_challenge(username, badge):
  author = reddit.redditor(username)
  challenges = challenges_list(author, badge)
  if len(challenges) > 0:
    challenges[0].mod.flair(text='Removed', css_class='')
    challenges[0].reply('Your challenge has been removed')
    challenges[0].mod.remove()
    return True
  else:
    return False

def get_league_pass(username):
  if username in ['me', 'my', 'your']:
    return 'User is me'
  author = reddit.redditor(username)
  cards = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_text == 'League Pass' and replied(x) and season_start_date < datetime.datetime.utcfromtimestamp(x.created_utc), author.submissions.new(limit=10)))
  if len(cards) == 0:
    return username + ' does not have a registered league pass'
  else:
    return cards[0].url

def get_badges(username):
  if username in ['me', 'my', 'your']:
    return 'User is me'
  elif wiki_exists(username):
    return 'https://reddit.com/r/PokeVerseLeague/wiki/s2lps/'+username
  else:
    return 'User does not have a badge sheet'

def time_to_challenge(name):
  author = reddit.redditor(name)
  challenges = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_text in challenge_flairs, author.submissions.new(limit=10)))
  if len(challenges) > 0:
    time_dif = datetime.datetime.utcnow() - datetime.datetime.fromtimestamp(challenges[0].created_utc)
    since_20 = datetime.timedelta(hours=20) - time_dif
    if since_20.days >= 0:
      return name + ' can post a challenge in ' + ':'.join(str(since_20).split(':')[:2])
  return name + ' is ready to post their next challenge!'

def getmention(message):
  return message.mentions[0] if len(message.mentions) > 0 else None

def haspermission(author):
  author = id_to_discorduser(author.id)
  return any(role.hoist for role in author.roles)

def helpfunc(message, args):
  user = getmention(message)
  if user == None:
    user = message.author
  if haspermission(user):
    return (user,(help_message, help_message_mod))
  return (user,(help_message,))

def setfc(message, args):
  if len(message.mentions) > 0:
    msg = "Please do not include user tags in your FC"
  elif len(args) == 0:
    msg = "Please provide a friend code"
  else:
    user = message.author.id
    url = None
    if len(message.attachments) > 0:
      url = message.attachments[0]['url']
    cursor.execute(fc_select_str, (user,))
    result = cursor.fetchone()
    if result == None:
      cursor.execute(fc_insert_pic_str, (user, args, url))
    else:
      cursor.execute(fc_update_pic_str, (args, url, user))
    connection.commit()
    msg = 'Friend code set to ' + args
    return msg

def getfc(message, args):
  user = getmention(message)
  if user == None:
    user = message.author
  userid = discorduser_to_id(user)
  cursor.execute(fc_select_str, (userid,))
  result = cursor.fetchone()
  if result == None:
    msg = id_to_discordname(userid) + " does not have a registered friend code."
  else:
    msg = result[0]
  return msg

def getlp(message, args):
  user = getmention(message)
  if user == None:
    if len(args) == 0:
      user = message.author
      name = discorduser_to_redditname(message.author)
    else:
      name = args
  else:
    name = discorduser_to_redditname(user)
  if name == None:
    msg = no_reddit_message.format(discorduser_to_discordname(user))
  else:
    msg = get_league_pass(name)
  return msg

def getbadge(message, args):
  user = getmention(message)
  if user == None:
    if len(args) == 0:
      user = message.author
      name = discorduser_to_redditname(message.author)
    else:
      name = args
  else:
    name = discorduser_to_redditname(user)
  if name == None:
    msg = no_reddit_message.format(discorduser_to_discordname(user))
  else:
    msg = get_badges(name)
  return msg


def setreddit(message, args):
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
    return msg

def getreddit(message, args):
  user = getmention(message)
  if user == None:

    if len(args) > 0:
      cursor.execute(reddit_select_name_str, (args.lower(),))
      result = cursor.fetchone()
      if result == None:
        msg = 'There is no one on this server with the reddit username ' + args
      else:
        msg = id_to_discordname( result[0] )
      return msg

    user = message.author.id
  else:
    user = user.id
  cursor.execute(reddit_select_str, (user,))
  result = cursor.fetchone()
  if result == None:
    msg = no_reddit_message.format(id_to_discordname(user))
  else:
    msg = result[0]
  return msg

def addtsv(message, args):
  user = message.author.id
  val = args.split(maxsplit=1)
  if len(val) < 2:
    msg = "To assign your tsv, use the command '!addtsv XXXX Game'"
  else:
    tsv = val[0]
    game = val[1]
    if len(tsv) != 4 or not tsv.isdigit():
      msg = "Your tsv must be exactly 4 numbers"
    else:
      cursor.execute(tsv_insert_str, (user, tsv, game))
      connection.commit()
      msg = 'Added ' + tsv + ' for ' + game
  return msg

def deletetsv(message, args):
  user = message.author.id
  if len(args) != 4:
    msg = "The tsv you want to delete must be exactly 4 characters"
  else:
    cursor.execute(tsv_delete_str, (user, args))
    connection.commit()
    msg = 'Deleted ' + args
  return msg

def gettsv(message, args):
  user = message.author.id
  if len(args) == 0:
    cursor.execute(tsv_select_str, (user,))
    results = cursor.fetchall()
    if results == None or len(results) == 0:
      msg = "You don't have any registered tsvs"
    else:
      msg = ''
      for result in results:
        msg += result[0] + ' ' + result[1] + '\n'
  else:
      if len(args) != 4:
        msg = 'The tsv you are searching for must be exactly 4 characters'
      else:
        cursor.execute(tsv_request_str, (args,))
        results = cursor.fetchall()
        if results == None or len(results) == 0:
          msg = "No one has that tsv"
        else:
          msg = ''
          server = message.server
          for result in results:
            member = server.get_member(result[0])
            msg += discorduser_to_discordname(member) + ' has that tsv in the game ' + result[1] + '\n'
  return msg

def dumptsv(message, args):
  cursor.execute(tsv_dump_str)
  results = cursor.fetchall()
  results = list(filter(lambda x: id_to_discordname(x[0]) != None, results))
  results.sort(key=lambda x: x[1])
  dump = ''
  for result in results:
    dump += result[1] + ' ' + result[2] + ' ' + id_to_discordname(result[0]) + '\n'
  post = requests.post("https://hastebin.com/documents", data=dump.encode('utf-8'))
  return "https://hastebin.com/" + post.json()["key"]

def gettime(message, args):
  user = getmention(message)
  if user == None:
    if len(args) == 0:
      user = message.author
      name = discorduser_to_redditname(message.author)
    else:
      name = args
  else:
    name = discorduser_to_redditname(user)
  if name == None:
    msg = no_reddit_message.format(discorduser_to_discordname(user))
  else:
    msg = time_to_challenge(name)
  return msg


def badge(message, args):
  if haspermission(message.author):
    (name, badge) = args.split(maxsplit=1)
    user = getmention(message)
    if user != None:
      name = discorduser_to_redditname(user)
    badge = badge.lower()
    if name == None:
      msg = no_reddit_message.format(discorduser_to_discordname(user))
    elif not wiki_exists(name):
      msg = name + ' does not have a reigstered league pass'
    elif not isbadge(badge):
      msg = badge + ' is not a valid badge'
    elif flair_post(name, badge, 'Victory'):
      add_badge(name, badge)
      msg = 'Assigned badge ' + badge + ' to ' + name
    else:
      msg = name + ' does not have a matching challenge'
  else:
    msg = no_permissions_message
  return msg

def loss(message, args):
  if haspermission(message.author):
    (name, badge) = args.split(maxsplit=1)
    user = getmention(message)
    if user != None:
      name = discorduser_to_redditname(user)
    badge = badge.lower()
    if name == None:
      msg = no_reddit_message.format(discorduser_to_discordname(user))
    elif not wiki_exists(name):
      msg = name + ' does not have a reigstered league pass'
    elif not isbadge(badge):
      msg = badge + ' is not a valid badge'
    elif flair_post(name, badge, 'Defeat'):
      msg = 'Assigned loss to ' + name
    else:
      msg = name + ' does not have a matching challenge'
  else:
    msg = no_permissions_message
  return msg

def retry(message, args):
  if haspermission(message.author):
    user = getmention(message)
    name = args
    if user != None:
      name = discorduser_to_redditname(user)
    if name == None:
      msg = no_reddit_message.format(discorduser_to_discordname(user))
    elif approve_rematch(name):
      msg = 'Retry approved for ' + name
    else:
      msg = name + ' does not have a pending retry'
  else:
    msg = no_permissions_message
  return msg

def cancel(message, args):
  if haspermission(message.author):
    (name, badge) = args.split(maxsplit=1)
    user = getmention(message)
    if user != None:
      name = discorduser_to_redditname(user)
    badge = badge.lower()
    if name == None:
      msg = no_reddit_message.format(discorduser_to_discordname(user))
    elif not isbadge(badge):
      msg = badge + ' is not a valid badge'
    elif cancel_challenge(name, badge):
      msg = 'Canceled challenge for ' + name
    else:
      msg = name + ' does not have an open challenge'
  else:
    msg = no_permissions_message
  return msg

def message(message, args):
  if haspermission(message.author):
    (userid, messagetext) = args.split(maxsplit=1)
    if userid == 'Emoswo2h':
      user = client.get_channel('372042060913442820')
    else:
      user = id_to_discorduser(userid)
    if user == None or messagetext == None or len(messagetext) == 0:
      msg = ('Usage: !message USER-ID-HERE message text goes here', message.channel)
    else:
      msg = (messagetext, user)
  else:
    msg = (no_permissions_message, message.channel)
  return msg

def custom(message, args):
  if haspermission(message.author):
    user = getmention(message)
    if user == None:
      user = message.author
    userid = discorduser_to_id(user)
    cursor.execute(fc_select_str, (userid,))
    result = cursor.fetchone()
    if result == None:
      msg = id_to_discordname(userid) + " does not have a registered friend code."
    else:
      print(result)
      msg='Done'
  else:
    msg = no_permissions_message
  return msg

async def leaks(message):
  roles = message.server.roles
  for role in roles:
    if role.name=='Leaks':
      leak_role=role

  if any([role == leak_role for role in message.author.roles]):
    await client.remove_roles(message.author, leak_role)
  else:
    await client.add_roles(message.author, leak_role)

def swearlist(message, args):
  cursor.execute(swear_dump_str)
  results = cursor.fetchall()
  results = list(filter(lambda x: id_to_discordname(x[0]) != None, results))
  dump = ''
  for result in results:
    dump += str(result[1]) + ' - ' + id_to_discordname(result[0]) + '\n'
  return dump

def est(message, args):
  return datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-4))).strftime('%I:%M%p')

async def wipe(message):
  redditn = discorduser_to_redditname(message.author)
  if redditn in singles_leaders:
    ms=[]
    async for m in client.logs_from(client.get_channel(singles_channels[singles_leaders.index(redditn)])):
      if not m.pinned:
        ms.append(m)
    await client.delete_messages(ms)

@client.event
async def on_member_remove(member):
  await client.send_message(client.get_channel('378725359014641667'), discorduser_to_discordname(member) + ' has left')

@client.event
async def on_ready():
  print('Logged in as')
  print(client.user.name)
  print(client.user.id)
  print(datetime.datetime.now())
  print('------')
  await client.change_presence(game=discord.Game(name='!help'))


commands = {
    'help': helpfunc,
    'setfc': setfc,
    'getfc': getfc,
    'getreddit': getreddit,
    'setreddit': setreddit,
    'getlp': getlp,
    'getbadge': getbadge,
    'getbadges': getbadge,
    'gettsv': gettsv,
    'getsv': gettsv,
    'addtsv': addtsv,
    'dumptsv': dumptsv,
    'deletetsv': deletetsv,
    'badge': badge,
    'loss': loss,
    'retry': retry,
    'cancel': cancel,
    'pyramid': pyramid,
    'gettime': gettime,
    'getime': gettime,
    'custom': custom,
    'message': message,
    'swearlist': swearlist,
    'est': est
    }
swear = 40

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if swear_jar(message) and message.author.id != '103049236525887488':
    global swear
    swear = (swear + 1)%50
    if swear==0:
      await client.send_message(message.channel, 'You triggered the swear jar '+message.author.mention+'!')
      cursor.execute(swear_select_str, (message.author.id,))
      result = cursor.fetchone()
      if result == None:
        cursor.execute(swear_insert_str, (message.author.id,))
      else:
        cursor.execute(swear_update_str, (message.author.id,))
      connection.commit()

  m = re.search(tag_err_reg, message.content)
  if len(message.mentions) == 0 and m != None:
    print(m.group(1))
    print(m.group(2))
    user = discord.utils.get(message.server.members, name=m.group(1), discriminator=m.group(2))
    if user != None:
      text = re.sub(tag_err_reg, user.mention, message.content)
      print(text)
      await client.send_message(message.channel, text)
  else:
    text = message.content

  if len(text) > 0 and text[0] == '!':
    args = text[1:].split(maxsplit=1)
    if args[0].lower() == 'leaks':
      await leaks(message)
      return
    if args[0].lower() == 'wipe':
      await wipe(message)
      return

    msg = commands[args[0].lower()](message, args[1] if len(args) > 1 else '')
    if args[0].lower() == 'help':
      for m in msg[1]:
        await client.send_message(msg[0], m)
    elif args[0].lower() == 'message':
      await client.send_message(msg[1], msg[0])
      await client.send_message(message.channel, 'Sent to ' + discorduser_to_discordname(msg[1]))
    else:
      await client.send_message(message.channel, msg)

showdown_name_reg=r'\|queryresponse\|userdetails\|{"userid":"(.*?)"'
showdown_battle_reg='(battle-.*?)":'
showdown_inbattle_reg=r'>(battle-.*?)\n(.*)'
showdown_win_reg=r'>(battle-.*?-\d*).*\|win\|'
query = '|/cmd userdetails %s'
opps = ['roprcrusader', 'ghostwafers',  'dshmucker', 'princemiasma', 'tort']

async def send(websocket):
  await client.wait_until_ready()
  while not client.is_closed:
    for opp in opps:
      new_q = query % opp
      await websocket.send(new_q)
    await asyncio.sleep(120)

async def recieve(websocket):
  await client.wait_until_ready()
  current_battles = []
  while not client.is_closed:
    response = await websocket.recv()
    #Case 1: Recieved userdetails response
    name = re.search(showdown_name_reg, response)
    if name != None:
      name = name.group(1)
      matches = re.findall(showdown_battle_reg, response)
      for match in matches:
        entry = [name, match, '']
        if ('custom' in match or 'gen7ou' in match or 'anything' in match) and  all([e[1]!=match for e in current_battles]):
          if len(current_battles) > 50:
            current_battles.pop()
          current_battles.append(entry)
          await websocket.send('|/join ' + match)
          await sendH2(name + ': https://play.pokemonshowdown.com/' + match)
    #Case 2: Recieve in-battle message
    battle = re.search(showdown_inbattle_reg, response, re.DOTALL)
    if battle != None:
      for i, _ in enumerate(current_battles):
        if current_battles[i][1]==battle.group(1):
          current_battles[i][2] += battle.group(2)
    #Case 3: Recieved battle end response
    battle = re.search(showdown_win_reg, response, re.DOTALL)
    if battle != None:
      battle = battle.group(1)
      remInd = -1
      for i, _ in enumerate(current_battles):
        if current_battles[i][1]==battle:
          remInd=i
          writebattle(current_battles[i])
          await websocket.send('|/leave ' + battle)

async def sendH2(message):
  i=0
  h2=id_to_discorduser('242558859300831232')
  while i+1000<len(message):
    await client.send_message(h2, message[i:i+1000])
    i+=1000
  await client.send_message(h2, message[i:])

def writebattle(entry):
  fo = open('/root/verse-bot/battles/' + entry[0] + ':' + entry[1], 'w')
  fo.write(entry[2])
  fo.close()

async def connect(future):
  websocket = await websockets.connect('ws://sim.smogon.com:8000/showdown/websocket')
  future.set_result(websocket)

future = asyncio.Future()
asyncio.ensure_future(connect(future))
client.loop.run_until_complete(future)
websocket = future.result()
client.loop.create_task(send(websocket))
client.loop.create_task(recieve(websocket))
client.run('MzY4MjA3OTA4MjU4NzA5NTA4.DVEzAw.5EcJ2rBPRcRi6RJeKCg96cdLUX0')
