
import customtkinter as ctk
import tkinter as tk

from tkinter import messagebox, filedialog
from datetime import datetime

from database import get_connection
from theme import *

from searchable_combobox import SearchableComboBox

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib.units import mm


class PendingWork(ctk.CTkFrame):

    def __init__(self, master, user=None):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.user = user

        # =========================================================
        # FONTS
        # =========================================================

        self.title_font = ctk.CTkFont(
            size=SIZES["title_size"],
            weight="bold"
        )

        self.heading_font = ctk.CTkFont(
            size=SIZES["heading_size"],
            weight="bold"
        )

        self.normal_font = ctk.CTkFont(
            size=SIZES["normal_size"]
        )

        self.normal_bold_font = ctk.CTkFont(
            size=SIZES["normal_size"],
            weight="bold"
        )

        self.small_font = ctk.CTkFont(
            size=SIZES["small_size"]
        )

        self.small_bold_font = ctk.CTkFont(
            size=SIZES["small_size"],
            weight="bold"
        )

        self.card_value_font = ctk.CTkFont(
            size=SIZES["normal_size"] + 2
        )

        self.card_value_bold_font = ctk.CTkFont(
            size=SIZES["normal_size"] + 2,
            weight="bold"
        )

        # =========================================================
        # TITLE
        # =========================================================

        ctk.CTkLabel(
            self,
            text="Pending Works",
            font=self.title_font,
            text_color=COLORS["text"]
        ).pack(
            pady=(0, 5),
            padx=5,
            anchor="w"
        )

        # =========================================================
        # HELP
        # =========================================================

        ctk.CTkLabel(
            self,
            text=(
                "Pending work includes tasks that are Not Started "
                "or In Progress. Click 'View History' to see the "
                "date-wise updates recorded by employees."
            ),
            font=self.normal_font,
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

        self.client_filter = SearchableComboBox(
            self.filter_frame,
            values=["All Clients"],
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
            dropdown_hover_color=SIDEBAR_HOVER,
            dropdown_text_color=COLORS["text"],
            corner_radius=SIZES["corner_radius"]
        )

        self.client_filter.set("All Clients")

        self.client_filter.grid(
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
            width=170,
            height=SIZES["entry_height"],
            font=self.normal_font,
            dropdown_font=self.normal_font,
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

        self.department_filter.set("All Departments")

        self.department_filter.grid(
            row=0,
            column=3,
            padx=5,
            pady=12,
            sticky="ew"
        )

        # =========================================================
        # EMPLOYEE
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
            dropdown_hover_color=SIDEBAR_HOVER,
            dropdown_text_color=COLORS["text"],
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
        # STATUS
        # =========================================================

        ctk.CTkLabel(
            self.filter_frame,
            text="Status:",
            font=self.normal_bold_font,
            text_color=COLORS["text"]
        ).grid(
            row=1,
            column=0,
            padx=(15, 5),
            pady=(0, 12),
            sticky="w"
        )

        self.status_filter = SearchableComboBox(
            self.filter_frame,
            values=[
                "All Pending",
                "Not Started",
                "In Progress"
            ],
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
            dropdown_hover_color=SIDEBAR_HOVER,
            dropdown_text_color=COLORS["text"],
            corner_radius=SIZES["corner_radius"]
        )

        self.status_filter.set("All Pending")

        self.status_filter.grid(
            row=1,
            column=1,
            padx=5,
            pady=(0, 12),
            sticky="ew"
        )

        # =========================================================
        # DATE FROM
        # =========================================================

        ctk.CTkLabel(
            self.filter_frame,
            text="From:",
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
            corner_radius=SIZES["corner_radius"],
            font=self.normal_font
        )

        self.start_date.grid(
            row=1,
            column=3,
            padx=5,
            pady=(0, 12),
            sticky="ew"
        )

        # =========================================================
        # DATE TO
        # =========================================================

        ctk.CTkLabel(
            self.filter_frame,
            text="To:",
            font=self.normal_bold_font,
            text_color=COLORS["text"]
        ).grid(
            row=1,
            column=4,
            padx=(20, 5),
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
            corner_radius=SIZES["corner_radius"],
            font=self.normal_font
        )

        self.end_date.grid(
            row=1,
            column=5,
            padx=5,
            pady=(0, 12),
            sticky="ew"
        )

        # =========================================================
        # BUTTONS
        # =========================================================

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

        ctk.CTkButton(
            button_frame,
            text="Apply Filters",
            command=self.load_tasks,
            width=150,
            height=SIZES["button_height"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=TEXT_LIGHT,
            corner_radius=SIZES["corner_radius"],
            font=self.normal_bold_font
        ).pack(
            side="left",
            padx=(0, 8)
        )

        ctk.CTkButton(
            button_frame,
            text="Export PDF",
            command=self.export_pdf,
            width=150,
            height=SIZES["button_height"],
            fg_color=LOGOUT,
            hover_color=LOGOUT_HOVER,
            text_color=TEXT_LIGHT,
            corner_radius=SIZES["corner_radius"],
            font=self.normal_bold_font
        ).pack(
            side="left"
        )

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

        self.canvas = tk.Canvas(
            self.data_container,
            bg=COLORS["toggle"],
            highlightthickness=0
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # =========================================================
        # SCROLLBAR
        # =========================================================

        self.scrollbar = ctk.CTkScrollbar(
            self.data_container,
            orientation="vertical",
            command=self.canvas.yview
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        # =========================================================
        # DATA FRAME
        # =========================================================

        self.data_frame = ctk.CTkFrame(
            self.canvas,
            fg_color=COLORS["toggle"]
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.data_frame,
            anchor="nw"
        )

        self.data_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_canvas_window
        )

        # =========================================================
        # MOUSE WHEEL
        # =========================================================

        self.canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

        # =========================================================
        # CURRENT FILTERED TASKS
        # =========================================================

        self.current_tasks = []

        # =========================================================
        # LOAD DATA
        # =========================================================

        self.load_filter_values()
        self.load_tasks()

    # =============================================================
    # DATE HELPERS
    # =============================================================

    @staticmethod
    def format_date(value):

        if value is None:
            return "-"

        value = str(value).strip()

        if not value:
            return "-"

        formats = [
            "%d-%m-%Y",
            "%Y-%m-%d",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f"
        ]

        for date_format in formats:

            try:

                parsed = datetime.strptime(
                    value,
                    date_format
                )

                return parsed.strftime(
                    "%d-%m-%Y"
                )

            except ValueError:
                continue

        return value

    @staticmethod
    def format_timestamp(value):

        if value is None:
            return "-"

        value = str(value).strip()

        if not value:
            return "-"

        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%d-%m-%Y %H:%M:%S",
            "%d-%m-%Y %H:%M"
        ]

        for date_format in formats:

            try:

                parsed = datetime.strptime(
                    value,
                    date_format
                )

                if parsed.second:

                    return parsed.strftime(
                        "%d-%m-%Y %H:%M:%S"
                    )

                return parsed.strftime(
                    "%d-%m-%Y %H:%M"
                )

            except ValueError:
                continue

        # PostgreSQL timestamptz may arrive with timezone
        # information. Try ISO parsing as a fallback.

        try:

            parsed = datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )

            if parsed.second:

                return parsed.strftime(
                    "%d-%m-%Y %H:%M:%S"
                )

            return parsed.strftime(
                "%d-%m-%Y %H:%M"
            )

        except ValueError:
            pass

        return value

    @staticmethod
    def input_date_to_database(value):

        value = value.strip()

        if not value:
            return ""

        try:

            parsed = datetime.strptime(
                value,
                "%d-%m-%Y"
            )

            return parsed.strftime(
                "%Y-%m-%d"
            )

        except ValueError:

            raise ValueError(
                f"Invalid date '{value}'. "
                "Please use DD-MM-YYYY."
            )

    # =============================================================
    # RESIZE CANVAS
    # =============================================================

    def resize_canvas_window(self, event):

        self.canvas.itemconfigure(
            self.canvas_window,
            width=event.width
        )

        self.update_scroll_region()

    # =============================================================
    # UPDATE SCROLL REGION
    # =============================================================

    def update_scroll_region(self, event=None):

        try:

            self.data_frame.update_idletasks()

            self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )

        except tk.TclError:
            pass

    # =============================================================
    # MOUSE WHEEL
    # =============================================================

    def on_mousewheel(self, event):

        try:

            if self.canvas.winfo_exists():

                self.canvas.yview_scroll(
                    int(-1 * (event.delta / 120)),
                    "units"
                )

        except tk.TclError:
            pass

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
                SELECT DISTINCT c.name
                FROM clients c
                JOIN tasks t
                    ON t.client_id = c.id
                WHERE t.status IN (0, 10)
                ORDER BY c.name
            """)

            clients = [
                row[0]
                for row in cursor.fetchall()
                if row[0]
            ]

            self.client_filter.configure_values(
                ["All Clients"] + clients
            )

            # -----------------------------------------------------
            # DEPARTMENTS
            # -----------------------------------------------------

            cursor.execute("""
                SELECT DISTINCT department
                FROM tasks
                WHERE status IN (0, 10)
                ORDER BY department
            """)

            departments = [
                row[0]
                for row in cursor.fetchall()
                if row[0]
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
                if row[0]
            ]

            self.employee_filter.configure_values(
                ["All Employees"] + employees
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Could not load filters:\n{e}"
            )

        finally:

            cursor.close()
            conn.close()

    # =============================================================
    # LOAD TASKS
    # =============================================================

    def load_tasks(self):

        client = self.client_filter.get().strip()

        department = self.department_filter.get().strip()

        employee = self.employee_filter.get().strip()

        status_filter = self.status_filter.get().strip()

        start_date_input = self.start_date.get().strip()

        end_date_input = self.end_date.get().strip()

        # =========================================================
        # CONVERT DATES
        # =========================================================

        try:

            start_date = self.input_date_to_database(
                start_date_input
            )

            end_date = self.input_date_to_database(
                end_date_input
            )

        except ValueError as e:

            messagebox.showwarning(
                "Invalid Date",
                str(e)
            )

            return

        # =========================================================
        # QUERY
        #
        # The latest document associated with each task is used
        # for:
        #
        #   Nature of Papers
        #   How Received
        #   Received By
        #   Received Date
        #
        # PostgreSQL LATERAL JOIN ensures only one document is
        # returned for each task.
        # =========================================================

        query = """
            SELECT
                t.id,
                t.task_name,
                c.name,
                t.department,
                d.nature_of_papers,
                assigned.username,
                received.username,
                d.how_received,
                t.status,
                d.received_at,
                created.username

            FROM tasks t

            LEFT JOIN clients c
                ON t.client_id = c.id

            LEFT JOIN users assigned
                ON t.assigned_to = assigned.id

            LEFT JOIN users created
                ON t.created_by = created.id

            LEFT JOIN LATERAL (
                SELECT
                    doc.nature_of_papers,
                    doc.how_received,
                    doc.received_at,
                    doc.received_by
                FROM documents doc
                WHERE doc.task_id = t.id
                ORDER BY
                    doc.received_at DESC,
                    doc.id DESC
                LIMIT 1
            ) d
                ON TRUE

            LEFT JOIN users received
                ON d.received_by = received.id

            WHERE
                t.status IN (0, 10)
        """

        params = []

        # =========================================================
        # CLIENT FILTER
        # =========================================================

        if client and client != "All Clients":

            query += """
                AND c.name = %s
            """

            params.append(client)

        # =========================================================
        # DEPARTMENT FILTER
        # =========================================================

        if department and department != "All Departments":

            query += """
                AND t.department = %s
            """

            params.append(department)

        # =========================================================
        # EMPLOYEE FILTER
        # =========================================================

        if employee and employee != "All Employees":

            query += """
                AND assigned.username = %s
            """

            params.append(employee)

        # =========================================================
        # STATUS FILTER
        # =========================================================

        if status_filter == "Not Started":

            query += """
                AND t.status = 0
            """

        elif status_filter == "In Progress":

            query += """
                AND t.status = 10
            """

        # =========================================================
        # DATE FROM
        #
        # Date filtering is based on document.received_at.
        # =========================================================

        if start_date:

            query += """
                AND d.received_at::date >= %s
            """

            params.append(start_date)

        # =========================================================
        # DATE TO
        # =========================================================

        if end_date:

            query += """
                AND d.received_at::date <= %s
            """

            params.append(end_date)

        # =========================================================
        # ORDER
        # =========================================================

        query += """
            ORDER BY
                CASE
                    WHEN t.status = 10 THEN 0
                    ELSE 1
                END,
                t.id DESC
        """

        conn = get_connection()

        try:

            cursor = conn.cursor()

            cursor.execute(
                query,
                params
            )

            tasks = cursor.fetchall()

            self.current_tasks = tasks

            self.display_tasks(tasks)

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

            cursor.close()
            conn.close()

    # =============================================================
    # DISPLAY TASKS
    # =============================================================

    def display_tasks(self, tasks):

        for widget in self.data_frame.winfo_children():

            widget.destroy()

        if not tasks:

            ctk.CTkLabel(
                self.data_frame,
                text="No pending work found.",
                font=self.heading_font,
                text_color=COLORS["text_secondary"]
            ).pack(
                padx=30,
                pady=40
            )

            self.update_scroll_region()

            return

        for task in tasks:

            self.create_task(task)

        self.update_scroll_region()

    # =============================================================
    # CREATE TASK CARD
    # =============================================================

    def create_task(self, task):

        (
            task_id,
            task_name,
            client,
            department,
            papers,
            employee,
            received_by,
            how_received,
            status,
            received_date,
            created_by
        ) = task

        # =========================================================
        # OUTER CARD
        # =========================================================

        outer = ctk.CTkFrame(
            self.data_frame,
            fg_color=COLORS["card_alt"],
            corner_radius=SIZES["large_corner_radius"]
        )

        outer.pack(
            fill="x",
            padx=15,
            pady=8
        )

        # =========================================================
        # HEADER
        # =========================================================

        header = ctk.CTkFrame(
            outer,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(18, 14)
        )

        header.grid_columnconfigure(
            1,
            weight=1
        )

        # =========================================================
        # TASK NUMBER
        # =========================================================

        ctk.CTkLabel(
            header,
            text=f"TASK #{task_id}",
            font=ctk.CTkFont(
                size=SIZES["heading_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            padx=(0, 25),
            sticky="w"
        )

        # =========================================================
        # TASK NAME + CLIENT
        # =========================================================

        task_title_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        task_title_frame.grid(
            row=0,
            column=1,
            sticky="w"
        )

        ctk.CTkLabel(
            task_title_frame,
            text=task_name or "Unnamed Task",
            font=ctk.CTkFont(
                size=SIZES["heading_size"],
                weight="bold"
            ),
            text_color=COLORS["primary"],
            anchor="w"
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            task_title_frame,
            text=client or "No Client",
            font=self.normal_font,
            text_color=COLORS["text_secondary"],
            anchor="w"
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        # =========================================================
        # STATUS + RECEIVED DATE
        # =========================================================

        status_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        status_frame.grid(
            row=0,
            column=2,
            padx=(20, 20),
            sticky="e"
        )

        ctk.CTkLabel(
            status_frame,
            text=(
                "Work Status: "
                f"{self.status_to_text(status)}"
            ),
            font=self.normal_bold_font,
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            padx=(0, 18),
            sticky="e"
        )

        ctk.CTkLabel(
            status_frame,
            text=(
                "Received: "
                f"{self.format_date(received_date)}"
            ),
            font=self.normal_bold_font,
            text_color=COLORS["text_secondary"]
        ).grid(
            row=0,
            column=1,
            sticky="e"
        )

        # =========================================================
        # HISTORY BUTTON
        # =========================================================

        history_button = ctk.CTkButton(
            header,
            text="View History",
            width=140,
            height=36,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=TEXT_LIGHT,
            corner_radius=SIZES["corner_radius"],
            font=self.normal_bold_font
        )

        history_button.grid(
            row=0,
            column=3,
            sticky="e"
        )

        # =========================================================
        # MAIN INFORMATION CARD
        # =========================================================

        info_frame = ctk.CTkFrame(
            outer,
            fg_color=COLORS["toggle"],
            corner_radius=SIZES["corner_radius"]
        )

        info_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 18)
        )

        for column in range(4):

            info_frame.grid_columnconfigure(
                column,
                weight=1
            )

        # =========================================================
        # NATURE OF PAPERS
        # =========================================================

        ctk.CTkLabel(
            info_frame,
            text="Nature of Papers",
            font=self.normal_bold_font,
            text_color=COLORS["text_secondary"],
            anchor="w"
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            padx=18,
            pady=(16, 5),
            sticky="w"
        )

        ctk.CTkLabel(
            info_frame,
            text=papers or "-",
            font=self.card_value_bold_font,
            text_color=COLORS["text"],
            anchor="w",
            justify="left",
            wraplength=1200
        ).grid(
            row=1,
            column=0,
            columnspan=4,
            padx=18,
            pady=(0, 18),
            sticky="ew"
        )

        # =========================================================
        # DEPARTMENT
        # =========================================================

        ctk.CTkLabel(
            info_frame,
            text="Department",
            font=self.normal_bold_font,
            text_color=COLORS["text_secondary"],
            anchor="w"
        ).grid(
            row=2,
            column=0,
            padx=(18, 8),
            pady=(2, 5),
            sticky="w"
        )

        ctk.CTkLabel(
            info_frame,
            text=department or "-",
            font=self.card_value_bold_font,
            text_color=COLORS["text"],
            anchor="w"
        ).grid(
            row=3,
            column=0,
            padx=(18, 8),
            pady=(0, 18),
            sticky="w"
        )

        # =========================================================
        # ASSIGNED TO
        # =========================================================

        ctk.CTkLabel(
            info_frame,
            text="Assigned To",
            font=self.normal_bold_font,
            text_color=COLORS["text_secondary"],
            anchor="w"
        ).grid(
            row=2,
            column=1,
            padx=8,
            pady=(2, 5),
            sticky="w"
        )

        ctk.CTkLabel(
            info_frame,
            text=employee or "-",
            font=self.card_value_bold_font,
            text_color=COLORS["text"],
            anchor="w"
        ).grid(
            row=3,
            column=1,
            padx=8,
            pady=(0, 18),
            sticky="w"
        )

        # =========================================================
        # RECEIVED BY
        # =========================================================

        ctk.CTkLabel(
            info_frame,
            text="Received By",
            font=self.normal_bold_font,
            text_color=COLORS["text_secondary"],
            anchor="w"
        ).grid(
            row=2,
            column=2,
            padx=8,
            pady=(2, 5),
            sticky="w"
        )

        ctk.CTkLabel(
            info_frame,
            text=received_by or "-",
            font=self.card_value_bold_font,
            text_color=COLORS["text"],
            anchor="w"
        ).grid(
            row=3,
            column=2,
            padx=8,
            pady=(0, 18),
            sticky="w"
        )

        # =========================================================
        # HOW RECEIVED
        # =========================================================

        ctk.CTkLabel(
            info_frame,
            text="How Received",
            font=self.normal_bold_font,
            text_color=COLORS["text_secondary"],
            anchor="w"
        ).grid(
            row=2,
            column=3,
            padx=(8, 18),
            pady=(2, 5),
            sticky="w"
        )

        ctk.CTkLabel(
            info_frame,
            text=how_received or "-",
            font=self.card_value_bold_font,
            text_color=COLORS["text"],
            anchor="w"
        ).grid(
            row=3,
            column=3,
            padx=(8, 18),
            pady=(0, 18),
            sticky="w"
        )

        # =========================================================
        # HISTORY CONTAINER
        # =========================================================

        history_frame = ctk.CTkFrame(
            outer,
            fg_color=COLORS["toggle"],
            corner_radius=SIZES["corner_radius"]
        )

        history_frame.pack_forget()

        outer.history_frame = history_frame
        outer.history_expanded = False

        # =========================================================
        # HISTORY COMMAND
        # =========================================================

        history_button.configure(
            command=lambda
                tid=task_id,
                container=outer,
                btn=history_button:
                    self.toggle_history(
                        tid,
                        container,
                        btn
                    )
        )

    # =============================================================
    # TOGGLE HISTORY
    # =============================================================

    def toggle_history(
        self,
        task_id,
        parent,
        button
    ):

        history_frame = getattr(
            parent,
            "history_frame",
            None
        )

        if history_frame is None:
            return

        # =========================================================
        # COLLAPSE
        # =========================================================

        if getattr(
            parent,
            "history_expanded",
            False
        ):

            history_frame.pack_forget()

            parent.history_expanded = False

            button.configure(
                text="View History"
            )

            self.after(
                10,
                self.update_scroll_region
            )

            return

        # =========================================================
        # CLEAR OLD HISTORY
        # =========================================================

        for widget in history_frame.winfo_children():

            widget.destroy()

        # =========================================================
        # DATABASE
        # =========================================================

        conn = get_connection()

        try:

            cursor = conn.cursor()

            # -----------------------------------------------------
            # CURRENT STATUS
            # -----------------------------------------------------

            cursor.execute("""
                SELECT status
                FROM tasks
                WHERE id = %s
            """, (
                task_id,
            ))

            record = cursor.fetchone()

            if record:
                current_status = record[0]
            else:
                current_status = None

            # -----------------------------------------------------
            # TASK HISTORY
            # -----------------------------------------------------

            cursor.execute("""
                SELECT
                    t.id,
                    t.update_date,
                    u.username,
                    t.description,
                    t.created_at

                FROM task_updates t

                LEFT JOIN users u
                    ON t.updated_by = u.id

                WHERE t.task_id = %s

                ORDER BY
                    t.update_date DESC,
                    t.id DESC
            """, (
                task_id,
            ))

            updates = cursor.fetchall()

        except Exception as e:

            messagebox.showerror(
                "History Error",
                str(e)
            )

            return

        finally:

            cursor.close()
            conn.close()

        # =========================================================
        # HISTORY HEADER
        # =========================================================

        history_header = ctk.CTkFrame(
            history_frame,
            fg_color="transparent"
        )

        history_header.pack(
            fill="x",
            padx=18,
            pady=(15, 10)
        )

        history_header.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            history_header,
            text="Work History",
            font=self.heading_font,
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        # =========================================================
        # CURRENT STATUS
        # =========================================================

        if current_status is not None:

            ctk.CTkLabel(
                history_header,
                text=(
                    "Current Status: "
                    f"{self.status_to_text(current_status)}"
                ),
                font=self.normal_bold_font,
                text_color=COLORS["text_secondary"]
            ).grid(
                row=0,
                column=1,
                sticky="e"
            )

        # =========================================================
        # NO HISTORY
        # =========================================================

        if not updates:

            ctk.CTkLabel(
                history_frame,
                text=(
                    "No updates have been recorded "
                    "for this task yet."
                ),
                font=self.normal_font,
                text_color=COLORS["text_secondary"],
                anchor="w"
            ).pack(
                fill="x",
                padx=18,
                pady=(0, 18),
                anchor="w"
            )

        # =========================================================
        # HISTORY ENTRIES
        # =========================================================

        else:

            for (
                update_id,
                update_date,
                username,
                description,
                created_at
            ) in updates:

                entry = ctk.CTkFrame(
                    history_frame,
                    fg_color=COLORS["card_alt"],
                    corner_radius=SIZES["corner_radius"]
                )

                entry.pack(
                    fill="x",
                    padx=15,
                    pady=5
                )

                # -------------------------------------------------
                # ENTRY HEADER
                # -------------------------------------------------

                entry_header = ctk.CTkFrame(
                    entry,
                    fg_color="transparent"
                )

                entry_header.pack(
                    fill="x",
                    padx=15,
                    pady=(12, 5)
                )

                entry_header.grid_columnconfigure(
                    1,
                    weight=1
                )

                # -------------------------------------------------
                # USER
                # -------------------------------------------------

                ctk.CTkLabel(
                    entry_header,
                    text=f"Updated by: {username or '-'}",
                    font=self.normal_bold_font,
                    text_color=COLORS["primary_hover"]
                ).grid(
                    row=0,
                    column=0,
                    sticky="w"
                )

                # -------------------------------------------------
                # TIMESTAMP
                # -------------------------------------------------

                created_text = self.format_timestamp(
                    created_at
                )

                ctk.CTkLabel(
                    entry_header,
                    text=created_text,
                    font=self.card_value_bold_font,
                    text_color=COLORS["primary_hover"]
                ).grid(
                    row=0,
                    column=1,
                    sticky="e"
                )

                # -------------------------------------------------
                # DESCRIPTION LABEL
                # -------------------------------------------------

                ctk.CTkLabel(
                    entry,
                    text="What was done:",
                    font=self.normal_bold_font,
                    text_color=COLORS["primary_hover"],
                    anchor="w"
                ).pack(
                    fill="x",
                    padx=15,
                    pady=(3, 2),
                    anchor="w"
                )

                # -------------------------------------------------
                # DESCRIPTION
                # -------------------------------------------------

                ctk.CTkLabel(
                    entry,
                    text=description or "-",
                    font=self.card_value_bold_font,
                    text_color=COLORS["primary"],
                    anchor="w",
                    justify="left",
                    wraplength=1100
                ).pack(
                    fill="x",
                    padx=15,
                    pady=(0, 15),
                    anchor="w"
                )

        # =========================================================
        # SHOW HISTORY
        # =========================================================

        history_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 18)
        )

        parent.history_expanded = True

        button.configure(
            text="Hide History"
        )

        # =========================================================
        # FORCE LAYOUT
        # =========================================================

        self.update_idletasks()

        history_frame.update_idletasks()

        parent.update_idletasks()

        self.data_frame.update_idletasks()

        self.canvas.update_idletasks()

        self.update_scroll_region()

        # =========================================================
        # SCROLL TO HISTORY
        # =========================================================

        self.after(
            50,
            lambda:
                self.scroll_to_widget(
                    history_frame
                )
        )

    # =============================================================
    # SCROLL TO EXPANDED HISTORY
    # =============================================================

    def scroll_to_widget(self, widget):

        try:

            self.update_scroll_region()

            widget.update_idletasks()

            self.canvas.update_idletasks()

            bbox = self.canvas.bbox("all")

            if not bbox:
                return

            total_height = (
                bbox[3] - bbox[1]
            )

            canvas_height = (
                self.canvas.winfo_height()
            )

            if total_height <= canvas_height:
                return

            widget_y = widget.winfo_rooty()

            canvas_y = self.canvas.winfo_rooty()

            relative_y = (
                widget_y - canvas_y
            )

            current_top = (
                self.canvas.yview()[0]
                * total_height
            )

            target_y = (
                current_top
                + relative_y
                - 40
            )

            max_scroll = max(
                0,
                total_height - canvas_height
            )

            target_y = max(
                0,
                min(
                    target_y,
                    max_scroll
                )
            )

            fraction = (
                target_y / total_height
            )

            self.canvas.yview_moveto(
                fraction
            )

        except tk.TclError:
            pass

    # =============================================================
    # EXPORT PDF
    # =============================================================

    def export_pdf(self):

        # =========================================================
        # MAKE SURE PDF REPRESENTS WHAT IS CURRENTLY ON SCREEN
        # =========================================================

        if not self.current_tasks:

            messagebox.showinfo(
                "Export PDF",
                "There are no pending works to export."
            )

            return

        # =========================================================
        # FILE NAME
        # =========================================================

        filename = filedialog.asksaveasfilename(
            title="Export Pending Works",
            defaultextension=".pdf",
            filetypes=[
                ("PDF files", "*.pdf")
            ],
            initialfile=(
                "Pending_Works_"
                + datetime.now().strftime("%d-%m-%Y")
                + ".pdf"
            )
        )

        if not filename:
            return

        try:

            # =====================================================
            # LANDSCAPE A4
            # =====================================================

            doc = SimpleDocTemplate(
                filename,
                pagesize=landscape(A4),
                rightMargin=12 * mm,
                leftMargin=12 * mm,
                topMargin=12 * mm,
                bottomMargin=12 * mm
            )

            styles = getSampleStyleSheet()

            title_style = ParagraphStyle(
                "PendingTitle",
                parent=styles["Title"],
                fontSize=18,
                leading=22,
                alignment=TA_LEFT,
                spaceAfter=5
            )

            subtitle_style = ParagraphStyle(
                "PendingSubtitle",
                parent=styles["Normal"],
                fontSize=8,
                leading=11,
                textColor=colors.grey,
                spaceAfter=10
            )

            header_style = ParagraphStyle(
                "TableHeader",
                parent=styles["Normal"],
                fontSize=7,
                leading=9,
                textColor=colors.white
            )

            cell_style = ParagraphStyle(
                "TableCell",
                parent=styles["Normal"],
                fontSize=7,
                leading=9
            )

            small_style = ParagraphStyle(
                "SmallCell",
                parent=styles["Normal"],
                fontSize=6.5,
                leading=8
            )

            story = []

            # =====================================================
            # TITLE
            # =====================================================

            story.append(
                Paragraph(
                    "Pending Works",
                    title_style
                )
            )

            # =====================================================
            # FILTER SUMMARY
            # =====================================================

            client = self.client_filter.get().strip()
            department = self.department_filter.get().strip()
            employee = self.employee_filter.get().strip()
            status = self.status_filter.get().strip()
            start_date = self.start_date.get().strip()
            end_date = self.end_date.get().strip()

            filter_parts = []

            if client and client != "All Clients":
                filter_parts.append(
                    f"Client: {client}"
                )

            if (
                department
                and department != "All Departments"
            ):
                filter_parts.append(
                    f"Department: {department}"
                )

            if employee and employee != "All Employees":
                filter_parts.append(
                    f"Assigned To: {employee}"
                )

            if status and status != "All Pending":
                filter_parts.append(
                    f"Status: {status}"
                )

            if start_date:
                filter_parts.append(
                    f"From: {start_date}"
                )

            if end_date:
                filter_parts.append(
                    f"To: {end_date}"
                )

            if filter_parts:

                filter_text = (
                    "Filters: "
                    + " | ".join(filter_parts)
                )

            else:

                filter_text = "Filters: All Pending Works"

            story.append(
                Paragraph(
                    filter_text,
                    subtitle_style
                )
            )

            story.append(
                Paragraph(
                    (
                        f"Exported: "
                        f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} "
                        f"| Total Tasks: {len(self.current_tasks)}"
                    ),
                    subtitle_style
                )
            )

            # =====================================================
            # TABLE
            # =====================================================

            data = []

            data.append([
                Paragraph("Task", header_style),
                Paragraph("Task Name", header_style),
                Paragraph("Client", header_style),
                Paragraph("Department", header_style),
                Paragraph("Nature of Papers", header_style),
                Paragraph("Assigned To", header_style),
                Paragraph("Received By", header_style),
                Paragraph("How Received", header_style),
                Paragraph("Status", header_style),
                Paragraph("Received", header_style)
            ])

            for task in self.current_tasks:

                (
                    task_id,
                    task_name,
                    client,
                    department,
                    papers,
                    employee,
                    received_by,
                    how_received,
                    status,
                    received_date,
                    created_by
                ) = task

                data.append([
                    Paragraph(
                        str(task_id or "-"),
                        cell_style
                    ),

                    Paragraph(
                        str(task_name or "-"),
                        cell_style
                    ),

                    Paragraph(
                        str(client or "-"),
                        cell_style
                    ),

                    Paragraph(
                        str(department or "-"),
                        cell_style
                    ),

                    Paragraph(
                        str(papers or "-"),
                        small_style
                    ),

                    Paragraph(
                        str(employee or "-"),
                        cell_style
                    ),

                    Paragraph(
                        str(received_by or "-"),
                        cell_style
                    ),

                    Paragraph(
                        str(how_received or "-"),
                        cell_style
                    ),

                    Paragraph(
                        self.status_to_text(status),
                        cell_style
                    ),

                    Paragraph(
                        self.format_date(received_date),
                        cell_style
                    )
                ])

            # =====================================================
            # COLUMN WIDTHS
            # =====================================================

            page_width, page_height = landscape(A4)

            usable_width = (
                page_width
                - 24 * mm
            )

            col_widths = [
                11 * mm,   # Task
                34 * mm,   # Task Name
                30 * mm,   # Client
                25 * mm,   # Department
                45 * mm,   # Nature
                25 * mm,   # Assigned
                25 * mm,   # Received By
                25 * mm,   # How Received
                23 * mm,   # Status
                25 * mm    # Received
            ]

            current_width = sum(col_widths)

            if current_width > usable_width:

                scale = (
                    usable_width
                    / current_width
                )

                col_widths = [
                    width * scale
                    for width in col_widths
                ]

            table = Table(
                data,
                colWidths=col_widths,
                repeatRows=1,
                hAlign="LEFT"
            )

            table.setStyle(
                TableStyle([
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#333333")
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
                        0.4,
                        colors.grey
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
                    ),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [
                            colors.white,
                            colors.HexColor("#F3F3F3")
                        ]
                    )
                ])
            )

            story.append(table)

            # =====================================================
            # BUILD
            # =====================================================

            doc.build(story)

            messagebox.showinfo(
                "Export Successful",
                f"Pending works exported successfully to:\n\n{filename}"
            )

        except Exception as e:

            messagebox.showerror(
                "PDF Export Error",
                f"Could not export PDF:\n\n{e}"
            )

    # =============================================================
    # STATUS TEXT
    # =============================================================

    @staticmethod
    def status_to_text(status):

        if status == 0:
            return "Not Started"

        if status == 10:
            return "In Progress"

        if status == 1:
            return "Completed"

        if status == 2:
            return "Dispatched"

        return "Unknown"
