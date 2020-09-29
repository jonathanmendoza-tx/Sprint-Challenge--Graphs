from room import Room
from player import Player
from world import World
import random

class Stack:
	"""
	Standard stack class

	"""

	def __init__(self):

		self.stack = []

	def size(self):

		return len(self.stack)

	def push(self, value):

		self.stack.append(value)

	def pop(self):

		if self.size() > 0:
			return self.stack.pop()
		else:
			return None

	def peek(self):
         return self.stack[len(self.stack)-1]


class Pathfinder:

	def __init__(self, world, starting_room):

		self.path = []
		self.world = world
		self.direction_stack = Stack()
		self.visited = set()
		self.player = Player(starting_room)
		self.traversal_graph = {}

	def update_traversal_graph(self):
		"""
		create new, initialized entries for traversal graph

		"""

		if self.player.current_room.id not in self.traversal_graph:
			self.traversal_graph[self.player.current_room.id] = {}

		for direction in self.player.current_room.get_exits():
			if direction not in self.traversal_graph[self.player.current_room.id]:
				self.traversal_graph[
					self.player.current_room.id][direction] = '?'

	def opposite(self, direction):
		"""
		input: single cardinal direction

		returns: opposite cardinal direction when called

		"""

		opposite_direction = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

		return opposite_direction[direction]

	def move(self, direction):
		"""
		input: single cardinal direction

		output: moves player character and updates traversal graph for both the 
			previous and new room the player has occupied

		"""

		self.update_traversal_graph()

		from_room = self.player.current_room.id

		self.player.travel(direction)

		self.path.append(direction)

		self.update_traversal_graph()

		if self.traversal_graph[from_room][direction] == '?':

			self.traversal_graph[from_room][
				direction] = self.player.current_room.id

			self.traversal_graph[self.player.current_room.id][
				self.opposite(direction)] = from_room

	def make_path(self):
		"""
		Start traversing the world.

		Loops until stack is empty or all rooms have been visited

		"""

		#start traversal
		exits = self.player.current_room.get_exits()

		#random start direction
		random.shuffle(exits)

		for direction in exits:
			self.direction_stack.push((direction, "?"))

		self.visited.add(self.player.current_room)


		#traverse maze until all rooms visited and/or stack is empty
		while self.direction_stack.size() > 0:


			if len(self.visited) == len(self.world.rooms):
				return

			direction_info = self.direction_stack.pop()

			#check if room has been visited, or is marked as unknown
			if direction_info[1] is "?":

				if self.player.current_room.get_room_in_direction(direction_info[0]) not in self.visited:

					self.move(direction_info[0])
					self.visited.add(self.player.current_room)
					self.add_directions(direction_info[0])

			else:

				self.move(direction_info[0])

	def add_directions(self, last_direction):
		"""
		input: direction last traveled

		output: updates stack with reverse direction for backtracking and new 
			directions if unvisited rooms are found in neighboring rooms.

		"""

		self.direction_stack.push((self.opposite(last_direction), "visited"))
		
		available_directions = self.player.current_room.get_exits()

		random.shuffle(available_directions)

		for direction in available_directions:
			room = self.player.current_room.get_room_in_direction(direction)

			if room not in self.visited:
				self.direction_stack.push((direction, "?"))
