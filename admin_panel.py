import customtkinter as ctk
import bcrypt
import psycopg

from database import get_connection
from tkinter import messagebox

from theme import *

import constants


class AdminPanel(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            fg_color=COLORS["background"],
            corner_radius=0
        )

        # ============================================================
        # GRID CONFIGURATION
        # ============================================================

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        # ============================================================
        # TITLE
        # ============================================================

        self.title_label = ctk.CTkLabel(
            self,
            text="Admin Panel",
            font=ctk.CTkFont(
                size=SIZES["title_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        )

        self.title_label.grid(
            row=0,
            column=0,
            padx=PADDING["section_x"],
            pady=(0, PADDING["section_y"]),
            sticky="w"
        )

        # ============================================================
        # MAIN SCROLLABLE AREA
        # ============================================================

        self.main_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS["background"],
            corner_radius=0
        )

        self.main_scroll.grid(
            row=1,
            column=0,
            padx=PADDING["section_x"],
            pady=(0, PADDING["section_y"]),
            sticky="nsew"
        )

        self.main_scroll.grid_columnconfigure(
            0,
            weight=1
        )

        # ============================================================
        # USERS MANAGEMENT
        # ============================================================

        self.create_users_section()

        # ============================================================
        # BANK DETAILS
        # ============================================================

        self.create_bank_section()

        # ============================================================
        # NARRATIVE VALUES
        # ============================================================

        self.create_dropdown_section(
            row=2,
            title="Narrative Values",
            category="narrative",
            entry_attribute="narrative_entry",
            add_method=self.add_narrative,
            list_attribute="narrative_scroll"
        )

        # ============================================================
        # FINANCIAL YEARS
        # ============================================================

        self.create_dropdown_section(
            row=3,
            title="Financial Years",
            category="financial_year",
            entry_attribute="financial_year_entry",
            add_method=self.add_financial_year,
            list_attribute="financial_year_scroll"
        )

        # ============================================================
        # TDS FORM TYPES
        # ============================================================

        self.create_dropdown_section(
            row=4,
            title="TDS Form Types",
            category="tds_form_type",
            entry_attribute="tds_form_entry",
            add_method=self.add_tds_form_type,
            list_attribute="tds_form_scroll"
        )

    # ================================================================
    # GENERIC SECTION STYLING
    # ================================================================

    def create_section_frame(self):

        frame = ctk.CTkFrame(
            self.main_scroll,
            fg_color=COLORS["card"],
            corner_radius=SIZES["large_corner_radius"],
            border_width=3,
            border_color=COLORS["border"]
        )

        return frame

    # ================================================================
    # USERS MANAGEMENT
    # ================================================================

    def create_users_section(self):

        self.users_frame = self.create_section_frame()

        self.users_frame.grid(
            row=0,
            column=0,
            padx=0,
            pady=(0, PADDING["section_y"]),
            sticky="ew"
        )

        self.users_frame.grid_rowconfigure(
            2,
            weight=1
        )

        self.users_frame.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            self.users_frame,
            text="User Management",
            font=ctk.CTkFont(
                size=SIZES["heading_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            padx=PADDING["form_x"],
            pady=PADDING["form_y"],
            sticky="w"
        )

        # ------------------------------------------------------------
        # ADD USER FORM
        # ------------------------------------------------------------

        self.add_user_frame = ctk.CTkFrame(
            self.users_frame,
            fg_color=COLORS["card_alt"],
            corner_radius=SIZES["corner_radius"]
        )

        self.add_user_frame.grid(
            row=1,
            column=0,
            padx=PADDING["form_x"],
            pady=PADDING["form_y"],
            sticky="ew"
        )

        self.add_user_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.add_user_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.add_user_frame.grid_columnconfigure(
            2,
            weight=1
        )

        self.new_username = ctk.CTkEntry(
            self.add_user_frame,
            placeholder_text="Username",
            width=SIZES["entry_width"],
            height=SIZES["entry_height"],
            fg_color=COLORS["input"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            border_color=COLORS["border"],
            border_width=3,
            corner_radius=SIZES["small_corner_radius"]
        )

        self.new_username.grid(
            row=0,
            column=0,
            padx=6,
            pady=6,
            sticky="ew"
        )

        self.new_password = ctk.CTkEntry(
            self.add_user_frame,
            placeholder_text="Password",
            show="*",
            width=SIZES["entry_width"],
            height=SIZES["entry_height"],
            fg_color=COLORS["input"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            border_color=COLORS["border"],
            border_width=3,
            corner_radius=SIZES["small_corner_radius"]
        )

        self.new_password.grid(
            row=1,
            column=0,
            padx=6,
            pady=6,
            sticky="ew"
        )

        self.new_role = ctk.CTkComboBox(
            self.add_user_frame,
            values=["Employee", "Accounts", "Admin"],
            width=SIZES["dropdown_width"],
            height=SIZES["entry_height"],
            fg_color=COLORS["input"],
            button_color=SIDEBAR_HOVER,
            button_hover_color=COLORS["primary_hover"],
            text_color=COLORS["text"],
            border_color=COLORS["border"],
            dropdown_fg_color=COLORS["card"],
            dropdown_hover_color=COLORS["primary_hover"],
            dropdown_text_color=COLORS["text"],
            corner_radius=SIZES["small_corner_radius"]
        )

        self.new_role.grid(
            row=2,
            column=0,
            padx=6,
            pady=6,
            sticky="ew"
        )

        self.add_user_btn = ctk.CTkButton(
            self.add_user_frame,
            text="Add User",
            command=self.add_user,
            width=SIZES["button_width"],
            height=SIZES["button_height"],
            fg_color=SIDEBAR_HOVER,
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["toggle"],
            corner_radius=SIZES["corner_radius"],
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            )
        )

        self.add_user_btn.grid(
            row=3,
            column=0,
            padx=6,
            pady=10,
            sticky="ew"
        )

        # ------------------------------------------------------------
        # USER LIST
        # ------------------------------------------------------------

        self.user_scroll = ctk.CTkScrollableFrame(
            self.users_frame,
            fg_color=COLORS["input"],
            corner_radius=SIZES["corner_radius"]
        )

        self.user_scroll.grid(
            row=2,
            column=0,
            padx=PADDING["form_x"],
            pady=PADDING["form_y"],
            sticky="nsew"
        )

        self.user_scroll.grid_columnconfigure(
            0,
            weight=1
        )

        self.load_users()

    # ================================================================
    # LOAD USERS
    # ================================================================

    def load_users(self):

        for widget in self.user_scroll.winfo_children():
            widget.destroy()

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id, username, role, is_active
                FROM users
                ORDER BY username
                """
            )

            users = cursor.fetchall()

        except psycopg.Error as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load users:\n{e}"
            )

            return

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        for i, (uid, uname, role, active) in enumerate(users):

            status = "Active" if active else "Inactive"

            ctk.CTkLabel(
                self.user_scroll,
                text=f"{uname} ({role}) - {status}",
                font=ctk.CTkFont(
                    size=SIZES["normal_size"]
                ),
                text_color=COLORS["text"]
            ).grid(
                row=i,
                column=0,
                padx=PADDING["x"],
                pady=8,
                sticky="w"
            )

            btn_text = (
                "Deactivate"
                if active
                else "Activate"
            )

            btn_color = (
                LOGOUT
                if active
                else COLORS["primary"]
            )

            btn_hover = (
                LOGOUT_HOVER
                if active
                else COLORS["primary_hover"]
            )

            ctk.CTkButton(
                self.user_scroll,
                text=btn_text,
                width=120,
                height=SIZES["button_height"],
                fg_color=btn_color,
                hover_color=btn_hover,
                text_color=COLORS["toggle"],
                corner_radius=SIZES["small_corner_radius"],
                font=ctk.CTkFont(
                    size=SIZES["small_size"],
                    weight="bold"
                ),
                command=lambda u=uid, s=active:
                    self.toggle_user_status(u, s)
            ).grid(
                row=i,
                column=1,
                padx=6,
                pady=8
            )

            ctk.CTkButton(
                self.user_scroll,
                text="Reset Password",
                width=140,
                height=SIZES["button_height"],
                fg_color=SIDEBAR_HOVER,
                hover_color=COLORS["primary_hover"],
                text_color=COLORS["toggle"],
                corner_radius=SIZES["small_corner_radius"],
                font=ctk.CTkFont(
                    size=SIZES["small_size"],
                    weight="bold"
                ),
                command=lambda u=uid, n=uname:
                    self.reset_password(u, n)
            ).grid(
                row=i,
                column=2,
                padx=PADDING["x"],
                pady=8
            )

    # ================================================================
    # TOGGLE USER STATUS
    # ================================================================

    def toggle_user_status(
        self,
        user_id,
        current_status
    ):

        new_status = 0 if current_status else 1

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE users
                SET is_active = %s
                WHERE id = %s
                """,
                (
                    new_status,
                    user_id
                )
            )

            conn.commit()

        except psycopg.Error as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to update user status:\n{e}"
            )

            return

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        self.load_users()

    # ================================================================
    # ADD USER
    # ================================================================

    def add_user(self):

        username = self.new_username.get().strip()
        password = self.new_password.get().strip()
        role = self.new_role.get()

        if not username or not password:

            messagebox.showerror(
                "Error",
                "Username and password required"
            )

            return

        if not role:

            messagebox.showerror(
                "Error",
                "Please select a role"
            )

            return

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users (
                    username,
                    password,
                    role
                )
                VALUES (%s, %s, %s)
                """,
                (
                    username,
                    hashed_password,
                    role
                )
            )

            conn.commit()

            self.new_username.delete(
                0,
                "end"
            )

            self.new_password.delete(
                0,
                "end"
            )

            self.load_users()

            messagebox.showinfo(
                "Success",
                "User added successfully"
            )

        except psycopg.errors.UniqueViolation:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Error",
                "Username already exists"
            )

        except psycopg.Error as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to add user:\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

    # ================================================================
    # RESET PASSWORD
    # ================================================================

    def reset_password(
        self,
        user_id,
        username
    ):

        dialog = ctk.CTkInputDialog(
            text=f"Enter a new password for '{username}':",
            title="Reset Password"
        )

        new_password = dialog.get_input()

        if new_password is None:
            return

        new_password = new_password.strip()

        if not new_password:

            messagebox.showerror(
                "Error",
                "Password cannot be empty"
            )

            return

        hashed_password = bcrypt.hashpw(
            new_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE users
                SET password = %s
                WHERE id = %s
                """,
                (
                    hashed_password,
                    user_id
                )
            )

            if cursor.rowcount == 0:

                conn.rollback()

                messagebox.showerror(
                    "Error",
                    "User not found"
                )

                return

            conn.commit()

            messagebox.showinfo(
                "Success",
                f"Password for '{username}' "
                f"has been reset successfully."
            )

        except psycopg.Error as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to reset password:\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

    # ================================================================
    # BANK DETAILS SECTION
    # ================================================================

    def create_bank_section(self):

        self.bank_frame = self.create_section_frame()

        self.bank_frame.grid(
            row=1,
            column=0,
            padx=0,
            pady=(0, PADDING["section_y"]),
            sticky="ew"
        )

        self.bank_frame.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            self.bank_frame,
            text="Bank Details",
            font=ctk.CTkFont(
                size=SIZES["heading_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            padx=PADDING["form_x"],
            pady=PADDING["form_y"],
            sticky="w"
        )

        self.add_bank_frame = ctk.CTkFrame(
            self.bank_frame,
            fg_color=COLORS["card_alt"],
            corner_radius=SIZES["corner_radius"]
        )

        self.add_bank_frame.grid(
            row=1,
            column=0,
            padx=PADDING["form_x"],
            pady=PADDING["form_y"],
            sticky="ew"
        )

        for i in range(2):
            self.add_bank_frame.grid_columnconfigure(
                i,
                weight=1
            )

        self.bank_display_name = self.make_entry(
            self.add_bank_frame,
            "Display Name (e.g. CUB - Kuttalam)"
        )

        self.bank_display_name.grid(
            row=0,
            column=0,
            padx=6,
            pady=6,
            sticky="ew"
        )

        self.bank_name = self.make_entry(
            self.add_bank_frame,
            "Bank Name"
        )

        self.bank_name.grid(
            row=0,
            column=1,
            padx=6,
            pady=6,
            sticky="ew"
        )

        self.bank_ifsc = self.make_entry(
            self.add_bank_frame,
            "IFSC"
        )

        self.bank_ifsc.grid(
            row=1,
            column=0,
            padx=6,
            pady=6,
            sticky="ew"
        )

        self.bank_branch = self.make_entry(
            self.add_bank_frame,
            "Branch"
        )

        self.bank_branch.grid(
            row=1,
            column=1,
            padx=6,
            pady=6,
            sticky="ew"
        )

        self.bank_account_number = self.make_entry(
            self.add_bank_frame,
            "Account Number"
        )

        self.bank_account_number.grid(
            row=2,
            column=0,
            padx=6,
            pady=6,
            sticky="ew"
        )

        self.bank_account_holder = self.make_entry(
            self.add_bank_frame,
            "Account Holder Name"
        )

        self.bank_account_holder.grid(
            row=2,
            column=1,
            padx=6,
            pady=6,
            sticky="ew"
        )

        self.bank_upi_id = self.make_entry(
            self.add_bank_frame,
            "UPI ID"
        )

        self.bank_upi_id.grid(
            row=3,
            column=0,
            padx=6,
            pady=6,
            sticky="ew"
        )

        ctk.CTkButton(
            self.add_bank_frame,
            text="Add Bank",
            command=self.add_bank,
            height=SIZES["button_height"],
            fg_color=SIDEBAR_HOVER,
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["toggle"],
            corner_radius=SIZES["corner_radius"],
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            )
        ).grid(
            row=3,
            column=1,
            padx=6,
            pady=10,
            sticky="ew"
        )

        self.bank_scroll = ctk.CTkScrollableFrame(
            self.bank_frame,
            fg_color=COLORS["input"],
            corner_radius=SIZES["corner_radius"],
            height=250
        )

        self.bank_scroll.grid(
            row=2,
            column=0,
            padx=PADDING["form_x"],
            pady=PADDING["form_y"],
            sticky="ew"
        )

        self.bank_scroll.grid_columnconfigure(
            0,
            weight=1
        )

        self.load_banks()

    # ================================================================
    # MAKE ENTRY
    # ================================================================

    def make_entry(
        self,
        parent,
        placeholder
    ):

        return ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            height=SIZES["entry_height"],
            fg_color=COLORS["input"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            border_color=COLORS["border"],
            border_width=3,
            corner_radius=SIZES["small_corner_radius"]
        )

    # ================================================================
    # LOAD BANKS
    # ================================================================

    def load_banks(self):

        for widget in self.bank_scroll.winfo_children():
            widget.destroy()

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    display_name,
                    bank_name,
                    ifsc,
                    branch,
                    account_number,
                    account_holder_name,
                    upi_id
                FROM bank_details
                ORDER BY display_name
                """
            )

            banks = cursor.fetchall()

        except psycopg.Error as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load bank details:\n{e}"
            )

            return

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        for i, bank in enumerate(banks):

            (
                bank_id,
                display_name,
                bank_name,
                ifsc,
                branch,
                account_number,
                account_holder_name,
                upi_id
            ) = bank

            bank_text = (
                f"{display_name}\n"
                f"{bank_name} | {branch}\n"
                f"IFSC: {ifsc} | "
                f"Account: {account_number}\n"
                f"Holder: {account_holder_name} | "
                f"UPI: {upi_id}"
            )

            ctk.CTkLabel(
                self.bank_scroll,
                text=bank_text,
                font=ctk.CTkFont(
                    size=SIZES["small_size"]
                ),
                text_color=COLORS["text"],
                justify="left",
                anchor="w"
            ).grid(
                row=i,
                column=0,
                padx=PADDING["x"],
                pady=8,
                sticky="ew"
            )

            ctk.CTkButton(
                self.bank_scroll,
                text="Delete",
                width=90,
                height=SIZES["button_height"],
                fg_color=LOGOUT,
                hover_color=LOGOUT_HOVER,
                text_color=COLORS["toggle"],
                corner_radius=SIZES["small_corner_radius"],
                font=ctk.CTkFont(
                    size=SIZES["small_size"],
                    weight="bold"
                ),
                command=lambda b=bank_id, n=display_name:
                    self.delete_bank(b, n)
            ).grid(
                row=i,
                column=1,
                padx=6,
                pady=8
            )

    # ================================================================
    # ADD BANK
    # ================================================================

    def add_bank(self):

        display_name = self.bank_display_name.get().strip()
        bank_name = self.bank_name.get().strip()
        ifsc = self.bank_ifsc.get().strip()
        branch = self.bank_branch.get().strip()
        account_number = self.bank_account_number.get().strip()
        account_holder_name = self.bank_account_holder.get().strip()
        upi_id = self.bank_upi_id.get().strip()

        fields = [
            (display_name, "Display Name"),
            (bank_name, "Bank Name"),
            (ifsc, "IFSC"),
            (branch, "Branch"),
            (account_number, "Account Number"),
            (account_holder_name, "Account Holder Name"),
            (upi_id, "UPI ID")
        ]

        for value, label in fields:

            if not value:

                messagebox.showerror(
                    "Error",
                    f"{label} is required"
                )

                return

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO bank_details (
                    display_name,
                    bank_name,
                    ifsc,
                    branch,
                    account_number,
                    account_holder_name,
                    upi_id
                )
                VALUES (
                    %s, %s, %s, %s,
                    %s, %s, %s
                )
                """,
                (
                    display_name,
                    bank_name,
                    ifsc,
                    branch,
                    account_number,
                    account_holder_name,
                    upi_id
                )
            )

            conn.commit()

            self.clear_bank_form()

            self.load_banks()

            # Refresh global bank values
            constants.refresh_bank_details()

            constants.UPI_BANKS = constants.get_upi_banks()

            messagebox.showinfo(
                "Success",
                "Bank details added successfully"
            )

        except psycopg.errors.UniqueViolation:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Error",
                "A bank with this Display Name already exists"
            )

        except psycopg.Error as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to add bank details:\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

    # ================================================================
    # CLEAR BANK FORM
    # ================================================================

    def clear_bank_form(self):

        for widget in [
            self.bank_display_name,
            self.bank_name,
            self.bank_ifsc,
            self.bank_branch,
            self.bank_account_number,
            self.bank_account_holder,
            self.bank_upi_id
        ]:

            widget.delete(
                0,
                "end"
            )

    # ================================================================
    # DELETE BANK
    # ================================================================

    def delete_bank(
        self,
        bank_id,
        display_name
    ):

        confirm = messagebox.askyesno(
            "Delete Bank",
            f"Are you sure you want to delete "
            f"'{display_name}'?"
        )

        if not confirm:
            return

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM bank_details
                WHERE id = %s
                """,
                (
                    bank_id,
                )
            )

            conn.commit()

            constants.refresh_bank_details()

            constants.UPI_BANKS = constants.get_upi_banks()

            self.load_banks()

            messagebox.showinfo(
                "Success",
                "Bank details deleted successfully"
            )

        except psycopg.Error as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to delete bank details:\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

    # ================================================================
    # GENERIC DROPDOWN SECTION
    # ================================================================

    def create_dropdown_section(
        self,
        row,
        title,
        category,
        entry_attribute,
        add_method,
        list_attribute
    ):

        frame = self.create_section_frame()

        frame.grid(
            row=row,
            column=0,
            padx=0,
            pady=(0, PADDING["section_y"]),
            sticky="ew"
        )

        frame.grid_columnconfigure(
            0,
            weight=1
        )

        # ------------------------------------------------------------
        # HEADING
        # ------------------------------------------------------------

        ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(
                size=SIZES["heading_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            padx=PADDING["form_x"],
            pady=PADDING["form_y"],
            sticky="w"
        )

        # ------------------------------------------------------------
        # ADD FORM
        # ------------------------------------------------------------

        add_frame = ctk.CTkFrame(
            frame,
            fg_color=COLORS["card_alt"],
            corner_radius=SIZES["corner_radius"]
        )

        add_frame.grid(
            row=1,
            column=0,
            padx=PADDING["form_x"],
            pady=PADDING["form_y"],
            sticky="ew"
        )

        add_frame.grid_columnconfigure(
            0,
            weight=1
        )

        entry = ctk.CTkEntry(
            add_frame,
            placeholder_text=f"Add {title[:-1] if title.endswith('s') else title}",
            height=SIZES["entry_height"],
            fg_color=COLORS["input"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            border_color=COLORS["border"],
            border_width=3,
            corner_radius=SIZES["small_corner_radius"]
        )

        entry.grid(
            row=0,
            column=0,
            padx=6,
            pady=6,
            sticky="ew"
        )

        setattr(
            self,
            entry_attribute,
            entry
        )

        ctk.CTkButton(
            add_frame,
            text="Add",
            command=add_method,
            width=SIZES["button_width"],
            height=SIZES["button_height"],
            fg_color=SIDEBAR_HOVER,
            hover_color=COLORS["primary_hover"],
            text_color=COLORS["toggle"],
            corner_radius=SIZES["corner_radius"],
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            )
        ).grid(
            row=0,
            column=1,
            padx=6,
            pady=6
        )

        # ------------------------------------------------------------
        # LIST
        # ------------------------------------------------------------

        scroll = ctk.CTkScrollableFrame(
            frame,
            fg_color=COLORS["input"],
            corner_radius=SIZES["corner_radius"],
            height=180
        )

        scroll.grid(
            row=2,
            column=0,
            padx=PADDING["form_x"],
            pady=PADDING["form_y"],
            sticky="ew"
        )

        scroll.grid_columnconfigure(
            0,
            weight=1
        )

        setattr(
            self,
            list_attribute,
            scroll
        )

        self.load_dropdown_values(
            category,
            scroll
        )

    # ================================================================
    # LOAD DROPDOWN VALUES
    # ================================================================

    def load_dropdown_values(
        self,
        category,
        scroll
    ):

        for widget in scroll.winfo_children():
            widget.destroy()

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    value
                FROM app_dropdown_values
                WHERE category = %s
                ORDER BY sort_order, value
                """,
                (
                    category,
                )
            )

            values = cursor.fetchall()

        except psycopg.Error as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load {category} values:\n{e}"
            )

            return

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        for i, (value_id, value) in enumerate(values):

            ctk.CTkLabel(
                scroll,
                text=value,
                font=ctk.CTkFont(
                    size=SIZES["normal_size"]
                ),
                text_color=COLORS["text"],
                anchor="w"
            ).grid(
                row=i,
                column=0,
                padx=PADDING["x"],
                pady=8,
                sticky="ew"
            )

            ctk.CTkButton(
                scroll,
                text="Delete",
                width=90,
                height=SIZES["button_height"],
                fg_color=LOGOUT,
                hover_color=LOGOUT_HOVER,
                text_color=COLORS["toggle"],
                corner_radius=SIZES["small_corner_radius"],
                font=ctk.CTkFont(
                    size=SIZES["small_size"],
                    weight="bold"
                ),
                command=lambda vid=value_id, v=value, c=category:
                    self.delete_dropdown_value(
                        vid,
                        v,
                        c
                    )
            ).grid(
                row=i,
                column=1,
                padx=6,
                pady=8
            )

    # ================================================================
    # ADD GENERIC DROPDOWN VALUE
    # ================================================================

    def add_dropdown_value(
        self,
        category,
        entry,
        scroll,
        label
    ):

        value = entry.get().strip()

        if not value:

            messagebox.showerror(
                "Error",
                f"{label} cannot be empty"
            )

            return

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            # --------------------------------------------------------
            # Get next sort order
            # --------------------------------------------------------

            cursor.execute(
                """
                SELECT COALESCE(
                    MAX(sort_order),
                    0
                ) + 1
                FROM app_dropdown_values
                WHERE category = %s
                """,
                (
                    category,
                )
            )

            sort_order = cursor.fetchone()[0]

            # --------------------------------------------------------
            # Insert
            # --------------------------------------------------------

            cursor.execute(
                """
                INSERT INTO app_dropdown_values (
                    category,
                    value,
                    sort_order
                )
                VALUES (
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    category,
                    value,
                    sort_order
                )
            )

            conn.commit()

            entry.delete(
                0,
                "end"
            )

            # Reload UI
            self.load_dropdown_values(
                category,
                scroll
            )

            # Reload global constants
            constants.refresh_dropdown_values()

            messagebox.showinfo(
                "Success",
                f"{label} added successfully."
            )

        except psycopg.errors.UniqueViolation:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Error",
                f"'{value}' already exists."
            )

        except psycopg.Error as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to add {label.lower()}:\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

    # ================================================================
    # DELETE GENERIC DROPDOWN VALUE
    # ================================================================

    def delete_dropdown_value(
        self,
        value_id,
        value,
        category
    ):

        confirm = messagebox.askyesno(
            "Delete Value",
            f"Are you sure you want to delete "
            f"'{value}'?"
        )

        if not confirm:
            return

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM app_dropdown_values
                WHERE id = %s
                """,
                (
                    value_id,
                )
            )

            conn.commit()

            # Reload global constants
            constants.refresh_dropdown_values()

            # Reload appropriate UI
            if category == "narrative":

                self.load_dropdown_values(
                    category,
                    self.narrative_scroll
                )

            elif category == "financial_year":

                self.load_dropdown_values(
                    category,
                    self.financial_year_scroll
                )

            elif category == "tds_form_type":

                self.load_dropdown_values(
                    category,
                    self.tds_form_scroll
                )

            messagebox.showinfo(
                "Success",
                "Value deleted successfully."
            )

        except psycopg.Error as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to delete value:\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

    # ================================================================
    # ADD NARRATIVE
    # ================================================================

    def add_narrative(self):

        self.add_dropdown_value(
            category="narrative",
            entry=self.narrative_entry,
            scroll=self.narrative_scroll,
            label="Narrative"
        )

    # ================================================================
    # ADD FINANCIAL YEAR
    # ================================================================

    def add_financial_year(self):

        self.add_dropdown_value(
            category="financial_year",
            entry=self.financial_year_entry,
            scroll=self.financial_year_scroll,
            label="Financial Year"
        )

    # ================================================================
    # ADD TDS FORM TYPE
    # ================================================================

    def add_tds_form_type(self):

        self.add_dropdown_value(
            category="tds_form_type",
            entry=self.tds_form_entry,
            scroll=self.tds_form_scroll,
            label="TDS Form Type"
        )