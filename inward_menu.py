
import customtkinter as ctk
import sqlite3
from searchable_combobox import SearchableComboBox
from datetime import datetime
from database import DB_NAME
from tkinter import messagebox

from theme import *


class InwardMenu(ctk.CTkFrame):

    def __init__(self, master, user):

        super().__init__(
            master,
            fg_color=COLORS["background"]
        )

        self.user = user

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
            text="Inward Entry Form",
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

    def on_client_selected(self, selected_value):

        client_id = self.client_map.get(
            selected_value
        )

        if client_id is not None:

            self.selected_client_id = client_id

        else:

            self.selected_client_id = None

    # =========================================================
    # HELPER - LABEL
    # =========================================================

    def create_label(
        self,
        text,
        row
    ):

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
    # HELPER - ENTRY
    # =========================================================

    def create_entry(
        self,
        placeholder=""
    ):

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
    # HELPER - DROPDOWN
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

            dropdown_fg_color=COLORS['primary_hover'],
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

        # -----------------------------------------------------
        # DATE OF ENTRY
        # -----------------------------------------------------

        # Display format:
        # DD-MM-YYYY
        #
        # Database format remains:
        # YYYY-MM-DD

        self.date_of_entry = datetime.now().strftime(
            "%d-%m-%Y"
        )

        # -----------------------------------------------------
        # DATE OF RECEIPT
        # -----------------------------------------------------

        self.create_label(
            "Date of Receipt (DD-MM-YYYY):",
            0
        )

        self.receipt_date_entry = self.create_entry(
            "DD-MM-YYYY"
        )

        self.receipt_date_entry.insert(
            0,
            self.date_of_entry
        )

        self.receipt_date_entry.grid(
            row=0,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # -----------------------------------------------------
        # CLIENT
        # -----------------------------------------------------

        self.create_label(
            "Client Name:",
            1
        )

        self.client_var = ctk.StringVar(
            value=""
        )

        self.clients = self.get_clients()

        self.client_dropdown = SearchableComboBox(
            self.form_frame,

            values=[
                client["display"]
                for client in self.clients
            ],

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
            row=1,
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
            2
        )

        depts = [
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
            depts,
            self.on_dept_change
        )

        self.dept_dropdown.grid(
            row=2,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # -----------------------------------------------------
        # MISCELLANEOUS
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # NATURE OF PAPERS
        # -----------------------------------------------------

        self.create_label(
            "Nature of Papers:",
            4
        )

        self.nature_entry = ctk.CTkEntry(
            self.form_frame,

            width=SIZES["textbox_width"],
            height=SIZES["entry_height"],

            fg_color=COLORS["input"],
            border_color=COLORS["border"],

            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],

            placeholder_text="Describe the papers received",

            corner_radius=SIZES["corner_radius"],

            font=ctk.CTkFont(
                size=SIZES["normal_size"]
            )
        )

        self.nature_entry.grid(
            row=4,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # -----------------------------------------------------
        # ASSIGN TO
        # -----------------------------------------------------

        self.create_label(
            "Assign To:",
            5
        )

        self.employee_var = ctk.StringVar(
            value=""
        )

        self.employees = self.get_employees()

        emp_names = [
            e["username"]
            for e in self.employees
        ]

        self.assign_dropdown = self.create_dropdown(
            self.employee_var,
            (
                emp_names
                if emp_names
                else ["No employees found"]
            )
        )

        self.assign_dropdown.grid(
            row=5,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # -----------------------------------------------------
        # HOW RECEIVED
        # -----------------------------------------------------

        self.create_label(
            "How Received:",
            6
        )

        methods = [
            "hand delivery",
            "email",
            "courier",
            "speed post"
        ]

        self.received_var = ctk.StringVar(
            value=methods[0]
        )

        self.received_dropdown = self.create_dropdown(
            self.received_var,
            methods
        )

        self.received_dropdown.grid(
            row=6,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # -----------------------------------------------------
        # SUBMIT
        # -----------------------------------------------------

        self.submit_btn = ctk.CTkButton(
            self.form_frame,

            text="✓  Submit Entry",

            command=self.submit_entry,

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
            row=7,
            column=0,
            columnspan=2,
            padx=PADDING["x"],
            pady=(25, 30)
        )

    # =========================================================
    # DEPARTMENT CHANGE
    # =========================================================

    def on_dept_change(self, choice):

        if choice == "Miscellaneous":

            self.misc_label.grid(
                row=3,
                column=0,
                padx=PADDING["x"],
                pady=PADDING["y"],
                sticky="w"
            )

            self.misc_entry.grid(
                row=3,
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

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    mobile
                FROM clients
                ORDER BY name COLLATE NOCASE
                """
            )

            clients = cursor.fetchall()

        finally:

            conn.close()

        self.client_map = {}

        result = []

        for cid, name, mobile in clients:

            display_name = (
                f"{name} — {mobile}"
                if mobile
                else f"{name} — No mobile"
            )

            client = {
                "id": cid,
                "name": name,
                "mobile": mobile,
                "display": display_name
            }

            result.append(client)

            self.client_map[
                display_name
            ] = cid

        return result

    # =========================================================
    # EMPLOYEES
    # =========================================================

    def get_employees(self):

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

            emps = cursor.fetchall()

        finally:

            conn.close()

        return [
            {
                "id": eid,
                "username": uname
            }
            for eid, uname in emps
        ]

    # =========================================================
    # SUBMIT
    # =========================================================

    def submit_entry(self):

        # -----------------------------------------------------
        # DATE ENTERED BY USER
        # -----------------------------------------------------

        receipt_date_display = (
            self.receipt_date_entry
            .get()
            .strip()
        )

        # -----------------------------------------------------
        # CONVERT DISPLAY DATE TO DATABASE DATE
        # -----------------------------------------------------

        try:

            receipt_date_obj = datetime.strptime(
                receipt_date_display,
                "%d-%m-%Y"
            )

            receipt_date = receipt_date_obj.strftime(
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Date",
                "Please enter the date in DD-MM-YYYY format."
            )

            return

        client_name = self.client_var.get()
        client_display = self.client_var.get()

        client_id = self.client_map.get(
            client_display
        )

        dept = self.dept_var.get()

        misc = (
            self.misc_entry.get().strip()
            if dept == "Miscellaneous"
            else ""
        )

        nature = (
            self.nature_entry
            .get()
            .strip()
        )

        assigned_name = self.employee_var.get()

        how_rec = self.received_var.get()

        # -----------------------------------------------------
        # VALIDATION
        # -----------------------------------------------------

        if (
            not nature
            or not client_display
            or client_id is None
            or client_display == "No clients found"
            or assigned_name == "No employees found"
            or not assigned_name
        ):

            messagebox.showerror(
                "Error",
                "Please fill in all required fields and ensure "
                "clients/employees exist."
            )

            return

        client_id = self.client_map.get(
            client_name
        )

        assigned_id = next(
            (
                e["id"]
                for e in self.employees
                if e["username"] == assigned_name
            ),
            None
        )

        if not client_id or not assigned_id:

            messagebox.showerror(
                "Error",
                "Invalid client or employee selection."
            )

            return

        # -----------------------------------------------------
        # DATABASE INSERT
        # -----------------------------------------------------

        try:

            conn = sqlite3.connect(DB_NAME)

            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO records (
                    date_of_entry,
                    date_of_receipt,
                    client_id,
                    department,
                    miscellaneous_details,
                    nature_of_papers,
                    entered_by,
                    assigned_to,
                    how_received,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
            """, (
                # Database format remains YYYY-MM-DD
                datetime.now().strftime("%Y-%m-%d"),

                # Converted from user's DD-MM-YYYY input
                receipt_date,

                client_id,
                dept,
                misc,
                nature,
                self.user["id"],
                assigned_id,
                how_rec
            ))

            conn.commit()

            conn.close()

            messagebox.showinfo(
                "Success",
                "Inward entry successfully added."
            )

            # -------------------------------------------------
            # RESET FORM
            # -------------------------------------------------

            self.nature_entry.delete(
                0,
                "end"
            )

            self.misc_entry.delete(
                0,
                "end"
            )

            self.receipt_date_entry.delete(
                0,
                "end"
            )

            # Display format remains DD-MM-YYYY
            self.receipt_date_entry.insert(
                0,
                datetime.now().strftime("%d-%m-%Y")
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Database error: {e}"
            )
