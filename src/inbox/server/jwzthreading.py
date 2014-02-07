"""jwzthreading.py

Contains an implementation of an algorithm for threading mail
messages, as described at http://www.jwz.org/doc/threading.html.

"""

# This code is under a BSD-style license; see the LICENSE file for details.
# __revision__ = "$Id: jwzthreading.py,v 1.2 2003/03/26 13:45:11 akuchling Exp $"

import re

restrip_pat = re.compile("""(                                                                                                                                                                          
  (Re(\[\d+\])?:) | (\[ [^]]+ \])                                                                                                                                                                      
\s*)+                                                                                                                                                                                                  
""", re.I | re.VERBOSE)

__all__ = ['Message', 'thread']

class Container:
    __slots__ = ['message', 'parent', 'children', 'id']
    def __init__ (self):
        self.message = self.parent = None
        self.children = []

    def __repr__ (self):
        return '<%s %x: %r>' % (self.__class__.__name__, id(self),
            self.message)
    
    def is_dummy (self):
        return self.message is None

    def add_child (self, child):
        if child.parent:
            child.parent.remove_child(child)
        self.children.append(child)
        child.parent = self
        
    def remove_child (self, child):
        self.children.remove(child)
        child.parent = None

    def has_descendant (self, ctr):
        if self is ctr:
            return True
        for c in self.children:
            if c is ctr:
                return True
            elif c.has_descendant(ctr):
                return True
        return False

def prune_container (container):
    """prune_container(container:Container) : [Container]
    Recursively prune a tree of containers, as described in step 4
    of the algorithm.  Returns a list of the children that should replace
    this container.
    """

    # Prune children, assembling a new list of children
    new_children = []
    for ctr in container.children[:]:
        L = prune_container(ctr)
        new_children.extend(L)
        container.remove_child(ctr)

    for c in new_children:
        container.add_child(c)

    if (container.message is None and
        len(container.children) == 0):
        # 4.A: nuke empty containers
        return []
    elif (container.message is None and
          (len(container.children)==1 or
           container.parent is not None)):
        # 4.B: promote children
        L = container.children[:]
        for c in L:
            container.remove_child(c)
        return L
    else:
        # Leave this node in place
        return [container]
        
def thread (msglist):
    """thread([JWZ_Message]) : {string:Container}

    The main threading function.  This takes a list of Message
    objects, and returns a dictionary mapping subjects to Containers.
    Containers are trees, with the .children attribute containing a
    list of subtrees, so callers can then sort children by date or
    poster or whatever.
    """
    
    id_table = {}
    for msg in msglist:
        # 1A
        this_container = id_table.get(msg.message_id, None)
        if this_container is not None:
            this_container.message = msg
        else:
            this_container = Container()
            this_container.message = msg
            id_table[msg.message_id] = this_container

        # 1B
        prev = None
        for ref in msg.references:
            container = id_table.get(ref, None)
            if container is None:
                container = Container()
                container.message_id = ref

                id_table[ref] = container

            if (prev is not None):
                # Don't add link if it would create a loop
                if container is this_container:
                    continue
                if container.has_descendant(prev):
                    continue
                prev.add_child(container)

            prev = container

        if prev is not None:
            prev.add_child(this_container)

    # 2. Find root set
    root_set = [container for container in id_table.values()
                if container.parent is None]

    # 3. Delete id_table
    del id_table

    # 4. Prune empty containers
    for container in root_set:
        assert container.parent == None
        
    new_root_set = []
    for container in root_set:
        L = prune_container(container)
        new_root_set.extend(L)

    root_set = new_root_set
        
    # 5AB. Group root set by subject
    subject_table = {}
    for container in root_set:
        if container.message:
            subj = container.message.subject
        else:
            subj = container.children[0].message.subject

        subj = restrip_pat.sub('', subj)
        if subj == "":
            continue

        existing = subject_table.get(subj, None)
        if (existing is None or
            (existing.message is not None and
             container.message is None) or
            (existing.message is not None and
             container.message is not None and 
             len(existing.message.subject) > len(container.message.subject))):
            subject_table[subj] = container

    # 5C
    for container in root_set:
        if container.message:
            subj = container.message.subject
        else:
            subj = container.children[0].message.subject

        subj = restrip_pat.sub('', subj)
        ctr = subject_table.get(subj)
        if ctr is None or ctr is container:
            continue
        if ctr.is_dummy() and container.is_dummy():
            for c in ctr.children:
                container.add_child(c)
        elif ctr.is_dummy() or container.is_dummy():
            if ctr.is_dummy():
                ctr.add_child(container)
            else:
                container.add_child(ctr)
        elif len(ctr.message.subject) < len(container.message.subject):
            # ctr has fewer levels of 're:' headers
            ctr.add_child(container)
        elif len(ctr.message.subject) > len(container.message.subject):
            # container has fewer levels of 're:' headers
            container.add_child(ctr)
        else:
            new = Container()
            new.add_child(ctr)
            new.add_child(container)
            subject_table[subj] = new

    return subject_table

def thread_from_container(ctr, depth):
    messages = [ctr.message]

    # Base case
    if len(ctr.children) == 0:
        return messages

    # Recursive case
    for c in ctr.children:
        child_messages = thread_from_container(c, depth+1)
        
        # TODO[kavya]: Check if this is true
        if child_messages is not None:
            messages += child_messages
    return messages

# TODO[kavya]: New Thread table?
def create_threads(msglist):
    subject_table = thread(msglist)
    items = subject_table.items()

    for subj, container in items:
        if container.message is None:
            for c in container.children:
                child_thread = thread_from_container(c, 0)
                
                print "\nTHREAD = ", child_thread

                assign_thread_id(child_thread)
        else:
            # TODO[kavya]: Check if this is true
            print "\n SHOULD NOT GET HERE!"

def assign_thread_id(thread):
    thread_id = None
    for message in thread:
        if message.thread_id is not None:
            if ((thread_id is not None) and (message.thread_id != thread_id)):
                print "ERROR!"
            else:
                thread_id = message.thread_id

    if thread_id is None:
        thread = Thread.from_message_yahoo()
        db_session.add(thread)
        db_session.flush()

        thread_id = thread.id        

    # NEED TO SAVE TO DB HERE
    for message in thread:
        if message.thread_id is None:
            message.thread_id = thread_id

    return thread_id

# For debugging:
def print_container(ctr, depth=0, debug=0):
    import sys
    sys.stdout.write(depth*' m***m ')
    if debug:
        # Printing the repr() is more useful for debugging                                                                                                                                             
        sys.stdout.write(repr(ctr))
    else:
        sys.stdout.write(repr(ctr.message and ctr.message.message_id))
        sys.stdout.write(repr(ctr.message and ctr.message.subject))

    sys.stdout.write('\n')
    if len(ctr.children) == 0:
        print "No children\n"
    for c in ctr.children:
        print_container(c, depth+1)



# Usage:
# subject_table = thread(msglist)
# L = subject_table.items()
# L.sort()
# for subj, container in L:
#     print_container(container)
