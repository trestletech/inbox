# Requirements of the message_table: 
# message_id, jwz_parent, jwz_children, jwz_dummy.
# has_descendant()

class JWZThread(object):
	def __init__(db_session, message_table, thread_table):
		self.db_session = db_session
		self.message_table = message_table
		self.thread_table = thread_table

	def thread(self, message):
		self.message = message
        self.chain_references()

	# Step1
	def chain_references(self):
		db_session = self.db_session
		message_table = self.message_table
		message = self.message

		# TODO[kavya]
        # CHECK goto step_5()?
		if len(message.references) == 0:
			do_something()

		# .references includes in-reply-to as last elt
        # TODO[kavya]: Get indv. columns only, or whole Message?
    	msglist = db_session.query(
            message_table.message_id, 
            message_table.jwz_parent, 
            message_table.jwz_children,
            message_table.jwz_dummy).filter(
            message_table.message_id.in_(message.references)).all()

        # TODO[kavya]
        if len(msglist) == 0:
            do_something()

        # TODO[kavya]: Is this dict needed; could query DB one-by-one?
    	self.msgdict = { m[0]: m for m in msglist }

        prev = None
        for ref_id in message.references:
            if ref_id not in msgdict:
                self.msgdict[ref_id] = create_dummy_message(ref_id)

            if (prev is not None):
                # Cycle prevention 1:
                # TODO[kavya]: How the fuck? CHECK: Don't need anymore!
                if ref_id is message.message_id:
                    continue

                # Cycle prevention 2: 
                if message_table.has_descendant(ref_id, prev):
                    continue

                self.link(prev, ref_id)

            prev = container

        # TODO[kavya]: Check What about Cycle prevention HERE?
        if prev is not None:
            # Needed here? Only if this message existed as dummy earlier
            self.last_link(prev)

    def find_root(self):
        self.root = None

        # May not be SELECT-ed, therefore get from database
        if self.message.references[0].parent is None:
            self.root = self.message.references[0]
        else:
            self.root = recurse()

        assert (self.root and self.root.parent == None)
        
        new_root_set = []
        for container in root_set:
            L = prune_container(container)
            new_root_set.extend(L)

        root_set = new_root_set

    # TODO[kavya]: Pull from database!
    def prune(self):
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

    def link(self, parent, child):
        assert (parent in self.msgdict)
        assert (child in self.msgdict)

        # Don't change existing links
        if (self.msgdict[child][1] is None):
            self.msgdict[child][1] = parent

        self.msgdict[parent][2].append(child)

    def last_link(self, parent):
        assert (parent in self.msgdict)

        # Remove old parent + as child in old parent
        if self.message.parent is not None:
            # Is parent guaranteed to be in msgdict?
            # If not remove this message id as parent's child from the database!

            #self.message.parent = None

        self.message.parent = parent
        self.msgdict[parent][2].append(self.message.message_id)
