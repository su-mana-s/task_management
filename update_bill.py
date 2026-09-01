import customtkinter as ctk
import psycopg

from tkinter import messagebox

from database import get_connection
from theme import *

from searchable_combobox import SearchableComboBox


class AdminBillUpdate(ctk.CTkFrame):

    def __init__(self, master, user):

        super().__init__(
            master,
            fg_color=COLORS["background"]
        )

        self.user = user
        self.task_map = {}

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
            size=SIZES["normal_size"],
            weight="normal"
        )

        self.bold_font = ctk.CTkFont(
            size=SIZES["normal_size"],
            weight="bold"
        )

        # =====================================================
        # LAYOUT
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
            text="Admin - Update Bill",
            font=self.title_font,
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
        # MAIN FRAME
        # =====================================================

        self.form_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS["card"],
            corner_radius=SIZES["large_corner_radius"],
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["primary_hover"]
        )

        self.form_frame.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 20),
            sticky="nsew"
        )

        self.form_frame.grid_columnconfigure(
            0,
            minsize=230
        )

        self.form_frame.grid_columnconfigure(
            1,
            weight=1
        )

        # =====================================================
        # SELECT WORK
        # =====================================================

        self.create_label(
            "Select Work:",
            0
        )

        self.case_var = ctk.StringVar()

        self.case_dropdown = SearchableComboBox(
            self.form_frame,

            variable=self.case_var,

            width=700,
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

            command=self.load_selected_record
        )

        self.case_dropdown.grid(
            row=0,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # BILL INFORMATION HEADING
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="BILL INFORMATION",
            font=self.heading_font,
            text_color=COLORS["primary"]
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            padx=PADDING["x"],
            pady=(30, 15),
            sticky="w"
        )

        # =====================================================
        # BILL TYPE
        # =====================================================

        self.create_label(
            "Bill Type:",
            2
        )

        self.bill_type = ctk.CTkEntry(
            self.form_frame,
            width=400,
            height=SIZES["entry_height"],
            font=self.normal_font,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text="Bill type",
            placeholder_text_color=COLORS["placeholder"],
            corner_radius=SIZES["corner_radius"]
        )

        self.bill_type.grid(
            row=2,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # BILLED UNDER
        # =====================================================

        self.create_label(
            "Billed Under:",
            3
        )

        self.billed_under = ctk.CTkComboBox(
            self.form_frame,
            values=["S", "V"],
            width=250,
            height=SIZES["entry_height"],
            font=self.normal_font,

            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],

            button_color=SIDEBAR_HOVER,
            button_hover_color=COLORS["primary_hover"],

            dropdown_fg_color=COLORS["card"],
            dropdown_text_color=COLORS["text"],
            dropdown_hover_color=SIDEBAR_HOVER,

            corner_radius=SIZES["corner_radius"]
        )

        self.billed_under.grid(
            row=3,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # BILL NUMBER
        # =====================================================

        self.create_label(
            "Bill Number:",
            4
        )

        self.bill_number = ctk.CTkEntry(
            self.form_frame,
            width=400,
            height=SIZES["entry_height"],
            font=self.normal_font,

            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],

            placeholder_text="Bill number",
            placeholder_text_color=COLORS["placeholder"],

            corner_radius=SIZES["corner_radius"]
        )

        self.bill_number.grid(
            row=4,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # BILL DATE
        # =====================================================

        self.create_label(
            "Bill Date:",
            5
        )

        self.bill_date = ctk.CTkEntry(
            self.form_frame,
            width=300,
            height=SIZES["entry_height"],
            font=self.normal_font,

            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],

            placeholder_text="YYYY-MM-DD",
            placeholder_text_color=COLORS["placeholder"],

            corner_radius=SIZES["corner_radius"]
        )

        self.bill_date.grid(
            row=5,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # BILL AMOUNT
        # =====================================================

        self.create_label(
            "Bill Amount:",
            6
        )

        self.bill_amount = ctk.CTkEntry(
            self.form_frame,
            width=300,
            height=SIZES["entry_height"],
            font=self.normal_font,

            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],

            placeholder_text="Enter bill amount",
            placeholder_text_color=COLORS["placeholder"],

            corner_radius=SIZES["corner_radius"]
        )

        self.bill_amount.grid(
            row=6,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        self.bill_amount.bind(
            "<KeyRelease>",
            lambda event: self.update_pending_preview()
        )

        # =====================================================
        # ACTUAL AMOUNT RECEIVED
        # =====================================================

        self.create_label(
            "Actual Amount Received:",
            7
        )

        self.actual_received_label = ctk.CTkLabel(
            self.form_frame,
            text="₹0.00",
            font=self.bold_font,
            text_color=COLORS["success"]
        )

        self.actual_received_label.grid(
            row=7,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # AMOUNT PENDING
        # =====================================================

        self.create_label(
            "Amount Pending:",
            8
        )

        self.pending_label = ctk.CTkLabel(
            self.form_frame,
            text="₹0.00",
            font=self.bold_font,
            text_color=COLORS["warning"]
        )

        self.pending_label.grid(
            row=8,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # BILLING FINANCIAL YEAR
        # =====================================================

        self.create_label(
            "Billing Financial Year:",
            9
        )

        self.billing_fin_year = ctk.CTkEntry(
            self.form_frame,
            width=300,
            height=SIZES["entry_height"],
            font=self.normal_font,

            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],

            placeholder_text="e.g. 2025-26",
            placeholder_text_color=COLORS["placeholder"],

            corner_radius=SIZES["corner_radius"]
        )

        self.billing_fin_year.grid(
            row=9,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # BILLING QUARTERS
        # =====================================================

        self.create_label(
            "Billing Quarters:",
            10
        )

        self.billing_quarters = ctk.CTkEntry(
            self.form_frame,
            width=500,
            height=SIZES["entry_height"],
            font=self.normal_font,

            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],

            placeholder_text="e.g. Q1, Q2",
            placeholder_text_color=COLORS["placeholder"],

            corner_radius=SIZES["corner_radius"]
        )

        self.billing_quarters.grid(
            row=10,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # BILLING FORM TYPES
        # =====================================================

        self.create_label(
            "Billing Form Types:",
            11
        )

        self.billing_form_types = ctk.CTkEntry(
            self.form_frame,
            width=500,
            height=SIZES["entry_height"],
            font=self.normal_font,

            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],

            placeholder_text="Form types",
            placeholder_text_color=COLORS["placeholder"],

            corner_radius=SIZES["corner_radius"]
        )

        self.billing_form_types.grid(
            row=11,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # BILLING MONTHS
        # =====================================================

        self.create_label(
            "Billing Months:",
            12
        )

        self.billing_months = ctk.CTkEntry(
            self.form_frame,
            width=500,
            height=SIZES["entry_height"],
            font=self.normal_font,

            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],

            placeholder_text="Months",
            placeholder_text_color=COLORS["placeholder"],

            corner_radius=SIZES["corner_radius"]
        )

        self.billing_months.grid(
            row=12,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # LOADING CHARGES
        # =====================================================

        self.create_label(
            "Loading Charges:",
            13
        )

        self.loading_charges = ctk.CTkEntry(
            self.form_frame,
            width=300,
            height=SIZES["entry_height"],
            font=self.normal_font,

            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],

            placeholder_text="0.00",
            placeholder_text_color=COLORS["placeholder"],

            corner_radius=SIZES["corner_radius"]
        )

        self.loading_charges.grid(
            row=13,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # GST REGISTRATION FEE
        # =====================================================

        self.create_label(
            "GST Registration Fee:",
            14
        )

        self.gst_registration_fee = ctk.CTkEntry(
            self.form_frame,
            width=300,
            height=SIZES["entry_height"],
            font=self.normal_font,

            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],

            placeholder_text="0.00",
            placeholder_text_color=COLORS["placeholder"],

            corner_radius=SIZES["corner_radius"]
        )

        self.gst_registration_fee.grid(
            row=14,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # APPLICATION TYPE
        # =====================================================

        self.create_label(
            "Application Type:",
            15
        )

        self.application_type = ctk.CTkEntry(
            self.form_frame,
            width=500,
            height=SIZES["entry_height"],
            font=self.normal_font,

            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],

            placeholder_text="Application type",
            placeholder_text_color=COLORS["placeholder"],

            corner_radius=SIZES["corner_radius"]
        )

        self.application_type.grid(
            row=15,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # BILLING NARRATIVE
        # =====================================================

        self.create_label(
            "Billing Narrative:",
            16
        )

        self.billing_narrative = ctk.CTkEntry(
            self.form_frame,
            width=600,
            height=SIZES["entry_height"],
            font=self.normal_font,

            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],

            placeholder_text="Billing narrative",
            placeholder_text_color=COLORS["placeholder"],

            corner_radius=SIZES["corner_radius"]
        )

        self.billing_narrative.grid(
            row=16,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # PAY TO
        # =====================================================

        self.create_label(
            "Pay To:",
            17
        )

        self.pay_to = ctk.CTkEntry(
            self.form_frame,
            width=500,
            height=SIZES["entry_height"],
            font=self.normal_font,

            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],

            placeholder_text="Pay to",
            placeholder_text_color=COLORS["placeholder"],

            corner_radius=SIZES["corner_radius"]
        )

        self.pay_to.grid(
            row=17,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # BILLING REMARKS
        # =====================================================

        self.create_label(
            "Billing Remarks:",
            18
        )

        self.billing_remarks = ctk.CTkTextbox(
            self.form_frame,
            width=600,
            height=120,
            font=self.normal_font,

            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],

            corner_radius=SIZES["corner_radius"]
        )

        self.billing_remarks.grid(
            row=18,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # UPDATE BUTTON
        # =====================================================

        self.update_btn = ctk.CTkButton(
            self.form_frame,

            text="Update Bill",

            command=self.update_bill,

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

        self.update_btn.grid(
            row=19,
            column=1,
            padx=PADDING["x"],
            pady=(25, 30),
            sticky="w"
        )

        # =====================================================
        # NOTE
        # =====================================================

        self.note_label = ctk.CTkLabel(
            self.form_frame,

            text=(
                "Note: Actual Amount Received is read-only. "
                "Amount Pending is automatically calculated from "
                "Bill Amount minus Actual Amount Received."
            ),

            font=self.normal_font,

            text_color=COLORS["text_secondary"],

            wraplength=800,

            justify="left"
        )

        self.note_label.grid(
            row=20,
            column=0,
            columnspan=2,
            padx=PADDING["x"],
            pady=(5, 30),
            sticky="w"
        )

        # =====================================================
        # LOAD
        # =====================================================

        self.load_records()

    # =========================================================
    # LABEL HELPER
    # =========================================================

    def create_label(
        self,
        text,
        row
    ):

        label = ctk.CTkLabel(
            self.form_frame,
            text=text,
            font=self.label_font,
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
    # ENTRY HELPER
    # =========================================================

    def set_entry(
        self,
        entry,
        value
    ):

        entry.delete(
            0,
            "end"
        )

        if value is not None:

            entry.insert(
                0,
                str(value)
            )

    # =========================================================
    # LOAD RECORDS
    # =========================================================

    def load_records(
        self,
        selected_task_id=None
    ):

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    t.id,
                    c.name,
                    t.task_name,
                    t.department,
                    t.status,
                    t.bill_number,
                    t.bill_amount,
                    t.actual_amount_received,
                    t.amount_pending_receipt
                FROM tasks t

                LEFT JOIN clients c
                    ON t.client_id = c.id

                WHERE
                    t.bill_number IS NOT NULL
                    AND TRIM(t.bill_number) != ''

                ORDER BY t.id DESC
            """)

            records = cursor.fetchall()

        except psycopg.Error as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load billed work:\n{e}"
            )

            return

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        self.task_map = {}

        display_values = []

        for record in records:

            (
                task_id,
                client_name,
                task_name,
                department,
                status,
                bill_number,
                bill_amount,
                actual_received,
                pending
            ) = record

            bill_amount = float(
                bill_amount or 0
            )

            actual_received = float(
                actual_received or 0
            )

            pending = max(
                0,
                bill_amount - actual_received
            )

            display = (
                f"ID: {task_id} | "
                f"{client_name or '-'} | "
                f"{task_name or '-'} | "
                f"{department or '-'} | "
                f"Bill: {bill_number or '-'} | "
                f"Amount: ₹{bill_amount:.2f} | "
                f"Balance: ₹{pending:.2f}"
            )

            self.task_map[display] = task_id

            display_values.append(
                display
            )

        if display_values:

            self.case_dropdown.configure_values(
                values=display_values
            )

            selected_display = display_values[0]

            if selected_task_id is not None:

                for display_text, task_id in self.task_map.items():

                    if task_id == selected_task_id:

                        selected_display = display_text

                        break

            self.case_dropdown.set(
                selected_display
            )

            self.load_selected_record(
                selected_display
            )

        else:

            self.case_dropdown.configure_values(
                values=["No billed work available"]
            )

            self.case_dropdown.set(
                "No billed work available"
            )

            self.clear_bill_information()

    # =========================================================
    # LOAD SELECTED RECORD
    # =========================================================

    def load_selected_record(
        self,
        choice=None
    ):

        if choice is None:

            choice = self.case_var.get()

        task_id = self.task_map.get(
            choice
        )

        if not task_id:

            return

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    bill_type,
                    billed_under,
                    bill_number,
                    bill_date,
                    bill_amount,
                    actual_amount_received,
                    amount_pending_receipt,
                    billing_fin_year,
                    billing_quarters,
                    billing_form_types,
                    billing_months,
                    loading_charges,
                    gst_registration_fee,
                    application_type,
                    billing_remarks,
                    billing_narrative,
                    pay_to
                FROM tasks
                WHERE id = %s
            """, (
                task_id,
            ))

            record = cursor.fetchone()

        except psycopg.Error as e:

            messagebox.showerror(
                "Database Error",
                f"Unable to load bill information:\n{e}"
            )

            return

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        if not record:

            return

        (
            bill_type,
            billed_under,
            bill_number,
            bill_date,
            bill_amount,
            actual_received,
            pending,
            billing_fin_year,
            billing_quarters,
            billing_form_types,
            billing_months,
            loading_charges,
            gst_registration_fee,
            application_type,
            billing_remarks,
            billing_narrative,
            pay_to
        ) = record

        # =====================================================
        # POPULATE FORM
        # =====================================================

        self.set_entry(
            self.bill_type,
            bill_type
        )

        self.billed_under.set(
            billed_under or ""
        )

        self.set_entry(
            self.bill_number,
            bill_number
        )

        self.set_entry(
            self.bill_date,
            bill_date
        )

        self.set_entry(
            self.bill_amount,
            f"{float(bill_amount or 0):.2f}"
        )

        self.actual_received_label.configure(
            text=f"₹{float(actual_received or 0):.2f}"
        )

        # Always calculate pending from current values
        calculated_pending = max(
            0,
            float(bill_amount or 0)
            - float(actual_received or 0)
        )

        self.pending_label.configure(
            text=f"₹{calculated_pending:.2f}"
        )

        self.set_entry(
            self.billing_fin_year,
            billing_fin_year
        )

        self.set_entry(
            self.billing_quarters,
            self.array_to_text(
                billing_quarters
            )
        )

        self.set_entry(
            self.billing_form_types,
            self.array_to_text(
                billing_form_types
            )
        )

        self.set_entry(
            self.billing_months,
            self.array_to_text(
                billing_months
            )
        )

        self.set_entry(
            self.loading_charges,
            f"{float(loading_charges or 0):.2f}"
        )

        self.set_entry(
            self.gst_registration_fee,
            f"{float(gst_registration_fee or 0):.2f}"
        )

        self.set_entry(
            self.application_type,
            application_type
        )

        self.set_entry(
            self.billing_narrative,
            billing_narrative
        )

        self.set_entry(
            self.pay_to,
            pay_to
        )

        self.billing_remarks.delete(
            "1.0",
            "end"
        )

        if billing_remarks:

            self.billing_remarks.insert(
                "1.0",
                billing_remarks
            )

    # =========================================================
    # ARRAY -> TEXT
    # =========================================================

    def array_to_text(
        self,
        value
    ):

        if not value:

            return ""

        if isinstance(
            value,
            (list, tuple)
        ):

            return ", ".join(
                str(x)
                for x in value
                if x is not None
            )

        return str(value)

    # =========================================================
    # TEXT -> POSTGRES ARRAY
    # =========================================================

    def text_to_array(
        self,
        value
    ):

        value = (
            value
            .strip()
        )

        if not value:

            return None

        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    # =========================================================
    # CLEAR
    # =========================================================

    def clear_bill_information(self):

        entries = [
            self.bill_type,
            self.bill_number,
            self.bill_date,
            self.bill_amount,
            self.billing_fin_year,
            self.billing_quarters,
            self.billing_form_types,
            self.billing_months,
            self.loading_charges,
            self.gst_registration_fee,
            self.application_type,
            self.billing_narrative,
            self.pay_to
        ]

        for entry in entries:

            entry.delete(
                0,
                "end"
            )

        self.billed_under.set(
            ""
        )

        self.billing_remarks.delete(
            "1.0",
            "end"
        )

        self.actual_received_label.configure(
            text="₹0.00"
        )

        self.pending_label.configure(
            text="₹0.00"
        )

    # =========================================================
    # UPDATE PENDING PREVIEW
    # =========================================================

    def update_pending_preview(self):

        selected = self.case_var.get()

        task_id = self.task_map.get(
            selected
        )

        if not task_id:

            return

        amount_text = (
            self.bill_amount
            .get()
            .strip()
        )

        try:

            new_amount = float(
                amount_text
            )

        except ValueError:

            self.pending_label.configure(
                text="Invalid amount"
            )

            return

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT actual_amount_received
                FROM tasks
                WHERE id = %s
            """, (
                task_id,
            ))

            result = cursor.fetchone()

        except psycopg.Error:

            return

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        if not result:

            return

        received = float(
            result[0] or 0
        )

        new_pending = (
            new_amount
            - received
        )

        if new_pending < 0:

            self.pending_label.configure(
                text="Cannot be less than received amount"
            )

        else:

            self.pending_label.configure(
                text=f"₹{new_pending:.2f}"
            )

    # =========================================================
    # UPDATE BILL
    # =========================================================

    def update_bill(self):

        selected = self.case_var.get()

        task_id = self.task_map.get(
            selected
        )

        if not task_id:

            messagebox.showerror(
                "Error",
                "Please select a valid billed work record."
            )

            return

        # =====================================================
        # GET VALUES
        # =====================================================

        bill_type = (
            self.bill_type
            .get()
            .strip()
        )

        billed_under = (
            self.billed_under
            .get()
            .strip()
        )

        bill_number = (
            self.bill_number
            .get()
            .strip()
        )

        bill_date = (
            self.bill_date
            .get()
            .strip()
        )

        bill_amount_text = (
            self.bill_amount
            .get()
            .strip()
        )

        billing_fin_year = (
            self.billing_fin_year
            .get()
            .strip()
        )

        billing_quarters = self.text_to_array(
            self.billing_quarters.get()
        )

        billing_form_types = self.text_to_array(
            self.billing_form_types.get()
        )

        billing_months = self.text_to_array(
            self.billing_months.get()
        )

        loading_charges_text = (
            self.loading_charges
            .get()
            .strip()
        )

        gst_registration_fee_text = (
            self.gst_registration_fee
            .get()
            .strip()
        )

        application_type = (
            self.application_type
            .get()
            .strip()
        )

        billing_narrative = (
            self.billing_narrative
            .get()
            .strip()
        )

        pay_to = (
            self.pay_to
            .get()
            .strip()
        )

        billing_remarks = (
            self.billing_remarks
            .get(
                "1.0",
                "end"
            )
            .strip()
        )

        # =====================================================
        # VALIDATION
        # =====================================================

        if not bill_amount_text:

            messagebox.showerror(
                "Error",
                "Please enter the bill amount."
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
                "Bill amount must be greater than zero."
            )

            return

        if billed_under not in (
            "S",
            "V"
        ):

            messagebox.showerror(
                "Error",
                "Billed Under must be either S or V."
            )

            return

        try:

            loading_charges = float(
                loading_charges_text
                or 0
            )

            gst_registration_fee = float(
                gst_registration_fee_text
                or 0
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Loading Charges and GST Registration Fee must be valid numbers."
            )

            return

        if loading_charges < 0:

            messagebox.showerror(
                "Error",
                "Loading Charges cannot be negative."
            )

            return

        if gst_registration_fee < 0:

            messagebox.showerror(
                "Error",
                "GST Registration Fee cannot be negative."
            )

            return

        conn = None
        cursor = None

        try:

            conn = get_connection()
            cursor = conn.cursor()

            # =================================================
            # GET EXISTING RECORD
            # =================================================

            cursor.execute("""
                SELECT
                    bill_number,
                    bill_amount,
                    actual_amount_received
                FROM tasks
                WHERE id = %s
            """, (
                task_id,
            ))

            existing = cursor.fetchone()

            if not existing:

                messagebox.showerror(
                    "Error",
                    "Task not found."
                )

                return

            (
                old_bill_number,
                old_bill_amount,
                actual_received
            ) = existing

            old_bill_amount = float(
                old_bill_amount or 0
            )

            actual_received = float(
                actual_received or 0
            )

            # =================================================
            # BILL CANNOT BE LESS THAN RECEIVED
            # =================================================

            if bill_amount < actual_received:

                messagebox.showerror(
                    "Invalid Amount",
                    (
                        "The bill amount cannot be less "
                        "than the amount already received.\n\n"
                        f"Already received: ₹{actual_received:.2f}"
                    )
                )

                return

            new_pending = (
                bill_amount
                - actual_received
            )

            # =================================================
            # UPDATE TASK
            # =================================================

            cursor.execute("""
                UPDATE tasks
                SET
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
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (
                bill_type or None,
                billed_under,
                bill_number or None,
                bill_date or None,
                bill_amount,
                new_pending,
                billing_fin_year or None,
                billing_quarters,
                billing_form_types,
                billing_months,
                loading_charges,
                gst_registration_fee,
                application_type or None,
                billing_remarks or None,
                billing_narrative or None,
                pay_to or None,
                task_id
            ))

            if cursor.rowcount == 0:

                conn.rollback()

                messagebox.showerror(
                    "Error",
                    "No task was updated."
                )

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
                    %s,
                    %s,
                    %s,
                    %s
                )
            """, (
                task_id,
                "BILL_UPDATED_BY_ADMIN",
                self.user["id"],
                bill_amount,
                (
                    f"Bill updated by admin. "
                    f"Bill number: {bill_number or '-'}; "
                    f"Previous amount: ₹{old_bill_amount:.2f}; "
                    f"New amount: ₹{bill_amount:.2f}; "
                    f"Already received: ₹{actual_received:.2f}; "
                    f"New pending: ₹{new_pending:.2f}"
                )
            ))

            conn.commit()

        except psycopg.errors.UniqueViolation:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Error",
                "That bill number already exists."
            )

            return

        except psycopg.Error as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to update bill:\n{e}"
            )

            return

        except Exception as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Error",
                str(e)
            )

            return

        finally:

            if cursor:
                cursor.close()

            if conn:
                conn.close()

        # =====================================================
        # SUCCESS
        # =====================================================

        messagebox.showinfo(
            "Success",
            (
                "Bill updated successfully.\n\n"
                f"Bill Number: {bill_number or '-'}\n"
                f"Bill Amount: ₹{bill_amount:.2f}\n"
                f"Already Received: ₹{actual_received:.2f}\n"
                f"Amount Pending: ₹{new_pending:.2f}"
            )
        )

        self.load_records(
            selected_task_id=task_id
        )
