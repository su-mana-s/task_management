
import customtkinter as ctk
import sqlite3
from database import DB_NAME
from tkinter import messagebox

from theme import *


class Client(ctk.CTkFrame):

    def __init__(self, master, user):

        super().__init__(
            master,
            fg_color=COLORS["background"]
        )

        self.user = user

        # Track expanded client cards
        self.expanded_clients = set()

        # ============================================================
        # MAIN PAGE LAYOUT
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
        # FULL PAGE SCROLLABLE CONTAINER
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
        # PAGE TITLE
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
        # MAIN CLIENT CARD
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

        # ============================================================
        # DESCRIPTION
        # ============================================================

        self.section_description = ctk.CTkLabel(
            self.clients_frame,
            text="Add new clients and view your existing clients.",
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
        # ADD CLIENT PANEL
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

        self.add_client_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.add_client_frame.grid_columnconfigure(
            3,
            weight=1
        )

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

        self.new_client_mobile = self.create_entry(
            self.add_client_frame,
            "Enter mobile number"
        )

        self.new_client_mobile.grid(
            row=1,
            column=3,
            padx=(0, 20),
            pady=(10, 8),
            sticky="ew"
        )

        # ============================================================
        # EMAIL
        # ============================================================

        self.email_label = ctk.CTkLabel(
            self.add_client_frame,
            text="Email",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=COLORS["text"]
        )

        self.email_label.grid(
            row=2,
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
            row=2,
            column=1,
            padx=(0, 15),
            pady=8,
            sticky="ew"
        )

        # ============================================================
        # PAN
        # ============================================================

        self.pan_label = ctk.CTkLabel(
            self.add_client_frame,
            text="PAN",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=COLORS["text"]
        )

        self.pan_label.grid(
            row=2,
            column=2,
            padx=(10, 10),
            pady=8,
            sticky="w"
        )

        self.new_client_pan = self.create_entry(
            self.add_client_frame,
            "Enter PAN"
        )

        self.new_client_pan.grid(
            row=2,
            column=3,
            padx=(0, 20),
            pady=8,
            sticky="ew"
        )

        # ============================================================
        # TAN
        # ============================================================

        self.tan_label = ctk.CTkLabel(
            self.add_client_frame,
            text="TAN",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=COLORS["text"]
        )

        self.tan_label.grid(
            row=3,
            column=0,
            padx=(20, 10),
            pady=8,
            sticky="w"
        )

        self.new_client_tan = self.create_entry(
            self.add_client_frame,
            "Enter TAN"
        )

        self.new_client_tan.grid(
            row=3,
            column=1,
            padx=(0, 15),
            pady=8,
            sticky="ew"
        )

        # ============================================================
        # GST
        # ============================================================

        self.gst_label = ctk.CTkLabel(
            self.add_client_frame,
            text="GST",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=COLORS["text"]
        )

        self.gst_label.grid(
            row=3,
            column=2,
            padx=(10, 10),
            pady=8,
            sticky="w"
        )

        self.new_client_gst = self.create_entry(
            self.add_client_frame,
            "Enter GST number"
        )

        self.new_client_gst.grid(
            row=3,
            column=3,
            padx=(0, 20),
            pady=8,
            sticky="ew"
        )

        # ============================================================
        # FILE NUMBER
        # ============================================================

        self.file_no_label = ctk.CTkLabel(
            self.add_client_frame,
            text="File No.",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=COLORS["text"]
        )

        self.file_no_label.grid(
            row=4,
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
            row=4,
            column=1,
            padx=(0, 15),
            pady=8,
            sticky="ew"
        )

        # ============================================================
        # AADHAR
        # ============================================================

        self.aadhar_label = ctk.CTkLabel(
            self.add_client_frame,
            text="Aadhar",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=COLORS["text"]
        )

        self.aadhar_label.grid(
            row=4,
            column=2,
            padx=(10, 10),
            pady=8,
            sticky="w"
        )

        self.new_client_aadhar = self.create_entry(
            self.add_client_frame,
            "Enter Aadhar number"
        )

        self.new_client_aadhar.grid(
            row=4,
            column=3,
            padx=(0, 20),
            pady=8,
            sticky="ew"
        )

        # ============================================================
        # ADDRESS
        # ============================================================

        self.address_label = ctk.CTkLabel(
            self.add_client_frame,
            text="Address",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=COLORS["text"]
        )

        self.address_label.grid(
            row=5,
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
            font=ctk.CTkFont(
                size=15
            )
        )

        self.new_client_address.grid(
            row=5,
            column=1,
            columnspan=3,
            padx=(0, 20),
            pady=8,
            sticky="ew"
        )

        # ============================================================
        # ADD BUTTON
        # ============================================================

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
            row=6,
            column=0,
            columnspan=4,
            padx=20,
            pady=(10, 20),
            sticky="e"
        )

        # ============================================================
        # CLIENT LIST TITLE
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
        # SEARCH / FILTER
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

        # ------------------------------------------------------------
        # SEARCH LABEL
        # ------------------------------------------------------------

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

        # ------------------------------------------------------------
        # SEARCH ENTRY
        # ------------------------------------------------------------

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search by name, mobile, PAN, GST...",
            height=40,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            corner_radius=SIZES["corner_radius"],
            font=ctk.CTkFont(
                size=14
            )
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

        # ------------------------------------------------------------
        # FILTER LABEL
        # ------------------------------------------------------------

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

        # ------------------------------------------------------------
        # FILTER DROPDOWN
        # ------------------------------------------------------------

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
            font=ctk.CTkFont(
                size=14
            ),
            command=self.on_filter_change
        )

        self.filter_dropdown.set(
            "All"
        )

        self.filter_dropdown.grid(
            row=0,
            column=3,
            padx=(5, 15),
            pady=10
        )

        # ============================================================
        # RESULTS COUNT
        # ============================================================

        self.results_label = ctk.CTkLabel(
            self.clients_frame,
            text="",
            font=ctk.CTkFont(
                size=13
            ),
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
        # CLIENT LIST
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

        # ============================================================
        # LOAD CLIENTS
        # ============================================================

        self.load_clients()

    # ================================================================
    # CREATE ENTRY
    # ================================================================

    def create_entry(
        self,
        parent,
        placeholder
    ):

        return ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            height=42,
            fg_color=COLORS["input"],
            border_color=COLORS["border"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["placeholder"],
            corner_radius=SIZES["corner_radius"],
            font=ctk.CTkFont(
                size=15
            )
        )

    # ================================================================
    # SEARCH CHANGE
    # ================================================================

    def on_search_change(
        self,
        event=None
    ):

        self.expanded_clients.clear()

        self.load_clients()

    # ================================================================
    # FILTER CHANGE
    # ================================================================

    def on_filter_change(
        self,
        value=None
    ):

        self.expanded_clients.clear()

        self.load_clients()

    # ================================================================
    # LOAD CLIENTS
    # ================================================================

    def load_clients(self):

        # ------------------------------------------------------------
        # CLEAR EXISTING CLIENT CARDS
        # ------------------------------------------------------------

        for widget in self.client_scroll.winfo_children():

            widget.destroy()

        search_text = self.search_entry.get().strip()

        selected_filter = self.filter_dropdown.get()

        clients = []

        conn = None

        try:

            conn = sqlite3.connect(DB_NAME)

            cursor = conn.cursor()

            # --------------------------------------------------------
            # FILTER COLUMN MAPPING
            # --------------------------------------------------------

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

            # --------------------------------------------------------
            # SEARCH
            # --------------------------------------------------------

            if search_text:

                if selected_filter == "All":

                    search_pattern = f"%{search_text}%"

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
                            LOWER(COALESCE(name, ''))
                                LIKE LOWER(?)
                            OR LOWER(COALESCE(mobile, ''))
                                LIKE LOWER(?)
                            OR LOWER(COALESCE(email, ''))
                                LIKE LOWER(?)
                            OR LOWER(COALESCE(address, ''))
                                LIKE LOWER(?)
                            OR LOWER(COALESCE(pan, ''))
                                LIKE LOWER(?)
                            OR LOWER(COALESCE(tan, ''))
                                LIKE LOWER(?)
                            OR LOWER(COALESCE(gst, ''))
                                LIKE LOWER(?)
                            OR LOWER(COALESCE(file_no, ''))
                                LIKE LOWER(?)
                            OR LOWER(COALESCE(aadhar, ''))
                                LIKE LOWER(?)
                        ORDER BY name COLLATE NOCASE
                        """,
                        (
                            search_pattern,
                            search_pattern,
                            search_pattern,
                            search_pattern,
                            search_pattern,
                            search_pattern,
                            search_pattern,
                            search_pattern,
                            search_pattern
                        )
                    )

                else:

                    column = filter_columns.get(
                        selected_filter
                    )

                    if column:

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
                            WHERE LOWER(
                                COALESCE({column}, '')
                            ) LIKE LOWER(?)
                            ORDER BY name COLLATE NOCASE
                            """,
                            (
                                f"%{search_text}%",
                            )
                        )

                clients = cursor.fetchall()

            else:

                # ----------------------------------------------------
                # NO SEARCH
                # ----------------------------------------------------

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
                    ORDER BY name COLLATE NOCASE
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
        # RESULTS COUNT
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
        # NO RESULTS
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
                font=ctk.CTkFont(
                    size=15
                ),
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
        # CREATE CLIENT CARDS
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
    # CREATE CLIENT CARD
    # ================================================================

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

        # ============================================================
        # CARD
        # ============================================================

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
            weight=1
        )

        # ------------------------------------------------------------
        # NUMBER
        # ------------------------------------------------------------

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

        # ------------------------------------------------------------
        # NAME
        # ------------------------------------------------------------

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

        # ------------------------------------------------------------
        # MOBILE
        # ------------------------------------------------------------

        mobile_label = ctk.CTkLabel(
            header_frame,
            text=f"Mobile: {mobile or '-'}",
            font=ctk.CTkFont(
                size=13
            ),
            text_color=COLORS["text_secondary"],
            anchor="w"
        )

        mobile_label.grid(
            row=1,
            column=1,
            padx=10,
            pady=(0, 10),
            sticky="w"
        )

        # ------------------------------------------------------------
        # EXPAND ICON
        # ------------------------------------------------------------

        is_expanded = (
            cid in self.expanded_clients
        )

        arrow = "▲" if is_expanded else "▼"

        expand_label = ctk.CTkLabel(
            header_frame,
            text=arrow,
            width=35,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            text_color=COLORS["text_secondary"]
        )

        expand_label.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=(5, 15),
            pady=10
        )

        # ============================================================
        # CLICKABLE HEADER
        # ============================================================

        clickable_widgets = [
            row_frame,
            header_frame,
            number_label,
            name_label,
            mobile_label,
            expand_label
        ]

        for widget in clickable_widgets:

            widget.bind(
                "<Button-1>",
                lambda event, client_id=cid:
                self.toggle_client(client_id)
            )

        # ============================================================
        # EXPANDED DETAILS
        # ============================================================

        if is_expanded:

            details_frame = ctk.CTkFrame(
                row_frame,
                fg_color=SIDEBAR_HOVER,
                corner_radius=SIZES["small_corner_radius"],
                
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

            # --------------------------------------------------------
            # DETAILS TITLE
            # --------------------------------------------------------

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

            # --------------------------------------------------------
            # EMAIL
            # --------------------------------------------------------

            self.add_detail(
                details_frame,
                "Email",
                email,
                1,
                0
            )

            # --------------------------------------------------------
            # PAN
            # --------------------------------------------------------

            self.add_detail(
                details_frame,
                "PAN",
                pan,
                1,
                2
            )

            # --------------------------------------------------------
            # TAN
            # --------------------------------------------------------

            self.add_detail(
                details_frame,
                "TAN",
                tan,
                2,
                0
            )

            # --------------------------------------------------------
            # GST
            # --------------------------------------------------------

            self.add_detail(
                details_frame,
                "GST",
                gst,
                2,
                2
            )

            # --------------------------------------------------------
            # FILE NUMBER
            # --------------------------------------------------------

            self.add_detail(
                details_frame,
                "File No.",
                file_no,
                3,
                0
            )

            # --------------------------------------------------------
            # AADHAR
            # --------------------------------------------------------

            self.add_detail(
                details_frame,
                "Aadhar",
                aadhar,
                3,
                2
            )

            # --------------------------------------------------------
            # MOBILE
            # --------------------------------------------------------

            self.add_detail(
                details_frame,
                "Mobile",
                mobile,
                4,
                0
            )

            # --------------------------------------------------------
            # ADDRESS
            # --------------------------------------------------------

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
                font=ctk.CTkFont(
                    size=14
                ),
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

            # --------------------------------------------------------
            # CLICK DETAILS TO COLLAPSE
            # --------------------------------------------------------

            for widget in details_frame.winfo_children():

                widget.bind(
                    "<Button-1>",
                    lambda event, client_id=cid:
                    self.toggle_client(client_id)
                )

    # ================================================================
    # ADD DETAIL
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
            font=ctk.CTkFont(
                size=14
            ),
            text_color=COLORS["toggle"],
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
    # TOGGLE CLIENT
    # ================================================================

    def toggle_client(
        self,
        client_id
    ):

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
    # CLEAR FORM
    # ================================================================

    def clear_form(self):

        self.new_client_name.delete(
            0,
            "end"
        )

        self.new_client_mobile.delete(
            0,
            "end"
        )

        self.new_client_email.delete(
            0,
            "end"
        )

        self.new_client_pan.delete(
            0,
            "end"
        )

        self.new_client_tan.delete(
            0,
            "end"
        )

        self.new_client_gst.delete(
            0,
            "end"
        )

        self.new_client_file_no.delete(
            0,
            "end"
        )

        self.new_client_aadhar.delete(
            0,
            "end"
        )

        self.new_client_address.delete(
            "1.0",
            "end"
        )

    # ================================================================
    # ADD CLIENT
    # ================================================================

    def add_client(self):

        name = self.new_client_name.get().strip()

        mobile = self.new_client_mobile.get().strip()

        email = self.new_client_email.get().strip()

        pan = self.new_client_pan.get().strip().upper()

        tan = self.new_client_tan.get().strip().upper()

        gst = self.new_client_gst.get().strip().upper()

        file_no = self.new_client_file_no.get().strip()

        aadhar = self.new_client_aadhar.get().strip()

        address = self.new_client_address.get(
            "1.0",
            "end"
        ).strip()

        # ============================================================
        # REQUIRED FIELDS
        # ============================================================

        if not name:

            messagebox.showerror(
                "Error",
                "Client name is required."
            )

            self.new_client_name.focus()

            return

        if not mobile:

            messagebox.showerror(
                "Error",
                "Mobile number is required."
            )

            self.new_client_mobile.focus()

            return

        # ============================================================
        # MOBILE VALIDATION
        # ============================================================

        mobile_digits = "".join(
            character
            for character in mobile
            if character.isdigit()
        )

        if len(mobile_digits) < 10:

            messagebox.showerror(
                "Error",
                "Please enter a valid mobile number."
            )

            self.new_client_mobile.focus()

            return

        # ============================================================
        # EMAIL VALIDATION
        # ============================================================

        if email and (
            "@" not in email
            or "." not in email.split("@")[-1]
        ):

            messagebox.showerror(
                "Error",
                "Please enter a valid email address."
            )

            self.new_client_email.focus()

            return

        # ============================================================
        # AADHAR VALIDATION
        # ============================================================

        if aadhar:

            aadhar_digits = "".join(
                character
                for character in aadhar
                if character.isdigit()
            )

            if len(aadhar_digits) != 12:

                messagebox.showerror(
                    "Error",
                    "Aadhar number must contain 12 digits."
                )

                self.new_client_aadhar.focus()

                return

            aadhar = aadhar_digits

        # ============================================================
        # INSERT CLIENT
        # ============================================================

        conn = None

        try:

            conn = sqlite3.connect(DB_NAME)

            cursor = conn.cursor()

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
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    mobile,
                    email or None,
                    address or None,
                    pan or None,
                    tan or None,
                    gst or None,
                    file_no or None,
                    aadhar or None
                )
            )

            conn.commit()

            # ========================================================
            # CLEAR FORM
            # ========================================================

            self.clear_form()

            # ========================================================
            # RESET SEARCH
            # ========================================================

            self.search_entry.delete(
                0,
                "end"
            )

            self.filter_dropdown.set(
                "All"
            )

            self.expanded_clients.clear()

            # ========================================================
            # REFRESH
            # ========================================================

            self.load_clients()

            messagebox.showinfo(
                "Success",
                "Client added successfully."
            )

            self.new_client_name.focus()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "Client already exists."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"Database error: {e}"
            )

        finally:

            if conn:

                conn.close()
