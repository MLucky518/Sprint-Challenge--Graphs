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
    moves = starting_room.get_exits()
    random.shuffle(moves)

    for move in moves:
        next_room = starting_room.get_room_in_direction(move)

        # walk backwards and find more moves in there are none currently
        if len(moves) > 2:
            path = []
        if len(moves) == 2 and starting_room.get_room_in_direction(moves[0]).name in visited and len(moves) == 2 and starting_room.get_room_in_direction(moves[1]).name in visited:
            traversal_path.extend(calculate_path(path))
            return
        elif len(moves) == 1 and starting_room.get_room_in_direction(move).name in visited:
            traversal_path.extend(calculate_path(path))
            return
        elif next_room.name not in visited:
            path.append(move)
            moves2 = next_room.get_exits()
        
            if len(moves2) == 2:
                path_clone = path.copy()
                traverse_graph(next_room, path_clone, visited)
            elif len(moves2) > 2:
                path_clone = path.copy()
                traversal_path.extend(path)
                traverse_graph(next_room, visited=visited)
                traversal_path.extend(calculate_path(path_clone, False))
            else:
                path_clone = path.copy()
                traverse_graph(next_room, path_clone, visited)

# https://stackoverflow.com/questions/41223744/keeping-the-initial-value-of-a-variable-in-recursive-function


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
