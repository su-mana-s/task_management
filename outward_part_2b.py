import os
import psycopg

import customtkinter as ctk
from num2words import num2words
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from tkinter import messagebox, filedialog

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether
)

from database import get_connection
from theme import *
import psycopg

from database import get_connection
import constants

from constants import (
    BUSINESS_DETAILS,
    BILL_TYPES,
    BILLED_UNDER,
    PAYMENT_MODES,
    BANK_TRANSFER_MODES,
    MONTHS,
    QUARTERS,
)





# ============================================================
# MAIN CLASS
# ============================================================

class OutwardPart2BMenu(ctk.CTkFrame):

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self, master, user):

        super().__init__(
            master,
            fg_color=COLORS["background"]
        )

        self.user = user
        self.case_map = {}

        self.current_task_id = None

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

        self.prepare_billing_database()

        self.create_interface()

        self.load_records()


    # ========================================================
    # DATABASE PREPARATION
    # ========================================================

    def prepare_billing_database(self):

        conn = get_connection()

        try:

            cursor = conn.cursor()

            # ------------------------------------------------
            # The new database should already contain these
            # tables. This method only verifies connectivity.
            # ------------------------------------------------

            cursor.execute("""
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = 'tasks'
            """)

            if cursor.fetchone() is None:

                raise RuntimeError(
                    "The PostgreSQL database has not been initialized.\n\n"
                    "Run database.py first."
                )

            cursor.execute("""
                ALTER TABLE tasks
                ADD COLUMN IF NOT EXISTS billing_narrative TEXT
            """)
            cursor.execute("""
                ALTER TABLE tasks
                ADD COLUMN IF NOT EXISTS pay_to TEXT
            """)

            conn.commit()

        finally:

            conn.close()


    # ========================================================
    # UI
    # ========================================================

    def create_interface(self):

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


        # ====================================================
        # SELECT WORK
        # ====================================================

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
            width=750,
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


        # ====================================================
        # CURRENT STATUS
        # ====================================================

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


        # ====================================================
        # BILLING
        # ====================================================

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


        # ====================================================
        # BILL TYPE
        # ====================================================

        self.create_label(
            "Bill Type:",
            3
        )

        self.bill_type_var = ctk.StringVar(
            value="Software"
        )

        self.bill_type_dropdown = ctk.CTkComboBox(
            self.form_frame,
            variable=self.bill_type_var,
            values=BILL_TYPES,
            command=self.on_bill_type_change,
            width=300,
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


        # ====================================================
        # BILLED UNDER
        # ====================================================

        self.create_label(
            "Billed Under:",
            4
        )

        self.billed_under_var = ctk.StringVar(
            value="Sridharan"
        )

        self.billed_under_dropdown = ctk.CTkComboBox(
            self.form_frame,
            variable=self.billed_under_var,
            values=BILLED_UNDER,
            command=self.on_billed_under_change,
            width=300,
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


        # ====================================================
        # BILL NUMBER
        # ====================================================

        self.create_label(
            "Bill Number:",
            5
        )

        self.bill_num_entry = self.create_entry()

        self.bill_num_entry.grid(
            row=5,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )


        # ====================================================
        # BILL DATE
        # ====================================================

        self.create_label(
            "Bill Date:",
            6
        )

        self.bill_date_entry = self.create_entry(
            placeholder="DD-MM-YYYY"
        )

        self.bill_date_entry.grid(
            row=6,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )


        # ====================================================
        # BILLING-SPECIFIC FIELDS
        # ====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Department Billing Details",
            font=self.heading_font,
            text_color=COLORS["primary"]
        ).grid(
            row=7,
            column=0,
            columnspan=2,
            pady=(20, 10),
            sticky="w"
        )


        self.department_fields_frame = ctk.CTkFrame(
            self.form_frame,
            fg_color="transparent"
        )

        self.department_fields_frame.grid(
            row=8,
            column=0,
            columnspan=2,
            padx=10,
            pady=5,
            sticky="w"
        )


        self.create_department_fields()


        # ====================================================
        # BILL AMOUNT
        # ====================================================

        self.create_label(
            "Total Bill Amount:",
            9
        )

        self.bill_amt_entry = self.create_entry()

        self.bill_amt_entry.grid(
            row=9,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )


        # ====================================================
        # BILL INFORMATION
        # ====================================================

        self.bill_info_label = ctk.CTkLabel(
            self.form_frame,
            text="",
            font=self.bold_font,
            text_color=COLORS["text_secondary"]
        )

        self.bill_info_label.grid(
            row=10,
            column=0,
            columnspan=2,
            padx=10,
            pady=5,
            sticky="w"
        )


        # ====================================================
        # BILL BUTTONS
        # ====================================================

        self.save_bill_btn = ctk.CTkButton(
            self.form_frame,
            text="Generate / Save Bill",
            command=self.save_bill,
            font=self.bold_font,
            height=SIZES["button_height"],
            width=SIZES["button_width"],
            fg_color=LOGOUT,
            hover_color=LOGOUT_HOVER,
            text_color=COLORS["toggle"]
        )

        self.save_bill_btn.grid(
            row=11,
            column=1,
            padx=10,
            pady=15,
            sticky="w"
        )


        self.print_bill_btn = ctk.CTkButton(
            self.form_frame,
            text="Print / Save Bill PDF",
            command=self.print_bill,
            font=self.bold_font,
            height=SIZES["button_height"],
            width=SIZES["button_width"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            state="disabled"
        )

        self.print_bill_btn.grid(
            row=12,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )


        # ====================================================
        # PAYMENT SECTION
        # ====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="PAYMENT",
            font=self.heading_font,
            text_color=COLORS["primary"]
        ).grid(
            row=13,
            column=0,
            columnspan=2,
            pady=(30, 10),
            sticky="w"
        )


        # ====================================================
        # TOTAL
        # ====================================================

        self.create_label(
            "Bill Amount:",
            14
        )

        self.total_bill_label = ctk.CTkLabel(
            self.form_frame,
            text="Rs.0.00",
            font=self.bold_font,
            text_color=COLORS["text"]
        )

        self.total_bill_label.grid(
            row=14,
            column=1,
            padx=10,
            pady=5,
            sticky="w"
        )


        self.create_label(
            "Already Received:",
            15
        )

        self.received_label = ctk.CTkLabel(
            self.form_frame,
            text="Rs.0.00",
            font=self.bold_font,
            text_color=COLORS["primary_hover"]
        )

        self.received_label.grid(
            row=15,
            column=1,
            padx=10,
            pady=5,
            sticky="w"
        )


        self.create_label(
            "Balance:",
            16
        )

        self.pending_label = ctk.CTkLabel(
            self.form_frame,
            text="Rs.0.00",
            font=self.bold_font,
            text_color=COLORS["warning"]
        )

        self.pending_label.grid(
            row=16,
            column=1,
            padx=10,
            pady=5,
            sticky="w"
        )


        # ====================================================
        # PAYMENT BILL TYPE
        # ====================================================

        self.create_label(
            "Receipt Bill Type:",
            17
        )

        self.payment_bill_type_var = ctk.StringVar(
            value="Software"
        )

        self.payment_bill_type_dropdown = ctk.CTkComboBox(
            self.form_frame,
            variable=self.payment_bill_type_var,
            values=BILL_TYPES,
            width=300,
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
            dropdown_hover_color=COLORS["primary_hover"],
            command=self.on_payment_bill_type_change
        )

        self.payment_bill_type_dropdown.grid(
            row=17,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )


        # ====================================================
        # MANUAL/TALLY RECEIPT NUMBER
        # ====================================================

        self.create_label(
            "Receipt Number:",
            18
        )

        self.receipt_number_entry = self.create_entry()

        self.receipt_number_entry.grid(
            row=18,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )


        # ====================================================
        # RECEIPT DATE
        # ====================================================

        self.create_label(
            "Receipt Date:",
            19
        )

        self.receipt_date_entry = self.create_entry(
            placeholder="DD-MM-YYYY"
        )

        self.receipt_date_entry.insert(
            0,
            date.today().strftime("%d-%m-%Y")
        )

        self.receipt_date_entry.grid(
            row=19,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )


        # ====================================================
        # PAYMENT AMOUNT
        # ====================================================

        self.create_label(
            "New Payment Amount:",
            20
        )

        self.payment_amount_entry = self.create_entry(
            width=300,
            placeholder="Enter amount received now"
        )

        self.payment_amount_entry.grid(
            row=20,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )


        # ====================================================
        # PAYMENT MODE
        # ====================================================

        self.create_label(
            "Payment Mode:",
            21
        )

        self.payment_mode_var = ctk.StringVar(
            value="Cash"
        )

        self.payment_mode_dropdown = ctk.CTkComboBox(
            self.form_frame,
            variable=self.payment_mode_var,
            values=PAYMENT_MODES,
            command=self.on_payment_mode_change,
            width=300,
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
            row=21,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )


        # ====================================================
        # CONDITIONAL PAYMENT FRAME
        # ====================================================

        self.payment_details_frame = ctk.CTkFrame(
            self.form_frame,
            fg_color="transparent"
        )

        self.payment_details_frame.grid(
            row=22,
            column=0,
            columnspan=2,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.create_payment_detail_fields()


        # ====================================================
        # PAYMENT NOTES
        # ====================================================

        self.create_label(
            "Payment Notes:",
            23
        )

        self.payment_notes_entry = self.create_entry(
            width=450,
            placeholder="Optional"
        )

        self.payment_notes_entry.grid(
            row=23,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )


        # ====================================================
        # RECORD PAYMENT
        # ====================================================

        self.receive_payment_btn = ctk.CTkButton(
            self.form_frame,
            text="Record Payment",
            command=self.record_payment,
            font=self.bold_font,
            height=SIZES["button_height"],
            width=SIZES["button_width"],
            fg_color=LOGOUT,
            hover_color=LOGOUT_HOVER,
            text_color=COLORS["toggle"]
        )

        self.receive_payment_btn.grid(
            row=24,
            column=1,
            padx=10,
            pady=15,
            sticky="w"
        )


        # ====================================================
        # PRINT RECEIPT
        # ====================================================

        self.print_receipt_btn = ctk.CTkButton(
            self.form_frame,
            text="Print / Save Latest Receipt PDF",
            command=self.print_latest_receipt,
            font=self.bold_font,
            height=SIZES["button_height"],
            width=SIZES["button_width"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            state="disabled"
        )

        self.print_receipt_btn.grid(
            row=25,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )


        # ====================================================
        # PAYMENT HISTORY
        # ====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="Payment History",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color=COLORS["primary"]
        ).grid(
            row=26,
            column=0,
            columnspan=2,
            pady=(30, 12),
            sticky="ew"
        )

        self.payment_history_frame = ctk.CTkScrollableFrame(
            self.form_frame,
            width=1000,
            height=280,
            fg_color=COLORS["card"],
            border_width=3,
            border_color=COLORS["border"]
        )

        self.payment_history_frame.grid(
            row=27,
            column=0,
            columnspan=2,
            padx=10,
            pady=10
        )


        # ====================================================
        # INITIAL STATE
        # ====================================================

        self.on_bill_type_change("Software")
        self.on_payment_bill_type_change("Software")
        self.on_payment_mode_change("Cash")
        self.on_pay_to_change(self.pay_to_var.get())


    # ========================================================
    # UI HELPERS
    # ========================================================

    def create_label(self, text, row):

        ctk.CTkLabel(
            self.form_frame,
            text=text,
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=row,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )


    def create_entry(
        self,
        width=300,
        placeholder=None
    ):

        return ctk.CTkEntry(
            self.form_frame,
            width=width,
            height=SIZES["entry_height"],
            font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            placeholder_text=placeholder
        )

    def normalize_billed_under(self, value):
        """
        Normalize billed-under values to the database codes:
            Sridharan    -> S
            Vijayalakshmi -> V
            S            -> S
            V            -> V
        """
        if value is None:
            return ""

        value = str(value).strip()

        mapping = {
            "S": "S",
            "V": "V",
            "SRIDHARAN": "S",
            "SRIDHARAN": "S",
            "VIJAYALAKSHMI": "V",
        }

        normalized = mapping.get(value.upper())

        if normalized:
            return normalized

        raise ValueError(
            f"Invalid billed-under value: {value}"
        )
    def create_department_fields(self):

        for widget in self.department_fields_frame.winfo_children():
            widget.destroy()

        self.department_vars = {}

        self.tds_quarter_vars = []
        self.tds_form_vars = []

        self.gst_month_vars = []
        self.gst_quarter_vars = []


        # ====================================================
        # FINANCIAL YEAR
        # ====================================================

        ctk.CTkLabel(
            self.department_fields_frame,
            text="Financial Year:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            padx=(0, 15),
            pady=8,
            sticky="w"
        )

        self.fin_year_var = ctk.StringVar(
            value="2025-26"
        )

        self.fin_year_dropdown = ctk.CTkComboBox(
            self.department_fields_frame,
            variable=self.fin_year_var,
            values=constants.FINANCIAL_YEARS,
            width=300,
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

        self.fin_year_dropdown.grid(
            row=0,
            column=1,
            padx=0,
            pady=8,
            sticky="w"
        )


        # ====================================================
        # TDS FRAME
        # ====================================================

        self.tds_frame = ctk.CTkFrame(
            self.department_fields_frame,
            fg_color="transparent"
        )


        # ====================================================
        # TDS QUARTERS
        # ====================================================

        ctk.CTkLabel(
            self.tds_frame,
            text="Quarter:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            padx=(0, 15),
            pady=8,
            sticky="nw"
        )

        quarter_frame = ctk.CTkFrame(
            self.tds_frame,
            fg_color="transparent"
        )

        quarter_frame.grid(
            row=0,
            column=1,
            sticky="w"
        )

        for idx, value in enumerate(QUARTERS):

            var = ctk.BooleanVar(value=False)

            self.tds_quarter_vars.append(
                (value, var)
            )

            ctk.CTkCheckBox(
                quarter_frame,
                text=value,
                variable=var,
                font=self.normal_font,
                text_color=COLORS["text"]
            ).grid(
                row=0,
                column=idx,
                padx=5
            )


        # ====================================================
        # TDS FORM TYPES
        # ====================================================

        ctk.CTkLabel(
            self.tds_frame,
            text="Form Type:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=1,
            column=0,
            padx=(0, 15),
            pady=8,
            sticky="nw"
        )

        form_frame = ctk.CTkFrame(
            self.tds_frame,
            fg_color="transparent"
        )

        form_frame.grid(
            row=1,
            column=1,
            sticky="w"
        )

        for idx, value in enumerate(constants.TDS_FORM_TYPES):

            var = ctk.BooleanVar(value=False)

            self.tds_form_vars.append(
                (value, var)
            )

            ctk.CTkCheckBox(
                form_frame,
                text=value,
                variable=var,
                font=self.normal_font,
                text_color=COLORS["text"]
            ).grid(
                row=0,
                column=idx,
                padx=5
            )


        # ====================================================
        # LOADING CHARGES
        # ====================================================

        ctk.CTkLabel(
            self.tds_frame,
            text="Loading Charges:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=2,
            column=0,
            padx=(0, 15),
            pady=8,
            sticky="w"
        )

        self.loading_charges_entry = ctk.CTkEntry(
            self.tds_frame,
            width=300,
            height=SIZES["entry_height"],
            font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"]
        )

        self.loading_charges_entry.grid(
            row=2,
            column=1,
            sticky="w"
        )


        # ====================================================
        # GST FRAME
        # ====================================================

        self.gst_frame = ctk.CTkFrame(
            self.department_fields_frame,
            fg_color="transparent"
        )


        # ====================================================
        # GST MONTHS
        # ====================================================

        ctk.CTkLabel(
            self.gst_frame,
            text="Month:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            padx=(0, 15),
            pady=8,
            sticky="nw"
        )

        month_frame = ctk.CTkScrollableFrame(
            self.gst_frame,
            width=500,
            height=100,
            fg_color=COLORS["input"]
        )

        month_frame.grid(
            row=0,
            column=1,
            sticky="w"
        )

        for idx, value in enumerate(MONTHS):

            var = ctk.BooleanVar(value=False)

            self.gst_month_vars.append(
                (value, var)
            )

            ctk.CTkCheckBox(
                month_frame,
                text=value,
                variable=var,
                font=self.normal_font,
                text_color=COLORS["text"]
            ).grid(
                row=idx // 4,
                column=idx % 4,
                padx=5,
                pady=3,
                sticky="w"
            )


        # ====================================================
        # GST QUARTERS
        # ====================================================

        ctk.CTkLabel(
            self.gst_frame,
            text="Quarter:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=1,
            column=0,
            padx=(0, 15),
            pady=8,
            sticky="nw"
        )

        gst_quarter_frame = ctk.CTkFrame(
            self.gst_frame,
            fg_color="transparent"
        )

        gst_quarter_frame.grid(
            row=1,
            column=1,
            sticky="w"
        )

        for idx, value in enumerate(QUARTERS):

            var = ctk.BooleanVar(value=False)

            self.gst_quarter_vars.append(
                (value, var)
            )

            ctk.CTkCheckBox(
                gst_quarter_frame,
                text=value,
                variable=var,
                font=self.normal_font,
                text_color=COLORS["text"]
            ).grid(
                row=0,
                column=idx,
                padx=5
            )


        # ====================================================
        # GST REGISTRATION FEE
        # ====================================================

        ctk.CTkLabel(
            self.gst_frame,
            text="GST Registration Fee:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=2,
            column=0,
            padx=(0, 15),
            pady=8,
            sticky="w"
        )

        self.gst_registration_fee_entry = ctk.CTkEntry(
            self.gst_frame,
            width=300,
            height=SIZES["entry_height"],
            font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"]
        )

        self.gst_registration_fee_entry.grid(
            row=2,
            column=1,
            sticky="w"
        )


        # ====================================================
        # IT / ACCOUNTS FRAME
        # ====================================================

        self.application_frame = ctk.CTkFrame(
            self.department_fields_frame,
            fg_color="transparent"
        )


        ctk.CTkLabel(
            self.application_frame,
            text="Application Type:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=0,
            column=0,
            padx=(0, 15),
            pady=8,
            sticky="w"
        )

        self.application_type_var = ctk.StringVar(
            value=None
        )

        self.application_type_dropdown = ctk.CTkComboBox(
            self.application_frame,
            variable=self.application_type_var,
            values=[
                "PAN Application",
                "TAN Application"
            ],
            width=300,
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

        self.application_type_dropdown.grid(
            row=0,
            column=1,
            sticky="w"
        )


        # ====================================================
        # NARRATIVE
        # ====================================================

        ctk.CTkLabel(
            self.department_fields_frame,
            text="Narrative:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=18,
            column=0,
            padx=(0, 15),
            pady=8,
            sticky="w"
        )

        self.narrative_var = ctk.StringVar(value="PAN Application")
        self.narrative_dropdown = ctk.CTkComboBox(
            self.department_fields_frame,
            variable=self.narrative_var,
            values=constants.NARRATIVE_VALUES,
            width=500,
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
        self.narrative_dropdown.grid(row=18, column=1, sticky="w")

        # ====================================================
        # PAY TO
        # ====================================================

        ctk.CTkLabel(
            self.department_fields_frame,
            text="Pay To:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=19,
            column=0,
            padx=(0, 15),
            pady=8,
            sticky="w"
        )

        self.pay_to_var = ctk.StringVar(value=constants.UPI_BANKS[0])
        self.pay_to_dropdown = ctk.CTkComboBox(
            self.department_fields_frame,
            variable=self.pay_to_var,
            values=constants.UPI_BANKS,
            command=self.on_pay_to_change,
            width=500,
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
        self.pay_to_dropdown.grid(row=19, column=1, sticky="w")

        self.pay_to_details_label = ctk.CTkLabel(
            self.department_fields_frame,
            text="",
            font=self.normal_font,
            text_color=COLORS["text_secondary"],
            justify="left",
            anchor="w"
        )
        self.pay_to_details_label.grid(
            row=19,
            column=2,
            padx=(10, 10),
            pady=8,
            sticky="w"
        )

        # ====================================================
        # REMARKS
        # ====================================================

        ctk.CTkLabel(
            self.department_fields_frame,
            text="Remarks:",
            font=self.label_font,
            text_color=COLORS["text"]
        ).grid(
            row=20,
            column=0,
            padx=(0, 15),
            pady=8,
            sticky="nw"
        )

        self.billing_remarks_entry = ctk.CTkEntry(
            self.department_fields_frame,
            width=500,
            height=SIZES["entry_height"],
            font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text="Optional"
        )

        self.billing_remarks_entry.grid(
            row=20,
            column=1,
            sticky="w"
        )


        self.show_department_fields()


    # ========================================================
    # PAYMENT CONDITIONAL FIELDS
    # ========================================================

    def create_payment_detail_fields(self):

        self.upi_bank_var = ctk.StringVar(
            value=None
        )

        self.bank_name_var = ctk.StringVar(
                    value=None
                )

        self.bank_transfer_mode_var = ctk.StringVar(
            value="NEFT"
        )

        self.cheque_number_entry = None
        self.cheque_date_entry = None

        self.render_payment_details("Cash")


    def render_payment_details(self, mode):

        for widget in self.payment_details_frame.winfo_children():
            widget.destroy()

        if mode == "UPI":

            ctk.CTkLabel(
                self.payment_details_frame,
                text="UPI Bank Account:",
                font=self.label_font,
                text_color=COLORS["text"]
            ).grid(
                row=0,
                column=0,
                padx=(0, 15),
                pady=8,
                sticky="w"
            )

            self.upi_bank_dropdown = ctk.CTkComboBox(
                self.payment_details_frame,
                variable=self.upi_bank_var,
                values=constants.UPI_BANKS,
                width=300,
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

            self.upi_bank_dropdown.grid(
                row=0,
                column=1,
                sticky="w"
            )


        elif mode == "Bank Transfer":
            ctk.CTkLabel(
                self.payment_details_frame,
                text="Bank Account:",
                font=self.label_font,
                text_color=COLORS["text"]
            ).grid(
                row=0,
                column=0,
                padx=(0, 15),
                pady=8,
                sticky="w"
            )

            self.bank_name_drop = ctk.CTkComboBox(
                self.payment_details_frame,
                variable=self.bank_name_var,
                values=constants.UPI_BANKS,
                width=300,
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

            self.bank_name_drop.grid(
                row=0,
                column=1,
                sticky="w"
            )

            ctk.CTkLabel(
                self.payment_details_frame,
                text="Transfer Mode:",
                font=self.label_font,
                text_color=COLORS["text"]
            ).grid(
                row=1,
                column=0,
                padx=(0, 15),
                pady=8,
                sticky="w"
            )

            self.bank_transfer_mode_dropdown = ctk.CTkComboBox(
                self.payment_details_frame,
                variable=self.bank_transfer_mode_var,
                values=BANK_TRANSFER_MODES,
                width=300,
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

            self.bank_transfer_mode_dropdown.grid(
                row=1,
                column=1,
                sticky="w"
            )


        elif mode == "Cheque":

            ctk.CTkLabel(
                self.payment_details_frame,
                text="Cheque Number:",
                font=self.label_font,
                text_color=COLORS["text"]
            ).grid(
                row=0,
                column=0,
                padx=(0, 15),
                pady=8,
                sticky="w"
            )

            self.cheque_number_entry = ctk.CTkEntry(
                self.payment_details_frame,
                width=300,
                height=SIZES["entry_height"],
                font=self.normal_font,
                fg_color=COLORS["input"],
                border_color=COLORS["border"],
                text_color=COLORS["text"]
            )

            self.cheque_number_entry.grid(
                row=0,
                column=1,
                sticky="w"
            )


            ctk.CTkLabel(
                self.payment_details_frame,
                text="Cheque Drawn On:",
                font=self.label_font,
                text_color=COLORS["text"]
            ).grid(
                row=1,
                column=0,
                padx=(0, 15),
                pady=8,
                sticky="w"
            )

            self.cheque_date_entry = ctk.CTkEntry(
                self.payment_details_frame,
                width=300,
                height=SIZES["entry_height"],
                font=self.normal_font,
                fg_color=COLORS["input"],
                border_color=COLORS["border"],
                text_color=COLORS["text"],
                placeholder_text="DD-MM-YYYY"
            )

            self.cheque_date_entry.grid(
                row=1,
                column=1,
                sticky="w"
            )


    # ========================================================
    # PAYMENT MODE CHANGE
    # ========================================================

    def on_payment_mode_change(self, choice):

        self.render_payment_details(
            choice
        )


    # ========================================================
    # PAYMENT BILL TYPE
    # ========================================================

    def on_payment_bill_type_change(self, choice):

        if choice == "Software":

            self.receipt_number_entry.configure(
                state="disabled"
            )

            self.receipt_number_entry.delete(
                0,
                "end"
            )

            self.receipt_number_entry.insert(
                0,
                "Will be generated automatically"
            )

        else:

            self.receipt_number_entry.configure(
                state="normal"
            )

            self.receipt_number_entry.delete(
                0,
                "end"
            )


    # ========================================================
    # DATE CONVERSION
    # ========================================================

    @staticmethod
    def format_date_for_display(db_date):

        if not db_date:
            return ""

        if isinstance(db_date, datetime):
            return db_date.strftime("%d-%m-%Y")

        if isinstance(db_date, date):
            return db_date.strftime("%d-%m-%Y")

        try:

            return datetime.strptime(
                str(db_date),
                "%Y-%m-%d"
            ).strftime("%d-%m-%Y")

        except ValueError:

            return str(db_date)


    @staticmethod
    def format_date_for_database(display_date):

        if not display_date:
            return None

        try:

            return datetime.strptime(
                str(display_date).strip(),
                "%d-%m-%Y"
            ).date()

        except ValueError:

            return None


    # ========================================================
    # MONEY
    # ========================================================

    @staticmethod
    def money(value):

        if value is None:
            return Decimal("0.00")

        try:

            return Decimal(
                str(value)
            ).quantize(
                Decimal("0.01")
            )

        except (
            InvalidOperation,
            ValueError
        ):

            return Decimal("0.00")


    # ========================================================
    # MULTI SELECT
    # ========================================================

    @staticmethod
    def selected_values(items):

        return [
            value
            for value, variable in items
            if variable.get()
        ]


    # ========================================================
    # DEPARTMENT
    # ========================================================

    def get_department(self):

        if not self.current_task_id:
            return ""

        conn = get_connection()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT department
                FROM tasks
                WHERE id = %s
            """, (
                self.current_task_id,
            ))

            row = cursor.fetchone()

            return (
                (row[0] or "").strip()
                if row
                else ""
            )

        finally:

            conn.close()


    # ========================================================
    # SHOW DEPARTMENT FIELDS
    # ========================================================

    def show_department_fields(self):

        department = self.get_department().upper()


        self.tds_frame.grid_remove()
        self.gst_frame.grid_remove()
        self.application_frame.grid_remove()


        if department == "TDS":

            self.tds_frame.grid(
                row=1,
                column=0,
                columnspan=2,
                sticky="w"
            )

        elif department == "GST":

            self.gst_frame.grid(
                row=1,
                column=0,
                columnspan=2,
                sticky="w"
            )

        elif department in (
            "IT",
            "ACCOUNTS"
        ):

            self.application_frame.grid(
                row=1,
                column=0,
                columnspan=2,
                sticky="w"
            )


    # ========================================================
    # BILL TYPE CHANGE
    # ========================================================

    def on_bill_type_change(self, choice):

        if choice not in BILL_TYPES:
            return

        if choice == "Software":

            self.bill_num_entry.configure(
                state="disabled"
            )

            self.bill_date_entry.configure(
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
                    "Software bill number is generated "
                    "automatically when saved."
                )
            )

        else:

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

            self.bill_date_entry.insert(
                0,
                date.today().strftime("%d-%m-%Y")
            )

            self.bill_info_label.configure(
                text=(
                    f"{choice} bill: enter the external "
                    "bill number and date."
                )
            )


    # ========================================================
    # BILLED UNDER CHANGE
    # ========================================================

    def on_pay_to_change(self, choice):
        details = constants.BANK_DETAILS.get(choice, {})
        if not details:
            self.pay_to_details_label.configure(text="Bank details not configured.")
            return
        self.pay_to_details_label.configure(
            text=(
                f"Bank: {details.get('bank_name', '-')}\n"
                f"IFSC: {details.get('ifsc', '-')}\n"
                f"Branch: {details.get('branch', '-')}\n"
                f"A/C No.: {details.get('account_number', '-')}\n"
                f"A/C Holder: {details.get('account_holder_name', '-')}\n"
                f"UPI ID: {details.get('upi_id', '-')}"
            )
        )


    def on_billed_under_change(self, choice):

        if choice not in BILLED_UNDER:
            return


    # ========================================================
    # LOAD RECORDS
    # ========================================================

    def load_records(
        self,
        selected_record_id=None
    ):

        conn = get_connection()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    t.id,
                    c.name,
                    t.department,
                    t.task_name,
                    t.status,
                    t.bill_number,
                    t.bill_amount,
                    t.amount_pending_receipt
                FROM tasks t
                LEFT JOIN clients c
                    ON t.client_id = c.id
                WHERE t.status in (1,2)
                ORDER BY t.id DESC
            """)

            records = cursor.fetchall()

        finally:

            conn.close()


        self.case_map = {}

        display_values = []


        for record in records:

            (
                task_id,
                client_name,
                department,
                task_name,
                status,
                bill_number,
                bill_amount,
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
                f"ID: {task_id} | "
                f"{client_name or '-'} | "
                f"{department or '-'} | "
                f"{task_name or '-'} | "
                f"{status_text} | "
                f"Bill: "
                f"{bill_number or 'Not Generated'} | "
                f"Rs.{self.money(bill_amount):.2f} | "
                f"Balance: "
                f"Rs.{self.money(pending):.2f}"
            )


            self.case_map[
                display
            ] = task_id

            display_values.append(
                display
            )


        if display_values:

            self.case_dropdown.configure_values(
                display_values
            )

            selected_display = display_values[0]


            if selected_record_id is not None:

                for display_text, task_id in self.case_map.items():

                    if task_id == selected_record_id:

                        selected_display = display_text
                        break


            self.case_dropdown.set(
                selected_display
            )

            self.load_selected_record(
                selected_display
            )

        else:

            self.current_task_id = None

            self.case_dropdown.set(
                "No work available"
            )

            self.clear_bill_display()


    # ========================================================
    # LOAD SELECTED RECORD
    # ========================================================

    def load_selected_record(
        self,
        choice=None
    ):

        if choice is None:

            choice = self.case_var.get()


        task_id = self.case_map.get(
            choice
        )


        if not task_id:
            return


        self.current_task_id = task_id


        conn = get_connection()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    t.status,
                    t.department,
                    t.bill_type,
                    t.billed_under,
                    t.bill_number,
                    t.bill_date,
                    t.bill_amount,
                    t.actual_amount_received,
                    t.amount_pending_receipt,
                    t.billing_fin_year,
                    t.billing_quarters,
                    t.billing_form_types,
                    t.billing_months,
                    t.loading_charges,
                    t.gst_registration_fee,
                    t.application_type,
                    t.billing_remarks,
                    t.billing_narrative,
                    t.pay_to
                FROM tasks t
                WHERE t.id = %s
            """, (
                task_id,
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
            pending,
            fin_year,
            quarters,
            form_types,
            months,
            loading_charges,
            gst_registration_fee,
            application_type,
            remarks,
            narrative,
            pay_to
        ) = record


        # ====================================================
        # STATUS
        # ====================================================

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


        # ====================================================
        # DEPARTMENT
        # ====================================================

        self.show_department_fields()


        # ====================================================
        # BILL TYPE
        # ====================================================

        self.bill_type_var.set(
            bill_type or "Software"
        )


        self.payment_bill_type_var.set(
            bill_type or "Software"
        )


        # ====================================================
        # BILLED UNDER
        # ====================================================

        billed_under_display = {
            "S": "Sridharan",
            "V": "V"
        }.get(
            str(billed_under or "").strip().upper(),
            "Sridharan"
        )

        self.billed_under_var.set(
            billed_under_display
        )


        # ====================================================
        # AMOUNTS
        # ====================================================

        total = self.money(
            bill_amount
        )

        received = self.money(
            actual_received
        )

        calculated_pending = max(
            Decimal("0.00"),
            total - received
        )


        self.total_bill_label.configure(
            text=f"Rs.{total:.2f}"
        )

        self.received_label.configure(
            text=f"Rs.{received:.2f}"
        )

        self.pending_label.configure(
            text=f"Rs.{calculated_pending:.2f}"
        )


        # ====================================================
        # BILL DETAILS
        # ====================================================

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


        if bill_number:

            self.bill_num_entry.insert(
                0,
                bill_number
            )

            self.bill_num_entry.configure(
                state="disabled"
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


            self.save_bill_btn.configure(
                state="disabled",
                text="Bill Already Generated"
            )

            self.print_bill_btn.configure(
                state="normal"
            )

            self.bill_info_label.configure(
                text=(
                    f"Bill generated: {bill_number}"
                )
            )

        else:

            self.bill_type_var.set(
                bill_type or "Software"
            )

            self.on_bill_type_change(
                bill_type or "Software"
            )

            self.save_bill_btn.configure(
                state="normal",
                text="Generate / Save Bill"
            )

            self.print_bill_btn.configure(
                state="disabled"
            )


        # ====================================================
        # BILL AMOUNT
        # ====================================================

        self.bill_amt_entry.delete(
            0,
            "end"
        )

        if total > 0:

            self.bill_amt_entry.insert(
                0,
                f"{total:.2f}"
            )


        # ====================================================
        # DEPARTMENT VALUES
        # ====================================================

        self.fin_year_var.set(
            fin_year or "2025-26"
        )


        self.set_multi_select(
            self.tds_quarter_vars,
            quarters or []
        )

        self.set_multi_select(
            self.tds_form_vars,
            form_types or []
        )

        self.set_multi_select(
            self.gst_month_vars,
            months or []
        )

        self.set_multi_select(
            self.gst_quarter_vars,
            quarters or []
        )


        self.loading_charges_entry.delete(
            0,
            "end"
        )

        if self.money(loading_charges) > 0:

            self.loading_charges_entry.insert(
                0,
                f"{self.money(loading_charges):.2f}"
            )


        self.gst_registration_fee_entry.delete(
            0,
            "end"
        )

        if self.money(gst_registration_fee) > 0:

            self.gst_registration_fee_entry.insert(
                0,
                f"{self.money(gst_registration_fee):.2f}"
            )


        if application_type:

            self.application_type_var.set(
                application_type
            )


        self.billing_remarks_entry.delete(
            0,
            "end"
        )

        if remarks:

            self.billing_remarks_entry.insert(
                0,
                remarks
            )

        self.narrative_var.set(narrative or "PAN Application")
        self.pay_to_var.set(pay_to if pay_to in constants.UPI_BANKS else constants.UPI_BANKS[0])
        self.on_pay_to_change(self.pay_to_var.get())


        # ====================================================
        # PAYMENT ENTRY
        # ====================================================

        self.payment_amount_entry.delete(
            0,
            "end"
        )


        # ====================================================
        # HISTORY
        # ====================================================

        self.load_payment_history(
            task_id
        )


    # ========================================================
    # MULTI SELECT RESTORE
    # ========================================================

    @staticmethod
    def set_multi_select(
        items,
        selected
    ):

        selected = set(
            selected or []
        )

        for value, variable in items:

            variable.set(
                value in selected
            )


    # ========================================================
    # CLEAR
    # ========================================================

    def clear_bill_display(self):

        self.current_task_id = None

        self.status_label.configure(
            text="-"
        )

        self.total_bill_label.configure(
            text="Rs.0.00"
        )

        self.received_label.configure(
            text="Rs.0.00"
        )

        self.pending_label.configure(
            text="Rs.0.00"
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

        self.narrative_var.set("PAN Application")
        self.pay_to_var.set(constants.UPI_BANKS[0])
        self.on_pay_to_change(self.pay_to_var.get())

        self.save_bill_btn.configure(
            state="normal",
            text="Generate / Save Bill"
        )

        self.print_bill_btn.configure(
            state="disabled"
        )


    # ========================================================
    # GENERATE SOFTWARE BILL NUMBER
    # ========================================================

    def generate_software_bill_number(
        self,
        department,
        billed_under,
        cursor
    ):

        department = (
            department or ""
        ).strip().upper()

        billed_under = self.normalize_billed_under(
        billed_under[0]
    )


        if not department:

            raise ValueError(
                "Department is missing."
            )


        if billed_under not in ("S", "V"):

            raise ValueError(
                "Invalid billed-under value."
            )


        # ====================================================
        # PostgreSQL row lock
        # ====================================================

        cursor.execute("""
            SELECT last_number
            FROM bill_sequences
            WHERE department = %s
              AND billed_under = %s
            FOR UPDATE
        """, (
            department,
            billed_under
        ))


        row = cursor.fetchone()


        if row:

            next_number = int(
                row[0]
            ) + 1

            cursor.execute("""
                UPDATE bill_sequences
                SET last_number = %s
                WHERE department = %s
                  AND billed_under = %s
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
                VALUES (%s, %s, %s)
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


    # ========================================================
    # GENERATE PAYMENT RECEIPT NUMBER
    # ========================================================

    def generate_payment_receipt_number(
        self,
        department,
        billed_under,
        cursor
    ):

        department = (
            department or ""
        ).strip().upper()

        billed_under = self.normalize_billed_under(
        billed_under[0]
    )


        cursor.execute("""
            SELECT last_number
            FROM payment_receipt_sequences
            WHERE department = %s
              AND billed_under = %s
            FOR UPDATE
        """, (
            department,
            billed_under
        ))


        row = cursor.fetchone()


        if row:

            next_number = int(
                row[0]
            ) + 1

            cursor.execute("""
                UPDATE payment_receipt_sequences
                SET last_number = %s
                WHERE department = %s
                  AND billed_under = %s
            """, (
                next_number,
                department,
                billed_under
            ))

        else:

            next_number = 1

            cursor.execute("""
                INSERT INTO payment_receipt_sequences (
                    department,
                    billed_under,
                    last_number
                )
                VALUES (%s, %s, %s)
            """, (
                department,
                billed_under,
                next_number
            ))


        return (
            f"R"
            f"{billed_under}"
            f"{department}"
            f"{next_number}"
        )


    # ========================================================
    # SAVE BILL
    # ========================================================

    def save_bill(self):

        task_id = self.current_task_id


        if not task_id:

            messagebox.showerror(
                "Error",
                "Please select a valid work record."
            )

            return


        conn = get_connection()


        try:

            cursor = conn.cursor()


            # =================================================
            # CURRENT TASK
            # =================================================

            cursor.execute("""
                SELECT
                    status,
                    department,
                    bill_number,
                    actual_amount_received
                FROM tasks
                WHERE id = %s
                FOR UPDATE
            """, (
                task_id,
            ))


            record = cursor.fetchone()


            if not record:

                messagebox.showerror(
                    "Error",
                    "Task not found."
                )

                return


            (
                status,
                department,
                existing_bill_number,
                received
            ) = record


            department = (
                department or ""
            ).strip().upper()


            # =================================================
            # ALREADY BILLED
            # =================================================

            if existing_bill_number:

                messagebox.showerror(
                    "Bill Already Generated",
                    (
                        f"This task already has bill "
                        f"{existing_bill_number}."
                    )
                )

                return


            # =================================================
            # STATUS
            # =================================================

            if status < 1:

                messagebox.showerror(
                    "Error",
                    (
                        "Billing is available only after "
                        "the work is completed."
                    )
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


            if bill_type not in BILL_TYPES:

                messagebox.showerror(
                    "Error",
                    "Please select a valid bill type."
                )

                return


            # =================================================
            # BILLED UNDER
            # =================================================

            try:
                billed_under = self.normalize_billed_under(
                    self.billed_under_var.get()
                )
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Please select a valid billed-under value."
                )
                return


            # =================================================
            # TOTAL BILL AMOUNT
            # =================================================

            bill_amount_text = (
                self.bill_amt_entry
                .get()
                .strip()
            )


            if not bill_amount_text:

                messagebox.showerror(
                    "Error",
                    "Total Bill Amount is required."
                )

                return


            try:

                bill_amount = Decimal(
                    bill_amount_text
                ).quantize(
                    Decimal("0.01")
                )

            except InvalidOperation:

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


            received = self.money(
                received
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
            # FINANCIAL YEAR
            # =================================================

            fin_year = (
                self.fin_year_var
                .get()
                .strip()
            )


            if department in (
                "TDS",
                "GST",
                "IT",
                "ACCOUNTS"
            ):

                if not fin_year:

                    messagebox.showerror(
                        "Error",
                        "Financial Year is required."
                    )

                    return


            # =================================================
            # TDS
            # =================================================

            quarters = []
            form_types = []


            if department == "TDS":

                quarters = self.selected_values(
                    self.tds_quarter_vars
                )

                form_types = self.selected_values(
                    self.tds_form_vars
                )


                if not quarters:

                    messagebox.showerror(
                        "Error",
                        "Select at least one TDS quarter."
                    )

                    return


                if not form_types:

                    messagebox.showerror(
                        "Error",
                        "Select at least one TDS form type."
                    )

                    return


            # =================================================
            # GST
            # =================================================

            months = []
            gst_quarters = []


            if department == "GST":

                months = self.selected_values(
                    self.gst_month_vars
                )

                gst_quarters = self.selected_values(
                    self.gst_quarter_vars
                )


                # Both are optional.


            # =================================================
            # LOADING CHARGES
            # =================================================

            loading_text = (
                self.loading_charges_entry
                .get()
                .strip()
            )


            if loading_text:

                try:

                    loading_charges = Decimal(
                        loading_text
                    ).quantize(
                        Decimal("0.01")
                    )

                except InvalidOperation:

                    messagebox.showerror(
                        "Error",
                        "Invalid loading charges."
                    )

                    return

            else:

                loading_charges = Decimal("0.00")


            if loading_charges < 0:

                messagebox.showerror(
                    "Error",
                    "Loading charges cannot be negative."
                )

                return


            # =================================================
            # GST REGISTRATION FEE
            # =================================================

            gst_fee_text = (
                self.gst_registration_fee_entry
                .get()
                .strip()
            )


            if gst_fee_text:

                try:

                    gst_registration_fee = Decimal(
                        gst_fee_text
                    ).quantize(
                        Decimal("0.01")
                    )

                except InvalidOperation:

                    messagebox.showerror(
                        "Error",
                        "Invalid GST registration fee."
                    )

                    return

            else:

                gst_registration_fee = Decimal(
                    "0.00"
                )


            if gst_registration_fee < 0:

                messagebox.showerror(
                    "Error",
                    "GST registration fee cannot be negative."
                )

                return


            # =================================================
            # APPLICATION
            # =================================================

            application_type = None


            if department in (
                "IT",
                "ACCOUNTS"
            ):

                application_type = (
                    self.application_type_var
                    .get()
                    .strip()
                )


            # =================================================
            # REMARKS
            # =================================================

            remarks = (
                self.billing_remarks_entry
                .get()
                .strip()
            )

            narrative = self.narrative_var.get().strip()
            if not narrative:
                messagebox.showerror("Error", "Narrative is required.")
                return

            pay_to = self.pay_to_var.get().strip()
            if pay_to not in constants.UPI_BANKS:
                messagebox.showerror("Error", "Please select a valid Pay To bank.")
                return


            # =================================================
            # BILL DATE / NUMBER
            # =================================================

            if bill_type == "Software":

                bill_number = (
                    self.generate_software_bill_number(
                        department,
                        billed_under,
                        cursor
                    )
                )

                bill_date = date.today()

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
                        "Bill Number is required."
                    )

                    return


                if not bill_date_display:

                    messagebox.showerror(
                        "Error",
                        "Bill Date is required."
                    )

                    return


                bill_date = (
                    self.format_date_for_database(
                        bill_date_display
                    )
                )


                if bill_date is None:

                    messagebox.showerror(
                        "Invalid Bill Date",
                        "Use DD-MM-YYYY."
                    )

                    return


                # Add S/V if not already present.

                if not bill_number.upper().startswith(
                    billed_under
                ):

                    bill_number = (
                        billed_under
                        + bill_number
                    )


            # =================================================
            # DUPLICATE BILL
            # =================================================

            cursor.execute("""
                SELECT id
                FROM tasks
                WHERE bill_number = %s
                  AND id != %s
            """, (
                bill_number,
                task_id
            ))


            if cursor.fetchone():

                messagebox.showerror(
                    "Duplicate Bill",
                    (
                        f"Bill number '{bill_number}' "
                        "already exists."
                    )
                )

                return


            # =================================================
            # SAVE
            # =================================================

            now = datetime.now()


            cursor.execute("""
                UPDATE tasks
                SET
                    bill_raised = TRUE,
                    bill_type = %s,
                    billed_under = %s,
                    bill_number = %s,
                    bill_date = %s,
                    bill_amount = %s,
                    amount_pending_receipt = %s,
                    billing_fin_year = %s,
                    billing_quarters = %s,
                    billing_form_types = %s,
                    billing_months = %s,
                    loading_charges = %s,
                    gst_registration_fee = %s,
                    application_type = %s,
                    billing_remarks = %s,
                    billing_narrative = %s,
                    pay_to = %s,
                    bill_raised_by = %s,
                    bill_raised_at = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
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
                fin_year or None,
                quarters or None,
                form_types or None,
                months or gst_quarters or None,
                loading_charges,
                gst_registration_fee,
                application_type,
                remarks or None,
                narrative,
                pay_to,
                self.user["id"],
                now,
                task_id
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
                    task_id,
                    action_type,
                    performed_by,
                    amount,
                    description
                )
                VALUES (
                    %s,
                    'BILL_RAISED',
                    %s,
                    %s,
                    %s
                )
            """, (
                task_id,
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
                "Bill generated successfully.\n\n"
                f"Bill Type: {bill_type}\n"
                f"Bill Number: {bill_number}\n"
                f"Bill Date: "
                f"{self.format_date_for_display(bill_date)}\n"
                f"Bill Amount: Rs.{bill_amount:.2f}\n"
                f"Loading Charges: Rs.{loading_charges:.2f}\n"
                f"GST Registration Fee: "
                f"Rs.{gst_registration_fee:.2f}\n"
                f"Balance: Rs.{pending:.2f}"
            )
        )


        self.load_records(
            selected_record_id=task_id
        )


        # =====================================================
        # AUTOMATIC PDF SAVE PROMPT
        # =====================================================

        self.print_bill()


    # ========================================================
    # RECORD PAYMENT
    # ========================================================

    def record_payment(self):

        task_id = self.current_task_id


        if not task_id:

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

            amount = Decimal(
                amount_text
            ).quantize(
                Decimal("0.01")
            )

        except InvalidOperation:

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


        if payment_mode not in PAYMENT_MODES:

            messagebox.showerror(
                "Error",
                "Select a valid payment mode."
            )

            return


        # ====================================================
        # PAYMENT BILL TYPE
        # ====================================================

        receipt_type = (
            self.payment_bill_type_var
            .get()
            .strip()
        )


        # ====================================================
        # RECEIPT DATE
        # ====================================================

        receipt_date_display = (
            self.receipt_date_entry
            .get()
            .strip()
        )


        receipt_date = (
            self.format_date_for_database(
                receipt_date_display
            )
        )


        if receipt_date is None:

            messagebox.showerror(
                "Invalid Receipt Date",
                "Use DD-MM-YYYY."
            )

            return


        # ====================================================
        # PAYMENT DATE
        #
        # Main payment date uses today's date.
        # For bank transfer and cheque, the specific
        # instrument date is stored separately.
        # ====================================================

        payment_date = date.today()


        notes = (
            self.payment_notes_entry
            .get()
            .strip()
        )


        # ====================================================
        # CONDITIONAL DETAILS
        # ====================================================

        upi_bank = None
        bank_name = None
        bank_transfer_mode = None
        cheque_number = None
        cheque_date = None


        if payment_mode == "UPI":

            upi_bank = (
                self.upi_bank_var
                .get()
                .strip()
            )


            if not upi_bank:

                messagebox.showerror(
                    "Error",
                    "Select the UPI bank account."
                )

                return


        elif payment_mode == "Bank Transfer":
            bank_name = (
                            self.bank_name_var
                            .get()
                            .strip()
                        )
            
            
            if not bank_name:
            
                            messagebox.showerror(
                                "Error",
                                "Select the bank account."
                            )
            
                            return

            # if self.bank_name_entry is None:

            #     messagebox.showerror(
            #         "Error",
            #         "Enter the bank name."
            #     )

            #     return


            # bank_name = (
            #     self.bank_name_entry
            #     .get()
            #     .strip()
            # )


            # if not bank_name:

            #     messagebox.showerror(
            #         "Error",
            #         "Bank name is required."
            #     )

            #     return


            bank_transfer_mode = (
                self.bank_transfer_mode_var
                .get()
                .strip()
            )


            if bank_transfer_mode not in BANK_TRANSFER_MODES:

                messagebox.showerror(
                    "Error",
                    "Select NEFT, RTGS or Cash Deposit."
                )

                return


        elif payment_mode == "Cheque":

            cheque_number = (
                self.cheque_number_entry
                .get()
                .strip()
                if self.cheque_number_entry
                else ""
            )


            cheque_date_display = (
                self.cheque_date_entry
                .get()
                .strip()
                if self.cheque_date_entry
                else ""
            )


            if not cheque_number:

                messagebox.showerror(
                    "Error",
                    "Cheque number is required."
                )

                return


            cheque_date = (
                self.format_date_for_database(
                    cheque_date_display
                )
            )


            if cheque_date is None:

                messagebox.showerror(
                    "Invalid Cheque Date",
                    "Use DD-MM-YYYY."
                )

                return


        conn = get_connection()


        try:

            cursor = conn.cursor()


            # =================================================
            # LOCK TASK
            # =================================================

            cursor.execute("""
                SELECT
                    department,
                    billed_under,
                    bill_number,
                    bill_amount,
                    actual_amount_received
                FROM tasks
                WHERE id = %s
                FOR UPDATE
            """, (
                task_id,
            ))


            record = cursor.fetchone()


            if not record:

                messagebox.showerror(
                    "Error",
                    "Task not found."
                )

                return


            (
                department,
                billed_under,
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
                    (
                        "Generate the bill before "
                        "recording a payment."
                    )
                )

                return


            bill_amount = self.money(
                bill_amount
            )

            current_received = self.money(
                current_received
            )


            balance = (
                bill_amount
                - current_received
            )


            if amount > balance:

                messagebox.showerror(
                    "Error",
                    (
                        "Payment is greater than "
                        "the outstanding balance.\n\n"
                        f"Balance available: "
                        f"Rs.{balance:.2f}"
                    )
                )

                return


            # =================================================
            # RECEIPT NUMBER
            # =================================================

            if receipt_type == "Software":

                receipt_number = (
                    self.generate_payment_receipt_number(
                        department,
                        billed_under or "Sridharan",
                        cursor
                    )
                )

                receipt_date = date.today()

            else:

                receipt_number = (
                    self.receipt_number_entry
                    .get()
                    .strip()
                )


                if not receipt_number:

                    messagebox.showerror(
                        "Error",
                        (
                            "Receipt number is required "
                            "for Manual/Tally."
                        )
                    )

                    return


                cursor.execute("""
                    SELECT id
                    FROM payment_transactions
                    WHERE receipt_number = %s
                """, (
                    receipt_number,
                ))


                if cursor.fetchone():

                    messagebox.showerror(
                        "Duplicate Receipt",
                        (
                            f"Receipt number "
                            f"'{receipt_number}' already exists."
                        )
                    )

                    return


            # =================================================
            # NEW TOTALS
            # =================================================

            new_received = (
                current_received + amount
            )

            new_pending = (
                bill_amount - new_received
            )


            if abs(new_pending) < Decimal("0.01"):

                new_pending = Decimal("0.00")


            # =================================================
            # PAYMENT
            # =================================================

            cursor.execute("""
                INSERT INTO payment_transactions (
                    task_id,
                    amount,
                    payment_mode,
                    payment_date,
                    received_by,
                    notes,
                    receipt_type,
                    receipt_number,
                    receipt_date,
                    upi_bank,
                    bank_name,
                    bank_transfer_mode,
                    cheque_number,
                    cheque_date
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
                RETURNING id
            """, (
                task_id,
                amount,
                payment_mode,
                payment_date,
                self.user["id"],
                notes or None,
                receipt_type,
                receipt_number,
                receipt_date,
                upi_bank,
                bank_name,
                bank_transfer_mode,
                cheque_number,
                cheque_date
            ))
            
            payment_id = cursor.fetchone()[0]

            self.latest_receipt_id = payment_id
            self.print_receipt_btn.configure(
    state="normal"
)


            # =================================================
            # UPDATE TASK
            # =================================================

            cursor.execute("""
                UPDATE tasks
                SET
                    actual_amount_received = %s,
                    amount_pending_receipt = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (
                new_received,
                new_pending,
                task_id
            ))


            # =================================================
            # ACTIVITY LOG
            # =================================================

            cursor.execute("""
                INSERT INTO activity_log (
                    task_id,
                    action_type,
                    performed_by,
                    amount,
                    payment_mode,
                    description
                )
                VALUES (
                    %s,
                    'PAYMENT_RECEIVED',
                    %s,
                    %s,
                    %s,
                    %s
                )
            """, (
                task_id,
                self.user["id"],
                amount,
                payment_mode,
                (
                    f"Receipt {receipt_number}. "
                    f"{notes or 'Payment received'}"
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
            "Payment Recorded",
            (
                f"Payment received: Rs.{amount:.2f}\n\n"
                f"Receipt Number: {receipt_number}\n"
                f"Total received: Rs.{new_received:.2f}\n"
                f"Remaining Amount to Be Paid: Rs.{new_pending:.2f}"
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


        self.latest_receipt_id = payment_id


        self.load_records(
            selected_record_id=task_id
        )


        # =====================================================
        # SAVE / PRINT RECEIPT PDF
        # =====================================================

        self.print_latest_receipt()


    # ========================================================
    # PAYMENT HISTORY
    # ========================================================

    def load_payment_history(
        self,
        task_id
    ):

        for widget in self.payment_history_frame.winfo_children():

            widget.destroy()


        conn = get_connection()


        try:

            cursor = conn.cursor()


            cursor.execute("""
                SELECT
                    p.id,
                    p.payment_date,
                    p.amount,
                    p.payment_mode,
                    p.receipt_number,
                    p.receipt_type,
                    p.upi_bank,
                    p.bank_name,
                    p.bank_transfer_mode,
                    p.cheque_number,
                    p.cheque_date,
                    u.username,
                    p.notes
                FROM payment_transactions p
                LEFT JOIN users u
                    ON p.received_by = u.id
                WHERE p.task_id = %s
                ORDER BY p.id DESC
            """, (
                task_id,
            ))


            payments = cursor.fetchall()


        finally:

            conn.close()


        headers = [
            "ID",
            "Date",
            "Amount",
            "Mode",
            "Receipt",
            "Details",
            "Received By",
            "Notes"
        ]


        for col, header in enumerate(headers):

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


        if not payments:

            ctk.CTkLabel(
                self.payment_history_frame,
                text="No payments recorded yet.",
                font=self.normal_font,
                text_color=COLORS["text_secondary"]
            ).grid(
                row=1,
                column=0,
                columnspan=len(headers),
                padx=10,
                pady=10
            )

            return


        for row_idx, payment in enumerate(
            payments,
            start=1
        ):

            (
                payment_id,
                payment_date,
                amount,
                mode,
                receipt_number,
                receipt_type,
                upi_bank,
                bank_name,
                bank_transfer_mode,
                cheque_number,
                cheque_date,
                received_by,
                notes
            ) = payment


            details = "-"


            if mode == "UPI":

                details = (
                    f"UPI: {upi_bank or '-'}"
                )

            elif mode == "Bank Transfer":

                details = (
                    f"{bank_name or '-'} / "
                    f"{bank_transfer_mode or '-'}"
                )

            elif mode == "Cheque":

                details = (
                    f"Cheque: "
                    f"{cheque_number or '-'} / "
                    f"{self.format_date_for_display(cheque_date)}"
                )


            values = [
                payment_id,
                self.format_date_for_display(
                    payment_date
                ),
                f"Rs.{self.money(amount):.2f}",
                mode,
                receipt_number or "-",
                details,
                received_by or "-",
                notes or "-"
            ]


            for col_idx, value in enumerate(values):

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


    # ========================================================
    # PRINT BILL
    # ========================================================

    def print_bill(self):

        if not self.current_task_id:

            messagebox.showerror(
                "Error",
                "Please select a task."
            )

            return


        conn = get_connection()


        try:

            cursor = conn.cursor()


            cursor.execute("""
                SELECT
                    t.id,
                    t.task_name,
                    t.task_details,
                    t.department,
                    t.billed_under,
                    t.bill_type,
                    t.bill_number,
                    t.bill_date,
                    t.bill_amount,
                    t.actual_amount_received,
                    t.amount_pending_receipt,
                    t.billing_fin_year,
                    t.billing_quarters,
                    t.billing_form_types,
                    t.billing_months,
                    t.loading_charges,
                    t.gst_registration_fee,
                    t.application_type,
                    t.billing_remarks,
                    t.billing_narrative,
                    t.pay_to,
                    c.name,
                    c.mobile,
                    c.email,
                    c.address,
                    c.pan,
                    c.tan,
                    c.gst
                FROM tasks t
                LEFT JOIN clients c
                    ON t.client_id = c.id
                WHERE t.id = %s
            """, (
                self.current_task_id,
            ))


            task = cursor.fetchone()


        finally:

            conn.close()


        if not task:

            messagebox.showerror(
                "Error",
                "Task not found."
            )

            return


        if not task[6]:

            messagebox.showerror(
                "Bill Not Generated",
                "Generate the bill first."
            )

            return


        default_name = (
            f"Bill_{task[6]}.pdf"
        )


        filepath = filedialog.asksaveasfilename(
            title="Save Bill PDF",
            defaultextension=".pdf",
            initialfile=default_name,
            filetypes=[
                ("PDF files", "*.pdf")
            ]
        )


        if not filepath:
            return


        try:

            self.create_bill_pdf(
                task,
                filepath
            )

            messagebox.showinfo(
                "PDF Created",
                (
                    "Bill PDF created successfully.\n\n"
                    f"{filepath}"
                )
            )

        except Exception as e:

            messagebox.showerror(
                "PDF Error",
                str(e)
            )


    # ========================================================
    # CREATE BILL PDF
    # ========================================================

    def create_bill_pdf(
        self,
        task,
        filepath
    ):

        (
            task_id,
            task_name,
            task_details,
            department,
            billed_under,
            bill_type,
            bill_number,
            bill_date,
            bill_amount,
            actual_received,
            pending,
            fin_year,
            quarters,
            form_types,
            months,
            loading_charges,
            gst_registration_fee,
            application_type,
            remarks,
            narrative,
            pay_to,
            client_name,
            client_mobile,
            client_email,
            client_address,
            client_pan,
            client_tan,
            client_gst
        ) = task

        styles = getSampleStyleSheet()

        # ====================================================
        # STYLES
        # ====================================================

        title_style = ParagraphStyle(
            "InvoiceTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=18,
            leading=22,
            spaceAfter=10
        )

        heading_style = ParagraphStyle(
            "Heading",
            parent=styles["Heading2"],
            fontSize=11,
            leading=14,
            spaceBefore=5,
            spaceAfter=5
        )

        normal_style = ParagraphStyle(
            "NormalCustom",
            parent=styles["Normal"],
            fontSize=9,
            leading=12
        )

        small_style = ParagraphStyle(
            "Small",
            parent=normal_style,
            fontSize=8.5,
            leading=11
        )

        right_style = ParagraphStyle(
            "Right",
            parent=normal_style,
            alignment=TA_RIGHT
        )

        center_style = ParagraphStyle(
            "Center",
            parent=normal_style,
            alignment=TA_CENTER
        )

        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=15 * mm,
            leftMargin=15 * mm,
            topMargin=15 * mm,
            bottomMargin=15 * mm
        )

        story = []

        # ====================================================
        # HEADER
        # ====================================================

        story.append(
            Paragraph(
                "INVOICE",
                title_style
            )
        )

        # ====================================================
        # 0. BILL NUMBER + BILL DATE
        # ====================================================

        bill_info = Table(
            [
                [
                    Paragraph(
                        "<b>Invoice No.</b>",
                        normal_style
                    ),
                    Paragraph(
                        str(bill_number or "-"),
                        normal_style
                    ),
                    Paragraph(
                        "<b>Invoice Date</b>",
                        normal_style
                    ),
                    Paragraph(
                        self.format_date_for_display(bill_date),
                        normal_style
                    )
                ]
            ],
            colWidths=[
                30 * mm,
                60 * mm,
                30 * mm,
                60 * mm
            ]
        )

        bill_info.setStyle(
            TableStyle([
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, 0),
                    colors.whitesmoke
                ),
                (
                    "BACKGROUND",
                    (2, 0),
                    (2, 0),
                    colors.whitesmoke
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                )
            ])
        )

        story.append(bill_info)
        story.append(Spacer(1, 10))

        # ====================================================
        # 1. BUSINESS DETAILS | CLIENT DETAILS
        # ====================================================

        # story.append(
        #     Paragraph(
        #         "PARTIES",
        #         heading_style
        #     )
        # )

        # ----------------------------------------------------
        # BUSINESS DETAILS
        # ----------------------------------------------------
        #
        # Leave these as placeholders so they can be replaced
        # later with the actual business details.
        #

        business_details = BUSINESS_DETAILS

        # ----------------------------------------------------
        # CLIENT DETAILS
        # ----------------------------------------------------

        client_parts = []

        if client_name:
            client_parts.append(
                f"<b>Bill To: {client_name}</b>"
            )

        if client_address:
            client_parts.append(
                f"Address: {client_address}"
            )

        if client_gst:
            client_parts.append(
                f"GST: {client_gst}"
            )

        if client_pan:
            client_parts.append(
                f"PAN: {client_pan}"
            )

        if client_tan:
            client_parts.append(
                f"TAN: {client_tan}"
            )

        if client_mobile:
            client_parts.append(
                f"Mobile: {client_mobile}"
            )

        if client_email:
            client_parts.append(
                f"Email: {client_email}"
            )

        if not client_parts:
            client_parts.append("-")

        client_details = "<br/>".join(client_parts)

        parties_table = Table(
            [
                [
                    Paragraph(
                        business_details,
                        normal_style
                    ),
                    Paragraph(
                        client_details,
                        normal_style
                    )
                ]
            ],
            colWidths=[
                90 * mm,
                90 * mm
            ]
        )

        parties_table.setStyle(
            TableStyle([
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ])
        )

        story.append(parties_table)
        story.append(Spacer(1, 10))

        # ====================================================
        # 2. DETAILS
        # ====================================================

        # story.append(
        #     Paragraph(
        #         "DETAILS",
        #         heading_style
        #     )
        # )

        details = []

        if fin_year:
            details.append(
                [
                    Paragraph(
                        "<b>Financial Year</b>",
                        small_style
                    ),
                    Paragraph(
                        str(fin_year),
                        small_style
                    )
                ]
            )

        # if department:
        #     details.append(
        #         [
        #             Paragraph(
        #                 "<b>Department</b>",
        #                 small_style
        #             ),
        #             Paragraph(
        #                 str(department),
        #                 small_style
        #             )
        #         ]
        #     )

        # if billed_under:
        #     details.append(
        #         [
        #             Paragraph(
        #                 "<b>Billed Under</b>",
        #                 small_style
        #             ),
        #             Paragraph(
        #                 str(billed_under),
        #                 small_style
        #             )
        #         ]
        #     )

        # if bill_type:
        #     details.append(
        #         [
        #             Paragraph(
        #                 "<b>Bill Type</b>",
        #                 small_style
        #             ),
        #             Paragraph(
        #                 str(bill_type),
        #                 small_style
        #             )
        #         ]
        #     )

        if quarters:
            details.append(
                [
                    Paragraph(
                        "<b>Quarter</b>",
                        small_style
                    ),
                    Paragraph(
                        ", ".join(quarters),
                        small_style
                    )
                ]
            )

        if form_types:
            details.append(
                [
                    Paragraph(
                        "<b>Form Type</b>",
                        small_style
                    ),
                    Paragraph(
                        ", ".join(form_types),
                        small_style
                    )
                ]
            )

        if months:
            details.append(
                [
                    Paragraph(
                        "<b>Month</b>",
                        small_style
                    ),
                    Paragraph(
                        ", ".join(months),
                        small_style
                    )
                ]
            )

        if application_type:
            details.append(
                [
                    Paragraph(
                        "<b>Application Type</b>",
                        small_style
                    ),
                    Paragraph(
                        str(application_type),
                        small_style
                    )
                ]
            )

        if remarks:
            details.append(
                [
                    Paragraph(
                        "<b>Remarks</b>",
                        small_style
                    ),
                    Paragraph(
                        str(remarks),
                        small_style
                    )
                ]
            )

        # Arrange details as horizontal rows.
        # Each row contains up to 2 label/value pairs.
        details_rows = []

        for i in range(0, len(details), 2):

            row = details[i].copy()

            if i + 1 < len(details):
                row.extend(details[i + 1])
            else:
                row.extend(["", ""])

            details_rows.append(row)

        if details_rows:

            details_table = Table(
                details_rows,
                colWidths=[
                    30 * mm,
                    60 * mm,
                    30 * mm,
                    60 * mm
                ]
            )

            details_table.setStyle(
                TableStyle([
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey
                    ),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (0, -1),
                        colors.whitesmoke
                    ),
                    (
                        "BACKGROUND",
                        (2, 0),
                        (2, -1),
                        colors.whitesmoke
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    )
                ])
            )

            story.append(details_table)
            story.append(Spacer(1, 10))

        # ====================================================
        # 3. PARTICULARS
        # ====================================================

        # story.append(
        #     Paragraph(
        #         "PARTICULARS",
        #         heading_style
        #     )
        # )

        particulars_data = [
            [
                Paragraph(
                    "<b>Particulars</b>",
                    normal_style
                ),
                Paragraph(
                    "<b>Amount</b>",
                    right_style
                )
            ]
        ]

        # ----------------------------------------------------
        # Main narrative
        # ----------------------------------------------------
        # The main narrative does not have an amount against it.

        if narrative:
            particulars_data.append(
                [
                    Paragraph(
                        str(narrative),
                        normal_style
                    ),
                    Paragraph(
                        "",
                        right_style
                    )
                ]
            )

        # ----------------------------------------------------
        # Loading Charges
        # ----------------------------------------------------

        if loading_charges is not None:

            try:
                loading_value = self.money(loading_charges)
            except Exception:
                loading_value = 0

            if loading_value:
                particulars_data.append(
                    [
                        Paragraph(
                            "Loading Charges",
                            normal_style
                        ),
                        Paragraph(
                            f"Rs.{loading_value:.2f}",
                            right_style
                        )
                    ]
                )

        # ----------------------------------------------------
        # GST Registration Fee
        # ----------------------------------------------------

        if gst_registration_fee is not None:

            try:
                gst_value = self.money(gst_registration_fee)
            except Exception:
                gst_value = 0

            if gst_value:
                particulars_data.append(
                    [
                        Paragraph(
                            "GST Registration Fee",
                            normal_style
                        ),
                        Paragraph(
                            f"Rs.{gst_value:.2f}",
                            right_style
                        )
                    ]
                )

        # ----------------------------------------------------
        # PARTICULARS TABLE
        # ----------------------------------------------------

        particulars_table = Table(
            particulars_data,
            colWidths=[
                125 * mm,
                55 * mm
            ]
        )

        particulars_table.setStyle(
            TableStyle([
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.whitesmoke
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (1, -1),
                    "RIGHT"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ])
        )

        story.append(
            particulars_table
        )

        story.append(
            Spacer(1, 10)
        )

        # ====================================================
        # 4. TOTAL AMOUNT
        # ====================================================

        total_table = Table(
            [
                [
                    Paragraph(
                        "<b>TOTAL AMOUNT PAYABLE</b>",
                        normal_style
                    ),
                    Paragraph(
                        f"<b>Rs.{self.money(bill_amount):.2f}</b>",
                        right_style
                    )
                ]
            ],
            colWidths=[
                125 * mm,
                55 * mm
            ]
        )

        total_table.setStyle(
            TableStyle([
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.75,
                    colors.grey
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.whitesmoke
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (1, 0),
                    "RIGHT"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )
            ])
        )

        story.append(
            total_table
        )

        story.append(
            Spacer(1, 12)
        )
        amount = float(bill_amount or 0)

        rupees = int(amount)
        paise = round((amount - rupees) * 100)

        if paise > 0:
            amount_in_words = (
                f"{num2words(rupees, lang='en_IN').title()} Rupees "
                f"And {num2words(paise, lang='en_IN').title()} Paise Only"
            )
        else:
            amount_in_words = (
                f"{num2words(rupees, lang='en_IN').title()} Rupees Only"
            )

        story.append(
            Paragraph(
                f"<b>Amount Payable in Words:</b> {amount_in_words}",
                normal_style
            )
        )

        story.append(
            Spacer(1, 12)
        )
        # ====================================================
        # 5. PAY TO / BANK DETAILS
        # ====================================================

        story.append(
            Paragraph(
                "BANK DETAILS",
                heading_style
            )
        )

        bank_details = constants.BANK_DETAILS.get(
            pay_to,
            {}
        )

        bank_data = []

        # if pay_to:
        #     bank_data.append(
        #         [
        #             Paragraph(
        #                 "<b>Pay To</b>",
        #                 normal_style
        #             ),
        #             Paragraph(
        #                 str(pay_to),
        #                 normal_style
        #             )
        #         ]
        #     )

        if bank_details.get("bank_name"):
            bank_data.append(
                [
                    Paragraph(
                        "<b>Bank Name</b>",
                        normal_style
                    ),
                    Paragraph(
                        str(bank_details.get("bank_name")),
                        normal_style
                    )
                ]
            )

        if bank_details.get("account_holder_name"):
            bank_data.append(
                [
                    Paragraph(
                        "<b>Account Holder Name</b>",
                        normal_style
                    ),
                    Paragraph(
                        str(
                            bank_details.get(
                                "account_holder_name"
                            )
                        ),
                        normal_style
                    )
                ]
            )

        if bank_details.get("account_number"):
            bank_data.append(
                [
                    Paragraph(
                        "<b>Account Number</b>",
                        normal_style
                    ),
                    Paragraph(
                        str(
                            bank_details.get(
                                "account_number"
                            )
                        ),
                        normal_style
                    )
                ]
            )

        if bank_details.get("ifsc"):
            bank_data.append(
                [
                    Paragraph(
                        "<b>IFSC</b>",
                        normal_style
                    ),
                    Paragraph(
                        str(bank_details.get("ifsc")),
                        normal_style
                    )
                ]
            )

        if bank_details.get("branch"):
            bank_data.append(
                [
                    Paragraph(
                        "<b>Branch</b>",
                        normal_style
                    ),
                    Paragraph(
                        str(bank_details.get("branch")),
                        normal_style
                    )
                ]
            )

        if bank_details.get("upi_id"):
            bank_data.append(
                [
                    Paragraph(
                        "<b>UPI ID</b>",
                        normal_style
                    ),
                    Paragraph(
                        str(bank_details.get("upi_id")),
                        normal_style
                    )
                ]
            )

        if not bank_data:
            bank_data.append(
                [
                    Paragraph(
                        "<b>Pay To</b>",
                        normal_style
                    ),
                    Paragraph(
                        str(pay_to or "-"),
                        normal_style
                    )
                ]
            )

        bank_table = Table(
            bank_data,
            colWidths=[
                55 * mm,
                125 * mm
            ]
        )

        bank_table.setStyle(
            TableStyle([
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.whitesmoke
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5
                )
            ])
        )

        story.append(bank_table)
        story.append(Spacer(1, 15))

        # ====================================================
        # FOOTER
        # ====================================================

        story.append(
            Paragraph(
                "This is a computer-generated invoice.",
                ParagraphStyle(
                    "Footer",
                    parent=normal_style,
                    alignment=TA_CENTER
                )
            )
        )

        # ====================================================
        # BUILD PDF
        # ====================================================

        doc.build(story)

    # ========================================================
    # PRINT LATEST RECEIPT
    # ========================================================

    def print_latest_receipt(self):

        if not hasattr(
            self,
            "latest_receipt_id"
        ):

            if not self.current_task_id:

                messagebox.showerror(
                    "Error",
                    "No receipt is available."
                )

                return


            conn = get_connection()

            try:

                cursor = conn.cursor()

                cursor.execute("""
                    SELECT id
                    FROM payment_transactions
                    WHERE task_id = %s
                    ORDER BY id DESC
                    LIMIT 1
                """, (
                    self.current_task_id,
                ))

                row = cursor.fetchone()

                if row:

                    self.latest_receipt_id = row[0]

            finally:

                conn.close()


        if not hasattr(
            self,
            "latest_receipt_id"
        ):

            messagebox.showerror(
                "Error",
                "No payment receipt is available."
            )

            return


        conn = get_connection()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    p.id,
                    p.amount,
                    p.payment_mode,
                    p.payment_date,
                    p.received_by,
                    p.notes,
                    p.receipt_type,
                    p.receipt_number,
                    p.receipt_date,
                    p.upi_bank,
                    p.bank_name,
                    p.bank_transfer_mode,
                    p.cheque_number,
                    p.cheque_date,

                    t.task_name,
                    t.department,
                    t.billed_under,
                    t.billing_narrative,
                    t.bill_number,
                    t.bill_date,
                    t.bill_amount,
                    t.actual_amount_received,
                    t.amount_pending_receipt,

                    c.name,
                    c.mobile,
                    c.email,
                    c.address

                FROM payment_transactions p

                JOIN tasks t
                    ON p.task_id = t.id

                LEFT JOIN clients c
                    ON t.client_id = c.id

                WHERE p.id = %s
            """, (
                self.latest_receipt_id,
            ))

            receipt = cursor.fetchone()

        finally:

            conn.close()


        if not receipt:

            messagebox.showerror(
                "Error",
                "Receipt not found."
            )

            return


        default_name = (
            f"Receipt_{receipt[7]}.pdf"
        )


        filepath = filedialog.asksaveasfilename(
            title="Save Payment Receipt PDF",
            defaultextension=".pdf",
            initialfile=default_name,
            filetypes=[
                ("PDF files", "*.pdf")
            ]
        )


        if not filepath:
            return


        try:

            self.create_receipt_pdf(
                receipt,
                filepath
            )

            messagebox.showinfo(
                "Receipt PDF Created",
                (
                    "Payment receipt PDF created successfully.\n\n"
                    f"{filepath}"
                )
            )

        except Exception as e:

            messagebox.showerror(
                "PDF Error",
                str(e)
            )


    # ========================================================
    # CREATE RECEIPT PDF
    # ========================================================

    def create_receipt_pdf(
        self,
        receipt,
        filepath
    ):

        (
            payment_id,
            amount,
            payment_mode,
            payment_date,
            received_by,
            notes,
            receipt_type,
            receipt_number,
            receipt_date,
            upi_bank,
            bank_name,
            bank_transfer_mode,
            cheque_number,
            cheque_date,

            task_name,
            department,
            billed_under,
            narrative,
            bill_number,
            bill_date,
            bill_amount,
            actual_received,
            pending,

            client_name,
            client_mobile,
            client_email,
            client_address
        ) = receipt

        styles = getSampleStyleSheet()

        # ====================================================
        # STYLES
        # ====================================================

        title_style = ParagraphStyle(
            "ReceiptTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=18,
            leading=22,
            spaceAfter=10
        )

        heading_style = ParagraphStyle(
            "ReceiptHeading",
            parent=styles["Heading2"],
            fontSize=11,
            leading=14,
            spaceBefore=5,
            spaceAfter=5
        )

        normal_style = ParagraphStyle(
            "ReceiptNormal",
            parent=styles["Normal"],
            fontSize=9,
            leading=12
        )

        right_style = ParagraphStyle(
            "ReceiptRight",
            parent=normal_style,
            alignment=TA_RIGHT
        )

        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=15 * mm,
            leftMargin=15 * mm,
            topMargin=15 * mm,
            bottomMargin=15 * mm
        )

        story = []

        # ====================================================
        # HEADER
        # ====================================================

        story.append(
            Paragraph(
                "PAYMENT RECEIPT",
                title_style
            )
        )

        # ====================================================
        # 1. RECEIPT / BILL DETAILS
        # ====================================================

        # story.append(
        #     Paragraph(
        #         "RECEIPT / BILL DETAILS",
        #         heading_style
        #     )
        # )

        receipt_bill_data = [
            [
                Paragraph(
                    "<b>Receipt Number</b>",
                    normal_style
                ),
                Paragraph(
                    str(receipt_number or "-"),
                    normal_style
                ),
                Paragraph(
                    "<b>Receipt Date</b>",
                    normal_style
                ),
                Paragraph(
                    self.format_date_for_display(
                        receipt_date
                    ),
                    normal_style
                )
            ],
            [
                Paragraph(
                    "<b>Bill Number</b>",
                    normal_style
                ),
                Paragraph(
                    str(bill_number or "-"),
                    normal_style
                ),
                Paragraph(
                    "<b>Bill Date</b>",
                    normal_style
                ),
                Paragraph(
                    self.format_date_for_display(
                        bill_date
                    ),
                    normal_style
                )
            ]
        ]

        receipt_bill_table = Table(
            receipt_bill_data,
            colWidths=[
                35 * mm,
                55 * mm,
                35 * mm,
                55 * mm
            ]
        )

        receipt_bill_table.setStyle(
            TableStyle([
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.whitesmoke
                ),
                (
                    "BACKGROUND",
                    (2, 0),
                    (2, -1),
                    colors.whitesmoke
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                )
            ])
        )

        story.append(
            receipt_bill_table
        )

        story.append(
            Spacer(1, 10)
        )

        # ====================================================
        # 2. PARTIES
        # ====================================================

        # story.append(
        #     Paragraph(
        #         "PARTIES",
        #         heading_style
        #     )
        # )

        # ----------------------------------------------------
        # BUSINESS DETAILS
        # ----------------------------------------------------

        business_details = (
            BUSINESS_DETAILS
            if BUSINESS_DETAILS
            else "-"
        )

        # ----------------------------------------------------
        # CLIENT DETAILS
        # ----------------------------------------------------

        client_parts = []

        if client_name:
            client_parts.append(
                f"<b>{client_name}</b>"
            )

        if client_address:
            client_parts.append(
                f"Address: {client_address}"
            )

        if client_mobile:
            client_parts.append(
                f"Mobile: {client_mobile}"
            )

        if client_email:
            client_parts.append(
                f"Email: {client_email}"
            )

        if not client_parts:
            client_parts.append("-")

        client_details = "<br/>".join(
            client_parts
        )

        parties_table = Table(
            [
                [
                    Paragraph(
                        business_details,
                        normal_style
                    ),
                    Paragraph(
                        client_details,
                        normal_style
                    )
                ]
            ],
            colWidths=[
                90 * mm,
                90 * mm
            ]
        )

        parties_table.setStyle(
            TableStyle([
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ])
        )

        story.append(
            parties_table
        )

        story.append(
            Spacer(1, 10)
        )

        # ====================================================
        # 3. BILL NARRATIVE
        # ====================================================

     
        
        # narrative_data = [
        #     [
        #         Paragraph(
        #             "<b>Narrative</b>",
        #             normal_style
        #         ),
        #         Paragraph(
        #             narrative or task_name or "-",
        #             normal_style
        #         )
        #     ]
        # ]

        # narrative_table = Table(
        #     narrative_data,
        #     colWidths=[
        #         35 * mm,
        #         145 * mm
        #     ]
        # )

        # narrative_table.setStyle(
        #     TableStyle([
        #         (
        #             "GRID",
        #             (0, 0),
        #             (-1, -1),
        #             0.5,
        #             colors.grey
        #         ),
        #         (
        #             "BACKGROUND",
        #             (0, 0),
        #             (0, -1),
        #             colors.whitesmoke
        #         ),
        #         (
        #             "VALIGN",
        #             (0, 0),
        #             (-1, -1),
        #             "TOP"
        #         ),
        #         (
        #             "LEFTPADDING",
        #             (0, 0),
        #             (-1, -1),
        #             7
        #         ),
        #         (
        #             "RIGHTPADDING",
        #             (0, 0),
        #             (-1, -1),
        #             7
        #         ),
        #         (
        #             "TOPPADDING",
        #             (0, 0),
        #             (-1, -1),
        #             7
        #         ),
        #         (
        #             "BOTTOMPADDING",
        #             (0, 0),
        #             (-1, -1),
        #             7
        #         )
        #     ])
        # )

        # story.append(
        #     narrative_table
        # )

        story.append(
            Spacer(1, 10)
        )

        # ====================================================
        # 4. PAYMENT DETAILS
        # ====================================================

        story.append(
            Paragraph(
                "PAYMENT DETAILS",
                heading_style
            )
        )

        payment_data = [
            [
                Paragraph(
                                    "<b>Payment For</b>",
                                    normal_style
                                ),
                                Paragraph(
                                    narrative or task_name or "-",
                                    right_style
                                )
          

            ],
            [
                Paragraph(
                    "<b>Payment Amount</b>",
                    normal_style
                ),
                Paragraph(
                    f"Rs.{self.money(amount):.2f}",
                    right_style
                )
            ],
            [
                Paragraph(
                    "<b>Payment Mode</b>",
                    normal_style
                ),
                Paragraph(
                    payment_mode or "-",
                    right_style
                )
            ]
        ]

        # ----------------------------------------------------
        # UPI
        # ----------------------------------------------------

        if payment_mode == "UPI":

            payment_data.append(
                [
                    Paragraph(
                        "<b>UPI Bank</b>",
                        normal_style
                    ),
                    Paragraph(
                        upi_bank or "-",
                        right_style
                    )
                ]
            )

        # ----------------------------------------------------
        # BANK TRANSFER
        # ----------------------------------------------------

        elif payment_mode == "Bank Transfer":

            payment_data.extend([
                [
                    Paragraph(
                        "<b>Bank Name</b>",
                        normal_style
                    ),
                    Paragraph(
                        bank_name or "-",
                        right_style
                    )
                ],
                [
                    Paragraph(
                        "<b>Transfer Mode</b>",
                        normal_style
                    ),
                    Paragraph(
                        bank_transfer_mode or "-",
                        right_style
                    )
                ]
            ])

        # ----------------------------------------------------
        # CHEQUE
        # ----------------------------------------------------

        elif payment_mode == "Cheque":

            payment_data.extend([
                [
                    Paragraph(
                        "<b>Cheque Number</b>",
                        normal_style
                    ),
                    Paragraph(
                        cheque_number or "-",
                        normal_style
                    )
                ],
                [
                    Paragraph(
                        "<b>Cheque Date</b>",
                        normal_style
                    ),
                    Paragraph(
                        self.format_date_for_display(
                            cheque_date
                        ),
                        normal_style
                    )
                ]
            ])

        # ----------------------------------------------------
        # PAYMENT SUMMARY
        # ----------------------------------------------------

        payment_data.extend([
            [
                Paragraph(
                    "<b>Total Bill Amount</b>",
                    normal_style
                ),
                Paragraph(
                    f"Rs.{self.money(bill_amount):.2f}",
                    right_style
                )
            ],
            [
                Paragraph(
                    "<b>Total Received</b>",
                    normal_style
                ),
                Paragraph(
                    f"Rs.{self.money(actual_received):.2f}",
                    right_style
                )
            ],
            [
                Paragraph(
                    "<b>Balance Remaining</b>",
                    normal_style
                ),
                Paragraph(
                    f"Rs.{self.money(pending):.2f}",
                    right_style
                )
            ]
        ])

        # if received_by:
        #     payment_data.append(
        #         [
        #             Paragraph(
        #                 "<b>Received By</b>",
        #                 normal_style
        #             ),
        #             Paragraph(
        #                 str(received_by),
        #                 normal_style
        #             )
        #         ]
        #     )

        if notes:
            payment_data.append(
                [
                    Paragraph(
                        "<b>Notes</b>",
                        normal_style
                    ),
                    Paragraph(
                        str(notes),
                        normal_style
                    )
                ]
            )

        payment_table = Table(
            payment_data,
            colWidths=[
                55 * mm,
                125 * mm
            ]
        )

        payment_table.setStyle(
            TableStyle([
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.whitesmoke
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (1, -1),
                    "RIGHT"
                )
            ])
        )

        story.append(
            payment_table
        )

        story.append(
            Spacer(1, 20)
        )

        # ====================================================
        # FOOTER
        # ====================================================

        story.append(
            Paragraph(
                (
                    "Received with thanks. "
                    "This is a computer-generated "
                    "payment receipt."
                ),
                ParagraphStyle(
                    "ReceiptFooter",
                    parent=normal_style,
                    alignment=TA_CENTER
                )
            )
        )

        # ====================================================
        # BUILD PDF
        # ====================================================

        doc.build(
            story
        )
