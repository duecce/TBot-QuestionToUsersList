# TBot-QuestionToUsersList
This _simple_ Python software implements a Telegram Bot that _sends a daily question to a restricted (and registered also) list of contacts_.
Software need to have one file, in source is called: Rubrica.txt, contains a list of users

### Example of Rubrica.txt
- 44422334455, John Ally, 0
- 3334445588, Allison Park, 1
- 2223344224, Claude Smit, 0

Rubrica: file format explained

_phone_number_, _name surname_, _0/1_(0 if user is not registered, 1 if is registered)

When a user will be registered, in data file (called data.txt in source) we can find chat_id associated to that user, TBot use chat_id to send the question to a specified user.

In the end:
- Rubrica.txt have to be written by user
- Data.txt will be written by software

#### This image should clear all your doubts (MSPaint <3)
![Bot communication scheme](/imgs/scheme.png)
