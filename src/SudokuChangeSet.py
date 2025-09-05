class SudokuChangeSet:
    def __init__(self, ):
        self._changes = []
        self.debug = False

    def __bool__(self):
        return len(self._changes)>0

    def add(self, change):
        self._changes.append(change)

    def add_many(self, changes):
        self._changes = [ *changes, *self._changes]

    def add_changeset(self, changeset):
        self._changes = [ *changeset._changes, *self._changes]

        

class SudokuChange:
    def __init__(self, y, x, new_value=None, remove_value=None, remove_values=None):
        """
        Initialize SudokuMap with a puzzle (9x9 grid).
        0 means unknown.
        """
        self.debug=False
        self.x = x
        self.y = y
        self.value =  new_value
        self.removal = remove_value
        self.removals = remove_values
    def __str__(self):
        if self.value is not None:
            return f'({self.y},{self.x})={self.value}'
            
        if self.removal is not None:
            return f'({self.y},{self.x}).remove({self.removal})'
         
        if self.removals is not None:
            return f'({self.y},{self.x}).remove({self.removals})'
           
           
        
   
        