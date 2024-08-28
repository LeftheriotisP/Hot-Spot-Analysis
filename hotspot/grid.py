#Cell Class
class Cell:  # Cell class consists of the borders of the cell and the number of points inside the cell
    def __init__(self, min_x, max_x, min_y, max_y, min_t, max_t, count=0):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_t = min_t
        self.max_t = max_t
        self.count = count
        self.getis_ord = None  # Initialize Getis-Ord statistic

#Grid Class
class Grid:
    """
    Grid class is a 3D Array divided into cells

    'm, n, v' is the number of splits on each axis
    m for x, n for y and v for t axis

    'data' is a list of points in the form of (x, y, t)
    """
    def __init__(self, min_x, max_x, min_y, max_y, min_t, max_t, m, n, v, data):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.min_t = min_t
        self.max_t = max_t
        self.m = m
        self.n = n
        self.v = v
        self.hotspots_90th = []
        self.hotspots_getis_ord = []

        # Calculate the step size for each axis
        x_step = (max_x - min_x) / m
        y_step = (max_y - min_y) / n
        t_step = (max_t - min_t) / v
        print(f"x_step: {x_step}, y_step: {y_step}, t_step: {t_step}")
        
        # Cell(min_x, max_x, min_y, max_y, min_t, max_t)
        self.cells = [
            [
                [
                    Cell(
                        min_x + x * x_step, min_x + (x + 1) * x_step,   # Cell size
                        min_y + y * y_step, min_y + (y + 1) * y_step,
                        min_t + t * t_step, min_t + (t + 1) * t_step
                    )
                    for t in range(v)
                ]
                for y in range(n)
            ]
            for x in range(m)
        ]
        
        self.find_points(data)  # Calls the find_points method
        print("\nProcessing grid")
        
    def find_points(self, data):  # Finds the points based on the data and adds them to the count of the cell they are in
        for x, y, t in data:
            cell = self.findCell(x, y, t)  # Calls the findCell method
            if cell:
                cell.count += 1
            else:
                print("Couldn't update count")

    def findCell(self, x, y, t):  # findCell returns the cell that x, y, t belongs to
        col = int((x - self.min_x) / (self.max_x - self.min_x) * self.m)  # (x-x_min)/x_step
        row = int((y - self.min_y) / (self.max_y - self.min_y) * self.n)  # (y-y_min)/y_step
        layer = int((t - self.min_t) / (self.max_t - self.min_t) * self.v)  # (t-t_min)/t_step

        if x == self.max_x:  # If x, y or t = max values
            col = self.m - 1
        if y == self.max_y:
            row = self.n - 1
        if t == self.max_t:
            layer = self.v - 1
            
        if 0 <= col < self.m and 0 <= row < self.n and 0 <= layer < self.v:
            return self.cells[col][row][layer]
        else:
            print("Couldn't find cell")
    pass
    