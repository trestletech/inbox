import re
from flanker import mime

def uniq(alist):
        set = {}
        return [set.setdefault(e,e) for e in alist if e not in set.keys()]

msgid_pat = re.compile('<([^>]+)>')

class JWZ_Message(object):
    def __init__(self, message): 
        self.parsed = mime.from_string(message)
        self.headers = self.parsed.headers

        # Used by JWZ Algorithm
        self._message = message
        self._message_id = self.headers.get('Message-ID')
        self._references = None
        self._subject = self.headers.get('Subject', 'No Subject')

    @property
    def message(self):
        return self._message

    @property
    def message_id(self):
        if self._message_id is None:
            print "headers = ", self.headers

            raise ValueError, 'Message does not contain a Message-ID header'

        return self._message_id

    @property
    def references(self):
        if self._references is not None:
            return self._references

        # Get list of unique message IDs from the References: header  
        refs = self.headers.get('References', '')
        self._references = msgid_pat.findall(refs)
        self._references = uniq(self._references)

        # Get In-Reply-To: header and add it to references                                                                                                                                                 
        in_reply_to = self.headers.get('In-Reply-To', '')
        matches = msgid_pat.search(in_reply_to)
        if matches:
            msg_id = matches.group(1)
            if msg_id not in self._references:
                self._references.append(msg_id)

        return self._references

    @property
    def subject(self):
        return self._subject

    def __repr__ (self):
        return '<%s: %r>' % (self.__class__.__name__, self._message_id)