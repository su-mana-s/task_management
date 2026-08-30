import customtkinter as ctk
import sqlite3
import pandas as pd
import tkinter as tk

from datetime import datetime
from tkinter import messagebox

from database import DB_NAME
from theme import *


class PendingBills(ctk.CTkFrame):

    def __init__(self, master, user=None):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.user = user
        self.current_data = pd.DataFrame()

        # =========================================================
        # DATE HELPERS
        # =========================================================

        def display_date(value):
            """
            Convert database date YYYY-MM-DD
            to user-facing date DD-MM-YYYY.

            Database value is NOT modified.
            """

            if value is None:
                return "-"

            value = str(value).strip()

            if not value:
                return "-"

            # Try normal database format
            try:
                return datetime.strptime(
                    value[:10],
                    "%Y-%m-%d"
                ).strftime(
                    "%d-%m-%Y"
                )
            except ValueError:
                pass

            # If the value is already DD-MM-YYYY
            # or some other format, leave it unchanged.
            return value

        def database_date(value):
            """
            Convert user-entered date DD-MM-YYYY
            to database/query date YYYY-MM-DD.

            The database format remains unchanged.
            """

            if not value:
                return ""

            value = value.strip()

            try:
                return datetime.strptime(
                    value,
                    "%d-%m-%Y"
                ).strftime(
                    "%Y-%m-%d"
                )
            except ValueError:
                raise ValueError(
                    "Date must be entered as DD-MM-YYYY."
                )

        self.display_date = display_date
        self.database_date = database_date

        # =========================================================
        # TITLE
        # =========================================================

        ctk.CTkLabel(
            self,
            text="Pending Bills",
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
                "Bill Generated = a bill amount exists and payment is still pending.   "
                "Bill Not Generated = completed work where the bill amount is 0 or blank. "
                "Use the filters below to narrow the results."
            ),
            font=ctk.CTkFont(
                size=SIZES["normal_size"]
            ),
            text_color=COLORS["primary_hover"],
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
        # ROW 1
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

        # Department

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

        # Bill Status

        ctk.CTkLabel(
            self.filter_frame,
            text="Bill Status:",
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

        self.bill_status = ctk.CTkComboBox(
            self.filter_frame,
            values=[
                "All Pending",
                "Bill Generated",
                "Bill Not Generated"
            ],
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

        self.bill_status.set("All Pending")

        self.bill_status.grid(
            row=0,
            column=5,
            padx=5,
            pady=12
        )

        # =========================================================
        # ROW 2
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
            row=1,
            column=0,
            padx=(15, 5),
            pady=(0, 12)
        )

        self.employee_filter = ctk.CTkComboBox(
            self.filter_frame,
            values=["All Employees"],
            width=200,
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
            row=1,
            column=1,
            padx=5,
            pady=(0, 12)
        )

        # =========================================================
        # START DATE
        # =========================================================

        ctk.CTkLabel(
            self.filter_frame,
            text="Start Date:",
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
            column=3,
            padx=5,
            pady=(0, 12)
        )

        # =========================================================
        # END DATE
        # =========================================================

        ctk.CTkLabel(
            self.filter_frame,
            text="End Date:",
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=1,
            column=4,
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
            column=5,
            padx=5,
            pady=(0, 12)
        )

        # =========================================================
        # GENERATE
        # =========================================================

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
            row=2,
            column=0,
            columnspan=6,
            padx=15,
            pady=(0, 15),
            sticky="e"
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
    # LOAD EMPLOYEES
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
        bill_status = self.bill_status.get()
        employee = self.employee_filter.get()

        # =========================================================
        # USER-FACING DATE INPUT
        #
        # User enters:
        #     DD-MM-YYYY
        #
        # Database still uses:
        #     YYYY-MM-DD
        # =========================================================

        start_date_display = (
            self.start_date
            .get()
            .strip()
        )

        end_date_display = (
            self.end_date
            .get()
            .strip()
        )

        try:

            start_date = self.database_date(
                start_date_display
            ) if start_date_display else ""

            end_date = self.database_date(
                end_date_display
            ) if end_date_display else ""

        except ValueError as e:

            messagebox.showerror(
                "Invalid Date",
                str(e)
            )

            return

        # =========================================================
        # IMPORTANT BILL LOGIC
        #
        # Bill Generated:
        #     bill_amount > 0
        #     AND pending amount > 0
        #
        # Bill Not Generated:
        #     Work is completed (status = 1)
        #     AND bill_amount is NULL or <= 0
        #
        # bill_raised is intentionally NOT used here because the
        # actual bill amount is the source of truth.
        # =========================================================

        query = """
            SELECT
                r.inward_id AS "Task ID",
                c.name AS "Client",
                r.department AS "Department",

                u.username AS "Assigned To",

                CASE r.status
                    WHEN 0 THEN 'Inward'
                    WHEN 1 THEN 'Work Done'
                    WHEN 2 THEN 'Dispatched'
                    ELSE 'Unknown'
                END AS "Work Status",

                CASE
                    WHEN r.bill_amount > 0
                         AND COALESCE(r.amount_pending_receipt, 0) > 0
                        THEN 'Bill Generated'

                    WHEN r.status = 1
                         AND (
                             r.bill_amount IS NULL
                             OR r.bill_amount <= 0
                         )
                        THEN 'Bill Not Generated'

                    ELSE 'Unknown'
                END AS "Bill Status",

                r.bill_number AS "Bill No",
                r.bill_date AS "Bill Date",
                r.bill_amount AS "Bill Amount",
                r.actual_amount_received AS "Received",
                r.amount_pending_receipt AS "Pending",

                r.date_of_entry AS "Entry Date",
                r.date_of_completion AS "Completion Date"

            FROM records r

            LEFT JOIN clients c
                ON r.client_id = c.id

            LEFT JOIN users u
                ON r.assigned_to = u.id

            WHERE
                (
                    -- =================================================
                    -- BILL GENERATED BUT PAYMENT IS PENDING
                    -- =================================================
                    (
                        r.bill_amount > 0
                        AND COALESCE(
                            r.amount_pending_receipt,
                            0
                        ) > 0
                    )

                    OR

                    -- =================================================
                    -- WORK COMPLETED BUT BILL NOT GENERATED
                    -- =================================================
                    (
                        r.status = 1
                        AND (
                            r.bill_amount IS NULL
                            OR r.bill_amount <= 0
                        )
                    )
                )
        """

        params = []

        # =========================================================
        # CLIENT
        # =========================================================

        if client:

            query += """
                AND c.name LIKE ?
            """

            params.append(
                f"%{client}%"
            )

        # =========================================================
        # DEPARTMENT
        # =========================================================

        if department:

            query += """
                AND r.department LIKE ?
            """

            params.append(
                f"%{department}%"
            )

        # =========================================================
        # EMPLOYEE
        # =========================================================

        if employee and employee != "All Employees":

            query += """
                AND u.username = ?
            """

            params.append(
                employee
            )

        # =========================================================
        # BILL STATUS
        # =========================================================

        if bill_status == "Bill Generated":

            query += """
                AND r.bill_amount > 0
                AND COALESCE(
                    r.amount_pending_receipt,
                    0
                ) > 0
            """

        elif bill_status == "Bill Not Generated":

            query += """
                AND r.status = 1
                AND (
                    r.bill_amount IS NULL
                    OR r.bill_amount <= 0
                )
            """

        # =========================================================
        # DATES
        #
        # User:
        #     DD-MM-YYYY
        #
        # Database:
        #     YYYY-MM-DD
        #
        # Filters continue to use Entry Date exactly as before.
        # =========================================================

        if start_date:

            query += """
                AND r.date_of_entry >= ?
            """

            params.append(
                start_date
            )

        if end_date:

            query += """
                AND r.date_of_entry <= ?
            """

            params.append(
                end_date
            )

        # =========================================================
        # SORT
        # =========================================================

        query += """
            ORDER BY r.inward_id DESC
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
                text="No pending bills found.",
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

        columns = list(
            self.current_data.columns
        )

        # =========================================================
        # DATE COLUMNS
        #
        # These are changed ONLY for display.
        #
        # self.current_data still contains the original
        # database values internally.
        # =========================================================

        date_columns = {
            "Bill Date",
            "Entry Date",
            "Completion Date"
        }

        # =========================================================
        # CALCULATE WIDTHS
        # =========================================================

        widths = {}

        for col in columns:

            max_length = len(
                str(col)
            )

            for value in self.current_data[col]:

                if pd.isnull(value):

                    value = "-"

                elif col in date_columns:

                    value = self.display_date(
                        value
                    )

                max_length = max(
                    max_length,
                    len(str(value))
                )

            widths[col] = max(
                100,
                min(
                    max_length * 8 + 30,
                    350
                )
            )

        # =========================================================
        # HEADER
        # =========================================================

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

        # =========================================================
        # DATA
        # =========================================================

        for row_idx, row in self.current_data.iterrows():

            for col_idx, col in enumerate(columns):

                value = row[col]

                if pd.isnull(value):

                    value = "-"

                elif col in date_columns:

                    # -------------------------------------------------
                    # DATABASE:
                    #     YYYY-MM-DD
                    #
                    # DISPLAY:
                    #     DD-MM-YYYY
                    # -------------------------------------------------

                    value = self.display_date(
                        value
                    )

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
        # TOTALS
        # =========================================================

        total_row = len(
            self.current_data
        ) + 1

        totals = {
            "Task ID": f"{len(self.current_data)} items",

            "Bill Amount":
                self.current_data[
                    "Bill Amount"
                ].fillna(0).sum(),

            "Received":
                self.current_data[
                    "Received"
                ].fillna(0).sum(),

            "Pending":
                self.current_data[
                    "Pending"
                ].fillna(0).sum()
        }

        for col_idx, col in enumerate(columns):

            value = ""

            if col in totals:

                value = totals[col]

            if isinstance(
                value,
                (int, float)
            ):

                value = f"{value:,.2f}"

            ctk.CTkLabel(
                self.data_frame,
                text=str(value),
                font=ctk.CTkFont(
                    size=SIZES["normal_size"],
                    weight="bold"
                ),
                text_color=TEXT_LIGHT,
                fg_color=SIDEBAR_HOVER,
                corner_radius=10,
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