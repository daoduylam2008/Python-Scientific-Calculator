from tkinter import *
import math
import subprocess
import sys
# tkinter, pygame
# pip / pip3 install <package>


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
    import numpy
except Exception as bug:
    print(bug)
    install("numpy")
    import numpy


button_width = 2
button_height = 2


def sin(alpha): return round(math.sin(math.radians(alpha)), 4)


def cos(alpha): return round(math.cos(math.radians(alpha)), 4)


def tan(alpha): return round(math.tan(math.radians(alpha)), 4)


def cotg(alpha): return 1 / tan(alpha)


def cbrt(value): return value ** (1 / 3)


def regularCalculate(calculation):
    calculation = calculation.replace("^", "**")
    calculation = calculation.replace("\u221A", "math.sqrt")
    calculation = calculation.replace("\u03C0", "math.pi")

    return eval(calculation)


def quadratic_equation_one(a, b):
    return [-b/a]


def quadratic_equation_two(a, b, c):
    delta = b ** 2 - 4 * a * c
    if delta < 0:
        return ["No solution"]
    elif delta > 0:
        x1 = (-b - math.sqrt(delta)) / (2 * a)
        x2 = (-b + math.sqrt(delta)) / (2 * a)
        return [x1, x2]
    else:
        return [-b / (2 * a)]


def quadratic_equation_three(a, b, c, d):
    if a == 0: return ["Can't calculate"]
    else:
        delta = b ** 2 - 3 * a * c
        k = ((9 * a * b * c) - 2 * (b ** 3) - 27 * a * (d ** 2)) / (2 * math.sqrt(abs(delta) ** 3))

        if delta > 0:
            if abs(k) <= 1:
                t = [0, (2 * math.pi) / 3, -(2 * math.pi) / 3]
                solutions = [((2 * math.sqrt(delta) * (cos(math.radians(math.acos(math.radians(k))) + i)) - b) / (3 * a))
                             for i in t]

                return solutions
            else:
                t = cbrt(abs(k) + math.sqrt(k ** 2 - 1)) + cbrt(abs(k) - math.sqrt(k ** 2 - 1))
                l = (math.sqrt(delta) * abs(k)) / (3 * a * k)
                solution = l * t - (b / (3 * a))

                return [solution]
        elif delta == 0:
            t = cbrt(abs(k) + math.sqrt(k ** 2 - 1)) + cbrt(abs(k) - math.sqrt(k ** 2 - 1))
            l = (math.sqrt(delta) / (3 * a))
            solution = l * t - (b / (3 * a))

            return [solution]
        else:
            x = (-b + cbrt(b ** 3 - 27 * (a ** 2) * d)) / 3 * a
            return [x]


def system_of_equations_with_two_unknowns(a, b, c, d, e, f):
    if (a / d == b / e != c / f) or (a / d == b / e == c / f):
        return ["No Solution"]
    elif a / d == b / e == c / f:
        return ["Infinity solution"]
    else:
        delta = e * a - b * d
        y = (f * a - c * d) / delta
        x = (b * f - e * c) / (-delta)
        return [x, y]


def system_of_equations_with_three_unknowns(a, b, c, d,
                                            e, f, g, h,
                                            i, j, k, l):

    A = numpy.array([[a, b, c], [e, f, g], [i, j, k]])
    b = numpy.array([d, h, l])
    try:
        solutions = [round(i, 4) for i in numpy.linalg.solve(A, b).tolist()]
    except Exception as bug:
        print(bug)
        if a / e == b / f == c / g == d / h:
            solutions = ["Infinity solutions"]
        elif a / i == b / j == c / k == l / d:
            solutions = ["Infinity solutions"]
        elif e / i == f / j == g / k == h / l:
            solutions = ["Infinity solutions"]
        else:
            solutions = ["No solution"]

    return solutions


class TextWithVar(Text):
    '''A text widget that accepts a 'textvariable' option'''

    def __init__(self, parent, *args, **kwargs):
        try:
            self._textvariable = kwargs.pop("textvariable")
        except KeyError:
            self._textvariable = None

        Text.__init__(self, parent, *args, **kwargs)

        # if the variable has data in it, use it to initialize
        # the widget
        if self._textvariable is not None:
            self.insert("1.0", self._textvariable.get())

        # this defines an internal proxy which generates a
        # virtual event whenever text is inserted or deleted
        self.tk.eval('''
            proc widget_proxy {widget widget_command args} {

                # call the real tk widget command with the real args
                set result [uplevel [linsert $args 0 $widget_command]]

                # if the contents changed, generate an event we can bind to
                if {([lindex $args 0] in {insert replace delete})} {
                    event generate $widget <<Change>> -when tail
                }
                # return the result from the real widget command
                return $result
            }
            ''')

        # this replaces the underlying widget with the proxy
        self.tk.eval('''
            rename {widget} _{widget}
            interp alias {{}} ::{widget} {{}} widget_proxy {widget} _{widget}
        '''.format(widget=str(self)))

        # set up a binding to update the variable whenever
        # the widget changes
        self.bind("<<Change>>", self._on_widget_change)

        # set up a trace to update the text widget when the
        # variable changes
        if self._textvariable is not None:
            self._textvariable.trace("wu", self._on_var_change)

    def _on_var_change(self, *args):
        '''Change the text widget when the associated textvariable changes'''

        # only change the widget if something actually
        # changed, otherwise we'll get into an endless
        # loop
        text_current = self.get("1.0", "end-1c")
        var_current = self._textvariable.get()
        if text_current != var_current:
            self.delete("1.0", "end")
            self.insert("1.0", var_current)

    def _on_widget_change(self, event=None):
        '''Change the variable when the widget changes'''
        if self._textvariable is not None:
            self._textvariable.set(self.get("1.0", "end-1c"))


class Calculator(Frame):
    def __init__(self):
        super().__init__()
        self.string = StringVar()
        self.solution = StringVar()
        self.formation = StringVar()
        self.option_choice = StringVar()
        self.option_choice.set("0")

        self.calculation = []
        self.expression = ["+", "-", "*", "/", "=", "^"]
        self.options = ["0", "1", "2", "3", "4"]

        self.initUI()

    def initUI(self):
        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)

        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)

        # Menu button

        # ROW 1:
        frame = Frame(self, width=5)
        frame.grid(row=0, columnspan=5)
        self.entry = TextWithVar(frame, font=("Andalus", 20, "bold"), textvariable=self.string, width=23, height=3)
        self.entry.bind("<Return>", self.onEqualPressed)
        self.entry.pack(side="left")
        solutionLabel = Label(frame, font=("Andalus", 20, "bold"), textvariable=self.solution)
        solutionLabel.pack(side="right")

        # ROW 2:
        calc = Button(self, text="=0", bg="grey", fg="black", command=lambda: self.addValue("=0"), height=button_height,
                     padx=10, pady=10, width=button_width)
        calc.grid(row=2, column=0)
        sev = Button(self, text="7", bg="grey", fg="black", command=lambda: self.addValue("=0"), height=button_height,
                     padx=10, pady=10, width=button_width)
        sev.grid(row=2, column=1)
        eig = Button(self, text="8", bg="grey", fg="black", command=lambda: self.addValue("8"), height=button_height,
                     padx=10, pady=10, width=button_width)
        eig.grid(row=2, column=2)
        nin = Button(self, text="9", bg="grey", fg="black", command=lambda: self.addValue("9"), height=button_height,
                     padx=10, pady=10, width=button_width)
        nin.grid(row=2, column=3)
        delete = Button(self, text="DEL", bg="grey", fg="black", command=self.onDELPressed, height=button_height,
                        padx=10, pady=10, width=button_width)
        delete.grid(row=2, column=4)
        ac = Button(self, text="AC", bg="grey", fg="black", command=self.onACPressed, height=button_height, padx=10,
                    pady=10, width=button_width)
        ac.grid(row=2, column=5)
        sin_btn = Button(self, text="sin", bg="grey", fg="black", command=lambda: self.addValue("sin("),
                         height=button_height, padx=10,
                         pady=10, width=button_width)
        sin_btn.grid(row=2, column=6)

        # ROW 3:
        exponential = Button(self, text="x^y", bg="grey", fg="black", command=lambda: self.addValue("^("),
                        height=button_height,
                        padx=10, pady=10, width=button_width)
        exponential.grid(row=3, column=0)
        fou = Button(self, text="4", bg="grey", fg="black", command=lambda: self.addValue("4"), height=button_height,
                     padx=10, pady=10, width=button_width)
        fou.grid(row=3, column=1)
        fiv = Button(self, text="5", bg="grey", fg="black", command=lambda: self.addValue("5"), height=button_height,
                     padx=10, pady=10, width=button_width)
        fiv.grid(row=3, column=2)
        six = Button(self, text="6", bg="grey", fg="black", command=lambda: self.addValue("6"), height=button_height,
                     padx=10, pady=10, width=button_width)
        six.grid(row=3, column=3)
        mul = Button(self, text="*", bg="grey", fg="black", command=lambda: self.addValue("*"), height=button_height,
                     padx=10, pady=10, width=button_width)
        mul.grid(row=3, column=4)
        div = Button(self, text="/", bg="grey", fg="black", command=lambda: self.addValue("/"),
                     height=button_height, padx=10, pady=10, width=button_width)
        div.grid(row=3, column=5)
        cos_btn = Button(self, text="cos", bg="grey", fg="black", command=lambda: self.addValue("cos("),
                         height=button_height, padx=10,
                         pady=10, width=button_width)
        cos_btn.grid(row=3, column=6)

        # ROW 4:
        square_root = Button(self, text="\u221Ax", bg="grey", fg="black", command=lambda: self.addValue("\u221A("),
                             height=button_height, padx=10, pady=10, width=button_width)
        square_root.grid(row=4, column=0)
        one = Button(self, text="1", bg="grey", fg="black", command=lambda: self.addValue("1"), height=button_height,
                     padx=10, pady=10, width=button_width)
        one.grid(row=4, column=1)
        two = Button(self, text="2", bg="grey", fg="black", command=lambda: self.addValue("2"), height=button_height,
                     padx=10, pady=10, width=button_width)
        two.grid(row=4, column=2)
        thr = Button(self, text="3", bg="grey", fg="black", command=lambda: self.addValue("3"), height=button_height,
                     padx=10, pady=10, width=button_width)
        thr.grid(row=4, column=3)

        mns = Button(self, text="-", bg="grey", fg="black", command=lambda: self.addValue("-"), height=button_height,
                     padx=10, pady=10, width=button_width)
        mns.grid(row=4, column=4)
        pls = Button(self, text="+", bg="grey", fg="black", command=lambda: self.addValue("+"),
                     height=button_height, padx=10, pady=10, width=button_width)
        pls.grid(row=4, column=5)
        tan_btn = Button(self, text="tan", bg="grey", fg="black", command=lambda: self.addValue("tan("),
                         height=button_height, padx=10,
                         pady=10, width=button_width)
        tan_btn.grid(row=4, column=6)

        # ROW 5:
        pi_btn = Button(self, text="x", bg="grey", fg="black", command=lambda: self.addValue("x"),
                        height=button_height, padx=10, pady=10, width=button_width)
        pi_btn.grid(row=5, column=0)
        zer = Button(self, text="0", bg="grey", fg="black", command=lambda: self.addValue("0"), height=button_height,
                     padx=10, pady=10, width=button_width)
        zer.grid(row=5, column=1)
        dot = Button(self, text=".", bg="grey", fg="black", command=lambda: self.addValue("."), height=button_height,
                     padx=10, pady=10, width=button_width)
        dot.grid(row=5, column=2)
        equ = Button(self, text="=", bg="grey", fg="black", command=self.onEqualPressed, height=button_height, padx=10,
                     pady=10, width=button_width)
        equ.grid(row=5, column=3)
        left_r = Button(self, text="(", bg="grey", fg="black", command=lambda: self.addValue("("),
                        height=button_height, padx=10, pady=10, width=button_width)
        left_r.grid(row=5, column=4)
        right_r = Button(self, text=")", bg="grey", fg="black", command=lambda: self.addValue(")"),
                         height=button_height, padx=10, pady=10, width=button_width)
        right_r.grid(row=5, column=5)
        cotg_btn = Button(self, text="cotg", bg="grey", fg="black", command=lambda: self.addValue("cotg("),
                          height=button_height, padx=10,
                          pady=10, width=button_width)
        cotg_btn.grid(row=5, column=6)

        self.pack()

    def addValue(self, value):
        self.calculation.clear()
        self.entry.insert(self.entry.index(INSERT), value)
        self.calculation = [i for i in self.string.get()]
        self.calculation.insert(int(self.entry.index(INSERT).split(".")[1]) - 1, value)

    def clearValues(self):
        self.calculation.clear()
        self.string.set("")

    def onACPressed(self):
        self.clearValues()

    def onDELPressed(self):
        pos = self.entry.index(INSERT).split(".")
        self.calculation.pop(int(pos[1]) - 1)
        self.string.set("".join(self.calculation))

    def onEqualPressed(self, *args):
        string = self.string.get().replace('=0', '')
        print(string)
        if "x^(3)" in string:
            argument = string
            argument = argument.split("x^(3)")
            argument = [argument[0], argument[1].split("x^2")[0]] + argument[1].split("x^2")[1].split("x")

            arguments = [regularCalculate(i) for i in argument]

            solutions = quadratic_equation_three(int(arguments[0]), int(arguments[1]), int(arguments[2]), int(arguments[3]))
            sol = ["Solutions: \n"]

            for solution in solutions:
                sol.append("x" + str(solutions.index(solution) + 1) + "=" + str(solution) + "\n")
            self.solution.set("".join(sol))
        elif "x^(2)" in string:
            argument = string
            argument = argument.split("x^(2)")
            print(argument)
            if len(argument) == 2:
                argument[0] = '1'
            argument = [argument[0]] + argument[1].split("x")
            arguments = [regularCalculate(i) for i in argument]

            solutions = quadratic_equation_two(int(arguments[0]), int(arguments[1]), int(arguments[2]))
            if solutions[0] == "No solution":
                self.solution.set("No solution")
            else:
                sol = ["Solutions: \n"]
                for solution in solutions:
                    sol.append("x" + str(solutions.index(solution) + 1) + "=" + str(solution) + "\n")

                self.solution.set("".join(sol))
        elif "y" in string:
            argument = string

            # First line calculate
            argument1 = argument.split("\n")[0]
            argument1 = argument1.replace("=", "")
            argument1 = argument1.replace(" ", "")
            arguments1 = [regularCalculate(argument1.split("x")[0]), regularCalculate(argument1.split("x")[1].split("y")[0]),
                          regularCalculate(argument1.split("x")[1].split("y")[1])]

            # Second line calculate
            argument2 = argument.split("\n")[1]
            argument2 = argument2.replace("=", "")
            argument2 = argument2.replace(" ", "")
            arguments2 = [regularCalculate(argument2.split("x")[0]), regularCalculate(argument2.split("x")[1].split("y")[0]),
                          regularCalculate(argument2.split("x")[1].split("y")[1])]

            solutions = system_of_equations_with_two_unknowns(arguments1[0], arguments1[1], arguments1[2], arguments2[0], arguments2[1], arguments2[2])

            if solutions[0] == "No solution":
                self.solution.set("No solution")
            elif solutions[0] == "Infinity solutions":
                self.solution.set("Infinity solution")
            else:
                sol = ["Solutions: \n"]
                for solution in solutions:
                    sol.append("x" + str(solutions.index(solution) + 1) + "=" + str(solution) + "\n")

                self.solution.set("".join(sol))
        elif "z" in string:
            argument = string
            # First line calculate
            argument1 = argument.split("\n")[0]
            argument1 = argument1.replace("=", "")
            argument1 = argument1.replace(" ", "")
            arguments1 = ([regularCalculate(argument1.split("x")[0]),
                           regularCalculate(argument1.split("x")[1].split("y")[0])]
                          + [regularCalculate(i) for i in argument1.split("x")[1].split("y")[1].split("z")])
            # Second line calculate
            argument2 = argument.split("\n")[1]
            argument2 = argument2.replace("=", "")
            argument2 = argument2.replace(" ", "")
            arguments2 = ([regularCalculate(argument2.split("x")[0]), regularCalculate(argument2.split("x")[1].split("y")[0])]
                          + [regularCalculate(i) for i in argument2.split("x")[1].split("y")[1].split("z")])

            # Third line calculate
            argument3 = argument.split("\n")[2]
            argument3 = argument3.replace("=", "")
            argument3 = argument3.replace(" ", "")
            arguments3 = ([regularCalculate(argument3.split("x")[0]), regularCalculate(argument3.split("x")[1].split("y")[0])]
                          + [regularCalculate(i) for i in argument3.split("x")[1].split("y")[1].split("z")])

            solutions = system_of_equations_with_three_unknowns(arguments1[0], arguments1[1], arguments1[2], arguments1[3], arguments2[0], arguments2[1], arguments2[2], arguments2[3], arguments3[0], arguments3[1], arguments3[2], arguments3[3])

            sol = ["Solutions: \n"]

            for solution in solutions:
                sol.append("x" + str(solutions.index(solution) + 1) + "=" + str(solution) + "\n")
            self.solution.set("".join(sol))
        else:
            try:
                result = regularCalculate(string)
                self.string.set(result)
                self.calculation.clear()
                self.calculation.append(str(result))
            except:
                self.solution.set("Math Error: Can't solve")

    def onModePressed(self):
        if self.option_choice.get() == "0":
            self.string.set("")
        elif self.option_choice.get() == "1":
            self.string.set("ax^2 + bx + c")
        elif self.option_choice.get() == "2":
            self.string.set("ax^3 + bx^2 + cx + d")
        elif self.option_choice.get() == "3":
            self.string.set("ax + by = c\ndx + ey = f")
        elif self.option_choice.get() == "4":
            self.string.set("ax + by + cz = d\nex + fy + gz = h\nix + jy + kz = l")


def main():
    root = Tk()
    Calculator()
    root.mainloop()


if __name__ == '__main__':
    main()
