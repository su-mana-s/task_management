import customtkinter as ctk
import pandas as pd
import tkinter as tk
import psycopg

from tkinter import messagebox, filedialog
from datetime import datetime
from decimal import Decimal

from database import get_connection
from theme import *

from searchable_combobox import SearchableComboBox


class PendingDispatch(ctk.CTkFrame):

    def __init__(self, master, user=None):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.user = user
        self.current_data = pd.DataFrame()

        # =========================================================
        # FONTS
        # =========================================================

        self.title_font = ctk.CTkFont(
            size=SIZES["title_size"],
            weight="bold"
        )

        self.normal_font = ctk.CTkFont(
            size=SIZES["normal_size"]
        )

        self.normal_bold_font = ctk.CTkFont(
            size=SIZES["normal_size"],
            weight="bold"
        )

        # =========================================================
        # TITLE
        # =========================================================

        ctk.CTkLabel(
            self,
            text="Pending Dispatch",
            font=self.title_font,
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
            font=self.normal_font,
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
        # FILTER GRID
        # =========================================================

        for column in range(6):
            self.filter_frame.grid_columnconfigure(
                column,
                weight=1
            )

        # =========================================================
        # CLIENT
        # =========================================================

        ctk.CTkLabel(
            self.filter_frame,
            text="Client:",
            font=self.normal_bold_font,
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            padx=(15, 5),
            pady=12,
            sticky="w"
        )

        self.client_search = SearchableComboBox(
            self.filter_frame,
            values=["All Clients"],
            width=200,
            height=SIZES["entry_height"],
            font=self.normal_font,
            dropdown_font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            button_color=SIDEBAR_HOVER,
            button_hover_color=COLORS["primary_hover"],
            text_color=COLORS["text"],
            dropdown_fg_color=COLORS["toggle"],
            dropdown_text_color=COLORS["text"],
            dropdown_hover_color=SIDEBAR_HOVER,
            corner_radius=SIZES["corner_radius"]
        )

        self.client_search.set("All Clients")

        self.client_search.grid(
            row=0,
            column=1,
            padx=5,
            pady=12,
            sticky="ew"
        )

        # =========================================================
        # DEPARTMENT
        # =========================================================

        ctk.CTkLabel(
            self.filter_frame,
            text="Department:",
            font=self.normal_bold_font,
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=2,
            padx=(20, 5),
            pady=12,
            sticky="w"
        )

        self.department_filter = SearchableComboBox(
            self.filter_frame,
            values=["All Departments"],
            width=180,
            height=SIZES["entry_height"],
            font=self.normal_font,
            dropdown_font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            button_color=SIDEBAR_HOVER,
            button_hover_color=COLORS["primary_hover"],
            text_color=COLORS["text"],
            dropdown_fg_color=COLORS["toggle"],
            dropdown_text_color=COLORS["text"],
            dropdown_hover_color=SIDEBAR_HOVER,
            corner_radius=SIZES["corner_radius"]
        )

        self.department_filter.set("All Departments")

        self.department_filter.grid(
            row=0,
            column=3,
            padx=5,
            pady=12,
            sticky="ew"
        )

        # =========================================================
        # ASSIGNED EMPLOYEE
        # =========================================================

        ctk.CTkLabel(
            self.filter_frame,
            text="Assigned To:",
            font=self.normal_bold_font,
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=4,
            padx=(20, 5),
            pady=12,
            sticky="w"
        )

        self.employee_filter = SearchableComboBox(
            self.filter_frame,
            values=["All Employees"],
            width=190,
            height=SIZES["entry_height"],
            font=self.normal_font,
            dropdown_font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            button_color=SIDEBAR_HOVER,
            button_hover_color=COLORS["primary_hover"],
            text_color=COLORS["text"],
            dropdown_fg_color=COLORS["toggle"],
            dropdown_text_color=COLORS["text"],
            dropdown_hover_color=SIDEBAR_HOVER,
            corner_radius=SIZES["corner_radius"]
        )

        self.employee_filter.set("All Employees")

        self.employee_filter.grid(
            row=0,
            column=5,
            padx=5,
            pady=12,
            sticky="ew"
        )

        # =========================================================
        # TASK NAME
        # =========================================================

        ctk.CTkLabel(
            self.filter_frame,
            text="Task Name:",
            font=self.normal_bold_font,
            text_color=COLORS["text"]
        ).grid(
            row=1,
            column=0,
            padx=(15, 5),
            pady=(0, 12),
            sticky="w"
        )

        self.task_name_filter = SearchableComboBox(
            self.filter_frame,
            values=["All Task Names"],
            width=200,
            height=SIZES["entry_height"],
            font=self.normal_font,
            dropdown_font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            button_color=SIDEBAR_HOVER,
            button_hover_color=COLORS["primary_hover"],
            text_color=COLORS["text"],
            dropdown_fg_color=COLORS["toggle"],
            dropdown_text_color=COLORS["text"],
            dropdown_hover_color=SIDEBAR_HOVER,
            corner_radius=SIZES["corner_radius"]
        )

        self.task_name_filter.set("All Task Names")

        self.task_name_filter.grid(
            row=1,
            column=1,
            padx=5,
            pady=(0, 12),
            sticky="ew"
        )

        # =========================================================
        # DATE FILTERS
        # =========================================================

        ctk.CTkLabel(
            self.filter_frame,
            text="Completion From:",
            font=self.normal_bold_font,
            text_color=COLORS["text"]
        ).grid(
            row=1,
            column=2,
            padx=(20, 5),
            pady=(0, 12),
            sticky="w"
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
            pady=(0, 12),
            sticky="ew"
        )

        ctk.CTkLabel(
            self.filter_frame,
            text="Completion To:",
            font=self.normal_bold_font,
            text_color=COLORS["text"]
        ).grid(
            row=2,
            column=0,
            padx=(15, 5),
            pady=(0, 12),
            sticky="w"
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
            row=2,
            column=1,
            padx=5,
            pady=(0, 12),
            sticky="ew"
        )

        # =========================================================
        # APPLY FILTERS
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
            font=self.normal_bold_font
        ).grid(
            row=2,
            column=4,
            padx=5,
            pady=(0, 12),
            sticky="e"
        )

        # =========================================================
        # EXPORT PDF
        # =========================================================

        ctk.CTkButton(
            self.filter_frame,
            text="Export as PDF",
            command=self.export_pdf,
            width=150,
            height=SIZES["button_height"],
            fg_color=LOGOUT,
            hover_color=LOGOUT_HOVER,
            text_color=TEXT_LIGHT,
            corner_radius=SIZES["corner_radius"],
            font=self.normal_bold_font
        ).grid(
            row=2,
            column=5,
            padx=(5, 15),
            pady=(0, 12),
            sticky="e"
        )

        # =========================================================
        # LOAD FILTER VALUES
        # =========================================================

        self.load_filter_values()

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
        # DATA FRAME
        # =========================================================

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

        # =========================================================
        # LOAD INITIAL REPORT
        # =========================================================

        self.generate_report()

    # =============================================================
    # DATE HELPERS
    # =============================================================

    def display_date(self, value):

        if value is None:
            return "-"

        try:

            if pd.isnull(value):
                return "-"

        except Exception:
            pass

        value = str(value).strip()

        if not value:
            return "-"

        try:

            return pd.to_datetime(
                value
            ).strftime("%d-%m-%Y")

        except (ValueError, TypeError):

            return value

    def database_date(self, value):

        if not value:
            return None

        try:

            return datetime.strptime(
                value,
                "%d-%m-%Y"
            ).date()

        except ValueError:

            raise ValueError(
                f"Invalid date: {value}\n"
                "Please enter the date as DD-MM-YYYY."
            )

    # =============================================================
    # LOAD FILTER VALUES
    # =============================================================

    def load_filter_values(self):

        conn = get_connection()

        try:

            cursor = conn.cursor()

            # -----------------------------------------------------
            # CLIENTS
            # -----------------------------------------------------

            cursor.execute("""
                SELECT DISTINCT name
                FROM clients
                WHERE name IS NOT NULL
                  AND TRIM(name) <> ''
                ORDER BY name
            """)

            clients = [
                row[0]
                for row in cursor.fetchall()
            ]

            self.client_search.configure_values(
                ["All Clients"] + clients
            )

            # -----------------------------------------------------
            # DEPARTMENTS
            # -----------------------------------------------------

            cursor.execute("""
                SELECT DISTINCT department
                FROM tasks
                WHERE department IS NOT NULL
                  AND TRIM(department) <> ''
                ORDER BY department
            """)

            departments = [
                row[0]
                for row in cursor.fetchall()
            ]

            self.department_filter.configure_values(
                ["All Departments"] + departments
            )

            # -----------------------------------------------------
            # EMPLOYEES
            # -----------------------------------------------------

            cursor.execute("""
                SELECT username
                FROM users
                WHERE is_active = TRUE
                ORDER BY username
            """)

            employees = [
                row[0]
                for row in cursor.fetchall()
            ]

            self.employee_filter.configure_values(
                ["All Employees"] + employees
            )

            # -----------------------------------------------------
            # TASK NAMES
            # -----------------------------------------------------

            cursor.execute("""
                SELECT DISTINCT task_name
                FROM tasks
                WHERE task_name IS NOT NULL
                  AND TRIM(task_name) <> ''
                ORDER BY task_name
            """)

            task_names = [
                row[0]
                for row in cursor.fetchall()
            ]

            self.task_name_filter.configure_values(
                ["All Task Names"] + task_names
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not load filter values:\n{e}"
            )

        finally:

            cursor.close()
            conn.close()

    # =============================================================
    # GENERATE REPORT
    # =============================================================

    def generate_report(self):

        client = self.client_search.get().strip()
        department = self.department_filter.get().strip()
        employee = self.employee_filter.get().strip()
        task_name = self.task_name_filter.get().strip()

        start_date_input = self.start_date.get().strip()
        end_date_input = self.end_date.get().strip()

        # =========================================================
        # DATES
        # =========================================================

        try:

            start_date = (
                self.database_date(start_date_input)
                if start_date_input
                else None
            )

            end_date = (
                self.database_date(end_date_input)
                if end_date_input
                else None
            )

        except ValueError as e:

            messagebox.showerror(
                "Invalid Date",
                str(e)
            )

            return

        # =========================================================
        # QUERY
        #
        # Pending Dispatch:
        #
        # tasks.status = 1
        #
        # Documents are joined through a LATERAL query so that
        # the latest document for each task is used.
        # =========================================================

        query = """
            SELECT
                t.id AS "Task ID",

                t.task_name AS "Task Name",

                c.name AS "Client",

                t.department AS "Department",

                u.username AS "Assigned To",

                d.nature_of_papers AS "Nature of Papers",

                d.how_received AS "How Received",

                received.username AS "Received By",

                d.received_at AS "Entry Date",

                t.date_of_completion AS "Completion Date",

                t.details_of_work_done AS "Work Done",

                t.how_despatched AS "Dispatch Mode",

                CASE
                    WHEN t.bill_raised = TRUE
                        THEN 'Bill Generated'
                    ELSE 'Bill Not Generated'
                END AS "Bill Status",

                t.bill_number AS "Bill No",

                t.bill_date AS "Bill Date",

                t.bill_amount AS "Bill Amount",

                t.amount_pending_receipt AS "Pending Amount"

            FROM tasks t

            LEFT JOIN clients c
                ON t.client_id = c.id

            LEFT JOIN users u
                ON t.assigned_to = u.id

            LEFT JOIN LATERAL (
                SELECT
                    d1.nature_of_papers,
                    d1.how_received,
                    d1.received_at,
                    d1.received_by
                FROM documents d1
                WHERE d1.task_id = t.id
                ORDER BY d1.received_at DESC, d1.id DESC
                LIMIT 1
            ) d
                ON TRUE

            LEFT JOIN users received
                ON d.received_by = received.id

            WHERE t.status = 1
        """

        params = []

        # =========================================================
        # CLIENT
        # =========================================================

        if client and client != "All Clients":

            query += """
                AND c.name = %s
            """

            params.append(client)

        # =========================================================
        # DEPARTMENT
        # =========================================================

        if (
            department
            and department != "All Departments"
        ):

            query += """
                AND t.department = %s
            """

            params.append(department)

        # =========================================================
        # EMPLOYEE
        # =========================================================

        if (
            employee
            and employee != "All Employees"
        ):

            query += """
                AND u.username = %s
            """

            params.append(employee)

        # =========================================================
        # TASK NAME
        # =========================================================

        if (
            task_name
            and task_name != "All Task Names"
        ):

            query += """
                AND t.task_name = %s
            """

            params.append(task_name)

        # =========================================================
        # COMPLETION FROM
        # =========================================================

        if start_date:

            query += """
                AND t.date_of_completion >= %s
            """

            params.append(start_date)

        # =========================================================
        # COMPLETION TO
        # =========================================================

        if end_date:

            query += """
                AND t.date_of_completion <= %s
            """

            params.append(end_date)

        # =========================================================
        # ORDER
        # =========================================================

        query += """
            ORDER BY
                t.date_of_completion ASC,
                t.id DESC
        """

        # =========================================================
        # DATABASE
        # =========================================================

        conn = get_connection()

        try:

            cursor = conn.cursor()

            cursor.execute(
                query,
                params
            )

            rows = cursor.fetchall()

            columns = [
                desc.name
                for desc in cursor.description
            ]

            self.current_data = pd.DataFrame(
                rows,
                columns=columns
            )

            self.display_data()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            cursor.close()
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

        columns = list(
            self.current_data.columns
        )

        widths = {}

        # =========================================================
        # CALCULATE COLUMN WIDTHS
        # =========================================================

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

                else:

                    value = str(value)

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
                font=self.normal_bold_font,
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

                elif col in [
                    "Entry Date",
                    "Completion Date",
                    "Bill Date"
                ]:

                    value = self.display_date(value)

                elif col in [
                    "Bill Amount",
                    "Pending Amount"
                ]:

                    try:

                        value = f"₹{float(value):,.2f}"

                    except (
                        ValueError,
                        TypeError
                    ):

                        value = str(value)

                else:

                    value = str(value)

                ctk.CTkLabel(
                    self.data_frame,
                    text=value,
                    font=self.normal_font,
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

        total_row = (
            len(self.current_data) + 1
        )

        bill_total = (
            pd.to_numeric(
                self.current_data["Bill Amount"],
                errors="coerce"
            )
            .fillna(0)
            .sum()
        )

        pending_total = (
            pd.to_numeric(
                self.current_data["Pending Amount"],
                errors="coerce"
            )
            .fillna(0)
            .sum()
        )

        for col_idx, col in enumerate(columns):

            value = ""

            if col == "Task ID":

                value = (
                    f"Total Pending Dispatch: "
                    f"{len(self.current_data)}"
                )

            elif col == "Bill Amount":

                value = (
                    f"₹{bill_total:,.2f}"
                )

            elif col == "Pending Amount":

                value = (
                    f"₹{pending_total:,.2f}"
                )

            ctk.CTkLabel(
                self.data_frame,
                text=value,
                font=self.normal_bold_font,
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

        # =========================================================
        # SCROLL REGION
        # =========================================================

        self.data_frame.update_idletasks()

        self.table_canvas.configure(
            scrollregion=self.table_canvas.bbox("all")
        )

    # =============================================================
    # EXPORT PDF
    # =============================================================

    def export_pdf(self):

        if self.current_data.empty:

            messagebox.showwarning(
                "No Data",
                "There is no filtered data to export."
            )

            return

        file_path = filedialog.asksaveasfilename(
            title="Export Pending Dispatch Report",
            defaultextension=".pdf",
            filetypes=[
                (
                    "PDF Files",
                    "*.pdf"
                )
            ]
        )

        if not file_path:

            return

        try:

            from reportlab.lib import colors
            from reportlab.lib.pagesizes import landscape, A4
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib.enums import TA_LEFT
            from reportlab.platypus import (
                SimpleDocTemplate,
                Table,
                TableStyle,
                Paragraph,
                Spacer
            )

            # =====================================================
            # PAGE
            # =====================================================

            document = SimpleDocTemplate(
                file_path,
                pagesize=landscape(A4),
                rightMargin=20,
                leftMargin=20,
                topMargin=20,
                bottomMargin=20
            )

            styles = getSampleStyleSheet()

            title_style = styles["Title"]
            title_style.alignment = TA_LEFT

            normal_style = styles["BodyText"]
            normal_style.fontSize = 7
            normal_style.leading = 9

            header_style = styles["BodyText"]
            header_style.fontSize = 7
            header_style.leading = 8

            # =====================================================
            # TITLE
            # =====================================================

            story = []

            story.append(
                Paragraph(
                    "Pending Dispatch Report",
                    title_style
                )
            )

            story.append(
                Spacer(
                    1,
                    10
                )
            )

            # =====================================================
            # FILTER SUMMARY
            # =====================================================

            filter_text = []

            client = self.client_search.get().strip()

            if client and client != "All Clients":

                filter_text.append(
                    f"Client: {client}"
                )

            department = (
                self.department_filter.get().strip()
            )

            if (
                department
                and department != "All Departments"
            ):

                filter_text.append(
                    f"Department: {department}"
                )

            employee = (
                self.employee_filter.get().strip()
            )

            if (
                employee
                and employee != "All Employees"
            ):

                filter_text.append(
                    f"Assigned To: {employee}"
                )

            task_name = (
                self.task_name_filter.get().strip()
            )

            if (
                task_name
                and task_name != "All Task Names"
            ):

                filter_text.append(
                    f"Task Name: {task_name}"
                )

            start_date = (
                self.start_date.get().strip()
            )

            if start_date:

                filter_text.append(
                    f"Completion From: {start_date}"
                )

            end_date = (
                self.end_date.get().strip()
            )

            if end_date:

                filter_text.append(
                    f"Completion To: {end_date}"
                )

            if filter_text:

                story.append(
                    Paragraph(
                        " | ".join(filter_text),
                        normal_style
                    )
                )

                story.append(
                    Spacer(
                        1,
                        8
                    )
                )

            # =====================================================
            # TABLE DATA
            # =====================================================

            columns = list(
                self.current_data.columns
            )

            table_data = []

            table_data.append(
                [
                    Paragraph(
                        str(col),
                        header_style
                    )
                    for col in columns
                ]
            )

            for _, row in self.current_data.iterrows():

                row_data = []

                for col in columns:

                    value = row[col]

                    if pd.isnull(value):

                        value = "-"

                    elif col in [
                        "Entry Date",
                        "Completion Date",
                        "Bill Date"
                    ]:

                        value = self.display_date(
                            value
                        )

                    elif col in [
                        "Bill Amount",
                        "Pending Amount"
                    ]:

                        try:

                            value = (
                                f"₹{float(value):,.2f}"
                            )

                        except (
                            ValueError,
                            TypeError
                        ):

                            value = str(value)

                    else:

                        value = str(value)

                    row_data.append(
                        Paragraph(
                            str(value),
                            normal_style
                        )
                    )

                table_data.append(
                    row_data
                )

            # =====================================================
            # SUMMARY ROW
            # =====================================================

            bill_total = (
                pd.to_numeric(
                    self.current_data["Bill Amount"],
                    errors="coerce"
                )
                .fillna(0)
                .sum()
            )

            pending_total = (
                pd.to_numeric(
                    self.current_data["Pending Amount"],
                    errors="coerce"
                )
                .fillna(0)
                .sum()
            )

            summary_row = []

            for col in columns:

                value = ""

                if col == "Task ID":

                    value = (
                        f"Total Pending Dispatch: "
                        f"{len(self.current_data)}"
                    )

                elif col == "Bill Amount":

                    value = (
                        f"₹{bill_total:,.2f}"
                    )

                elif col == "Pending Amount":

                    value = (
                        f"₹{pending_total:,.2f}"
                    )

                summary_row.append(
                    Paragraph(
                        value,
                        header_style
                    )
                )

            table_data.append(
                summary_row
            )

            # =====================================================
            # COLUMN WIDTHS
            # =====================================================

            page_width = landscape(A4)[0]

            usable_width = (
                page_width
                - 40
            )

            raw_widths = []

            for col in columns:

                max_length = len(
                    str(col)
                )

                for value in self.current_data[col]:

                    if pd.isnull(value):

                        value = "-"

                    else:

                        value = str(value)

                    max_length = max(
                        max_length,
                        len(value)
                    )

                raw_widths.append(
                    min(
                        max(
                            45,
                            max_length * 3.5
                        ),
                        120
                    )
                )

            total_raw_width = sum(
                raw_widths
            )

            if total_raw_width > usable_width:

                scale = (
                    usable_width
                    / total_raw_width
                )

                col_widths = [
                    width * scale
                    for width in raw_widths
                ]

            else:

                col_widths = raw_widths

            # =====================================================
            # TABLE
            # =====================================================

            table = Table(
                table_data,
                colWidths=col_widths,
                repeatRows=1
            )

            table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, 0),
                            colors.HexColor("#404040")
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
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "TOP"
                        ),
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.3,
                            colors.grey
                        ),
                        (
                            "BACKGROUND",
                            (0, -1),
                            (-1, -1),
                            colors.HexColor("#404040")
                        ),
                        (
                            "TEXTCOLOR",
                            (0, -1),
                            (-1, -1),
                            colors.white
                        ),
                        (
                            "FONTNAME",
                            (0, -1),
                            (-1, -1),
                            "Helvetica-Bold"
                        ),
                        (
                            "LEFTPADDING",
                            (0, 0),
                            (-1, -1),
                            4
                        ),
                        (
                            "RIGHTPADDING",
                            (0, 0),
                            (-1, -1),
                            4
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            4
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            4
                        )
                    ]
                )
            )

            story.append(table)

            # =====================================================
            # BUILD
            # =====================================================

            document.build(
                story
            )

            messagebox.showinfo(
                "Export Successful",
                f"Pending dispatch report exported successfully:\n\n"
                f"{file_path}"
            )

        except ImportError:

            messagebox.showerror(
                "Missing Package",
                "ReportLab is required to export PDF files.\n\n"
                "Install it using:\n"
                "pip install reportlab"
            )

        except Exception as e:

            messagebox.showerror(
                "Export Error",
                f"Could not export the PDF:\n\n{e}"
            )