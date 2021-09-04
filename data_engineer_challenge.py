import sys

def manage_snake(snk_raw):
	"""
	gets the snake in string form and returns the snake as a list

	@param snk -> string representation of the snake (eg: '[[2,2],[3,2],[3,1],[3,0],[2,0],[1,0],[0,0]]')

	@returns [[int,int]] snake representation
	"""
	snk = snk_raw[2:-2].split('],[')
	snk = [[int(row),int(col)] for row,col in (point.split(',') for point in snk)]
	
	return snk



def step(rows,cols,snk,direction):
	"""
	takes the snake, direction and bounds of the board and returns the snake moved in the given direction

	@param rows -> int number of rows in the board
	@param cols -> int number of columns in the board
	@param snk -> [[int,int]] snake representation
	@param direction -> string options:'U','D','R','L'

	@returns [[int,int]] snake representation
	"""
	if direction == 'U':
		head_row = snk[0][0]
		head_col = snk[0][1] + 1
		if head_col >= cols: return None
	elif direction == 'D':
		head_row = snk[0][0]
		head_col = snk[0][1] - 1
		if head_col < 0: return None
	elif direction == 'R':
		head_row = snk[0][0] + 1
		head_col = snk[0][1]
		if head_row >= rows: return None
	elif direction == 'L':
		head_row = snk[0][0] - 1 
		head_col = snk[0][1]
		if head_row < 0: return None

	aux_snk = snk[:] #making a copy because pop and insert cause troubles when passing lists by refference and re-using them
	# pop, check and insert in this order because all the moves are simmultaneous
	# and the head can occupy the place of the tail in the next step
	aux_snk.pop()
	if [head_row,head_col] in aux_snk: return None
	aux_snk.insert(0,[head_row,head_col])

	return aux_snk

def compute_snake(snk,path):
	"""
	takes the snake, and the path, and returns the snake after moving said path

	@param snk -> [[int,int]] snake representation
	@param direction -> string eg: 'ULLRD'

	@returns [[int,int]] snake representation
	"""
	if path == '': return snk
	snk = step(rows,cols,snk,path[0])
	path = path[1:]
	return compute_snake(snk,path)

def compute_valid_paths(snk,paths,depth):
	"""
	recursive search for valid paths, all non valid paths are pruned so only potential candidates are evaluated each level

	@param snk -> [[int,int]] snake representation
	@param paths -> list of paths with potential to become a final path
	@param depth -> remaining depth, stops at 0

	@returns list of valid paths
	"""
	if depth == 0: return paths
	valid_paths = []
	#for each potential path, we try to see if each direction is valid
	for path in paths:
		for direction in directions:
			aux_snk = compute_snake(snk,path)
			if aux_snk is not None:
				if step(rows,cols,aux_snk,direction) is not None:
					#if the step function returns a non None value, the path is valid
					valid_paths += [path+direction]
	return compute_valid_paths(snk,valid_paths,depth-1)

def print_board(rows,cols,snk):
	"""
	prints a visual representation of the state of the board
	"""
	board = [['0' for i in range(cols)] for j in range(rows)]
	board[snake[0][0]][snake[0][1]] = 'H'
	for point in snk[1:-1]:
		board[point[0]][point[1]] = 'S'
	board[snake[-1][0]][snake[-1][1]] = 'T'

	for row in board:
		print(row)

if __name__ == "__main__":

	board_raw = sys.argv[1]
	#must be passed without spaces because of how argument capture works in bash 
	# valid example ->'[[5,5],[5,4],[4,4],[4,5]]' 
	# not valid example -> '[[5,5], [5,4], [4,4], [4,5]]'
	snake_raw = sys.argv[2] 
	max_depth = int(sys.argv[3])

	snake = manage_snake(snake_raw)
	rows,cols = board_raw[1:-1].split(',')
	rows = int(rows)
	cols = int(cols)

	print_board(rows,cols,snake)

	directions = ['U','D','R','L']

	#first layer computed this way because param paths of compute_valid_paths assumes that all the paths in said list are valid
	initial_paths = []
	aux_snake = snake
	if step(rows,cols,aux_snake,'U') is not None: initial_paths+=['U']
	if step(rows,cols,aux_snake,'D') is not None: initial_paths+=['D']
	if step(rows,cols,aux_snake,'R') is not None: initial_paths+=['R']
	if step(rows,cols,aux_snake,'L') is not None: initial_paths+=['L']

	if max_depth == 1: 
		print('valid paths are: ',initial_paths)
		print('number of paths is:', len(initial_paths))
		exit(0)

	valid_paths = compute_valid_paths(snake,initial_paths,max_depth-1)
	print('valid paths are: ',valid_paths)
	print('number of paths is:', len(valid_paths))




