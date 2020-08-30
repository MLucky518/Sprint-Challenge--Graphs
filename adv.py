from room import Room
from player import Player
from world import World

import random
from ast import literal_eval


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
visited_matrix = []

# for i in range(world.grid_size):
#     visited_matrix.append([False] * world.grid_size)

# for el in range(world.grid_size):
#     print(f"{ world.room_grid[el] } ")

# for el in visited_matrix:
#     print(el)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
opposite = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}


def calculate_path(path, return_full=True):
    backtrack_path = []
    # Reverse incrementation to start at the last visited room in path
    for i in range(len(path))[::-1]:
        backtrack_path.append(opposite[path[i]])

    path.extend(backtrack_path)
    if return_full:
        return path
    else:
        return backtrack_path


def traverse_graph(starting_room, path=None, visited=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(starting_room.name)
    directions = starting_room.get_exits()
    random.shuffle(directions)

    for direction in directions:
        next_room = starting_room.get_room_in_direction(direction)

        # walk backwards and find more moves in there are none currently
        if len(directions) > 2:
            # if true were at the very beginning
            path = []
        if len(directions) == 2 and starting_room.get_room_in_direction(directions[0]).name in visited and starting_room.get_room_in_direction(directions[1]).name in visited:
            traversal_path.extend(calculate_path(path))
            return
        elif len(directions) == 1 and starting_room.get_room_in_direction(direction).name in visited:
            traversal_path.extend(calculate_path(path))
            return
        elif next_room.name not in visited:
            path.append(direction)
            directions2 = next_room.get_exits()
            random.shuffle(directions2)

            if len(directions2) > 2:  # ******
                path_clone = path.copy()
                traversal_path.extend(path)
                # https://stackoverflow.com/questions/41223744/keeping-the-initial-value-of-a-variable-in-recursive-function
                traverse_graph(next_room, visited=visited)
                traversal_path.extend(calculate_path(path_clone, False))

            elif len(directions2) == 2:
                path_clone = path.copy()
                traverse_graph(next_room, path_clone, visited)

            else:
                path_clone = path.copy()
                traverse_graph(next_room, path_clone, visited)


traverse_graph(world.starting_room)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")


# def bfs(starting_vertex, explored):
#     q = Queue()
#     q.enqueue([starting_vertex])
#     visited = []
#     print(starting_vertex)
#     while q.size() > 0:
#         current_path = q.dequeue()
#         current_vertex = current_path[-1]
#         print(current_vertex)
#         if current_vertex not in visited:
#             exits = current_vertex.get_exits()
#             if "?" in explored[current_vertex.id].values():
#                 for exit in explored[current_vertex.id].values():
#                     if exit == "?":
#                         return current_path
#             else:
#                 visited.append(current_vertex)
#                 for exit in exits:
#                     q.enqueue(exit)


# def traverse_graph():
#     current = player.current_room
#     visited = {}
#     directions = current.get_exits()

#     visited[current.id] = {direc: "?" for direc in directions}

#     random.shuffle(directions)
#     s = Stack()

#     for el in directions:
#         s.push(el)

#     while s.size() > 0:
#         unvisited_directions = []
#         next_direction = s.pop()

#         prev_room = current
#         player.travel(next_direction)
#         # logs direction traveled by player
#         traversal_path.append(next_direction)
#         current = player.current_room
#         # gets all exits for the current room
#         current_exits = current.get_exits()

#         visited[prev_room.id][next_direction] = current.id

#         # If not visited then add to graph
#         if current.id not in visited:
#             visited[current.id] = {exit: "?" for exit in current_exits}

#         for (exit, room_id) in visited[current.id].items():
#             if room_id == "?":
#                 unvisited_directions.append(exit)
#         opposite_direction = opposite[next_direction]
#         if opposite_direction in current_exits:
#             visited[current.id][opposite_direction] = prev_room.id

#         if len(unvisited_directions) > 0:
#             s.push(unvisited_directions[-1])

#         else:
#             path_back = bfs(current, visited)
#             if path_back is not None:
#                 for direc in path_back:
#                     player.travel(direc)
#                     traversal_path.append(direc)
#             current = player.current_room

#         for (exit, room_id) in visited[current.id].items():
#             if room_id == "?":
#                 unvisited_directions.append(exit)
#         if len(unvisited_directions) > 0:
#             s.push(unvisited_directions[0])
