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
from commands.gettime import *
from commands.gettsv import *
from commands.help import *
from commands.loss import *
from commands.message import *
from commands.setfc import *
from commands.swearlist import *
from commands.wipe import *
from commands.coin import *
from commands.forcewipe import *
from commands.info import *
from commands.draft import *
from commands.spooky import *
from commands.setlp import *
from commands.challenge import *
from commands.sideboard import *
from commands.remindme import *
from commands.propose import *
from commands.setbday import *
from commands.getbday import *
from commands.bdaylist import *
from commands.settime import *
from commands.swap import *
from commands.accept import *
from commands.addteam import *
from commands.challengetime import *
from commands.mute import *

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
  await client.send_message(client.get_channel('384790941564796930'),
      '<@242558859300831232>\nRestarted at ' + datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=(-8)))).strftime('%I:%M%p'))

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
'commands.gettime',
'commands.gettsv',
'commands.help',
'commands.loss',
'commands.message',
'commands.setfc',
'commands.swearlist',
'commands.wipe',
'commands.coin',
'commands.forcewipe',
'commands.info',
'commands.draft',
'commands.spooky',
'commands.setlp',
'commands.challenge',
'commands.sideboard',
'commands.remindme',
'commands.propose',
'commands.getbday',
'commands.setbday',
'commands.bdaylist',
'commands.settime',
'commands.swap',
'commands.accept',
'commands.addteam',
'commands.challengetime',
'commands.mute',
]

commands = {
  'help': help,
  'commands': help,
  'setfc': setfc,
  'getfc': getfc,
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
  'cancel': cancel,
  'gettime': gettime,
  'getime': gettime,
  'custom': custom,
  'message': message,
  'swearlist': swearlist,
  'est': est,
  'wipe': wipe,
  'reset': reset,
  'coin': coin,
  'coins': coin,
  'calculate': calculate,
  'forcewipe': forcewipe,
  'info': info,
  'draft':draft,
  'spooky':spooky,
  'setlp':setlp,
  'challenge':challenge,
  'sideboard':sideboard,
  'remindme':remindme,
  'propose':propose,
  'getbday':getbday,
  'setbday':setbday,
  'bdaylist':bdaylist,
  'settime':settime,
  'swap':swap,
  'accept':accept,
  'addteam':addteam,
  'challengetime':challengetime,
  'mute':mute,
  }


async def gcreate(message):
  if message.server.id == '372042060913442818':
    gcreator = message.author.id
    resp = await client.wait_for_message(timeout=600, channel=client.get_channel('480933325759053854'),check=lambda x: x.author.id == giveawaybot and '**G' in x.content)
    if resp != None:
      await client.pin_message(resp)
      cursor.execute('INSERT INTO giveaways (id, gid) values (?,?)', (gcreator, resp.id))
      connection.commit()



@client.event
async def on_message(message):
  try:
    if message.author.id == '245963462952484864' and 'butthead' in message.content.lower():
      await client.send_message(message.channel, 'buttheat*')
    if message.author.id == giveawaybot and 'Congratulations' in message.content:
      m = re.search(r'the \*\*(.*)\*\*', message.content)
      prize = m.group(1)
      pins = await client.pins_from(message.channel)
      for p in pins:
        if p.embeds != None and len(p.embeds) > 0 and prize in p.embeds[0]['author']['name']:
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
        await client.send_message(message.channel, 'You triggered the swear jar '+message.author.mention+'! Get yourself to #bot-spam and start a giveaway using the command !gcreate. you filthy mouthed trainer...\n<:Dragonite:387809726227939328> frowns upon you.')
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
    if text.lower().startswith('!bestpokemon'):
      await client.send_message(message.channel, embed=discord.Embed(color=discord.Color(0xbc614e)).set_image(url=sprite_url.format('pyukumuku')))
    if text.lower().startswith('!cutestpokemon'):
      await client.send_message(message.channel, embed=discord.Embed(color=discord.Color(0xbc614e)).set_image(url=sprite_url.format('ralts')))
    if text.lower().startswith('!leek'):
      await client.send_message(message.channel, embed=discord.Embed(color=discord.Color(0xbc614e)).set_image(url=sprite_url.format('farfetchd')))
    if text.lower().startswith('!wiki'):
      await client.send_message(message.channel, wiki_url)
    if text.lower().startswith('!hitormiss') and message.channel.id in ['481721487569453076', '547137198328250369']: # Allowed spam channels
      await client.send_message(message.channel, ':head_bandage:Hit :punch: or miss:flushed: I guess :thinking:they :point_right:never :x: miss, huh :confused::confused:? You :raised_hands:got a boyfriend:heart_eyes:, I bet :slot_machine::no_mouth:he :fearful:doesn\'t :thumbsdown:kiss :kissing_heart::kissing_heart: ya mwah:sparkling_heart: :heart_eyes_cat:He gon\' find :mag::mag: another girl :baby: and he :open_mouth:won\'t:triumph: miss:ok_hand: ya:scream_cat: He :drooling_face:gon\' :astonished:skrrt and hit :punch::punch: the dab:sunglasses: like :smile::smile: Wiz :cowboy:Khalifa:money_mouth:')
    if any([m.id=='213008672610189312' for m in message.mentions]):
      await client.send_message(message.channel, 'Ponged!')
    if any([m.id=='227824927854559242' for m in message.mentions]):
      await client.send_message(message.channel, 'Your goddess will arrive shortly.')

    for command, rolename in command_roles.items():
      if text.lower().startswith('!'+command):
        roles = message.server.roles
        for role in roles:
          if role.name==rolename:
            key_role=role

        if any([role == key_role for role in message.author.roles]):
          await client.remove_roles(message.author, key_role)
        else:
          await client.add_roles(message.author, key_role)

    if len(text) > 0 and text[0] == '!':
      args = text[1:].split(maxsplit=1)
      if len(args) > 0 and args[0].lower() in commands:
        await commands[args[0].lower()](message, args[1] if len(args) > 1 else '')
  except Exception as e:
    errormsg = '\n'.join(['<@242558859300831232>',
      discorduser_to_discordname(message.author),
      str(args),
      '```\n'+traceback.format_exc()+'\n```',
      message.channel.name if message.channel.is_private else message.channel.mention])
    await client.send_message(client.get_channel('384790941564796930'), errormsg)
    raise e

os.chdir('/root/badgebot/')
cursor.execute('SELECT * FROM reminders')
result = cursor.fetchall()
for r in result:
  client.loop.create_task(load_reminder(*r))
client.run(passwords.discordpass)
