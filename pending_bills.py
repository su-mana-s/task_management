
import customtkinter as ctk
import pandas as pd
import tkinter as tk

from datetime import datetime
from tkinter import messagebox, filedialog

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from database import get_connection
from theme import *


# =============================================================
# SEARCHABLE COMBO BOX
# =============================================================

class SearchableComboBox(ctk.CTkFrame):

    def __init__(
        self,
        master,
        values=None,
        variable=None,
        command=None,
        width=400,
        height=40,
        font=None,
        dropdown_font=None,
        fg_color=None,
        border_color=None,
        button_color=None,
        button_hover_color=None,
        text_color=None,
        dropdown_fg_color=None,
        dropdown_text_color=None,
        dropdown_hover_color=None,
        corner_radius=10,
        **kwargs
    ):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.values = list(values or [])
        self.filtered_values = self.values.copy()

        self.variable = (
            variable
            if variable is not None
            else ctk.StringVar()
        )

        self.command = command

        self.width = width
        self.height = height

        self.font = font
        self.dropdown_font = dropdown_font or font

        self.fg_color = fg_color
        self.border_color = border_color
        self.button_color = button_color
        self.button_hover_color = button_hover_color
        self.text_color = text_color
        self.dropdown_fg_color = dropdown_fg_color
        self.dropdown_text_color = dropdown_text_color
        self.dropdown_hover_color = dropdown_hover_color
        self.corner_radius = corner_radius

        self.is_open = False
        self.dropdown = None

        # =====================================================
        # MAIN ENTRY
        # =====================================================

        self.entry = ctk.CTkEntry(
            self,
            width=width - 45,
            height=height,
            textvariable=self.variable,
            font=font,
            fg_color=fg_color,
            border_color=border_color,
            text_color=text_color,
            **kwargs
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        # =====================================================
        # DROPDOWN BUTTON
        # =====================================================

        self.button = ctk.CTkButton(
            self,
            text="▼",
            width=45,
            height=height,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            fg_color=button_color,
            hover_color=button_hover_color,
            text_color=text_color,
            corner_radius=0,
            command=self.toggle_dropdown
        )

        self.button.pack(
            side="right"
        )

        # =====================================================
        # EVENTS
        # =====================================================

        self.entry.bind(
            "<KeyRelease>",
            self.on_type
        )

        self.entry.bind(
            "<FocusIn>",
            self.on_focus
        )

        self.entry.bind(
            "<Down>",
            self.open_dropdown_event
        )

    # =========================================================
    # SET VALUES
    # =========================================================

    def configure_values(self, values):

        self.values = list(values or [])
        self.filtered_values = self.values.copy()

    # =========================================================
    # FILTER
    # =========================================================

    def on_type(self, event=None):

        search_text = (
            self.variable
            .get()
            .strip()
            .lower()
        )

        if not search_text:

            self.filtered_values = (
                self.values.copy()
            )

        else:

            self.filtered_values = [
                value
                for value in self.values
                if search_text in str(value).lower()
            ]

        self.show_dropdown()

    # =========================================================
    # FOCUS
    # =========================================================

    def on_focus(self, event=None):

        self.show_dropdown()

    # =========================================================
    # TOGGLE
    # =========================================================

    def toggle_dropdown(self):

        if self.is_open:

            self.hide_dropdown()

        else:

            self.filtered_values = (
                self.values.copy()
            )

            self.show_dropdown()

            self.entry.focus_set()

    # =========================================================
    # KEYBOARD
    # =========================================================

    def open_dropdown_event(self, event=None):

        self.show_dropdown()

        return "break"

    # =========================================================
    # SHOW DROPDOWN
    # =========================================================

    def show_dropdown(self):

        if self.dropdown is not None:

            try:
                self.dropdown.destroy()
            except Exception:
                pass

        self.update_idletasks()

        x = self.winfo_rootx()

        y = (
            self.winfo_rooty()
            + self.winfo_height()
        )

        self.dropdown = ctk.CTkToplevel(
            self
        )

        self.dropdown.overrideredirect(
            True
        )

        self.dropdown.geometry(
            f"{self.width}x300+{x}+{y}"
        )

        self.dropdown.configure(
            fg_color=(
                self.dropdown_fg_color
                or self.fg_color
                or "white"
            )
        )

        self.dropdown.lift()

        list_frame = ctk.CTkScrollableFrame(
            self.dropdown,
            width=self.width - 20,
            height=280,
            fg_color=(
                self.dropdown_fg_color
                or self.fg_color
                or "white"
            )
        )

        list_frame.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # =====================================================
        # NO RESULTS
        # =====================================================

        if not self.filtered_values:

            label = ctk.CTkLabel(
                list_frame,
                text="No matching records",
                font=self.dropdown_font,
                text_color=(
                    self.dropdown_text_color
                    or self.text_color
                )
            )

            label.pack(
                fill="x",
                padx=5,
                pady=8
            )

        # =====================================================
        # RESULTS
        # =====================================================

        else:

            for value in self.filtered_values:

                btn = ctk.CTkButton(
                    list_frame,
                    text=str(value),
                    anchor="w",
                    height=38,
                    font=self.dropdown_font,
                    fg_color="transparent",
                    hover_color=(
                        self.dropdown_hover_color
                        or self.button_hover_color
                    ),
                    corner_radius=self.corner_radius,
                    text_color=(
                        self.dropdown_text_color
                        or self.text_color
                    ),
                    command=lambda v=value: (
                        self.select_value(v)
                    )
                )

                btn.pack(
                    fill="x",
                    padx=2,
                    pady=1
                )

        self.is_open = True

        self.dropdown.bind(
            "<FocusOut>",
            self.on_dropdown_focus_out
        )

    # =========================================================
    # SELECT
    # =========================================================

    def select_value(self, value):

        self.variable.set(
            str(value)
        )

        self.hide_dropdown()

        self.entry.focus_set()

        if self.command:

            self.command(
                str(value)
            )

    # =========================================================
    # HIDE
    # =========================================================

    def hide_dropdown(self):

        if self.dropdown is not None:

            try:
                self.dropdown.destroy()
            except Exception:
                pass

            self.dropdown = None

        self.is_open = False

    # =========================================================
    # FOCUS OUT
    # =========================================================

    def on_dropdown_focus_out(self, event=None):

        self.after(
            100,
            self.check_focus
        )

    def check_focus(self):

        try:

            focused = self.focus_get()

            if focused != self.entry:

                self.hide_dropdown()

        except Exception:

            self.hide_dropdown()

    # =========================================================
    # SET
    # =========================================================

    def set(self, value):

        self.variable.set(
            str(value)
        )

    # =========================================================
    # GET
    # =========================================================

    def get(self):

        return self.variable.get()

    # =========================================================
    # DELETE
    # =========================================================

    def delete(
        self,
        first=0,
        last="end"
    ):

        self.entry.delete(
            first,
            last
        )

    # =========================================================
    # INSERT
    # =========================================================

    def insert(
        self,
        index,
        string
    ):

        self.entry.insert(
            index,
            string
        )

    # =========================================================
    # FOCUS
    # =========================================================

    def focus_set(self):

        self.entry.focus_set()


# =============================================================
# PENDING BILLS
# =============================================================

class PendingBills(ctk.CTkFrame):

    def __init__(self, master, user=None):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.user = user
        self.current_data = pd.DataFrame()

        # =====================================================
        # DATE HELPERS
        # =====================================================

        def display_date(value):

            if value is None:
                return "-"

            value = str(value).strip()

            if not value:
                return "-"

            try:

                return datetime.strptime(
                    value[:10],
                    "%Y-%m-%d"
                ).strftime(
                    "%d-%m-%Y"
                )

            except ValueError:

                return value

        def database_date(value):

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

        # =====================================================
        # TITLE
        # =====================================================

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

        # =====================================================
        # HELP TEXT
        # =====================================================

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

        # =====================================================
        # FILTER CARD
        # =====================================================

        self.filter_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS["toggle"],
            corner_radius=SIZES["large_corner_radius"]
        )

        self.filter_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        # =====================================================
        # CLIENT
        # =====================================================

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

        self.client_search = SearchableComboBox(
            self.filter_frame,
            values=["All Clients"],
            width=200,
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
            dropdown_text_color=COLORS["text"],
            dropdown_hover_color=SIDEBAR_HOVER,
            corner_radius=SIZES["corner_radius"]
        )

        self.client_search.set(
            "All Clients"
        )

        self.client_search.grid(
            row=0,
            column=1,
            padx=5,
            pady=12
        )

        # =====================================================
        # DEPARTMENT
        # =====================================================

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

        self.department_filter = SearchableComboBox(
            self.filter_frame,
            values=["All Departments"],
            width=180,
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
            dropdown_text_color=COLORS["text"],
            dropdown_hover_color=SIDEBAR_HOVER,
            corner_radius=SIZES["corner_radius"]
        )

        self.department_filter.set(
            "All Departments"
        )

        self.department_filter.grid(
            row=0,
            column=3,
            padx=5,
            pady=12
        )

        # =====================================================
        # BILL STATUS
        # =====================================================

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

        self.bill_status.set(
            "All Pending"
        )

        self.bill_status.grid(
            row=0,
            column=5,
            padx=5,
            pady=12
        )

        # =====================================================
        # ASSIGNED TO
        # =====================================================

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

        self.employee_filter.set(
            "All Employees"
        )

        self.employee_filter.grid(
            row=1,
            column=1,
            padx=5,
            pady=(0, 12)
        )

        # =====================================================
        # START DATE
        # =====================================================

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

        # =====================================================
        # END DATE
        # =====================================================

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

        # =====================================================
        # BUTTONS
        # =====================================================

        button_frame = ctk.CTkFrame(
            self.filter_frame,
            fg_color="transparent"
        )

        button_frame.grid(
            row=2,
            column=0,
            columnspan=6,
            padx=15,
            pady=(0, 15),
            sticky="e"
        )

        # -----------------------------------------------------
        # APPLY FILTERS
        # -----------------------------------------------------

        ctk.CTkButton(
            button_frame,
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
        ).pack(
            side="left",
            padx=(0, 8)
        )

        # -----------------------------------------------------
        # EXPORT PDF
        # -----------------------------------------------------

        ctk.CTkButton(
            button_frame,
            text="Export as PDF",
            command=self.export_pdf,
            width=150,
            height=SIZES["button_height"],
            fg_color=LOGOUT,
            hover_color=LOGOUT_HOVER,
            text_color=TEXT_LIGHT,
            corner_radius=SIZES["corner_radius"],
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            )
        ).pack(
            side="left"
        )

        # =====================================================
        # LOAD FILTER VALUES
        # =====================================================

        self.load_filter_values()
        self.load_employees()

        # =====================================================
        # DATA CONTAINER
        # =====================================================

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
    # LOAD CLIENTS / DEPARTMENTS
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

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not load filter values:\n{e}"
            )

        finally:

            conn.close()

    # =============================================================
    # LOAD EMPLOYEES
    # =============================================================

    def load_employees(self):

        conn = get_connection()

        try:

            cursor = conn.cursor()

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

            self.employee_filter.configure(
                values=["All Employees"] + employees
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not load employees:\n{e}"
            )

        finally:

            conn.close()

    # =============================================================
    # GENERATE
    # =============================================================

    def generate_report(self):

        client = (
            self.client_search
            .get()
            .strip()
        )

        department = (
            self.department_filter
            .get()
            .strip()
        )

        bill_status = (
            self.bill_status
            .get()
        )

        employee = (
            self.employee_filter
            .get()
        )

        # =========================================================
        # DATES
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

            start_date = (
                self.database_date(
                    start_date_display
                )
                if start_date_display
                else ""
            )

            end_date = (
                self.database_date(
                    end_date_display
                )
                if end_date_display
                else ""
            )

        except ValueError as e:

            messagebox.showerror(
                "Invalid Date",
                str(e)
            )

            return

        # =========================================================
        # QUERY
        # =========================================================

        query = """

            SELECT

                t.id AS "Task ID",

                c.name AS "Client",

                t.department AS "Department",

                u.username AS "Assigned To",

                CASE t.status
                    WHEN 0 THEN 'Inward'
                    WHEN 1 THEN 'Work Done'
                    WHEN 2 THEN 'Dispatched'
                    ELSE 'Unknown'
                END AS "Work Status",

                CASE
                    WHEN t.bill_amount > 0
                         AND COALESCE(
                             t.amount_pending_receipt,
                             0
                         ) > 0
                        THEN 'Bill Generated'

                    WHEN t.status = 1
                         AND (
                             t.bill_amount IS NULL
                             OR t.bill_amount <= 0
                         )
                        THEN 'Bill Not Generated'

                    ELSE 'Unknown'
                END AS "Bill Status",

                t.bill_number AS "Bill No",

                t.bill_date AS "Bill Date",

                t.bill_type AS "Bill Type",

                t.billed_under AS "Billed Under",


                t.bill_amount AS "Bill Amount",

                t.loading_charges AS "Loading Charges",

                t.gst_registration_fee AS "GST Registration Fee",

                t.actual_amount_received AS "Received",

                t.amount_pending_receipt AS "Pending",

                t.billing_remarks AS "Billing Remarks",

                bu.username AS "Bill Raised By",

                t.bill_raised_at AS "Bill Raised At",

                t.created_at AS "Entry Date",

                t.date_of_completion AS "Completion Date",

                t.date_of_despatch AS "Dispatch Date"

            FROM tasks t

            LEFT JOIN clients c
                ON t.client_id = c.id

            LEFT JOIN users u
                ON t.assigned_to = u.id

            LEFT JOIN users bu
                ON t.bill_raised_by = bu.id

            WHERE

                (

                    (
                        t.bill_amount > 0

                        AND COALESCE(
                            t.amount_pending_receipt,
                            0
                        ) > 0
                    )

                    OR

                    (
                        t.status = 1

                        AND (
                            t.bill_amount IS NULL
                            OR t.bill_amount <= 0
                        )
                    )

                )

        """

        params = []

        # =========================================================
        # CLIENT
        # =========================================================

        if client and client != "All Clients":

            query += """
                AND c.name = %s
            """

            params.append(
                client
            )

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

            params.append(
                department
            )

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

            params.append(
                employee
            )

        # =========================================================
        # BILL STATUS
        # =========================================================

        if bill_status == "Bill Generated":

            query += """

                AND t.bill_amount > 0

                AND COALESCE(
                    t.amount_pending_receipt,
                    0
                ) > 0

            """

        elif bill_status == "Bill Not Generated":

            query += """

                AND t.status = 1

                AND (
                    t.bill_amount IS NULL
                    OR t.bill_amount <= 0
                )

            """

        # =========================================================
        # DATES
        # =========================================================

        if start_date:

            query += """
                AND t.created_at::date >= %s
            """

            params.append(
                start_date
            )

        if end_date:

            query += """
                AND t.created_at::date <= %s
            """

            params.append(
                end_date
            )

        # =========================================================
        # SORT
        # =========================================================

        query += """
            ORDER BY t.id DESC
        """

        conn = get_connection()

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

        for widget in (
            self.data_frame
            .winfo_children()
        ):

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

        date_columns = {
            "Bill Date",
            "Bill Raised At",
            "Entry Date",
            "Completion Date",
            "Dispatch Date"
        }

        # =========================================================
        # WIDTHS
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

        for row_idx, row in (
            self.current_data.iterrows()
        ):

            for col_idx, col in enumerate(columns):

                value = row[col]

                if pd.isnull(value):

                    value = "-"

                elif col in date_columns:

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

        total_row = (
            len(self.current_data) + 1
        )

        totals = {
            "Task ID":
                f"{len(self.current_data)} items",

            "Bill Amount":
                self.current_data[
                    "Bill Amount"
                ].fillna(0).sum(),

            "Loading Charges":
                self.current_data[
                    "Loading Charges"
                ].fillna(0).sum(),

            "GST Registration Fee":
                self.current_data[
                    "GST Registration Fee"
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

    # =============================================================
    # EXPORT PDF
    # =============================================================

    def export_pdf(self):

        # ---------------------------------------------------------
        # Only export the currently filtered report.
        # ---------------------------------------------------------

        if self.current_data.empty:

            messagebox.showinfo(
                "Export PDF",
                "There is no data to export."
            )

            return

        # ---------------------------------------------------------
        # FILE NAME
        # ---------------------------------------------------------

        filename = (
            "Pending_Bills_"
            + datetime.now().strftime(
                "%d-%m-%Y_%H-%M-%S"
            )
            + ".pdf"
        )

        filepath = filedialog.asksaveasfilename(
            title="Export Pending Bills",
            defaultextension=".pdf",
            initialfile=filename,
            filetypes=[
                (
                    "PDF files",
                    "*.pdf"
                )
            ]
        )

        if not filepath:

            return

        try:

            # =====================================================
            # LANDSCAPE A4
            # =====================================================

            page_width, page_height = landscape(
                A4
            )

            document = SimpleDocTemplate(
                filepath,
                pagesize=landscape(A4),
                rightMargin=8 * mm,
                leftMargin=8 * mm,
                topMargin=8 * mm,
                bottomMargin=8 * mm
            )

            styles = getSampleStyleSheet()

            title_style = styles["Title"]

            normal_style = styles["Normal"]

            small_style = styles["Normal"].clone(
                "small"
            )

            small_style.fontSize = 6.5
            small_style.leading = 8

            # =====================================================
            # CONTENT
            # =====================================================

            elements = []

            elements.append(
                Paragraph(
                    "Pending Bills",
                    title_style
                )
            )

            elements.append(
                Spacer(
                    1,
                    4 * mm
                )
            )

            # -----------------------------------------------------
            # FILTER SUMMARY
            # -----------------------------------------------------

            client = self.client_search.get()

            department = (
                self.department_filter.get()
            )

            bill_status = (
                self.bill_status.get()
            )

            employee = (
                self.employee_filter.get()
            )

            start_date = (
                self.start_date.get().strip()
                or "-"
            )

            end_date = (
                self.end_date.get().strip()
                or "-"
            )

            filter_text = (
                f"<b>Client:</b> {client}    "
                f"<b>Department:</b> {department}    "
                f"<b>Bill Status:</b> {bill_status}<br/>"
                f"<b>Assigned To:</b> {employee}    "
                f"<b>Start Date:</b> {start_date}    "
                f"<b>End Date:</b> {end_date}"
            )

            elements.append(
                Paragraph(
                    filter_text,
                    normal_style
                )
            )

            elements.append(
                Spacer(
                    1,
                    4 * mm
                )
            )

            # =====================================================
            # TABLE DATA
            # =====================================================

            columns = list(
                self.current_data.columns
            )

            date_columns = {
                "Bill Date",
                "Bill Raised At",
                "Entry Date",
                "Completion Date",
                "Dispatch Date"
            }

            table_data = []

            # -----------------------------------------------------
            # HEADER
            # -----------------------------------------------------

            table_data.append(
                [
                    Paragraph(
                        str(column),
                        small_style
                    )
                    for column in columns
                ]
            )

            # -----------------------------------------------------
            # ROWS
            # -----------------------------------------------------

            for _, row in (
                self.current_data.iterrows()
            ):

                table_row = []

                for column in columns:

                    value = row[column]

                    if pd.isnull(value):

                        value = "-"

                    elif column in date_columns:

                        value = self.display_date(
                            value
                        )

                    else:

                        value = str(value)

                    table_row.append(
                        Paragraph(
                            str(value),
                            small_style
                        )
                    )

                table_data.append(
                    table_row
                )

            # =====================================================
            # TOTAL ROW
            # =====================================================

            totals = {
                "Task ID":
                    f"{len(self.current_data)} items",

                "Bill Amount":
                    self.current_data[
                        "Bill Amount"
                    ].fillna(0).sum(),

                "Loading Charges":
                    self.current_data[
                        "Loading Charges"
                    ].fillna(0).sum(),

                "GST Registration Fee":
                    self.current_data[
                        "GST Registration Fee"
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

            total_row = []

            for column in columns:

                value = totals.get(
                    column,
                    ""
                )

                if isinstance(
                    value,
                    (int, float)
                ):

                    value = f"{value:,.2f}"

                total_row.append(
                    Paragraph(
                        str(value),
                        small_style
                    )
                )

            table_data.append(
                total_row
            )

            # =====================================================
            # COLUMN WIDTHS
            # =====================================================

            available_width = (
                page_width
                - document.leftMargin
                - document.rightMargin
            )

            column_count = len(columns)

            if column_count:

                column_width = (
                    available_width
                    / column_count
                )

                column_widths = [
                    column_width
                    for _ in columns
                ]

            else:

                column_widths = None

            # =====================================================
            # TABLE
            # =====================================================

            table = Table(
                table_data,
                colWidths=column_widths,
                repeatRows=1
            )

            table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, 0),
                            colors.HexColor(
                                "#444444"
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
                            "ALIGN",
                            (0, 0),
                            (-1, 0),
                            "CENTER"
                        ),

                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "MIDDLE"
                        ),

                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.25,
                            colors.grey
                        ),

                        (
                            "BACKGROUND",
                            (0, -1),
                            (-1, -1),
                            colors.HexColor(
                                "#666666"
                            )
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
                            3
                        ),

                        (
                            "RIGHTPADDING",
                            (0, 0),
                            (-1, -1),
                            3
                        ),

                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            3
                        ),

                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            3
                        )
                    ]
                )
            )

            elements.append(
                table
            )

            # =====================================================
            # BUILD
            # =====================================================

            document.build(
                elements
            )

            messagebox.showinfo(
                "Export Successful",
                f"PDF exported successfully:\n\n{filepath}"
            )

        except Exception as e:

            messagebox.showerror(
                "PDF Export Error",
                str(e)
            )
