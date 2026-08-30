import customtkinter as ctk
import sqlite3

from datetime import date, datetime
from tkinter import messagebox

from database import DB_NAME
from theme import *


class OutwardPart2BMenu(ctk.CTkFrame):

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self, master, user):

        super().__init__(
            master,
            fg_color=COLORS["background"]
        )

        self.user = user
        self.case_map = {}

        # =====================================================
        # FONTS
        # =====================================================

        self.title_font = ctk.CTkFont(
            size=SIZES["title_size"],
            weight="bold"
        )

        self.heading_font = ctk.CTkFont(
            size=SIZES["heading_size"],
            weight="bold"
        )

        self.label_font = ctk.CTkFont(
            size=SIZES["label_size"],
            weight="bold"
        )

        self.normal_font = ctk.CTkFont(
            size=SIZES["normal_size"]
        )

        self.bold_font = ctk.CTkFont(
            size=SIZES["normal_size"],
            weight="bold"
        )

        # =====================================================
        # DATABASE PREPARATION
        # =====================================================

        self.prepare_billing_database()

        # =====================================================
        # TITLE
        # =====================================================

        self.title_label = ctk.CTkLabel(
            self,
            text="Billing & Payment",
            font=self.title_font,
            text_color=COLORS["text"]
        )

        self.title_label.pack(
            pady=(0, 20),
            anchor="w"
        )

        # =====================================================
        # MAIN FORM
        # =====================================================

        self.form_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS["card"],
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["primary_hover"]
        )

        self.form_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =====================================================
        # SELECT WORK
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Select Work:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.case_var = ctk.StringVar()

        from searchable_combobox import SearchableComboBox

        self.case_dropdown = SearchableComboBox(
            self.form_frame,

            variable=self.case_var,

            width=650,
            height=SIZES["entry_height"],

            corner_radius=SIZES["corner_radius"],

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

            command=self.load_selected_record
        )

        self.case_dropdown.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="w"
        )

        # =====================================================
        # CURRENT STATUS
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Current Status:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.status_label = ctk.CTkLabel(
            self.form_frame,
            text="-",
            font=self.bold_font,
            text_color=COLORS["primary_hover"]
        )

        self.status_label.grid(
            row=1,
            column=1,
            padx=10,
            pady=5,
            sticky="w"
        )

        # =====================================================
        # BILLING SECTION
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="BILLING",
            font=self.heading_font,
            text_color=COLORS["primary"]
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=(20, 10),
            sticky="w"
        )

        # =====================================================
        # BILL TYPE
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Bill Type:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=3,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.bill_type_var = ctk.StringVar(
            value="Software"
        )

        self.bill_type_dropdown = ctk.CTkComboBox(
            self.form_frame,
            variable=self.bill_type_var,
            values=[
                "Manual",
                "Tally",
                "Software"
            ],
            command=self.on_bill_type_change,
            width=250,
            height=SIZES["entry_height"],
            font=self.normal_font,
            dropdown_font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            button_color=SIDEBAR_HOVER,
            button_hover_color=COLORS["primary_hover"],
            text_color=COLORS["text"],
            dropdown_fg_color=COLORS["card"],
            dropdown_text_color=COLORS["text"],
            dropdown_hover_color=COLORS["primary_hover"]
        )

        self.bill_type_dropdown.grid(
            row=3,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )

        # =====================================================
        # BILLED UNDER
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Billed Under:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=4,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.billed_under_var = ctk.StringVar(
            value="S"
        )

        self.billed_under_dropdown = ctk.CTkComboBox(
            self.form_frame,
            variable=self.billed_under_var,
            values=[
                "S",
                "V"
            ],
            command=self.on_billed_under_change,
            width=250,
            height=SIZES["entry_height"],
            font=self.bold_font,
            dropdown_font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            button_color=SIDEBAR_HOVER,
            button_hover_color=COLORS["primary_hover"],
            text_color=COLORS["text"],
            dropdown_fg_color=COLORS["card"],
            dropdown_text_color=COLORS["text"],
            dropdown_hover_color=COLORS["primary_hover"]
        )

        self.billed_under_dropdown.grid(
            row=4,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )

        # =====================================================
        # BILL DETAILS FRAME
        # =====================================================

        self.bill_fields_frame = ctk.CTkFrame(
            self.form_frame,
            fg_color="transparent"
        )

        self.bill_fields_frame.grid(
            row=5,
            column=0,
            columnspan=2,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.bill_fields_frame.grid_columnconfigure(
            1,
            weight=1
        )

        # =====================================================
        # BILL ID
        # =====================================================

        ctk.CTkLabel(
            self.bill_fields_frame,
            text="Bill ID:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            padx=(0, 15),
            pady=8,
            sticky="w"
        )

        self.bill_num_entry = ctk.CTkEntry(
            self.bill_fields_frame,
            width=300,
            height=42,
            font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"]
        )

        self.bill_num_entry.grid(
            row=0,
            column=1,
            padx=0,
            pady=8,
            sticky="w"
        )

        # =====================================================
        # BILL DATE
        # =====================================================

        ctk.CTkLabel(
            self.bill_fields_frame,
            text="Bill Date:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=1,
            column=0,
            padx=(0, 15),
            pady=8,
            sticky="w"
        )

        self.bill_date_entry = ctk.CTkEntry(
            self.bill_fields_frame,
            width=300,
            height=42,
            font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            placeholder_text="DD-MM-YYYY"
        )

        self.bill_date_entry.grid(
            row=1,
            column=1,
            padx=0,
            pady=8,
            sticky="w"
        )

        # =====================================================
        # BILL AMOUNT
        # =====================================================

        ctk.CTkLabel(
            self.bill_fields_frame,
            text="Bill Amount:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=2,
            column=0,
            padx=(0, 15),
            pady=8,
            sticky="w"
        )

        self.bill_amt_entry = ctk.CTkEntry(
            self.bill_fields_frame,
            width=300,
            height=42,
            font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"]
        )

        self.bill_amt_entry.grid(
            row=2,
            column=1,
            padx=0,
            pady=8,
            sticky="w"
        )

        # =====================================================
        # BILLING INFORMATION
        # =====================================================

        self.bill_info_label = ctk.CTkLabel(
            self.bill_fields_frame,
            text="",
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            text_color=COLORS["text_secondary"]
        )

        self.bill_info_label.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=0,
            pady=(5, 10),
            sticky="w"
        )

        # =====================================================
        # SAVE BILL
        # =====================================================

        self.save_bill_btn = ctk.CTkButton(
            self.form_frame,
            text="Generate / Save Bill",
            command=self.save_bill,
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            height=SIZES["button_height"],
            width=SIZES["button_width"],
            fg_color=LOGOUT,
            hover_color=LOGOUT_HOVER,
            text_color=COLORS["toggle"]
        )

        self.save_bill_btn.grid(
            row=6,
            column=1,
            padx=10,
            pady=25,
            sticky="w"
        )

        # =====================================================
        # PAYMENT SECTION
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="PAYMENT",
            font=self.heading_font,
            text_color=COLORS["primary"]
        ).grid(
            row=7,
            column=0,
            columnspan=2,
            pady=(25, 10),
            sticky="w"
        )

        ctk.CTkLabel(
            self.form_frame,
            text="STATUS",
            font=self.heading_font,
            text_color=COLORS["primary_hover"]
        ).grid(
            row=8,
            column=0,
            columnspan=2,
            pady=(25, 10),
            sticky="w"
        )

        # =====================================================
        # TOTAL BILL
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Bill Amount:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=9,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.total_bill_label = ctk.CTkLabel(
            self.form_frame,
            text="₹0.00",
            font=self.bold_font,
            text_color=COLORS["text"]
        )

        self.total_bill_label.grid(
            row=9,
            column=1,
            padx=10,
            pady=5,
            sticky="w"
        )

        # =====================================================
        # ALREADY RECEIVED
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Already Received:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=10,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.received_label = ctk.CTkLabel(
            self.form_frame,
            text="₹0.00",
            font=self.bold_font,
            text_color=COLORS["primary_hover"]
        )

        self.received_label.grid(
            row=10,
            column=1,
            padx=10,
            pady=5,
            sticky="w"
        )

        # =====================================================
        # BALANCE
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Balance:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=11,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.pending_label = ctk.CTkLabel(
            self.form_frame,
            text="₹0.00",
            font=self.bold_font,
            text_color=COLORS["warning"]
        )

        self.pending_label.grid(
            row=11,
            column=1,
            padx=10,
            pady=5,
            sticky="w"
        )

        # =====================================================
        # NEW PAYMENT
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="New Payment Amount:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=12,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.payment_amount_entry = ctk.CTkEntry(
            self.form_frame,
            width=250,
            height=SIZES["entry_height"],
            font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            placeholder_text="Enter amount received now"
        )

        self.payment_amount_entry.grid(
            row=12,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )

        # =====================================================
        # PAYMENT MODE
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Payment Mode:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=13,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.payment_mode_var = ctk.StringVar(
            value="Cash"
        )

        self.payment_mode_dropdown = ctk.CTkComboBox(
            self.form_frame,
            variable=self.payment_mode_var,
            values=[
                "Cash",
                "UPI",
                "Bank Transfer",
                "Cheque",
                "Card",
                "Other"
            ],
            width=250,
            height=SIZES["entry_height"],
            font=self.normal_font,
            dropdown_font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            button_color=SIDEBAR_HOVER,
            button_hover_color=COLORS["primary_hover"],
            text_color=COLORS["text"],
            dropdown_fg_color=COLORS["card"],
            dropdown_text_color=COLORS["text"],
            dropdown_hover_color=COLORS["primary_hover"]
        )

        self.payment_mode_dropdown.grid(
            row=13,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )

        # =====================================================
        # PAYMENT DATE
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Payment Date:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=14,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.payment_date_entry = ctk.CTkEntry(
            self.form_frame,
            width=250,
            height=SIZES["entry_height"],
            font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            placeholder_text="DD-MM-YYYY"
        )

        self.payment_date_entry.insert(
            0,
            date.today().strftime("%d-%m-%Y")
        )

        self.payment_date_entry.grid(
            row=14,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )

        # =====================================================
        # NOTES
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Payment Notes:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=15,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.payment_notes_entry = ctk.CTkEntry(
            self.form_frame,
            width=350,
            height=SIZES["entry_height"],
            font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            placeholder_text="Optional"
        )

        self.payment_notes_entry.grid(
            row=15,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )

        # =====================================================
        # RECORD PAYMENT
        # =====================================================

        self.receive_payment_btn = ctk.CTkButton(
            self.form_frame,
            text="Record Payment",
            command=self.record_payment,
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            height=SIZES["button_height"],
            width=SIZES["button_width"],
            fg_color=LOGOUT,
            hover_color=LOGOUT_HOVER,
            text_color=COLORS["toggle"]
        )

        self.receive_payment_btn.grid(
            row=16,
            column=1,
            padx=10,
            pady=25,
            sticky="w"
        )

        # =====================================================
        # PAYMENT HISTORY
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Payment History",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color=COLORS["primary"]
        ).grid(
            row=17,
            column=0,
            columnspan=2,
            pady=(25, 12),
            sticky="ew"
        )

        self.payment_history_frame = ctk.CTkScrollableFrame(
            self.form_frame,
            width=800,
            height=250,
            fg_color=COLORS["card"],
            border_width=3,
            border_color=COLORS["border"]
        )

        self.payment_history_frame.grid(
            row=18,
            column=0,
            columnspan=2,
            padx=10,
            pady=10
        )

        # =====================================================
        # INITIAL BILL TYPE STATE
        # =====================================================

        self.on_bill_type_change("Software")

        # =====================================================
        # LOAD
        # =====================================================

        self.load_records()

    # =========================================================
    # DATE DISPLAY / DATABASE CONVERSION
    # =========================================================

    @staticmethod
    def format_date_for_display(db_date):
        """
        Database:
            YYYY-MM-DD

        Display:
            DD-MM-YYYY
        """

        if not db_date:
            return ""

        try:

            return datetime.strptime(
                str(db_date),
                "%Y-%m-%d"
            ).strftime(
                "%d-%m-%Y"
            )

        except ValueError:

            # Keep unexpected/legacy values unchanged
            return str(db_date)

    @staticmethod
    def format_date_for_database(display_date):
        """
        Display:
            DD-MM-YYYY

        Database:
            YYYY-MM-DD
        """

        if not display_date:
            return ""

        try:

            return datetime.strptime(
                str(display_date).strip(),
                "%d-%m-%Y"
            ).strftime(
                "%Y-%m-%d"
            )

        except ValueError:

            return None

    # =========================================================
    # DATABASE PREPARATION
    # =========================================================

    def prepare_billing_database(self):

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            # -------------------------------------------------
            # Billing fields in records
            # -------------------------------------------------

            cursor.execute(
                "PRAGMA table_info(records)"
            )

            columns = {
                row[1]
                for row in cursor.fetchall()
            }

            required_columns = {
                "bill_type": "TEXT",
                "billed_under": "TEXT",
                "bill_number": "TEXT",
                "bill_date": "TEXT",
                "bill_amount": "REAL DEFAULT 0",
                "actual_amount_received": "REAL DEFAULT 0",
                "amount_pending_receipt": "REAL DEFAULT 0",
                "billed_by": "INTEGER",
                "bill_raised_at": "TEXT"
            }

            for column_name, column_definition in required_columns.items():

                if column_name not in columns:

                    cursor.execute(
                        f"""
                        ALTER TABLE records
                        ADD COLUMN {column_name}
                        {column_definition}
                        """
                    )

            # -------------------------------------------------
            # Software bill sequence table
            # -------------------------------------------------

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bill_sequences (
                    department TEXT NOT NULL,
                    billed_under TEXT NOT NULL,
                    last_number INTEGER NOT NULL DEFAULT 0,
                    PRIMARY KEY (
                        department,
                        billed_under
                    )
                )
            """)

            conn.commit()

        finally:

            conn.close()

    # =========================================================
    # GENERATE SOFTWARE BILL NUMBER
    # =========================================================

    def generate_software_bill_number(
        self,
        department,
        billed_under,
        cursor
    ):

        department = (
            department or ""
        ).strip().upper()

        billed_under = (
            billed_under or ""
        ).strip().upper()

        if not department:

            raise ValueError(
                "Department is missing for this work."
            )

        if billed_under not in ("S", "V"):

            raise ValueError(
                "Invalid billed-under value."
            )

        # -----------------------------------------------------
        # Get current sequence
        # -----------------------------------------------------

        cursor.execute("""
            SELECT last_number
            FROM bill_sequences
            WHERE department = ?
              AND billed_under = ?
        """, (
            department,
            billed_under
        ))

        row = cursor.fetchone()

        if row:

            next_number = int(row[0]) + 1

            cursor.execute("""
                UPDATE bill_sequences
                SET last_number = ?
                WHERE department = ?
                  AND billed_under = ?
            """, (
                next_number,
                department,
                billed_under
            ))

        else:

            next_number = 1

            cursor.execute("""
                INSERT INTO bill_sequences (
                    department,
                    billed_under,
                    last_number
                )
                VALUES (?, ?, ?)
            """, (
                department,
                billed_under,
                next_number
            ))

        return (
            f"{billed_under}"
            f"{department}"
            f"{next_number}"
        )

    # =========================================================
    # BILL TYPE CHANGE
    # =========================================================

    def on_bill_type_change(self, choice):

        if choice not in (
            "Manual",
            "Tally",
            "Software"
        ):

            return

        # -----------------------------------------------------
        # Clear fields
        # -----------------------------------------------------

        self.bill_num_entry.configure(
            state="normal"
        )

        self.bill_date_entry.configure(
            state="normal"
        )

        self.bill_num_entry.delete(
            0,
            "end"
        )

        self.bill_date_entry.delete(
            0,
            "end"
        )

        # -----------------------------------------------------
        # SOFTWARE
        # -----------------------------------------------------

        if choice == "Software":

            selected = self.case_var.get()
            record_id = self.case_map.get(selected)

            if record_id:

                self.load_software_bill_preview(
                    record_id
                )

            else:

                self.bill_num_entry.configure(
                    state="disabled"
                )

                self.bill_date_entry.configure(
                    state="disabled"
                )

                self.bill_info_label.configure(
                    text=(
                        "Software bill number and date "
                        "will be generated automatically."
                    )
                )

        # -----------------------------------------------------
        # MANUAL / TALLY
        # -----------------------------------------------------

        else:

            self.bill_num_entry.configure(
                state="normal"
            )

            self.bill_date_entry.configure(
                state="normal"
            )

            self.bill_info_label.configure(
                text=(
                    f"{choice} bill: enter the external "
                    f"bill ID and bill date."
                )
            )

            self.bill_date_entry.insert(
                0,
                date.today().strftime("%d-%m-%Y")
            )

    # =========================================================
    # BILLED UNDER CHANGE
    # =========================================================

    def on_billed_under_change(self, choice):

        if self.bill_type_var.get() == "Software":

            selected = self.case_var.get()
            record_id = self.case_map.get(selected)

            if record_id:

                self.load_software_bill_preview(
                    record_id
                )

    # =========================================================
    # SOFTWARE BILL PREVIEW
    # =========================================================

    def load_software_bill_preview(self, record_id):

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    department,
                    bill_number,
                    bill_date,
                    bill_amount
                FROM records
                WHERE inward_id = ?
            """, (
                record_id,
            ))

            record = cursor.fetchone()

        finally:

            conn.close()

        if not record:

            return

        (
            department,
            existing_bill_number,
            existing_bill_date,
            existing_bill_amount
        ) = record

        # -----------------------------------------------------
        # Existing bill
        # -----------------------------------------------------

        if existing_bill_number:

            self.bill_num_entry.configure(
                state="normal"
            )

            self.bill_num_entry.delete(
                0,
                "end"
            )

            self.bill_num_entry.insert(
                0,
                str(existing_bill_number)
            )

            self.bill_num_entry.configure(
                state="disabled"
            )

            self.bill_date_entry.configure(
                state="normal"
            )

            self.bill_date_entry.delete(
                0,
                "end"
            )

            self.bill_date_entry.insert(
                0,
                self.format_date_for_display(
                    existing_bill_date
                )
            )

            self.bill_date_entry.configure(
                state="disabled"
            )

            self.bill_info_label.configure(
                text="Bill already generated. It cannot be generated again."
            )

            self.save_bill_btn.configure(
                state="disabled",
                text="Bill Already Generated"
            )

            return

        # -----------------------------------------------------
        # New software bill
        # -----------------------------------------------------

        self.bill_num_entry.configure(
            state="disabled"
        )

        self.bill_num_entry.delete(
            0,
            "end"
        )

        self.bill_num_entry.insert(
            0,
            "Will be generated automatically"
        )

        self.bill_date_entry.configure(
            state="disabled"
        )

        self.bill_date_entry.delete(
            0,
            "end"
        )

        self.bill_date_entry.insert(
            0,
            date.today().strftime("%d-%m-%Y")
        )

        self.bill_info_label.configure(
            text=(
                "Software bill ID and date are generated "
                "automatically when the bill is saved."
            )
        )

        self.save_bill_btn.configure(
            state="normal",
            text="Generate / Save Bill"
        )

    # =========================================================
    # LOAD RECORDS
    # =========================================================

    def load_records(self, selected_record_id=None):

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    r.inward_id,
                    c.name,
                    r.department,
                    r.nature_of_papers,
                    r.status,
                    r.bill_number,
                    r.bill_amount,
                    r.actual_amount_received,
                    r.amount_pending_receipt
                FROM records r
                LEFT JOIN clients c
                    ON r.client_id = c.id
                WHERE r.status >= 1
                ORDER BY r.inward_id DESC
            """)

            records = cursor.fetchall()

        finally:

            conn.close()

        self.case_map = {}

        display_values = []

        for record in records:

            (
                record_id,
                client_name,
                department,
                nature,
                status,
                bill_number,
                bill_amount,
                actual_received,
                pending
            ) = record

            if status == 1:

                status_text = (
                    "Work Done - Not Dispatched"
                )

            elif status == 2:

                status_text = "Dispatched"

            else:

                status_text = str(status)

            display = (
                f"ID: {record_id} | "
                f"{client_name} | "
                f"{department or '-'} | "
                f"{nature} | "
                f"{status_text} | "
                f"Bill: "
                f"{bill_number or 'Not Generated'} | "
                f"₹{float(bill_amount or 0):.2f} | "
                f"Balance: "
                f"₹{float(pending or 0):.2f}"
            )

            self.case_map[
                display
            ] = record_id

            display_values.append(
                display
            )

        if display_values:

            self.case_dropdown.configure_values(
                display_values
            )

            selected_display = (
                display_values[0]
            )

            if selected_record_id is not None:

                for (
                    display_text,
                    rid
                ) in self.case_map.items():

                    if rid == selected_record_id:

                        selected_display = (
                            display_text
                        )

                        break

            self.case_dropdown.set(
                selected_display
            )

            self.load_selected_record(
                selected_display
            )

        else:

            self.case_dropdown.set(
                "No work available"
            )

            self.clear_bill_display()

    # =========================================================
    # LOAD SELECTED RECORD
    # =========================================================

    def load_selected_record(
        self,
        choice=None
    ):

        if choice is None:

            choice = self.case_var.get()

        record_id = self.case_map.get(
            choice
        )

        if not record_id:

            return

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    status,
                    department,
                    bill_type,
                    billed_under,
                    bill_number,
                    bill_date,
                    bill_amount,
                    actual_amount_received,
                    amount_pending_receipt
                FROM records
                WHERE inward_id = ?
            """, (
                record_id,
            ))

            record = cursor.fetchone()

        finally:

            conn.close()

        if not record:

            return

        (
            status,
            department,
            bill_type,
            billed_under,
            bill_number,
            bill_date,
            bill_amount,
            actual_received,
            pending
        ) = record

        # =====================================================
        # STATUS
        # =====================================================

        if status == 1:

            self.status_label.configure(
                text="WORK COMPLETED - AVAILABLE FOR BILLING",
                text_color=COLORS["success"]
            )

        elif status == 2:

            self.status_label.configure(
                text="DISPATCHED",
                text_color=COLORS["dispatch"]
            )

        else:

            self.status_label.configure(
                text=str(status),
                text_color=COLORS["text"]
            )

        # =====================================================
        # PAYMENT STATUS
        # =====================================================

        bill_amount = float(
            bill_amount or 0
        )

        actual_received = float(
            actual_received or 0
        )

        calculated_pending = max(
            0,
            bill_amount - actual_received
        )

        self.total_bill_label.configure(
            text=f"₹{bill_amount:.2f}"
        )

        self.received_label.configure(
            text=f"₹{actual_received:.2f}"
        )

        self.pending_label.configure(
            text=f"₹{calculated_pending:.2f}"
        )

        # =====================================================
        # BILL INFORMATION
        # =====================================================

        if bill_type:

            self.bill_type_var.set(
                bill_type
            )

        else:

            self.bill_type_var.set(
                "Software"
            )

        if billed_under:

            self.billed_under_var.set(
                billed_under
            )

        else:

            self.billed_under_var.set(
                "S"
            )

        # -----------------------------------------------------
        # Existing bill
        # -----------------------------------------------------

        if bill_number:

            self.bill_num_entry.configure(
                state="normal"
            )

            self.bill_num_entry.delete(
                0,
                "end"
            )

            self.bill_num_entry.insert(
                0,
                str(bill_number)
            )

            self.bill_num_entry.configure(
                state="disabled"
            )

            self.bill_date_entry.configure(
                state="normal"
            )

            self.bill_date_entry.delete(
                0,
                "end"
            )

            self.bill_date_entry.insert(
                0,
                self.format_date_for_display(
                    bill_date
                )
            )

            self.bill_date_entry.configure(
                state="disabled"
            )

            self.bill_info_label.configure(
                text=(
                    f"Bill generated: "
                    f"{bill_number}"
                )
            )

            self.save_bill_btn.configure(
                state="disabled",
                text="Bill Already Generated"
            )

        # -----------------------------------------------------
        # No bill yet
        # -----------------------------------------------------

        else:

            self.bill_num_entry.configure(
                state="normal"
            )

            self.bill_num_entry.delete(
                0,
                "end"
            )

            self.bill_date_entry.configure(
                state="normal"
            )

            self.bill_date_entry.delete(
                0,
                "end"
            )

            self.bill_amt_entry.delete(
                0,
                "end"
            )

            if bill_type == "Software":

                self.load_software_bill_preview(
                    record_id
                )

            else:

                self.on_bill_type_change(
                    bill_type or "Manual"
                )

        # =====================================================
        # BILL AMOUNT
        # =====================================================

        self.bill_amt_entry.delete(
            0,
            "end"
        )

        if bill_amount > 0:

            self.bill_amt_entry.insert(
                0,
                f"{bill_amount:.2f}"
            )

        # =====================================================
        # PAYMENT ENTRY
        # =====================================================

        self.payment_amount_entry.delete(
            0,
            "end"
        )

        # =====================================================
        # PAYMENT HISTORY
        # =====================================================

        self.load_payment_history(
            record_id
        )

    # =========================================================
    # CLEAR BILL DISPLAY
    # =========================================================

    def clear_bill_display(self):

        self.status_label.configure(
            text="-"
        )

        self.total_bill_label.configure(
            text="₹0.00"
        )

        self.received_label.configure(
            text="₹0.00"
        )

        self.pending_label.configure(
            text="₹0.00"
        )

        self.bill_num_entry.configure(
            state="normal"
        )

        self.bill_num_entry.delete(
            0,
            "end"
        )

        self.bill_date_entry.configure(
            state="normal"
        )

        self.bill_date_entry.delete(
            0,
            "end"
        )

        self.bill_amt_entry.delete(
            0,
            "end"
        )

    # =========================================================
    # SAVE / GENERATE BILL
    # =========================================================

    def save_bill(self):

        selected = self.case_var.get()

        record_id = self.case_map.get(
            selected
        )

        if not record_id:

            messagebox.showerror(
                "Error",
                "Please select a valid work record."
            )

            return

        conn = sqlite3.connect(
            DB_NAME
        )

        try:

            cursor = conn.cursor()

            # =================================================
            # GET CURRENT RECORD
            # =================================================

            cursor.execute("""
                SELECT
                    status,
                    department,
                    bill_type,
                    billed_under,
                    bill_number,
                    bill_date,
                    bill_amount,
                    actual_amount_received
                FROM records
                WHERE inward_id = ?
            """, (
                record_id,
            ))

            record = cursor.fetchone()

            if not record:

                messagebox.showerror(
                    "Error",
                    "Record not found."
                )

                return

            (
                status,
                department,
                existing_bill_type,
                existing_billed_under,
                existing_bill_number,
                existing_bill_date,
                existing_bill_amount,
                received
            ) = record

            # =================================================
            # BILL CAN ONLY BE CREATED ONCE
            # =================================================

            if existing_bill_number:

                messagebox.showerror(
                    "Bill Already Generated",
                    (
                        f"This work already has bill "
                        f"{existing_bill_number}.\n\n"
                        "A bill can only be generated once."
                    )
                )

                return

            # =================================================
            # WORK STATUS
            # =================================================

            if status < 1:

                messagebox.showerror(
                    "Error",
                    "Billing is available only after the work is completed."
                )

                return

            # =================================================
            # BILL TYPE
            # =================================================

            bill_type = (
                self.bill_type_var
                .get()
                .strip()
            )

            if bill_type not in (
                "Manual",
                "Tally",
                "Software"
            ):

                messagebox.showerror(
                    "Error",
                    "Please select a valid bill type."
                )

                return

            # =================================================
            # BILLED UNDER
            # =================================================

            billed_under = (
                self.billed_under_var
                .get()
                .strip()
                .upper()
            )

            if billed_under not in (
                "S",
                "V"
            ):

                messagebox.showerror(
                    "Error",
                    "Please select S or V under 'Billed Under'."
                )

                return

            # =================================================
            # BILL AMOUNT
            # =================================================

            bill_amount_text = (
                self.bill_amt_entry
                .get()
                .strip()
            )

            if not bill_amount_text:

                messagebox.showerror(
                    "Error",
                    "Bill Amount is required."
                )

                return

            try:

                bill_amount = float(
                    bill_amount_text
                )

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Invalid bill amount."
                )

                return

            if bill_amount <= 0:

                messagebox.showerror(
                    "Error",
                    "Bill Amount must be greater than zero."
                )

                return

            # =================================================
            # EXISTING RECEIVED CHECK
            # =================================================

            received = float(
                received or 0
            )

            if received > bill_amount:

                messagebox.showerror(
                    "Error",
                    (
                        "Bill amount cannot be less than "
                        "the amount already received."
                    )
                )

                return

            pending = (
                bill_amount - received
            )

            # =================================================
            # BILL ID / DATE
            # =================================================

            # -------------------------------------------------
            # SOFTWARE
            # -------------------------------------------------

            if bill_type == "Software":

                # Generate the ID ONLY NOW.

                bill_number = (
                    self.generate_software_bill_number(
                        department,
                        billed_under,
                        cursor
                    )
                )

                # DATABASE FORMAT REMAINS YYYY-MM-DD
                bill_date = (
                    date.today()
                    .isoformat()
                )

            # -------------------------------------------------
            # MANUAL / TALLY
            # -------------------------------------------------

            else:

                bill_number = (
                    self.bill_num_entry
                    .get()
                    .strip()
                )

                bill_date_display = (
                    self.bill_date_entry
                    .get()
                    .strip()
                )

                if not bill_number:

                    messagebox.showerror(
                        "Error",
                        "Bill ID is required."
                    )

                    conn.rollback()
                    return

                if not bill_date_display:

                    messagebox.showerror(
                        "Error",
                        "Bill Date is required."
                    )

                    conn.rollback()
                    return

                # -------------------------------------------------
                # Convert UI DD-MM-YYYY to DB YYYY-MM-DD
                # -------------------------------------------------

                bill_date = (
                    self.format_date_for_database(
                        bill_date_display
                    )
                )

                if bill_date is None:

                    messagebox.showerror(
                        "Invalid Bill Date",
                        "Please enter the bill date in DD-MM-YYYY format."
                    )

                    conn.rollback()
                    return

                # -------------------------------------------------
                # Prefix S/V to manually entered bill number
                # -------------------------------------------------

                # Prevent accidental double-prefixing.

                if not bill_number.startswith(
                    billed_under
                ):

                    bill_number = (
                        billed_under
                        + bill_number
                    )

            # =================================================
            # FINAL DUPLICATE CHECK
            # =================================================

            cursor.execute("""
                SELECT inward_id
                FROM records
                WHERE bill_number = ?
                  AND inward_id != ?
            """, (
                bill_number,
                record_id
            ))

            duplicate = cursor.fetchone()

            if duplicate:

                messagebox.showerror(
                    "Duplicate Bill ID",
                    (
                        f"Bill ID '{bill_number}' "
                        "already exists."
                    )
                )

                conn.rollback()
                return

            # =================================================
            # SAVE BILL
            # =================================================

            now = datetime.now().isoformat(
                timespec="seconds"
            )

            cursor.execute("""
                UPDATE records
                SET
                    bill_type = ?,
                    billed_under = ?,
                    bill_number = ?,
                    bill_date = ?,
                    bill_amount = ?,
                    amount_pending_receipt = ?,
                    billed_by = ?,
                    bill_raised_at = ?
                WHERE inward_id = ?
                  AND status >= 1
                  AND (
                      bill_number IS NULL
                      OR bill_number = ''
                  )
            """, (
                bill_type,
                billed_under,
                bill_number,
                bill_date,
                bill_amount,
                pending,
                self.user["id"],
                now,
                record_id
            ))

            if cursor.rowcount != 1:

                messagebox.showerror(
                    "Error",
                    (
                        "The bill could not be saved. "
                        "It may already have been generated."
                    )
                )

                conn.rollback()
                return

            # =================================================
            # ACTIVITY LOG
            # =================================================

            cursor.execute("""
                INSERT INTO activity_log (
                    record_id,
                    action_type,
                    performed_by,
                    amount,
                    description
                )
                VALUES (
                    ?,
                    'BILL_RAISED',
                    ?,
                    ?,
                    ?
                )
            """, (
                record_id,
                self.user["id"],
                bill_amount,
                (
                    f"{bill_type} bill "
                    f"{bill_number} generated "
                    f"under {billed_under}"
                )
            ))

            conn.commit()

        except Exception as e:

            conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            return

        finally:

            conn.close()

        # =====================================================
        # SUCCESS
        # =====================================================

        messagebox.showinfo(
            "Bill Generated",
            (
                f"Bill generated successfully.\n\n"
                f"Bill Type: {bill_type}\n"
                f"Bill ID: {bill_number}\n"
                f"Bill Date: "
                f"{self.format_date_for_display(bill_date)}\n"
                f"Bill Amount: ₹{bill_amount:.2f}\n"
                f"Already Received: ₹{received:.2f}\n"
                f"Balance: ₹{pending:.2f}"
            )
        )

        saved_record_id = record_id

        self.load_records(
            selected_record_id=saved_record_id
        )

    # =========================================================
    # RECORD PAYMENT
    # =========================================================

    def record_payment(self):

        selected = self.case_var.get()

        record_id = self.case_map.get(
            selected
        )

        if not record_id:

            messagebox.showerror(
                "Error",
                "Please select a valid work record."
            )

            return

        amount_text = (
            self.payment_amount_entry
            .get()
            .strip()
        )

        if not amount_text:

            messagebox.showerror(
                "Error",
                "Enter the amount received now."
            )

            return

        try:

            amount = float(
                amount_text
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Invalid payment amount."
            )

            return

        if amount <= 0:

            messagebox.showerror(
                "Error",
                "Payment amount must be greater than zero."
            )

            return

        payment_mode = (
            self.payment_mode_var
            .get()
            .strip()
        )

        # -----------------------------------------------------
        # Payment date is entered by user as DD-MM-YYYY
        # -----------------------------------------------------

        payment_date_display = (
            self.payment_date_entry
            .get()
            .strip()
        )

        notes = (
            self.payment_notes_entry
            .get()
            .strip()
        )

        if not payment_date_display:

            messagebox.showerror(
                "Error",
                "Payment date is required."
            )

            return

        # -----------------------------------------------------
        # Convert DD-MM-YYYY to YYYY-MM-DD
        # before saving to database
        # -----------------------------------------------------

        payment_date = (
            self.format_date_for_database(
                payment_date_display
            )
        )

        if payment_date is None:

            messagebox.showerror(
                "Invalid Payment Date",
                "Please enter the payment date in DD-MM-YYYY format."
            )

            return

        conn = sqlite3.connect(
            DB_NAME
        )

        try:

            cursor = conn.cursor()

            # =================================================
            # GET BILL
            # =================================================

            cursor.execute("""
                SELECT
                    bill_number,
                    bill_amount,
                    actual_amount_received
                FROM records
                WHERE inward_id = ?
            """, (
                record_id,
            ))

            record = cursor.fetchone()

            if not record:

                messagebox.showerror(
                    "Error",
                    "Record not found."
                )

                return

            (
                bill_number,
                bill_amount,
                current_received
            ) = record

            # =================================================
            # BILL MUST EXIST
            # =================================================

            if not bill_number:

                messagebox.showerror(
                    "Error",
                    "Generate the bill before recording a payment."
                )

                return

            bill_amount = float(
                bill_amount or 0
            )

            current_received = float(
                current_received or 0
            )

            balance = (
                bill_amount
                - current_received
            )

            if amount > balance + 0.001:

                messagebox.showerror(
                    "Error",
                    (
                        "Payment is greater than "
                        "the outstanding balance.\n\n"
                        f"Balance available: "
                        f"₹{balance:.2f}"
                    )
                )

                return

            # =================================================
            # NEW TOTALS
            # =================================================

            new_received = (
                current_received
                + amount
            )

            new_pending = (
                bill_amount
                - new_received
            )

            if abs(new_pending) < 0.01:

                new_pending = 0.0

            # =================================================
            # PAYMENT TRANSACTION
            # =================================================

            cursor.execute("""
                INSERT INTO payment_transactions (
                    record_id,
                    amount,
                    payment_mode,
                    payment_date,
                    received_by,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                record_id,
                amount,
                payment_mode,
                payment_date,
                self.user["id"],
                notes
            ))

            # =================================================
            # UPDATE RUNNING TOTAL
            # =================================================

            cursor.execute("""
                UPDATE records
                SET
                    actual_amount_received = ?,
                    amount_pending_receipt = ?
                WHERE inward_id = ?
            """, (
                new_received,
                new_pending,
                record_id
            ))

            # =================================================
            # AUDIT LOG
            # =================================================

            cursor.execute("""
                INSERT INTO activity_log (
                    record_id,
                    action_type,
                    performed_by,
                    amount,
                    payment_mode,
                    description
                )
                VALUES (
                    ?,
                    'PAYMENT_RECEIVED',
                    ?,
                    ?,
                    ?,
                    ?
                )
            """, (
                record_id,
                self.user["id"],
                amount,
                payment_mode,
                notes or "Payment received"
            ))

            conn.commit()

        except Exception as e:

            conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            return

        finally:

            conn.close()

        # =====================================================
        # SUCCESS
        # =====================================================

        messagebox.showinfo(
            "Payment Recorded",
            (
                f"Payment received: ₹{amount:.2f}\n\n"
                f"Total received: ₹{new_received:.2f}\n"
                f"Balance remaining: ₹{new_pending:.2f}"
            )
        )

        self.payment_amount_entry.delete(
            0,
            "end"
        )

        self.payment_notes_entry.delete(
            0,
            "end"
        )

        saved_record_id = record_id

        self.load_records(
            selected_record_id=saved_record_id
        )

    # =========================================================
    # PAYMENT HISTORY
    # =========================================================

    def load_payment_history(
        self,
        record_id
    ):

        for widget in (
            self.payment_history_frame
            .winfo_children()
        ):

            widget.destroy()

        conn = sqlite3.connect(
            DB_NAME
        )

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    p.id,
                    p.payment_date,
                    p.amount,
                    p.payment_mode,
                    u.username,
                    p.notes
                FROM payment_transactions p
                LEFT JOIN users u
                    ON p.received_by = u.id
                WHERE p.record_id = ?
                ORDER BY p.id DESC
            """, (
                record_id,
            ))

            payments = cursor.fetchall()

        finally:

            conn.close()

        # =====================================================
        # HEADERS
        # =====================================================

        headers = [
            "Payment ID",
            "Date",
            "Amount",
            "Mode",
            "Received By",
            "Notes"
        ]

        for col, header in enumerate(
            headers
        ):

            ctk.CTkLabel(
                self.payment_history_frame,
                text=header,
                font=ctk.CTkFont(
                    size=SIZES["normal_size"],
                    weight="bold"
                ),
                text_color=COLORS["primary"]
            ).grid(
                row=0,
                column=col,
                padx=8,
                pady=5,
                sticky="w"
            )

        # =====================================================
        # NO PAYMENTS
        # =====================================================

        if not payments:

            ctk.CTkLabel(
                self.payment_history_frame,
                text="No payments recorded yet.",
                font=self.normal_font,
                text_color=COLORS["text_secondary"]
            ).grid(
                row=1,
                column=0,
                columnspan=6,
                padx=10,
                pady=10
            )

            return

        # =====================================================
        # PAYMENT ROWS
        # =====================================================

        for row_idx, payment in enumerate(
            payments,
            start=1
        ):

            (
                payment_id,
                payment_date,
                amount,
                mode,
                received_by,
                notes
            ) = payment

            values = [
                payment_id,

                # Database YYYY-MM-DD
                # displayed as DD-MM-YYYY
                self.format_date_for_display(
                    payment_date
                ),

                f"₹{float(amount):.2f}",

                mode,

                received_by or "-",

                notes or "-"
            ]

            for col_idx, value in enumerate(
                values
            ):

                ctk.CTkLabel(
                    self.payment_history_frame,
                    text=str(value),
                    font=self.normal_font,
                    text_color=COLORS["text"]
                ).grid(
                    row=row_idx,
                    column=col_idx,
                    padx=8,
                    pady=4,
                    sticky="w"
                )