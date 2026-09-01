import customtkinter as ctk
from searchable_combobox import SearchableComboBox
from database import get_connection
from tkinter import messagebox

from theme import *


class InwardMenu(ctk.CTkFrame):

    def __init__(self, master, user):

        super().__init__(
            master,
            fg_color=COLORS["background"]
        )

        self.user = user

        self.selected_client_id = None
        self.selected_employee_id = None

        # =====================================================
        # PAGE LAYOUT
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
            text="Create New Task",
            font=ctk.CTkFont(
                size=SIZES["title_size"],
                weight="bold"
            ),
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
        # FORM CONTAINER
        # =====================================================

        self.form_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS["card"],
            corner_radius=SIZES["large_corner_radius"]
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

        self.create_form()

    # =========================================================
    # LABEL
    # =========================================================

    def create_label(self, text, row):

        label = ctk.CTkLabel(
            self.form_frame,
            text=text,
            font=ctk.CTkFont(
                size=SIZES["label_size"],
                weight="bold"
            ),
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
    # ENTRY
    # =========================================================

    def create_entry(self, placeholder=""):

        return ctk.CTkEntry(
            self.form_frame,
            width=SIZES["entry_width"],
            height=SIZES["entry_height"],
            placeholder_text=placeholder,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            corner_radius=SIZES["corner_radius"],
            font=ctk.CTkFont(
                size=SIZES["normal_size"]
            )
        )

    # =========================================================
    # DROPDOWN
    # =========================================================

    def create_dropdown(
        self,
        variable,
        values,
        command=None
    ):

        return ctk.CTkComboBox(
            self.form_frame,

            variable=variable,
            values=values,
            command=command,

            width=SIZES["dropdown_width"],
            height=SIZES["entry_height"],

            fg_color=COLORS["input"],
            border_color=COLORS["border"],

            button_color=SIDEBAR_HOVER,
            button_hover_color=COLORS["primary_hover"],

            text_color=COLORS["text"],

            dropdown_fg_color=COLORS["primary_hover"],
            dropdown_hover_color=SIDEBAR_HOVER,
            dropdown_text_color=COLORS["toggle"],

            corner_radius=SIZES["corner_radius"],

            font=ctk.CTkFont(
                size=SIZES["normal_size"]
            )
        )

    # =========================================================
    # FORM
    # =========================================================

    def create_form(self):

        # =====================================================
        # TASK NAME
        # =====================================================

        self.create_label(
            "Task Name:",
            0
        )

        self.task_name_entry = self.create_entry(
            "Enter task name"
        )

        self.task_name_entry.grid(
            row=0,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # TASK DETAILS
        # =====================================================

        self.create_label(
            "Task Details:",
            1
        )

        self.task_details_entry = ctk.CTkEntry(
            self.form_frame,

            width=SIZES["textbox_width"],
            height=SIZES["entry_height"],

            fg_color=COLORS["input"],
            border_color=COLORS["border"],

            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],

            placeholder_text="Enter task details",

            corner_radius=SIZES["corner_radius"],

            font=ctk.CTkFont(
                size=SIZES["normal_size"]
            )
        )

        self.task_details_entry.grid(
            row=1,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # CLIENT
        # =====================================================

        self.create_label(
            "Client Name:",
            2
        )

        self.client_var = ctk.StringVar(
            value=""
        )

        self.clients = self.get_clients()

        client_values = [
            client["display"]
            for client in self.clients
        ]

        if not client_values:
            client_values = [
                "No clients found"
            ]

        self.client_dropdown = SearchableComboBox(
            self.form_frame,

            values=client_values,

            variable=self.client_var,

            command=self.on_client_selected,

            width=SIZES["dropdown_width"],
            height=SIZES["entry_height"],

            font=ctk.CTkFont(
                size=SIZES["normal_size"]
            ),

            fg_color=COLORS["input"],
            border_color=COLORS["border"],

            button_color=SIDEBAR_HOVER,
            button_hover_color=COLORS["primary_hover"],

            text_color=COLORS["text"],

            dropdown_fg_color=COLORS["primary_hover"],
            dropdown_text_color=COLORS["toggle"],
            dropdown_hover_color=SIDEBAR_HOVER,

            corner_radius=SIZES["corner_radius"]
        )

        self.client_dropdown.grid(
            row=2,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # DEPARTMENT
        # =====================================================

        self.create_label(
            "Department:",
            3
        )

        departments = [
            "TDS",
            "GST",
            "IT",
            "ACCOUNTS",
            "PAN",
            "TAN",
            "Miscellaneous"
        ]

        self.dept_var = ctk.StringVar(
            value="TDS"
        )

        self.dept_dropdown = self.create_dropdown(
            self.dept_var,
            departments,
            self.on_dept_change
        )

        self.dept_dropdown.grid(
            row=3,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # MISCELLANEOUS
        # =====================================================

        self.misc_label = ctk.CTkLabel(
            self.form_frame,
            text="Misc Details:",
            font=ctk.CTkFont(
                size=SIZES["label_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        )

        self.misc_entry = self.create_entry(
            "Enter miscellaneous details"
        )

        # =====================================================
        # ASSIGN TO
        # =====================================================

        self.create_label(
            "Assign To:",
            5
        )

        self.employee_var = ctk.StringVar(
            value=""
        )

        self.employees = self.get_employees()

        employee_values = [
            employee["username"]
            for employee in self.employees
        ]

        if not employee_values:
            employee_values = [
                "No employees found"
            ]

        self.assign_dropdown = self.create_dropdown(
            self.employee_var,
            employee_values,
            self.on_employee_selected
        )

        self.assign_dropdown.grid(
            row=5,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # CREATED BY
        # =====================================================

        self.create_label(
            "Created By:",
            6
        )

        self.created_by_label = ctk.CTkLabel(
            self.form_frame,

            text=self.user["username"],

            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),

            text_color=COLORS["text"]
        )

        self.created_by_label.grid(
            row=6,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # STATUS
        # =====================================================

        self.create_label(
            "Initial Status:",
            7
        )

        self.status_label = ctk.CTkLabel(
            self.form_frame,

            text="Not Started",

            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),

            text_color=COLORS["text"]
        )

        self.status_label.grid(
            row=7,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # SUBMIT
        # =====================================================

        self.submit_btn = ctk.CTkButton(
            self.form_frame,

            text="✓  Create Task",

            command=self.create_task,

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

        self.submit_btn.grid(
            row=8,
            column=0,
            columnspan=2,
            padx=PADDING["x"],
            pady=(25, 30)
        )

    # =========================================================
    # CLIENT SELECTED
    # =========================================================

    def on_client_selected(self, selected_value):

        self.selected_client_id = self.client_map.get(
            selected_value
        )

    # =========================================================
    # EMPLOYEE SELECTED
    # =========================================================

    def on_employee_selected(self, selected_value):

        self.selected_employee_id = next(
            (
                employee["id"]
                for employee in self.employees
                if employee["username"] == selected_value
            ),
            None
        )

    # =========================================================
    # DEPARTMENT CHANGE
    # =========================================================

    def on_dept_change(self, choice):

        if choice == "Miscellaneous":

            self.misc_label.grid(
                row=4,
                column=0,
                padx=PADDING["x"],
                pady=PADDING["y"],
                sticky="w"
            )

            self.misc_entry.grid(
                row=4,
                column=1,
                padx=PADDING["x"],
                pady=PADDING["y"],
                sticky="w"
            )

        else:

            self.misc_label.grid_forget()
            self.misc_entry.grid_forget()

    # =========================================================
    # CLIENTS
    # =========================================================

    def get_clients(self):

        conn = get_connection()

        cursor = None

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    id,
                    name,
                    mobile
                FROM clients
                ORDER BY name
            """)

            clients = cursor.fetchall()

            self.client_map = {}

            result = []

            for cid, name, mobile in clients:

                display_name = (
                    f"{name} — {mobile}"
                    if mobile
                    else f"{name} — No mobile"
                )

                self.client_map[
                    display_name
                ] = cid

                result.append({
                    "id": cid,
                    "name": name,
                    "mobile": mobile,
                    "display": display_name
                })

            return result

        finally:

            if cursor:
                cursor.close()

            conn.close()

    # =========================================================
    # EMPLOYEES
    # =========================================================

    def get_employees(self):

        conn = get_connection()

        cursor = None

        try:

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

            return [
                {
                    "id": employee_id,
                    "username": username
                }
                for employee_id, username in employees
            ]

        finally:

            if cursor:
                cursor.close()

            conn.close()

    # =========================================================
    # CREATE TASK
    # =========================================================

    def create_task(self):

        # =====================================================
        # GET VALUES
        # =====================================================

        task_name = (
            self.task_name_entry
            .get()
            .strip()
        )

        task_details = (
            self.task_details_entry
            .get()
            .strip()
        )

        client_display = (
            self.client_var
            .get()
            .strip()
        )

        client_id = self.client_map.get(
            client_display
        )

        department = (
            self.dept_var
            .get()
            .strip()
        )

        miscellaneous_details = (
            self.misc_entry
            .get()
            .strip()
            if department == "Miscellaneous"
            else ""
        )

        assigned_name = (
            self.employee_var
            .get()
            .strip()
        )

        assigned_id = next(
            (
                employee["id"]
                for employee in self.employees
                if employee["username"] == assigned_name
            ),
            None
        )

        # =====================================================
        # VALIDATION
        # =====================================================

        if not task_name:

            messagebox.showerror(
                "Missing Task Name",
                "Please enter a task name."
            )

            return

        if client_id is None:

            messagebox.showerror(
                "Invalid Client",
                "Please select a valid client."
            )

            return

        if not assigned_name or assigned_id is None:

            messagebox.showerror(
                "Invalid Assignment",
                "Please select an employee to assign the task to."
            )

            return

        if (
            department == "Miscellaneous"
            and not miscellaneous_details
        ):

            messagebox.showerror(
                "Missing Details",
                "Please enter miscellaneous details."
            )

            return

        # =====================================================
        # DATABASE INSERT
        # =====================================================

        conn = None
        cursor = None

        try:

            conn = get_connection()

            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO tasks (
                    task_name,
                    task_details,
                    client_id,
                    department,
                    miscellaneous_details,
                    assigned_to,
                    created_by,
                    status
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                RETURNING id
            """, (
                task_name,
                task_details,
                client_id,
                department,
                miscellaneous_details,
                assigned_id,
                self.user["id"],
                0
            ))

            task_id = cursor.fetchone()[0]

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
                    %s,
                    %s,
                    %s
                )
            """, (
                task_id,
                "TASK_CREATED",
                self.user["id"],
                f"Task created: {task_name}"
            ))

            conn.commit()

            messagebox.showinfo(
                "Success",
                f"Task created successfully.\n\nTask ID: {task_id}"
            )

            self.reset_form()

        except Exception as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                f"Database error:\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

    # =========================================================
    # RESET
    # =========================================================

    def reset_form(self):

        self.task_name_entry.delete(
            0,
            "end"
        )

        self.task_details_entry.delete(
            0,
            "end"
        )

        self.misc_entry.delete(
            0,
            "end"
        )

        self.client_var.set(
            ""
        )

        self.employee_var.set(
            ""
        )

        self.selected_client_id = None
        self.selected_employee_id = None

        self.dept_var.set(
            "TDS"
        )

        self.misc_label.grid_forget()
        self.misc_entry.grid_forget()