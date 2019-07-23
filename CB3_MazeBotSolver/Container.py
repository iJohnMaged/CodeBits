class Container:

    """
        Custom class to represent the open_list in my maze solver to make things faster
        by using a set to look-up if a tile exists in the list.
    """

    def __init__(self, initial_tiles):
        self.positions = set()
        self.tiles = initial_tiles
        for tile in self.tiles:
            self.positions.add(tile.pos)

    def __contains__(self, m):
        return m in self.positions

    def add(self, item):
        self.positions.add(item.pos)
        self.tiles.append(item)

    def update(self, T):
        for k in self.tiles:
            if T.pos == k.pos and T.f < k.f:
                self.tiles.remove(k)
                self.tiles.append(T)
                break
            elif T.pos == k.pos and T.f >= k.f:
                break

    def get(self):
        self.tiles.sort(key = lambda x: x.f)
        tile = self.tiles.pop(0)
        self.positions.remove(tile.pos)
        return tile

    def __len__(self):
        return len(self.tiles)