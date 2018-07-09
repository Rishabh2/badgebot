from header import *
async def leaks(message, args):
  if haspermissions(message.author.id):
    roles = message.server.roles
    for role in roles:
      if role.name=='Leaks':
        leak_role=role
    for member in get_all_members():
      if any([role == leak_role for role in member.roles]):
        salvation = random.randint(1,2)
        if salvation == 1:
          await client.remove_roles(member, leak_role)
          await client.send_message(member, "Hear me, and rejoice. You are about to die at the hand of the children of H2nos. Be thankful, that your meaningless lives are now contributed to the balance. Soon, you will have the great privilege of being saved by the great titan. Some of you may think this is suffering... no! It is salvation. The universal scales... tip toward balance because of your sacrifice. Smile... for even in death, you will have become children of H2nos!")
