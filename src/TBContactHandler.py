class RubricaHandler:
    def __init__ ( self, filename='/Rubrica.txt' ):
        self.filename = filename
    def updateContact ( self, _contact, registered='1' ):
        contactList = []
        contactList = self.readContactList ( False )
        contactList.remove ( _contact )
        _contact['registered'] = registered
        contactList.append(_contact)
        file = open(self.filename, 'w')
        for item in contactList:
            file.write(item['phone_number'] + ',' + item['name'] + ',' + item['registered'] + '\n')
        file.close ( );
    # first step: read the list of contact that are allow to interact with bot
    # file scheme: phone_number, name surname, registered
    def readContactList ( self, only_not_recorded=True ):
        try:
            file = open ( self.filename, 'r' )
        except ( ValueError ):
            print ( "Exception: " + ValueError )
            return -1
        _contactList = []
        for line in file:
            if line.startswith ( '#' ) == False:
                fields = [field.strip() for field in line.split(',')]
                contact = { 'phone_number':fields[0], 'name':fields[1], 'registered':fields[2]}
                # if contact isn't registered yet add it to contactList
                if only_not_recorded == True and contact['registered'] == '0':
                    _contactList.append(contact)
                elif only_not_recorded == False:
                    _contactList.append(contact)
        file.close ( )
        return _contactList

class UserDataHandler:
    def __init__ ( self, filename='/data.txt' ):
        self.filename = filename
    # this function read the list of contact that are need to be questioned
    def readBroadcastList ( self ):
        try:
            file = open( self.filename, 'r+' )
        except ( ValueError ):
            print ( "Exception: " + ValueError )
            return -1
        broadcastList = []
        for line in file:
            fields = [field.strip() for field in line.split(',')]
            broadcastList.append ( {'chat_id': fields[0], 'phone_number':fields[1], 'name':fields[2]})
        file.close( )
        return broadcastList
    # this function save a new contact info
    def saveInfoContact ( self, infoContact ):
        file = open(self.filename, 'a+')
        file.write ( str(infoContact['chat_id']) + ',' + str(infoContact['phone_number']) + ',' + infoContact['name'] + '\n')
        file.close( )
