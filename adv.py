# from room import Room
from player import Player
from world import World

# import random
from ast import literal_eval

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

opposite_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}
starting_room = player.current_room
visited = {}  # dictionary
reversed_direction = []
current_room = starting_room
previous_room = []


# Return a direction that is unexplored
def find_next_move(visited, current_room):
    curr_room = current_room.id
    room_exits = visited[curr_room]

    # Check each direction and return a direction not explored
    for direction in room_exits:
        if room_exits[direction] == '?' and current_room.get_room_in_direction(direction).id not in visited:
            return direction
    return None


def find_unexplored_room():
    while True:
        back_direction = reversed_direction.pop()
        traversal_path.append(back_direction)
        player.travel(back_direction)
        next_room = player.current_room
        print("Values:", visited[next_room.id].values())
        if '?' in visited[next_room.id].values():
            return next_room


while len(visited) < len(world.rooms):
    # put current room in visited  with empty routes
    if current_room.id not in visited:
        curr_exits = current_room.get_exits()  # ["n"]

        exits = {}
        # build up current visited dictionary with exits not visited
        # -> {"n": "?", "s": "?", "w": "?", "e": "?"}
        for ext in curr_exits:
            exits[ext] = "?"
            visited[current_room.id] = exits

    next_room_direction = find_next_move(visited, current_room)

    # If at a dead end find a room with exits = "?"
    if next_room_direction is None:
        # Backtrack until valid exits are found
        new_room = find_unexplored_room()
        current_room = new_room
        print(new_room)
    else:
        #  Add direction to path, move into next room
        player.travel(next_room_direction)
        traversal_path.append(next_room_direction)

        # Keep track of reverse direction for backtracking
        reversed_direction.append(opposite_directions[next_room_direction])
        previous_room = current_room
        current_room = player.current_room  # set current room to new room
        # print("prev", previous_room.id)

        # update visiteds
        new_exits = {}
        for ext in current_room.get_exits():
            new_exits[ext] = "?"
            visited[current_room.id] = new_exits

        # set previous room direction to new room
        visited[previous_room.id][next_room_direction] = current_room.id
        visited[current_room.id][opposite_directions[next_room_direction]
                                 ] = previous_room.id  # set new room direction

    print("next room in direction:", next_room_direction)
    print("visited:", visited)

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
"""

player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")

"""
