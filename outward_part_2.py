
import customtkinter as ctk
import sqlite3
from datetime import datetime
from database import DB_NAME
from searchable_combobox import SearchableComboBox
from tkinter import messagebox

from theme import (
    COLORS,
    SIZES,
    PADDING,
    PRIMARY,
    PRIMARY_HOVER,
    TEXT_LIGHT,
    SIDEBAR_HOVER
)


class OutwardPart2Menu(ctk.CTkFrame):
    """
    Outward Part 2 - Dispatch

    Workflow:

        Work Done (status = 1)
                |
                +--------------------+
                |                    |
                v                    v
             Billing             Dispatch
                                  |
                                  v
                            status = 2

    IMPORTANT:
        Any user who has access to this screen can dispatch
        any completed work.

        The person who completed the work does NOT have to
        be the person who dispatches it.
    """

    def __init__(self, master, user):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.user = user

        # =========================================================
        # TITLE
        # =========================================================

        self.title_label = ctk.CTkLabel(
            self,
            text="Dispatch",
            font=ctk.CTkFont(
                size=SIZES["title_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        )

        self.title_label.pack(
            pady=(0, 20),
            anchor="w"
        )

        # =========================================================
        # MAIN FORM
        # =========================================================

        self.form_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS["card"],
            corner_radius=SIZES["large_corner_radius"],
            scrollbar_button_color=SIDEBAR_HOVER,
            scrollbar_button_hover_color=PRIMARY_HOVER
        )

        self.form_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =========================================================
        # SELECT COMPLETED TASK
        # =========================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Select Completed Task:",
            font=ctk.CTkFont(
                size=SIZES["label_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        self.case_var = ctk.StringVar(
            value=""
        )

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
            corner_radius=SIZES["corner_radius"],

            command=self.case_selected
        )

        self.case_dropdown.grid(
            row=0,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =========================================================
        # SHOW WHO COMPLETED THE WORK
        # =========================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Completed By:",
            font=ctk.CTkFont(
                size=SIZES["label_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=1,
            column=0,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        self.completed_by_label = ctk.CTkLabel(
            self.form_frame,
            text="-",
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            text_color=COLORS["text_secondary"]
        )

        self.completed_by_label.grid(
            row=1,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =========================================================
        # DISPATCH DATE
        # =========================================================

        # Display format:
        # DD-MM-YYYY
        #
        # Database format remains:
        # YYYY-MM-DD

        self.despatch_date = (
            datetime.now().strftime("%d-%m-%Y")
        )

        ctk.CTkLabel(
            self.form_frame,
            text=f"Date of Dispatch: {self.despatch_date}",
            font=ctk.CTkFont(
                size=SIZES["label_size"],
                weight="bold"
            ),
            text_color=COLORS["primary"]
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =========================================================
        # DISPATCHED BY
        # =========================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Dispatching User:",
            font=ctk.CTkFont(
                size=SIZES["label_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=3,
            column=0,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        self.dispatching_user_label = ctk.CTkLabel(
            self.form_frame,
            text=self.user["username"],
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            text_color=PRIMARY
        )

        self.dispatching_user_label.grid(
            row=3,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =========================================================
        # HOW DISPATCHED
        # =========================================================

        ctk.CTkLabel(
            self.form_frame,
            text="How Dispatched:",
            font=ctk.CTkFont(
                size=SIZES["label_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=4,
            column=0,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        methods = [
            "courier",
            "speed post",
            "hand delivery at office"
        ]

        self.despatch_method_var = ctk.StringVar(
            value=methods[0]
        )

        self.despatch_method_dropdown = ctk.CTkComboBox(
            self.form_frame,
            variable=self.despatch_method_var,
            values=methods,
            width=300,
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
            text_color=COLORS["text"],
            button_color=SIDEBAR_HOVER,
            button_hover_color=PRIMARY_HOVER,
            dropdown_fg_color=COLORS["card"],
            dropdown_hover_color=SIDEBAR_HOVER,
            dropdown_text_color=COLORS["text"],
            corner_radius=SIZES["corner_radius"]
        )

        self.despatch_method_dropdown.grid(
            row=4,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =========================================================
        # SUBMIT
        # =========================================================

        self.submit_btn = ctk.CTkButton(
            self.form_frame,
            text="Mark as Dispatched",
            command=self.submit_dispatch,
            width=SIZES["button_width"],
            height=SIZES["button_height"],
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            fg_color=PRIMARY,
            hover_color=PRIMARY_HOVER,
            text_color=TEXT_LIGHT,
            corner_radius=SIZES["corner_radius"]
        )

        self.submit_btn.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=30
        )

        # =========================================================
        # LOAD AVAILABLE CASES
        # =========================================================

        self.load_completed_cases()

    # =============================================================
    # LOAD COMPLETED CASES
    # =============================================================

    def load_completed_cases(self):

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            # =====================================================
            # IMPORTANT:
            #
            # There is NO assigned_to restriction here.
            #
            # Anyone with access to Dispatch can dispatch
            # anybody's completed work.
            # =====================================================

            cursor.execute("""
                SELECT
                    r.inward_id,
                    c.name,
                    r.nature_of_papers,
                    u.username
                FROM records r

                JOIN clients c
                    ON r.client_id = c.id

                LEFT JOIN users u
                    ON r.completed_by = u.id

                WHERE r.status = 1

                ORDER BY r.inward_id DESC
            """)

            cases = cursor.fetchall()

        finally:

            conn.close()

        # =========================================================
        # BUILD DROPDOWN
        # =========================================================

        self.case_map = {}
        self.completed_by_map = {}

        for (
            record_id,
            client_name,
            nature,
            completed_by
        ) in cases:

            display = (
                f"ID: {record_id} | "
                f"{client_name} | "
                f"{nature} | "
                f"Completed By: {completed_by or '-'}"
            )

            self.case_map[display] = record_id

            self.completed_by_map[display] = (
                completed_by or "-"
            )

        display_values = list(
            self.case_map.keys()
        )

        if display_values:

            self.case_dropdown.configure_values(
                display_values
            )

            self.case_dropdown.set(
                display_values[0]
            )

            self.submit_btn.configure(
                state="normal"
            )

            self.case_selected(
                display_values[0]
            )

        else:

            self.case_dropdown.configure_values(
                [
                    "No cases ready for dispatch"
                ]
            )

            self.case_dropdown.set(
                "No cases ready for dispatch"
            )

            self.completed_by_label.configure(
                text="-"
            )

            self.submit_btn.configure(
                state="disabled"
            )

    # =============================================================
    # SELECTION CHANGED
    # =============================================================

    def case_selected(self, choice=None):

        if choice is None:
            choice = self.case_var.get()

        completed_by = (
            self.completed_by_map.get(
                choice,
                "-"
            )
        )

        self.completed_by_label.configure(
            text=completed_by
        )

    # =============================================================
    # DISPATCH
    # =============================================================

    def submit_dispatch(self):

        selected = self.case_var.get()

        if (
            selected == "No cases ready for dispatch"
            or not selected
        ):
            return

        record_id = self.case_map.get(
            selected
        )

        if not record_id:

            messagebox.showerror(
                "Error",
                "Invalid record selected."
            )

            return

        despatch_method = (
            self.despatch_method_var
            .get()
            .strip()
        )

        if not despatch_method:

            messagebox.showerror(
                "Error",
                "Please select how the record was dispatched."
            )

            return

        conn = None

        try:

            conn = sqlite3.connect(DB_NAME)

            cursor = conn.cursor()

            # =====================================================
            # DATABASE DATE
            #
            # IMPORTANT:
            # self.despatch_date is displayed as DD-MM-YYYY,
            # but the database must continue to receive
            # YYYY-MM-DD.
            # =====================================================

            database_dispatch_date = datetime.strptime(
                self.despatch_date,
                "%d-%m-%Y"
            ).strftime(
                "%Y-%m-%d"
            )

            # =====================================================
            # UPDATE DISPATCH
            #
            # There is intentionally NO:
            #
            #     AND assigned_to = ?
            #
            # because anybody can dispatch completed work.
            # =====================================================

            cursor.execute("""
                UPDATE records

                SET
                    status = 2,
                    date_of_despatch = ?,
                    how_despatched = ?,
                    dispatched_by = ?,
                    dispatch_at = ?

                WHERE inward_id = ?
                  AND status = 1
            """, (
                database_dispatch_date,
                despatch_method,
                self.user["id"],
                datetime.now().isoformat(
                    timespec="seconds"
                ),
                record_id
            ))

            if cursor.rowcount == 0:

                conn.rollback()

                messagebox.showerror(
                    "Error",
                    "This record is no longer available for dispatch."
                )

                self.load_completed_cases()

                return

            # =====================================================
            # AUDIT LOG
            # =====================================================

            cursor.execute("""
                INSERT INTO activity_log (
                    record_id,
                    action_type,
                    performed_by,
                    action_date,
                    description
                )
                VALUES (
                    ?,
                    'DISPATCHED',
                    ?,
                    ?,
                    ?
                )
            """, (
                record_id,
                self.user["id"],
                datetime.now().isoformat(
                    timespec="seconds"
                ),
                f"Dispatched by {self.user['username']} "
                f"via {despatch_method}"
            ))

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Record dispatched successfully."
            )

            self.load_completed_cases()

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
