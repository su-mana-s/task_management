import customtkinter as ctk
import sqlite3

from tkinter import messagebox

from database import DB_NAME
from theme import *

from searchable_combobox import SearchableComboBox


class AdminBillUpdate(ctk.CTkFrame):

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
            text="Admin - Update Bill Amount",
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

            width=650,
            height=SIZES["entry_height"],

            # font=self.normal_font,
            # dropdown_font=self.normal_font,
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
        # CURRENT BILL INFORMATION
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

        # -----------------------------------------------------
        # BILL NUMBER
        # -----------------------------------------------------

        self.create_label(
            "Bill Number:",
            2
        )

        self.bill_number_label = ctk.CTkLabel(
            self.form_frame,
            text="-",
            font=self.bold_font,
            text_color=COLORS["text"]
        )

        self.bill_number_label.grid(
            row=2,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # -----------------------------------------------------
        # BILL DATE
        # -----------------------------------------------------

        self.create_label(
            "Bill Date:",
            3
        )

        self.bill_date_label = ctk.CTkLabel(
            self.form_frame,
            text="-",
            font=self.bold_font,
            text_color=COLORS["text"]
        )

        self.bill_date_label.grid(
            row=3,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # -----------------------------------------------------
        # ORIGINAL BILL AMOUNT
        # -----------------------------------------------------

        self.create_label(
            "Current Bill Amount:",
            4
        )

        self.current_bill_label = ctk.CTkLabel(
            self.form_frame,
            text="₹0.00",
            font=self.bold_font,
            text_color=COLORS["primary_hover"]
        )

        self.current_bill_label.grid(
            row=4,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # -----------------------------------------------------
        # ALREADY RECEIVED
        # -----------------------------------------------------

        self.create_label(
            "Already Received:",
            5
        )

        self.received_label = ctk.CTkLabel(
            self.form_frame,
            text="₹0.00",
            font=self.bold_font,
            text_color=COLORS["success"]
        )

        self.received_label.grid(
            row=5,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # -----------------------------------------------------
        # CURRENT BALANCE
        # -----------------------------------------------------

        self.create_label(
            "Current Balance:",
            6
        )

        self.current_balance_label = ctk.CTkLabel(
            self.form_frame,
            text="₹0.00",
            font=self.bold_font,
            text_color=COLORS["warning"]
        )

        self.current_balance_label.grid(
            row=6,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )

        # =====================================================
        # UPDATE SECTION
        # =====================================================

        ctk.CTkLabel(
            self.form_frame,
            text="UPDATE BILL AMOUNT",
            font=self.heading_font,
            text_color=COLORS["primary"]
        ).grid(
            row=7,
            column=0,
            columnspan=2,
            padx=PADDING["x"],
            pady=(35, 15),
            sticky="w"
        )

        self.create_label(
            "New Bill Amount:",
            8
        )

        self.new_amount_entry = ctk.CTkEntry(
            self.form_frame,
            width=300,
            height=SIZES["entry_height"],
            font=self.normal_font,

            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],

            placeholder_text="Enter new bill amount",
            placeholder_text_color=COLORS["placeholder"],

            corner_radius=SIZES["corner_radius"]
        )

        self.new_amount_entry.grid(
            row=8,
            column=1,
            padx=PADDING["x"],
            pady=PADDING["y"],
            sticky="w"
        )
        self.new_amount_entry.bind(
            "<KeyRelease>",
            lambda event: self.update_preview()
        )
        # =====================================================
        # NEW BALANCE PREVIEW
        # =====================================================

        self.create_label(
            "New Balance:",
            9
        )

        self.new_balance_label = ctk.CTkLabel(
            self.form_frame,
            text="₹0.00",
            font=ctk.CTkFont(
                size=SIZES["normal_size"],
                weight="bold"
            ),
            text_color=COLORS["warning"]
        )

        self.new_balance_label.grid(
            row=9,
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

            text="Update Bill Amount",

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
            row=10,
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
                "Note: Bill number and bill date cannot be changed. "
                "Only the bill amount can be modified."
            ),
            font=self.normal_font,
            text_color=COLORS["text_secondary"],
            wraplength=700,
            justify="left"
        )

        self.note_label.grid(
            row=11,
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
    # LOAD RECORDS
    # =========================================================

    def load_records(
        self,
        selected_record_id=None
    ):

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
                    r.bill_date,
                    r.bill_amount,
                    r.actual_amount_received,
                    r.amount_pending_receipt
                FROM records r

                LEFT JOIN clients c
                    ON r.client_id = c.id

                WHERE
                    r.bill_number IS NOT NULL
                    AND TRIM(r.bill_number) != ''
                    AND r.bill_amount IS NOT NULL
                    AND r.bill_amount > 0

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
                bill_date,
                bill_amount,
                actual_received,
                pending
            ) = record

            bill_amount = float(bill_amount or 0)
            actual_received = float(actual_received or 0)
            pending = float(pending or 0)

            display = (
                f"ID: {record_id} | "
                f"{client_name or '-'} | "
                f"{department or '-'} | "
                f"{nature or '-'} | "
                f"Bill: {bill_number} | "
                f"Amount: ₹{bill_amount:.2f} | "
                f"Balance: ₹{pending:.2f}"
            )

            self.case_map[display] = record_id

            display_values.append(display)

        if display_values:

            self.case_dropdown.configure_values(
                values=display_values
            )

            selected_display = display_values[0]

            if selected_record_id is not None:

                for display_text, rid in self.case_map.items():

                    if rid == selected_record_id:

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

        record_id = self.case_map.get(choice)

        if not record_id:

            return

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT
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
            bill_number,
            bill_date,
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

        self.bill_number_label.configure(
            text=str(bill_number or "-")
        )

        self.bill_date_label.configure(
            text=str(bill_date or "-")
        )

        self.current_bill_label.configure(
            text=f"₹{bill_amount:.2f}"
        )

        self.received_label.configure(
            text=f"₹{actual_received:.2f}"
        )

        self.current_balance_label.configure(
            text=f"₹{pending:.2f}"
        )

        self.new_amount_entry.delete(
            0,
            "end"
        )

        self.new_amount_entry.insert(
            0,
            f"{bill_amount:.2f}"
        )

        self.new_balance_label.configure(
            text=f"₹{pending:.2f}"
        )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear_bill_information(self):

        self.bill_number_label.configure(
            text="-"
        )

        self.bill_date_label.configure(
            text="-"
        )

        self.current_bill_label.configure(
            text="₹0.00"
        )

        self.received_label.configure(
            text="₹0.00"
        )

        self.current_balance_label.configure(
            text="₹0.00"
        )

        self.new_balance_label.configure(
            text="₹0.00"
        )

        self.new_amount_entry.delete(
            0,
            "end"
        )

    # =========================================================
    # UPDATE PREVIEW
    # =========================================================

    def update_preview(self):

        selected = self.case_var.get()

        record_id = self.case_map.get(
            selected
        )

        if not record_id:

            return

        amount_text = (
            self.new_amount_entry
            .get()
            .strip()
        )

        try:

            new_amount = float(
                amount_text
            )

        except ValueError:

            self.new_balance_label.configure(
                text="Invalid amount"
            )

            return

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

            cursor.execute("""
                SELECT actual_amount_received
                FROM records
                WHERE inward_id = ?
            """, (
                record_id,
            ))

            result = cursor.fetchone()

        finally:

            conn.close()

        if not result:

            return

        received = float(
            result[0] or 0
        )

        new_balance = new_amount - received

        if new_balance < 0:

            self.new_balance_label.configure(
                text="Cannot be less than received amount"
            )

        else:

            self.new_balance_label.configure(
                text=f"₹{new_balance:.2f}"
            )

    # =========================================================
    # UPDATE BILL
    # =========================================================

    def update_bill(self):

        selected = self.case_var.get()

        record_id = self.case_map.get(
            selected
        )

        if not record_id:

            messagebox.showerror(
                "Error",
                "Please select a valid billed work record."
            )

            return

        amount_text = (
            self.new_amount_entry
            .get()
            .strip()
        )

        if not amount_text:

            messagebox.showerror(
                "Error",
                "Please enter the new bill amount."
            )

            return

        try:

            new_amount = float(
                amount_text
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Invalid bill amount."
            )

            return

        if new_amount <= 0:

            messagebox.showerror(
                "Error",
                "Bill amount must be greater than zero."
            )

            return

        conn = sqlite3.connect(DB_NAME)

        try:

            cursor = conn.cursor()

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
                old_amount,
                received
            ) = record

            old_amount = float(
                old_amount or 0
            )

            received = float(
                received or 0
            )

            # -------------------------------------------------
            # IMPORTANT:
            # The new bill cannot be lower than money already
            # received from the client.
            # -------------------------------------------------

            if new_amount < received:

                messagebox.showerror(
                    "Invalid Amount",
                    (
                        "The new bill amount cannot be less "
                        "than the amount already received.\n\n"
                        f"Already received: ₹{received:.2f}"
                    )
                )

                return

            new_pending = new_amount - received

            # -------------------------------------------------
            # UPDATE BILL AMOUNT ONLY
            # -------------------------------------------------

            cursor.execute("""
                UPDATE records
                SET
                    bill_amount = ?,
                    amount_pending_receipt = ?
                WHERE inward_id = ?
                  AND bill_number IS NOT NULL
                  AND TRIM(bill_number) != ''
            """, (
                new_amount,
                new_pending,
                record_id
            ))

            if cursor.rowcount == 0:

                messagebox.showerror(
                    "Error",
                    "This work does not have a generated bill."
                )

                conn.rollback()

                return

            # -------------------------------------------------
            # AUDIT LOG
            # -------------------------------------------------

            cursor.execute("""
                INSERT INTO activity_log (
                    record_id,
                    action_type,
                    performed_by,
                    amount,
                    description
                )
                VALUES (?, 'BILL_AMOUNT_UPDATED', ?, ?, ?)
            """, (
                record_id,
                self.user["id"],
                new_amount,
                (
                    f"Bill {bill_number} amount changed "
                    f"from ₹{old_amount:.2f} "
                    f"to ₹{new_amount:.2f}"
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

        messagebox.showinfo(
            "Success",
            (
                "Bill amount updated successfully.\n\n"
                f"Bill Number: {bill_number}\n"
                f"Old Amount: ₹{old_amount:.2f}\n"
                f"New Amount: ₹{new_amount:.2f}\n"
                f"Already Received: ₹{received:.2f}\n"
                f"New Balance: ₹{new_pending:.2f}"
            )
        )

        self.load_records(
            selected_record_id=record_id
        )

