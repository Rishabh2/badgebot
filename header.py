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
import passwords
from profanityfilter import ProfanityFilter


fc_insert_str = 'INSERT INTO friendcodes (id, fc, url) VALUES (?, ?, ?);'

fc_select_str = 'SELECT fc, url FROM friendcodes WHERE id=?;'

fc_update_str = 'UPDATE friendcodes SET fc=?, url=? WHERE id=?;'

fc_delete_str = 'DELETE FROM friendcodes WHERE id=?;'


tsv_insert_str = 'INSERT INTO tsv (id, tsv, game) VALUES (?, ?, ?);'

tsv_request_str = 'SELECT id, game FROM tsv WHERE tsv=?;'

tsv_delete_str = 'DELETE FROM tsv WHERE id=? AND tsv=?;'

tsv_select_str = 'SELECT tsv, game FROM tsv WHERE id=?;'

tsv_dump_str = 'SELECT * FROM tsv'


reddit_insert_str = 'INSERT INTO reddit (id, name) VALUES (?, ?);'

reddit_select_str = 'SELECT name FROM reddit WHERE id=?;'

reddit_select_name_str = 'SELECT id FROM reddit WHERE lower(name)=?;'

reddit_update_str = 'UPDATE reddit SET name=? WHERE id=?;'

reddit_delete_str = 'DELETE FROM reddit WHERE id=?;'


pings_insert_str = 'INSERT into pings (id, message) VALUES (?, ?);'

pings_select_str = 'SELECT * FROM pings'

pings_clear_str = 'DELETE FROM pings'


swear_insert_str = 'INSERT INTO swears (id,count) VALUES (?, 1);'

swear_select_str = 'SELECT count FROM swears WHERE id=?;'

swear_update_str = 'UPDATE swears SET count=count+1 WHERE id=?;'

swear_dump_str = 'SELECT * from swears ORDER BY count DESC;'


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

facilities = ['tower', 'palace', 'factory', 'pyramid', 'arena', 'pike', 'dome']

frontier_brains = ['KoheMaster133', 'H2owsome', 'SinkingWafers', 'Sceptistar', 'anthonyprz29', 'Sharbae', 'RoPr-Crusader']


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


help_message = '''**How To Friend Codes!**

*!setfc XXXX-XXXX-XXXX Additional Text Here* - Sets your FC
     -The additional text can be your IGN, games, etc.
     -You can also include a picture, if you like!
*!getfc* - fetches your own FC
*!getfc @someone* - fetches tagged user's FC

**How To TSV!**

*!addtsv XXXX Game Name Here* - adds your TSV to the database.
     -If you have multiple games, please only add ONE AT A TIME to the bot. You can add multiple, but need to enter each TSV SEPARATELY
*!gettsv* - pulls up a list of all TSVs that you have entered
*!deletetsv XXXX* - deletes TSV that you have entered with the value XXXX
*!gettsv XXXX* - pulls up a list of anyone who has entered their TSV as value XXXX in the database
*!dumptsv* - lists all tsvs currently stored on the server

**How To Reddit!**

*!setreddit redditusername* - links your Reddit username with your Discord Account. Required to earn badges.
     -Do NOT put anything that's not your Reddit username into the bot. Enter as "username" not "u/username"
*!getreddit @someone* - fetches @someone's Reddit username
*!getreddit redditusername* - fetches the discord name of the user with the specified reddit name

*!getLP @someone* - fetches a quick link to @someone's League Pass
*!getLP redditusername* - fetches redditusername's LP in the event that they have not set their username with badge bot

*!getBadges @someone* - fetches a quick link to @someone's Records Page
*!getBadges redditusername* - fetches redditusername's Records Page in the event that they have not set their username with badge bot

**Misc**

*!gettime - get the time remainaing until you can send your next gym leader challenge
*!leaks - toggle access to the leaks and spoilers channel

**If you still have questions, contact H2owsome**'''

help_message_mod = '''**GLs/FBs only:**
*!badge @someone badgename* - assigns a badge and autoflairs user's reddit post
*!loss @someone badgename* - assings a loss and autoflairs user's reddit post
*!retry @someone badgename* - approves a retry
*!cancel @someone badgename* - cancels someone's challenge

For any of these commands, if someone has not registered their redditname, ask them to do so
**If a command does not work, DO NOT try it again. Double check if it went through on reddit, and if not, please contact H2owsome**'''

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


connection = sqlite3.connect("/root/verse-bot/friendcodes.db")
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

logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

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
  cards = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_text  == 'League Pass' and replied(x)>0 and season_start_date < datetime.datetime.utcfromtimestamp(x.created_utc), author.submissions.new()))
  if len(cards) == 0:
    return username + ' does not have a registered league pass'
  else:
    return cards[0]

def getmention(message):
  return message.mentions[0] if len(message.mentions) > 0 else None

def haspermission(user):
  if isinstance(user, str):
    user = id_to_discorduser(user)
  return any(role.hoist for role in user.roles)

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
  embed = discord.Embed(title=text)
  if haspermission(user):
    embed.set_thumbnail(url=url)
  else:
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

def id_to_discorduser(discord_id):
  result = list(filter( lambda x: x.id == discord_id, client.get_all_members()  ))
  if len(result) == 0:
    return None
  return result[0]

def id_to_discordname(discord_id):
  return discorduser_to_discordname( id_to_discorduser( discord_id ) )


def redditname_to_discorduser(redditname):
  return id_to_discorduser( redditname_to_id( redditname ) )

def redditname_to_discordname(redditname):
  return id_to_discordname( redditname_to_id( redditname ) )

def redditname_to_id(redditname):
  cursor.execute(reddit_select_name_str, (redditname.lower(),))
  result = cursor.fetchone()
  if result == None:
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
  if result == None:
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
