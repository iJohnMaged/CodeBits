import requests
from collections import namedtuple
from Container import Container


# Object to represent a tile in a maze
Tile = namedtuple('Tile', ['pos', 'g', 'h', 'f', 'trace'])

# Allowed directions to move to, no diagonal movements
directions = {
    'E': (0, 1), 
    'S': (1, 0),
    'W': (0, -1),
    'N': (-1, 0)
}


def get_random_maze(min_size = 10, max_size = 20):
    contents = requests.get(url = f'https://api.noopschallenge.com/mazebot/random?minSize={min_size}&maxSize={max_size}').json()
    return contents


def manhattan_dist(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def get_adjacent_tiles(maze, parent, end_position):
    """
        Returns the adjacent tiles of parent that parent can move to.
    """
    rows = len(maze)
    cols = len(maze[0])
    position = parent.pos
    result = []

    for key, dir in directions.items():
        row = position[0] + dir[0]
        col = position[1] + dir[1]

        if row >= 0 and row < rows and col >= 0 and col < cols:
            if maze[row][col] != 'X':
                h = manhattan_dist([row, col], end_position)
                result.append(Tile((row, col), parent.g+1, h, parent.g+1+h, parent.trace + key))

    return result


def solve_maze(maze, start_position, end_position):
    """
        Maze solver using A* pathfinding algorithm
    """

    closed_list = set()
    
    start_tile_h = manhattan_dist(start_position, end_position)
    start_tile = Tile(start_position, 0, start_tile_h, start_tile_h, '')
    closed_list.add(start_tile.pos)
    open_list = Container(get_adjacent_tiles(maze, start_tile, end_position))

    while len(open_list) > 0:
        current_tile = open_list.get()
        closed_list.add(current_tile.pos)

        for T in get_adjacent_tiles(maze, current_tile, end_position):

            if T.pos == end_position:
                return T

            if T.pos in closed_list:
                continue

            if T.pos not in open_list:
                open_list.add(T)

            if T.pos in open_list:
                open_list.update(T)


def post_solution(post_url, soltion_tile):
    data = {
        'directions': soltion_tile.trace
    }
    r = requests.post(url = post_url, json=data)
    print(r.text)


def main():
    response = get_random_maze(10, 200)
    start_position = tuple(reversed(response['startingPosition']))
    end_position = tuple(reversed(response['endingPosition']))
    soltion_tile = solve_maze(response['map'], start_position, end_position)
    print(f'Solution: {soltion_tile.trace}')
    post_solution(f'https://api.noopschallenge.com{response["mazePath"]}', soltion_tile)


if __name__ == '__main__':
    main()