from header import *
async def draft(message, args):
  if haspermission(message.author):
    result = service.spreadsheets().values().get(spreadsheetId=TEMPLATE_ID, range='Tiers', majorDimension='COLUMNS').execute()
    values = result.get('values', [])
    found = False
    for i, tier in enumerate(values):
      if args in tier:
        msg = tier[0] + ' Cost: ' + values[i+1][0]
        found = True

        cellRow = tier.index(args)

        strike = [{'updateCells':{
          'rows': [{
            'values':[{
              'userEnteredFormat': {
                'textFormat':{
                  'strikethrough': True
                  }
                }
              }]
            }],
          'fields': 'userEnteredFormat.textFormat.strikethrough',
          'range': {
            'sheetId': 161954080,
            'startRowIndex': cellRow,
            'endRowIndex': cellRow+1,
            'startColumnIndex': i,
            'endColumnIndex': i+1
            }

          }}]
        body = {'requests':strike}
        response = service.spreadsheets().batchUpdate(spreadsheetId=TEMPLATE_ID, body=body).execute()
    if not found:
      msg = 'This is not a pokemon you can draft'
  else:
    msg = no_permissions_message
  await client.send_message(message.channel, msg)
