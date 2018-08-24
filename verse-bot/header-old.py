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
from profanityfilter import ProfanityFilter


fc_insert_str = 'INSERT INTO friendcodes (id, fc) VALUES (?, ?);'

fc_select_str = 'SELECT fc FROM friendcodes WHERE id=?;'

fc_update_str = 'UPDATE friendcodes SET fc=? WHERE id=?;'

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


swear_insert_str = 'INSERT INTO swears (id,count) VALUES (?, 1);'

swear_select_str = 'SELECT count FROM swears WHERE id=?;'

swear_update_str = 'UPDATE swears SET count=count+1 WHERE id=?;'

swear_dump_str = 'SELECT * from swears ORDER BY count DESC;'

singles_types = ['psychic', 'ghost', 'dragon', 'normal', 'fire', 'grass', 'steel', 'flying']

singles_leaders = ['Pokemonstay', 'SinkingWafers', 'dshmucker', 'Sandman4999', 's0apyjam', '--Tort--', 'Imperial_Eye', 'Ody_Calaith']

doubles_types = ['ground', 'fire', 'flying', 'psychic', 'fighting', 'water', 'dark', 'ghost']

doubles_leaders = ['dshmucker', 's0apyjam', 'Ody_Calaith', 'Pokemonstay', 'Imperial_Eye', 'leader_violist', 'Zavtra13', 'SinkingWafers']

facilities = ['tower', 'palace', 'factory', 'pyramid', 'arena', 'pike', 'dome']

frontier_brains = ['KoheMaster133', 'H2owsome', 'SinkingWafers', 'Sceptistar', 'anthonyprz29', 'Sharbae', 'RoPr-Crusader']


s_gym_flair = 'Gym Battle [B]'

s_e4champ_flair = 'E4-Champ [B]'

d_gym_flair = 'Gym Battle [I]'

d_e4champ_flair = 'E4-Champ [I]'

multi_flair = 'Multi Battle'

fb_flair = 'Frontier Brain'

win_flair = 'Victory'

loss_flair = 'Defeat'

challenge_flairs = [ s_gym_flair, s_e4champ_flair, d_gym_flair, d_e4champ_flair, multi_flair, fb_flair, win_flair, loss_flair ]

singles_flairs = [ s_gym_flair, s_e4champ_flair, win_flair, loss_flair ]

singles_css = [ 'ChallengeBGL', 'ChallengeBE4C', 'Singles'+win_flair, 'Singles'+loss_flair ]

doubles_flairs = [ d_gym_flair, d_e4champ_flair, win_flair, loss_flair ]

doubles_css = [ 'ChallengeIGL', 'ChallengeIE4C', 'Doubles'+win_flair, 'Doubles'+loss_flair ]

finished_flairs = [ win_flair, loss_flair ]

title_flairs = ['[b-gl]', '[b-e4/c]', '[i-gl]', '[i-e4/c]', '[fb]', '[mb]']

challenge_css = [ 'ChallengeBGL', 'ChallengeIGL', 'ChallengeFB', 'ChallengeMulti' ]

tag_err_reg = '@(.*)#(\d*)'

showdown_battle_reg='(battle-gen7.*?)":'

time_limit_message = ">**Hello Challenger!** We are just as excited as you are about your next challenge, but as per the rules, at least 20 hours must pass between each of your challenges."

multi_challenge_message = ">**Hello Challenger!** We're glad you're excited about your next challenge, but the rules state that you cannot have multiple challenges open at once. Please contact the gym leader you challenged to ensure that your previous challenge has closed before creating a new one."

league_pass_message = ">**Hello Challenger!** Thank you for your interest in challenging the league! As per league rules, you must submit a League Pass before you can start taking challenges. Please read the WiKi for more information."

league_pass_link = "[**Link to League Pass**]({})  \n"

no_leader_message = "Please tag the Gym Leader you are battling in a comment"

badgesheet_message = ">**Hello Challenger!** Your badgesheet has been created. Check it out [here](https://www.reddit.com/r/pokeverseleague/wiki/s1lps/{})"


help_message = '''**How To Friend Codes!**

*!setfc XXXX-XXXX-XXXX Additional Text Here* - Sets your FC
     -The additional text can be your IGN, games, etc.
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

**If you still have questions, contact H2owsome**'''

help_message_mod = '''**GLs/FBs only:**
*!badge @someone badgename* - assigns a badge and autoflairs user's reddit post
*!loss @someone badgename* - assings a loss and autoflairs user's reddit post
*!retry @someone badgename* - approves a retry
*!cancel @someone badgename* - cancels someone's challenge

For any of these commands, if someone has not registered their redditname, ask them to do so
**If a command does not work, wait 60 seconds and try again. If it still does not work, please contact H2owsome**'''

invalid_command_message = 'There was a problem with that command, pm me for "!help" for a full list of commands with instructions'

no_reddit_message = "{} does not have a registered reddit username."

no_lp_message = "{} does not have a registered league pass"

invalid_badge_message = "{} is not a valid badge"

no_permissions_message = "You do not have permission to use that command"

connection = sqlite3.connect("/root/verse-bot/friendcodes.db")
cursor = connection.cursor()

reddit = praw.Reddit(user_agent='PokeVerseLeagueBot v0.1',
                     client_id='fgFoep4zeL4Odg',
                     client_secret='DsV7S24RQ9b67VRwVJ15AtT7PCs',
                     username='BananaHammerBot',
                     password='nanananabatman')

subreddit = reddit.subreddit('PokeVerseLeague')

client = discord.Client()

pf = ProfanityFilter(extra_censor_list=['twat', 'bellend', 'bloody', 'bugger'])

def swear_jar(message):
  #return any([swear in message.content.lower() for swear in swear_list])
  return pf.is_profane(message.content)


def id_to_discorduser(discord_id):
  result = list(filter( lambda x: x.id == discord_id, client.get_all_members() ))
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

def replied(submission):
    for comment in submission.comments:
        if comment.author == reddit.user.me():
            return True
    return False

def ischallenge(title):
  for word in title_flairs:
    if word in title:
      return True
  return False

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

def wiki_exists( username ):
  return ('[u/' + username.lower() + ']') in subreddit.wiki['s1lps'].content_md.lower()

def wiki_sort( wiki_text ):
  wiki_part = wiki_text.partition("#Season 1 LPs")
  lines = wiki_part[2].split("\n")
  lines.sort(key=lambda x: x.lower())
  sted = "\n".join(lines)
  return wiki_part[0] + wiki_part[1] + "\n" + sted

def create_wiki( username ):
  if not wiki_exists( username ):
    template = subreddit.wiki['badges/base']
    badgepass = template.content_md.replace('$$$$', username)
    subreddit.wiki.create('s1lps/'+username, badgepass, reason='Assign Badge Pass')
    index = subreddit.wiki['s1lps']
    updated_index = index.content_md + '\n* [u/' + username + '](https://www.reddit.com/r/PokeVerseLeague/wiki/s1lps/'+username+')'
    index.edit(wiki_sort(updated_index))
    print('Created BadgeSheet for ' + username)
  else:
    print('BadgeSheet already exists for ' + username)

def add_badge( username, badge ):
  badgesheet = subreddit.wiki['s1lps/' + username]
  badgesheetupdate = badgesheet.content_md.replace(badge+'no', badge)
  badgesheet.edit(badgesheetupdate)
  print('Granted badge ' + badge + ' for ' + username )

def challenges_list(author, badge):
  challenges = []
  if issingles(badge):
    challenges = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_text in singles_flairs, author.submissions.new()))
  if isfrontier(badge):
    challenges = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_text == fb_flair, author.submissions.new()))
  if isdoubles(badge):
    challenges = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_text in doubles_flairs, author.submissions.new()))
  return challenges


