import customtkinter as ctk
import sqlite3
import pandas as pd
import tkinter as tk

from tkinter import filedialog, messagebox

from database import DB_NAME
from theme import *


class ReportsMenu(ctk.CTkFrame):

    def __init__(self, master, user):

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
            text="Search & Reports",
            font=ctk.CTkFont(
                size=SIZES["title_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).pack(
            pady=(0, 20),
            padx=5,
            anchor="w"
        )

        # =========================================================
        # CONTROLS CARD
        # =========================================================

        self.action_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS["toggle"],
            corner_radius=SIZES["large_corner_radius"]
        )

        self.action_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        self.action_frame.grid_columnconfigure(
            1,
            weight=1
        )

        # =========================================================
        # REPORT SELECTION
        # =========================================================

        ctk.CTkLabel(
            self.action_frame,
            text="Report:",
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            padx=(15, 8),
            pady=15,
            sticky="w"
        )

        self.report_type = ctk.StringVar(
            value="All Records"
        )

        reports = [
            "All Records",
            "Payment Transactions",
            "Dispatch Activity",
            "Billing Activity",
            "Complete Activity Log",
            "Pending Payments"
        ]

        self.report_dropdown = ctk.CTkComboBox(
            self.action_frame,
            variable=self.report_type,
            values=reports,
            width=300,
            height=SIZES["entry_height"],
            font=ctk.CTkFont(
                size=SIZES["normal_size"]
            ),
            dropdown_font=ctk.CTkFont(
                size=SIZES["normal_size"]
            ),
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

        self.report_dropdown.grid(
            row=0,
            column=1,
            padx=8,
            pady=15,
            sticky="w"
        )

        # =========================================================
        # GENERATE BUTTON
        # =========================================================

        self.generate_btn = ctk.CTkButton(
            self.action_frame,
            text="Generate Report",
            command=self.generate_report,
            width=170,
            height=SIZES["button_height"],
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=TEXT_LIGHT,
            corner_radius=SIZES["corner_radius"]
        )

        self.generate_btn.grid(
            row=0,
            column=2,
            padx=8,
            pady=15
        )

        # =========================================================
        # EXPORT EXCEL
        # =========================================================

        self.export_excel_btn = ctk.CTkButton(
            self.action_frame,
            text="Export Excel",
            command=self.export_excel,
            width=150,
            height=SIZES["button_height"],
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            fg_color=LOGOUT,
            hover_color=LOGOUT_HOVER,
            text_color=TEXT_LIGHT,
            corner_radius=SIZES["corner_radius"]
        )

        self.export_excel_btn.grid(
            row=0,
            column=3,
            padx=8,
            pady=15
        )

        # =========================================================
        # EXPORT PDF
        # =========================================================

        self.export_pdf_btn = ctk.CTkButton(
            self.action_frame,
            text="Export PDF",
            command=self.export_pdf,
            width=150,
            height=SIZES["button_height"],
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            fg_color=LOGOUT,
            hover_color=LOGOUT_HOVER,
            text_color=TEXT_LIGHT,
            corner_radius=SIZES["corner_radius"]
        )

        self.export_pdf_btn.grid(
            row=0,
            column=4,
            padx=8,
            pady=15
        )

        # =========================================================
        # FILTER SECTION
        # =========================================================

        self.search_frame = ctk.CTkFrame(
            self.action_frame,
            fg_color=COLORS["card_alt"],
            corner_radius=SIZES["corner_radius"]
        )

        self.search_frame.grid(
            row=1,
            column=0,
            columnspan=8,
            padx=15,
            pady=(0, 15),
            sticky="ew"
        )

        # =========================================================
        # CLIENT FILTER
        # =========================================================

        ctk.CTkLabel(
            self.search_frame,
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
            self.search_frame,
            width=220,
            height=SIZES["entry_height"],
            placeholder_text="Client name",
            font=ctk.CTkFont(
                size=SIZES["normal_size"]
            ),
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
        # DEPARTMENT FILTER
        # =========================================================

        ctk.CTkLabel(
            self.search_frame,
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

        self.department_filter = ctk.StringVar(
            value="All Departments"
        )

        self.department_dropdown = ctk.CTkComboBox(
            self.search_frame,
            variable=self.department_filter,
            values=["All Departments"],
            width=220,
            height=SIZES["entry_height"],
            font=ctk.CTkFont(
                size=SIZES["normal_size"]
            ),
            dropdown_font=ctk.CTkFont(
                size=SIZES["normal_size"]
            ),
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

        self.department_dropdown.grid(
            row=0,
            column=3,
            padx=5,
            pady=12
        )

        # =========================================================
        # START DATE
        # =========================================================

        ctk.CTkLabel(
            self.search_frame,
            text="Start Date:",
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

        self.start_date = ctk.CTkEntry(
            self.search_frame,
            width=150,
            height=SIZES["entry_height"],
            placeholder_text="DD-MM-YYYY",
            font=ctk.CTkFont(
                size=SIZES["normal_size"]
            ),
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            corner_radius=SIZES["corner_radius"]
        )

        self.start_date.grid(
            row=0,
            column=5,
            padx=5,
            pady=12
        )

        # =========================================================
        # END DATE
        # =========================================================

        ctk.CTkLabel(
            self.search_frame,
            text="End Date:",
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=6,
            padx=(20, 5),
            pady=12
        )

        self.end_date = ctk.CTkEntry(
            self.search_frame,
            width=150,
            height=SIZES["entry_height"],
            placeholder_text="DD-MM-YYYY",
            font=ctk.CTkFont(
                size=SIZES["normal_size"]
            ),
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            corner_radius=SIZES["corner_radius"]
        )

        self.end_date.grid(
            row=0,
            column=7,
            padx=5,
            pady=12
        )

        # =========================================================
        # DATA FRAME
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

        # =========================================================
        # CANVAS
        # =========================================================

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

        # =========================================================
        # VERTICAL SCROLLBAR
        # =========================================================

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

        # =========================================================
        # HORIZONTAL SCROLLBAR
        # =========================================================

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

        # =========================================================
        # CONNECT SCROLLBARS
        # =========================================================

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

        # =========================================================
        # TABLE FRAME
        # =========================================================

        self.data_frame = ctk.CTkFrame(
            self.table_canvas,
            fg_color=COLORS["toggle"]
        )

        self.table_window = self.table_canvas.create_window(
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

        # =========================================================
        # LOAD DEPARTMENTS
        # =========================================================

        self.load_departments()

        # =========================================================
        # INITIAL REPORT
        # =========================================================

        self.generate_report()

    # =============================================================
    # DATE FORMAT HELPERS
    # =============================================================

    @staticmethod
    def display_date(value):

        """
        Convert database date format YYYY-MM-DD
        to user display format DD-MM-YYYY.
        """

        if pd.isnull(value) or value in ("", "-"):
            return value

        try:

            return pd.to_datetime(
                value
            ).strftime("%d-%m-%Y")

        except Exception:

            return value

    @staticmethod
    def database_date(value):

        """
        Convert user-entered date DD-MM-YYYY
        to database format YYYY-MM-DD.
        """

        if not value:
            return ""

        try:

            return pd.to_datetime(
                value,
                format="%d-%m-%Y"
            ).strftime("%Y-%m-%d")

        except ValueError:

            raise ValueError(
                f"Invalid date '{value}'. "
                "Please use DD-MM-YYYY."
            )

    # =============================================================
    # LOAD DEPARTMENTS
    # =============================================================

    def load_departments(self):

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT DISTINCT department
                FROM records
                WHERE department IS NOT NULL
                  AND TRIM(department) != ''
                ORDER BY department
            """)

            departments = [
                row[0]
                for row in cursor.fetchall()
            ]

            values = [
                "All Departments"
            ] + departments

            self.department_dropdown.configure(
                values=values
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Unable to load departments:\n{e}"
            )

        finally:

            conn.close()

    # =============================================================
    # GENERATE REPORT
    # =============================================================

    def generate_report(self):

        report = self.report_type.get()

        client_filter = (
            self.client_search.get()
            .strip()
        )

        department_filter = (
            self.department_filter.get()
            .strip()
        )

        start_date_input = (
            self.start_date.get()
            .strip()
        )

        end_date_input = (
            self.end_date.get()
            .strip()
        )

        # =========================================================
        # CONVERT DATES
        # =========================================================

        try:

            start_date = self.database_date(
                start_date_input
            )

            end_date = self.database_date(
                end_date_input
            )

        except ValueError as e:

            messagebox.showerror(
                "Invalid Date",
                str(e)
            )

            return

        # =========================================================
        # CHECK DATE RANGE
        # =========================================================

        if start_date and end_date:

            if start_date > end_date:

                messagebox.showerror(
                    "Invalid Date Range",
                    "Start Date cannot be later than End Date."
                )

                return

        conn = sqlite3.connect(DB_NAME)

        try:

            # =====================================================
            # ALL RECORDS
            # =====================================================

            if report == "All Records":

                query = """
                    SELECT
                        r.inward_id AS "ID",
                        c.name AS "Client",
                        r.department AS "Department",

                        r.date_of_entry AS "Entry Date",
                        r.date_of_completion AS "Completion Date",
                        r.date_of_despatch AS "Dispatch Date",

                        u_enter.username AS "Entered By",
                        u_assigned.username AS "Assigned To",
                        u_completed.username AS "Completed By",
                        u_dispatch.username AS "Dispatched By",
                        u_billed.username AS "Billed By",

                        CASE r.status
                            WHEN 0 THEN 'Not Started'
                            WHEN 10 THEN 'In Progress'
                            WHEN 1 THEN 'Work Done'
                            WHEN 2 THEN 'Dispatched'
                            ELSE 'Unknown'
                        END AS "Status",

                        r.bill_number AS "Bill Number",
                        r.bill_date AS "Bill Date",
                        r.bill_amount AS "Bill Amount",

                        r.actual_amount_received AS "Total Received",
                        r.amount_pending_receipt AS "Balance"

                    FROM records r

                    LEFT JOIN clients c
                        ON r.client_id = c.id

                    LEFT JOIN users u_enter
                        ON r.entered_by = u_enter.id

                    LEFT JOIN users u_assigned
                        ON r.assigned_to = u_assigned.id

                    LEFT JOIN users u_completed
                        ON r.completed_by = u_completed.id

                    LEFT JOIN users u_dispatch
                        ON r.dispatched_by = u_dispatch.id

                    LEFT JOIN users u_billed
                        ON r.billed_by = u_billed.id

                    WHERE 1=1
                """

            # =====================================================
            # PAYMENT TRANSACTIONS
            # =====================================================

            elif report == "Payment Transactions":

                query = """
                    SELECT
                        p.id AS "Payment ID",
                        r.inward_id AS "Work ID",
                        c.name AS "Client",
                        r.department AS "Department",

                        r.bill_number AS "Bill Number",
                        r.bill_amount AS "Bill Amount",

                        p.amount AS "Payment Amount",
                        p.payment_mode AS "Payment Mode",
                        p.payment_date AS "Payment Date",

                        u.username AS "Received By",

                        p.notes AS "Notes",
                        p.created_at AS "Recorded At",

                        r.amount_pending_receipt AS
                            "Balance After Payment"

                    FROM payment_transactions p

                    JOIN records r
                        ON p.record_id = r.inward_id

                    LEFT JOIN clients c
                        ON r.client_id = c.id

                    LEFT JOIN users u
                        ON p.received_by = u.id

                    WHERE 1=1
                """

            # =====================================================
            # DISPATCH ACTIVITY
            # =====================================================

            elif report == "Dispatch Activity":

                query = """
                    SELECT
                        a.id AS "Activity ID",
                        r.inward_id AS "Work ID",
                        c.name AS "Client",
                        r.department AS "Department",

                        a.action_date AS "Dispatch Date",
                        u.username AS "Dispatched By",

                        r.assigned_to AS "Assigned User ID",
                        r.date_of_completion AS "Completion Date",
                        r.how_despatched AS "Dispatch Mode"

                    FROM activity_log a

                    JOIN records r
                        ON a.record_id = r.inward_id

                    LEFT JOIN clients c
                        ON r.client_id = c.id

                    LEFT JOIN users u
                        ON a.performed_by = u.id

                    WHERE a.action_type = 'DISPATCHED'
                """

            # =====================================================
            # BILLING ACTIVITY
            # =====================================================

            elif report == "Billing Activity":

                query = """
                    SELECT
                        a.id AS "Activity ID",
                        r.inward_id AS "Work ID",
                        c.name AS "Client",
                        r.department AS "Department",

                        r.bill_number AS "Bill Number",
                        a.amount AS "Bill Amount",

                        a.action_date AS "Bill Raised Date",
                        u.username AS "Billed By",

                        r.bill_date AS "Bill Date"

                    FROM activity_log a

                    JOIN records r
                        ON a.record_id = r.inward_id

                    LEFT JOIN clients c
                        ON r.client_id = c.id

                    LEFT JOIN users u
                        ON a.performed_by = u.id

                    WHERE a.action_type = 'BILL_RAISED'
                """

            # =====================================================
            # COMPLETE ACTIVITY LOG
            # =====================================================

            elif report == "Complete Activity Log":

                query = """
                    SELECT
                        a.id AS "Activity ID",

                        r.inward_id AS "Work ID",
                        c.name AS "Client",
                        r.department AS "Department",

                        a.action_type AS "Action",

                        a.action_date AS "Date/Time",

                        u.username AS "Performed By",

                        a.amount AS "Amount",
                        a.payment_mode AS "Payment Mode",

                        a.description AS "Description"

                    FROM activity_log a

                    JOIN records r
                        ON a.record_id = r.inward_id

                    LEFT JOIN clients c
                        ON r.client_id = c.id

                    LEFT JOIN users u
                        ON a.performed_by = u.id

                    WHERE 1=1
                """

            # =====================================================
            # PENDING PAYMENTS
            # =====================================================

            elif report == "Pending Payments":

                query = """
                    SELECT
                        r.inward_id AS "Work ID",
                        c.name AS "Client",
                        r.department AS "Department",

                        r.bill_number AS "Bill Number",
                        r.bill_date AS "Bill Date",

                        r.bill_amount AS "Bill Amount",
                        r.actual_amount_received AS "Total Received",
                        r.amount_pending_receipt AS "Balance",

                        u.username AS "Billed By"

                    FROM records r

                    LEFT JOIN clients c
                        ON r.client_id = c.id

                    LEFT JOIN users u
                        ON r.billed_by = u.id

                    WHERE r.bill_raised = 'Y'
                      AND r.amount_pending_receipt > 0
                """

            else:

                return

            # =====================================================
            # FILTERS
            # =====================================================

            params = []

            # -----------------------------------------------------
            # CLIENT
            # -----------------------------------------------------

            if client_filter:

                query += """
                    AND c.name LIKE ?
                """

                params.append(
                    f"%{client_filter}%"
                )

            # -----------------------------------------------------
            # DEPARTMENT
            # -----------------------------------------------------

            if (
                department_filter
                and department_filter != "All Departments"
            ):

                query += """
                    AND r.department = ?
                """

                params.append(
                    department_filter
                )

            # =====================================================
            # DATE COLUMN
            # =====================================================

            date_column = None

            if report == "Payment Transactions":

                date_column = "p.payment_date"

            elif report == "Dispatch Activity":

                date_column = "a.action_date"

            elif report == "Billing Activity":

                date_column = "a.action_date"

            elif report == "Complete Activity Log":

                date_column = "a.action_date"

            elif report == "All Records":

                date_column = "r.date_of_entry"

            elif report == "Pending Payments":

                date_column = "r.bill_date"

            # =====================================================
            # START DATE
            # =====================================================

            if start_date and date_column:

                query += f"""
                    AND {date_column} >= ?
                """

                params.append(
                    start_date
                )

            # =====================================================
            # END DATE
            # =====================================================

            if end_date and date_column:

                query += f"""
                    AND {date_column} <= ?
                """

                params.append(
                    end_date
                )

            # =====================================================
            # SORT
            # =====================================================

            query += """
                ORDER BY 1 DESC
            """

            # =====================================================
            # LOAD DATA
            # =====================================================

            self.current_data = pd.read_sql_query(
                query,
                conn,
                params=params
            )

            # =====================================================
            # DISPLAY
            # =====================================================

            self.display_data()

        except Exception as e:

            messagebox.showerror(
                "Report Error",
                str(e)
            )

        finally:

            conn.close()

    # =============================================================
    # SUMMARY
    # =============================================================

    def get_summary_row(self):

        """
        Create a summary row.

        Only financial/amount columns are summed.
        """

        summary = {}

        sum_columns = {
            "Bill Amount",
            "Total Received",
            "Balance",
            "Payment Amount",
            "Balance After Payment",
            "Amount"
        }

        for col in self.current_data.columns:

            if col in sum_columns:

                numeric_values = pd.to_numeric(
                    self.current_data[col],
                    errors="coerce"
                )

                summary[col] = numeric_values.sum()

            elif col == "Client":

                summary[col] = "TOTAL"

            else:

                summary[col] = ""

        return summary

    # =============================================================
    # DISPLAY
    # =============================================================

    def display_data(self):

        # =========================================================
        # CLEAR PREVIOUS TABLE
        # =========================================================

        for widget in self.data_frame.winfo_children():

            widget.destroy()

        # =========================================================
        # NO DATA
        # =========================================================

        if self.current_data.empty:

            ctk.CTkLabel(
                self.data_frame,
                text="No records found.",
                font=ctk.CTkFont(
                    size=SIZES["heading_size"],
                    weight="bold"
                ),
                text_color=COLORS["text_secondary"]
            ).grid(
                row=0,
                column=0,
                padx=20,
                pady=30
            )

            self.table_canvas.configure(
                scrollregion=self.table_canvas.bbox("all")
            )

            return

        columns = list(
            self.current_data.columns
        )

        # =========================================================
        # DATE COLUMNS
        # =========================================================

        date_columns = {
            "Entry Date",
            "Completion Date",
            "Dispatch Date",
            "Payment Date",
            "Bill Date",
            "Recorded At",
            "Date/Time",
            "Bill Raised Date"
        }

        # =========================================================
        # TOTAL COLUMNS
        # =========================================================

        sum_columns = {
            "Bill Amount",
            "Total Received",
            "Balance",
            "Payment Amount",
            "Balance After Payment",
            "Amount"
        }

        # =========================================================
        # COLUMN WIDTHS
        # =========================================================

        column_widths = {}

        for col in columns:

            max_length = len(
                str(col)
            )

            for value in self.current_data[col]:

                if pd.isnull(value):

                    value_length = 1

                else:

                    if col in date_columns:

                        display_value = self.display_date(
                            value
                        )

                    elif col in sum_columns:

                        try:

                            display_value = (
                                f"{float(value):,.2f}"
                            )

                        except (TypeError, ValueError):

                            display_value = str(
                                value
                            )

                    else:

                        display_value = str(
                            value
                        )

                    value_length = len(
                        str(display_value)
                    )

                max_length = max(
                    max_length,
                    value_length
                )

            # -----------------------------------------------------
            # Summary value may be wider than record values.
            # -----------------------------------------------------

            if col in sum_columns:

                summary_values = pd.to_numeric(
                    self.current_data[col],
                    errors="coerce"
                )

                summary_value = summary_values.sum()

                max_length = max(
                    max_length,
                    len(
                        f"{summary_value:,.2f}"
                    )
                )

            width = max(
                100,
                min(
                    max_length * 8 + 30,
                    350
                )
            )

            column_widths[col] = width

        # =========================================================
        # HEADER
        # =========================================================

        for col_idx, col in enumerate(columns):

            self.data_frame.grid_columnconfigure(
                col_idx,
                minsize=column_widths[col]
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
                corner_radius=10,
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
        # DATA ROWS
        # =========================================================

        for row_idx, row in self.current_data.iterrows():

            for col_idx, col in enumerate(columns):

                value = row[col]

                if pd.isnull(value):

                    value = "-"

                else:

                    if col in date_columns:

                        value = self.display_date(
                            value
                        )

                    elif col in sum_columns:

                        try:

                            value = f"{float(value):,.2f}"

                        except (TypeError, ValueError):

                            value = str(
                                value
                            )

                    else:

                        value = str(
                            value
                        )

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
        # SUMMARY / TOTAL ROW
        # =========================================================

        summary_row = self.get_summary_row()

        summary_grid_row = (
            len(self.current_data) + 1
        )

        for col_idx, col in enumerate(columns):

            value = summary_row.get(
                col,
                ""
            )

            if col in sum_columns:

                try:

                    value = f"{float(value):,.2f}"

                except (TypeError, ValueError):

                    value = "0.00"

            if value == "":

                value = "-"

            ctk.CTkLabel(
                self.data_frame,
                text=value,
                font=ctk.CTkFont(
                    size=SIZES["normal_size"],
                    weight="bold"
                ),
                text_color=TEXT_LIGHT,
                fg_color=SIDEBAR_HOVER,
                corner_radius=8,
                anchor="w"
            ).grid(
                row=summary_grid_row,
                column=col_idx,
                padx=2,
                pady=(8, 5),
                ipadx=8,
                ipady=7,
                sticky="nsew"
            )

        # =========================================================
        # UPDATE SCROLL REGION
        # =========================================================

        self.data_frame.update_idletasks()

        self.table_canvas.configure(
            scrollregion=self.table_canvas.bbox("all")
        )

    # =============================================================
    # PREPARE DATA FOR EXPORT
    # =============================================================

    def get_export_data(self):

        """
        Create a copy of current_data for export.

        Dates are converted to DD-MM-YYYY.

        A summary row is appended at the bottom.
        """

        export_data = self.current_data.copy()

        date_columns = {
            "Entry Date",
            "Completion Date",
            "Dispatch Date",
            "Payment Date",
            "Bill Date",
            "Recorded At",
            "Date/Time",
            "Bill Raised Date"
        }

        # =========================================================
        # FORMAT DATES
        # =========================================================

        for col in date_columns:

            if col in export_data.columns:

                export_data[col] = export_data[col].apply(
                    self.display_date
                )

        # =========================================================
        # SUMMARY
        # =========================================================

        summary = self.get_summary_row()

        summary_dataframe = pd.DataFrame(
            [summary],
            columns=export_data.columns
        )

        export_data = pd.concat(
            [
                export_data,
                summary_dataframe
            ],
            ignore_index=True
        )

        return export_data

    # =============================================================
    # EXPORT EXCEL
    # =============================================================

    def export_excel(self):

        if self.current_data.empty:

            messagebox.showinfo(
                "Info",
                "No data to export."
            )

            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[
                ("Excel files", "*.xlsx")
            ]
        )

        if not file_path:

            return

        try:

            export_data = self.get_export_data()

            export_data.to_excel(
                file_path,
                index=False
            )

            messagebox.showinfo(
                "Success",
                "Excel exported successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # =============================================================
    # EXPORT PDF
    # =============================================================

    def export_pdf(self):

        if self.current_data.empty:

            messagebox.showinfo(
                "Info",
                "No data to export."
            )

            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[
                ("PDF files", "*.pdf")
            ]
        )

        if not file_path:

            return

        try:

            from reportlab.lib.pagesizes import (
                landscape,
                letter
            )

            from reportlab.platypus import (
                SimpleDocTemplate,
                Table,
                TableStyle
            )

            from reportlab.lib import colors

            # =====================================================
            # PREPARE DATA
            # =====================================================

            export_data = self.get_export_data()

            doc = SimpleDocTemplate(
                file_path,
                pagesize=landscape(letter)
            )

            data = [
                export_data.columns.tolist()
            ]

            data.extend(
                export_data
                .fillna("-")
                .astype(str)
                .values
                .tolist()
            )

            # =====================================================
            # CREATE TABLE
            # =====================================================

            table = Table(
                data,
                repeatRows=1
            )

            # Summary row index
            summary_row_index = len(data) - 1

            table_style = [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        PRIMARY
                    )
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, 0),
                    8
                ),
                (
                    "FONTSIZE",
                    (0, 1),
                    (-1, -1),
                    7
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor(
                        SIDEBAR_HOVER
                    )
                ),
                (
                    "FONTNAME",
                    (0, summary_row_index),
                    (-1, summary_row_index),
                    "Helvetica-Bold"
                ),
                (
                    "BACKGROUND",
                    (0, summary_row_index),
                    (-1, summary_row_index),
                    colors.HexColor(
                        SIDEBAR_HOVER
                    )
                ),
                (
                    "TEXTCOLOR",
                    (0, summary_row_index),
                    (-1, summary_row_index),
                    colors.white
                )
            ]

            table.setStyle(
                TableStyle(
                    table_style
                )
            )

            # =====================================================
            # BUILD PDF
            # =====================================================

            doc.build(
                [table]
            )

            messagebox.showinfo(
                "Success",
                "PDF exported successfully."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )