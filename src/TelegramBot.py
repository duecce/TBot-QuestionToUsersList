# token: get it from Bot Father
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from TBContactHandler import RubricaHandler, UserDataHandler
import datetime, copy

from TOKEN import BOT_TOKEN

# to init a new user is necessary to check the mobile number
# user is allow to interact with bot only if its mobile number will be recognized
def start(update, context):
    if context.bot_data['ALL_CONTACT_REGISTERED'] == 'FALSE':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hi from bot, this bot recognize you by your phone number, enter it: ")
        context.user_data['state'] = 'GET_PHONE_NUMBER'

def messageHandler(update, context):
    if context.user_data['state'] == 'GET_PHONE_NUMBER':
        # check if phone number is in rubrica
        contact = list(filter(lambda _contact: _contact['phone_number'] == update.message.text, context.bot_data['contactList']))
        if len(contact) == 1:
            context.bot.send_message ( chat_id=update.effective_chat.id, text=contact[0]['name'] + ' welcome!' )
            if contact[0]['registered'] == '0':
                newContact = copy.deepcopy(contact[0])
                rubrica = RubricaHandler()
                broadcastList = UserDataHandler()
                rubrica.updateContact(newContact)
                print ( '- Rubrica: ' + newContact['name'] + ' registered')
                context.bot_data['broadcastList'].append ( {'chat_id':str(update.effective_chat.id), 'phone_number':contact[0]['phone_number'], 'name':contact[0]['name']} )
                broadcastList.saveInfoContact ( {'chat_id':update.effective_chat.id, 'phone_number':contact[0]['phone_number'], 'name':contact[0]['name']})
                context.bot_data['contactList'].remove(contact[0]) # remove contact from contactList
                if len(context.bot_data['contactList']) == 0 :
                    context.bot_data['ALL_CONTACT_REGISTERED'] = 'TRUE'
                    print ( '- Rubrica: all contact registered' )
            else:
                print ( '- Rubrica: contact already registered')
        else:
            print ( '- Rubrica: contact number not found' )
            context.bot.send_message ( chat_id=update.effective_chat.id, text='Phone number not found' )
        context.user_data['state'] = 'IN_GAME'

# send question to all contact registered
def dailyQuestion ( context ):
    print ( 'Daily question, or daily message, what you want\n')
    for item in context.bot_data['broadcastList']:
        print(item)
    for item in context.bot_data['broadcastList']:
        chat_id = item['chat_id']
        # Question header
        context.bot.send_message(chat_id, text= "Hi " + item['name'] + ", this is an example of daily question" )
        # Question 1 with InlineKeyboard
        keyboard = [[InlineKeyboardButton("Button 0", callback_data='0')], [InlineKeyboardButton("Button 1", callback_data='1')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id, text="Question?", reply_markup=reply_markup)
        # goodbye line
        context.bot.send_message(chat_id, text="Goodbye! See you next time")

def button_selected ( update, context ):
    query = update.callback_query
    query.answer()
    query.edit_message_text ( text='Change button text' )
    if query.data == '0':
        context.bot.send_message ( chat_id=update.effective_chat.id, text='Button 0 selected, OMG, do something here')
    elif query.data == '1':
        context.bot.send_message (chat_id=update.effective_chat.id, text='Button 1 selected, and now?' )

def main():
    # Step 1: parsing contact file
    rubrica = RubricaHandler()
    broadcastList = UserDataHandler()
    contactList = rubrica.readContactList()
    broadcastList = broadcastList.readBroadcastList ( )
    if ( broadcastList == -1 ):
        print ( "broadcastList.readBroadcastList() error")
        exit(0)
    # Step 2: create bot
    updater = Updater ( token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start)) # command recv: /start 
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), messageHandler))
    dp.add_handler(CallbackQueryHandler(button_selected))
    updater.job_queue.run_daily(dailyQuestion, datetime.time(hour=18-2, minute=24), days=(0,1,2,3,4,5,6)) # UCT Time is (Rome time - 2h)
    if len(broadcastList) > 0:
        dp.bot_data['broadcastList'] = broadcastList
        print ( '- Broadcast list: ' + str(len(broadcastList)) + ' users to contact' )
    else:
        dp.bot_data['broadcastList'] = []
    # store contactList in bot_data variabile
    if len(contactList) > 0:
        dp.bot_data['contactList'] = contactList
        dp.bot_data['ALL_CONTACT_REGISTERED'] = 'FALSE'
        print ('- Rubrica: ' + str(len(contactList)) + ' people has to be registered')
    else:
        dp.bot_data['ALL_CONTACT_REGISTERED'] = 'TRUE'
        print ( '- Rubrica: all contacts already registered' )

    # now we can run our bot (bot run on another thread so we can continue on this flow) and wait for a message 
    print ( "Bot running..." )
    updater.start_polling()


if __name__ == '__main__':
    main()
