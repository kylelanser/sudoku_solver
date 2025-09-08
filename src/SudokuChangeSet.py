class SudokuChangeSet:
 
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
           
           
    def apply(self, map):
        
        if self.value is not None:
            map[self.y][self.x]=self.value
   
        if self.removal is not None:
            if self.debug: print(self)
            if self.debug: print(f'map:{map[self.y][self.x]}, {self.removal}')
            if self.removal in map[self.y][self.x]:
                if len(map[self.y][self.x])==1:
                  print(f'error!')
                  print(f'map:{map[self.y][self.x]}, {self.removal}')
                map[self.y][self.x].remove(self.removal)
      
        if self.removals is not None:
            if self.debug: print(self)
            if self.debug: print(f'map:{map[self.y][self.x]}, {self.removals}')
            for value in self.removals:
                if value in map[self.y][self.x]:
                    map[self.y][self.x].remove(value)
      
        
   
        