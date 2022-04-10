import tkinter as tk


class View:
    def __init__(self, montecarlo):
        self.origin = (400, 400)
        self.scale = 15
        self.win = tk.Tk()

        tk.Frame(self.win).grid(row=0, column=0)
        self.frame = self.win.grid_slaves(0, 0)[0]

        tk.Canvas(self.win, highlightthickness=2, highlightbackground="black", width=800, height=800).grid(
            row=1, column=0)
        self.can = self.win.grid_slaves(1, 0)[0]

        tk.Label(self.frame, text="Aire attendue :", font=('Arial', 13)).grid(row=0, column=0, padx=(50, 50))
        tk.Label(self.frame, text="0", font=('Arial', 13)).grid(row=1, column=0, padx=(50, 50))
        tk.Label(self.frame, text="Aire calculée :", font=('Arial', 13)).grid(row=0, column=1, padx=(50, 50))
        tk.Label(self.frame, text="0", font=('Arial', 13)).grid(row=1, column=1, padx=(50, 50))
        tk.Label(self.frame, text="Nombre de points :", font=('Arial', 13)).grid(row=0, column=2, padx=(50, 50))
        tk.Label(self.frame, text="0", font=('Arial', 13)).grid(row=1, column=2, padx=(50, 50))

        self.expectedAreaLabel = self.frame.grid_slaves(1, 0)[0]
        self.areaLabel = self.frame.grid_slaves(1, 1)[0]
        self.numberOfPointsLabel = self.frame.grid_slaves(1, 2)[0]

        self.pointsToDraw = []
        montecarlo.set_view(self)
        self.create_circle_at(self.can, 0, 0, 10, "black")
        self.win.mainloop()

    def update_canvas(self):
        self.create_circle_at(self.can, 0, 0, 10, "black")

    def create_circle_at(self, can, x, y, r, color):  # center coordinates, radius
        x_transform = int(x * self.scale) + self.origin[0]
        y_transform = int(y * self.scale) + self.origin[1]
        r_rescaled = int(r * self.scale)
        x0 = x_transform - r_rescaled
        y0 = y_transform - r_rescaled
        x1 = x_transform + r_rescaled
        y1 = y_transform + r_rescaled
        return can.create_oval(x0, y0, x1, y1, fill=color)

    def create_circle_in_can_at(self, x, y, r, color):  # center coordinates, radius
        x_transform = int(x * self.scale) + self.origin[0]
        y_transform = int(y * self.scale) + self.origin[1]
        r_rescaled = int(r * self.scale)
        x0 = x_transform - r_rescaled
        y0 = y_transform - r_rescaled
        x1 = x_transform + r_rescaled
        y1 = y_transform + r_rescaled
        return self.can.create_oval(x0, y0, x1, y1, fill=color)

    def create_rectangle_at(self, can, x, y, h_2, l_2, color):
        x_transform = int(x * self.scale) + self.origin[0]
        y_transform = int(y * self.scale) + self.origin[1]
        h_2_rescaled = int(h_2 * self.scale)
        l_2_rescaled = int(l_2 * self.scale)
        # top left corner
        x0 = x_transform - l_2_rescaled
        y0 = y_transform - h_2_rescaled
        # bottom right corner
        x1 = x_transform + l_2_rescaled
        y1 = y_transform + h_2_rescaled
        return can.create_rectangle(x0, y0, x1, y1, fill=color)
