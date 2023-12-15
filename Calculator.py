## Calculator
## Pip Install: pip install tkintertable
## Run: python Calculator.py

import tkinter as tk

from fractions import Fraction


class CalculatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        self.master.resizable(False, False)
        self.expression = tk.StringVar()
        self.to_fraction = False

        entry = tk.Entry(
            master,
            textvariable=self.expression,
            font=("Helvetica", 24),
            bd=0,
            insertwidth=12,
            width=14,
            justify="right",
        )
        entry.grid(row=0, column=0, columnspan=4, sticky="nsew", ipadx=10, ipady=10)
        entry.configure(readonlybackground="#2C2C2C", fg="white")
        entry.config(state="readonly")

        buttons = [
            ("AC", 2, "#A7A7A7", "#BBBBBB"),
            ("←", 1, "#A7A7A7", "#BBBBBB"),
            ("/", 1, "#DFA200", "#FFC669"),
            ("7", 1, "#4E4E4E", "#BBBBBB"),
            ("8", 1, "#4E4E4E", "#BBBBBB"),
            ("9", 1, "#4E4E4E", "#BBBBBB"),
            ("x", 1, "#DFA200", "#FFC669"),
            ("4", 1, "#4E4E4E", "#BBBBBB"),
            ("5", 1, "#4E4E4E", "#BBBBBB"),
            ("6", 1, "#4E4E4E", "#BBBBBB"),
            ("-", 1, "#DFA200", "#FFC669"),
            ("1", 1, "#4E4E4E", "#BBBBBB"),
            ("2", 1, "#4E4E4E", "#BBBBBB"),
            ("3", 1, "#4E4E4E", "#BBBBBB"),
            ("+", 1, "#DFA200", "#FFC669"),
            ("0", 2, "#4E4E4E", "#BBBBBB"),
            (".", 1, "#4E4E4E", "#BBBBBB"),
            ("=", 1, "#e74c3c", "#FF6969"),
            ("(", 1, "#A7A7A7", "#2C2C2C"),
            (")", 1, "#A7A7A7", "#2C2C2C"),
            ("Xⁿ", 1, "#A7A7A7", "#2C2C2C"),
            ("a/b", 1, "#A7A7A7", "#2C2C2C"),
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            button_text, col_span, color, border_color = button
            fg_color = "white"

            if button_text == "AC" or button_text == "←":
                fg_color = "black"

            tk.Button(
                master,
                text=button_text,
                padx=20,
                pady=20,
                font=("Helvetica", 14),
                command=lambda b=button_text: self.button_click(b),
                bg=color if color else "#3498db",
                fg="white",
                activebackground=border_color,
                activeforeground=fg_color,
                borderwidth=0,
                relief="ridge",
                bd=0,
            ).grid(
                row=row_val,
                column=col_val,
                columnspan=col_span,
                sticky="nsew",
                ipadx=10,
                ipady=10,
            )

            col_val += col_span
            if col_val > 3:
                col_val = 0
                row_val += 1

        for i in range(6):
            master.columnconfigure(i, weight=1)
            master.rowconfigure(i, weight=1)

        entry.focus_set()

    def button_click(self, symbol):
        if self.expression.get() == "Error" or self.expression.get() == "Syntax Error":
            self.expression.set("")

        if symbol == "=":
            self.evaluate_expression()
        elif symbol == "AC":
            self.expression.set("")
        elif symbol == "←":
            if (
                self.expression.get() == "Error"
                or self.expression.get() == "Syntax Error"
            ):
                self.expression.set("")
            else:
                self.expression.set(self.expression.get()[:-1])
        elif symbol == "Xⁿ":
            self.expression.set(self.expression.get() + "^")
        elif symbol == ".":
            current_expression = self.expression.get()
            if not current_expression or current_expression[-1] in "+-*/^(":
                self.expression.set(current_expression + "0.")
            elif "." not in current_expression.split(" ")[-1]:
                self.expression.set(current_expression + ".")
        elif symbol == "a/b":
            self.convert_to_fraction()
        else:
            current_expression = self.expression.get()
            self.expression.set(current_expression + str(symbol))
            self.expression.set(current_expression + str(symbol))

    def check_syntax(self):
        dfa = {
            "start": {"0-9": "operand", "(": "open_paren"},
            "operand": {
                "0-9": "operand",
                "+": "operator",
                "-": "operator",
                "x": "operator",
                "/": "operator",
                "^": "exponent",
                ")": "close_paren",
                ".": "decimal",
            },
            "operator": {"0-9": "operand", "(": "open_paren"},
            "open_paren": {"0-9": "operand", "(": "open_paren", ".": "operand"},
            "close_paren": {
                "+": "operator",
                "-": "operator",
                "x": "operator",
                "/": "operator",
                "^": "operator",
                ")": "close_paren",
            },
            "exponent": {"0-9": "operand", "(": "open_paren", "-": "operand"},
            "decimal": {"0-9": "operand"},
        }

        stack = []
        current_state = "start"

        for symbol in self.expression.get():
            symbol_type = self.get_symbol_type(symbol)
            current_state = dfa[current_state].get(symbol_type)

            if not current_state:
                return False

            if symbol == "(":
                stack.append("(")
            elif symbol == ")":
                if stack.pop() != "(":
                    return False

        return current_state in {"operand", "close_paren"} and not stack

    @staticmethod
    def get_symbol_type(symbol):
        if symbol.isdigit():
            return "0-9"
        elif symbol == "^":
            return "^"
        elif symbol == ".":
            return "."

        else:
            return symbol

    def evaluate_expression(self):
        try:
            if self.check_syntax():
                modified_expression = self.expression.get().replace("^", "**")
                modified_expression = modified_expression.replace("x", "*")

                result = str(eval(modified_expression))
                self.expression.set(result)
            else:
                self.expression.set("Syntax Error")
        except Exception as e:
            self.expression.set("Error")

    def convert_to_fraction(self):
        try:
            current_result = self.expression.get()

            if self.to_fraction:
                fraction_result = Fraction(current_result)
                decimal_result = float(fraction_result)
                self.expression.set(decimal_result)
            else:
                decimal_result = float(current_result)
                fraction_result = Fraction(decimal_result).limit_denominator()
                self.expression.set(fraction_result)

            self.to_fraction = not self.to_fraction

        except ValueError:
            self.expression.set("Error")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.configure(bg="#2C2C2C")
    root.mainloop()
