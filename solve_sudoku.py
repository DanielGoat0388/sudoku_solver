#Solve sudoku

"""
This is the sudoku board to be used
 ___________   ___________   ___________
|___|___|___| |___|___|___| |___|___|___|
|___|___|___| |___|___|___| |___|___|___|
|___|___|___| |___|___|___| |___|___|___|
 ___________   ___________   ___________
|___|___|___| |___|___|___| |___|___|___|
|___|___|___| |___|___|___| |___|___|___|
|___|___|___| |___|___|___| |___|___|___|
 ___________   ___________   ___________
|___|___|___| |___|___|___| |___|___|___|
|___|___|___| |___|___|___| |___|___|___|
|___|___|___| |___|___|___| |___|___|___|

A 'row' and 'column' refers to a row/column of dimensions 3 by 9 
A 'subrow' and 'subcolunm' refers to a row/column of dimension 1 by 9

"""


from numpy import square


example_point  = [True, True, True, True, True, True, True, True, True]
example_subrow = [example_point,example_point,example_point]
example_square = [example_subrow, example_subrow, example_subrow]
example_row    = [example_square, example_square, example_square]
example_board  = [example_row, example_row, example_row]

#printing board
def print_row(row):
    print(" ___________   ___________   ___________")
    for x in range(3): #each column
        row_string = '|'
        for y in range(3): #row in plane
            subrow  = row[y][x] #yth row on the xth plane, 
            for subcolumn in subrow:
                length = len(row_string)
                if  length==13 or length ==27: #time to add space
                    row_string+= " |"

                if type(subcolumn) != int: #list of bools
                    row_string+=("___|")
                else:
                    row_string+=('_')
                    row_string+=str(subcolumn) #an integer
                    row_string+=("_|")
        print(row_string)

def print_board(board):
    count= 0 
    for row in board:
        print_row(row)
        count+=1
    if count==3:
        print("")

#functions return 'groups' for board data
def create_row_list(board):
    """
    (list) -> (list)
    board list -> list of sub lists representing each subrow (line)
    
    """
    row_list = []
    for w in range(3): #rows
        for y in range(3): #sub rows
            subrow = []
            for x in range(3): #columns
                for z in range(3): #sub columns
                    subrow.append(board[w][x][y][z])
                    #print(w,x,y,z)
            row_list.append(subrow)
    return row_list

def create_column_list(board):
    """
    (list) -> (list)
    board list -> list of sub lists representing each subcolumn (line)
    
    """
    column_list = []
    for x in range(3): #columns
        for z in range(3): #sub columns
            subcolumn = []
            for w in range(3): #rows
                for y in range(3): #sub rows
                    subcolumn.append(board[w][x][y][z])
                    #print(w,x,y,z)
            column_list.append(subcolumn)
    return column_list

def create_square_list(board):
    """
    (list) -> (list)
    board list -> list of sub lists representing each square (3 by 3)
    
    """
    square_list = []
    for w in range(3): #rows
        for x in range(3): #columns
            square = []
            for y in range(3): #sub rows
                for z in range(3): #sub columns
                    square.append(board[w][x][y][z])
                    #print(w,x,y,z)
            square_list.append(square)
    return square_list

#for debugging
def print_group_data(group_data):
    for subgroup in group_data:
        print(subgroup)
        print("")

def print_subgroup_data(subgroup):
    for point in subgroup:
        print(point)


#'sub groups' rep each row, column or square
def update_bools(sub_group):
    """
    if one element in list is integer, eliminate index of all other elements (lists)
    where each element represents a point
    """
    integer_list = []
    for point in sub_group:
        if type(point) == int:
            integer_list.append(point)
        
    for point in sub_group:
        if type(point) == list: #should be all the other points
            for integer in integer_list:
                if integer in integer_list:
                    #print(integer)
                    #print(point)
                    point[integer-1] = False #one less for index
    return sub_group

def update_bools_given_group(group): #change boolean values
    for sub_group in group:
        sub_group = update_bools(sub_group)
    return group

def change_point_list_to_number(point): #change point to integer
    """
    input point
    return (bool, integer/list)
    True if one answer, false if not one answer
    Integer if one answer, list if not
    """
    sum = 0
    one_answer = False
    integer = 1
    if type(point)!=int:
        for bool in point:
            sum+=bool
        #print("Sum of this list: " , sum)
        if sum==1:
            one_answer = True
        if one_answer:
            for x in range(9):
                if point[x]:
                    integer+=x #index + 1 = true value
        if one_answer:
            return [one_answer, integer]
    return [one_answer, point]

def check_and_update_subgroup(subgroup): #change point to integer
    """input subgroup
    checks if any points are one integer
    updates points
    updates other 
    returns subgroup"""
    #print_subgroup_data(subgroup)
    for x in range(len(subgroup)):
        subgroup[x] = change_point_list_to_number(subgroup[x])
        #print(subgroup[x][1] , 'subgroup point or int')
        subgroup[x] = subgroup[x][1]
    #print(exrow)
    #print("_____________________________________________________")
    #print_subgroup_data(subgroup)
    #print("")
    return subgroup

def check_and_update_group(group): #change point to integer
    """
    same as check_and_update_subgroup but for group of rows/columns/squares
    returns updated group using group data
    """
    for sub_group in group:
        #sub_group = eliminate_num(sub_group)
        sub_group = check_and_update_subgroup(sub_group)
    return group


def deduce_point_integer_subgroup(subgroup): #if every other point CANNOT be x int, then last point must be x
    """
    (subgroup line) -> (updated subgroup line)
    deduces if a point MUST be a certain integer if every other point CANNOT be that integer
    """
    counter=0
    point_to_change = ''
    point_to_integer_index = ''
    for x in range(9): #iterate through bools of index
        bool_index_sum = 0
        for point in subgroup:                 #go through every point's 1st bool, 2nd bool... 9th bool
            if type(point)==list:              #only iterable if its a list
                bool_index_sum+=point[x]       #sum these bools
                
        
        if bool_index_sum==1:                  #if sum==1, then all but one is potentially that integer
            counter2 = 0                       #counting the point's index within the line 
            for point in subgroup:             #iterate through points again
                if type(point)==list:          #only list points of course
                    if point[x] == True:           #this is the only point that can potentially be that integer
                        point_to_change = counter2  #this is the point's index within line to be changed
                        point_to_integer_index = x  #this is the index bool of the point to change
                counter2+=1

        counter+=1
    if type(point_to_change)==int and type(point_to_integer_index)==int:
        subgroup[point_to_change] = point_to_integer_index +1
    
    return subgroup

def deduce_point_integer_group(group):
    for subgroup in group:
        subgroup = deduce_point_integer_subgroup(subgroup)
    return group


#converting row, column and square data to board format
def make_master_list(group):
    master_list = []
    for subgroup in group:
        for point in subgroup:
            master_list.append(point)
    return master_list

def row_group_to_board(row_group,board):
    """
    (row_group) , (board) -> updated board
    """
    master_list = make_master_list(row_group)
    counter = 0
    for w in range(3): #rows
        for y in range(3): #sub rows
            for x in range(3): #columns
                for z in range(3): #sub columns
                    board[w][x][y][z] = master_list[counter]
                    counter+=1
    return board

def column_group_to_board(column_group,board):
    """
    (row_group) , (board) -> updated board
    """
    master_list = make_master_list(column_group)
    #print(master_list[45])
    counter = 0
    for x in range(3): #rows
        for z in range(3): #sub rows
            for w in range(3): #columns
                for y in range(3): #sub columns
                    board[w][x][y][z] = master_list[counter]
                    #print(w,x,y,z)
                    counter+=1
    return board

def square_group_to_board(square_group,board):
    """
    (row_group) , (board) -> updated board
    """
    master_list = make_master_list(square_group)
    counter = 0
    for w in range(3): #rows
        for x in range(3): #columns
            for y in range(3): #sub rows
                for z in range(3): #sub columns
                    board[w][x][y][z] = master_list[counter]
                    counter+=1
    return board

""""
board  -> row group data
row group data -> updated bools
updated bools -> deduce point ints
updated bools -> change point lists to ints
group data -> board

rowdata = create_row_list(board2)
updated_bools= eliminate_num_given_group(rowdata)
updated_ints_row_data = check_and_update_group(updated_bools)
new_board = row_group_to_board(updated_ints_row_data,board2)

repeat for column, square"""

#________________________________________________________________

def update_board(board): #not working at all
    """
    (board) -> (updated board)
    Updates bools in subgroup of points
    Updates point lists to point ints if possible
    """
    
    rowdata = create_row_list(board)                          #collect data for every subrow line
    updated_bools_row = update_bools_given_group(rowdata)         #update bools
    updated_bools_row  = deduce_point_integer_group(updated_bools_row)       #deduce point integers
    updated_rowdata = check_and_update_group(updated_bools_row)   #change point lists to point ints
    board = row_group_to_board(updated_rowdata,board)         #convert to standard board data structure

    #print_board(board)
    #input("Press enter ")

    columndata = create_column_list(board)                     #collect data for every subcolumn line
    updated_bools_column= update_bools_given_group(columndata)        #update bools
    updated_bools_column  = deduce_point_integer_group(updated_bools_column)       #deduce point integers
    updated_columndata = check_and_update_group(updated_bools_column) #change point lists to point ints
    board = column_group_to_board(updated_columndata,board)    #convert to standard board data structure

    #print_board(board)
    #input("Press enter ") #check every step

    squaredata = create_square_list(board)                                         #collect data for every 3 by 3 square
    updated_bools_square= update_bools_given_group(squaredata)                     #update bools
    updated_bools_square  = deduce_point_integer_group(updated_bools_square)       #deduce point integers
    updated_squaredata = check_and_update_group(updated_bools_square)              #change point lists to point ints
    board = square_group_to_board(updated_squaredata,board)                        #convert to standard board data structure


    
    return board


#for user input to mark board
def check_integer(x): #check integer x, if int, return true
    try:
        xint=int(x)
        return True
    except ValueError:
        return False

def get_value():
    not_valid = True
    while not_valid:
        value = input("Enter value: ")
        if check_integer(value) and len(value)==1 :
            not_valid = False
    return int(value)

def get_coordinates():
    get_bool = True
    while get_bool:
        coordinate_string = input("Enter coordinates in form 'w,x,y,z': ")
        if len(coordinate_string)!=7: #check length for proper format
            print("Invalid format")
        elif coordinate_string[1] and coordinate_string[3] and coordinate_string[5] != ',': #make sure it has commas
            print("Invalid format")
        else:
            coordinate_list=[]
            valid = 0 #valid is intially false
            for x in range(len(coordinate_string)): #iterate through string
                if coordinate_string[x]!=',': #if its not the comma
                    if check_integer(coordinate_string[x]):
                        if (int(coordinate_string[x])<4 and int(coordinate_string[x])!=0):
                            valid += 1 #count valid integer coordinate
                            coordinate_list.append(int(coordinate_string[x]))
                    
            if valid==4: #must have THREE integer coordinates
                get_bool = False
            else:
                print('Invalid format')
    #print("coordinate list: " , coordinate_list)
    return coordinate_list

def write_board(board,number,coordinates):
    w,x,y,z = coordinates[0] -1 , coordinates[1] -1 , coordinates[2] -1 ,coordinates[3] -1
    print('coordinate indices:  ' , w, x,y,z)
    if number!=0:
        board[w][x][y][z] = number
    else:
        board[w][x][y][z] = [True, True, True, True, True, True, True, True, True]
    return board

def write_whole_board():
    board = [[[[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]]],[[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]]],[[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]]]],[[[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]]],[[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]]],[[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]]]],[[[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]]],[[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]]],[[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]],[[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True],[True, True, True, True, True, True, True, True, True]]]]]
    overwrite= True
    print("""Welcome to sudoku solver
To begin, enter puzzle with coordinates in form w,x,y,z
Where 
w is 3 by 9 row
x is 3 by 9 column
y is row within square
z is column within square""")
    print_board(board)
    while overwrite:
        value = get_value()
        coordinates = get_coordinates()
        board = write_board(board, value, coordinates)
        print_board(board)
        if input("Press 'q' to end writing: ") == 'q':
            if input("Are you sure? (y/n) ") == 'y':
                overwrite = False
    return board

#board = write_whole_board()
#print(board)


board2 = [[[[5, 4, 3], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]]], [[2, 1, 6], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]]], [[7, 8, [True, True, True, True, True, True, True, True, True]], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]]]], [[[[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]]], [[[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]]], [[[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]]]], [[[[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]]], [[[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]]], [[[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]], [[True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True]]]]]
board3 = [[[[1, 2, 3], [[True, True, True, True, True, True, True, True, True], 5, 6], [8, 9, 7]], [[[False, False, False, True, True, True, True, True, True], [False, False, False, True, True, True, True, True, True], [False, False, False, True, True, True, True, True, True]], [[True, True, True, False, False, False, True, True, True], [True, True, True, False, False, False, True, True, True], [True, True, True, False, False, False, True, True, True]], [[True, True, True, True, True, True, False, False, False], [True, True, True, True, True, True, False, False, False], [True, True, True, True, True, True, False, False, False]]], [[[False, False, False, True, True, True, True, True, True], [False, False, False, True, True, True, True, True, True], [False, False, False, True, True, True, True, True, True]], [[True, True, True, False, False, False, True, True, True], [True, True, True, False, False, False, True, True, True], [True, True, True, False, False, False, True, True, True]], [[True, True, True, True, True, True, False, False, False], [True, True, True, True, True, True, False, False, False], [True, True, True, True, True, True, False, False, False]]]], [[[[False, True, True, False, True, True, True, False, True], [True, False, True, True, False, True, True, True, False], [True, True, False, True, True, False, False, True, True]], [[False, True, True, False, True, True, True, False, True], [True, False, True, True, False, True, True, True, False], [True, True, False, True, True, False, False, True, True]], [[False, True, True, False, True, True, True, False, True], [True, False, True, True, False, True, True, True, False], [True, True, False, True, True, False, False, True, True]]], [[[False, True, True, True, True, True, True, True, True], [True, False, True, True, True, True, True, True, True], [True, True, False, True, True, True, True, True, True]], [[True, True, True, False, True, True, True, True, True], [True, True, True, True, False, True, True, True, True], [True, True, True, True, True, False, True, True, True]], [[True, True, True, True, True, True, True, False, True], [True, True, True, True, True, True, True, True, False], [True, True, True, True, True, True, False, True, True]]], [[[False, True, True, True, True, True, True, True, True], [True, False, True, True, True, True, True, True, True], [True, True, False, True, True, True, True, True, True]], [[True, True, True, False, True, True, True, True, True], [True, True, True, True, False, True, True, True, True], [True, True, True, True, True, False, True, True, True]], [[True, True, True, True, True, True, True, False, True], [True, True, True, True, True, True, True, True, False], [True, True, True, True, True, True, False, True, True]]]], [[[[False, True, True, False, True, True, True, False, True], [True, False, True, True, False, True, True, True, False], [True, True, False, True, True, False, False, True, True]], [[False, True, True, False, True, True, True, False, True], [True, False, True, True, False, True, True, True, False], [True, True, False, True, True, False, False, True, True]], [[False, True, True, False, True, True, True, False, True], [True, False, True, True, False, True, True, True, False], [True, True, False, True, True, False, False, True, True]]], [[[False, True, True, True, True, True, True, True, True], [True, False, True, True, True, True, True, True, True], [True, True, False, True, True, True, True, True, True]], [[True, True, True, False, True, True, True, True, True], [True, True, True, True, False, True, True, True, True], [True, True, True, True, True, False, True, True, True]], [[True, True, True, True, True, True, True, False, True], [True, True, True, True, True, True, True, True, False], [True, True, True, True, True, True, False, True, True]]], [[[False, True, True, True, True, True, True, True, True], [True, False, True, True, True, True, True, True, True], [True, True, False, True, True, True, True, True, True]], [[True, True, True, False, True, True, True, True, True], [True, True, True, True, False, True, True, True, True], [True, True, True, True, True, False, True, True, True]], [[True, True, True, True, True, True, True, False, True], [True, True, True, True, True, True, True, True, False], [True, True, True, True, True, True, False, True, True]]]]]


#testing deduction
#square1 = [[False, True, True, True, True, True, True, True, True], [False, True, True, True, True, True, True, True, True], [False, True, True, True, True, True, True, True, True], [False, True, True, True, True, True, True, True, True], [False, True, True, True, True, True, True, True, True], [False, True, True, True, True, True, True, True, True], [True, True, True, True, True, True, True, True, True], [False, True, True, True, True, True, True, True, True], [False, True, True, True, True, True, True, True, True]]
#print_subgroup_data(square1)
#new_square = deduce_point_integer_subgroup(square1)
#print("")
#print_subgroup_data(new_square)


def test_program():
    board = write_whole_board()
    go = True
    while go:
        board = update_board(board)
        print_board(board)
        if input("Press 'q' to stop: ") == 'q':
            go = False
    print(board)

def looper():
    play_again = True
    while play_again:
        test_program()
        if input("Press 'q' to end: ") == 'q':
            play_again = False

looper()