from header import *

def matching_flairs(flair):
  if flair in singles_css:
    return singles_css
  if flair in doubles_css:
    return doubles_css

def incompatible_challenges(challenge1, challenge2):
  flair1 = challenge1.link_flair_text
  flair2 = challenge2.link_flair_text
  if flair1 == s_e4champ_flair and flair2 == d_gym_flair:
    return False
  if flair2 == s_e4champ_flair and flair1 == d_gym_flair:
    return False
  return flair2 not in finished_flairs and flair1 not in finished_flairs

def process():
  members = []
  for submission in subreddit.new(limit=5):
    title = submission.title.lower()
    author = submission.author

    # First check that the submission is a challenge
    if not ischallenge(title) or datetime.datetime.utcfromtimestamp(submission.created_utc) < season_start_date:
      continue
    # Get the list of challenges, sorted by time
    challenges = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_css_class in matching_flairs(submission.link_flair_css_class), author.submissions.new(limit=10)))
    challenges.sort(key=lambda x: x.created_utc, reverse=True)

    # Check if the submission was already approved by a moderator
    if submission.approved == False:
      # Check if this challenge is less than 20 hours from the previous challenge
      if len(challenges) > 1 and challenges.index(submission) < len(challenges) - 1:
        time_dif = submission.created_utc - challenges[challenges.index(submission)+1].created_utc
        if time_dif < 72000:
          submission.reply(time_limit_message)
          submission.mod.flair(text='Removed', css_class='')
          submission.mod.remove()
          print('Removed challenge of ' + author.name + ' for breaking the 20 hour rule')
          continue

        if challenges[challenges.index(submission)+1].link_flair_text not in finished_flairs:
          submission.reply(multi_challenge_message)
          submission.mod.flair(text='Removed', css_class='')
          submission.mod.remove()
          print('Removed challenge of ' + author.name + ' for breaking the one challenge at a time rule')
          continue
    # Get the most recent league pass from the author
    cards = list(filter(lambda x: x.subreddit == subreddit and x.link_flair_text == 'League Pass' and replied(x)>0 and season_start_date < datetime.datetime.utcfromtimestamp(x.created_utc), author.submissions.new()))
    if len(cards) == 0:
      submission.reply(league_pass_message)
      submission.mod.flair(text='Removed', css_class='')
      submission.mod.remove()
      print('Removed challenge of ' + author.name + ' as they did not have a League Pass')
      continue
    cont = True
    for comment in submission.comments:
      if comment.author == reddit.user.me() and comment.body.find('Link') != -1:
        cont = False
    if cont:
      leader = tag_leader(submission)
      reply = league_pass_link.format(cards[0].url)
      if leader == None:
        reply += no_leader_message
      else:
        reply += '/u/'+leader
        discorduser = redditname_to_discorduser(leader)
        members.append((discorduser, submission.url))
      submission.reply(reply)
      print('League Pass link attached to latest challenge from ' + author.name)

  for comment in subreddit.comments(limit=15):
    if comment.body.startswith('Approve') or comment.body.startswith('approve'):
      parent = comment.parent()
      if '[lp]' in parent.title.lower() and replied(parent)==0:
        create_wiki(parent.author.name)
        parent.reply(badgesheet_message.format(parent.author.name))
        parent.mod.approve()

  return members

@client.event
async def on_ready():
  await client.wait_until_ready()
  members = process()
  for m, url in members:
    await client.send_message(m , 'You have a challenge!\n' + url)

client.run('MzY4MjA3OTA4MjU4NzA5NTA4.DlZnfQ.7mAb9yTYOdT-w2NYl6ffd1uskBc')
