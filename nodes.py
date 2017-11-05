class Node(object):
	def __init__(self, *children):
		*self.children, = children

	def eval(self):
		pass
	
	def append_child(self, child):
		self.children.append(child)

class Unary(Node):
	def eval(self):
		return self.children[0](self.children[1].eval())

class Binary(Node):
	def eval(self):
		return self.children[0](self.children[1].eval(), self.children[2].eval())

class Block(Node):
	def eval(self):
		for child in self.children:
			child.eval()

class Literal(Node):
	def eval(self):
		return self.children[0]

class Symbol_Lookup(Node):
	def eval(self):
		return env[self.children[0]]

class Assign(Node):
	def eval(self):
		env[self.children[0]]=self.children[1].eval()

class While(Node):
	def eval(self):
		while self.children[0].eval():
			self.children[1].eval()
