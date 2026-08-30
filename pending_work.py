
import customtkinter as ctk
import sqlite3
import tkinter as tk

from tkinter import messagebox
from datetime import datetime

from database import DB_NAME
from theme import *


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

        self.filter_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.filter_frame.grid_columnconfigure(
            3,
            weight=1
        )

        self.filter_frame.grid_columnconfigure(
            5,
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

        self.client_filter = ctk.CTkEntry(
            self.filter_frame,
            width=190,
            height=SIZES["entry_height"],
            placeholder_text="Client name",
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            corner_radius=SIZES["corner_radius"]
        )

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

        self.department_filter = ctk.CTkEntry(
            self.filter_frame,
            width=170,
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

        self.employee_filter = ctk.CTkComboBox(
            self.filter_frame,
            values=["All Employees"],
            width=180,
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

        self.status_filter = ctk.CTkComboBox(
            self.filter_frame,
            values=[
                "All Pending",
                "Not Started",
                "In Progress"
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

        self.status_filter.set(
            "All Pending"
        )

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
            corner_radius=SIZES["corner_radius"]
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
            corner_radius=SIZES["corner_radius"]
        )

        self.end_date.grid(
            row=1,
            column=5,
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
            command=self.load_tasks,
            width=150,
            height=SIZES["button_height"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=TEXT_LIGHT,
            corner_radius=SIZES["corner_radius"],
            font=self.normal_bold_font
        ).grid(
            row=2,
            column=0,
            columnspan=6,
            padx=15,
            pady=(0, 15),
            sticky="e"
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
        # LOAD DATA
        # =========================================================

        self.load_employees()
        self.load_tasks()

    # =============================================================
    # DATE HELPERS
    # =============================================================

    @staticmethod
    def format_date(value):

        """
        Convert database date values to DD-MM-YYYY.

        Handles:
            YYYY-MM-DD
            YYYY-MM-DD HH:MM:SS
            DD-MM-YYYY
            datetime/date objects
        """

        if value is None:
            return "-"

        value = str(value).strip()

        if not value:
            return "-"

        # ---------------------------------------------------------
        # Already DD-MM-YYYY
        # ---------------------------------------------------------

        try:

            parsed = datetime.strptime(
                value,
                "%d-%m-%Y"
            )

            return parsed.strftime(
                "%d-%m-%Y"
            )

        except ValueError:
            pass

        # ---------------------------------------------------------
        # YYYY-MM-DD
        # ---------------------------------------------------------

        try:

            parsed = datetime.strptime(
                value[:10],
                "%Y-%m-%d"
            )

            return parsed.strftime(
                "%d-%m-%Y"
            )

        except ValueError:
            pass

        # ---------------------------------------------------------
        # Other common datetime formats
        # ---------------------------------------------------------

        formats = [
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

        # ---------------------------------------------------------
        # If unknown format, return original value
        # ---------------------------------------------------------

        return value

    @staticmethod
    def format_timestamp(value):

        """
        Convert a timestamp to:

            DD-MM-YYYY HH:MM:SS

        The time is retained.
        """

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

        # ---------------------------------------------------------
        # Try to format the date portion while retaining
        # the original time if possible.
        # ---------------------------------------------------------

        if len(value) >= 10:

            date_part = value[:10]

            formatted_date = PendingWork.format_date(
                date_part
            )

            if formatted_date != date_part:

                remaining = value[10:].strip()

                if remaining:
                    return (
                        f"{formatted_date} "
                        f"{remaining}"
                    )

                return formatted_date

        return value

    @staticmethod
    def input_date_to_database(value):

        """
        Convert user-entered DD-MM-YYYY to
        database-friendly YYYY-MM-DD.

        Empty values remain empty.
        """

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
    # LOAD TASKS
    # =============================================================

    def load_tasks(self):

        client = self.client_filter.get().strip()

        department = (
            self.department_filter.get().strip()
        )

        employee = self.employee_filter.get()

        status_filter = self.status_filter.get()

        start_date_input = (
            self.start_date.get().strip()
        )

        end_date_input = (
            self.end_date.get().strip()
        )

        # =========================================================
        # CONVERT USER DATES
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
        # DATABASE QUERY
        #
        # entered_by = person who originally received/entered work
        # how_received = method through which work was received
        #
        # date_of_entry = date work was received/entered
        # =========================================================

        query = """
            SELECT
                r.inward_id,
                c.name,
                r.department,
                r.nature_of_papers,
                u.username,
                entered.username,
                r.how_received,
                r.status,
                r.date_of_entry

            FROM records r

            LEFT JOIN clients c
                ON r.client_id = c.id

            LEFT JOIN users u
                ON r.assigned_to = u.id

            LEFT JOIN users entered
                ON r.entered_by = entered.id

            WHERE
                r.status IN (0, 10)
        """

        params = []

        # =========================================================
        # CLIENT FILTER
        # =========================================================

        if client:

            query += """
                AND c.name LIKE ?
            """

            params.append(
                f"%{client}%"
            )

        # =========================================================
        # DEPARTMENT FILTER
        # =========================================================

        if department:

            query += """
                AND r.department LIKE ?
            """

            params.append(
                f"%{department}%"
            )

        # =========================================================
        # EMPLOYEE FILTER
        # =========================================================

        if (
            employee
            and employee != "All Employees"
        ):

            query += """
                AND u.username = ?
            """

            params.append(
                employee
            )

        # =========================================================
        # STATUS FILTER
        # =========================================================

        if status_filter == "Not Started":

            query += """
                AND r.status = 0
            """

        elif status_filter == "In Progress":

            query += """
                AND r.status = 10
            """

        # =========================================================
        # DATE FROM
        # =========================================================

        if start_date:

            query += """
                AND r.date_of_entry >= ?
            """

            params.append(
                start_date
            )

        # =========================================================
        # DATE TO
        # =========================================================

        if end_date:

            query += """
                AND r.date_of_entry <= ?
            """

            params.append(
                end_date
            )

        # =========================================================
        # ORDER
        # =========================================================

        query += """
            ORDER BY
                CASE
                    WHEN r.status = 10 THEN 0
                    ELSE 1
                END,
                r.inward_id DESC
        """

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            cursor.execute(
                query,
                params
            )

            tasks = cursor.fetchall()

            self.display_tasks(tasks)

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

        finally:

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
            client,
            department,
            papers,
            employee,
            received_by,
            how_received,
            status,
            received_date
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
        # CLIENT
        # =========================================================

        ctk.CTkLabel(
            header,
            text=client or "No Client",
            font=ctk.CTkFont(
                size=SIZES["heading_size"],
                weight="bold"
            ),
            text_color=COLORS["primary"],
            anchor="w"
        ).grid(
            row=0,
            column=1,
            sticky="w"
        )

        # =========================================================
        # STATUS + RECEIVED DATE
        #
        # Received Date is displayed beside Work Status.
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

        status_frame.grid_columnconfigure(
            0,
            weight=1
        )

        # ---------------------------------------------------------
        # WORK STATUS
        # ---------------------------------------------------------

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

        # ---------------------------------------------------------
        # RECEIVED DATE
        # ---------------------------------------------------------

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
        #
        # ROW 1:
        # Nature of Papers
        #
        # ROW 2:
        # Department | Assigned To | Received By | How Received
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

        # =========================================================
        # FOUR EQUAL COLUMNS
        # =========================================================

        for column in range(4):

            info_frame.grid_columnconfigure(
                column,
                weight=1
            )

        # =========================================================
        # ROW 1 - NATURE OF PAPERS
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
        # ROW 2 - DEPARTMENT
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
        # ROW 2 - ASSIGNED TO
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
        # ROW 2 - RECEIVED BY
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
        # ROW 2 - HOW RECEIVED
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
        #
        # Starts hidden.
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
        # HISTORY BUTTON COMMAND
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

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            # =====================================================
            # CURRENT STATUS
            #
            # Status is stored in records, NOT task_updates.
            # =====================================================

            cursor.execute("""
                SELECT status
                FROM records
                WHERE inward_id = ?
            """, (
                task_id,
            ))

            record = cursor.fetchone()

            if record:

                current_status = record[0]

            else:

                current_status = None

            # =====================================================
            # TASK HISTORY
            #
            # update_date is still retrieved only for sorting.
            # It is NOT displayed anymore.
            #
            # created_at is the only date/time displayed in history.
            # =====================================================

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

                WHERE t.record_id = ?

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

                # =================================================
                # ENTRY HEADER
                # =================================================

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

                # =================================================
                # USER
                # =================================================

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

                # =================================================
                # TIMESTAMP
                #
                # This is now the ONLY date displayed in the
                # expanded history.
                #
                # Format:
                # DD-MM-YYYY HH:MM:SS
                # =================================================

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

                # =================================================
                # DESCRIPTION LABEL
                # =================================================

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

                # =================================================
                # DESCRIPTION
                # =================================================

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
        # FORCE LAYOUT UPDATE
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

            bbox = self.canvas.bbox(
                "all"
            )

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

            # =====================================================
            # WIDGET POSITION
            # =====================================================

            widget_y = widget.winfo_rooty()

            canvas_y = self.canvas.winfo_rooty()

            relative_y = (
                widget_y - canvas_y
            )

            # =====================================================
            # CURRENT SCROLL POSITION
            # =====================================================

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
