from enum import Enum

class MatchingLocation(Enum):
    NONE = 1
    ROW = 2
    COLUMN = 3
    BOTH = 4
   
    
    
def populate_possibilities():
  hard_puzzle = [ 
[6,0,0,2,9,0,7,0,0],
[0,0,7,0,3,4,0,8,6],
[1,0,0,7,8,0,0,2,0],
[8,0,0,0,2,0,4,9,0],
[0,3,0,9,6,8,0,7,0],
[0,2,9,0,4,0,0,0,8],
[0,7,0,0,1,2,0,0,9],
[3,1,0,4,7,0,6,0,0],
[0,0,2,0,5,3,0,0,7]]

  easy_puzzle = [ 
[4,0,0,5,0,1,0,0,8],
[0,0,7,3,8,0,4,0,0],
[ 0,6,0,4,0,7,0,0,1 ],
[ 7,0,0,0,0,0,9,1,0 ],
[ 1,0,6,0,0,0,5,0,7 ],
[ 0,2,4,0,0,0,0,0,3 ],
[ 8,0,0,2,0,6,0,7,0 ],
[ 0,0,3,0,1,4,8,0,0 ],
[ 6,0,0,7,0,8,0,0,9 ]]

  medium_puzzle=[
[ 0,5,0,0,7,0,0,2,0 ],
[ 0,0,0,0,0,0,4,9,7 ],
[ 0,0,0,2,0,8,0,5,0 ],
[ 0,4,0,0,0,0,0,3,9 ],
[ 9,0,0,1,3,7,0,0,6 ],
[ 1,2,0,0,0,0,0,7,0 ],
[ 0,9,0,8,0,6,0,0,0 ],
[ 3,1,8,0,0,0,0,0,0 ],
[ 0,7,0,0,1,0,0,8,0 ]
]

# 0 means unknown

  possibilities= [ 
[6,[ ],[ ],2,9,[ ],7,[ ],[ ]],
[[ ],[ ],7,[ ],3,4,[ ],8,6],
[1,[ ],[ ],7,8,[ ],[ ],2,[ ]],
[8,[ ],[ ],[ ],2,[ ],4,9,[ ]],
[[ ],3,[ ],9,6,8,[ ],7,[ ]],
[[ ],2,9,[ ],4,[ ],[ ],[ ],8],
[[ ],7,[ ],[ ],1,2,[ ],[ ],9],
[3,1,[ ],4,7,[ ],6,[ ],[ ]],
[[ ],[ ],2,[ ],5,3,[ ],[ ],7],
]
  for y in range(0,9):
    for x in range(0,9):
      possibilities[y][x]=what_could_go_here(x,y, medium_puzzle)
  
  reduce_again=True
  count=1
  while reduce_again==True:
    print(f'reduce, round: {count}')
    count+=1
    reduce_again=False
    for y in range(0,9):
      for x in range(0,9):
         before = possibilities[y][x]
         after = reduce(x,y, possibilities)
         
         if before != after:
           print(f'{y},{x},{before}=={after}')
           possibilities[y][x]=after
           reduce_again=True
           
    possibilities=clear_singles(possibilities)
    possibilities=clear_sets(possibilities)
  
  # all done, print final map
  for y in range(0,9):
    print(possibilities[y])
  
      
def what_could_go_here(x,y,map):
  all_possibilities=set([1,2,3,4,5,6,7,8,9])
  claimed=[]
  # check if it has a value
  if map[y][x] != 0:
    return [map[y][x]]
  
  # do the y row first
  for i in range(0,9):
    value=map[y][i]
    if value != 0: claimed.append(value)

  # do the x column second
  for i in range(0,9):
    value=map[i][x]
    if value != 0: claimed.append(value)

  # do the 3x3 around it.
  top_y=y-(y%3)
  left_x=x-(x%3)
  for current_y in range(top_y,top_y+3):
    for current_x in range(left_x,left_x+3):
      value=map[current_y][current_x]
      if value != 0: claimed.append(value)
 
  return sorted(all_possibilities-set(claimed))  
  
  
def reduce(x,y,map):
  #
  # is it the only possibility in this cell?
  #
  
  # is it the only thing that could go there?
  second_one_found=False
  if len(map[y][x]) == 1:
    return map[y][x]
  
  # for each possible value in this cell
  for value in map[y][x]:
    # check across
    for i in range(0,9):
      if i==x:
        continue #skip itself
      cell=map[y][i]
      if value in cell:
        second_one_found=True
        break          
    
    if not second_one_found:
      return [value] # it was unique in its row
  
    second_one_found = False
    # check down
    for i in range(0,9):
      if i==y:
        continue #skip itself
      cell=map[i][x]
      if value in cell:
        second_one_found=True
        break
    
    if not second_one_found:
      return [value] # it was unique in its column
  
    second_one_found = False
    
    # check the 3x3 around it.
    top_y=y-(y%3)
    left_x=x-(x%3)
    for current_y in range(top_y,top_y+3):
      for current_x in range(left_x,left_x+3):
        if current_y==y and current_x==x:
          continue #skip itself
        cell=map[current_y][current_x]     
        if value in cell:
          second_one_found=True
          break
        
      if second_one_found:
        break
        
    if not second_one_found:
      return [value] # it was unique in its square
   
  # no unique value found, leave it
  return map[y][x]
  
 
def clear_singles(map):
  #
  # if a cell only has a single value
  # remove all possibility of that value
  # from the row, column, and square.
  #
  
  clear_again=True
  count=1
  while clear_again==True:
    print(f'clear(), round: {count}')
    count+=1
    clear_again=False
    
  for y in range(0,9):
    for x in range(0,9): 
      if len(map[y][x]) != 1:
        continue
      value = map[y][x][0]
      
      # clear it from the row
      for j in range(0,9):
        if j==x:
          continue #skip itself
          
        cell=map[y][j]
        if value in cell:
          cell.remove(value)
          clear_again=True
          
      # clear it from the column
      for i in range(0,9):
        if i==y:
          continue #skip itself
          
        cell=map[i][x]
        if value in cell:
          cell.remove(value)
          clear_again=True
          
      # clear it from the square
      top_y=y-(y%3)
      left_x=x-(x%3)
      for current_y in range(top_y,top_y+3):
        for current_x in range(left_x,left_x+3):
          if current_y==y and current_x==x:
            continue #skip itself
          cell=map[current_y][current_x]  
          if value in cell:
            cell.remove(value)
            clear_again=True
          
  return map
  
def clear_sets(map):
  #
  # if a grid square has a value only in
  # a single row or column,
  # remove all possibility of that value
  # from the rest of the row or column
  #
  
  clear_again=True
  count=1
  while clear_again==True:
    print(f'clear_sets(), round: {count}')
    count+=1
    clear_again=False
    
    for y in range(0,9):
      for x in range(0,9): 
        for value in map[y][x]:
      
          # how big is our square?
          top_y=y-(y%3)
          bottom_y=top_y+3
          left_x=x-(x%3)
          right_x=left_x+3
        
          # is the value only in this squares row
          # if so, remove it from the rest off the row.
          # is the value only in this squares column
          # if so, remove it from the rest off the row.
          location = get_matching_location(value,x,y,map)
          if location == MatchingLocation.NONE:
            continue
          if location == MatchingLocation.ROW or location == MatchingLocation.BOTH:
            # clear it from the row
            for j in range(0,9):
              if j>=left_x and j<=right_x:
                continue #skip itself
          
              cell=map[y][j]
              if value in cell:
                cell.remove(value)
                clear_again=True
       
          if location == MatchingLocation.COLUMN or location == MatchingLocation.BOTH:
            # clear it from the column
            for i in range(0,9):
              if i>=top_y and i<=bottom_y:
                continue #skip itself
          
              cell=map[i][x]
              if value in cell:
                cell.remove(value)
                clear_again=True
                
  return map

def get_matching_location(value, x,y,map):
  # look for value only existing in
  # the single row or single column
  same_row=False
  same_column=False
  top_y=y-(y%3)
  left_x=x-(x%3)
  for current_y in range(top_y,top_y+3):
    for current_x in range(left_x,left_x+3):
      if current_y==y and current_x==x:
        continue #skip itself
      cell=map[current_y][current_x]  
      if value in cell:
        if current_y!=y and current_x!=x:
          # not_same_row_or_colummn=True
          return MatchingLocation.NONE # onto the next value
        if current_y==y:
          same_row=True
        if current_x==x:
          same_column=True
  if same_row and same_column:
    # not uniquely in one row or column
    return MatchingLocation.NONE 
  if same_column:
    return MatchingLocation.COLUMN
  if same_row:
    return MatchingLocation.ROW

  return MatchingLocation.BOTH
  
  
if __name__ == '__main__':
  # Execute when the module is not initialized from an import statement.
  populate_possibilities()
    
    
    
           