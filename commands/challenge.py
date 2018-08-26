#imports all of the needed info from header.py

from header import *

#async def defines the 'challenge' method whilst 'message' retrives info like who sent the message and the chat it was sent to
#args gets the argument like the badge kentioned kn the message 
#the method then retrives the users sent information as well as looking for thier league pass in the data base

async def challenge(message, args):
  userid = message.author.id
  cursor.execute('SELECT * FROM betalp WHERE id=?', (userid,))
  result = cursor.fetchone()
  
  #the method then checks the result. if the user does not have a league pass it displays the message
  
  if result == None:
    msg = 'You do not have a league pass. Create one with !setlp'
  
  #if the user does have a registered league pass it then checks the data base for an open challenge
  
  else:
    cursor.execute('SELECT badge FROM betachallenge WHERE id=? AND status="O"', (userid,))
    result = cursor.fetchone()
    
    #if the method finds a challenge it displays what challenge is currently open with a message
    
    if result != None:
      msg = 'You have an open ' + result[0] + ' challenge'
   
  #if the length of the message after !challenge is 0 it displays this message
  
    elif len(args) == 0:
      msg = 'You do not have an active challenge'
    
    #if there is a valid badge argument after !challenge and inserts it into the data base
    
    elif issingles(args):
      cursor.execute('INSERT INTO betachallenge (id, time, badge, status) VALUES (?,?,?,"O")', (userid, int(message.timestamp.timestamp()), args))
      connection.commit()
      msg = 'Challenge Submitted!'
    
    #if there is an argument after !challenge that isnt a valid badge it gives this message
    
    else:
      msg = args + ' is not a valid badge'
  await client.send_message(message.channel, msg)
