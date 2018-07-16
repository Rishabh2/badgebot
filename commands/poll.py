from header import *
async def poll(message, args):
  global optiona
  global optionb
  global optionc
  global optiond
  global a
  global b
  global c
  global d
  if message.content.lower().startswith("!"):
    splt = args.split("|", maxsplit=5)
    if splt[0] == "create":
      optiona = "null"
      optionb = "null"
      optionc = "null"
      optiond = "null"
      a = 0
      b = 0
      c = 0
      d = 0
      if len(splt) < 3:
        await client.send_message(message.channel, "Please include 2-4 options")
      elif len(splt) == 3:
        optiona = splt[1]
        a = 0
        optionb = splt[2]
        b = 0
        await client.send_message(message.channel, "A poll was created with the options: " + optiona + ", " + optionb)
      elif len(splt) == 4:
        optiona = splt[1]
        a = 0
        optionb = splt[2]
        b = 0
        optionc = splt[3]
        c = 0
        await client.send_message(message.channel, "A poll was created with the options: " + optiona + ", " + optionb + ", " + optionc)
      elif len(splt) == 5:
        optiona = splt[1]
        a = 0
        optionb = splt[2]
        b = 0
        optionc = splt[3]
        c = 0
        optiond = splt[4]
        d = 0
        await client.send_message(message.channel, "A poll was created with the options: " + optiona + ", " + optionb + ", " + optionc + ", " + optiond)
    elif splt[0] == "end":
      if optiona != "null":
        await client.send_message(message.channel, optiona + ":" + str(a))
      if optionb != "null":
        await client.send_message(message.channel, optionb + ":" + str(b))
      if optionc != "null":
        await client.send_message(message.channel, optionc + ":" + str(c))
      if optiond != "null":
        await client.send_message(message.channel, optiond + ":" + str(d))
      optiona = "null"
      optionb = "null"
      optionc = "null"
      optiond = "null"
      a = 0
      b = 0
      c = 0
      d = 0
    elif splt[0] == "vote":
      if splt[1] == optiona:
        a = a + 1
      if splt[1] == optionb:
        b = b + 1
      if splt[1] == optionc:
        c = c + 1
      if splt[1] == optiond:
        d = d + 1
      await client.send_message(message.channel, "Your vote has been cast")
    elif len(args) == 0:
      await client.send_message(message.channel, "To create a poll use: `!poll|create|option 1|option 2` To end a poll and see the results use `!poll|end` and to vote on an existing poll use `!poll|vote|[your option]`")
