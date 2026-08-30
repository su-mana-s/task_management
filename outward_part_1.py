
import customtkinter as ctk
import sqlite3

from datetime import datetime

from tkinter import messagebox

from database import DB_NAME

from theme import *

from searchable_combobox import SearchableComboBox


class OutwardPart1Menu(ctk.CTkFrame):

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
            text="Work Done",
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

        self.form_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS["card"],
            corner_radius=SIZES["large_corner_radius"]
        )

        self.form_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =========================================================
        # SELECT PENDING / IN-PROGRESS CASE
        # =========================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Select Case:",
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

            command=self.load_pending_cases
        )

        self.case_dropdown.grid(
            row=0,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =========================================================
        # DATE OF COMPLETION
        # =========================================================

        # Display format:
        # DD-MM-YYYY
        #
        # Database format remains:
        # YYYY-MM-DD

        self.completion_date = (
            datetime.now().strftime("%d-%m-%Y")
        )

        ctk.CTkLabel(
            self.form_frame,
            text=f"Date of Completion: {self.completion_date}",
            font=ctk.CTkFont(
                size=SIZES["label_size"],
                weight="bold"
            ),
            text_color=COLORS["primary"]
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =========================================================
        # DETAILS
        # =========================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Details of Work Done:",
            font=ctk.CTkFont(
                size=SIZES["label_size"],
                weight="bold"
            ),
            text_color=COLORS["text"]
        ).grid(
            row=2,
            column=0,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="nw"
        )

        self.work_details = ctk.CTkTextbox(
            self.form_frame,
            width=500,
            height=150,
            font=ctk.CTkFont(
                size=SIZES["normal_size"]
            ),
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            border_width=3,
            text_color=COLORS["text"],
            corner_radius=SIZES["corner_radius"]
        )

        self.work_details.grid(
            row=2,
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
            text="Mark Work Done",
            command=self.submit_work,
            width=SIZES["button_width"],
            height=SIZES["button_height"],
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            fg_color=LOGOUT,
            hover_color=LOGOUT_HOVER,
            text_color=COLORS["toggle"],
            corner_radius=SIZES["corner_radius"]
        )

        self.submit_btn.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=30
        )

        # =========================================================
        # LOAD CASES
        # =========================================================

        self.load_pending_cases()


    # =============================================================
    # LOAD CASES AVAILABLE FOR COMPLETION
    #
    # STATUS 0  = Not Started
    # STATUS 10 = In Progress
    #
    # Both are allowed to move to Completed.
    # =============================================================

    def load_pending_cases(self):

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            # -----------------------------------------------------
            # ADMIN CAN SEE ALL UNCOMPLETED / UNDISPATCHED WORK
            # -----------------------------------------------------

            if self.user["role"] == "Admin":

                cursor.execute("""
                    SELECT
                        r.inward_id,
                        c.name,
                        r.nature_of_papers,
                        u.username,
                        r.status

                    FROM records r

                    JOIN clients c
                        ON r.client_id = c.id

                    LEFT JOIN users u
                        ON r.assigned_to = u.id

                    WHERE r.status IN (0, 10)

                    ORDER BY r.inward_id DESC
                """)

            # -----------------------------------------------------
            # EMPLOYEE CAN SEE ONLY THEIR OWN WORK
            # -----------------------------------------------------

            else:

                cursor.execute("""
                    SELECT
                        r.inward_id,
                        c.name,
                        r.nature_of_papers,
                        u.username,
                        r.status

                    FROM records r

                    JOIN clients c
                        ON r.client_id = c.id

                    LEFT JOIN users u
                        ON r.assigned_to = u.id

                    WHERE r.status IN (0, 10)

                      AND r.assigned_to = ?

                    ORDER BY r.inward_id DESC
                """, (
                    self.user["id"],
                ))

            cases = cursor.fetchall()

        finally:

            conn.close()

        # =========================================================
        # BUILD DROPDOWN
        # =========================================================

        self.case_map = {}

        for (
            rid,
            client_name,
            nature,
            assigned_to,
            status
        ) in cases:

            status_text = self.status_to_text(status)

            display = (
                f"ID: {rid} | "
                f"{client_name} | "
                f"{nature} | "
                f"Status: {status_text} | "
                f"Assigned: {assigned_to or '-'}"
            )

            self.case_map[display] = rid

        display_values = list(
            self.case_map.keys()
        )

        if display_values:

            self.case_dropdown.configure_values(
                values=display_values
            )

            self.case_dropdown.set(
                display_values[0]
            )

            self.submit_btn.configure(
                state="normal"
            )

        else:

            self.case_dropdown.configure_values(
                values=["No pending cases found"]
            )

            self.case_dropdown.set(
                "No pending cases found"
            )

            self.submit_btn.configure(
                state="disabled"
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
    # MARK WORK DONE
    # =============================================================

    def submit_work(self):

        selected = self.case_var.get()

        if (
            selected == "No pending cases found"
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

        details = (
            self.work_details
            .get("1.0", "end-1c")
            .strip()
        )

        if not details:

            messagebox.showerror(
                "Error",
                "Please enter details of work done."
            )

            return

        # ---------------------------------------------------------
        # DATABASE DATE
        # ---------------------------------------------------------
        #
        # Keep database storage as YYYY-MM-DD.
        #
        # The date displayed to the user above is DD-MM-YYYY,
        # but the database continues using YYYY-MM-DD.
        # ---------------------------------------------------------

        completion_date = (
            datetime.now().strftime("%Y-%m-%d")
        )

        conn = None

        try:

            conn = sqlite3.connect(DB_NAME)

            # Important for this transaction
            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            # =====================================================
            # COMPLETE THE RECORD
            #
            # IMPORTANT:
            #
            # status can be:
            #
            # 0  = Not Started
            # 10 = In Progress
            #
            # Either can become 1 = Completed.
            #
            # The WHERE condition prevents another user from
            # completing an already completed/dispatched record.
            # =====================================================

            cursor.execute("""
                UPDATE records

                SET
                    status = 1,
                    date_of_completion = ?,
                    details_of_work_done = ?,
                    completed_by = ?

                WHERE inward_id = ?

                  AND status IN (0, 10)
            """, (
                completion_date,
                details,
                self.user["id"],
                record_id
            ))

            if cursor.rowcount == 0:

                conn.rollback()

                messagebox.showerror(
                    "Error",
                    (
                        "This record is no longer available "
                        "for completion."
                    )
                )

                self.load_pending_cases()

                return

            # =====================================================
            # SAVE FINAL WORK UPDATE
            #
            # This is history only.
            #
            # There is intentionally NO status column.
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
                record_id,
                self.user["id"],
                completion_date,
                details
            ))

            # =====================================================
            # AUDIT LOG
            # =====================================================

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
                record_id,
                "WORK_COMPLETED",
                self.user["id"],
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                details
            ))

            # =====================================================
            # COMMIT
            # =====================================================

            conn.commit()

            messagebox.showinfo(
                "Success",
                (
                    "Work marked as done.\n\n"
                    "The record is now immediately available "
                    "for Billing and Dispatch."
                )
            )

            # Clear form

            self.work_details.delete(
                "1.0",
                "end"
            )

            self.load_pending_cases()

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
