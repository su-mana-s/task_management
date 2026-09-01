
import customtkinter as ctk
from datetime import datetime

from database import get_connection
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
        any completed task.

        The person who completed the work does NOT have to
        be the person who dispatches it.

    DATABASE:
        tasks.id                    = Task ID
        tasks.task_name             = Task Name
        tasks.client_id             = Client
        tasks.status                = Workflow status
        tasks.completed_by          = User who completed work
        tasks.date_of_completion    = Completion date
        tasks.date_of_despatch      = Dispatch date
        tasks.dispatch_at           = Dispatch timestamp
        tasks.dispatched_by         = User who dispatched
        tasks.how_despatched        = Dispatch method

        documents.task_id           = Related task
        documents.nature_of_papers  = Documents/papers received

        activity_log.task_id        = Related task
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
        # Database receives a Python date object.

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
        # LOAD AVAILABLE TASKS
        # =========================================================

        self.load_completed_cases()


    # =============================================================
    # LOAD COMPLETED TASKS
    #
    # NEW DATABASE:
    #
    # tasks replaces records.
    #
    # tasks.id replaces inward_id.
    #
    # task_name is now displayed.
    #
    # nature_of_papers is stored in documents, not tasks.
    #
    # Because one task can have multiple documents, STRING_AGG()
    # is used so the same task appears only once.
    # =============================================================

    def load_completed_cases(self):

        conn = None
        cursor = None

        try:

            conn = get_connection()
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
                    u.username

                FROM tasks t

                JOIN clients c
                    ON t.client_id = c.id

                LEFT JOIN users u
                    ON t.completed_by = u.id

                LEFT JOIN documents d
                    ON d.task_id = t.id

                WHERE t.status = 1

                GROUP BY
                    t.id,
                    t.task_name,
                    c.name,
                    u.username

                ORDER BY t.id DESC
            """)

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
        self.completed_by_map = {}

        for (
            task_id,
            task_name,
            client_name,
            nature,
            completed_by
        ) in cases:

            display = (
                f"ID: {task_id} | "
                f"Task: {task_name} | "
                f"Client: {client_name} | "
                f"Papers: {nature} | "
                f"Completed By: {completed_by or '-'}"
            )

            self.case_map[display] = task_id

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

        task_id = self.case_map.get(
            selected
        )

        if not task_id:

            messagebox.showerror(
                "Error",
                "Invalid task selected."
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
                "Please select how the task was dispatched."
            )

            return

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            # =====================================================
            # DATABASE DATE
            #
            # PostgreSQL tasks.date_of_despatch is DATE.
            #
            # Passing a Python date object is preferable to
            # manually converting it to a string.
            # =====================================================

            dispatch_date = (
                datetime.now().date()
            )

            dispatch_timestamp = datetime.now()

            # =====================================================
            # UPDATE DISPATCH
            #
            # IMPORTANT:
            #
            # There is intentionally NO:
            #
            #     AND assigned_to = %s
            #
            # because anybody with access to Dispatch can dispatch
            # completed work.
            #
            # The status condition prevents two users from
            # dispatching the same task simultaneously.
            # =====================================================

            cursor.execute("""
                UPDATE tasks

                SET
                    status = 2,
                    date_of_despatch = %s,
                    how_despatched = %s,
                    dispatched_by = %s,
                    dispatch_at = %s,
                    updated_at = CURRENT_TIMESTAMP

                WHERE id = %s
                  AND status = 1
            """, (
                dispatch_date,
                despatch_method,
                self.user["id"],
                dispatch_timestamp,
                task_id
            ))

            if cursor.rowcount == 0:

                conn.rollback()

                messagebox.showerror(
                    "Error",
                    "This task is no longer available for dispatch."
                )

                self.load_completed_cases()

                return

            # =====================================================
            # AUDIT LOG
            #
            # NEW DATABASE:
            #
            # activity_log.task_id
            #
            # There is no record_id column anymore.
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
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """, (
                task_id,
                "DISPATCHED",
                self.user["id"],
                dispatch_timestamp,
                (
                    f"Dispatched by "
                    f"{self.user['username']} "
                    f"via {despatch_method}"
                )
            ))

            # =====================================================
            # COMMIT
            # =====================================================

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Task dispatched successfully."
            )

            # =====================================================
            # RELOAD COMPLETED TASKS
            #
            # The dispatched task has status = 2, so it will
            # automatically disappear from this list.
            # =====================================================

            self.load_completed_cases()

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
