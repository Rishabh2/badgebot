import discord
import sqlite3
import praw
import random
import re
import asyncio

# Helix here is the list of things to do to make this work for doubles:
#	On line 55, add in all of the types for doubles into the array, following the format of the singles_types array above it
#	On line 116, finish the function tag_leader_doubles. Just have 8 if statements, each of which checks if the title contains the type, and if it does, returns the reddit
#		name of the appropriate GL, and at the end returns None. Match the format of tag_leader_singles which is above it. Make sure it's the REDDIT NAME
#	

client = discord.Client()
connection = sqlite3.connect("/root/verse-bot/friendcodes.db")
cursor = connection.cursor()

reddit = praw.Reddit(user_agent='PokeVerseLeagueBot v0.1',
                     client_id='fgFoep4zeL4Odg',
                     client_secret='DsV7S24RQ9b67VRwVJ15AtT7PCs',
                     username='BananaHammerBot',
                     password='nanananabatman')


fc_insert_str = 'INSERT INTO friendcodes (id, fc) VALUES (?, ?);'

fc_select_str = 'SELECT fc FROM friendcodes WHERE id=?;'

fc_update_str = 'UPDATE friendcodes SET fc=? WHERE id=?;'

fc_delete_str = 'DELETE FROM friendcodes WHERE id=?;' 

tsv_insert_str = 'INSERT INTO tsv (id, tsv, game) VALUES (?, ?, ?);'

tsv_request_str = 'SELECT id, game FROM tsv WHERE tsv=?;'

tsv_delete_str = 'DELETE FROM tsv WHERE id=? AND tsv=?;'

tsv_select_str = 'SELECT tsv, game FROM tsv WHERE id=?;'

reddit_insert_str = 'INSERT INTO reddit (id, name) VALUES (?, ?);'

reddit_select_str = 'SELECT name FROM reddit WHERE id=?;'

reddit_select_name_str = 'SELECT id FROM reddit WHERE name=?;'

reddit_update_str = 'UPDATE reddit SET name=? WHERE id=?;'

reddit_delete_str = 'DELETE FROM reddit WHERE id=?;' 

subreddit = reddit.subreddit('PokeVerseLeague')

singles_types = ['fire', 'steel', 'flying', 'ghost', 'grass', 'normal', 'dragon', 'psychic']

doubles_types = ['type1', 'type2', 'type3', 'type4', 'type5', 'type6', 'type7', 'type8']

facilities = ['tower', 'palace', 'factory', 'pyramid', 'arena', 'pike', 'dome']

headers = ['e4champsingles', 'e4champdoubles', 'multi', 'frontier']

challenge_flairs = ['Gym Battle [B]', 'E4-Champ [B]', 'Gym Battle [I]', 'E4-Champ [I]', 'Multi Battle', 'Frontier Brain', 'Victory', 'Defeat']

singles_flairs = challenge_flairs[:2]

doubles_flairs = challenge_flairs[2:3]

headers_flairs = ['E4-Champ [B]', 'E4-Champ [I]', 'Multi Battle', 'Frontier Brain']

tag_err_reg = '@(.*)#(\d*)'

responded = []
responded_posts = []
finished_challenge_flairs = ['Victory', 'Defeat']

def tag_leader(submission):
	if submission.link_flair_text == 'Gym Battle [B]':
		return tag_leader_singles(submission.title.lower())
	if submission.link_flair_text == 'Frontier Brain':
		return tag_leader_frontier(submission.title.lower())
	if submission.link_flair_text == 'Gym Battle [I]':
		return tag_leader_doubles(submission.title.lower())
	return None

def tag_leader_frontier(title):
	if 'tower' in title:
		return 'KoheMaster133'
	if 'palace' in title:
		return 'H2owsome'
	if 'factory' in title:
		return 'SinkingWafers'
	if 'pyramid' in title:
		return 'Sceptistar'
	if 'arena' in title:
		return 'anthonyprz29'
	if 'pike' in title:
		return 'Sharbae'
	if 'dome' in title:
		return 'RoPr-Crusader'
	return None

def tag_leader_singles(title):
	if 'psychic' in title:
		return 'Rainy_Days1115'
	if 'ghost' in title:
		return 'veenveen'
	if 'dragon' in title:
		return 'dshmucker'
	if 'normal' in title:
		return 'Sandman4999'
	if 'fire' in title:
		return 'PlokCro'
	if 'grass' in title:
		return '--Tort--'
	if 'steel' in title:
		return 'Imperial_Eye'
	if 'flying' in title:
		return 'Ody_Calaith'
	return None

def tag_leader_doubles(title):
	if 'type1' in title:
		return 'Leader1'
	if 'type2' in title:
		return 'Leader2'
	if 'type3' in title:
		return 'Leader3'
	if 'type4' in title:
		return 'Leader4'
	if 'type5' in title:
		return 'Leader5'
	if 'type6' in title:
		return 'Leader6'
	if 'type7' in title:
		return 'Leader7'
	if 'type8' in title:
		return 'Leader8'
	return None

def replied(submission):
    for comment in submission.comments:
        if comment.author == reddit.user.me():
            return True
    return False

def ischallenge(title):
 return '[b-gl]' in title or '[b-e4/c]' in title or '[i-gl]' in title or '[i-e4/c]' in title or '[fb]' in title or '[mb]' in title

def process():
    members=[]
    for submission in subreddit.new(limit=5):
        cont = True
        if ischallenge(submission.title.lower()):
            author = submission.author
            challenges = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_text == submission.link_flair_text, author.submissions.new()))
            challenges.sort(key=lambda x: x.created_utc, reverse=True)
            if author not in responded_posts and submission.approved == False:
                responded_posts.append(author)
                if len(challenges) > 1 and challenges.index(submission) < len(challenges) - 1:
                    time_dif = submission.created_utc - challenges[challenges.index(submission)+1].created_utc
                    if time_dif < 72000:
                        submission.reply(">**Hello Challenger!** We are just as excited as you are about your next challenge, but as per the rules, at least 20 hours must pass between each of your challenges.")
                        submission.mod.flair(text='Removed', css_class='')
                        submission.mod.remove()
                        cont = False
                        print('Removed challenge of ' + author.name + ' for breaking the 20 hour rule')
                    if challenges[1].link_flair_text not in finished_challenge_flairs:
                        submission.reply(">Hi There! We're glad you're excited about your next challenge, but the rules state that you cannot have multiple challenges open at once. Please contact the gym leader you challenged to ensure that your previous challenge has closed before creating a new one.")
                        submission.mod.flair(text='Removed', css_class='')
                        submission.mod.remove()
                        cont = False
                        print('Removed challenge of ' + author.name + ' for breaking the one challenge ever 20 hours rule') 
            if cont:
                cards = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_text == 'League Pass', author.submissions.new()))
                if len(cards) == 0:
                    submission.reply(">**Hello Challenger!** Thank you for your interest in challenging the league!** As per league rules, you must submit a League Pass before you can start taking challenges. Please read the WiKi for more information.")
                    submission.mod.flair(text='Removed', css_class='')
                    submission.mod.remove()
                    print('Removed challenge of ' + author.name + ' as they did not have a League Pass')
                elif submission.id not in responded:
                    for comment in submission.comments:
                        if comment.author == reddit.user.me() and comment.body.find('Link') != -1:
                            cont = False
                    if cont:
                        leader = tag_leader(submission) 
                        reply = "[**Link to League Pass**](" + cards[0].url + ")  \n"
                        if leader == None:
                            reply += "Please tag the Gym Leader you are battling in a comment"
                        else:
                            reply += '/u/'+leader
                            cursor.execute('SELECT id from reddit WHERE name=?', (leader,))
                            result = cursor.fetchone()
                            if result != None:
                                discord_member = discord_user(result[0])
                                members.append((discord_member, submission.url))
                        submission.reply(reply)
                        responded.append(submission.id)
                        print('League Pass link attached to latest challenge from ' + author.name)
        
    for comment in subreddit.comments(limit=5):
        if comment.body.startswith('Approve') or comment.body.startswith('approve'):
            parent = comment.parent()
            if '[lp]' in parent.title.lower() and not replied(parent):
                create_wiki(parent.author.name)
                parent.reply(">**Hello Challenger!** Your badgesheet has been created. Check it out [here](https://www.reddit.com/r/pokeverseleague/wiki/s1lps/" + parent.author.name + ")") 
    return members


def pyramid():
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

def issingles(badge):
	for st in singles_types:
		if badge == st + 'singles':
			return True
	return False

def isfrontier(badge):
	return badge in facilities

def isdoubles(badge):
	for dt in doubles_types:
		if badge == dt + 'doubles':
			return True
	return False

def isheaders(badge):
	return badge in headers

def isbadge(badge):
	return issingles(badge) or isfrontier(badge) or isdoubles(badge) or isheaders(badge)

def wiki_exists( username ):
	return ('[u/' + username.lower() + ']') in subreddit.wiki['s1lps'].content_md.lower()

def create_wiki( username ):
	template = subreddit.wiki['badges/base']
	badgepass = template.content_md.replace('$$$$', username)
	subreddit.wiki.create('s1lps/'+username, badgepass, reason='Assign Badge Pass')
	index = subreddit.wiki['s1lps']
	updated_index = index.content_md + '\n* [u/' + username + '](https://www.reddit.com/r/PokeVerseLeague/wiki/s1lps/'+username+')'
	index.edit(updated_index)
	print('Created BadgeSheet for ' + username)

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
		challenges = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_text == challenge_flairs[5], author.submissions.new()))
	if isdoubles(badge):
		challenges = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_text in doubles_flairs, author.submissions.new()))
	if isheaders(badge):
		challenges = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_text in headers_flairs, author.submissions.new()))
	return challenges

def flair_post( username, badge, flair ):
	author = reddit.redditor(username)
	challenges = challenges_list(author, badge)
	if len(challenges) > 0:
		challenges[0].mod.flair(text=flair, css_class=flair)
		return True
	return False

def approve_rematch( username ):
	for submission in subreddit.mod.modqueue(only='submissions'):
		if submission.author.name.lower() == username.lower():
			submission.mod.approve()
			if  '[B-GL]' in submission.title:
				submission.mod.flair(text='Gym Battle [B]', css_class='ChallengeBGL')
			elif  '[I-GL]' in submission.title:
				submission.mod.flair(text='Gym Battle [I]', css_class='ChallengeIGL')
			elif  '[FB]' in submission.title:
				submission.mod.flair(text='Frontier Brain', css_class='ChallengeFB')
			elif  '[MB]' in submission.title:
    				submission.mod.flair(text='Multi Battle', css_class='ChallengeMulti')	
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
	cards = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_text == 'League Pass', author.submissions.new()))
	if len(cards) == 0:
		return username + ' does not have a registered league pass'
	else:
		return cards[0].url

def get_badges(username):
	if username in ['me', 'my', 'your']:
		return 'User is me'
	elif wiki_exists(username):
		return 'https://reddit.com/r/PokeVerseLeague/wiki/s1lps/'+username
	else:
		return 'User does not have a badge sheet'

def startswith( text, prefix ):
	return text.lower().startswith(prefix)

def discord_user( discord_id ):
	return list(filter( lambda x: x.id == discord_id, client.get_all_members() ))[0]

def redditname( user ):
	cursor.execute( reddit_select_str, (user,))
	result = cursor.fetchone()
	return result if result == None else result[0]

def discordname( member ):
	return member.name if member.nick == None else member.nick

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if startswith(message.content, '!help'):
		msg = '''**How To Friend Codes!**

*!setfc XXXX-XXXX-XXXX Additional Text Her*e - Sets your FC
     -The additional text can be your IGN, games, etc. 
*!getfc* - fetches your own FC
*!getfc @someone* - fetches tagged user's FC

**How To TSV!**

*!addtsv XXXX Game Name Here* - adds your TSV to the database. 
     -If you have multiple games, please only add ONE AT A TIME to the bot. You can add multiple, but need to enter each TSV SEPARATELY
*!gettsv* - pulls up a list of all TSVs that you have entered
*!deletetsv XXXX* - deletes TSV that you have entered with the value XXXX
*!gettsv XXXX* - pulls up a list of anyone who has entered their TSV as value XXXX in the database

**How To Reddit!**

*!setreddit redditusername* - links your Reddit username with your Discord Account. Required to earn badges. 
     -Do NOT put anything that's not your Reddit username into the bot. Enter as "username" not "u/username"
*!getreddit @someone* - fetches @someone's Reddit username
*!getLP @someone* - fetches a quick link to @someone's League Pass
*!getLP redditusername* - fetches redditusername's LP in the event that they have not set their username with badge bot
*!getBadges @someone* - fetches a quick link to @someone's Records Page
*!getBadges redditusername* - fetches redditusername's Records Page in the event that they have not set their username with badge bot

**If you still have questions, contact H2owsome**

**GLs/FBs only:**
*!badge @someone badgename* - assigns a badge and autoflairs user's reddit post
*!loss @someone badgename* - assings a loss and autoflairs user's reddit post
*!retry @someone badgename* - approves a retry
*!cancel @someone badgename* - cancel's someone's challenge

For any of these commands, if someone has not registered their redditname, ask them to do so
**If a command does not work, contact H2owsome before trying the command again**'''

		post = 'Sent response via PM'
		await client.send_message(message.channel, post)
		await client.send_message(message.author, msg)
	if startswith(message.content, '!setfc'):
		if len(message.mentions) > 0:
			msg = "Please do not include user tags in your FC"
			await client.send_message(message.channel, msg)
		else:
			user = message.author.id
			#if user == '368485403340046336':
			#	msg = 'No'
			#	await client.send_message(message.channel, msg)
			#else:
			val = message.content.split(" ", 1)
			if len(val) <= 1:
				msg = "To assign your friend code, use the command '!setfc XXXX-XXXX-XXXX'"
				await client.send_message(message.channel, msg)
			else:
				val = val[1]
				cursor.execute(fc_select_str, (user,))
				result = cursor.fetchone()
				if result == None:
					cursor.execute(fc_insert_str, (user, val))
				else:
					cursor.execute(fc_update_str, (val, user))
				connection.commit()
				msg = 'Friend code set to ' + val
				await client.send_message(message.channel, msg)
	if startswith(message.content, '!getfc'):
		ment = message.mentions
		user = message.author.id if len(ment) == 0 else ment[0].id
		username = message.author.name if len(ment) == 0 else ment[0].name
		cursor.execute(fc_select_str, (user,))
		result = cursor.fetchone()
		if result == None:
			msg = username + " does not have a registered friend code. Use the !setfc [code] command to register a friend code."
			await client.send_message(message.channel, msg)
		else:
			msg = result[0]
			await client.send_message(message.channel, msg)
	if startswith(message.content, '!setreddit'):
		user = message.author.id
		val = message.content.split(" ")
		if len(val) <= 1:
			msg = "To assign your reddit usernames, use the command '!setreddit redditusername'"
			await client.send_message(message.channel, msg)
		else:
			val = val[1]
			cursor.execute(reddit_select_str, (user,))
			result = cursor.fetchone()
			if result == None:
				cursor.execute(reddit_insert_str, (user, val))
			else:
				cursor.execute(reddit_update_str, (val, user))
			connection.commit()
			msg = 'Reddit username set to ' + val
			await client.send_message(message.channel, msg)
	if startswith(message.content, '!getreddit'):
		ment = message.mentions
		val = message.content.split(" ",1)
		if len(ment) > 0 or len(val) == 1:
			user = message.author.id if len(ment) == 0 else ment[0].id
			username = message.author.name if len(ment) == 0 else ment[0].name
			cursor.execute(reddit_select_str, (user,))
			result = cursor.fetchone()
			if result == None:
				msg = username + " does not have a registered reddit username. Use the !setreddit redditusername command to register a reddit username."
				await client.send_message(message.channel, msg)
			else:
				msg = result[0]
		else:
			name = val[1]
			cursor.execute(reddit_select_name_str, (name,))
			result = cursor.fetchone()
			if result == None:
				msg = 'There is no one on this server with the reddit username ' + name
			else:
				msg = discordname( discord_user( result[0] ) )
		await client.send_message(message.channel, msg)
	if startswith(message.content, '!deletereddit'):
		if len(message.author.roles) > 1:
			ment = message.mentions
			if len(ment) < 1:
				msg = 'Provide a user to delete'
			else:
				user = ment[0].id
				cursor.execute(reddit_delete_str, (user,))
				connection.commit()
				msg = 'Reddit username of ' + ment[0].name + ' deleted'
			await client.send_message(message.channel, msg)
	if startswith(message.content, '!addtsv') or startswith(message.content, '!settsv') or startswith(message.content, '!setsv'):
		if len(message.mentions) > 0:
			msg = "Please do not include user tags in your TSV"
			await client.send_message(message.channel, msg)
		else:
			user = message.author.id
			val = message.content.split(" ", 2)
			if len(val) <= 2:
				msg = "To assign your tsv, use the command '!addtsv XXXX Game'"
				await client.send_message(message.channel, msg)
			else:
				tsv = val[1]
				game = val[2]
				if len(tsv) != 4 or not tsv.isdigit():
					msg = "Your tsv must be exactly 4 numbers"
					await client.send_message(message.channel, msg)
				else:
					cursor.execute(tsv_insert_str, (user, tsv, game))
					connection.commit()
					msg = 'Added ' + tsv + ' for ' + game
					await client.send_message(message.channel, msg)
	if startswith(message.content, '!deletetsv'):
		user = message.author.id
		val = message.content.split(" ", 1)
		if len(val) <= 1:
			msg = "Provde a tsv to delete"
			await client.send_message(message.channel, msg)
		else:
			tsv = val[1]
			if len(tsv) != 4:
				msg = "A tsv must be exactly 4 characters"
				await client.send_message(message.channel, msg)
			else:
				cursor.execute(tsv_delete_str, (user, tsv))
				connection.commit()
				msg = 'Deleted ' + tsv
				await client.send_message(message.channel, msg)
	if startswith(message.content, '!gettsv') or startswith(message.content, '!getsv'):
		user = message.author.id
		val = message.content.split(" ", 1)
		if len(val) == 1:
			cursor.execute(tsv_select_str, (user,))
			results = cursor.fetchall()
			if results == None or len(results) == 0:
				msg = "You don't have any registered tsvs"
				await client.send_message(message.channel, msg)
			else:
				msg = ''
				for result in results:
					msg += result[0] + ' ' + result[1] + '\n'
				await client.send_message(message.channel, msg)
		else:
			tsv = val[1]
			if len(tsv) != 4:
				msg = 'A tsv must be exactly 4 characters'
				await client.send_message(message.channel, msg)
			else:
				cursor.execute(tsv_request_str, (tsv,))
				results = cursor.fetchall()
				if results == None or len(results) == 0:
					msg = "No one has that tsv"
					await client.send_message(message.channel, msg)
				else:
					msg = ''
					server = message.server
					for result in results:
						member = server.get_member(result[0])
						msg += discordname(member) + ' has that tsv in the game ' + result[1] + '\n'
					await client.send_message(message.channel, msg)
	if startswith(message.content, '!create'):
		name = message.content.split(" ", 1)[1]
		msg = ''
		if wiki_exists(name):
			msg = name + ' already has a wiki page'
		else:
			create_wiki(name)
			msg = 'Created wiki page for ' + name
		await client.send_message(message.channel, msg)
	if startswith(message.content, '!badge') or startswith(message.content, '!bagde'):
		if len(message.author.roles) > 1:
			(foo, name, badge) = message.content.split(" ", 2)
			if len(message.mentions) > 0:
				name = redditname( message.mentions[0].id )
			badge = badge.lower()
			msg = ''
			if name == None:
				msg = message.mentions[0].name + ' does not have a registered reddit name'
			elif not wiki_exists(name):
				msg = name + ' does not have a reigstered league pass'
			elif not isbadge(badge):
				msg = badge + ' is not a valid badge'
			elif flair_post(name, badge, 'Victory'):
				add_badge(name, badge)
				msg = 'Assigned badge ' + badge + ' to ' + name
			else:
				msg = name + ' does not have a matching challenge'
			print(msg)
			await client.send_message(message.channel, msg)
	if startswith(message.content, '!loss') or startswith(message.content, '!defeat'):
		if len(message.author.roles) > 1:
			(foo, name, badge) = message.content.split(" ", 2)
			if len(message.mentions) > 0:
				name = redditname( message.mentions[0].id )
			badge = badge.lower()
			msg = ''
			if name == None:
				msg = message.mentions[0].name + ' does not have a registered reddit name'
			elif not wiki_exists(name):
				msg = name + ' does not have a reigstered league pass'
			elif not isbadge(badge):
				msg = badge + ' is not a valid badge'
			elif flair_post(name, badge, 'Defeat'):
				msg = 'Assigned loss to ' + name
			else:
				msg = name + ' does not have a matching challenge'
			print(msg)
			await client.send_message(message.channel, msg)
	if startswith(message.content, '!retry') or startswith(message.content, '!rematch'):
		if len(message.author.roles) > 1:
			(foo, name) = message.content.split(" ", 1)
			if len(message.mentions) > 0:
				name = redditname( message.mentions[0].id )
			msg = ''
			if name == None:
				msg = message.mentions[0].name + ' does not have a registered reddit name'
			elif approve_rematch(name):
				msg = 'Retry approved for ' + name
			else:
				msg = name + ' does not have a pending retry'
			print(msg)
			await client.send_message(message.channel, msg)
	if startswith(message.content, '!cancel'):
		if len(message.author.roles) > 1:
			(foo, name, badge) = message.content.split(" ", 2)
			if len(message.mentions) > 0:
				name = redditname( message.mentions[0].id )
			msg = ''
			if name == None:
				msg = message.mentions[0].name + ' does not have a registered reddit name'
			elif not isbadge(badge):
				msg = badge + ' is not a valid badge'
			elif cancel_challenge(name, badge):
				msg = 'Challenge canceled for ' + name
			else:
				msg = name + ' does not have an open challenge'
			print(msg)
			await client.send_message(message.channel, msg)
	if startswith(message.content, '!getlp'):
		val = message.content.split(" ", 1)
		msg = ''
		if len(val) < 2:
			name = redditname(message.author.id)
		elif len(message.mentions) == 0:
			name = message.content.split(" ")[1]
		else:
			name = redditname(message.mentions[0].id)
		if name == None:
			msg = message.mentions[0].name + ' does not have a registered reddit name'
		else:
			msg = get_league_pass(name)
		await client.send_message(message.channel, msg)
	if startswith(message.content, '!getbadge') or startswith(message.content, '!getbagde'):
		val = message.content.split(" ")
		msg = ''
		if len(val) < 2:
			name = redditname(message.author.id)
		elif len(message.mentions) == 0:
			name = message.content.split(" ")[1]
		else:
			name = redditname(message.mentions[0].id)
		if name == None:
			msg = message.mentions[0].name + ' does not have a registered reddit name'
		else:
			msg = get_badges(name)
		await client.send_message(message.channel, msg)
	if startswith(message.content, '!pyramid'):
		if len(message.author.roles) > 1:
			msg = pyramid()
			await client.send_message(message.channel, msg)
	if len(message.mentions) == 0 and re.search(tag_err_reg, message.content) != None:
		m = re.search(tag_err_reg, message.content)
		user = discord.utils.get(message.server.members, name=m.group(1), discriminator=m.group(2))
		if user != None:
			msg = user.mention
		else:
			msg = 'There is no user matching that failed tag'
		await client.send_message(message.channel, msg)

async def reddit_crawl():
	await client.wait_until_ready()
	while not client.is_closed:
		members = process()
		for m, url in members:
			await client.send_message(m, 'You have a challenge!\n'+url)
		await asyncio.sleep(120)

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	await client.change_presence(game=discord.Game(name='!help'))

client.loop.create_task(reddit_crawl())
client.run('MzY4MjA3OTA4MjU4NzA5NTA4.DOrIoQ.LmWkhuK1_5-Qk12qet0pE7_ZtU0')
