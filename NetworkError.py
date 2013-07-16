class NetworkError(RuntimeError):

    def __init__(self, args, msg):
        self.args = args
        self.msg = msg
