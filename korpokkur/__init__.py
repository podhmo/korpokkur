# -*- coding:utf-8 -*-
class FileConflict(Exception):
    def __init__(self, path, *args, **kwargs):
        self.path = path
        super(FileConflict, self).__init__(*args, **kwargs)


class ScaffoldException(Exception):
    pass

class NotSupportExtension(ScaffoldException):
    pass
class ScaffoldNotFound(ScaffoldException):
    pass
