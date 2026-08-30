import customtkinter as ctk
import sqlite3

from tkinter import messagebox

from database import DB_NAME
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

            # font=self.normal_font,
            # dropdown_font=self.normal_font,
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
        # CLIENT
        # -----------------------------------------------------

        self.create_label(
            "Client:",
            2
        )

        self.client_label = ctk.CTkLabel(
            self.form_frame,
            text="-",
            font=self.bold_font,
            text_color=COLORS["text"]
        )

        self.client_label.grid(
            row=2,
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
            3
        )

        self.department_label = ctk.CTkLabel(
            self.form_frame,
            text="-",
            font=self.bold_font,
            text_color=COLORS["primary_hover"]
        )

        self.department_label.grid(
            row=3,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # -----------------------------------------------------
        # NATURE
        # -----------------------------------------------------

        self.create_label(
            "Nature of Work:",
            4
        )

        self.nature_label = ctk.CTkLabel(
            self.form_frame,
            text="-",
            font=self.normal_font,
            text_color=COLORS["text"],
            wraplength=700,
            justify="left"
        )

        self.nature_label.grid(
            row=4,
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
            5
        )

        self.status_label = ctk.CTkLabel(
            self.form_frame,
            text="-",
            font=self.bold_font,
            text_color=COLORS["primary_hover"]
        )

        self.status_label.grid(
            row=5,
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
            row=6,
            column=0,
            columnspan=2,
            padx=PADDING["x"],
            pady=(35, 15),
            sticky="w"
        )

        self.create_label(
            "Currently Assigned To:",
            7
        )

        self.current_employee_label = ctk.CTkLabel(
            self.form_frame,
            text="-",
            font=self.bold_font,
            text_color=COLORS["warning"]
        )

        self.current_employee_label.grid(
            row=7,
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
            row=8,
            column=0,
            columnspan=2,
            padx=PADDING["x"],
            pady=(35, 15),
            sticky="w"
        )

        self.create_label(
            "Assign To:",
            9
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
            row=9,
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
            row=10,
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
                "for the work. The original inward entry, client, "
                "department and work details remain unchanged."
            ),
            font=self.normal_font,
            text_color=COLORS["text_secondary"],
            wraplength=750,
            justify="left"
        )

        self.note_label.grid(
            row=11,
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

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id,
                    username
                FROM users
                WHERE
                    is_active = 1
                    AND role IN ('Employee', 'Admin')
                ORDER BY username
            """)

            employees = cursor.fetchall()

        finally:

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
        conn = sqlite3.connect(DB_NAME)

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    r.inward_id,
                    c.name,
                    r.department,
                    r.nature_of_papers,
                    r.assigned_to,
                    u.username
                FROM records r
                LEFT JOIN clients c
                    ON r.client_id = c.id
                LEFT JOIN users u
                    ON r.assigned_to = u.id
                WHERE r.status = 0
                ORDER BY r.inward_id DESC
            """)

            records = cursor.fetchall()

        finally:
            conn.close()

        self.case_map = {}

        display_values = []

        for record in records:

            (
                record_id,
                client_name,
                department,
                nature,
                assigned_to,
                assigned_name
            ) = record

            display = (
                f"ID: {record_id} | "
                f"{client_name} | "
                f"{department} | "
                f"{nature} | "
                f"Currently Assigned: {assigned_name or 'Unassigned'}"
            )

            self.case_map[display] = record_id
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

            self.current_assignee_label.configure(
                text="-"
            )
    # =========================================================
    # LOAD SELECTED WORK
    # =========================================================

    def load_selected_record(
        self,
        choice=None
    ):

        if choice is None:

            choice = self.case_var.get()

        record_id = self.case_map.get(
            choice
        )

        if not record_id:

            return

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    c.name,
                    r.department,
                    r.nature_of_papers,
                    r.status,
                    r.assigned_to,
                    u.username
                FROM records r

                LEFT JOIN clients c
                    ON r.client_id = c.id

                LEFT JOIN users u
                    ON r.assigned_to = u.id

                WHERE r.inward_id = ?
            """, (
                record_id,
            ))

            record = cursor.fetchone()

        finally:

            conn.close()

        if not record:

            return

        (
            client_name,
            department,
            nature,
            status,
            assigned_to,
            assigned_name
        ) = record

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

        self.client_label.configure(
            text=client_name or "-"
        )

        self.department_label.configure(
            text=department or "-"
        )

        self.nature_label.configure(
            text=nature or "-"
        )

        self.status_label.configure(
            text=status_text
        )

        self.current_employee_label.configure(
            text=assigned_name or "Unassigned"
        )

        # -----------------------------------------------------
        # Set dropdown to current employee
        # -----------------------------------------------------

        if assigned_name and assigned_name in self.employee_map:

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

        self.client_label.configure(
            text="-"
        )

        self.department_label.configure(
            text="-"
        )

        self.nature_label.configure(
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

        record_id = self.case_map.get(selected)

        if not record_id:

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

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            # -----------------------------------------------------
            # VERIFY THAT WORK IS STILL IN PROGRESS
            # -----------------------------------------------------

            cursor.execute("""
                SELECT
                    assigned_to,
                    status
                FROM records
                WHERE inward_id = ?
            """, (record_id,))

            record = cursor.fetchone()

            if not record:

                messagebox.showerror(
                    "Error",
                    "Work record not found."
                )

                return

            old_assigned_to, status = record

            # Only status 0 can be reassigned
            if status != 0:

                messagebox.showerror(
                    "Not Allowed",
                    "This work can no longer be reassigned.\n\n"
                    "Only work that is currently in progress "
                    "can be reassigned."
                )

                return

            # -----------------------------------------------------
            # UPDATE ASSIGNMENT
            # -----------------------------------------------------

            cursor.execute("""
                UPDATE records
                SET assigned_to = ?
                WHERE inward_id = ?
                AND status = 0
            """, (
                new_employee_id,
                record_id
            ))

            if cursor.rowcount != 1:

                conn.rollback()

                messagebox.showerror(
                    "Error",
                    "The work could not be reassigned."
                )

                return

            # -----------------------------------------------------
            # AUDIT LOG
            # -----------------------------------------------------

            cursor.execute("""
                INSERT INTO activity_log (
                    record_id,
                    action_type,
                    performed_by,
                    description
                )
                VALUES (
                    ?,
                    'WORK_REASSIGNED',
                    ?,
                    ?
                )
            """, (
                record_id,
                self.user["id"],
                f"Work reassigned to {new_employee}"
            ))

            conn.commit()

        except Exception as e:

            conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            return

        finally:

            conn.close()

        messagebox.showinfo(
            "Success",
            f"Work ID {record_id} has been reassigned to "
            f"{new_employee}."
        )

        self.load_records()