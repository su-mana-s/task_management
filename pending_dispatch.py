
import customtkinter as ctk
import sqlite3
import pandas as pd
import tkinter as tk

from tkinter import messagebox

from database import DB_NAME
from theme import *


class PendingDispatch(ctk.CTkFrame):

    def __init__(self, master, user=None):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.user = user
        self.current_data = pd.DataFrame()

        # =========================================================
        # TITLE
        # =========================================================

        ctk.CTkLabel(
            self,
            text="Pending Dispatch",
            font=ctk.CTkFont(
                size=SIZES["title_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).pack(
            pady=(0, 10),
            padx=5,
            anchor="w"
        )

        # =========================================================
        # HELP TEXT
        # =========================================================

        ctk.CTkLabel(
            self,
            text=(
                "This screen shows work that has been completed but not yet "
                "dispatched. Use Assigned To to filter by employee, or use "
                "Client and Department to narrow the results."
            ),
            font=ctk.CTkFont(
                size=SIZES["small_size"]
            ),
            text_color=COLORS["text_secondary"],
            anchor="w",
            justify="left"
        ).pack(
            padx=5,
            pady=(0, 12),
            anchor="w"
        )

        # =========================================================
        # FILTER CARD
        # =========================================================

        self.filter_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS["toggle"],
            corner_radius=SIZES["large_corner_radius"]
        )

        self.filter_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        # =========================================================
        # CLIENT
        # =========================================================

        ctk.CTkLabel(
            self.filter_frame,
            text="Client:",
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            padx=(15, 5),
            pady=12
        )

        self.client_search = ctk.CTkEntry(
            self.filter_frame,
            width=200,
            height=SIZES["entry_height"],
            placeholder_text="Client name",
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            corner_radius=SIZES["corner_radius"]
        )

        self.client_search.grid(
            row=0,
            column=1,
            padx=5,
            pady=12
        )

        # =========================================================
        # DEPARTMENT
        # =========================================================

        ctk.CTkLabel(
            self.filter_frame,
            text="Department:",
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=2,
            padx=(20, 5),
            pady=12
        )

        self.department_filter = ctk.CTkEntry(
            self.filter_frame,
            width=180,
            height=SIZES["entry_height"],
            placeholder_text="Department",
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            corner_radius=SIZES["corner_radius"]
        )

        self.department_filter.grid(
            row=0,
            column=3,
            padx=5,
            pady=12
        )

        # =========================================================
        # ASSIGNED EMPLOYEE
        # =========================================================

        ctk.CTkLabel(
            self.filter_frame,
            text="Assigned To:",
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=4,
            padx=(20, 5),
            pady=12
        )

        self.employee_filter = ctk.CTkComboBox(
            self.filter_frame,
            values=["All Employees"],
            width=190,
            height=SIZES["entry_height"],
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            button_color=SIDEBAR_HOVER,
            button_hover_color=COLORS["primary_hover"],
            text_color=COLORS["text"],
            dropdown_fg_color=COLORS["toggle"],
            dropdown_hover_color=SIDEBAR_HOVER,
            dropdown_text_color=COLORS["text"],
            corner_radius=SIZES["corner_radius"]
        )

        self.employee_filter.set("All Employees")

        self.employee_filter.grid(
            row=0,
            column=5,
            padx=5,
            pady=12
        )

        # =========================================================
        # DATE FILTERS
        # =========================================================

        ctk.CTkLabel(
            self.filter_frame,
            text="Completion From:",
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=1,
            column=0,
            padx=(15, 5),
            pady=(0, 12)
        )

        self.start_date = ctk.CTkEntry(
            self.filter_frame,
            width=150,
            height=SIZES["entry_height"],
            placeholder_text="DD-MM-YYYY",
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            corner_radius=SIZES["corner_radius"]
        )

        self.start_date.grid(
            row=1,
            column=1,
            padx=5,
            pady=(0, 12)
        )

        ctk.CTkLabel(
            self.filter_frame,
            text="Completion To:",
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=1,
            column=2,
            padx=(20, 5),
            pady=(0, 12)
        )

        self.end_date = ctk.CTkEntry(
            self.filter_frame,
            width=150,
            height=SIZES["entry_height"],
            placeholder_text="DD-MM-YYYY",
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            corner_radius=SIZES["corner_radius"]
        )

        self.end_date.grid(
            row=1,
            column=3,
            padx=5,
            pady=(0, 12)
        )

        ctk.CTkButton(
            self.filter_frame,
            text="Apply Filters",
            command=self.generate_report,
            width=150,
            height=SIZES["button_height"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=TEXT_LIGHT,
            corner_radius=SIZES["corner_radius"],
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            )
        ).grid(
            row=1,
            column=5,
            padx=5,
            pady=(0, 12)
        )

        self.load_employees()

        # =========================================================
        # DATA CONTAINER
        # =========================================================

        self.data_container = ctk.CTkFrame(
            self,
            fg_color=COLORS["toggle"],
            corner_radius=SIZES["large_corner_radius"]
        )

        self.data_container.pack(
            fill="both",
            expand=True
        )

        self.table_canvas = tk.Canvas(
            self.data_container,
            bg=COLORS["toggle"],
            highlightthickness=0,
            borderwidth=0
        )

        self.table_canvas.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.vertical_scrollbar = ctk.CTkScrollbar(
            self.data_container,
            orientation="vertical",
            command=self.table_canvas.yview
        )

        self.vertical_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.horizontal_scrollbar = ctk.CTkScrollbar(
            self.data_container,
            orientation="horizontal",
            command=self.table_canvas.xview
        )

        self.horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        self.table_canvas.configure(
            xscrollcommand=self.horizontal_scrollbar.set,
            yscrollcommand=self.vertical_scrollbar.set
        )

        self.data_container.grid_rowconfigure(
            0,
            weight=1
        )

        self.data_container.grid_columnconfigure(
            0,
            weight=1
        )

        self.data_frame = ctk.CTkFrame(
            self.table_canvas,
            fg_color=COLORS["toggle"]
        )

        self.table_canvas.create_window(
            (0, 0),
            window=self.data_frame,
            anchor="nw"
        )

        self.data_frame.bind(
            "<Configure>",
            lambda e: self.table_canvas.configure(
                scrollregion=self.table_canvas.bbox("all")
            )
        )

        self.generate_report()

    # =============================================================
    # DATE HELPERS
    # =============================================================

    def display_date(self, value):

        """
        Convert database date format YYYY-MM-DD
        to user-facing format DD-MM-YYYY.
        """

        if pd.isnull(value):
            return "-"

        value = str(value).strip()

        try:
            return pd.to_datetime(
                value,
                format="%Y-%m-%d"
            ).strftime("%d-%m-%Y")

        except (ValueError, TypeError):

            return value

    def database_date(self, value):

        """
        Convert user-entered date format DD-MM-YYYY
        to database format YYYY-MM-DD.
        """

        if not value:
            return None

        try:
            return pd.to_datetime(
                value,
                format="%d-%m-%Y"
            ).strftime("%Y-%m-%d")

        except (ValueError, TypeError):

            raise ValueError(
                f"Invalid date: {value}\n"
                "Please enter the date as DD-MM-YYYY."
            )

    # =============================================================
    # EMPLOYEES
    # =============================================================

    def load_employees(self):

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT username
                FROM users
                WHERE is_active = 1
                ORDER BY username
            """)

            employees = [
                row[0]
                for row in cursor.fetchall()
            ]

            self.employee_filter.configure(
                values=["All Employees"] + employees
            )

        finally:

            conn.close()

    # =============================================================
    # GENERATE
    # =============================================================

    def generate_report(self):

        client = self.client_search.get().strip()
        department = self.department_filter.get().strip()
        employee = self.employee_filter.get()

        start_date_input = self.start_date.get().strip()
        end_date_input = self.end_date.get().strip()

        try:

            start_date = self.database_date(
                start_date_input
            ) if start_date_input else None

            end_date = self.database_date(
                end_date_input
            ) if end_date_input else None

        except ValueError as e:

            messagebox.showerror(
                "Invalid Date",
                str(e)
            )

            return

        query = """
            SELECT
                r.inward_id AS "Task ID",

                c.name AS "Client",

                r.department AS "Department",

                u.username AS "Assigned To",

                r.date_of_entry AS "Entry Date",
                r.date_of_completion AS "Completion Date",

                r.details_of_work_done AS "Work Done",

                r.how_despatched AS "Dispatch Mode",

                CASE
                    WHEN r.bill_raised = 'Y'
                        THEN 'Bill Generated'
                    ELSE 'Bill Not Generated'
                END AS "Bill Status",

                r.bill_number AS "Bill No",
                r.bill_date AS "Bill Date",
                r.bill_amount AS "Bill Amount",
                r.amount_pending_receipt AS "Pending Amount"

            FROM records r

            LEFT JOIN clients c
                ON r.client_id = c.id

            LEFT JOIN users u
                ON r.assigned_to = u.id

            WHERE r.status = 1
        """

        params = []

        if client:

            query += """
                AND c.name LIKE ?
            """

            params.append(f"%{client}%")

        if department:

            query += """
                AND r.department LIKE ?
            """

            params.append(f"%{department}%")

        if employee and employee != "All Employees":

            query += """
                AND u.username = ?
            """

            params.append(employee)

        if start_date:

            query += """
                AND r.date_of_completion >= ?
            """

            params.append(start_date)

        if end_date:

            query += """
                AND r.date_of_completion <= ?
            """

            params.append(end_date)

        query += """
            ORDER BY r.date_of_completion ASC,
                     r.inward_id DESC
        """

        conn = sqlite3.connect(DB_NAME)

        try:

            self.current_data = pd.read_sql_query(
                query,
                conn,
                params=params
            )

            self.display_data()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            conn.close()

    # =============================================================
    # DISPLAY
    # =============================================================

    def display_data(self):

        for widget in self.data_frame.winfo_children():
            widget.destroy()

        if self.current_data.empty:

            ctk.CTkLabel(
                self.data_frame,
                text="No pending dispatches found.",
                font=ctk.CTkFont(
                    size=SIZES["heading_size"],
                    weight="bold"
                ),
                text_color=COLORS["text_secondary"]
            ).grid(
                row=0,
                column=0,
                padx=30,
                pady=30
            )

            return

        columns = list(self.current_data.columns)

        widths = {}

        for col in columns:

            max_length = len(str(col))

            for value in self.current_data[col]:

                if pd.isnull(value):
                    value = "-"
                elif col in [
                    "Entry Date",
                    "Completion Date",
                    "Bill Date"
                ]:
                    value = self.display_date(value)

                max_length = max(
                    max_length,
                    len(str(value))
                )

            widths[col] = max(
                100,
                min(
                    max_length * 8 + 30,
                    400
                )
            )

        # Header

        for col_idx, col in enumerate(columns):

            self.data_frame.grid_columnconfigure(
                col_idx,
                minsize=widths[col]
            )

            ctk.CTkLabel(
                self.data_frame,
                text=str(col),
                font=ctk.CTkFont(
                    size=SIZES["normal_size"],
                    weight="bold"
                ),
                text_color=TEXT_LIGHT,
                fg_color=SIDEBAR_HOVER,
                corner_radius=8,
                anchor="center"
            ).grid(
                row=0,
                column=col_idx,
                padx=2,
                pady=(5, 8),
                ipadx=8,
                ipady=7,
                sticky="nsew"
            )

        # Data

        for row_idx, row in self.current_data.iterrows():

            for col_idx, col in enumerate(columns):

                value = row[col]

                if pd.isnull(value):

                    value = "-"

                elif col in [
                    "Entry Date",
                    "Completion Date",
                    "Bill Date"
                ]:

                    value = self.display_date(value)

                else:

                    value = str(value)

                ctk.CTkLabel(
                    self.data_frame,
                    text=value,
                    font=ctk.CTkFont(
                        size=SIZES["normal_size"]
                    ),
                    text_color=COLORS["text"],
                    anchor="w"
                ).grid(
                    row=row_idx + 1,
                    column=col_idx,
                    padx=5,
                    pady=5,
                    ipadx=5,
                    ipady=4,
                    sticky="ew"
                )

        # =========================================================
        # SUMMARY
        # =========================================================

        total_row = len(self.current_data) + 1

        bill_total = self.current_data[
            "Bill Amount"
        ].fillna(0).sum()

        pending_total = self.current_data[
            "Pending Amount"
        ].fillna(0).sum()

        for col_idx, col in enumerate(columns):

            value = ""

            if col == "Task ID":

                value = (
                    f"Total Pending Dispatch: "
                    f"{len(self.current_data)}"
                )

            elif col == "Bill Amount":

                value = f"₹{bill_total:,.2f}"

            elif col == "Pending Amount":

                value = f"₹{pending_total:,.2f}"

            ctk.CTkLabel(
                self.data_frame,
                text=value,
                font=ctk.CTkFont(
                    size=SIZES["normal_size"],
                    weight="bold"
                ),
                text_color=TEXT_LIGHT,
                fg_color=SIDEBAR_HOVER,
                anchor="w"
            ).grid(
                row=total_row,
                column=col_idx,
                padx=2,
                pady=(10, 5),
                ipadx=8,
                ipady=7,
                sticky="ew"
            )

        self.data_frame.update_idletasks()

        self.table_canvas.configure(
            scrollregion=self.table_canvas.bbox("all")
        )
