from header import *
from commands.addtsv import *
from commands.badge import *
from commands.cancel import *
from commands.calculate import *
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
from commands.forcewipe import *
from commands.info import *
from commands.draft import *
from commands.art import *
from commands.setlp import *
from commands.challenge import *
from commands.sideboard import *
from commands.remindme import *

def resetModules():
  for mod in modules:
    importlib.reload(sys.modules[mod])
    commands[mod[mod.index('.')+1:]] = getattr(sys.modules[mod], mod[mod.index('.')+1:])


async def reset(message, args):
  if message.author.id == '242558859300831232':
    resetModules()
    await client.send_message(message.channel, 'Reset')
  else:
    await client.send_message(message.channel, no_permissions_message)

@client.event
async def on_member_remove(member):
  if member.server.id == '372042060913442818':
    await client.send_message(client.get_channel('378725359014641667'), discorduser_to_discordname(member) + ' has left')

@client.event
async def on_ready():
  print('Logged in as')
  print(client.user.name)
  print(client.user.id)
  print(datetime.datetime.now())
  print('------')
  resetModules()
  await client.change_presence(game=discord.Game(name='!help | Contact H2owsome if there is a problem'))


modules = [
'commands.addtsv',
'commands.badge',
'commands.cancel',
'commands.calculate',
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
'commands.forcewipe',
'commands.info',
'commands.draft',
'commands.art',
'commands.setlp',
'commands.challenge',
'commands.sideboard',
'commands.remindme'
]

commands = {
  'help': help,
  'commands': help,
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
  'win': badge,
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
  'coins': coin,
  'calculate': calculate,
  'forcewipe': forcewipe,
  'info': info,
  'draft':draft,
  'art':art,
  'setlp':setlp,
  'challenge':challenge,
  'sideboard':sideboard,
  'remindme':remindme
  }

swear=40

async def gcreate(message):
  gcreator = message.author.id
  print(gcreator)
  resp = await client.wait_for_message(timeout=600, check=lambda x: x.author.id == giveawaybot and len(x.embeds) > 0)
  print(resp)
  if resp != None:
    await client.pin_message(resp)
    cursor.execute('INSERT INTO giveaways (id, gid) values (?,?)', (gcreator, resp.id))
    connection.commit()



@client.event
async def on_message(message):
  if message.author.id == giveawaybot and 'Congratulations' in message.content:
    await asyncio.sleep(1)
    pins = await client.pins_from(message.channel)
    for p in pins:
      if 'ENDED' in p.content:
        cursor.execute('SELECT * from giveaways where gid=?', (p.id,))
        result = cursor.fetchone()
        cursor.execute('DELETE FROM giveaways where gid=?', (p.id,))
        connection.commit()
        if result != None:
          await client.send_message(message.channel, 'From <@{}>'.format(result[0]))
        await client.unpin_message(p)
  if message.author.bot:
    return

  try:
    s = message.server.id
  except:
    s = None

  if s=='372042060913442818' and swear_jar(message):
    global swear
    swear = (swear + 1)%50
    if swear == 0:

      roles = message.server.roles
      for role in roles:
        if role.name=='Giveaways':
          give_role=role
      if not any([role == give_role for role in message.author.roles]):
        await client.add_roles(message.author, give_role)

      await client.send_message(message.channel, 'You triggered the swear jar '+message.author.mention+'!')
      cursor.execute(swear_select_str, (message.author.id,))
      result = cursor.fetchone()
      if result == None: # No info
        cursor.execute(swear_insert_str, (message.author.id,))
      elif result[0] == None: # No swears
        cursor.execute(swear_begin_str, (message.author.id,))
      else: # Swears
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

  if text.lower().startswith('g!create') or text.lower().startswith('!gcreate'):
    await gcreate(message)

  if len(text) > 0 and text[0] == '!':
    args = text[1:].split(maxsplit=1)
    if args[0].lower() in commands:
      await commands[args[0].lower()](message, args[1] if len(args) > 1 else '')

os.chdir('/root/badgebot/')
cursor.execute('SELECT * FROM reminders')
result = cursor.fetchall()
for r in result:
  client.loop.create_task(load_reminder(*r))
client.run(passwords.discordpass)
