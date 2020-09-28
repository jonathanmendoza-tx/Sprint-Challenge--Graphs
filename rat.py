from room import Room
from player import Player
from world import World

class Stack:

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


class Pathfinder:

	def __init__(self, starting_room):

		self.path = []
		self.direction_stack = Stack()
		self.visited = set()
		self.player = Player(starting_room)
		self.traversal_graph = {}

	def update_traversal_graph(self):

		if self.player.current_room.id not in self.traversal_graph:
			self.traversal_graph[self.player.current_room.id] = {}

		for direction in self.player.current_room.get_exits():
			if direction not in self.traversal_graph[self.player.current_room.id]:
				self.traversal_graph[self.player.current_room.id][direction] = '?'

	def find_path(self):

		return self.path

	def opposite(self, direction):

		opposite_direction = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

		return opposite_direction[direction]

	def move(self, direction):

		self.update_traversal_graph()

		from_room = self.player.current_room.id

		self.player.travel(direction)

		self.path.append(direction)

		self.update_traversal_graph()

		if self.traversal_graph[from_room][direction] == '?':

			self.traversal_graph[from_room][direction] = self.player.current_room.id

			self.traversal_graph[self.player.current_room.id][self.opposite(direction)] = from_room

	def make_path(self, world):

		exits = self.player.current_room.get_exits()
		# goes through all exits possible at current roon
		for e in exits:
			self.direction_stack.push((e, "Ahead"))
		# add as visited room
		self.visited.add(self.player.current_room)

		# check if all rooms are visited
		while self.direction_stack.size() > 0:
			if len(self.visited) == len(world.rooms):
				return
			direction_info = self.direction_stack.pop()
			if direction_info[1] is "Ahead":  # if not visited room, we need to visit it
				if self.player.current_room.get_room_in_direction(direction_info[0]) not in self.visited:
					self.move(direction_info[0])
					# once visited, add it to visited list
					self.visited.add(self.player.current_room)
					self.add_directions(direction_info[0])
			elif direction_info[1] is "Back":  # if already visited
				self.move(direction_info[0])

	def add_directions(self, last_direction):

		self.direction_stack.push((self.opposite(last_direction), "Back"))
		# finding available direction
		available_directions = self.player.current_room.get_exits()

		for ad in available_directions:
			room = self.player.current_room.get_room_in_direction(ad)
			if room not in self.visited:
				self.direction_stack.push((ad, "Ahead"))
