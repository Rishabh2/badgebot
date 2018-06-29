from header import *
from commands.addtsv import *
from commands.badge import *
from commands.cancel import *
from commands.custom import *
from commands.deletetsv import *
from commands.dumptsv import *
from commands.est import *
from commands.getbadge import *
from commands.getfc import *
from commands.getlp import *
from commands.getreddit import *
from commands.gettime import *
from commands.gettsv import *
from commands.help import *
from commands.leaks import *
from commands.loss import *
from commands.message import *
from commands.retry import *
from commands.setfc import *
from commands.setreddit import *
from commands.swearlist import *
from commands.wipe import *
from commands.getchallenge import *


def resetModules():
  for mod in modules:
    importlib.reload(sys.modules[mod])
    commands[mod[mod.index('.')+1:]] = getattr(sys.modules[mod], mod[mod.index('.')+1:])


async def reset(message, args):
  if haspermission(message.author.id) and args == passwords.modpass:
    resetModules()
    await client.send_message(message.channel, 'Reset')
  else:
    await client.send_message(message.channel, no_permissions_message)

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

modules = [
'commands.addtsv',
'commands.badge',
'commands.cancel',
'commands.custom',
'commands.deletetsv',
'commands.dumptsv',
'commands.est',
'commands.getbadge',
'commands.getfc',
'commands.getlp',
'commands.getreddit',
'commands.gettime',
'commands.gettsv',
'commands.help',
'commands.leaks',
'commands.loss',
'commands.message',
'commands.retry',
'commands.setfc',
'commands.setreddit',
'commands.swearlist',
'commands.wipe',
]

commands = {
  'help': help,
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
  'gettime': gettime,
  'getime': gettime,
  'custom': custom,
  'message': message,
  'swearlist': swearlist,
  'est': est,
  'wipe': wipe,
  'reset': reset,
  'leaks': leaks,
  'getchallenge': getchallenge
  }


swear=40

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if swear_jar(message):
    global swear
    swear = (swear + 1)%50
    if swear == 0:
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
    user = discord.utils.get(message.server.members, name=m.group(1),discriminator=m.group(2))
    if user != None:
      text = re.sub(tag_err_reg, user.mention, message.content)
      await client.send_message(message.channel, text)
  else:
    text = message.content

  if len(text) > 0 and text[0] == '!':
    args = text[1:].split(maxsplit=1)
    if args[0].lower() in commands:
      await commands[args[0].lower()](message, args[1] if len(args) > 1 else '')

'''
showdown_name_reg=r'\|queryresponse\|userdetails\|{"userid":"(.*?)"'
showdown_battle_reg='(battle-.*?)":'
showdown_inbattle_reg=r'>(battle-.*?)\n(.*)'
showdown_win_reg=r'>(battle-.*?-\d*).*\|win\|'
query = '|/cmd userdetails %s'
opps = ['h2owsome', 'roprcrusader', 'ghostwafers',  'ballistiic', 'princemiasma']

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
'''
client.run(passwords.discordpass)
