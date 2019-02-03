import sqlite3
import websockets
import praw
import random
import re
import asyncio
import requests
import datetime
import discord
import sys
import time
import importlib
import logging
import os
import pickle
from PIL import Image
import subprocess
from io import BytesIO
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client as gclient, tools
import passwords
from profanityfilter import ProfanityFilter
import traceback


fc_insert_str = 'INSERT INTO userinfo (id, fc, url) VALUES (?, ?, ?);'

fc_select_str = 'SELECT fc, url FROM userinfo WHERE id=?;'

fc_update_str = 'UPDATE userinfo SET fc=?, url=? WHERE id=?;'

fc_delete_str = 'DELETE FROM userinfo WHERE id=?;'


tsv_insert_str = 'INSERT INTO tsv (id, tsv, game) VALUES (?, ?, ?);'

tsv_request_str = 'SELECT id, game FROM tsv WHERE tsv=?;'

tsv_delete_str = 'DELETE FROM tsv WHERE id=? AND tsv=?;'

tsv_select_str = 'SELECT tsv, game FROM tsv WHERE id=?;'

tsv_dump_str = 'SELECT * FROM tsv'


swear_insert_str = 'INSERT INTO userinfo (id,swears) VALUES (?, 1);'

swear_select_str = 'SELECT swears FROM userinfo WHERE id=?;'

swear_update_str = 'UPDATE userinfo SET swears=swears+1 WHERE id=?;'

swear_begin_str = 'UPDATE userinfo SET swears=1 WHERE id=?;'

swear_dump_str = 'SELECT id, swears from userinfo WHERE swears>? ORDER BY swears DESC;'


coins_insert_str = 'INSERT INTO userinfo (id, coins) VALUES (?, ?);'

coins_select_str = 'SELECT coins FROM userinfo WHERE id=?;'

coins_update_str = 'UPDATE userinfo SET coins=? WHERE id=?;'

coins_dump_str = 'SELECT id, coins from userinfo WHERE coins>0 ORDER BY coins DESC;'


info_dump_str = 'SELECT * from userinfo WHERE id=?;'


draft_select_str = 'SELECT conference, team FROM draft WHERE id=?;'

draft_insert_str = 'INSERT INTO draft (id, conference, team) VALUES (?,?,?);'


challenge_table = 's3challenge'

open_challenge_badge_select_str = 'SELECT * FROM {} WHERE id=? AND badge=? AND status="O"'.format(challenge_table)

open_challenge_select_str = 'SELECT * FROM {} WHERE id=? and status="O"'.format(challenge_table)

recent_challenge_select_str = 'SELECT opentime FROM {} WHERE id=? AND status NOT LIKE "%D" AND status != "C" ORDER BY opentime DESC'.format(challenge_table)

challenge_str = 'INSERT INTO {} (id, opentime, badge, status) VALUES (?,?,?,"O")'.format(challenge_table)

challenge_override_str = 'INSERT INTO {} (id, badge, opentime, accepttime, status) VALUES (?,?,?,?,"O")'.format(challenge_table)

challenge_win_str = 'UPDATE {} SET status="W", closetime=? WHERE id=? AND badge=? AND status="O"'.format(challenge_table)

challenge_loss_str = 'UPDATE {} SET status="L", closetime=? WHERE id=? AND badge=? AND status="O"'.format(challenge_table)

challenge_cancel_str = 'UPDATE {} SET status="C", closetime=? WHERE id=? AND status="O"'.format(challenge_table)

challenge_accept_str = 'UPDATE {} SET accepttime=? WHERE id=? AND badge=? AND status="O"'.format(challenge_table)

badge_select_str = 'SELECT badge FROM {} WHERE id=? AND status="W"'.format(challenge_table)

badge_reset_str = 'UPDATE {} SET status=status+"D" WHERE id=?'.format(challenge_table)


lp_table = 's3lp'

lp_select_str = 'SELECT * FROM {} WHERE id=?'.format(lp_table)

lp_insert_str = 'INSERT INTO {} (id, mons, salt) VALUES (?,?,?)'.format(lp_table)

lp_delete_str = 'DELETE FROM {} WHERE id=?'.format(lp_table)

lp_update_str = 'UPDATE {} SET mons=?, salt=? WHERE id=?'.format(lp_table)


bday_dump_str = 'SELECT bdaymonth, bdayday, id FROM userinfo WHERE bdaymonth IS NOT NULL ORDER BY bdaymonth, bdayday ASC'

bday_select_str = 'SELECT bdayday, bdaymonth FROM userinfo WHERE id=?'

bday_insert_str = 'INSERT INTO userinfo (id, bdaymonth, bdayday) VALUES (?,?,?)'

bday_update_str = 'UPDATE userinfo SET bdaymonth=?, bdayday=? WHERE id=?'

time_select_str = 'SELECT offset FROM time WHERE id=?'

time_insert_str = 'INSERT INTO time (id, offset) VALUES (?,?)'

time_update_str = 'UPDATE time SET offset=? WHERE id=?'

months = 'JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'.split()
days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

team_insert_str = 'INSERT INTO teams (id, team, timestamp) VALUES (?, ?, ?)'


arcade_channel = '463817264752492574'

gym_types = ['flying', 'poison', 'dragon', 'fairy', 'steel', 'dark', 'ground', 'psychic']
islands = ['melemele', 'poni', 'ulaula', 'akala', 'moone', 'sunne']
#Management, Gym Leader, Kahunas, Discipline
permission_roles = ['384724202613112843', '372559774350573570', '496397807494627338', '507833815696146434']
#Management and Discipline
mute_roles = ['384724202613112843', '507833815696146434']

badge_ids = {
    'grass':'<a:grasssingles:482073772535578655>',
    'normal':'<a:normalsingles:482073773730824192>',
    'fairy':'<a:fairysingles:482067974119882752>',
    'ice':'<a:icesingles:482067977714401302>',
    'ground':'<a:groundsingles:482067974027739137>',
    'poison':'<a:poisonsingles:482070458552942604>',
    'rock':'<a:rocksingles:482071206678495252>',
    'flying':'<a:flyingsingles:506409251326132305>',
    'dark':'<a:darksingles:506408993758117898>',
    'dragon':'<a:dragonsingles:482063698127749141>',
    'psychic':'<a:psychicsingles:506409264143794176>',
    'steel':'<a:steelsingles:482070459421294632>',
    'ulaula':'<a:ulaula:506385368002854912>',
    'poni':'<a:poni:506381370260455434>',
    'melemele':'<a:melemele:506385369760268289>',
    'akala':'<a:akala:506387179304648728>',
    'sunne':'<a:sunne:506387413350744064>',
    'moone':'<a:moone:506387413388754945>',
    'e4champ':'<a:bugsingles:506408913428676609><a:fightingsingles:506409118194597889><a:watersingles:506409275245985793><a:firesingles:506409126759497728>'
    }

challenge_time_limit = 19*60*60

tag_err_reg = '@(.*)#(\d*)'

badgebot_color = discord.Color(0x85bff8)
badgebot_icon = 'https://images-ext-2.discordapp.net/external/8Z0dL7YbZmXqgEYPI06J7m4Ht1jpRb9PxwvlAIy66mU/%3Fsize%3D128/https/cdn.discordapp.com/avatars/368207908258709508/65eec358e20f26f99b3ecfcfd5d1cb5d.png'

help_about = discord.Embed(title='About You', color=badgebot_color, description='Set your Friend Code and IGN, and other helpful information.')
help_about.set_footer(text="Please contact H2owsome with any questions.")
help_about.set_thumbnail(url=badgebot_icon)
help_about.add_field(name='!setfc', value='Anything you put directly after the command will be recorded in badgebot as-is, including line breaks and any text formatting (italics, bold, etc) If you’d like to add a picture, upload the image to Discord with your !setfc message.')
help_about.add_field(name='!settime', value='`!settime #` Replace the # with your personal UTC offset (Example: `!settime -7`) Be sure to update it when Daylight savings time rolls around')
help_about.add_field(name='!setbday', value='`!setbday ## month` You must use this format for this command')

help_info = discord.Embed(title='Getting info about people', color=badgebot_color, description='These commands pull up the saved information of yourself/others')
help_info.set_footer(text='Please contact H2owsome with any questions.')
help_info.set_thumbnail(url=badgebot_icon)
help_info.add_field(name='!getfc', value='`!getfc @someone` to pull up their FC')
help_info.add_field(name='!getlp', value='`!getlp @someone` to pull up their LP')
help_info.add_field(name='!getbadges', value='`!getbadges @someone` to pull up their badges')
help_info.add_field(name='!gettime', value='`!gettime @someone` to pull up their time')
help_info.add_field(name='!getbday', value='`!getbday @someone` to pull up their bday')
help_info.add_field(name='!info', value='`!info @someone` to pull up their full info')

help_lp = discord.Embed(title='Your League Pass', color=badgebot_color, description='Set up a League Pass to challenge to Gyms and other attractions')
help_lp.set_footer(text='Please contact H2owsome with any questions.')
help_lp.set_thumbnail(url=badgebot_icon)
help_lp.add_field(name='!setlp', value='Use this command in #bot-spam to being setting up your League Pass')
help_lp.add_field(name='!sideboard', value='`!sideboard Pokemon` to add `Pokemon` to your League Pass. (Replace `Pokemon` with the Pokemon you want)')
help_lp.add_field(name='!swap', value='`!swap PokemonA/PokemonB` to swap `PokemonA` and `PokemonB` on your League Pass')

help_gym = discord.Embed(title='Challenge the Gyms', color=badgebot_color, description='All the info you need about challenging gyms')
help_gym.set_footer(text='Please contact H2owsome with any questions.')
help_gym.set_thumbnail(url=badgebot_icon)
help_gym.add_field(name='!challenge', value='`!challenge gymname` will submit a challenge and notify the gym leader. Examples include `!challenge fairy` or `!challenge melemele`\nThe name of the gym you are challenging will match the name of the corresponding channel\nJust use `!challenge` to check if you have an open challenge')
help_gym.add_field(name='!cancel', value='Cancel an open challenge if you want to challenge someone else. A cancelled challenge will be ignored by the timer.')
help_gym.add_field(name='!challengetime', value='Tells you how much time you have remaining until you can challenge again. There is a 20 hour limit between challenges')

help_tsv = discord.Embed(title='Your TSVs', color=badgebot_color, description='Register your TSVs and find matched for your eggs')
help_tsv.set_footer(text='Please contact H2owsome with any questions.')
help_tsv.set_thumbnail(url=badgebot_icon)
help_tsv.add_field(name='!addtsv', value='`!addtsv #### Game Name` will add to your saved TSVs. `Game Name` can be anything that will identify the game')
help_tsv.add_field(name='!gettsv', value='`!gettsv @someone` to pull up their TSVs\n`!gettsv ####` to see if anyone has a matching TSV')
help_tsv.add_field(name='!deletetsv', value='`!deletetsv ####` to delete your saved TSV with value ####')
help_tsv.add_field(name='!dumptsv', value='Generates a text dump of every saved TSV')

help_misc = discord.Embed(title='Miscellaneous Commands', color=badgebot_color, description='Miscellaneous Commands')
help_misc.set_footer(text='Please contact H2owsome with any questions.')
help_misc.set_thumbnail(url=badgebot_icon)
help_misc.add_field(name='!coin', value='`!coin @someone` to see how many PVL coins someone has')
help_misc.add_field(name='!remindme', value='Set up a reminder that badgebot will ping you about')
help_misc.add_field(name='!gcreate', value='Start up a giveaway! (Please use command only in #bot-spam, and host the giveaway in #giveaways)')
help_misc.add_field(name='!swearlist', value='`!swearlist @someone` to see how many times they have triggered the swear jar')
help_misc.add_field(name='!bdaylist', value='`!bdaylist` to see some upcoming birthdays')
help_misc.add_field(name='!calculate', value='A helpful calculator if you need to math on discord')
help_misc.add_field(name='!leaks', value='Use `!leaks` to toggle access to the secret #leaks-and-spoilers channel')
help_misc.add_field(name='!breed', value='Use `!breed` to toggle the Breed Helper role')
help_misc.add_field(name='!leaks', value='Use `!smash` to toggle the Smasher role')

help_embeds = [help_about, help_info, help_lp, help_gym, help_tsv, help_misc]

no_reddit_message = "{} does not have a registered reddit username."

no_lp_message = "{} does not have a registered league pass"

invalid_badge_message = "{} is not a valid badge"

no_permissions_message = "You do not have permission to use that command"

singles_embed = discord.Embed(title='Congratulations Challenger!',
    description='''You've beaten the 8 singles GLs and advanced to the E4! To celebrate your accomplishment, you may choose any penta-perfect breeject you would like OR  a trophy shiny from [here](https://pokemon-trading-spreadsheet.tumblr.com/?1P2GfP-WjGFcT3KjVCdevajmuclGEHIqU-aHrzc6vfb0#4) or [here](https://pokemon-trading-spreadsheet.tumblr.com/?18aoKlyHek3DM9b1ZR1InCF5foEZ28sYR6sOgyv4W4WM#3). Contact @breeders on #comittee-contact and
      they'll get you your poke as soon as possible!

      Good luck on your E4 challenge!

      - PVL''')

singles_e4_embed=discord.Embed(title='Congratulations Challenger!',
    description='''You've beaten the singles E4! To celebrate your accomplishment, you may choose **one** of the following:

     any BR pokemon available [here](https://pokemon-trading-spreadsheet.tumblr.com/?18aoKlyHek3DM9b1ZR1InCF5foEZ28sYR6sOgyv4W4WM#2) or [here](https://pokemon-trading-spreadsheet.tumblr.com/?1P2GfP-WjGFcT3KjVCdevajmuclGEHIqU-aHrzc6vfb0#6)

     a comp/semi-comp shiny [here](https://pokemon-trading-spreadsheet.tumblr.com/?18aoKlyHek3DM9b1ZR1InCF5foEZ28sYR6sOgyv4W4WM#4) or [here](https://pokemon-trading-spreadsheet.tumblr.com/?1P2GfP-WjGFcT3KjVCdevajmuclGEHIqU-aHrzc6vfb0#5)

     Contact @breeders on #comittee-contact and they'll get you your poke as soon as possible!

     Good luck on your E4 challenge!

     - PVL''')

ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

with open('/root/badgebot/monlist', 'rb') as fp:
  pokemon_list = pickle.load(fp)

ubers = ['Gengar', 'Kangaskhan', 'Blaziken', 'Salamence', 'Metagross', 'Lucario', 'Aegislash', 'Wobuffet', 'Wynaut', 'Gothita', 'Gothorita', 'Gothitelle', 'Diglett', 'Dugtrio', 'Trapinch', 'Kecleon', 'Froakie', 'Frogadier', 'Greninja']

wiki_url = 'https://www.reddit.com/r/PokeVerseLeague/wiki/index'

sprite_url = 'https://raw.githubusercontent.com/msikma/pokesprite/master/icons/pokemon/regular/{}.png'
roster_url = 'https://raw.githubusercontent.com/Rishabh2/badgebot/master/rosters/{}.png'

connection = sqlite3.connect("/root/badgebot/userinfo.db")
cursor = connection.cursor()

reddit = praw.Reddit(user_agent='PokeVerseLeagueBot v0.1',
                     client_id=passwords.client_id,
                     client_secret=passwords.client_secret,
                     username='BananaHammerBot',
                     password=passwords.redditpass)

subreddit = reddit.subreddit('PokeVerseLeague')

client = discord.Client()


time_mult = {'s':1, 'm':60, 'h':3600, 'd':86400}

pf = ProfanityFilter(extra_censor_list=['twat', 'bellend', 'bloody', 'bugger'])
words = pf.get_profane_words()
words.remove('gay')
words.remove('gaybor')
words.remove('gayboy')
words.remove('gaygirl')
words.remove('gays')
words.remove('gayz')
words.remove('nasty')
pf.define_words(words)
giveawaybot = '294882584201003009'

logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
TEMPLATE_ID = '1nrDrIZ-XmpHw7dF8EMc0LXMSYOhoXTqoX4WO-k8jAgk'
SHEET_IDS = ['1HdtNLRyAMPCD2DYas7ChcS1luKcUTi4AvrdMIsbm1PQ', '1E6ew94iL4FaV2rWCIOdn_ibdFE3hJ_20lR-UmFDLwtk']
TEAM_COLS = 'C,F,I,L,O,R,U,X,AA,AD,AG,AJ'.split(',')
POINT_COLS = 'E,H,K,N,Q,T,W,Z,AC,AF,AI,AL'.split(',')
store = oauth_file.Storage('/root/badgebot/token.json')
creds = store.get()
if not creds or creds.invalid:
  flow = gclient.flow_from_clientsecrets('/root/badgebot/credentials.json', SCOPES)
  creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))



def getmention(message, args='', server=None):
  return message.mentions[0] if len(message.mentions) > 0 else server.get_member_named(args) if len(args) > 0 else message.author

def mutepermission(user):
  if not isinstance(user, str):
    user = discorduser_to_id(user)
  user = id_to_discorduser(user, client.get_server('372042060913442818'))
  return any([role.id in mute_roles for role in user.roles]) if user != None else False

def haspermission(user):
  if not isinstance(user, str):
    user = discorduser_to_id(user)
  user = id_to_discorduser(user, client.get_server('372042060913442818'))
  return any([role.id in permission_roles for role in user.roles]) if user != None else False

def coinpermission(user):
  if not isinstance(user, str):
    user = discorduser_to_id(user)
  user = id_to_discorduser(user, client.get_server('372042060913442818')
)
  return discorduser_to_id(user) == '202380877349650432' or any([role.name=='Arcade Master' for role in user.roles]) if user != None else False

def swear_jar(message):
  return random.random() < 0.02 and pf.is_profane(message.content)

def id_to_discorduser(discord_id, server):
  return server.get_member(discord_id)

def id_to_discordname(discord_id, server):
  return discorduser_to_discordname( id_to_discorduser( discord_id, server ) )

def redditname_to_discorduser(redditname, server):
  return id_to_discorduser( redditname_to_id( redditname ), server )

def redditname_to_discordname(redditname, server):
  return id_to_discordname( redditname_to_id( redditname ) )

def redditname_to_id(redditname):
  cursor.execute(reddit_select_name_str, (redditname.lower(),))
  result = cursor.fetchone()
  if result == None or result[0] == None:
    return None
  return result[0]

def discorduser_to_discordname(user):
  if user == None:
    return None
  result = user.name
  if user.nick != None:
    result = user.nick + ' (' + result + ')'
  return result

def discorduser_to_id(user):
  return user.id

def id_to_redditname(discord_id):
  cursor.execute(reddit_select_str, (discord_id,))
  result = cursor.fetchone()
  if result == None or result[0] == None:
    return None
  return result[0]

def discorduser_to_redditname(user):
  return id_to_redditname( discorduser_to_id( user ) )


def roster_sprites(mons, userid, salt):
  subprocess.call(['/root/badgebot/roster.sh' , userid])
  sprites = [pokemon_list[1][pokemon_list[0].index(mon)] for mon in mons if mon != None]
  moncount = len(sprites)
  sidecount = moncount - 6
  finalimg = Image.new('RGBA', (130 + (0 if sidecount<=0 else (100 + 45*(sidecount//3))), 65), (0,0,0,0))
  for i in range(moncount):
    mon = sprites[i]
    print(mon)
    url = sprite_url.format(mon)
    monimg = Image.open(requests.get(url, stream=True).raw)
    if i < 6:
      finalimg.paste(monimg, box=((i%3)*45, (i//3)*35))
    else:
      finalimg.paste(monimg, box=(190+45*((i-6)//2), 35*((i-6)%2)))
      print((150+45*((i-6)//2), 35*((i-6)%2)))
  filename ='/root/badgebot/rosters/{}.png'.format(userid+'-'+salt)
  finalimg.save(filename)
  subprocess.call(['/root/badgebot/git.sh', filename])

def time_parse_sec(time):
  try:
    return sum([int(t[:-1]) * time_mult[t[-1]] for t in time.split()])
  except:
    return None

async def load_reminder(userid, msg, end, target, salt):
  await client.wait_until_ready()
  time = end - datetime.datetime.utcnow().timestamp()
  await asyncio.sleep(time)
  await client.send_message(discord.Object(id=target), '<@{}>: '.format(userid) + msg)
  cursor.execute('DELETE FROM reminders WHERE salt=?', (salt,))
  connection.commit()

async def load_mute(userid, reason, end, target, salt):
  await client.wait_until_ready()
  time = end - datetime.datetime.utcnow().timestamp()
  await asyncio.sleep(time)

  roles = client.get_server('372042060913442818').roles
  for role in roles:
    if role.name=='Muted':
      mute_role=role
  await client.remove_roles(target, mute_role)
  cursor.execute('DELETE FROM reminders WHERE salt=?', (salt,))
  connection.commit()

def isbadge(badge):
  return badge.lower() in gym_types or badge.lower() in islands or badge.lower() == 'e4champ'

def pokemon_fix(pokemon_name):
  return pokemon_name #TODO: Fix, to make the method return the correct pokemon name if the input name is wrong

def user_badges(userid):
  cursor.execute(badge_select_str, (userid,))
  result = cursor.fetchall()
  if len(result) == 0:
    msg = 'No badges yet'
  else:
    msg = ' '.join([badge_ids[r[0].lower()] for r in result])
  return msg

