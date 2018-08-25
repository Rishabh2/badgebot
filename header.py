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


fc_insert_str = 'INSERT INTO userinfo (id, fc, url) VALUES (?, ?, ?);'

fc_select_str = 'SELECT fc, url FROM userinfo WHERE id=?;'

fc_update_str = 'UPDATE userinfo SET fc=?, url=? WHERE id=?;'

fc_delete_str = 'DELETE FROM userinfo WHERE id=?;'


tsv_insert_str = 'INSERT INTO tsv (id, tsv, game) VALUES (?, ?, ?);'

tsv_request_str = 'SELECT id, game FROM tsv WHERE tsv=?;'

tsv_delete_str = 'DELETE FROM tsv WHERE id=? AND tsv=?;'

tsv_select_str = 'SELECT tsv, game FROM tsv WHERE id=?;'

tsv_dump_str = 'SELECT * FROM tsv'


reddit_insert_str = 'INSERT INTO userinfo (id, reddit) VALUES (?, ?);'

reddit_select_str = 'SELECT reddit FROM userinfo WHERE id=?;'

reddit_select_name_str = 'SELECT id FROM userinfo WHERE lower(reddit)=?;'

reddit_update_str = 'UPDATE userinfo SET reddit=? WHERE id=?;'


swear_insert_str = 'INSERT INTO userinfo (id,swears) VALUES (?, 1);'

swear_select_str = 'SELECT swears FROM userinfo WHERE id=?;'

swear_update_str = 'UPDATE userinfo SET swears=swears+1 WHERE id=?;'

swear_begin_str = 'UPDATE userinfo SET swears=1 WHERE id=?;'

swear_dump_str = 'SELECT id, swears from userinfo WHERE swears>=? ORDER BY swears DESC;'


coins_insert_str = 'INSERT INTO userinfo (id, coins) VALUES (?, ?);'

coins_select_str = 'SELECT coins FROM userinfo WHERE id=?;'

coins_update_str = 'UPDATE userinfo SET coins=? WHERE id=?;'

coins_dump_str = 'SELECT id, coins from userinfo WHERE coins>0 ORDER BY coins DESC;'


info_dump_str = 'SELECT * from userinfo WHERE id=?;'


draft_select_str = 'SELECT conference, team FROM draft WHERE id=?;'

draft_insert_str = 'INSERT INTO draft (id, conference, team) VALUES (?,?,?);'


singles_types = ['grass', 'flying', 'poison', 'fairy', 'ice', 'normal', 'ground', 'rock']

singles_leaders = ['Yuknessia', 'RoPr-Crusader', 'Zavtra13', 'hannyfish', 'TheRogueCookie', 'silent_sage93', '--Tort--', 'Esskido']

singles_e4 = ['AgitatedDog', 'Lolzfool', 'dshmucker', 'SinkingWafers', 'thattimeyguy']

singles_e4_channel = '451919255244505098'

singles_channels = ['451919402280026162', '451919528436170754', '451919594224091136', '451919672938463255', '451919887066202113', '451920062434246656', '451920196848844810', '451920209226235914']

doubles_types = ['electric', 'fairy', 'ground', 'normal', 'psychic', 'bug', 'fire', 'ghost']

doubles_leaders = ['silent_sage93', 'hannyfish', 'dshmucker', 'H2owsome', 'anthonyprz29', 'PokemonStay', 's0apyjam', 'SinkingWafers']

doubles_e4 = ['--Tort--', 'RoPr-Crusader', 'thattimeyguy', 'Zavtra13', 'Lolzfool']

doubles_e4_channel = '455926712379768832'

doubles_channels = ['456191512439685140', '455926804872429579', '455926861348995073', '455927300790157322', '455927335573520386', '455927379810975746', '455927398756777985', '455927412622884864']

arcade_channel = '463817264752492574'

facilities = ['tower', 'palace', 'factory', 'pyramid', 'arena', 'pike', 'dome']

frontier_brains = ['KoheMaster133', 'H2owsome', 'SinkingWafers', 'Sceptistar', 'anthonyprz29', 'Sharbae', 'RoPr-Crusader']

badge_ids = {
    'grasssingles':'<a:grasssingles:482073772535578655>',
    'normalsingles':'<a:normalsingles:482073773730824192>',
    'fairysingles':'<a:fairysingles:482067974119882752>',
    'icesingles':'<a:icesingles:482067977714401302>',
    'groundsingles':'<a:groundsingles:482067974027739137>',
    'poisonsingles':'<a:poisonsingles:482070458552942604>',
    'rocksingles':'<a:rocksingles:482071206678495252>',
    'flyingsingles':'<a:flyingsingles:482071987984793600>',
    }

s_gym_flair = 'Singles Gym'

s_e4champ_flair = 'Singles E4/C'

d_gym_flair = 'Doubles Gym'

d_e4champ_flair = 'Doubles E4/C'

multi_flair = 'Multi Battle'

fb_flair = 'Battle Frontier'

win_flair = 'Victory'

loss_flair = 'Defeat'

challenge_flairs = [ s_gym_flair, s_e4champ_flair, d_gym_flair, d_e4champ_flair, multi_flair, fb_flair, win_flair, loss_flair ]

singles_flairs = [ s_gym_flair, s_e4champ_flair ]

singles_css = [ 'ChallengeBGL', 'ChallengeBE4C', 'Singles'+win_flair, 'Singles'+loss_flair ]

doubles_flairs = [ d_gym_flair, d_e4champ_flair ]

doubles_css = [ 'ChallengeIGL', 'ChallengeIE4C', 'Doubles'+win_flair, 'Doubles'+loss_flair ]

finished_flairs = [ win_flair, loss_flair ]

title_flairs = ['[b-gl]', '[b-e4/c]', '[i-gl]', '[i-e4/c]', '[fb]', '[mb]']

challenge_css = [ 'ChallengeBGL', 'ChallengeIGL', 'ChallengeFB', 'ChallengeMulti' ]

tag_err_reg = '@(.*)#(\d*)'

showdown_battle_reg='(battle-gen7(.*?))":'

time_limit_message = ">**Hello Challenger!** We are just as excited as you are about your next challenge, but as per the rules, at least 20 hours must pass between each of your challenges."

multi_challenge_message = ">**Hello Challenger!** We're glad you're excited about your next challenge, but the rules state that you cannot have multiple challenges open at once. Please contact the gym leader you challenged to ensure that your previous challenge has closed before creating a new one."

league_pass_message = ">**Hello Challenger!** Thank you for your interest in challenging the league! As per league rules, you must submit a League Pass before you can start taking challenges. Please read the WiKi for more information."

league_pass_link = "[**Link to League Pass**]({})  \n"

no_leader_message = "Please tag the Gym Leader you are battling in a comment"

badgesheet_message = ">**Hello Challenger!** Your badgesheet has been created. Check it out [here](https://www.reddit.com/r/pokeverseleague/wiki/s2lps/{})"


help_message = discord.Embed(title="Badgebot Commands", color=discord.Color(0x85bff8), description="Below is the documentation for the various badgebot commands.")
help_message.set_footer(text="Please contact H2owsome with any questions.")
help_message.add_field(name="Friends", value="Commands related to 3DS Friend Codes:\n!setFC Text - Sets your Friend Code to the specified Text\n!getFC/!getFC @User - Obtains your or the tagged user's FC")
help_message.add_field(name="TSV", value="Commands related to your games' shiny values:\n!addTSV XXXX GameName\n!deleteTSV XXXX - Deletes all instances of a given TSV you own\n!getTSV - Obtains all users with a matching TSV\n!gettsv @User - Get the user's TSVs\n!dumpTSV - Lists all TSVs on the server")
help_message.add_field(name="Reddit", value="Commands related to Reddit accounts:\n!setReddit Username - Links your discord and reddit accounts. *setReddit must be used before obtaining badges.*\n!getReddit @User - Obtains user's reddit account.\n!getLP @User - Obtains the tagged user's league pass.\n!getBadges @User - Obtains the tagged user's badges.\n*You may also provide a Reddit username to the above functions.*")
help_message.add_field(name="Misc", value="!gettime - Obtains the amount of time until you may challenge.\n!est - Obtains the time in the EST timezone\n!time TimeZone - Obtains the time in the specified time zone.\n!calculate - Performs basic math calculations.\n!leaks - Toggles access to the #leaks-and-spoilers channel.\n!coin - Get a list of who has PVL coins\n!coin @User - check how many coins a user has\n", inline=True)

help_message_mod = discord.Embed(title="GLs/Mods only:", color=discord.Color(0x85bff8), description="These commands are for use with the official Gym Challenge.\nIf a command fails, do not repeatedly attempt to use it.")
help_message_mod.set_footer(text="Please contact H2owsome with any questions.")
help_message_mod.add_field(name="Commands", value="!badge @someone badgename - assigns a badge and autoflairs user's reddit post\n!loss @someone badgename - assings a loss and autoflairs user's reddit post\nretry @someone badgename - approves a retry\n!cancel @someone badgename - cancels someone's challengei\n!wipe - wipe your channel\nFor any of these commands, if someone has not registered their redditname, ask them to do so", inline=True)

invalid_command_message = 'There was a problem with that command, pm me for "!help" for a full list of commands with instructions'

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

season_start_date = datetime.datetime(2018, 6, 1) # June 1st 2018, LP limit

pf = ProfanityFilter(extra_censor_list=['twat', 'bellend', 'bloody', 'bugger'])
words = pf.get_profane_words()
words.remove('gay')
words.remove('gaybor')
words.remove('gayboy')
words.remove('gaygirl')
words.remove('gays')
words.remove('gayz')
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



def add_badge( username, badge ):
  badgesheet = subreddit.wiki['s2lps/' + username]
  badgesheetupdate = badgesheet.content_md.replace(badge+'no', badge)
  badgesheet.edit(badgesheetupdate)
  card = get_league_pass(username)
  card.reply('Congrats on earning your ' + badge + ' badge!')
  return replied(card)

def approve_rematch( username ):
  for submission in subreddit.mod.modqueue(only='submissions'):
    if submission.author.name.lower() == username.lower():
      submission.mod.approve()
      for i, tf in enumerate(title_flairs):
        if tf in submission.title.lower():
          submission.mod.flair(text=challenge_flairs[i],css_class=challenge_css[i])
      return True
  return False

def cancel_challenge(username, badge):
  challenges = challenges_list(username, badge)
  if len(challenges) > 0:
    challenges[0].mod.flair(text='Removed', css_class='')
    challenges[0].reply('Your challenge has been removed')
    challenges[0].mod.remove()
    return True
  else:
    return False

def challenges_list(author, badge):
  if isinstance(author, str):
    author = reddit.redditor(author)
  challenges = []
  if issingles(badge):
    challenges = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_text in singles_flairs, author.submissions.new(limit=10)))
  if isfrontier(badge):
    challenges = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_text == fb_flair, author.submissions.new(limit=10)))
  if isdoubles(badge):
    challenges = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_text in doubles_flairs, author.submissions.new(limit=10)))
  return challenges

def flair_post( username, badge, flair ):
  challenges = challenges_list(username, badge)
  if len(challenges) > 0:
    challenge = challenges[0]
    if 'e4' in badge and flair=='Defeat':
      losses = replied(challenge)
      challenge.reply('This marks ' + str(losses) + ' loss(es) on your current run')
      if losses < 3:
        return True
    challenge.mod.flair(text=flair, css_class=flair_to_css(badge, flair))
    return True
  return False

def get_badges(username):
  if username in ['me', 'my', 'your']:
    return 'User is me'
  elif wiki_exists(username):
    return 'https://reddit.com/r/PokeVerseLeague/wiki/s2lps/'+username
  else:
    return 'User does not have a badge sheet'

def get_league_pass(username):
  if username in ['me', 'my', 'your']:
    return 'User is me'
  author = reddit.redditor(username)
  for x in author.submissions.new(limit=100):
    if x.subreddit == subreddit and x.link_flair_text  == 'League Pass' and replied(x)>0 and season_start_date < datetime.datetime.utcfromtimestamp(x.created_utc):
      return x
  return username + ' register your League Pass! Or face the wrath of  <@!103049236525887488>.'

def getmention(message):
  return message.mentions[0] if len(message.mentions) > 0 else None

def haspermission(user):
  if not isinstance(user, str):
    user = discorduser_to_id(user)
  user = id_to_discorduser(user, client.get_server('372042060913442818')
)
  return any(role.hoist for role in user.roles) if user != None else False

def coinpermission(user):
  if not isinstance(user, str):
    user = discorduser_to_id(user)
  user = id_to_discorduser(user, client.get_server('372042060913442818')
)
  return discorduser_to_id(user) == '202380877349650432' or any([role.name=='Arcade Master' for role in user.roles]) if user != None else False

def issingles(badge):
  if badge == 'e4champsingles':
    return True
  for st in singles_types:
    if badge == st + 'singles':
      return True
  return False

def isfrontier(badge):
  return badge in facilities

def isdoubles(badge):
  if badge == 'e4champdoubles':
    return True
  for dt in doubles_types:
    if badge == dt + 'doubles':
      return True
  return False

def isbadge(badge):
  return issingles(badge) or isfrontier(badge) or isdoubles(badge)

def flair_to_css(badge, flair):
  if issingles(badge):
    return 'Singles'+flair
  if isdoubles(badge):
    return 'Doubles'+flair
  if isfrontier(badge):
    return 'Frontier'+flair


def ischallenge(title):
  for word in title_flairs:
    if word in title:
      return True
  return False


def make_embed(text, url, user):
  if text != None:
    embed = discord.Embed(title=text)
  else:
    embed = discord.Embed()
  embed.set_thumbnail(url=url)
  return embed


def replied(submission):
  me = reddit.user.me()
  return sum([1 if comment.author == me else 0 for comment in submission.comments])

def swear_jar(message):
  return pf.is_profane(message.content)

def tag_leader(submission):
  if submission.link_flair_text == s_gym_flair:
    return tag_leader_singles(submission.title.lower())
  if submission.link_flair_text == fb_flair:
    return tag_leader_frontier(submission.title.lower())
  if submission.link_flair_text == d_gym_flair:
    return tag_leader_doubles(submission.title.lower())
  return None

def tag_leader_singles(title):
  for i, typ in enumerate(singles_types):
    if typ in title:
      return singles_leaders[i]
  return None

def tag_leader_doubles(title):
  for i, typ in enumerate(doubles_types):
    if typ in title:
      return doubles_leaders[i]
  return None

def tag_leader_frontier(title):
  for i, typ in enumerate(facilities):
    if typ in title:
      return frontier_brains[i]
  return None



def time_to_challenge(name):
  author = reddit.redditor(name)
  challenges = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_text in challenge_flairs, author.submissions.new(limit=10)))
  if len(challenges) > 0:
    time_dif = datetime.datetime.utcnow() - datetime.datetime.fromtimestamp(challenges[0].created_utc)
    since_20 = datetime.timedelta(hours=20) - time_dif
    if since_20.days >= 0:
      return name + ' can post a challenge in ' + ':'.join(str(since_20).split(':')[:2])
  return name + ' is ready to post their next challenge!'

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


def wiki_exists( username ):
  return ('[u/' + username.lower() + ']') in subreddit.wiki['s2lps'].content_md.lower()

def wiki_sort( wiki_text ):
  wiki_part = wiki_text.partition("#Season 2 LPs")
  lines = wiki_part[2].split("\n")
  lines.sort(key=lambda x: x.lower())
  sted = "\n".join(lines)
  return wiki_part[0] + wiki_part[1] + "\n" + sted

def create_wiki( username ):
  if not wiki_exists( username ):
    template = subreddit.wiki['badges/base']
    badgepass = template.content_md.replace('$$$$', username)
    subreddit.wiki.create('s2lps/'+username, badgepass, reason='Assign Badge Pass')
    index = subreddit.wiki['s2lps']
    updated_index = index.content_md + '\n* [u/' + username + '](https://www.reddit.com/r/PokeVerseLeague/wiki/s2lps/'+username+')'
    index.edit(wiki_sort(updated_index))

def roster_sprites(mons, userid, salt):
  subprocess.call(['/root/badgebot/roster.sh' , userid])
  sprites = [pokemon_list[1][pokemon_list[0].index(mon)] for mon in mons if mon != None]
  moncount = len(sprites)
  sidecount = moncount - 6
  finalimg = Image.new('RGBA', (130 + (0 if sidecount<=0 else (100 + 45*(sidecount//3))), 65), (0,0,0,0))
  for i in range(moncount):
    mon = sprites[i]
    print(mon)
    url = 'https://raw.githubusercontent.com/msikma/pokesprite/master/icons/pokemon/regular/{}.png'.format(mon)
    monimg = Image.open(requests.get(url, stream=True).raw)
    if i < 6:
      finalimg.paste(monimg, box=((i%3)*45, (i//3)*35))
    else:
      finalimg.paste(monimg, box=(190+45*((i-6)//2), 35*((i-6)%2)))
      print((150+45*((i-6)//2), 35*((i-6)%2)))
  filename ='/root/badgebot/rosters/{}.png'.format(userid+'-'+salt)
  finalimg.save(filename)
  subprocess.call(['/root/badgebot/git.sh', filename])

