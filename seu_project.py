import tkinter as tk
from tkinter import messagebox
import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FinanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("850x950")

        self.income = 0
        self.expenses = []

        # Create frames for income and expense
        self.income_frame = tk.Frame(root, bg="#f0f0f0", highlightthickness=2, highlightbackground="#4CAF50")
        self.income_frame.pack(pady=20)

        self.expense_frame = tk.Frame(root, bg="#f0f0f0", highlightthickness=2, highlightbackground="#4CAF50")
        self.expense_frame.pack(pady=20)

        # Add widgets to income frame
        income_label = tk.Label(self.income_frame, text="Enter Income Amount:", font=("Arial", 16), bg="#f0f0f0")
        income_label.grid(row=0, column=0, padx=10, pady=10)

        self.entry_income = tk.Entry(self.income_frame, font=("Arial", 16), width=20, highlightthickness=2, highlightbackground="#4CAF50")
        self.entry_income.grid(row=0, column=1, padx=10, pady=10)

        btn_add_income = tk.Button(self.income_frame, text="Add Income", font=("Arial", 12), bg="#4CAF50", fg="white",
                                   command=self.add_income, width=10, height=1, relief="flat",
                                   activebackground="#3e8e41", activeforeground="white", highlightthickness=2, highlightbackground="#4CAF50")
        btn_add_income.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Add widgets to expense frame
        expense_label = tk.Label(self.expense_frame, text="Enter Expense Amount:", font=("Arial", 16), bg="#f0f0f0")
        expense_label.grid(row=0, column=0, padx=10, pady=10)

        self.entry_expense = tk.Entry(self.expense_frame, font=("Arial", 16), width=20, highlightthickness=2, highlightbackground="#4CAF50")
        self.entry_expense.grid(row=0, column=1, padx=10, pady=10)

        category_label = tk.Label(self.expense_frame, text="Category:", font=("Arial", 16), bg="#f0f0f0")
        category_label.grid(row=1, column=0, padx=10, pady=10)

        self.entry_category = tk.Entry(self.expense_frame, font=("Arial", 16), width=20, highlightthickness=2, highlightbackground="#4CAF50")
        self.entry_category.grid(row=1, column=1, padx=10, pady=10)

        btn_add_expense = tk.Button(self.expense_frame, text="Add Expense", font=("Arial", 12), bg="#4CAF50", fg="white",
                                    command=self.add_expense, width=10, height=1, relief="flat",
                                    activebackground="#3e8e41", activeforeground="white", highlightthickness=2, highlightbackground="#4CAF50")
        btn_add_expense.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Buttons
        buttons_frame = tk.Frame(root, bg="#f0f0f0")
        buttons_frame.pack(pady=20)

        btn_show_summary = tk.Button(buttons_frame, text="Show Summary", font=("Arial", 10), bg="#4CAF50", fg="white",
                                     command=self.show_summary, width=10, height=1, relief="flat",
                                     activebackground="#3e8e41", activeforeground="white", highlightthickness=2, highlightbackground="#4CAF50")
        btn_show_summary.pack(side=tk.LEFT, padx=10, pady=10)

        btn_exit = tk.Button(buttons_frame, text="Exit", font=("Arial", 10), bg="#4CAF50", fg="white",
                              command=root.destroy, width=10, height=1, relief="flat",
                              activebackground="#3e8e41", activeforeground="white", highlightthickness=2, highlightbackground="#4CAF50")
        btn_exit.pack(side=tk.LEFT, padx=10, pady=10)

        # Chart frame
        self.chart_frame = tk.Frame(root, bg="#f0f0f0")
        self.chart_frame.pack(pady=20)

    def add_income(self):
        try:
            self.income = float(self.entry_income.get())
            self.entry_income.delete(0, tk.END)
            messagebox.showinfo("Success", "Income added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid income amount")

    def add_expense(self):
        try:
            amount = float(self.entry_expense.get())
            category = self.entry_category.get()
            self.expenses.append({"amount": amount, "category": category})
            self.entry_expense.delete(0, tk.END)
            self.entry_category.delete(0, tk.END)
            messagebox.showinfo("Success", "Expense added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid expense amount")

    def show_summary(self):
        total_expenses = sum(expense["amount"] for expense in self.expenses)
        savings = self.income - total_expenses

        if savings < 0:
            messagebox.showerror("Error", "You are in debt!")
        else:
            summary_label = tk.Label(self.chart_frame,
                                     text=f"Income: {self.income:.2f}\nExpenses: {total_expenses:.2f}\nSavings: {savings:.2f}",
                                     font=("Arial", 16), bg="#f0f0f0")
            summary_label.grid(row=0, column=0, columnspan=2, pady=10)

            self.fig1 = Figure(figsize=(4, 3), dpi=100)
            self.ax1 = self.fig1.add_subplot(111)

            self.ax1.pie([total_expenses, savings], labels=['Expenses', 'Savings'], autopct='%1.1f%%')
            self.ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            self.chart_type1 = FigureCanvasTkAgg(self.fig1, master=self.chart_frame)
            self.chart_type1.draw()
            self.chart_type1.get_tk_widget().grid(row=1, column=0, padx=10, pady=10)

            chart_label1 = tk.Label(self.chart_frame, text="Expense vs Savings", font=("Arial", 12), bg="#f0f0f0")
            chart_label1.grid(row=2, column=0, pady=10)

            self.fig2 = Figure(figsize=(4, 3), dpi=100)
            self.ax2 = self.fig2.add_subplot(111)

            expense_categories = {}
            for expense in self.expenses:
                if expense["category"] in expense_categories:
                    expense_categories[expense["category"]] += expense["amount"]
                else:
                    expense_categories[expense["category"]] = expense["amount"]

            self.ax2.pie(expense_categories.values(), labels=expense_categories.keys(), autopct='%1.1f%%')
            self.ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            self.chart_type2 = FigureCanvasTkAgg(self.fig2, master=self.chart_frame)
            self.chart_type2.draw()
            self.chart_type2.get_tk_widget().grid(row=1, column=1, padx=10, pady=10)

            chart_label2 = tk.Label(self.chart_frame, text="Expense Categories", font=("Arial", 12), bg="#f0f0f0")
            chart_label2.grid(row=2, column=1, pady=10)

root = tk.Tk()
finance_tracker = FinanceTracker(root)
root.mainloop()