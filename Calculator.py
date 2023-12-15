## Calculator
## Pip Install: pip install tkintertable
## Run: python Calculator.py

import tkinter as tk
import re
from fractions import Fraction


class CalculatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        self.master.resizable(False, False)
        self.expression = tk.StringVar()
        self.to_fraction = False
        self.history_window_open = False
        self.history = []
        self.runtime_history = []

        entry = tk.Entry(
            master,
            textvariable=self.expression,
            font=("Helvetica", 24),
            bd=0,
            insertwidth=12,
            width=16,
            justify="right",
        )
        entry.grid(row=0, column=0, columnspan=4, sticky="nsew", ipadx=25, ipady=15)
        entry.configure(readonlybackground="#2C2C2C", fg="white")
        entry.config(state="readonly")
        entry.bind("<Key>", self.handle_keypress)

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
                bg=color if color else "#2C2C2C",
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
            else:
                self.expression.set(current_expression + ".")
        elif symbol == "a/b":
            self.convert_to_fraction()
        else:
            current_expression = self.expression.get()
            self.expression.set(current_expression + str(symbol))
            self.expression.set(current_expression + str(symbol))
        if symbol not in {"=", "a/b"}:
            self.history.append(self.expression.get())

    def check_syntax(self):
        dfa = {
            "start": {"0-9": "operand", "(": "open_paren", "-": "negative"},
            "operand": {
                "0-9": "operand",
                "+": "operator",
                "-": "operator",
                "x": "operator",
                "*": "operator",
                "/": "operator",
                "^": "exponent",
                ")": "close_paren",
                ".": "decimal",
            },
            "operator": {
                "0-9": "operand",
                "(": "open_paren",
                "-": "negative",
                ".": "decimal",
            },
            "open_paren": {
                "0-9": "operand",
                "(": "open_paren",
                ".": "operand",
                "-": "negative",
            },
            "close_paren": {
                "+": "operator",
                "-": "operator",
                "x": "operator",
                "*": "operator",
                "/": "operator",
                "^": "operator",
                ")": "close_paren",
            },
            "exponent": {
                "0-9": "operand",
                "(": "open_paren",
                "-": "operand",
                "-": "negative",
            },
            "decimal": {"0-9": "operand"},
            "negative": {"0-9": "operand", "(": "open_paren", ".": "decimal"},
            "negative_start": {"0-9": "operand", ".": "decimal"},
        }

        stack = []
        current_state = "start"

        for i, symbol in enumerate(self.expression.get()):
            symbol_type = self.get_symbol_type(symbol)
            current_state = dfa[current_state].get(symbol_type)

            if not current_state:
                return False

            if symbol == "(":
                stack.append("(")
            elif symbol == ")":
                if stack.pop() != "(":
                    return False
            if current_state == "negative_start" and i > 0:
                return False

        return (
            current_state in {"operand", "close_paren", "negative_start"} and not stack
        )

    @staticmethod
    def get_symbol_type(symbol):
        if symbol.isdigit():
            return "0-9"
        elif symbol == "^":
            return "^"
        elif symbol == ".":
            return "."
        elif symbol == "-":
            return "-"

        else:
            return symbol

    def evaluate_expression(self):
        if not self.expression.get():
            return

        try:
            if self.check_syntax():
                original_expression = self.expression.get()
                modified_expression = original_expression.replace("^", "**")
                modified_expression = modified_expression.replace("x", "*")

                modified_expression = re.sub(r"\b0+(\d+)", r"\1", modified_expression)

                result = str(eval(modified_expression))
                entry = (original_expression, result)
                self.runtime_history.append(entry)
                self.expression.set(result)

            else:
                self.expression.set("Syntax Error")
        except Exception as e:
            self.expression.set("Error")

    def convert_to_fraction(self):
        if not self.expression.get():
            return

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

            entry = (f"{current_result}", str(self.expression.get()))
            self.runtime_history.append(entry)

            self.to_fraction = not self.to_fraction

        except ValueError:
            self.expression.set("Error")

    def display_history(self):
        if self.history_window_open:
            self.history_window.destroy()
            self.history_window_open = False
        else:
            self.history_window = tk.Toplevel(self.master)
            self.history_window.title("History")

            for entry in self.runtime_history:
                original_expression, result = entry
                label_text = f"{original_expression} = {result}"
                label = tk.Label(
                    self.history_window, text=label_text, font=("Helvetica", 12)
                )
                label.pack(pady=5)

            clear_button = tk.Button(
                self.history_window,
                text="Clear History",
                command=self.clear_history,
                padx=10,
                pady=5,
                font=("Helvetica", 12),
                bg="#A7A7A7",
                fg="white",
                activebackground="#2C2C2C",
                activeforeground="white",
                borderwidth=0,
                relief="ridge",
                bd=0,
            )
            clear_button.pack(pady=10)

            self.history_window_open = True

    def clear_history(self):
        self.runtime_history = []
        self.history_window.destroy()
        self.history_window_open = False

    def handle_keypress(self, event):
        key = event.char
        allowed_keys = "0123456789+-*/.^()=x"

        if key in allowed_keys:
            self.button_click(key)
        elif event.keysym == "BackSpace":
            self.button_click("←")
        elif event.keysym == "Return":
            self.button_click("=")
        elif event.keysym == "Escape":
            self.button_click("AC")
        elif key.lower() == "h":
            self.display_history()


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.configure(bg="#2C2C2C")
    root.mainloop()
