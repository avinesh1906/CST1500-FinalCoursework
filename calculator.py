# import libraries
from tkinter import *
import math

# global variable
calculation = ""
expression = "0"
history = []


# class to start the application
class App(Tk):
    """
        App Class
        Tk: Toplevel widget of Tk which represents mostly the main window of an application.
            It has an associated Tcl interpreter
        .
        .
        This class will:
        1) Create a frame
        2) Format the frame
        3) Allow to switch frame by destroying the previous used frame
    """

    # initialise constructor
    def __init__(self):
        super(App, self).__init__()
        self._frame = None
        self.switchFrame(Calculator)

    # function to switch Frame
    def switchFrame(self, class_Frame):
        newFrame = class_Frame(self)
        if self._frame is not None:
            self._frame.destroy()

        self._frame = newFrame
        self._frame.pack()


# subclass of frame
class History(Frame):
    """
        Standard Class of standard calculator
        Frame: Frame widget which may contain other widgets and can have a 3D border.
        .
        .
        This class will display the history of calculation
    """

    # initialise constructor
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master.geometry("270x250+650+300")  # width by height + position in the window
        self.master.title("History")  # set the window title
        self.master.resizable(0, 0)  # this prevent from resizing the window

        ''' Frame for history'''
        History_Frame = Frame(self, width=270, height=250, bg="azure2")
        History_Frame.pack(side=TOP)

        Button(History_Frame, text="BACK", font=('Serif', 10), command=lambda: master.switchFrame(Calculator),
               bg="wheat3").place(x=100, y=210)

        # check if the history list is empty
        if len(history) != 0:
            yAxis = 10
            # display the content of history in history_Frame
            for row in history:
                Label(History_Frame, text=row, font=('Serif', 12), bg="azure2").place(x=25, y=yAxis)
                yAxis += 25
        else:
            #  display "No History" if history is empty
            Label(History_Frame, text="No History", font=('Serif', 15), bg="azure2").place(x=85, y=65)


class Calculator(Frame):
    """
        Scientific Class of scientific calculator
        Frame: Frame widget which may contain other widgets and can have a 3D border.
        .
        .
        This class will carry out the basic operations:
        1) Addition / Subtraction
        2) Multiplication / Division
        3) Equal / Clear
        4) Display errors : 1. ZeroDivisionError 2.SyntaxError as ERROR

        Also, it will carry out the more complex operations:
        1) log()
        2) power
        3) square root
        4) exponential
    """

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master.geometry("328x386+650+300")  # width by height
        self.master.title("Calculator")  # set the window title
        self.master.resizable(0, 0)  # this prevent from resizing the window

        # Clears text field
        def ce():
            global calculation
            global expression
            calculation = ""
            expression = "0"
            output_text.set(expression)

        # Processes calculation and writes answer
        def equal():
            global calculation
            global expression
            # Exception handling
            try:
                # calculate the result by using eval
                result = str(eval(calculation))
                output_text.set(result)
                history.append(f"{expression} = {result}")
                calculation = ""  # set calculation to default
                expression = "0"
            except (ZeroDivisionError, SyntaxError):
                output_text.set("ERROR")  # display errors if divide by zero or syntax error

        # Writes constants
        # Used when button has different display and calculation
        def button_func(name, syntax):
            global expression
            global calculation
            if expression == "0":
                calculation = ""
                expression = ""
            expression += name  # this store the expression to be displayed on the screen
            calculation += str(syntax)  # this store the background calculation
            output_text.set(expression)  # display the expression

        output_text = StringVar()  # creating and accessing variables in the interpreter
        output_text.set("0")  # set zero to the display by default

        # Left frame for display and buttons
        left_frame = Frame(self)
        left_frame.pack(side=LEFT)

        ''' Frame for display '''
        display_frame = Frame(left_frame, width=328, height=70, bd=0, highlightcolor="LightSkyBlue3",
                              highlightbackground="gray", highlightthickness=2)

        display_frame.pack(side=TOP)

        input_Field = Entry(display_frame, font=('arial', 18, 'bold'), textvariable=output_text, width=25,
                            bg="#eee",
                            bd=15,
                            justify=RIGHT)

        input_Field.grid(row=0, column=0)
        input_Field.pack(
            ipady=10)  # How many pixels to pad widget, horizontally and vertically, inside widget's borders.

        ''' Frame for button '''
        main_frame = Frame(left_frame, width=328, height=275, bg="gray")
        main_frame.pack()

        # list to store button names
        button_names = ["π", "e^", "CE", "Abs(",
                        "^2", "(", ")", "x10^(",
                        "√(", "^", "ln(", "/",
                        "7", "8", "9", "*",
                        "4", "5", "6", "-",
                        "1", "2", "3", "+",
                        "📜", "0", "●", "="]

        # list to store button syntax
        button_syntax = ["math.pi", "(math.e)**", "", "abs(",
                         "**2", "(", ")", "*10**(",
                         "math.sqrt(", "**", "math.log(", "/",
                         "7", "8", "9", "*",
                         "4", "5", "6", "-",
                         "1", "2", "3", "+",
                         "", "0", ".", ""]

        # for-loop: display the buttons and carry out specific actions according to the button
        i = 0  # counter for index
        for row in range(0, 7):
            for column in range(0, 4):
                # make use of if statement to execute different action and display different button color
                if button_names[i] == "CE":
                    Button(main_frame, text="CE", bg="lightcoral", width=10, height=2, command=lambda: ce()).grid(
                        row=row, column=column, padx=1, pady=1)

                elif button_names[i] == "📜":
                    Button(main_frame, text="📜", bg="DarkOrange4", width=10, height=2,
                           command=lambda: master.switchFrame(History)).grid(
                        row=row, column=column, padx=1, pady=1)

                elif button_names[i] == "=":
                    Button(main_frame, text="=", width=10, height=2, bg="salmon4", command=lambda: equal()).grid(
                        row=row, column=column, padx=1, pady=1)

                elif button_names[i] == "●":
                    Button(main_frame, text=button_names[i], width=10, height=2, bg="coral",
                           command=lambda name=".", syntax=button_syntax[i]: button_func(name, syntax)).grid(
                        row=row, column=column, padx=1, pady=1)

                elif button_names[i].isdigit():
                    Button(main_frame, text=button_names[i], width=10, height=2, bg="NavajoWhite2",
                           command=lambda name=button_names[i], syntax=button_syntax[i]: button_func(name,
                                                                                                     syntax)).grid(
                        row=row, column=column, padx=1, pady=1)

                else:
                    Button(main_frame, text=button_names[i], width=10, height=2, bg="burlywood4",
                           command=lambda name=button_names[i], syntax=button_syntax[i]: button_func(name,
                                                                                                     syntax)).grid(
                        row=row, column=column, padx=1, pady=1)

                i += 1  # increment counter


# main function
def main():
    # start the application
    app = App()
    app.mainloop()


# the value of __name__ is set to '__main__' when module run as main program
if __name__ == '__main__':
    main()
