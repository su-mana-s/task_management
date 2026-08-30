
import customtkinter as ctk
import sqlite3
import bcrypt

from database import DB_NAME
from theme import COLORS, SIZES, PADDING


class LoginWindow(ctk.CTkFrame):

    def __init__(self, master, on_login_success):

        super().__init__(
            master,
            fg_color=COLORS["background"]
        )

        self.on_login_success = on_login_success

        # =====================================================
        # GRID CONFIGURATION
        # =====================================================

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # =====================================================
        # LOGIN CARD
        # =====================================================

        self.login_card = ctk.CTkFrame(
            self,
            fg_color=COLORS["card"],
            corner_radius=15,
            border_width=1,
            border_color=COLORS["border"]
        )

        self.login_card.grid(
            row=1,
            column=1,
            rowspan=4,
            padx=40,
            pady=20
        )

        # Internal padding / layout
        self.login_card.grid_columnconfigure(
            0,
            weight=1
        )

        # =====================================================
        # TITLE
        # =====================================================

        self.title_label = ctk.CTkLabel(
            self.login_card,
            text="Task Management System",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            ),
            text_color=COLORS["primary"]
        )

        self.title_label.grid(
            row=0,
            column=0,
            padx=40,
            pady=(35, 10)
        )

        # =====================================================
        # SUBTITLE
        # =====================================================

        self.subtitle_label = ctk.CTkLabel(
            self.login_card,
            text="Sign in to continue",
            font=ctk.CTkFont(
                size=SIZES["normal_size"]
            ),
            text_color=COLORS["text_secondary"]
        )

        self.subtitle_label.grid(
            row=1,
            column=0,
            padx=40,
            pady=(0, 25)
        )

        # =====================================================
        # USERNAME
        # =====================================================

        self.username_entry = ctk.CTkEntry(
            self.login_card,
            placeholder_text="Username",
            width=300,
            height=42,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            corner_radius=SIZES["corner_radius"]
        )

        self.username_entry.grid(
            row=2,
            column=0,
            padx=40,
            pady=8
        )

        # =====================================================
        # PASSWORD
        # =====================================================

        self.password_entry = ctk.CTkEntry(
            self.login_card,
            placeholder_text="Password",
            show="*",
            width=300,
            height=42,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            corner_radius=SIZES["corner_radius"]
        )

        self.password_entry.grid(
            row=3,
            column=0,
            padx=40,
            pady=8
        )

        # =====================================================
        # LOGIN BUTTON
        # =====================================================

        self.login_button = ctk.CTkButton(
            self.login_card,
            text="Login",
            command=self.login,
            width=300,
            height=42,
            corner_radius=SIZES["corner_radius"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        self.login_button.grid(
            row=4,
            column=0,
            padx=40,
            pady=(20, 10)
        )

        # =====================================================
        # ERROR MESSAGE
        # =====================================================

        self.error_label = ctk.CTkLabel(
            self.login_card,
            text="",
            font=ctk.CTkFont(
                size=SIZES["small_size"]
            ),
            text_color=COLORS["danger"]
        )

        self.error_label.grid(
            row=5,
            column=0,
            padx=40,
            pady=(5, 20)
        )

        # =====================================================
        # ENTER KEY
        # =====================================================

        self.master.bind(
            "<Return>",
            lambda event: self.login()
        )

        # Put cursor in username field
        self.username_entry.focus()

    # =========================================================
    # LOGIN
    # =========================================================

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        # -----------------------------------------------------
        # VALIDATION
        # -----------------------------------------------------

        if not username or not password:

            self.error_label.configure(
                text="Please enter both username and password",
                text_color=COLORS["danger"]
            )

            return

        # Clear previous error
        self.error_label.configure(
            text=""
        )

        conn = None

        try:

            conn = sqlite3.connect(
                DB_NAME
            )

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    username,
                    password,
                    role,
                    is_active
                FROM users
                WHERE username = ?
                """,
                (username,)
            )

            user = cursor.fetchone()

            if user:

                (
                    user_id,
                    db_username,
                    db_password,
                    role,
                    is_active
                ) = user

                # -------------------------------------------------
                # ACCOUNT DEACTIVATED
                # -------------------------------------------------

                if not is_active:

                    self.error_label.configure(
                        text="Account is deactivated",
                        text_color=COLORS["warning"]
                    )

                    return

                # -------------------------------------------------
                # PASSWORD CHECK
                # -------------------------------------------------

                if bcrypt.checkpw(
                    password.encode("utf-8"),
                    db_password.encode("utf-8")
                ):

                    user_data = {
                        "id": user_id,
                        "username": db_username,
                        "role": role
                    }

                    self.master.unbind(
                        "<Return>"
                    )

                    self.on_login_success(
                        user_data
                    )

                else:

                    self.error_label.configure(
                        text="Invalid credentials",
                        text_color=COLORS["danger"]
                    )

            else:

                self.error_label.configure(
                    text="Invalid credentials",
                    text_color=COLORS["danger"]
                )

        except Exception as e:

            self.error_label.configure(
                text=f"Database error: {e}",
                text_color=COLORS["danger"]
            )

        finally:

            if conn:
                conn.close()
