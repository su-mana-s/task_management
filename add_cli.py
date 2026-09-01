import re
import sqlite3

import customtkinter as ctk
import phonenumbers

from phonenumbers import NumberParseException
from tkinter import messagebox

from database import get_connection
from theme import *


class Client(ctk.CTkFrame):

    # ================================================================
    # COUNTRY CODES
    # ================================================================

    COUNTRY_CODES = [
        "+91",   # India
        "+1",    # USA / Canada
        "+44",   # UK
        "+61",   # Australia
        "+65",   # Singapore
        "+971",  # UAE
        "+966",  # Saudi Arabia
        "+974",  # Qatar
        "+968",  # Oman
        "+973",  # Bahrain
        "+94",   # Sri Lanka
        "+880",  # Bangladesh
        "+92",   # Pakistan
        "+86",   # China
        "+81",   # Japan
        "+82",   # South Korea
        "+49",   # Germany
        "+33",   # France
        "+39",   # Italy
        "+7",    # Russia / Kazakhstan
    ]

    # ================================================================
    # REGEX VALIDATORS
    # ================================================================

    PAN_PATTERN = re.compile(
        r"^[A-Z]{5}[0-9]{4}[A-Z]$"
    )

    TAN_PATTERN = re.compile(
        r"^[A-Z]{4}[0-9]{5}[A-Z]$"
    )

    GST_PATTERN = re.compile(
        r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z][Z][0-9A-Z]$"
    )

    EMAIL_PATTERN = re.compile(
        r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
        r"[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"
    )

    # ================================================================
    # INIT
    # ================================================================

    def __init__(self, master, user):

        super().__init__(
            master,
            fg_color=COLORS["background"]
        )

        self.user = user

        # Expanded client IDs
        self.expanded_clients = set()

        # Current edit mode
        self.editing_client_id = None

        # ============================================================
        # MAIN PAGE
        # ============================================================

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        # ============================================================
        # PAGE SCROLL
        # ============================================================

        self.page_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )

        self.page_scroll.grid(
            row=0,
            column=0,
            padx=0,
            pady=0,
            sticky="nsew"
        )

        self.page_scroll.grid_columnconfigure(
            0,
            weight=1
        )

        # ============================================================
        # TITLE
        # ============================================================

        self.title_label = ctk.CTkLabel(
            self.page_scroll,
            text="Clients",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            ),
            text_color=COLORS["text"]
        )

        self.title_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=(5, 15),
            sticky="w"
        )

        # ============================================================
        # MAIN CARD
        # ============================================================

        self.clients_frame = ctk.CTkFrame(
            self.page_scroll,
            fg_color=COLORS["card"],
            corner_radius=SIZES["large_corner_radius"],
            border_width=1,
            border_color=COLORS["border"]
        )

        self.clients_frame.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 20),
            sticky="ew"
        )

        self.clients_frame.grid_columnconfigure(
            0,
            weight=1
        )

        # ============================================================
        # SECTION TITLE
        # ============================================================

        self.section_title = ctk.CTkLabel(
            self.clients_frame,
            text="Client Management",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            ),
            text_color=COLORS["text"]
        )

        self.section_title.grid(
            row=0,
            column=0,
            padx=25,
            pady=(25, 5),
            sticky="w"
        )

        self.section_description = ctk.CTkLabel(
            self.clients_frame,
            text="Add new clients and manage your existing clients.",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=COLORS["text_secondary"]
        )

        self.section_description.grid(
            row=1,
            column=0,
            padx=25,
            pady=(0, 20),
            sticky="w"
        )

        # ============================================================
        # FORM
        # ============================================================

        self.add_client_frame = ctk.CTkFrame(
            self.clients_frame,
            fg_color=SIDEBAR_HOVER,
            corner_radius=SIZES["corner_radius"],
            border_width=2,
            border_color=COLORS["border"]
        )

        self.add_client_frame.grid(
            row=2,
            column=0,
            padx=25,
            pady=10,
            sticky="ew"
        )

        self.add_client_frame.grid_columnconfigure(1, weight=1)
        self.add_client_frame.grid_columnconfigure(3, weight=1)

        # ============================================================
        # FORM TITLE
        # ============================================================

        self.form_title = ctk.CTkLabel(
            self.add_client_frame,
            text="New Client",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color=COLORS["toggle"]
        )

        self.form_title.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=20,
            pady=(18, 5),
            sticky="w"
        )

        # ============================================================
        # NAME
        # ============================================================

        self.client_name_label = ctk.CTkLabel(
            self.add_client_frame,
            text="Name *",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=COLORS["danger_hover"]
        )

        self.client_name_label.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=(10, 8),
            sticky="w"
        )

        self.new_client_name = self.create_entry(
            self.add_client_frame,
            "Enter client name"
        )

        self.new_client_name.grid(
            row=1,
            column=1,
            padx=(0, 15),
            pady=(10, 8),
            sticky="ew"
        )

        # ============================================================
        # MOBILE
        # ============================================================

        self.mobile_label = ctk.CTkLabel(
            self.add_client_frame,
            text="Mobile No. *",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=COLORS["danger_hover"]
        )

        self.mobile_label.grid(
            row=1,
            column=2,
            padx=(10, 10),
            pady=(10, 8),
            sticky="w"
        )

        # ------------------------------------------------------------
        # MOBILE INPUT FRAME
        # ------------------------------------------------------------

        self.mobile_input_frame = ctk.CTkFrame(
            self.add_client_frame,
            fg_color="transparent"
        )

        self.mobile_input_frame.grid(
            row=1,
            column=3,
            padx=(0, 20),
            pady=(10, 8),
            sticky="ew"
        )

        self.mobile_input_frame.grid_columnconfigure(
            1,
            weight=1
        )

        # ------------------------------------------------------------
        # COUNTRY CODE
        # ------------------------------------------------------------

        self.country_code_dropdown = ctk.CTkComboBox(
            self.mobile_input_frame,
            values=self.COUNTRY_CODES,
            width=90,
            height=42,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            button_color=COLORS["input"],
            button_hover_color=SIDEBAR_HOVER,
            dropdown_fg_color=COLORS["card"],
            dropdown_hover_color=SIDEBAR_HOVER,
            dropdown_text_color=COLORS["text"],
            text_color=COLORS["text"],
            corner_radius=SIZES["corner_radius"],
            font=ctk.CTkFont(size=14)
        )

        self.country_code_dropdown.set("+91")

        self.country_code_dropdown.grid(
            row=0,
            column=0,
            padx=(0, 8),
            sticky="w"
        )

        # ------------------------------------------------------------
        # MOBILE ENTRY
        # ------------------------------------------------------------

        self.new_client_mobile = self.create_entry(
            self.mobile_input_frame,
            "Enter mobile number"
        )

        self.new_client_mobile.grid(
            row=0,
            column=1,
            sticky="ew"
        )

        # ============================================================
        # EMAIL
        # ============================================================

        self.email_label = self.create_label(
            self.add_client_frame,
            "Email"
        )

        self.email_label.grid(
            row=3,
            column=0,
            padx=(20, 10),
            pady=8,
            sticky="w"
        )

        self.new_client_email = self.create_entry(
            self.add_client_frame,
            "Enter email address"
        )

        self.new_client_email.grid(
            row=3,
            column=1,
            padx=(0, 15),
            pady=8,
            sticky="ew"
        )

        # ============================================================
        # PAN
        # ============================================================

        self.pan_label = self.create_label(
            self.add_client_frame,
            "PAN"
        )

        self.pan_label.grid(
            row=3,
            column=2,
            padx=(10, 10),
            pady=8,
            sticky="w"
        )

        self.new_client_pan = self.create_entry(
            self.add_client_frame,
            "ABCDE1234F"
        )

        self.new_client_pan.grid(
            row=3,
            column=3,
            padx=(0, 20),
            pady=8,
            sticky="ew"
        )

        # ============================================================
        # TAN
        # ============================================================

        self.tan_label = self.create_label(
            self.add_client_frame,
            "TAN"
        )

        self.tan_label.grid(
            row=4,
            column=0,
            padx=(20, 10),
            pady=8,
            sticky="w"
        )

        self.new_client_tan = self.create_entry(
            self.add_client_frame,
            "ABCD12345E"
        )

        self.new_client_tan.grid(
            row=4,
            column=1,
            padx=(0, 15),
            pady=8,
            sticky="ew"
        )

        # ============================================================
        # GST
        # ============================================================

        self.gst_label = self.create_label(
            self.add_client_frame,
            "GST"
        )

        self.gst_label.grid(
            row=4,
            column=2,
            padx=(10, 10),
            pady=8,
            sticky="w"
        )

        self.new_client_gst = self.create_entry(
            self.add_client_frame,
            "22AAAAA0000A1Z5"
        )

        self.new_client_gst.grid(
            row=4,
            column=3,
            padx=(0, 20),
            pady=8,
            sticky="ew"
        )

        # ============================================================
        # FILE NUMBER
        # ============================================================

        self.file_no_label = self.create_label(
            self.add_client_frame,
            "File No."
        )

        self.file_no_label.grid(
            row=5,
            column=0,
            padx=(20, 10),
            pady=8,
            sticky="w"
        )

        self.new_client_file_no = self.create_entry(
            self.add_client_frame,
            "Enter file number"
        )

        self.new_client_file_no.grid(
            row=5,
            column=1,
            padx=(0, 15),
            pady=8,
            sticky="ew"
        )

        # ============================================================
        # AADHAAR
        # ============================================================

        self.aadhar_label = self.create_label(
            self.add_client_frame,
            "Aadhaar"
        )

        self.aadhar_label.grid(
            row=5,
            column=2,
            padx=(10, 10),
            pady=8,
            sticky="w"
        )

        self.new_client_aadhar = self.create_entry(
            self.add_client_frame,
            "12 digit Aadhaar"
        )

        self.new_client_aadhar.grid(
            row=5,
            column=3,
            padx=(0, 20),
            pady=8,
            sticky="ew"
        )

        # ============================================================
        # ADDRESS
        # ============================================================

        self.address_label = self.create_label(
            self.add_client_frame,
            "Address"
        )

        self.address_label.grid(
            row=6,
            column=0,
            padx=(20, 10),
            pady=8,
            sticky="nw"
        )

        self.new_client_address = ctk.CTkTextbox(
            self.add_client_frame,
            height=70,
            fg_color=COLORS["input"],
            border_width=1,
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            corner_radius=SIZES["corner_radius"],
            font=ctk.CTkFont(size=15)
        )

        self.new_client_address.grid(
            row=6,
            column=1,
            columnspan=3,
            padx=(0, 20),
            pady=8,
            sticky="ew"
        )

        # ============================================================
        # FORM BUTTONS
        # ============================================================

        self.cancel_edit_btn = ctk.CTkButton(
            self.add_client_frame,
            text="Cancel",
            command=self.cancel_edit,
            width=120,
            height=44,
            corner_radius=SIZES["corner_radius"],
            fg_color=COLORS["border"],
            hover_color=SIDEBAR_HOVER,
            text_color=COLORS["text"],
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        self.cancel_edit_btn.grid(
            row=7,
            column=2,
            padx=5,
            pady=(10, 20),
            sticky="e"
        )

        self.cancel_edit_btn.grid_remove()

        self.add_client_btn = ctk.CTkButton(
            self.add_client_frame,
            text="＋  Add Client",
            command=self.add_client,
            width=160,
            height=44,
            corner_radius=SIZES["corner_radius"],
            fg_color=LOGOUT,
            hover_color=LOGOUT_HOVER,
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        self.add_client_btn.grid(
            row=7,
            column=3,
            padx=20,
            pady=(10, 20),
            sticky="e"
        )

        # ============================================================
        # CLIENT LIST
        # ============================================================

        self.client_list_title = ctk.CTkLabel(
            self.clients_frame,
            text="Client List",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color=COLORS["text"]
        )

        self.client_list_title.grid(
            row=3,
            column=0,
            padx=25,
            pady=(25, 10),
            sticky="w"
        )

        # ============================================================
        # SEARCH
        # ============================================================

        self.search_frame = ctk.CTkFrame(
            self.clients_frame,
            fg_color=SIDEBAR_HOVER,
            corner_radius=SIZES["corner_radius"],
            border_width=1,
            border_color=COLORS["border"]
        )

        self.search_frame.grid(
            row=4,
            column=0,
            padx=25,
            pady=(0, 10),
            sticky="ew"
        )

        self.search_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.search_label = ctk.CTkLabel(
            self.search_frame,
            text="Search",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=COLORS["text"]
        )

        self.search_label.grid(
            row=0,
            column=0,
            padx=(15, 10),
            pady=10
        )

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search by name, mobile, PAN, GST...",
            height=40,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            corner_radius=SIZES["corner_radius"],
            font=ctk.CTkFont(size=14)
        )

        self.search_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=10,
            sticky="ew"
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.on_search_change
        )

        self.filter_label = ctk.CTkLabel(
            self.search_frame,
            text="Search By",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=COLORS["text"]
        )

        self.filter_label.grid(
            row=0,
            column=2,
            padx=(15, 5),
            pady=10
        )

        self.filter_dropdown = ctk.CTkComboBox(
            self.search_frame,
            values=[
                "All",
                "Name",
                "Mobile",
                "Email",
                "PAN",
                "TAN",
                "GST",
                "File No.",
                "Aadhar"
            ],
            width=150,
            height=40,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            button_color=COLORS["input"],
            button_hover_color=SIDEBAR_HOVER,
            dropdown_fg_color=COLORS["card"],
            dropdown_hover_color=SIDEBAR_HOVER,
            dropdown_text_color=COLORS["text"],
            text_color=COLORS["text"],
            corner_radius=SIZES["corner_radius"],
            font=ctk.CTkFont(size=14),
            command=self.on_filter_change
        )

        self.filter_dropdown.set("All")

        self.filter_dropdown.grid(
            row=0,
            column=3,
            padx=(5, 15),
            pady=10
        )

        # ============================================================
        # RESULTS
        # ============================================================

        self.results_label = ctk.CTkLabel(
            self.clients_frame,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=COLORS["text_secondary"]
        )

        self.results_label.grid(
            row=5,
            column=0,
            padx=25,
            pady=(0, 5),
            sticky="w"
        )

        # ============================================================
        # CLIENT SCROLL
        # ============================================================

        self.client_scroll = ctk.CTkScrollableFrame(
            self.clients_frame,
            fg_color=SIDEBAR_HOVER,
            corner_radius=SIZES["corner_radius"],
            height=520
        )

        self.client_scroll.grid(
            row=6,
            column=0,
            padx=25,
            pady=(0, 25),
            sticky="ew"
        )

        self.client_scroll.grid_columnconfigure(
            0,
            weight=1
        )

        self.load_clients()

    # ================================================================
    # HELPERS
    # ================================================================

    def create_label(self, parent, text):

        return ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=COLORS["text"]
        )

    def create_entry(self, parent, placeholder):

        return ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            height=42,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            corner_radius=SIZES["corner_radius"],
            font=ctk.CTkFont(size=15)
        )

    # ================================================================
    # VALIDATION
    # ================================================================

    def validate_mobile(self, country_code, mobile):

        digits = re.sub(
            r"\D",
            "",
            mobile
        )

        if not digits:
            return None, "Mobile number is required."

        try:

            full_number = f"{country_code}{digits}"

            parsed = phonenumbers.parse(
                full_number,
                None
            )

            if not phonenumbers.is_possible_number(parsed):

                return None, "The mobile number is not a possible number."

            if not phonenumbers.is_valid_number(parsed):

                return None, "The mobile number is not valid for the selected country code."

            formatted = phonenumbers.format_number(
                parsed,
                phonenumbers.PhoneNumberFormat.E164
            )

            return formatted, None

        except NumberParseException:

            return None, "Please enter a valid mobile number."

    def validate_email(self, email):

        if not email:
            return True

        if len(email) > 254:
            return False

        return bool(
            self.EMAIL_PATTERN.fullmatch(email)
        )

    def validate_pan(self, pan):

        if not pan:
            return True

        return bool(
            self.PAN_PATTERN.fullmatch(pan)
        )

    def validate_tan(self, tan):

        if not tan:
            return True

        return bool(
            self.TAN_PATTERN.fullmatch(tan)
        )

    def validate_gst(self, gst):

        if not gst:
            return True

        return bool(
            self.GST_PATTERN.fullmatch(gst)
        )

    def validate_aadhar(self, aadhar):

        if not aadhar:
            return True

        return (
            aadhar.isdigit()
            and len(aadhar) == 12
        )

    # ================================================================
    # READ FORM
    # ================================================================

    def get_form_values(self):

        name = self.new_client_name.get().strip()

        country_code = (
            self.country_code_dropdown.get().strip()
        )

        mobile = self.new_client_mobile.get().strip()

        email = self.new_client_email.get().strip()

        pan = (
            self.new_client_pan
            .get()
            .strip()
            .upper()
        )

        tan = (
            self.new_client_tan
            .get()
            .strip()
            .upper()
        )

        gst = (
            self.new_client_gst
            .get()
            .strip()
            .upper()
        )

        file_no = (
            self.new_client_file_no
            .get()
            .strip()
        )

        aadhar = (
            self.new_client_aadhar
            .get()
            .strip()
        )

        address = (
            self.new_client_address
            .get("1.0", "end")
            .strip()
        )

        # ------------------------------------------------------------
        # NAME
        # ------------------------------------------------------------

        if not name:

            messagebox.showerror(
                "Validation Error",
                "Client name is required."
            )

            self.new_client_name.focus()

            return None

        if len(name) > 150:

            messagebox.showerror(
                "Validation Error",
                "Client name cannot exceed 150 characters."
            )

            self.new_client_name.focus()

            return None

        # ------------------------------------------------------------
        # MOBILE
        # ------------------------------------------------------------

        mobile_e164, error = self.validate_mobile(
            country_code,
            mobile
        )

        if error:

            messagebox.showerror(
                "Invalid Mobile Number",
                error
            )

            self.new_client_mobile.focus()

            return None

        # ------------------------------------------------------------
        # EMAIL
        # ------------------------------------------------------------

        if not self.validate_email(email):

            messagebox.showerror(
                "Invalid Email",
                "Please enter a valid email address."
            )

            self.new_client_email.focus()

            return None

        # ------------------------------------------------------------
        # PAN
        # ------------------------------------------------------------

        if not self.validate_pan(pan):

            messagebox.showerror(
                "Invalid PAN",
                "PAN must be in the format ABCDE1234F."
            )

            self.new_client_pan.focus()

            return None

        # ------------------------------------------------------------
        # TAN
        # ------------------------------------------------------------

        if not self.validate_tan(tan):

            messagebox.showerror(
                "Invalid TAN",
                "TAN must be in the format ABCD12345E."
            )

            self.new_client_tan.focus()

            return None

        # ------------------------------------------------------------
        # GST
        # ------------------------------------------------------------

        if not self.validate_gst(gst):

            messagebox.showerror(
                "Invalid GSTIN",
                "Please enter a valid 15-character GSTIN."
            )

            self.new_client_gst.focus()

            return None

        # ------------------------------------------------------------
        # AADHAAR
        # ------------------------------------------------------------

        if not self.validate_aadhar(aadhar):

            messagebox.showerror(
                "Invalid Aadhaar",
                "Aadhaar must contain exactly 12 digits."
            )

            self.new_client_aadhar.focus()

            return None

        return {
            "name": name,
            "mobile": mobile_e164,
            "email": email or None,
            "address": address or None,
            "pan": pan or None,
            "tan": tan or None,
            "gst": gst or None,
            "file_no": file_no or None,
            "aadhar": aadhar or None
        }

    # ================================================================
    # SEARCH
    # ================================================================

    def on_search_change(self, event=None):

        self.expanded_clients.clear()

        self.load_clients()

    def on_filter_change(self, value=None):

        self.expanded_clients.clear()

        self.load_clients()

    # ================================================================
    # LOAD CLIENTS
    # ================================================================

    def load_clients(self):

        for widget in self.client_scroll.winfo_children():
            widget.destroy()

        search_text = (
            self.search_entry
            .get()
            .strip()
        )

        selected_filter = (
            self.filter_dropdown
            .get()
        )

        clients = []

        conn = None

        try:

            conn = get_connection()

            with conn.cursor() as cursor:

                filter_columns = {
                    "Name": "name",
                    "Mobile": "mobile",
                    "Email": "email",
                    "PAN": "pan",
                    "TAN": "tan",
                    "GST": "gst",
                    "File No.": "file_no",
                    "Aadhar": "aadhar"
                }

                if search_text:

                    pattern = f"%{search_text}%"

                    if selected_filter == "All":

                        cursor.execute(
                            """
                            SELECT
                                id,
                                name,
                                mobile,
                                email,
                                address,
                                pan,
                                tan,
                                gst,
                                file_no,
                                aadhar
                            FROM clients
                            WHERE
                                name ILIKE %s
                                OR mobile ILIKE %s
                                OR email ILIKE %s
                                OR address ILIKE %s
                                OR pan ILIKE %s
                                OR tan ILIKE %s
                                OR gst ILIKE %s
                                OR file_no ILIKE %s
                                OR aadhar ILIKE %s
                            ORDER BY name ASC
                            """,
                            (
                                pattern,
                                pattern,
                                pattern,
                                pattern,
                                pattern,
                                pattern,
                                pattern,
                                pattern,
                                pattern
                            )
                        )

                    else:

                        column = filter_columns.get(
                            selected_filter
                        )

                        if column:

                            # Column comes only from the hardcoded
                            # dictionary above.
                            cursor.execute(
                                f"""
                                SELECT
                                    id,
                                    name,
                                    mobile,
                                    email,
                                    address,
                                    pan,
                                    tan,
                                    gst,
                                    file_no,
                                    aadhar
                                FROM clients
                                WHERE {column} ILIKE %s
                                ORDER BY name ASC
                                """,
                                (pattern,)
                            )

                    clients = cursor.fetchall()

                else:

                    cursor.execute(
                        """
                        SELECT
                            id,
                            name,
                            mobile,
                            email,
                            address,
                            pan,
                            tan,
                            gst,
                            file_no,
                            aadhar
                        FROM clients
                        ORDER BY name ASC
                        """
                    )

                    clients = cursor.fetchall()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not load clients:\n{e}"
            )

        finally:

            if conn:
                conn.close()

        # ============================================================
        # RESULTS
        # ============================================================

        if search_text:

            self.results_label.configure(
                text=f"{len(clients)} client(s) found"
            )

        else:

            self.results_label.configure(
                text=f"{len(clients)} client(s)"
            )

        # ============================================================
        # EMPTY
        # ============================================================

        if not clients:

            if search_text:

                empty_text = (
                    f'No clients found for "{search_text}".'
                )

            else:

                empty_text = (
                    "No clients have been added yet."
                )

            empty_label = ctk.CTkLabel(
                self.client_scroll,
                text=empty_text,
                font=ctk.CTkFont(size=15),
                text_color=COLORS["text_secondary"]
            )

            empty_label.grid(
                row=0,
                column=0,
                padx=20,
                pady=50
            )

            return

        # ============================================================
        # CARDS
        # ============================================================

        for index, client in enumerate(clients):

            (
                cid,
                name,
                mobile,
                email,
                address,
                pan,
                tan,
                gst,
                file_no,
                aadhar
            ) = client

            self.create_client_card(
                index=index,
                cid=cid,
                name=name,
                mobile=mobile,
                email=email,
                address=address,
                pan=pan,
                tan=tan,
                gst=gst,
                file_no=file_no,
                aadhar=aadhar
            )

    # ================================================================
    # CLIENT CARD
    # ================================================================
    def format_mobile_for_display(self, mobile):

        if not mobile:
            return "-"

        try:
            parsed = phonenumbers.parse(
                mobile,
                None
            )

            return phonenumbers.format_number(
                parsed,
                phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )

        except Exception:
            return mobile
    
    def create_client_card(
        self,
        index,
        cid,
        name,
        mobile,
        email,
        address,
        pan,
        tan,
        gst,
        file_no,
        aadhar
    ):

        row_frame = ctk.CTkFrame(
            self.client_scroll,
            fg_color=COLORS["card"],
            corner_radius=SIZES["small_corner_radius"],
            border_width=1,
            border_color=COLORS["border"]
        )

        row_frame.grid(
            row=index,
            column=0,
            padx=8,
            pady=5,
            sticky="ew"
        )

        row_frame.grid_columnconfigure(
            0,
            weight=1
        )

        # ============================================================
        # HEADER
        # ============================================================

        header_frame = ctk.CTkFrame(
            row_frame,
            fg_color="transparent"
        )

        header_frame.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        header_frame.grid_columnconfigure(
            1,
            weight=1,
            minsize=260
        )

        number_label = ctk.CTkLabel(
            header_frame,
            text=str(index + 1),
            width=45,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=COLORS["text_secondary"]
        )

        number_label.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(15, 5),
            pady=10
        )

        name_label = ctk.CTkLabel(
            header_frame,
            text=name or "-",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            text_color=COLORS["text"],
            anchor="w"
        )

        name_label.grid(
            row=0,
            column=1,
            padx=10,
            pady=(10, 2),
            sticky="ew"
        )

        mobile_label = ctk.CTkLabel(
            header_frame,
            text=f"Mobile: {self.format_mobile_for_display(mobile)}",
            font=ctk.CTkFont(
                size=13
            ),
            text_color=COLORS["text_secondary"],
            anchor="w",
            justify="left",
            wraplength=0
        )

        mobile_label.grid(
            row=1,
            column=1,
            padx=10,
            pady=(0, 10),
            sticky="w"
        )

        # ============================================================
        # EDIT BUTTON
        # ============================================================

        edit_button = ctk.CTkButton(
            header_frame,
            text="Edit",
            width=70,
            height=32,
            corner_radius=SIZES["small_corner_radius"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=lambda client_id=cid:
                self.edit_client(client_id)
        )

        edit_button.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=5,
            pady=10
        )

        # ============================================================
        # DELETE BUTTON
        # ============================================================

        delete_button = ctk.CTkButton(
            header_frame,
            text="Delete",
            width=75,
            height=32,
            corner_radius=SIZES["small_corner_radius"],
            fg_color=LOGOUT,
            hover_color=LOGOUT_HOVER,
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=lambda client_id=cid:
                self.delete_client(client_id)
        )

        delete_button.grid(
            row=0,
            column=3,
            rowspan=2,
            padx=5,
            pady=10
        )

        # ============================================================
        # EXPAND BUTTON
        # ============================================================

        is_expanded = (
            cid in self.expanded_clients
        )

        arrow = "▲" if is_expanded else "▼"

        expand_button = ctk.CTkButton(
            header_frame,
            text=arrow,
            width=35,
            height=32,
            corner_radius=SIZES["small_corner_radius"],
            fg_color="transparent",
            hover_color=SIDEBAR_HOVER,
            text_color=COLORS["text_secondary"],
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            command=lambda client_id=cid:
                self.toggle_client(client_id)
        )

        expand_button.grid(
            row=0,
            column=4,
            rowspan=2,
            padx=(5, 15),
            pady=10
        )

        # ============================================================
        # EXPANDED DETAILS
        # ============================================================

        if is_expanded:

            details_frame = ctk.CTkFrame(
                row_frame,
                fg_color=SIDEBAR_HOVER,
                corner_radius=SIZES["small_corner_radius"]
            )

            details_frame.grid(
                row=1,
                column=0,
                padx=10,
                pady=(0, 10),
                sticky="ew"
            )

            details_frame.grid_columnconfigure(
                1,
                weight=1
            )

            details_frame.grid_columnconfigure(
                3,
                weight=1
            )

            details_title = ctk.CTkLabel(
                details_frame,
                text="Client Details",
                font=ctk.CTkFont(
                    size=15,
                    weight="bold"
                ),
                text_color=COLORS["toggle"]
            )

            details_title.grid(
                row=0,
                column=0,
                columnspan=4,
                padx=15,
                pady=(15, 10),
                sticky="w"
            )

            self.add_detail(
                details_frame,
                "Email",
                email,
                1,
                0
            )

            self.add_detail(
                details_frame,
                "PAN",
                pan,
                1,
                2
            )

            self.add_detail(
                details_frame,
                "TAN",
                tan,
                2,
                0
            )

            self.add_detail(
                details_frame,
                "GST",
                gst,
                2,
                2
            )

            self.add_detail(
                details_frame,
                "File No.",
                file_no,
                3,
                0
            )

            self.add_detail(
                details_frame,
                "Aadhaar",
                aadhar,
                3,
                2
            )

            self.add_detail(
                details_frame,
                "Mobile",
                mobile,
                4,
                0
            )

            address_label = ctk.CTkLabel(
                details_frame,
                text="Address",
                font=ctk.CTkFont(
                    size=13,
                    weight="bold"
                ),
                text_color=COLORS["text_secondary"],
                anchor="nw"
            )

            address_label.grid(
                row=5,
                column=0,
                padx=(15, 10),
                pady=(8, 15),
                sticky="nw"
            )

            address_value = ctk.CTkLabel(
                details_frame,
                text=address or "-",
                font=ctk.CTkFont(size=14),
                text_color=COLORS["text"],
                justify="left",
                anchor="nw",
                wraplength=700
            )

            address_value.grid(
                row=5,
                column=1,
                columnspan=3,
                padx=(0, 15),
                pady=(8, 15),
                sticky="w"
            )

    # ================================================================
    # DETAIL
    # ================================================================

    def add_detail(
        self,
        parent,
        label_text,
        value,
        row,
        column
    ):

        label = ctk.CTkLabel(
            parent,
            text=label_text,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=COLORS["toggle"],
            anchor="w"
        )

        label.grid(
            row=row,
            column=column,
            padx=(15, 10),
            pady=7,
            sticky="w"
        )

        value_label = ctk.CTkLabel(
            parent,
            text=value or "-",
            font=ctk.CTkFont(size=14),
            text_color=COLORS["text"],
            anchor="w"
        )

        value_label.grid(
            row=row,
            column=column + 1,
            padx=(0, 15),
            pady=7,
            sticky="w"
        )

    # ================================================================
    # TOGGLE
    # ================================================================

    def toggle_client(self, client_id):

        if client_id in self.expanded_clients:

            self.expanded_clients.remove(
                client_id
            )

        else:

            self.expanded_clients.add(
                client_id
            )

        self.load_clients()

    # ================================================================
    # ADD CLIENT
    # ================================================================

    def add_client(self):

        values = self.get_form_values()

        if not values:
            return

        conn = None

        try:

            conn = get_connection()

            with conn.cursor() as cursor:

                # ----------------------------------------------------
                # EXTRA DUPLICATE CHECK
                # ----------------------------------------------------

                cursor.execute(
                    """
                    SELECT id
                    FROM clients
                    WHERE mobile = %s
                    LIMIT 1
                    """,
                    (values["mobile"],)
                )

                existing = cursor.fetchone()

                if existing:

                    messagebox.showerror(
                        "Duplicate Client",
                        "A client with this mobile number already exists."
                    )

                    self.new_client_mobile.focus()

                    return

                # ----------------------------------------------------
                # INSERT
                # ----------------------------------------------------

                cursor.execute(
                    """
                    INSERT INTO clients (
                        name,
                        mobile,
                        email,
                        address,
                        pan,
                        tan,
                        gst,
                        file_no,
                        aadhar
                    )
                    VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s
                    )
                    """,
                    (
                        values["name"],
                        values["mobile"],
                        values["email"],
                        values["address"],
                        values["pan"],
                        values["tan"],
                        values["gst"],
                        values["file_no"],
                        values["aadhar"]
                    )
                )

            conn.commit()

            self.clear_form()

            self.search_entry.delete(
                0,
                "end"
            )

            self.filter_dropdown.set(
                "All"
            )

            self.expanded_clients.clear()

            self.load_clients()

            messagebox.showinfo(
                "Success",
                "Client added successfully."
            )

            self.new_client_name.focus()

        except Exception as e:

            if conn:
                conn.rollback()

            # PostgreSQL UNIQUE violation
            if "duplicate key" in str(e).lower():

                messagebox.showerror(
                    "Duplicate Client",
                    "A client with this mobile number already exists."
                )

            else:

                messagebox.showerror(
                    "Database Error",
                    f"Could not add client:\n{e}"
                )

        finally:

            if conn:
                conn.close()

    # ================================================================
    # EDIT CLIENT
    # ================================================================

    def edit_client(self, client_id):

        conn = None

        try:

            conn = get_connection()

            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        id,
                        name,
                        mobile,
                        email,
                        address,
                        pan,
                        tan,
                        gst,
                        file_no,
                        aadhar
                    FROM clients
                    WHERE id = %s
                    """,
                    (client_id,)
                )

                client = cursor.fetchone()

            if not client:

                messagebox.showerror(
                    "Error",
                    "Client could not be found."
                )

                return

            (
                cid,
                name,
                mobile,
                email,
                address,
                pan,
                tan,
                gst,
                file_no,
                aadhar
            ) = client

            # --------------------------------------------------------
            # COUNTRY CODE / MOBILE
            # --------------------------------------------------------

            country_code = "+91"
            national_mobile = mobile or ""

            try:

                parsed = phonenumbers.parse(
                    mobile,
                    None
                )

                country_code = (
                    "+"
                    + str(
                        parsed.country_code
                    )
                )

                national_mobile = str(
                    parsed.national_number
                )

            except Exception:
                pass

            self.country_code_dropdown.set(
                country_code
            )

            self.set_entry(
                self.new_client_name,
                name
            )

            self.set_entry(
                self.new_client_mobile,
                national_mobile
            )

            self.set_entry(
                self.new_client_email,
                email
            )

            self.set_entry(
                self.new_client_pan,
                pan
            )

            self.set_entry(
                self.new_client_tan,
                tan
            )

            self.set_entry(
                self.new_client_gst,
                gst
            )

            self.set_entry(
                self.new_client_file_no,
                file_no
            )

            self.set_entry(
                self.new_client_aadhar,
                aadhar
            )

            self.new_client_address.delete(
                "1.0",
                "end"
            )

            if address:
                self.new_client_address.insert(
                    "1.0",
                    address
                )

            # --------------------------------------------------------
            # ENTER EDIT MODE
            # --------------------------------------------------------

            self.editing_client_id = cid

            self.form_title.configure(
                text="Edit Client"
            )

            self.add_client_btn.configure(
                text="✓  Save Changes",
                command=self.update_client
            )

            self.cancel_edit_btn.grid()

            self.new_client_name.focus()

            # Scroll page toward form
            self.page_scroll._parent_canvas.yview_moveto(0)

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not load client:\n{e}"
            )

        finally:

            if conn:
                conn.close()

    # ================================================================
    # SET ENTRY
    # ================================================================

    def set_entry(self, entry, value):

        entry.delete(
            0,
            "end"
        )

        if value:
            entry.insert(
                0,
                value
            )

    # ================================================================
    # UPDATE CLIENT
    # ================================================================

    def update_client(self):

        if self.editing_client_id is None:
            return

        values = self.get_form_values()

        if not values:
            return

        conn = None

        try:

            conn = get_connection()

            with conn.cursor() as cursor:

                # ----------------------------------------------------
                # DUPLICATE MOBILE
                # ----------------------------------------------------

                cursor.execute(
                    """
                    SELECT id
                    FROM clients
                    WHERE mobile = %s
                      AND id <> %s
                    LIMIT 1
                    """,
                    (
                        values["mobile"],
                        self.editing_client_id
                    )
                )

                duplicate = cursor.fetchone()

                if duplicate:

                    messagebox.showerror(
                        "Duplicate Mobile",
                        "Another client already uses this mobile number."
                    )

                    self.new_client_mobile.focus()

                    return

                # ----------------------------------------------------
                # UPDATE
                # ----------------------------------------------------

                cursor.execute(
                    """
                    UPDATE clients
                    SET
                        name = %s,
                        mobile = %s,
                        email = %s,
                        address = %s,
                        pan = %s,
                        tan = %s,
                        gst = %s,
                        file_no = %s,
                        aadhar = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                    """,
                    (
                        values["name"],
                        values["mobile"],
                        values["email"],
                        values["address"],
                        values["pan"],
                        values["tan"],
                        values["gst"],
                        values["file_no"],
                        values["aadhar"],
                        self.editing_client_id
                    )
                )

                if cursor.rowcount == 0:

                    conn.rollback()

                    messagebox.showerror(
                        "Error",
                        "Client could not be updated."
                    )

                    return

            conn.commit()

            edited_id = self.editing_client_id

            self.cancel_edit()

            self.expanded_clients.add(
                edited_id
            )

            self.load_clients()

            messagebox.showinfo(
                "Success",
                "Client updated successfully."
            )

        except Exception as e:

            if conn:
                conn.rollback()

            if "duplicate key" in str(e).lower():

                messagebox.showerror(
                    "Duplicate Mobile",
                    "Another client already uses this mobile number."
                )

            else:

                messagebox.showerror(
                    "Database Error",
                    f"Could not update client:\n{e}"
                )

        finally:

            if conn:
                conn.close()

    # ================================================================
    # DELETE CLIENT
    # ================================================================

    def delete_client(self, client_id):

        answer = messagebox.askyesno(
            "Delete Client",
            "Are you sure you want to delete this client?\n\n"
            "This action cannot be undone."
        )

        if not answer:
            return

        conn = None

        try:

            conn = get_connection()

            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT name, mobile
                    FROM clients
                    WHERE id = %s
                    """,
                    (client_id,)
                )

                client = cursor.fetchone()

                if not client:

                    messagebox.showerror(
                        "Error",
                        "Client could not be found."
                    )

                    return

                name, mobile = client

                confirm = messagebox.askyesno(
                    "Confirm Delete",
                    f"Delete client:\n\n"
                    f"{name}\n"
                    f"{mobile}\n\n"
                    f"Continue?"
                )

                if not confirm:
                    return

                cursor.execute(
                    """
                    DELETE FROM clients
                    WHERE id = %s
                    """,
                    (client_id,)
                )

            conn.commit()

            self.expanded_clients.discard(
                client_id
            )

            if self.editing_client_id == client_id:
                self.cancel_edit()

            self.load_clients()

            messagebox.showinfo(
                "Deleted",
                "Client deleted successfully."
            )

        except Exception as e:

            if conn:
                conn.rollback()

            messagebox.showerror(
                "Database Error",
                f"Could not delete client:\n{e}"
            )

        finally:

            if conn:
                conn.close()

    # ================================================================
    # CANCEL EDIT
    # ================================================================

    def cancel_edit(self):

        self.editing_client_id = None

        self.form_title.configure(
            text="New Client"
        )

        self.add_client_btn.configure(
            text="＋  Add Client",
            command=self.add_client
        )

        self.cancel_edit_btn.grid_remove()

        self.clear_form()

        self.new_client_name.focus()

    # ================================================================
    # CLEAR FORM
    # ================================================================

    def clear_form(self):

        entries = [
            self.new_client_name,
            self.new_client_mobile,
            self.new_client_email,
            self.new_client_pan,
            self.new_client_tan,
            self.new_client_gst,
            self.new_client_file_no,
            self.new_client_aadhar
        ]

        for entry in entries:

            entry.delete(
                0,
                "end"
            )

        self.country_code_dropdown.set(
            "+91"
        )

        self.new_client_address.delete(
            "1.0",
            "end"
        )