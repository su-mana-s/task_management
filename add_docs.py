import customtkinter as ctk
from searchable_combobox import SearchableComboBox
from database import get_connection
from tkinter import messagebox
from datetime import datetime

from theme import *


class AddDocuments(ctk.CTkFrame):

    def __init__(self, master, user):

        super().__init__(
            master,
            fg_color=COLORS["background"]
        )

        self.user = user

        self.selected_task_id = None

        self.tasks = []

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
            text="Add Documents",
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
        # MAIN CONTAINER
        # =====================================================

        self.main_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS["card"],
            corner_radius=SIZES["large_corner_radius"]
        )

        self.main_frame.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 20),
            sticky="nsew"
        )

        self.main_frame.grid_columnconfigure(
            0,
            minsize=230
        )

        self.main_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.create_form()

        self.load_tasks()

    # =========================================================
    # LABEL
    # =========================================================

    def create_label(self, text, row):

        label = ctk.CTkLabel(
            self.main_frame,
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
            self.main_frame,
            width=SIZES["textbox_width"],
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
    # FORM
    # =========================================================

    def create_form(self):

        # =====================================================
        # TASK
        # =====================================================

        self.create_label(
            "Active Task:",
            0
        )

        self.task_var = ctk.StringVar(
            value=""
        )

        self.task_dropdown = SearchableComboBox(
            self.main_frame,

            values=[],

            variable=self.task_var,

            command=self.on_task_selected,

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

        self.task_dropdown.grid(
            row=0,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # SELECTED TASK INFO
        # =====================================================

        self.task_info_label = ctk.CTkLabel(
            self.main_frame,

            text="Select a task to view its document history.",

            font=ctk.CTkFont(
                size=SIZES["normal_size"]
            ),

            text_color=COLORS["placeholder"]
        )

        self.task_info_label.grid(
            row=1,
            column=1,
            padx=PADDING["x"],
            pady=(0, 15),
            sticky="w"
        )

        # =====================================================
        # NATURE OF PAPERS
        # =====================================================

        self.create_label(
            "Nature of Papers:",
            2
        )

        self.nature_entry = self.create_entry(
            "Describe the documents/papers received"
        )

        self.nature_entry.grid(
            row=2,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # DOCUMENT DETAILS
        # =====================================================

        self.create_label(
            "Document Details:",
            3
        )

        self.details_entry = self.create_entry(
            "Optional additional details"
        )

        self.details_entry.grid(
            row=3,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # HOW RECEIVED
        # =====================================================

        self.create_label(
            "How Received:",
            4
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

        self.received_dropdown = ctk.CTkComboBox(
            self.main_frame,

            variable=self.received_var,

            values=methods,

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

        self.received_dropdown.grid(
            row=4,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # RECEIVED AT
        # =====================================================

        self.create_label(
            "Date & Time Received:",
            5
        )

        self.received_at_entry = self.create_entry(
            "DD-MM-YYYY HH:MM"
        )

        self.received_at_entry.grid(
            row=5,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        self.set_current_datetime()

        # =====================================================
        # RECEIVED BY
        # =====================================================

        self.create_label(
            "Received By:",
            6
        )

        self.received_by_label = ctk.CTkLabel(
            self.main_frame,

            text=self.user["username"],

            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),

            text_color=COLORS["text"]
        )

        self.received_by_label.grid(
            row=6,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # ADD BUTTON
        # =====================================================

        self.add_btn = ctk.CTkButton(
            self.main_frame,

            text="✓  Add Document",

            command=self.add_document,

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

        self.add_btn.grid(
            row=7,
            column=0,
            columnspan=2,
            padx=PADDING["x"],
            pady=(20, 30)
        )

        # =====================================================
        # HISTORY HEADER
        # =====================================================

        self.history_separator = ctk.CTkFrame(
            self.main_frame,
            height=2,
            fg_color=COLORS["border"]
        )

        self.history_separator.grid(
            row=8,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=PADDING["x"],
            pady=(10, 20)
        )

        self.history_title = ctk.CTkLabel(
            self.main_frame,

            text="Document History",

            font=ctk.CTkFont(
                size=SIZES["heading_size"],
                weight="bold"
            ),

            text_color=COLORS["text"]
        )

        self.history_title.grid(
            row=9,
            column=0,
            columnspan=2,
            padx=PADDING["x"],
            pady=(0, 15),
            sticky="w"
        )

        # =====================================================
        # HISTORY FRAME
        # =====================================================

        self.history_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color=COLORS["background"],
            corner_radius=SIZES["corner_radius"],
            height=300
        )

        self.history_frame.grid(
            row=10,
            column=0,
            columnspan=2,
            padx=PADDING["x"],
            pady=(0, 30),
            sticky="ew"
        )

        self.history_frame.grid_columnconfigure(
            0,
            weight=1
        )

    # =========================================================
    # LOAD ACTIVE TASKS
    # =========================================================

    def load_tasks(self):

        conn = get_connection()
        cursor = None

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    t.id,
                    t.task_name,
                    t.task_details,
                    t.department,
                    c.name AS client_name,
                    u.username AS assigned_to,
                    t.status
                FROM tasks t

                JOIN clients c
                    ON c.id = t.client_id

                LEFT JOIN users u
                    ON u.id = t.assigned_to

                WHERE t.status IN (0, 10)

                ORDER BY
                    c.name,
                    t.task_name
            """)

            rows = cursor.fetchall()

            self.tasks = []

            values = []

            for (
                task_id,
                task_name,
                task_details,
                department,
                client_name,
                assigned_to,
                status
            ) in rows:

                status_text = (
                    "Not Started"
                    if status == 0
                    else "In Progress"
                )

                display = (
                    f"{task_name} — "
                    f"{client_name} — "
                    f"{department} — "
                    f"{status_text}"
                )

                self.tasks.append({
                    "id": task_id,
                    "task_name": task_name,
                    "task_details": task_details,
                    "department": department,
                    "client_name": client_name,
                    "assigned_to": assigned_to,
                    "status": status,
                    "display": display
                })

                values.append(
                    display
                )

            self.task_dropdown.configure_values(
                values
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not load active tasks:\n{e}"
            )

        finally:

            if cursor:
                cursor.close()

            conn.close()

    # =========================================================
    # TASK SELECTED
    # =========================================================

    def on_task_selected(self, selected_value):

        selected_task = next(
            (
                task
                for task in self.tasks
                if task["display"] == selected_value
            ),
            None
        )

        if not selected_task:

            self.selected_task_id = None

            return

        self.selected_task_id = selected_task["id"]

        assigned_to = (
            selected_task["assigned_to"]
            or "Unassigned"
        )

        status_text = (
            "Not Started"
            if selected_task["status"] == 0
            else "In Progress"
        )

        self.task_info_label.configure(
            text=(
                f"Client: {selected_task['client_name']}   |   "
                f"Department: {selected_task['department']}   |   "
                f"Assigned To: {assigned_to}   |   "
                f"Status: {status_text}"
            )
        )

        self.load_document_history()

    # =========================================================
    # CURRENT DATE/TIME
    # =========================================================

    def set_current_datetime(self):

        self.received_at_entry.delete(
            0,
            "end"
        )

        self.received_at_entry.insert(
            0,
            datetime.now().strftime(
                "%d-%m-%Y %H:%M"
            )
        )

    # =========================================================
    # ADD DOCUMENT
    # =========================================================

    def add_document(self):

        # =====================================================
        # VALIDATE TASK
        # =====================================================

        if self.selected_task_id is None:

            messagebox.showerror(
                "No Task Selected",
                "Please select an active task."
            )

            return

        # =====================================================
        # GET VALUES
        # =====================================================

        nature = (
            self.nature_entry
            .get()
            .strip()
        )

        details = (
            self.details_entry
            .get()
            .strip()
        )

        how_received = (
            self.received_var
            .get()
            .strip()
        )

        received_at_text = (
            self.received_at_entry
            .get()
            .strip()
        )

        # =====================================================
        # VALIDATE DOCUMENT
        # =====================================================

        if not nature:

            messagebox.showerror(
                "Missing Information",
                "Please enter the nature of papers."
            )

            return

        if not how_received:

            messagebox.showerror(
                "Missing Information",
                "Please select how the document was received."
            )

            return

        # =====================================================
        # PARSE DATETIME
        # =====================================================

        try:

            received_at = datetime.strptime(
                received_at_text,
                "%d-%m-%Y %H:%M"
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Date/Time",
                "Please use DD-MM-YYYY HH:MM format."
            )

            return

        # =====================================================
        # DATABASE
        # =====================================================

        conn = None
        cursor = None

        try:

            conn = get_connection()

            cursor = conn.cursor()

            # =================================================
            # VERIFY TASK IS STILL ACTIVE
            # =================================================

            cursor.execute("""
                SELECT
                    task_name,
                    status
                FROM tasks
                WHERE id = %s
            """, (
                self.selected_task_id,
            ))

            task_row = cursor.fetchone()

            if not task_row:

                messagebox.showerror(
                    "Task Not Found",
                    "The selected task no longer exists."
                )

                return

            task_name, status = task_row

            if status not in (0, 10):

                messagebox.showerror(
                    "Task No Longer Active",
                    "This task has already been completed or dispatched."
                )

                self.load_tasks()

                return

            # =================================================
            # INSERT DOCUMENT
            #
            # PostgreSQL interprets the naive datetime as
            # connection timezone. To make this explicitly IST,
            # use AT TIME ZONE during insertion.
            # =================================================

            cursor.execute("""
                INSERT INTO documents (
                    task_id,
                    nature_of_papers,
                    document_details,
                    how_received,
                    received_at,
                    received_by
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s AT TIME ZONE 'Asia/Kolkata',
                    %s
                )
                RETURNING id
            """, (
                self.selected_task_id,
                nature,
                details,
                how_received,
                received_at,
                self.user["id"]
            ))

            document_id = cursor.fetchone()[0]

            # =================================================
            # ACTIVITY LOG
            # =================================================

            cursor.execute("""
                INSERT INTO activity_log (
                    task_id,
                    action_type,
                    performed_by,
                    action_date,
                    description
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s AT TIME ZONE 'Asia/Kolkata',
                    %s
                )
            """, (
                self.selected_task_id,
                "DOCUMENT_RECEIVED",
                self.user["id"],
                received_at,
                f"Document received: {nature}"
            ))

            # =================================================
            # OPTIONAL:
            # Automatically move a newly started task to
            # IN PROGRESS when its first document is received.
            #
            # If you don't want this behaviour, remove this
            # section.
            # =================================================

            if status == 0:

                cursor.execute("""
                    UPDATE tasks
                    SET status = 10
                    WHERE id = %s
                      AND status = 0
                """, (
                    self.selected_task_id,
                ))

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
                    self.selected_task_id,
                    "STATUS_CHANGED",
                    self.user["id"],
                    "Task automatically moved to In Progress after document receipt."
                ))

            conn.commit()

            messagebox.showinfo(
                "Success",
                f"Document added successfully.\n\n"
                f"Document ID: {document_id}"
            )

            # =================================================
            # RESET DOCUMENT FIELDS
            # =================================================

            self.nature_entry.delete(
                0,
                "end"
            )

            self.details_entry.delete(
                0,
                "end"
            )

            self.received_var.set(
                "hand delivery"
            )

            self.set_current_datetime()

            # =================================================
            # REFRESH TASK LIST
            # =================================================

            self.load_tasks()

            # Restore selected task if still active
            for task in self.tasks:

                if task["id"] == self.selected_task_id:

                    self.task_var.set(
                        task["display"]
                    )

                    break

            self.load_document_history()

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
    # DOCUMENT HISTORY
    # =========================================================

    def load_document_history(self):

        # Clear previous history

        for widget in self.history_frame.winfo_children():

            widget.destroy()

        if self.selected_task_id is None:

            label = ctk.CTkLabel(
                self.history_frame,
                text="Select a task to view documents.",
                text_color=COLORS["placeholder"]
            )

            label.pack(
                padx=10,
                pady=20
            )

            return

        conn = get_connection()
        cursor = None

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    d.id,
                    d.nature_of_papers,
                    d.document_details,
                    d.how_received,
                    d.received_at,
                    u.username
                FROM documents d

                JOIN users u
                    ON u.id = d.received_by

                WHERE d.task_id = %s

                ORDER BY
                    d.received_at DESC
            """, (
                self.selected_task_id,
            ))

            documents = cursor.fetchall()

            if not documents:

                label = ctk.CTkLabel(
                    self.history_frame,

                    text="No documents have been received for this task yet.",

                    font=ctk.CTkFont(
                        size=SIZES["normal_size"]
                    ),

                    text_color=COLORS["placeholder"]
                )

                label.pack(
                    padx=10,
                    pady=20
                )

                return

            # =================================================
            # HISTORY ITEMS
            # =================================================

            for (
                document_id,
                nature,
                details,
                how_received,
                received_at,
                received_by
            ) in documents:

                card = ctk.CTkFrame(
                    self.history_frame,
                    fg_color=COLORS["card"],
                    corner_radius=SIZES["corner_radius"]
                )

                card.pack(
                    fill="x",
                    padx=5,
                    pady=5
                )

                card.grid_columnconfigure(
                    1,
                    weight=1
                )

                # ---------------------------------------------
                # DOCUMENT NAME
                # ---------------------------------------------

                title = ctk.CTkLabel(
                    card,

                    text=nature,

                    font=ctk.CTkFont(
                        size=20,
                        weight="bold"
                    ),

                    text_color=COLORS["text"]
                )

                title.grid(
                    row=0,
                    column=0,
                    padx=12,
                    pady=(10, 3),
                    sticky="w"
                )

                # ---------------------------------------------
                # DATE
                # ---------------------------------------------

                if received_at:

                    local_time = received_at

                    date_text = local_time.strftime(
                        "%d-%m-%Y %H:%M"
                    )

                else:

                    date_text = "-"

                date_label = ctk.CTkLabel(
                    card,

                    text=date_text,

                    font=ctk.CTkFont(
                        size=SIZES["normal_size"]
                    ),

                    text_color=COLORS["text"]
                )

                date_label.grid(
                    row=0,
                    column=1,
                    padx=12,
                    pady=(10, 3),
                    sticky="e"
                )

                # ---------------------------------------------
                # DETAILS
                # ---------------------------------------------

                info_text = (
                    f"How received: {how_received}"
                    f"    •    "
                    f"Received by: {received_by}"
                )

                if details:

                    info_text += (
                        f"\nDetails: {details}"
                    )

                info_label = ctk.CTkLabel(
                    card,

                    text=info_text,

                    justify="left",

                    font=ctk.CTkFont(
                        size=SIZES["label_size"]
                    ),

                    text_color=COLORS["primary"]
                )

                info_label.grid(
                    row=1,
                    column=0,
                    columnspan=2,
                    padx=12,
                    pady=(3, 10),
                    sticky="w"
                )

        except Exception as e:

            error_label = ctk.CTkLabel(
                self.history_frame,

                text=f"Could not load history:\n{e}",

                text_color=COLORS["text"]
            )

            error_label.pack(
                padx=10,
                pady=20
            )

        finally:

            if cursor:
                cursor.close()

            conn.close()