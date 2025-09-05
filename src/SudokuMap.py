from enum import Enum
from .SudokuChangeSet import SudokuChange, SudokuChangeSet

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
        self.debug = False
        self.puzzle = puzzle
        self.possibilities = [[[] for _ in range(9)] for _ in range(9)]
        self._initialize_possibilities()


    def _initialize_possibilities(self):
        """Populate initial possibilities for each cell."""
        for y in range(9):
            for x in range(9):
                self.possibilities[y][x] = self.what_could_go_here(y, x)


    def what_could_go_here(self, y, x) -> list[int]:
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


    def solve(self):
        """Run iterative reduction until stable."""
        run_again = True
        count = 1

        while run_again:
            print(f"round: {count}")
            count += 1
            run_again = False
            
            done = False
            while not done:
                changes = self.are_unique()
                if not changes:
                    done = True
                else: 
                    changes.apply(self.possibilities)
                    run_again = True
                    
            done = False
            while not done:
                changes = self.clear_singles()
                if not changes:
                    done = True
                else: 
                    changes.apply(self.possibilities)
                    run_again = True
                    
            done = False
            while not done:
                changes = self.clear_sets()
                if not changes:
                    done = True
                else: 
                    changes.apply(self.possibilities)
                    run_again = True
                    


    def are_unique(self):
        
        results = SudokuChangeSet()
        for y in range(9):
            for x in range(9):
                before = self.possibilities[y][x]
                after = self._get_unique_value(y, x)
                if (after is not None) and (before != after):
                    remove=set(before)-set(after)
                    change = SudokuChange(y,x,remove_values=remove)
                    
                    if self.debug: print(f'added:{change}')
                    results.add(change)
        return results
      
        
    def _get_unique_value(self, y, x) -> bool:
        """Reduce possibilities for a cell based on uniqueness."""
        if len(self.possibilities[y][x]) == 1:
            return self.possibilities[y][x]

        for value in self.possibilities[y][x]:
            if self._is_unique_in_row(value, y, x):
                return [value]
            if self._is_unique_in_column(value, y, x):
                return [value]
            if self._is_unique_in_square(value, y, x):
                return [value]

        return None


    def _is_unique_in_row(self, value, y, x):
        return all(value not in self.possibilities[y][i] for i in range(9) if i != x)

    def _is_unique_in_column(self, value, y, x):
        return all(value not in self.possibilities[i][x] for i in range(9) if i != y)

    def _is_unique_in_square(self, value, y, x):
        top_y=y-(y%3)
        left_x=x-(x%3)
        for cy in range(top_y, top_y + 3):
            for cx in range(left_x, left_x + 3):
                if (cy, cx) != (y, x) and value in self.possibilities[cy][cx]:
                    return False
        return True
    

    def clear_singles(self):
        """Eliminate known single values from related cells."""
        
        results = SudokuChangeSet()
        for y in range(9):
            for x in range(9):
                if len(self.possibilities[y][x]) != 1:
                    continue
                    
                value = self.possibilities[y][x][0]
                changes = self._remove_from_peers(y, x, value)
                if changes:
                    results.add_changeset(changes)

        return results


    def _remove_from_peers(self, y, x, value):
        """Remove a value from row, col, and square peers."""
        results = SudokuChangeSet()

        # Row
        for j in range(9):
            if j != x and value in self.possibilities[y][j]:
                change = SudokuChange(y,j, remove_value=value)
                results.add(change)

        # Column
        for i in range(9):
            if i != y and value in self.possibilities[i][x]:
                change = SudokuChange(i,x, remove_value=value)
                results.add(change)

        # Square
        top_y, left_x = y - (y % 3), x - (x % 3)
        for cy in range(top_y, top_y + 3):
            for cx in range(left_x, left_x + 3):
                if (cy, cx) != (y, x) and value in self.possibilities[cy][cx]:
                    change = SudokuChange(cy,cx, remove_value=value)
                    results.add(change)
        return results


    def clear_sets(self):
        """Apply pointing pairs/triples logic to eliminate candidates."""
        results = SudokuChangeSet()
        for y in range(9):
            for x in range(9):
                for value in self.possibilities[y][x]:
                    location = self.get_matching_location(value, y, x)
                    if location == MatchingLocation.NONE:
                        continue
                    if location in (MatchingLocation.ROW, MatchingLocation.BOTH):
                        changes = self._remove_from_row(value, y, x)
                        if changes:
                            results.add_changeset(changes)

                    if location in (MatchingLocation.COLUMN, MatchingLocation.BOTH):
                        changes = self._remove_from_column(value, y, x)
                        if changes:
                            results.add_changeset(changes)

        return results


    def _remove_from_row(self, value, y, x) -> bool:
        results = SudokuChangeSet()
        left_x = x - (x % 3)
        right_x = left_x + 3
        changed = False
        for j in range(9):
            if not (left_x <= j < right_x) and value in self.possibilities[y][j]:
                change = SudokuChange(y,j, remove_value=value)
                results.add(change)            
        return results


    def _remove_from_column(self, value, y, x) -> bool:
        results = SudokuChangeSet()
        top_y = y - (y % 3)
        bottom_y = top_y + 3
        changed = False
        for i in range(9):
            if not (top_y <= i < bottom_y) and value in self.possibilities[i][x]:
                change = SudokuChange(i,x, remove_value=value)
                results.add(change)            
        return results


    def get_matching_location(self, value, y, x) -> MatchingLocation:
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
