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
        self.message = message

        self.set_message_id()
        self.set_references()
        self.set_subject()

    def set_message_id(self):
        self.message_id = msgid_pat.search(self.headers.get('Message-ID', ''))

        if self.message_id is None:
            raise ValueError, 'Message does not contain a Message-ID header'

        self.message_id = self.message_id.group(1)

    def set_references(self):
        # Get list of unique message IDs from the References: header  
        refs = self.headers.get('References', '')
        self.references = msgid_pat.findall(refs)
        self.references = uniq(self.references)

        # Get In-Reply-To: header and add it to references                                                                                                                                                 
        in_reply_to = self.headers.get('In-Reply-To', '')
        matches = msgid_pat.search(in_reply_to)
        if matches:
            msg_id = matches.group(1)
            if msg_id not in self.references:
                self.references.append(msg_id)

    def set_subject(self):
        self.subject = self.headers.get('Subject', 'No Subject')

    def __repr__ (self):
        return '<%s: %r>' % (self.__class__.__name__, self.message_id)
