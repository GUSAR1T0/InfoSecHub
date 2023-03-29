class DatabaseOptions:
    def __init__(self, **kwargs):
        self.__host = kwargs['host']
        self.__port = kwargs['port']
        self.__name = kwargs['name']
        self.__user = kwargs['user']
        self.__password = kwargs['password']

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def name(self):
        return self.__name

    @property
    def user(self):
        return self.__user

    @property
    def password(self):
        return self.__password
