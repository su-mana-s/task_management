import customtkinter as ctk

from datetime import date, datetime, timezone
from tkinter import messagebox
from zoneinfo import ZoneInfo

from database import get_connection
from theme import *
from searchable_combobox import SearchableComboBox


class UpdateTaskStatus(ctk.CTkFrame):

    IST = ZoneInfo("Asia/Kolkata")

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

        # =========================================================
        # PAGE GRID
        # =========================================================

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            2,
            weight=3
        )

        self.grid_rowconfigure(
            3,
            weight=2
        )

        # =========================================================
        # TITLE
        # =========================================================

        ctk.CTkLabel(
            self,
            text="Update Task Status",
            font=self.title_font,
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=(0, 5),
            sticky="w"
        )

        # =========================================================
        # DESCRIPTION
        # =========================================================

        ctk.CTkLabel(
            self,
            text=(
                "View your assigned pending work and record "
                "what you worked on today. Click a task to "
                "select it and update its status."
            ),
            font=self.normal_font,
            text_color=COLORS["primary_hover"],
            anchor="w"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=(0, 15),
            sticky="w"
        )

        # =========================================================
        # TOP AREA
        # =========================================================

        self.top_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.top_frame.grid(
            row=2,
            column=0,
            sticky="nsew"
        )

        self.top_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.top_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.top_frame.grid_rowconfigure(
            0,
            weight=1
        )

        # =========================================================
        # LEFT - TASK LIST
        # =========================================================

        self.task_card = ctk.CTkFrame(
            self.top_frame,
            fg_color=COLORS["toggle"],
            corner_radius=SIZES["large_corner_radius"]
        )

        self.task_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        ctk.CTkLabel(
            self.task_card,
            text="My Pending Tasks",
            font=self.heading_font,
            text_color=COLORS["text"]
        ).pack(
            padx=15,
            pady=(15, 10),
            anchor="w"
        )

        # =========================================================
        # FILTER FRAME
        # =========================================================

        self.filter_frame = ctk.CTkFrame(
            self.task_card,
            fg_color=COLORS["card_alt"],
            corner_radius=SIZES["corner_radius"]
        )

        self.filter_frame.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        self.filter_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.filter_frame.grid_columnconfigure(
            3,
            weight=1
        )

        # =========================================================
        # CLIENT FILTER
        # =========================================================

        ctk.CTkLabel(
            self.filter_frame,
            text="Client:",
            font=self.normal_bold_font,
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            padx=(12, 5),
            pady=10,
            sticky="w"
        )

        self.client_filter = SearchableComboBox(
            self.filter_frame,
            values=[],
            width=260,
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

        self.client_filter.grid(
            row=0,
            column=1,
            padx=5,
            pady=10,
            sticky="ew"
        )

        # =========================================================
        # DEPARTMENT FILTER
        # =========================================================

        ctk.CTkLabel(
            self.filter_frame,
            text="Department:",
            font=self.normal_bold_font,
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=2,
            padx=(12, 5),
            pady=10,
            sticky="w"
        )

        self.department_filter = SearchableComboBox(
            self.filter_frame,
            values=[],
            width=260,
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

        self.department_filter.grid(
            row=0,
            column=3,
            padx=5,
            pady=10,
            sticky="ew"
        )

        # =========================================================
        # FILTER BUTTONS
        # =========================================================

        button_frame = ctk.CTkFrame(
            self.filter_frame,
            fg_color="transparent"
        )

        button_frame.grid(
            row=1,
            column=0,
            columnspan=4,
            padx=10,
            pady=(0, 10),
            sticky="e"
        )

        ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_filters,
            width=90,
            height=SIZES["button_height"],
            fg_color=COLORS["input"],
            hover_color=SIDEBAR_HOVER,
            text_color=COLORS["text"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=SIZES["corner_radius"],
            font=self.normal_bold_font
        ).pack(
            side="left",
            padx=(0, 8)
        )

        ctk.CTkButton(
            button_frame,
            text="Apply Filters",
            command=self.load_tasks,
            width=130,
            height=SIZES["button_height"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=TEXT_LIGHT,
            corner_radius=SIZES["corner_radius"],
            font=self.normal_bold_font
        ).pack(
            side="left"
        )

        # =========================================================
        # TASK SCROLL
        # =========================================================

        self.task_scroll = ctk.CTkScrollableFrame(
            self.task_card,
            fg_color="transparent"
        )

        self.task_scroll.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        # =========================================================
        # RIGHT - TASK UPDATE
        # =========================================================

        self.update_card = ctk.CTkFrame(
            self.top_frame,
            fg_color=COLORS["toggle"],
            corner_radius=SIZES["large_corner_radius"]
        )

        self.update_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )

        self.update_scroll = ctk.CTkScrollableFrame(
            self.update_card,
            fg_color="transparent"
        )

        self.update_scroll.pack(
            fill="both",
            expand=True,
            padx=0,
            pady=0
        )

        # =========================================================
        # UPDATE HEADER
        # =========================================================

        ctk.CTkLabel(
            self.update_scroll,
            text="Task Update",
            font=self.heading_font,
            text_color=COLORS["text"]
        ).pack(
            padx=20,
            pady=(20, 15),
            anchor="w"
        )

        # =========================================================
        # SELECTED TASK
        # =========================================================

        self.selected_label = ctk.CTkLabel(
            self.update_scroll,
            text="Select a task from the list.",
            font=self.normal_font,
            text_color=COLORS["text_secondary"],
            wraplength=500,
            justify="left",
            anchor="w"
        )

        self.selected_label.pack(
            fill="x",
            padx=20,
            pady=(0, 15),
            anchor="w"
        )

        # =========================================================
        # STATUS
        # =========================================================

        ctk.CTkLabel(
            self.update_scroll,
            text="Current / New Status",
            font=self.normal_bold_font,
            text_color=COLORS["text"]
        ).pack(
            padx=20,
            pady=(5, 5),
            anchor="w"
        )

        self.status_dropdown = ctk.CTkComboBox(
            self.update_scroll,
            values=[
                "Not Started",
                "In Progress"
            ],
            width=240,
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

        self.status_dropdown.set(
            "In Progress"
        )

        self.status_dropdown.pack(
            padx=20,
            pady=(0, 15),
            anchor="w"
        )

        # =========================================================
        # DATE
        # =========================================================

        ctk.CTkLabel(
            self.update_scroll,
            text="Update Date",
            font=self.normal_bold_font,
            text_color=COLORS["text"]
        ).pack(
            padx=20,
            pady=(5, 5),
            anchor="w"
        )

        self.update_date_label = ctk.CTkLabel(
            self.update_scroll,
            text=self.format_datetime_ist(
                datetime.now(self.IST)
            ),
            font=self.normal_bold_font,
            text_color=COLORS["text_secondary"]
        )

        self.update_date_label.pack(
            padx=20,
            pady=(0, 15),
            anchor="w"
        )

        # =========================================================
        # DESCRIPTION
        # =========================================================

        ctk.CTkLabel(
            self.update_scroll,
            text="What did you do today?",
            font=self.normal_bold_font,
            text_color=COLORS["text"]
        ).pack(
            padx=20,
            pady=(5, 5),
            anchor="w"
        )

        self.description = ctk.CTkTextbox(
            self.update_scroll,
            height=180,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            corner_radius=SIZES["corner_radius"]
        )

        self.description.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        # =========================================================
        # SAVE BUTTON
        # =========================================================

        self.save_button = ctk.CTkButton(
            self.update_scroll,
            text="Save Update",
            command=self.save_update,
            width=180,
            height=SIZES["button_height"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color=TEXT_LIGHT,
            corner_radius=SIZES["corner_radius"],
            font=self.normal_bold_font
        )

        self.save_button.pack(
            padx=20,
            pady=(0, 20),
            anchor="e"
        )

        # =========================================================
        # TASK HISTORY PANEL
        # =========================================================

        self.history_card = ctk.CTkFrame(
            self,
            fg_color=COLORS["toggle"],
            corner_radius=SIZES["large_corner_radius"]
        )

        self.history_card.grid(
            row=3,
            column=0,
            sticky="nsew",
            pady=(10, 0)
        )

        self.history_card.grid_columnconfigure(
            0,
            weight=1
        )

        self.history_card.grid_rowconfigure(
            1,
            weight=1
        )

        # =========================================================
        # HISTORY HEADER
        # =========================================================

        self.history_header = ctk.CTkFrame(
            self.history_card,
            fg_color="transparent"
        )

        self.history_header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(12, 5)
        )

        self.history_header.grid_columnconfigure(
            0,
            weight=1
        )

        self.history_title = ctk.CTkLabel(
            self.history_header,
            text="Task History",
            font=self.heading_font,
            text_color=COLORS["text"]
        )

        self.history_title.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.history_task_label = ctk.CTkLabel(
            self.history_header,
            text="Select a task to view its history.",
            font=self.small_font,
            text_color=COLORS["text_secondary"]
        )

        self.history_task_label.grid(
            row=0,
            column=1,
            sticky="e"
        )

        # =========================================================
        # HISTORY SCROLL
        # =========================================================

        self.history_scroll = ctk.CTkScrollableFrame(
            self.history_card,
            fg_color=COLORS["input"],
            corner_radius=SIZES["corner_radius"]
        )

        self.history_scroll.grid(
            row=1,
            column=0,
            padx=15,
            pady=(5, 15),
            sticky="nsew"
        )

        self.history_scroll.grid_columnconfigure(
            0,
            weight=1
        )

        # =========================================================
        # STATE
        # =========================================================

        self.selected_task_id = None

        self.show_history_message(
            "Select a task from My Pending Tasks to view its history."
        )

        self.load_filter_values()
        self.load_tasks()

    # =============================================================
    # GET CURRENT USER ID
    # =============================================================

    def get_user_id(self):

        if self.user is None:
            return None

        if isinstance(self.user, int):
            return self.user

        if isinstance(self.user, dict):

            return (
                self.user.get("id")
                or self.user.get("user_id")
            )

        if hasattr(self.user, "id"):
            return self.user.id

        return None

    # =============================================================
    # DATE FORMAT
    # =============================================================

    @staticmethod
    def format_date_display(value):

        if not value:
            return "-"

        try:

            if isinstance(value, datetime):
                return value.strftime("%d-%m-%Y")

            if isinstance(value, date):
                return value.strftime("%d-%m-%Y")

            return datetime.strptime(
                str(value),
                "%Y-%m-%d"
            ).strftime("%d-%m-%Y")

        except (ValueError, TypeError):

            return str(value)

    # =============================================================
    # DATETIME FORMAT - IST
    # =============================================================

    @staticmethod
    def format_datetime_ist(value):

        if not value:
            return "-"

        try:

            ist = ZoneInfo("Asia/Kolkata")

            if isinstance(value, datetime):

                if value.tzinfo is None:

                    value = value.replace(
                        tzinfo=ZoneInfo("UTC")
                    )

                value = value.astimezone(ist)

                return value.strftime(
                    "%d-%m-%Y %H:%M:%S IST"
                )

            if isinstance(value, date):

                return value.strftime(
                    "%d-%m-%Y"
                ) + " 00:00:00 IST"

            value_string = str(value)

            parsed = datetime.fromisoformat(
                value_string.replace(
                    "Z",
                    "+00:00"
                )
            )

            if parsed.tzinfo is None:

                parsed = parsed.replace(
                    tzinfo=ZoneInfo("UTC")
                )

            parsed = parsed.astimezone(ist)

            return parsed.strftime(
                "%d-%m-%Y %H:%M:%S IST"
            )

        except Exception:

            return str(value)

    # =============================================================
    # LOAD FILTER VALUES
    #
    # CURRENT SCHEMA:
    #
    # clients
    # tasks
    #
    # NO records table.
    # =============================================================

    def load_filter_values(self):

        user_id = self.get_user_id()

        if user_id is None:
            return

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            # -----------------------------------------------------
            # CLIENTS
            # -----------------------------------------------------

            cursor.execute("""
                SELECT DISTINCT
                    c.name

                FROM tasks t

                INNER JOIN clients c
                    ON t.client_id = c.id

                WHERE
                    t.assigned_to = %s
                    AND t.status IN (0, 10)
                    AND c.name IS NOT NULL
                    AND TRIM(c.name) <> ''

                ORDER BY
                    c.name
            """, (
                user_id,
            ))

            clients = [
                row[0]
                for row in cursor.fetchall()
            ]

            # -----------------------------------------------------
            # DEPARTMENTS
            # -----------------------------------------------------

            cursor.execute("""
                SELECT DISTINCT
                    t.department

                FROM tasks t

                WHERE
                    t.assigned_to = %s
                    AND t.status IN (0, 10)
                    AND t.department IS NOT NULL
                    AND TRIM(t.department) <> ''

                ORDER BY
                    t.department
            """, (
                user_id,
            ))

            departments = [
                row[0]
                for row in cursor.fetchall()
            ]

            self.client_filter.configure_values(
                clients
            )

            self.department_filter.configure_values(
                departments
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

    # =============================================================
    # CLEAR FILTERS
    # =============================================================

    def clear_filters(self):

        self.client_filter.set("")
        self.department_filter.set("")

        self.load_filter_values()
        self.load_tasks()

    # =============================================================
    # LOAD TASKS
    #
    # CURRENT SCHEMA:
    #
    # tasks.id
    # tasks.task_name
    # tasks.client_id
    # tasks.department
    # tasks.created_at
    # tasks.status
    # tasks.assigned_to
    #
    # No nature_of_papers.
    # No records table.
    # =============================================================

    def load_tasks(self):

        for widget in self.task_scroll.winfo_children():
            widget.destroy()

        user_id = self.get_user_id()

        if user_id is None:

            ctk.CTkLabel(
                self.task_scroll,
                text="Unable to identify the logged-in user.",
                font=self.normal_font,
                text_color=COLORS["text_secondary"]
            ).pack(
                padx=20,
                pady=20
            )

            return

        client_filter = self.client_filter.get().strip()
        department_filter = self.department_filter.get().strip()

        conn = None
        cursor = None
        tasks = []

        try:

            conn = get_connection()
            cursor = conn.cursor()

            query = """
                SELECT
                    t.id,
                    t.task_name,
                    c.name,
                    t.department,
                    t.created_at,
                    t.status

                FROM tasks t

                LEFT JOIN clients c
                    ON t.client_id = c.id

                WHERE
                    t.assigned_to = %s
                    AND t.status IN (0, 10)
            """

            params = [
                user_id
            ]

            # -----------------------------------------------------
            # CLIENT FILTER
            # -----------------------------------------------------

            if client_filter:

                query += """
                    AND c.name ILIKE %s
                """

                params.append(
                    f"%{client_filter}%"
                )

            # -----------------------------------------------------
            # DEPARTMENT FILTER
            # -----------------------------------------------------

            if department_filter:

                query += """
                    AND t.department ILIKE %s
                """

                params.append(
                    f"%{department_filter}%"
                )

            query += """
                ORDER BY
                    CASE
                        WHEN t.status = 10 THEN 0
                        ELSE 1
                    END,
                    t.id DESC
            """

            cursor.execute(
                query,
                params
            )

            tasks = cursor.fetchall()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            return

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        if not tasks:

            if client_filter or department_filter:

                text = (
                    "No pending tasks match the selected filters."
                )

            else:

                text = (
                    "No pending tasks are currently assigned to you."
                )

            ctk.CTkLabel(
                self.task_scroll,
                text=text,
                font=self.normal_font,
                text_color=COLORS["text_secondary"],
                wraplength=400,
                justify="center"
            ).pack(
                padx=20,
                pady=30
            )

            return

        for task in tasks:

            self.create_task_card(
                task
            )

    # =============================================================
    # CREATE TASK CARD
    # =============================================================

    def create_task_card(self, task):

        (
            task_id,
            task_name,
            client,
            department,
            created_at,
            status
        ) = task

        status_text = self.status_to_text(
            status
        )

        card = ctk.CTkFrame(
            self.task_scroll,
            fg_color=COLORS["card_alt"],
            corner_radius=SIZES["corner_radius"]
        )

        card.pack(
            fill="x",
            padx=5,
            pady=5
        )

        # =========================================================
        # HEADER
        # =========================================================

        header = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=15,
            pady=(12, 8)
        )

        header.grid_columnconfigure(
            1,
            weight=1
        )

        # Task number

        task_label = ctk.CTkLabel(
            header,
            text=f"Task #{task_id}",
            font=self.normal_bold_font,
            text_color=COLORS["text"],
            anchor="w"
        )

        task_label.grid(
            row=0,
            column=0,
            padx=(0, 12),
            sticky="w"
        )

        # Task name

        name_label = ctk.CTkLabel(
            header,
            text=task_name or "Unnamed Task",
            font=self.normal_bold_font,
            text_color=COLORS["primary"],
            anchor="w",
            justify="left",
            wraplength=300
        )

        name_label.grid(
            row=0,
            column=1,
            sticky="w"
        )

        # Status

        status_label = ctk.CTkLabel(
            header,
            text=status_text,
            font=self.normal_bold_font,
            text_color=COLORS["primary_hover"],
            anchor="e"
        )

        status_label.grid(
            row=0,
            column=2,
            padx=(15, 0),
            sticky="e"
        )

        # =========================================================
        # DETAILS
        #
        # Deliberately compact.
        # =========================================================

        details = ctk.CTkFrame(
            card,
            fg_color=COLORS["toggle"],
            corner_radius=SIZES["corner_radius"]
        )

        details.pack(
            fill="x",
            padx=15,
            pady=(0, 12)
        )

        details.grid_columnconfigure(
            1,
            weight=1
        )

        # Client

        ctk.CTkLabel(
            details,
            text="Client",
            font=self.normal_font,
            text_color=COLORS["primary_hover"],
            anchor="w"
        ).grid(
            row=0,
            column=0,
            padx=(12, 5),
            pady=(10, 2),
            sticky="w"
        )

        ctk.CTkLabel(
            details,
            text=client or "-",
            font=self.normal_bold_font,
            text_color=COLORS["text"],
            anchor="w"
        ).grid(
            row=1,
            column=0,
            padx=(12, 15),
            pady=(0, 10),
            sticky="w"
        )

        # Department

        ctk.CTkLabel(
            details,
            text="Department",
            font=self.normal_font,
            text_color=COLORS["primary_hover"],
            anchor="w"
        ).grid(
            row=0,
            column=1,
            padx=(15, 5),
            pady=(10, 2),
            sticky="w"
        )

        ctk.CTkLabel(
            details,
            text=department or "-",
            font=self.normal_bold_font,
            text_color=COLORS["text"],
            anchor="w"
        ).grid(
            row=1,
            column=1,
            padx=(15, 12),
            pady=(0, 10),
            sticky="w"
        )

        # =========================================================
        # CLICK HANDLERS
        # =========================================================

        widgets_to_bind = [
            card,
            header,
            task_label,
            name_label,
            status_label,
            details
        ]

        for child in details.winfo_children():
            widgets_to_bind.append(child)

        for widget in widgets_to_bind:

            widget.bind(
                "<Button-1>",
                lambda event, tid=task_id:
                    self.select_task(tid)
            )

            try:
                widget.configure(
                    cursor="hand2"
                )
            except Exception:
                pass

    # =============================================================
    # SELECT TASK
    # =============================================================

    def select_task(self, task_id):

        self.selected_task_id = task_id

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    t.id,
                    t.task_name,
                    t.task_details,
                    c.name,
                    t.department,
                    t.status,
                    t.created_at

                FROM tasks t

                LEFT JOIN clients c
                    ON t.client_id = c.id

                WHERE
                    t.id = %s
                    AND t.assigned_to = %s
                    AND t.status IN (0, 10)
            """, (
                task_id,
                self.get_user_id()
            ))

            task = cursor.fetchone()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            return

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        if not task:

            self.selected_task_id = None

            self.show_history_message(
                "Select a task from My Pending Tasks to view its history."
            )

            messagebox.showwarning(
                "Task Unavailable",
                (
                    "This task is no longer available. "
                    "It may have been completed or dispatched."
                )
            )

            self.load_tasks()

            return

        (
            task_id,
            task_name,
            task_details,
            client,
            department,
            status,
            created_at
        ) = task

        # =========================================================
        # COMPACT SELECTED TASK INFORMATION
        # =========================================================

        self.selected_label.configure(
            text=(
                f"{task_name or 'Unnamed Task'}\n\n"
                f"Task #{task_id}\n"
                f"Client: {client or '-'}\n"
                f"Department: {department or '-'}\n"
                f"Current Status: {self.status_to_text(status)}\n"
                f"Created: {self.format_datetime_ist(created_at)}"
            ),
            text_color=COLORS["primary"],
            font=self.normal_font,
        )

        self.status_dropdown.set(
            self.status_to_text(status)
        )

        self.description.delete(
            "1.0",
            "end"
        )

        self.update_date_label.configure(
            text=self.format_datetime_ist(
                datetime.now(self.IST)
            )
        )

        self.load_task_history(
            task_id,
            client,
            task_name,
            created_at
        )

    # =============================================================
    # LOAD TASK HISTORY
    #
    # IMPORTANT:
    #
    # task_updates contains the actual work updates.
    #
    # activity_log contains other task events:
    #
    # TASK_CREATED
    # STATUS_CHANGED
    # COMPLETED
    # DISPATCHED
    # BILL_RAISED
    # PAYMENT_RECEIVED
    #
    # We intentionally DO NOT display:
    #
    # WORK_STARTED
    # WORK_UPDATE
    #
    # from activity_log because those correspond to the same
    # work update that is already present in task_updates.
    #
    # This eliminates duplicate "In Progress work update" entries.
    # =============================================================

    def load_task_history(
        self,
        task_id,
        client_name=None,
        task_name=None,
        created_at=None
    ):

        for widget in self.history_scroll.winfo_children():
            widget.destroy()

        self.history_task_label.configure(
            text=f"Task #{task_id}",
            text_color=COLORS["primary_hover"],
            font=self.heading_font
        )

        conn = None
        cursor = None

        history = []

        try:

            conn = get_connection()
            cursor = conn.cursor()

            # =====================================================
            # WORK UPDATES
            #
            # One history item for each task_updates row.
            # =====================================================

            cursor.execute("""
                SELECT
                    tu.id,
                    tu.update_date,
                    tu.description,
                    u.username

                FROM task_updates tu

                LEFT JOIN users u
                    ON tu.updated_by = u.id

                WHERE
                    tu.task_id = %s

                ORDER BY
                    tu.update_date DESC,
                    tu.id DESC
            """, (
                task_id,
            ))

            task_updates = cursor.fetchall()

            for (
                update_id,
                update_date,
                description,
                username
            ) in task_updates:

                history.append({
                    "id": f"update_{update_id}",
                    "event_date": update_date,
                    "event_type": "WORK_UPDATE",
                    "description": description,
                    "username": username
                })

            # =====================================================
            # ACTIVITY LOG
            #
            # Exclude WORK_STARTED and WORK_UPDATE because the
            # corresponding task_updates row is already displayed.
            # =====================================================

            cursor.execute("""
                SELECT
                    al.id,
                    al.action_type,
                    al.performed_by,
                    al.action_date,
                    al.amount,
                    al.payment_mode,
                    al.description,
                    u.username

                FROM activity_log al

                LEFT JOIN users u
                    ON al.performed_by = u.id

                WHERE
                    al.task_id = %s

                    AND al.action_type NOT IN (
                        'WORK_STARTED',
                        'WORK_UPDATE'
                    )

                ORDER BY
                    al.action_date DESC,
                    al.id DESC
            """, (
                task_id,
            ))

            activity_rows = cursor.fetchall()

            task_created_exists = False

            for (
                activity_id,
                action_type,
                performed_by,
                action_date,
                amount,
                payment_mode,
                activity_description,
                username
            ) in activity_rows:

                if action_type == "TASK_CREATED":
                    task_created_exists = True

                history.append({
                    "id": f"activity_{activity_id}",
                    "event_date": action_date,
                    "event_type": action_type,
                    "description": activity_description,
                    "username": username,
                    "amount": amount,
                    "payment_mode": payment_mode
                })

            # =====================================================
            # FALLBACK TASK CREATION EVENT
            #
            # If your inward-entry code did not create a
            # TASK_CREATED activity_log row, we still show task
            # creation using tasks.created_at.
            #
            # If TASK_CREATED already exists, we do NOT add this.
            #
            # Therefore there can only be ONE task-created event.
            # =====================================================

            if not task_created_exists and created_at:

                history.append({
                    "id": "task_creation",
                    "event_date": created_at,
                    "event_type": "TASK_CREATED",
                    "description": (
                        f"Task created"
                        + (
                            f" for client {client_name}"
                            if client_name
                            else ""
                        )
                    ),
                    "username": None,
                    "amount": None,
                    "payment_mode": None
                })

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            return

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        # =========================================================
        # SORT ALL EVENTS
        #
        # Newest first.
        # =========================================================

        history.sort(
            key=lambda item: (
                item.get("event_date") or datetime.min.replace(
                    tzinfo=timezone.utc
                )
            ),
            reverse=True
        )

        # =========================================================
        # NO HISTORY
        # =========================================================

        if not history:

            self.show_history_message(
                "No history has been recorded for this task yet."
            )

            return

        # =========================================================
        # DISPLAY HISTORY
        # =========================================================

        for event in history:

            self.create_history_item(
                event
            )

    # =============================================================
    # HISTORY EVENT TITLE
    # =============================================================

    @staticmethod
    def history_event_title(event_type):

        titles = {

            "TASK_CREATED":
                "Task Created",

            "STATUS_CHANGED":
                "Status Changed",

            "COMPLETED":
                "Task Completed",

            "DISPATCHED":
                "Task Dispatched",

            "BILL_RAISED":
                "Bill Raised",

            "PAYMENT_RECEIVED":
                "Payment Received",

            "DOCUMENT_RECEIVED":
                "Document Received",

            "TASK_UPDATED":
                "Task Updated",

            "WORK_UPDATE":
                "Work Update",

            "WORK_STARTED":
                "Work Started"
        }

        return titles.get(
            event_type,
            event_type.replace(
                "_",
                " "
            ).title()
        )

    # =============================================================
    # CREATE HISTORY ITEM
    # =============================================================

    def create_history_item(
        self,
        event
    ):

        event_type = event.get(
            "event_type"
        )

        event_date = event.get(
            "event_date"
        )

        description = event.get(
            "description"
        )

        username = event.get(
            "username"
        )

        amount = event.get(
            "amount"
        )

        payment_mode = event.get(
            "payment_mode"
        )

        item = ctk.CTkFrame(
            self.history_scroll,
            fg_color=COLORS["card_alt"],
            corner_radius=SIZES["corner_radius"]
        )

        item.pack(
            fill="x",
            padx=5,
            pady=5
        )

        item.grid_columnconfigure(
            0,
            weight=1
        )

        item.grid_columnconfigure(
            1,
            weight=1
        )

        # =========================================================
        # EVENT TITLE
        # =========================================================

        title = self.history_event_title(
            event_type
        )

        title_label = ctk.CTkLabel(
            item,
            text=title,
            font=self.normal_bold_font,
            text_color=COLORS["primary"],
            anchor="w"
        )

        title_label.grid(
            row=0,
            column=0,
            padx=(12, 15),
            pady=(12, 5),
            sticky="nw"
        )

        # =========================================================
        # DATE
        # =========================================================

        date_label = ctk.CTkLabel(
            item,
            text=self.format_datetime_ist(
                event_date
            ),
            font=self.normal_bold_font,
            text_color=COLORS["primary"],
            anchor="e"
        )

        date_label.grid(
            row=0,
            column=1,
            padx=(15, 12),
            pady=(12, 5),
            sticky="ne"
        )

        # =========================================================
        # PERFORMED BY
        # =========================================================

        if username:

            updated_by_label = ctk.CTkLabel(
                item,
                text=f"By: {username}",
                font=self.small_font,
                text_color=COLORS["text_secondary"],
                anchor="w"
            )

            updated_by_label.grid(
                row=1,
                column=0,
                columnspan=2,
                padx=12,
                pady=(0, 5),
                sticky="w"
            )

        # =========================================================
        # DESCRIPTION
        # =========================================================

        display_description = (
            description
            if description
            else ""
        )

        # ---------------------------------------------------------
        # PAYMENT DETAILS
        # ---------------------------------------------------------

        if amount is not None:

            payment_text = (
                f"Amount: {amount}"
            )

            if payment_mode:

                payment_text += (
                    f"    |    Mode: {payment_mode}"
                )

            if display_description:

                display_description = (
                    payment_text
                    + "\n"
                    + display_description
                )

            else:

                display_description = payment_text

        # ---------------------------------------------------------
        # DEFAULT DESCRIPTION FOR STATUS EVENTS
        # ---------------------------------------------------------

        if not display_description:

            if event_type == "TASK_CREATED":

                display_description = (
                    "Task was created."
                )

            elif event_type == "STATUS_CHANGED":

                display_description = (
                    "Task status was changed."
                )

            elif event_type == "COMPLETED":

                display_description = (
                    "Task was marked as completed."
                )

            elif event_type == "DISPATCHED":

                display_description = (
                    "Task was dispatched."
                )

            elif event_type == "BILL_RAISED":

                display_description = (
                    "Bill was raised for this task."
                )

            elif event_type == "PAYMENT_RECEIVED":

                display_description = (
                    "Payment was received for this task."
                )

            elif event_type == "DOCUMENT_RECEIVED":

                display_description = (
                    "A document was received for this task."
                )

            else:

                display_description = "-"

        description_label = ctk.CTkLabel(
            item,
            text=display_description,
            font=self.normal_font,
            text_color=COLORS["text"],
            anchor="w",
            justify="left",
            wraplength=900
        )

        description_label.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=12,
            pady=(3, 12),
            sticky="w"
        )

    # =============================================================
    # SHOW HISTORY MESSAGE
    # =============================================================

    def show_history_message(self, text):

        for widget in self.history_scroll.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.history_scroll,
            text=text,
            font=self.normal_font,
            text_color=COLORS["text_secondary"],
            wraplength=800,
            justify="center"
        ).pack(
            padx=20,
            pady=25
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

    # =============================================================
    # STATUS VALUE
    # =============================================================

    @staticmethod
    def status_to_value(status_text):

        if status_text == "Not Started":
            return 0

        if status_text == "In Progress":
            return 10

        return None

    # =============================================================
    # SAVE UPDATE
    # =============================================================

    def save_update(self):

        # =========================================================
        # TASK SELECTION
        # =========================================================

        if self.selected_task_id is None:

            messagebox.showwarning(
                "Select Task",
                "Please select a task first."
            )

            return

        # =========================================================
        # DESCRIPTION
        # =========================================================

        description = self.description.get(
            "1.0",
            "end"
        ).strip()

        if not description:

            messagebox.showwarning(
                "Update Required",
                "Please describe what you did today."
            )

            return

        # =========================================================
        # STATUS
        # =========================================================

        status_text = self.status_dropdown.get()

        new_status = self.status_to_value(
            status_text
        )

        if new_status is None:

            messagebox.showerror(
                "Invalid Status",
                "Please select a valid task status."
            )

            return

        # =========================================================
        # USER
        # =========================================================

        user_id = self.get_user_id()

        if user_id is None:

            messagebox.showerror(
                "Error",
                "Unable to identify the logged-in user."
            )

            return

        # =========================================================
        # CURRENT UTC TIME
        #
        # PostgreSQL TIMESTAMPTZ will store this correctly.
        # =========================================================

        now = datetime.now(
            timezone.utc
        )

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            # =====================================================
            # VERIFY TASK
            # =====================================================

            cursor.execute("""
                SELECT
                    assigned_to,
                    status,
                    task_name

                FROM tasks

                WHERE
                    id = %s
            """, (
                self.selected_task_id,
            ))

            row = cursor.fetchone()

            if not row:

                messagebox.showerror(
                    "Error",
                    "Task no longer exists."
                )

                return

            (
                assigned_to,
                current_status,
                task_name
            ) = row

            # =====================================================
            # OWNERSHIP
            # =====================================================

            if assigned_to != user_id:

                messagebox.showerror(
                    "Access Denied",
                    "This task is not assigned to you."
                )

                return

            # =====================================================
            # COMPLETED / DISPATCHED
            # =====================================================

            if current_status in (1, 2):

                messagebox.showwarning(
                    "Task Unavailable",
                    (
                        "This task has already been completed "
                        "or dispatched."
                    )
                )

                self.load_tasks()

                return

            # =====================================================
            # SAVE WORK HISTORY
            #
            # IMPORTANT:
            #
            # task_updates.task_id
            #
            # NOT record_id.
            # =====================================================

            cursor.execute("""
                INSERT INTO task_updates
                (
                    task_id,
                    updated_by,
                    update_date,
                    description
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (
                self.selected_task_id,
                user_id,
                now,
                description
            ))

            update_id = cursor.fetchone()[0]

            # =====================================================
            # UPDATE STATUS
            # =====================================================

            cursor.execute("""
                UPDATE tasks

                SET
                    status = %s

                WHERE
                    id = %s
                    AND assigned_to = %s
                    AND status IN (0, 10)
            """, (
                new_status,
                self.selected_task_id,
                user_id
            ))

            if cursor.rowcount == 0:

                conn.rollback()

                messagebox.showwarning(
                    "Task Changed",
                    (
                        "The task status changed before the "
                        "update could be saved."
                    )
                )

                self.load_tasks()

                return

            # =====================================================
            # ACTIVITY LOG
            #
            # This is retained for audit purposes.
            #
            # HOWEVER:
            #
            # load_task_history() deliberately does NOT display
            # WORK_STARTED / WORK_UPDATE activity entries because
            # task_updates already represents this event.
            # =====================================================

            if (
                current_status != new_status
            ):

                action_type = "STATUS_CHANGED"

            else:

                action_type = "WORK_UPDATE"

            cursor.execute("""
                INSERT INTO activity_log
                (
                    task_id,
                    action_type,
                    performed_by,
                    action_date,
                    description
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                self.selected_task_id,
                action_type,
                user_id,
                now,
                description
            ))

            # =====================================================
            # COMMIT
            # =====================================================

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Task update saved successfully."
            )

            # =====================================================
            # SAVE ID FOR HISTORY
            # =====================================================

            saved_task_id = self.selected_task_id

            # =====================================================
            # RESET DESCRIPTION
            # =====================================================

            self.description.delete(
                "1.0",
                "end"
            )

            self.selected_task_id = None

            self.selected_label.configure(
                text="Select a task from the list.",
                text_color=COLORS["primary_hover"]
            )

            self.status_dropdown.set(
                "In Progress"
            )

            # =====================================================
            # UPDATE DISPLAY TIME
            # =====================================================

            self.update_date_label.configure(
                text=self.format_datetime_ist(
                    datetime.now(self.IST)
                )
            )

            # =====================================================
            # HISTORY
            #
            # Reload from database so the complete history is shown.
            # =====================================================

            self.history_task_label.configure(
                text=f"Task #{saved_task_id}",
                text_color=COLORS["primary_hover"],
                font=self.heading_font
            )

            self.load_task_history(
                saved_task_id
            )

            # =====================================================
            # REFRESH TASK LIST / FILTERS
            # =====================================================

            self.load_filter_values()
            self.load_tasks()

        except Exception as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()