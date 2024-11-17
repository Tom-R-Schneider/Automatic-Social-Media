from enum import Enum
class VIDEO_TYPE_DETAILS:
    def __init__(self, id_suffix, upload_time, upload_day):
        self.ID_SUFFIX = id_suffix
        self.UPLOAD_TIME = upload_time
        self.UPLOAD_DAY = upload_day
class VIDEO_TYPE:
    WORD = VIDEO_TYPE_DETAILS('word', '19:00:00', 0)


class WORD_TYPE(Enum):   
    NOUN = "Substantiv"
    ADJECTIVE = "Adjektiv"
    VERB = "Verb"