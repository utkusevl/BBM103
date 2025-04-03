import sys

#Reads the input file and returns costs and matrix.
def read_input(input_file):

    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()


        costs = read_costs(lines[0])
        matrix = read_matrix(lines[1:])

        return costs, matrix

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        raise
    except ValueError as ve:
        print(f"Input format error: {ve}")
        raise

#Reads the costs from the first line of the input file.
def read_costs(line):

    try:
        costs = tuple(map(int, line.strip().split()))
        if len(costs) != 3:
            raise ValueError("Costs must have exactly 3 values.")
        return costs
    except ValueError:
        raise ValueError("Costs must be integers separated by spaces.")

#Reads the matrix from the remaining lines of the input file.
def read_matrix(lines):

    matrix = []
    for line in lines:
        row = []
        for value in line.split():
            try:
                cell = int(value)
                if cell not in (0, 1):
                    raise ValueError("Matrix can only contain 0s and 1s.")
                row.append(cell)
            except ValueError:
                raise ValueError("Matrix can only contain integers 0 or 1.")
        matrix.append(row)
    return matrix

#Calculates the cost of a cell based on its surroundings.
def calculate_cell_cost(matrix, costs, i, j):

    rows, cols = len(matrix), len(matrix[0])
    cost1, cost2, cost3 = costs

    diagonal_neighbors = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    hv_neighbors = [(-1, 0), (1, 0), (0, -1), (0, +1)]

    for dx, dy in hv_neighbors:
        ni, nj = i + dx, j + dy
        if 0 <= ni < rows and 0 <= nj < cols and matrix[ni][nj] == 0:
            return cost3


    for dx, dy in diagonal_neighbors:
        ni, nj = i + dx, j + dy
        if 0 <= ni < rows and 0 <= nj < cols and matrix[ni][nj] == 0:
            return cost2

    return cost1



    hv_sinkholes = False
    for dx, dy in hv_neighbors:
        ni, nj = i + dx, j + dy
        if 0 <= ni < rows and 0 <= nj < cols and matrix[ni][nj] == 0:
            hv_sinkholes = True
            break


    if hv_sinkholes:
        return cost3
    elif diagonal_sinkholes:
        return cost2
    else:
        return cost1

#Finds a path recursively while calculating costs and backtracking.
def find_path(matrix, costs, i, j, visited, path, current_cost, best_cost, best_path):

    rows, cols = len(matrix), len(matrix[0])
    cost = 0

    visited[i][j] = True
    path.append((i, j))
    if j == 0 and matrix[i][j] == 1:
        cost += calculate_cell_cost(matrix, costs, i, j)


    if j == cols - 1:
        if current_cost < best_cost[0]:
            best_cost[0] = current_cost
            best_path[0] = path[:]
        visited[i][j] = False
        path.pop()
        return


    directions = [(i, j + 1),  (i - 1, j),  (i + 1, j),  (i, j - 1)]
    for ni, nj in directions:
        if 0 <= ni < rows and 0 <= nj < cols and not visited[ni][nj] and matrix[ni][nj] == 1:
            new_cost = current_cost + calculate_cell_cost(matrix, costs, ni, nj)
            if new_cost < best_cost[0]:
                find_path(matrix, costs, ni, nj, visited, path, new_cost + cost, best_cost, best_path)


    visited[i][j] = False
    path.pop()


def main():

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    costs, matrix = read_input(input_file)
    rows, cols = len(matrix), len(matrix[0])


    visited = [[False] * cols for _ in range(rows)]
    best_cost = [float('inf')]
    best_path = [[]]
    path = []


    for i in range(rows):
        if matrix[i][0] == 1:
            find_path(matrix, costs, i, 0, visited, path, 0, best_cost, best_path)



    marking(matrix, best_path[0])
    writing_file(matrix , best_cost,output_file)

#Marks the best path on the matrix by replacing '1' with 'X' for the given path and writes the modified matrix to a file.
def marking(matrix, best_path):

    for i, j in best_path:
        if matrix[i][j] == 1:
           matrix[i][j] = 'X'


def writing_file(matrix , best_cost,output_file):
    with open(output_file, 'w') as file:
        if best_cost == [float('inf')]:
            file.write("There is no possible route!")
        else :
            file.write(f"Cost of the route: {best_cost[0]}")
            for row in matrix:
                file.write( "\n" + " ".join(map(str,row)))


if __name__ == "__main__":
    main()
