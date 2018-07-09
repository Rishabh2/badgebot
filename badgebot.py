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
from commands.time import *
from commands.coin import *

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
  resetModules()
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
'commands.time',
'commands.coin',
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
  'getchallenge': getchallenge,
  'time': time,
  'coin': coin,
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

  if 'pikasnap' in text.lower():
    await client.send_message(message.channel, embed=make_embed(None, 'https://cdn.discordapp.com/attachments/365313213673373706/465698751177031690/pikasnapmk4.gif', None))

  if len(text) > 0 and text[0] == '!':
    args = text[1:].split(maxsplit=1)
    if args[0].lower() in commands:
      await commands[args[0].lower()](message, args[1] if len(args) > 1 else '')
client.run(passwords.discordpass)
