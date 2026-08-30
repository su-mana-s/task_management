
import customtkinter as ctk
import sqlite3
import bcrypt

from database import DB_NAME
from tkinter import messagebox

from theme import *


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

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

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
        # USERS MANAGEMENT SECTION
        # ============================================================

        self.users_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS["card"],
            corner_radius=SIZES["large_corner_radius"],
            border_width=3,
            border_color=COLORS["border"]
        )

        self.users_frame.grid(
            row=1,
            column=0,
            padx=PADDING["section_x"],
            pady=(0, PADDING["section_y"]),
            sticky="nsew"
        )

        self.users_frame.grid_rowconfigure(2, weight=1)
        self.users_frame.grid_columnconfigure(0, weight=1)

        # ============================================================
        # SECTION HEADING
        # ============================================================

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

        # ============================================================
        # ADD USER FORM
        # ============================================================

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

        self.add_user_frame.grid_columnconfigure(0, weight=1)
        self.add_user_frame.grid_columnconfigure(1, weight=1)
        self.add_user_frame.grid_columnconfigure(2, weight=1)
        self.add_user_frame.grid_columnconfigure(3, weight=0)

        # ============================================================
        # USERNAME
        # ============================================================

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

        # ============================================================
        # PASSWORD
        # ============================================================

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

        # ============================================================
        # ROLE
        # ============================================================

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

        # ============================================================
        # ADD USER BUTTON
        # ============================================================

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

        # ============================================================
        # USER LIST
        # ============================================================

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

        self.user_scroll.grid_columnconfigure(0, weight=1)

        self.load_users()

    # ================================================================
    # USER MANAGEMENT
    # ================================================================

    def load_users(self):
        """
        Load all users from the database and display them.
        """

        # Clear existing widgets
        for widget in self.user_scroll.winfo_children():
            widget.destroy()

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, username, role, is_active
            FROM users
            ORDER BY username
            """
        )

        users = cursor.fetchall()
        conn.close()

        for i, (uid, uname, role, active) in enumerate(users):

            status = "Active" if active else "Inactive"

            # ========================================================
            # USER INFORMATION
            # ========================================================

            lbl = ctk.CTkLabel(
                self.user_scroll,
                text=f"{uname} ({role}) - {status}",
                font=ctk.CTkFont(
                    size=SIZES["normal_size"]
                ),
                text_color=COLORS["text"]
            )

            lbl.grid(
                row=i,
                column=0,
                padx=PADDING["x"],
                pady=8,
                sticky="w"
            )

            # ========================================================
            # TOGGLE STATUS BUTTON
            # ========================================================

            btn_text = "Deactivate" if active else "Activate"

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

            status_btn = ctk.CTkButton(
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
            )

            status_btn.grid(
                row=i,
                column=1,
                padx=6,
                pady=8
            )

            # ========================================================
            # RESET PASSWORD BUTTON
            # ========================================================

            reset_btn = ctk.CTkButton(
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
            )

            reset_btn.grid(
                row=i,
                column=2,
                padx=PADDING["x"],
                pady=8
            )

    # ================================================================
    # TOGGLE USER STATUS
    # ================================================================

    def toggle_user_status(self, user_id, current_status):
        """
        Activate or deactivate a user.
        """

        new_status = 0 if current_status else 1

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE users
            SET is_active = ?
            WHERE id = ?
            """,
            (new_status, user_id)
        )

        conn.commit()
        conn.close()

        self.load_users()

    # ================================================================
    # ADD USER
    # ================================================================

    def add_user(self):
        """
        Create a new user with a bcrypt-hashed password.
        """

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

        # Hash password using bcrypt
        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            salt
        ).decode("utf-8")

        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
                """,
                (
                    username,
                    hashed_password,
                    role
                )
            )

            conn.commit()
            conn.close()

            # Clear form
            self.new_username.delete(0, "end")
            self.new_password.delete(0, "end")

            # Refresh user list
            self.load_users()

            messagebox.showinfo(
                "Success",
                "User added successfully"
            )

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error",
                "Username already exists"
            )

        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error",
                f"Unable to add user:\n{e}"
            )

    # ================================================================
    # RESET PASSWORD
    # ================================================================

    def reset_password(self, user_id, username):
        """
        Reset the password for an existing user.
        """

        # Ask for new password
        dialog = ctk.CTkInputDialog(
            text=f"Enter a new password for '{username}':",
            title="Reset Password"
        )

        new_password = dialog.get_input()

        if new_password is None:
            # User cancelled the dialog
            return

        new_password = new_password.strip()

        if not new_password:
            messagebox.showerror(
                "Error",
                "Password cannot be empty"
            )
            return

        # Hash the new password using bcrypt
        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(
            new_password.encode("utf-8"),
            salt
        ).decode("utf-8")

        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE users
                SET password = ?
                WHERE id = ?
                """,
                (
                    hashed_password,
                    user_id
                )
            )

            conn.commit()

            # Check whether the user actually existed
            if cursor.rowcount == 0:
                conn.close()

                messagebox.showerror(
                    "Error",
                    "User not found"
                )
                return

            conn.close()

            messagebox.showinfo(
                "Success",
                f"Password for '{username}' has been reset successfully."
            )

        except sqlite3.Error as e:
            messagebox.showerror(
                "Database Error",
                f"Unable to reset password:\n{e}"
)
