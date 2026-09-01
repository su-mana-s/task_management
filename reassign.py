import customtkinter as ctk
import psycopg

from tkinter import messagebox

from database import get_connection
from theme import *
from searchable_combobox import SearchableComboBox


class AdminReassignWork(ctk.CTkFrame):

    def __init__(self, master, user):

        super().__init__(
            master,
            fg_color=COLORS["background"]
        )

        self.user = user
        self.case_map = {}
        self.employee_map = {}

        # =====================================================
        # FONTS
        # =====================================================

        self.title_font = ctk.CTkFont(
            size=SIZES["title_size"],
            weight="bold"
        )

        self.heading_font = ctk.CTkFont(
            size=SIZES["heading_size"],
            weight="bold"
        )

        self.label_font = ctk.CTkFont(
            size=SIZES["label_size"],
            weight="bold"
        )

        self.normal_font = ctk.CTkFont(
            size=SIZES["normal_size"],
            weight="normal"
        )

        self.bold_font = ctk.CTkFont(
            size=SIZES["normal_size"],
            weight="bold"
        )

        # =====================================================
        # LAYOUT
        # =====================================================

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        # =====================================================
        # TITLE
        # =====================================================

        self.title_label = ctk.CTkLabel(
            self,
            text="Admin - Reassign Work",
            font=self.title_font,
            text_color=COLORS["text"]
        )

        self.title_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=(5, 20),
            sticky="w"
        )

        # =====================================================
        # MAIN FRAME
        # =====================================================

        self.form_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS["card"],
            corner_radius=SIZES["large_corner_radius"],
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["primary_hover"]
        )

        self.form_frame.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 20),
            sticky="nsew"
        )

        self.form_frame.grid_columnconfigure(
            0,
            minsize=230
        )

        self.form_frame.grid_columnconfigure(
            1,
            weight=1
        )

        # =====================================================
        # SELECT WORK
        # =====================================================

        self.create_label(
            "Select Work:",
            0
        )

        self.case_var = ctk.StringVar()

        self.case_dropdown = SearchableComboBox(
            self.form_frame,

            variable=self.case_var,

            width=650,
            height=SIZES["entry_height"],

            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),

            dropdown_font=ctk.CTkFont(
                size=SIZES["normal_size"]
            ),

            fg_color=COLORS["input"],
            border_color=COLORS["border"],

            button_color=SIDEBAR_HOVER,
            button_hover_color=COLORS["primary_hover"],

            text_color=COLORS["text"],

            dropdown_fg_color=COLORS["card"],
            dropdown_text_color=COLORS["text"],
            dropdown_hover_color=SIDEBAR_HOVER,

            command=self.load_selected_record
        )

        self.case_dropdown.grid(
            row=0,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # WORK INFORMATION
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="WORK INFORMATION",
            font=self.heading_font,
            text_color=COLORS["primary"]
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            padx=PADDING["x"],
            pady=(30, 15),
            sticky="w"
        )

        # -----------------------------------------------------
        # TASK NAME
        # -----------------------------------------------------

        self.create_label(
            "Task Name:",
            2
        )

        self.task_name_label = ctk.CTkLabel(
            self.form_frame,
            text="-",
            font=self.bold_font,
            text_color=COLORS["text"],
            wraplength=700,
            justify="left"
        )

        self.task_name_label.grid(
            row=2,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # -----------------------------------------------------
        # CLIENT
        # -----------------------------------------------------

        self.create_label(
            "Client:",
            3
        )

        self.client_label = ctk.CTkLabel(
            self.form_frame,
            text="-",
            font=self.bold_font,
            text_color=COLORS["text"]
        )

        self.client_label.grid(
            row=3,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # -----------------------------------------------------
        # DEPARTMENT
        # -----------------------------------------------------

        self.create_label(
            "Department:",
            4
        )

        self.department_label = ctk.CTkLabel(
            self.form_frame,
            text="-",
            font=self.bold_font,
            text_color=COLORS["primary_hover"]
        )

        self.department_label.grid(
            row=4,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # -----------------------------------------------------
        # TASK DETAILS
        # -----------------------------------------------------

        self.create_label(
            "Work Details:",
            5
        )

        self.task_details_label = ctk.CTkLabel(
            self.form_frame,
            text="-",
            font=self.normal_font,
            text_color=COLORS["text"],
            wraplength=700,
            justify="left"
        )

        self.task_details_label.grid(
            row=5,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        self.create_label(
            "Status:",
            6
        )

        self.status_label = ctk.CTkLabel(
            self.form_frame,
            text="-",
            font=self.bold_font,
            text_color=COLORS["primary_hover"]
        )

        self.status_label.grid(
            row=6,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # CURRENT ASSIGNMENT
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="CURRENT ASSIGNMENT",
            font=self.heading_font,
            text_color=COLORS["primary"]
        ).grid(
            row=7,
            column=0,
            columnspan=2,
            padx=PADDING["x"],
            pady=(35, 15),
            sticky="w"
        )

        self.create_label(
            "Currently Assigned To:",
            8
        )

        self.current_employee_label = ctk.CTkLabel(
            self.form_frame,
            text="-",
            font=self.bold_font,
            text_color=COLORS["warning"]
        )

        self.current_employee_label.grid(
            row=8,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # REASSIGN
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="REASSIGN WORK",
            font=self.heading_font,
            text_color=COLORS["primary"]
        ).grid(
            row=9,
            column=0,
            columnspan=2,
            padx=PADDING["x"],
            pady=(35, 15),
            sticky="w"
        )

        self.create_label(
            "Assign To:",
            10
        )

        self.employee_var = ctk.StringVar()

        self.employee_dropdown = ctk.CTkComboBox(
            self.form_frame,

            variable=self.employee_var,

            width=350,
            height=SIZES["entry_height"],

            font=self.normal_font,
            dropdown_font=self.normal_font,

            fg_color=COLORS["input"],
            border_color=COLORS["border"],

            button_color=SIDEBAR_HOVER,
            button_hover_color=COLORS["primary_hover"],

            text_color=COLORS["text"],

            dropdown_fg_color=COLORS["card"],
            dropdown_text_color=COLORS["text"],
            dropdown_hover_color=SIDEBAR_HOVER
        )

        self.employee_dropdown.grid(
            row=10,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # REASSIGN BUTTON
        # =====================================================

        self.reassign_btn = ctk.CTkButton(
            self.form_frame,

            text="Reassign Work",

            command=self.reassign_work,

            width=SIZES["button_width"],
            height=SIZES["button_height"],

            corner_radius=SIZES["corner_radius"],

            fg_color=LOGOUT,
            hover_color=LOGOUT_HOVER,

            text_color=TEXT_LIGHT,

            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            )
        )

        self.reassign_btn.grid(
            row=11,
            column=1,
            padx=PADDING["x"],
            pady=(25, 30),
            sticky="w"
        )

        # =====================================================
        # NOTE
        # =====================================================

        self.note_label = ctk.CTkLabel(
            self.form_frame,
            text=(
                "Reassignment changes only the employee responsible "
                "for the work. The original task, client, department "
                "and work details remain unchanged."
            ),
            font=self.normal_font,
            text_color=COLORS["text_secondary"],
            wraplength=750,
            justify="left"
        )

        self.note_label.grid(
            row=12,
            column=0,
            columnspan=2,
            padx=PADDING["x"],
            pady=(5, 30),
            sticky="w"
        )

        # =====================================================
        # LOAD EMPLOYEES
        # =====================================================

        self.load_employees()

        # =====================================================
        # LOAD WORK
        # =====================================================

        self.load_records()

    # =========================================================
    # LABEL HELPER
    # =========================================================

    def create_label(
        self,
        text,
        row
    ):

        label = ctk.CTkLabel(
            self.form_frame,
            text=text,
            font=self.label_font,
            text_color=COLORS["text"]
        )

        label.grid(
            row=row,
            column=0,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        return label

    # =========================================================
    # EMPLOYEES
    # =========================================================

    def load_employees(self):

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id,
                    username
                FROM users
                WHERE
                    is_active = TRUE
                    AND role IN ('Employee', 'Admin')
                ORDER BY username
            """)

            employees = cursor.fetchall()

        except psycopg.Error as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load employees:\n{e}"
            )

            return

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        self.employee_map = {
            username: employee_id
            for employee_id, username in employees
        }

        names = [
            username
            for employee_id, username in employees
        ]

        if names:

            self.employee_dropdown.configure(
                values=names
            )

            self.employee_dropdown.set(
                names[0]
            )

        else:

            self.employee_dropdown.configure(
                values=["No employees found"]
            )

            self.employee_dropdown.set(
                "No employees found"
            )

    # =========================================================
    # LOAD WORK RECORDS
    # =========================================================

    def load_records(self):

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    t.id,
                    c.name,
                    t.task_name,
                    t.department,
                    t.task_details,
                    t.assigned_to,
                    u.username
                FROM tasks t

                LEFT JOIN clients c
                    ON t.client_id = c.id

                LEFT JOIN users u
                    ON t.assigned_to = u.id

                WHERE t.status IN (0, 10)

                ORDER BY t.id DESC
            """)

            records = cursor.fetchall()

        except psycopg.Error as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load work:\n{e}"
            )

            return

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        self.case_map = {}

        display_values = []

        for record in records:

            (
                task_id,
                client_name,
                task_name,
                department,
                task_details,
                assigned_to,
                assigned_name
            ) = record

            display = (
                f"ID: {task_id} | "
                f"{client_name or '-'} | "
                f"{task_name or '-'} | "
                f"{department or '-'} | "
                f"Currently Assigned: "
                f"{assigned_name or 'Unassigned'}"
            )

            self.case_map[display] = task_id
            display_values.append(display)

        if display_values:

            self.case_dropdown.configure_values(
                values=display_values
            )

            self.case_dropdown.set(
                display_values[0]
            )

            self.load_selected_record(
                display_values[0]
            )

        else:

            self.case_dropdown.configure_values(
                values=["No work in progress"]
            )

            self.case_dropdown.set(
                "No work in progress"
            )

            self.clear_information()

    # =========================================================
    # LOAD SELECTED WORK
    # =========================================================

    def load_selected_record(
        self,
        choice=None
    ):

        if choice is None:

            choice = self.case_var.get()

        task_id = self.case_map.get(
            choice
        )

        if not task_id:

            return

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    c.name,
                    t.task_name,
                    t.department,
                    t.task_details,
                    t.status,
                    t.assigned_to,
                    u.username
                FROM tasks t

                LEFT JOIN clients c
                    ON t.client_id = c.id

                LEFT JOIN users u
                    ON t.assigned_to = u.id

                WHERE t.id = %s
            """, (
                task_id,
            ))

            record = cursor.fetchone()

        except psycopg.Error as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load work:\n{e}"
            )

            return

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        if not record:

            return

        (
            client_name,
            task_name,
            department,
            task_details,
            status,
            assigned_to,
            assigned_name
        ) = record

        # =====================================================
        # STATUS TEXT
        # =====================================================

        if status == 0:

            status_text = "NOT STARTED"

        elif status == 1:

            status_text = "WORK COMPLETED - NOT DISPATCHED"

        elif status == 2:

            status_text = "DISPATCHED"

        elif status == 10:

            status_text = "IN PROGRESS"

        else:

            status_text = str(status)

        # =====================================================
        # DISPLAY
        # =====================================================

        self.task_name_label.configure(
            text=task_name or "-"
        )

        self.client_label.configure(
            text=client_name or "-"
        )

        self.department_label.configure(
            text=department or "-"
        )

        self.task_details_label.configure(
            text=task_details or "-"
        )

        self.status_label.configure(
            text=status_text
        )

        self.current_employee_label.configure(
            text=assigned_name or "Unassigned"
        )

        # =====================================================
        # SET DROPDOWN TO CURRENT EMPLOYEE
        # =====================================================

        if (
            assigned_name
            and assigned_name in self.employee_map
        ):

            self.employee_dropdown.set(
                assigned_name
            )

        else:

            employee_names = list(
                self.employee_map.keys()
            )

            if employee_names:

                self.employee_dropdown.set(
                    employee_names[0]
                )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear_information(self):

        self.task_name_label.configure(
            text="-"
        )

        self.client_label.configure(
            text="-"
        )

        self.department_label.configure(
            text="-"
        )

        self.task_details_label.configure(
            text="-"
        )

        self.status_label.configure(
            text="-"
        )

        self.current_employee_label.configure(
            text="-"
        )

    # =========================================================
    # REASSIGN
    # =========================================================

    def reassign_work(self):

        selected = self.case_var.get()

        task_id = self.case_map.get(
            selected
        )

        if not task_id:

            messagebox.showerror(
                "Error",
                "Please select a valid work record."
            )

            return

        new_employee = self.employee_var.get()

        new_employee_id = self.employee_map.get(
            new_employee
        )

        if not new_employee_id:

            messagebox.showerror(
                "Error",
                "Please select a valid employee."
            )

            return

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            # =================================================
            # VERIFY WORK IS STILL NOT STARTED
            # =================================================

            cursor.execute("""
                SELECT
                    assigned_to,
                    status,
                    task_name
                FROM tasks
                WHERE id = %s
            """, (
                task_id,
            ))

            record = cursor.fetchone()

            if not record:

                messagebox.showerror(
                    "Error",
                    "Work record not found."
                )

                return

            (
                old_assigned_to,
                status,
                task_name
            ) = record

            # =================================================
            # ONLY STATUS 0 CAN BE REASSIGNED
            # =================================================

            if status in (1, 2):

                messagebox.showerror(
                    "Not Allowed",
                    (
                        "This work can no longer be reassigned.\n\n"
                        "Only work that is currently not started or in progress "
                        "can be reassigned."
                    )
                )

                return

            # =================================================
            # UPDATE ASSIGNMENT
            # =================================================

            cursor.execute("""
                UPDATE tasks
                SET assigned_to = %s
                WHERE id = %s
                  AND status IN (0, 10)
            """, (
                new_employee_id,
                task_id
            ))

            if cursor.rowcount != 1:

                conn.rollback()

                messagebox.showerror(
                    "Error",
                    "The work could not be reassigned."
                )

                return

            # =================================================
            # AUDIT LOG
            # =================================================

            cursor.execute("""
                INSERT INTO activity_log (
                    task_id,
                    action_type,
                    performed_by,
                    description
                )
                VALUES (
                    %s,
                    'WORK_REASSIGNED',
                    %s,
                    %s
                )
            """, (
                task_id,
                self.user["id"],
                f"Work reassigned to {new_employee}"
            ))

            conn.commit()

        except psycopg.Error as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            return

        except Exception as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Error",
                str(e)
            )

            return

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        messagebox.showinfo(
            "Success",
            (
                f"Work ID {task_id}"
                f" ({task_name or 'Unnamed Task'}) "
                f"has been reassigned to "
                f"{new_employee}."
            )
        )

        self.load_records()