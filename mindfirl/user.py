from mutil import r
#from bson.objectid import ObjectId


class User(object):
    def __init__(self, username):
        self.username = username
        self.id = username


    @staticmethod
    def get(mongo, uid):
        user = mongo.db.users.find_one({'username': uid })
        if user:
            return User(uid)
        return None


    __hash__ = object.__hash__


    @property
    def is_active(self):
        return True


    @property
    def is_authenticated(self):
        return True


    @property
    def is_anonymous(self):
        return False


    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')


    def __eq__(self, other):
        '''
        Checks the equality of two `User` objects using `get_id`.
        '''
        if isinstance(other, User):
            return self.get_id() == other.get_id()
        return NotImplemented


    def __ne__(self, other):
        '''
        Checks the inequality of two `User` objects using `get_id`.
        '''
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal


def auth_user(mongo, data):
    username = data['name']
    password = data['pwd']
    user = mongo.db.users.find_one({'username': username})
    if not user:
        return None

    if password != user['password']:
        return None
    return User(username)


def register_user(mongo, data):
    username = data['name']
    password = data['pwd']
    user_exist = mongo.db.users.find_one({'username': username})
    if user_exist:
        return None
    users = mongo.db.users
    user_id = users.insert({'username': username, 'password': password})
    #print("user id: " + str(user_id))
    return True



