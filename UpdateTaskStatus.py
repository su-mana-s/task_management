import customtkinter as ctk
import sqlite3

from datetime import date, datetime

from tkinter import messagebox

from database import DB_NAME
from theme import *


class UpdateTaskStatus(ctk.CTkFrame):

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
        # TITLE
        # =========================================================

        ctk.CTkLabel(
            self,
            text="Update Task Status",
            font=self.title_font,
            text_color=COLORS["text"]
        ).pack(
            pady=(0, 5),
            padx=5,
            anchor="w"
        )

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
        ).pack(
            padx=5,
            pady=(0, 15),
            anchor="w"
        )

        # =========================================================
        # MAIN AREA
        # =========================================================

        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        self.main_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.main_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.main_frame.grid_rowconfigure(
            0,
            weight=1
        )

        # =========================================================
        # LEFT - TASK LIST
        # =========================================================

        self.task_card = ctk.CTkFrame(
            self.main_frame,
            fg_color=COLORS["toggle"],
            corner_radius=SIZES["large_corner_radius"]
        )

        self.task_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        # =========================================================
        # TASK LIST HEADER
        # =========================================================

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

        self.client_filter = ctk.CTkEntry(
            self.filter_frame,
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

        self.department_filter = ctk.CTkEntry(
            self.filter_frame,
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
        # RIGHT - UPDATE CARD
        # =========================================================

        self.update_card = ctk.CTkFrame(
            self.main_frame,
            fg_color=COLORS["toggle"],
            corner_radius=SIZES["large_corner_radius"]
        )

        self.update_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )

        ctk.CTkLabel(
            self.update_card,
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
            self.update_card,
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
            self.update_card,
            text="Current / New Status",
            font=self.normal_bold_font,
            text_color=COLORS["text"]
        ).pack(
            padx=20,
            pady=(5, 5),
            anchor="w"
        )

        self.status_dropdown = ctk.CTkComboBox(
            self.update_card,
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
            self.update_card,
            text="Update Date",
            font=self.normal_bold_font,
            text_color=COLORS["text"]
        ).pack(
            padx=20,
            pady=(5, 5),
            anchor="w"
        )

        # Display DD-MM-YYYY to user.
        # Database continues to use YYYY-MM-DD.

        self.update_date_label = ctk.CTkLabel(
            self.update_card,
            text=self.format_date_display(
                date.today().isoformat()
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
            self.update_card,
            text="What did you do today?",
            font=self.normal_bold_font,
            text_color=COLORS["text"]
        ).pack(
            padx=20,
            pady=(5, 5),
            anchor="w"
        )

        self.description = ctk.CTkTextbox(
            self.update_card,
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
        # SAVE
        # =========================================================

        self.save_button = ctk.CTkButton(
            self.update_card,
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
        # STATE
        # =========================================================

        self.selected_task_id = None

        # =========================================================
        # LOAD TASKS
        # =========================================================

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
    #
    # Database:
    #     YYYY-MM-DD
    #
    # Display:
    #     DD-MM-YYYY
    # =============================================================

    @staticmethod
    def format_date_display(value):

        if not value:
            return "-"

        try:

            return datetime.strptime(
                str(value),
                "%Y-%m-%d"
            ).strftime(
                "%d-%m-%Y"
            )

        except ValueError:

            return str(value)

    # =============================================================
    # CLEAR FILTERS
    # =============================================================

    def clear_filters(self):

        self.client_filter.delete(
            0,
            "end"
        )

        self.department_filter.delete(
            0,
            "end"
        )

        self.load_tasks()

    # =============================================================
    # LOAD TASKS
    #
    # ONLY:
    #
    # 0  = Not Started
    # 10 = In Progress
    #
    # Completed and Dispatched tasks are not shown.
    # =============================================================

    def load_tasks(self):

        # ---------------------------------------------------------
        # Clear current cards
        # ---------------------------------------------------------

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

        # ---------------------------------------------------------
        # Filters
        # ---------------------------------------------------------

        client_filter = (
            self.client_filter.get().strip()
        )

        department_filter = (
            self.department_filter.get().strip()
        )

        # ---------------------------------------------------------
        # Database
        # ---------------------------------------------------------

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            query = """
                SELECT
                    r.inward_id,
                    c.name,
                    c.mobile,
                    r.department,
                    r.nature_of_papers,
                    r.miscellaneous_details,
                    r.date_of_entry,
                    r.date_of_receipt,
                    r.status

                FROM records r

                LEFT JOIN clients c
                    ON r.client_id = c.id

                WHERE
                    r.assigned_to = ?

                    AND r.status IN (0, 10)
            """

            params = [
                user_id
            ]

            # -----------------------------------------------------
            # CLIENT FILTER
            # -----------------------------------------------------

            if client_filter:

                query += """
                    AND c.name LIKE ?
                """

                params.append(
                    f"%{client_filter}%"
                )

            # -----------------------------------------------------
            # DEPARTMENT FILTER
            # -----------------------------------------------------

            if department_filter:

                query += """
                    AND r.department LIKE ?
                """

                params.append(
                    f"%{department_filter}%"
                )

            # -----------------------------------------------------
            # ORDER
            # -----------------------------------------------------

            query += """
                ORDER BY
                    CASE
                        WHEN r.status = 10 THEN 0
                        ELSE 1
                    END,
                    r.inward_id DESC
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

            conn.close()

        # =========================================================
        # NO TASKS
        # =========================================================

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

        # =========================================================
        # CREATE CARDS
        # =========================================================

        for task in tasks:

            self.create_task_card(task)

    # =============================================================
    # CREATE TASK CARD
    #
    # Layout:
    #
    # ROW 1:
    #     TASK # + CLIENT                  STATUS
    #
    # ROW 2:
    #     DEPARTMENT                       NATURE OF PAPERS
    #
    # Clicking anywhere on the card selects the task.
    # =============================================================

    def create_task_card(self, task):

        (
            task_id,
            client,
            mobile,
            department,
            papers,
            miscellaneous,
            entry_date,
            receipt_date,
            status
        ) = task

        status_text = self.status_to_text(
            status
        )

        # =========================================================
        # CARD
        # =========================================================

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
        # CARD HEADER - ROW 1
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

        # ---------------------------------------------------------
        # TASK NUMBER
        # ---------------------------------------------------------

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

        # ---------------------------------------------------------
        # CLIENT
        # ---------------------------------------------------------

        client_label = ctk.CTkLabel(
            header,
            text=client or "No Client",
            font=self.normal_bold_font,
            text_color=COLORS["primary"],
            anchor="w"
        )

        client_label.grid(
            row=0,
            column=1,
            sticky="w"
        )

        # ---------------------------------------------------------
        # STATUS - TOP RIGHT
        # ---------------------------------------------------------

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
        # ROW 2
        # DEPARTMENT + PAPERS
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

        details.grid_columnconfigure(
            3,
            weight=2
        )

        # ---------------------------------------------------------
        # DEPARTMENT LABEL
        # ---------------------------------------------------------

        ctk.CTkLabel(
            details,
            text="Department",
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

        # ---------------------------------------------------------
        # DEPARTMENT VALUE
        # ---------------------------------------------------------

        ctk.CTkLabel(
            details,
            text=department or "-",
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

        # ---------------------------------------------------------
        # PAPERS LABEL
        # ---------------------------------------------------------

        ctk.CTkLabel(
            details,
            text="Nature of Papers",
            font=self.normal_font,
            text_color=COLORS["primary_hover"],
            anchor="w"
        ).grid(
            row=0,
            column=2,
            padx=(15, 5),
            pady=(10, 2),
            sticky="w"
        )

        # ---------------------------------------------------------
        # PAPERS VALUE
        # ---------------------------------------------------------

        ctk.CTkLabel(
            details,
            text=papers or "-",
            font=self.normal_bold_font,
            text_color=COLORS["text"],
            anchor="w",
            justify="left",
            wraplength=500
        ).grid(
            row=1,
            column=2,
            columnspan=2,
            padx=(15, 12),
            pady=(0, 10),
            sticky="w"
        )

        # =========================================================
        # MAKE THE ENTIRE CARD CLICKABLE
        # =========================================================

        widgets_to_bind = [
            card,
            header,
            task_label,
            client_label,
            status_label,
            details
        ]

        # Also bind all children of details.

        for child in details.winfo_children():
            widgets_to_bind.append(child)

        for widget in widgets_to_bind:

            widget.bind(
                "<Button-1>",
                lambda event, tid=task_id:
                    self.select_task(tid)
            )

            # Change cursor so it feels clickable.

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

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    r.inward_id,
                    c.name,
                    c.mobile,
                    r.department,
                    r.nature_of_papers,
                    r.miscellaneous_details,
                    r.status

                FROM records r

                LEFT JOIN clients c
                    ON r.client_id = c.id

                WHERE
                    r.inward_id = ?

                    AND r.assigned_to = ?

                    AND r.status IN (0, 10)
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

            conn.close()

        # =========================================================
        # TASK NO LONGER AVAILABLE
        # =========================================================

        if not task:

            self.selected_task_id = None

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
            client,
            mobile,
            department,
            papers,
            miscellaneous,
            status
        ) = task

        # =========================================================
        # DISPLAY SELECTED TASK
        # =========================================================

        self.selected_label.configure(
            text=(
                f"Task #{task_id}\n\n"
                f"Client: {client or '-'}\n"
                f"Mobile: {mobile or '-'}\n"
                f"Department: {department or '-'}\n"
                f"Nature of Papers: {papers or '-'}\n\n"
                f"Current Status: "
                f"{self.status_to_text(status)}"
            ),
            text_color=COLORS["text"]
        )

        # =========================================================
        # SET STATUS
        # =========================================================

        self.status_dropdown.set(
            self.status_to_text(status)
        )

        # =========================================================
        # CLEAR DESCRIPTION
        # =========================================================

        self.description.delete(
            "1.0",
            "end"
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
    #
    # This function NEVER completes the task.
    #
    # Completion is handled exclusively by Work Done.
    # =============================================================

    def save_update(self):

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
        # DATES
        #
        # Database format remains:
        #
        # YYYY-MM-DD
        #
        # Display format is:
        #
        # DD-MM-YYYY
        # =========================================================

        today = date.today().isoformat()

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        conn = None

        try:

            conn = sqlite3.connect(DB_NAME)

            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            # =====================================================
            # VERIFY TASK
            # =====================================================

            cursor.execute("""
                SELECT
                    assigned_to,
                    status

                FROM records

                WHERE inward_id = ?
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

            assigned_to, current_status = row

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
            # =====================================================

            cursor.execute("""
                INSERT INTO task_updates
                (
                    record_id,
                    updated_by,
                    update_date,
                    description
                )
                VALUES (?, ?, ?, ?)
            """, (
                self.selected_task_id,
                user_id,
                today,
                description
            ))

            # =====================================================
            # UPDATE STATUS
            # =====================================================

            cursor.execute("""
                UPDATE records

                SET status = ?

                WHERE
                    inward_id = ?

                    AND assigned_to = ?

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
            # =====================================================

            if new_status == 10:

                action_type = "WORK_STARTED"

            else:

                action_type = "WORK_UPDATE"

            cursor.execute("""
                INSERT INTO activity_log
                (
                    record_id,
                    action_type,
                    performed_by,
                    action_date,
                    description
                )
                VALUES (?, ?, ?, ?, ?)
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
            # RESET FORM
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
            # REFRESH TASK LIST
            # =====================================================

            self.load_tasks()

        except Exception as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            if conn:
                conn.close()