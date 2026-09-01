
import customtkinter as ctk
from database import get_connection
from datetime import datetime

from tkinter import messagebox

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
        # SELECT PENDING / IN-PROGRESS TASK
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
    #
    # NEW DATABASE:
    #
    # tasks.id          = task ID
    # tasks.task_name   = task name
    # documents         = document receipts
    #
    # We use STRING_AGG to display the document/paper nature
    # without creating duplicate task entries.
    # =============================================================

    def load_pending_cases(self):

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            # -----------------------------------------------------
            # ADMIN CAN SEE ALL UNCOMPLETED / ACTIVE TASKS
            # -----------------------------------------------------

            if self.user["role"] == "Admin":

                cursor.execute("""
                    SELECT
                        t.id,
                        t.task_name,
                        c.name,
                        COALESCE(
                            STRING_AGG(
                                DISTINCT d.nature_of_papers,
                                ', '
                            ),
                            '-'
                        ) AS nature_of_papers,
                        u.username,
                        t.status

                    FROM tasks t

                    JOIN clients c
                        ON t.client_id = c.id

                    LEFT JOIN users u
                        ON t.assigned_to = u.id

                    LEFT JOIN documents d
                        ON d.task_id = t.id

                    WHERE t.status IN (0, 10)

                    GROUP BY
                        t.id,
                        t.task_name,
                        c.name,
                        u.username,
                        t.status

                    ORDER BY t.id DESC
                """)

            # -----------------------------------------------------
            # EMPLOYEE CAN SEE ONLY THEIR OWN ACTIVE TASKS
            # -----------------------------------------------------

            else:

                cursor.execute("""
                    SELECT
                        t.id,
                        t.task_name,
                        c.name,
                        COALESCE(
                            STRING_AGG(
                                DISTINCT d.nature_of_papers,
                                ', '
                            ),
                            '-'
                        ) AS nature_of_papers,
                        u.username,
                        t.status

                    FROM tasks t

                    JOIN clients c
                        ON t.client_id = c.id

                    LEFT JOIN users u
                        ON t.assigned_to = u.id

                    LEFT JOIN documents d
                        ON d.task_id = t.id

                    WHERE t.status IN (0, 10)

                      AND t.assigned_to = %s

                    GROUP BY
                        t.id,
                        t.task_name,
                        c.name,
                        u.username,
                        t.status

                    ORDER BY t.id DESC
                """, (
                    self.user["id"],
                ))

            cases = cursor.fetchall()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            cases = []

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        # =========================================================
        # BUILD DROPDOWN
        # =========================================================

        self.case_map = {}

        for (
            task_id,
            task_name,
            client_name,
            nature,
            assigned_to,
            status
        ) in cases:

            status_text = self.status_to_text(
                status
            )

            # -----------------------------------------------------
            # TASK NAME IS NOW INCLUDED PROMINENTLY IN THE SEARCH
            # -----------------------------------------------------

            display = (
                f"ID: {task_id} | "
                f"Task: {task_name} | "
                f"Client: {client_name} | "
                f"Papers: {nature} | "
                f"Status: {status_text} | "
                f"Assigned: {assigned_to or '-'}"
            )

            self.case_map[display] = task_id

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

        task_id = self.case_map.get(
            selected
        )

        if not task_id:

            messagebox.showerror(
                "Error",
                "Invalid task selected."
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

        completion_date = (
            datetime.now().date()
        )

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            # =====================================================
            # COMPLETE THE TASK
            #
            # IMPORTANT:
            #
            # status:
            #
            # 0  = Not Started
            # 10 = In Progress
            #
            # Either can become:
            #
            # 1  = Completed
            #
            # The WHERE condition prevents another user from
            # completing an already completed/dispatched task.
            # =====================================================

            cursor.execute("""
                UPDATE tasks

                SET
                    status = 1,
                    date_of_completion = %s,
                    details_of_work_done = %s,
                    completed_by = %s,
                    updated_at = CURRENT_TIMESTAMP

                WHERE id = %s

                  AND status IN (0, 10)
            """, (
                completion_date,
                details,
                self.user["id"],
                task_id
            ))

            if cursor.rowcount == 0:

                conn.rollback()

                messagebox.showerror(
                    "Error",
                    (
                        "This task is no longer available "
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
            #
            # NEW DATABASE:
            # task_updates.task_id
            # =====================================================

            cursor.execute("""
                INSERT INTO task_updates
                (
                    task_id,
                    updated_by,
                    update_date,
                    description
                )
                VALUES (%s, %s, %s, %s)
            """, (
                task_id,
                self.user["id"],
                datetime.now(),
                details
            ))

            # =====================================================
            # AUDIT LOG
            #
            # NEW DATABASE:
            # activity_log.task_id
            #
            # action_type = WORK_COMPLETED
            # =====================================================

            cursor.execute("""
                INSERT INTO activity_log
                (
                    task_id,
                    action_type,
                    performed_by,
                    action_date,
                    description
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (
                task_id,
                "WORK_COMPLETED",
                self.user["id"],
                datetime.now(),
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
                    "The task is now immediately available "
                    "for Billing and Dispatch."
                )
            )

            # =====================================================
            # CLEAR FORM
            # =====================================================

            self.work_details.delete(
                "1.0",
                "end"
            )

            # =====================================================
            # RELOAD ACTIVE TASKS
            # =====================================================

            self.load_pending_cases()

        except Exception as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)

            )

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()
