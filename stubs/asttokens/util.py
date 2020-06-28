import collections


class Token(collections.namedtuple('Token', 'type string start end line index startpos endpos')):
    ...
