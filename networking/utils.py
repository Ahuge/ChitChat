BROADCAST_ADDR = "255.255.255.255"
BROADCAST_PORT = 10000


class ChatAppMessageError(Exception):
    pass


class InvalidMessageFormatError(ChatAppMessageError):
    pass


class InvalidMessageVersionError(ChatAppMessageError):
    pass


class MessageType(object):
    ehlo = 0
    chat = 1

    types = [ehlo, chat]


class Message(object):
    __version__ = "1.0.0"
    __schema__ = "ChatAppMessage"
    NULL_PAD = "\0"
    SEP = ":"
    HEADER_SEP = "|"
    HEADER_LENGTH = 150

    def __init__(self, user, hostname, message_type, message=""):
        super(Message, self).__init__()
        self.user = user
        self.hostname = hostname
        self.message_type = message_type
        self.message = message

    @staticmethod
    def pad(msg, length):
        if length < len(msg):
            raise ValueError("Could not pad. Header is too long!")
        return msg.rjust(length, Message.NULL_PAD)

    @classmethod
    def version_schema(cls):
        return Message.SEP.join([Message.__schema__, Message.__version__])

    def to_str(self):
        author = self.SEP.join([self.user, self.hostname])
        version = self.version_schema()
        header = self.HEADER_SEP.join([
                version, str(self.message_type), author
        ])
        return Message.pad(header, Message.HEADER_LENGTH) + self.message

    @classmethod
    def _header_version_check(cls, header):
        if header != Message.version_schema():
            raise InvalidMessageVersionError(
                "Received a message from a different version of the "
                "message schema. Expected version \"{schema\". "
                "Received \"{recv}\"".format(
                    schema=Message.version_schema(),
                    recv=header
                )
            )

    @classmethod
    def _type_check(cls, _type):
        if _type not in MessageType.types:
            raise InvalidMessageFormatError("Unknown Message Type: %s" % _type)

    @classmethod
    def from_str(cls, msg):
        try:
            header = msg[:Message.HEADER_LENGTH]
            message = msg[Message.HEADER_LENGTH:]
            header, _type, author = header.split(cls.HEADER_SEP, 2)

            # May raise InvalidMessageVersionError
            Message._header_version_check(header)
            # May raise InvalidMessageFormatError
            Message._type_check(header)

            author, _ = author.split(Message.NULL_PAD)
            user, hostname = author.split(cls.SEP, 1)
            return Message(
                user=user,
                hostname=hostname,
                message_type=_type,
                message=message
            )
        except ValueError:
            raise InvalidMessageFormatError(
                "Message \"{msg}\" is not a valid format.".format(msg=msg)
            )


