from enum import Enum


class MatchingLocation(Enum):
    NONE = 1
    ROW = 2
    COLUMN = 3
    BOTH = 4


class SudokuMap:
    def __init__(self, puzzle: list[list[int]]):
        """
        Initialize SudokuMap with a puzzle (9x9 grid).
        0 means unknown.
        """
        self.puzzle = puzzle
        self.possibilities = [[[] for _ in range(9)] for _ in range(9)]
        self._initialize_possibilities()

    def _initialize_possibilities(self):
        """Populate initial possibilities for each cell."""
        for y in range(9):
            for x in range(9):
                self.possibilities[y][x] = self.what_could_go_here(x, y)

    def solve(self):
        """Run iterative reduction until stable."""
        reduce_again = True
        count = 1

        while reduce_again:
            print(f"reduce, round: {count}")
            count += 1
            reduce_again = False

            for y in range(9):
                for x in range(9):
                    before = self.possibilities[y][x]
                    after = self.reduce(x, y)
                    if before != after:
                        print(f"{y},{x},{before}=={after}")
                        self.possibilities[y][x] = after
                        reduce_again = True

            self.possibilities = self.clear_singles()
            self.possibilities = self.clear_sets()

        # Print final map
        for row in self.possibilities:
            print(row)

    def what_could_go_here(self, x: int, y: int) -> list[int]:
        """Return all possible values that could go in a cell."""
        all_possibilities = set(range(1, 10))

        if self.puzzle[y][x] != 0:
            return [self.puzzle[y][x]]

        claimed = set()

        # Row
        claimed.update(self.puzzle[y][i] for i in range(9) if self.puzzle[y][i] != 0)

        # Column
        claimed.update(self.puzzle[i][x] for i in range(9) if self.puzzle[i][x] != 0)

        # do the 3x3 around it.
        top_y=y-(y%3)
        left_x=x-(x%3)
        for current_y in range(top_y,top_y+3):
            for current_x in range(left_x,left_x+3):
                value=self.puzzle[current_y][current_x]
                if value != 0: 
                    claimed.add(value)

        return sorted(all_possibilities - claimed)

    def reduce(self, x: int, y: int) -> list[int]:
        """Reduce possibilities for a cell based on uniqueness rules."""
        if len(self.possibilities[y][x]) == 1:
            return self.possibilities[y][x]

        for value in self.possibilities[y][x]:
            if self._is_unique_in_row(value, x, y):
                return [value]
            if self._is_unique_in_column(value, x, y):
                return [value]
            if self._is_unique_in_square(value, x, y):
                return [value]

        return self.possibilities[y][x]

    def _is_unique_in_row(self, value, x, y):
        return all(value not in self.possibilities[y][i] for i in range(9) if i != x)

    def _is_unique_in_column(self, value, x, y):
        return all(value not in self.possibilities[i][x] for i in range(9) if i != y)

    def _is_unique_in_square(self, value, x, y):
        top_y=y-(y%3)
        left_x=x-(x%3)
        for cy in range(top_y, top_y + 3):
            for cx in range(left_x, left_x + 3):
                if (cy, cx) != (y, x) and value in self.possibilities[cy][cx]:
                    return False
        return True

    def clear_singles(self):
        """Eliminate known single values from related cells."""
        clear_again = True
        count = 1
        while clear_again:
            print(f"clear(), round: {count}")
            count += 1
            clear_again = False

            for y in range(9):
                for x in range(9):
                    if len(self.possibilities[y][x]) != 1:
                        continue
                    value = self.possibilities[y][x][0]
                    if self._remove_from_peers(x, y, value):
                        clear_again = True
        return self.possibilities

    def _remove_from_peers(self, x, y, value) -> bool:
        """Remove a value from row, col, and square peers."""
        changed = False

        # Row
        for j in range(9):
            if j != x and value in self.possibilities[y][j]:
                self.possibilities[y][j].remove(value)
                changed = True

        # Column
        for i in range(9):
            if i != y and value in self.possibilities[i][x]:
                self.possibilities[i][x].remove(value)
                changed = True

        # Square
        top_y, left_x = y - (y % 3), x - (x % 3)
        for cy in range(top_y, top_y + 3):
            for cx in range(left_x, left_x + 3):
                if (cy, cx) != (y, x) and value in self.possibilities[cy][cx]:
                    self.possibilities[cy][cx].remove(value)
                    changed = True
        return changed

    def clear_sets(self):
        """Apply pointing pairs/triples logic to eliminate candidates."""
        clear_again = True
        count = 1
        while clear_again:
            print(f"clear_sets(), round: {count}")
            count += 1
            clear_again = False

            for y in range(9):
                for x in range(9):
                    for value in self.possibilities[y][x]:
                        location = self.get_matching_location(value, x, y)
                        if location == MatchingLocation.NONE:
                            continue
                        if location in (MatchingLocation.ROW, MatchingLocation.BOTH):
                            if self._remove_from_row(value, y, x):
                                clear_again = True
                        if location in (MatchingLocation.COLUMN, MatchingLocation.BOTH):
                            if self._remove_from_column(value, x, y):
                                clear_again = True
        return self.possibilities

    def _remove_from_row(self, value, y, x) -> bool:
        left_x = x - (x % 3)
        right_x = left_x + 3
        changed = False
        for j in range(9):
            if not (left_x <= j < right_x) and value in self.possibilities[y][j]:
                self.possibilities[y][j].remove(value)
                changed = True
        return changed

    def _remove_from_column(self, value, x, y) -> bool:
        top_y = y - (y % 3)
        bottom_y = top_y + 3
        changed = False
        for i in range(9):
            if not (top_y <= i < bottom_y) and value in self.possibilities[i][x]:
                self.possibilities[i][x].remove(value)
                changed = True
        return changed

    def get_matching_location(self, value, x, y) -> MatchingLocation:
        """Check if a value appears only in one row or col within its 3x3 block."""
        same_row, same_col = False, False
        top_y=y-(y%3)
        left_x=x-(x%3)

        for cy in range(top_y, top_y + 3):
            for cx in range(left_x, left_x + 3):
                if (cy, cx) == (y, x):
                    continue
                cell = self.possibilities[cy][cx]
                if value in cell:
                    if cy != y and cx != x:
                        return MatchingLocation.NONE
                    if cy == y:
                        same_row = True
                    if cx == x:
                        same_col = True

        if same_row and same_col:
            return MatchingLocation.NONE
        if same_col:
            return MatchingLocation.COLUMN
        if same_row:
            return MatchingLocation.ROW
        return MatchingLocation.BOTH
