
import customtkinter as ctk


# ============================================================
# IO SYSTEM COLOUR PALETTE
# ============================================================
from theme import *


class Dashboard(ctk.CTkFrame):

    def __init__(self, master, user, on_logout):

        super().__init__(
            master,
            fg_color=BACKGROUND,
            corner_radius=0
        )

        self.user = user
        self.on_logout = on_logout

        # =====================================================
        # GRID
        # =====================================================

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # =====================================================
        # SIDEBAR
        # =====================================================

        self.sidebar_frame = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color=SIDEBAR
        )

        self.sidebar_frame.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar_frame.grid_columnconfigure(
            0,
            weight=1
        )

        # Give the logout button room at the bottom
        self.sidebar_frame.grid_rowconfigure(
            99,
            weight=1
        )

        # =====================================================
        # LOGO
        # =====================================================

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="TASK MANAGEMENT",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            ),
            text_color=TEXT_LIGHT
        )

        self.logo_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=(25, 5)
        )

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Inward • Outward • Billing",
            font=ctk.CTkFont(
                size=14
            ),
            text_color=COLORS['toggle']
        )

        self.subtitle_label.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 20)
        )

        # =====================================================
        # USER INFORMATION
        # =====================================================

        self.user_frame = ctk.CTkFrame(
            self.sidebar_frame,
            fg_color=GOLD,
            corner_radius=8
        )

        self.user_frame.grid(
            row=2,
            column=0,
            padx=15,
            pady=(0, 20),
            sticky="ew"
        )

        self.user_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.user_label = ctk.CTkLabel(
            self.user_frame,
            text=(
                f"{self.user['username']}\n"
                f"{self.user['role']}"
            ),
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            ),
            text_color=TEXT_LIGHT
        )

        self.user_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        # =====================================================
        # NAVIGATION
        # =====================================================

        self.nav_buttons = {}

        row = 3

        # -----------------------------------------------------
        # ENTRY - Employee/Admin
        # -----------------------------------------------------
        if self.user["role"] in [
            "Employee",
            "Admin"
        ]:

            self.add_nav_button(
                "Entry",
                self.show_inward,
                row
            )

            row += 1

        # -----------------------------------------------------
        # UPDATE TASK STATUS - Accounts/Admin/Employee
        # -----------------------------------------------------
        if self.user["role"] in [
            "Accounts",
            "Admin",
            "Employee"
        ]:

            self.add_nav_button(
                "Update Task Status",
                self.show_update_ts,
                row
            )

            row += 1

        # -----------------------------------------------------
        # WORK DONE - Employee/Admin
        # -----------------------------------------------------
        if self.user["role"] in [
            "Employee",
            "Admin"
        ]:

            self.add_nav_button(
                "Work Done",
                self.show_outward_part_1,
                row
            )

            row += 1

        # -----------------------------------------------------
        # DISPATCH - Admin/Employee
        # -----------------------------------------------------
        if self.user["role"] in [
            "Admin",
            "Employee"
        ]:

            self.add_nav_button(
                "Dispatch",
                self.show_outward_part_2,
                row
            )

            row += 1

        # -----------------------------------------------------
        # BILLING & PAYMENTS - Accounts/Admin/Employee
        # -----------------------------------------------------
        if self.user["role"] in [
            "Accounts",
            "Admin",
            "Employee"
        ]:

            self.add_nav_button(
                "Billing & Payments",
                self.show_outward_part_2b,
                row
            )

            row += 1

        # -----------------------------------------------------
        # ADMIN ONLY
        # -----------------------------------------------------
        if self.user["role"] == "Admin":

            # Edit Bill
            self.add_nav_button(
                "Edit Bill",
                self.show_edit_bill,
                row
            )

            row += 1

            # Reassign Work
            self.add_nav_button(
                "Reassign Work",
                self.show_reassign,
                row
            )

            row += 1

            # Pending Bills
            self.add_nav_button(
                "Pending Bills",
                self.show_pb,
                row
            )

            row += 1

            # Pending Work
            self.add_nav_button(
                "Pending Work",
                self.show_pw,
                row
            )

            row += 1

            # Pending Dispatch
            self.add_nav_button(
                "Pending Dispatch",
                self.show_pd,
                row
            )

            row += 1

        # -----------------------------------------------------
        # CLIENTS - All roles
        # -----------------------------------------------------
        self.add_nav_button(
            "Clients",
            self.clients,
            row
        )

        row += 1

        # -----------------------------------------------------
        # SEARCH & REPORTS - Admin only
        # -----------------------------------------------------
        if self.user["role"] == "Admin":

            self.add_nav_button(
                "Search & Reports",
                self.show_reports,
                row
            )

            row += 1

        # -----------------------------------------------------
        # ADMIN PANEL - Admin only
        # -----------------------------------------------------
        if self.user["role"] == "Admin":

            self.add_nav_button(
                "Admin Panel",
                self.show_admin_panel,
                row
            )

            row += 1
        # =====================================================
        # LOGOUT
        # =====================================================

        self.logout_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Logout",
            command=self.on_logout,
            height=38,
            corner_radius=7,
            fg_color=LOGOUT,
            hover_color=LOGOUT_HOVER,
            border_width=1,
            border_color=COLORS['border'],
            text_color=TEXT_LIGHT,
            font=ctk.CTkFont( size=SIZES["sidebar_size"], weight="bold" )
            
        )

        self.logout_button.grid(
            row=99,
            column=0,
            padx=15,
            pady=20,
            sticky="ew"
        )

        # =====================================================
        # MAIN CONTENT
        # =====================================================

        self.main_content = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
        )

        self.main_content.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=20,
            pady=20
        )

        self.main_content.grid_rowconfigure(
            0,
            weight=1
        )

        self.main_content.grid_columnconfigure(
            0,
            weight=1
        )

        self.current_view = None

        # =====================================================
        # DEFAULT VIEW
        # =====================================================

        if self.user["role"] == "Admin":

            self.show_admin_panel()

        elif self.user["role"] == "Accounts":

            self.show_outward_part_2()

        else:

            self.show_inward()

    # =========================================================
    # NAVIGATION BUTTON
    # =========================================================

    def add_nav_button(
        self,
        text,
        command,
        row
    ):

        btn = ctk.CTkButton( self.sidebar_frame, text=text, command=command, height=40, corner_radius=6, fg_color="transparent", hover_color=SIDEBAR_HOVER, text_color=TEXT_LIGHT, anchor="w", 
        font=ctk.CTkFont( size=SIZES["sidebar_size"], weight="normal" ) ) 

        btn.grid( row=row, column=0, padx=15, pady=3, sticky="ew" ) 
        self.nav_buttons[text] = btn

    # =========================================================
    # CLEAR CONTENT
    # =========================================================

    def clear_main_content(self):

        for widget in self.main_content.winfo_children():

            widget.destroy()

    # =========================================================
    # INWARD
    # =========================================================

    def show_inward(self):

        self.clear_main_content()

        from inward_menu import InwardMenu

        menu = InwardMenu(
            self.main_content,
            self.user
        )

        menu.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # OUTWARD PART 1
    # =========================================================

    def show_outward_part_1(self):

        self.clear_main_content()

        from outward_part_1 import OutwardPart1Menu

        menu = OutwardPart1Menu(
            self.main_content,
            self.user
        )

        menu.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # DISPATCH
    # =========================================================

    def show_outward_part_2(self):

        self.clear_main_content()

        from outward_part_2 import OutwardPart2Menu

        menu = OutwardPart2Menu(
            self.main_content,
            self.user
        )

        menu.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # REPORTS
    # =========================================================

    def show_reports(self):

        self.clear_main_content()

        from reports_menu import ReportsMenu

        menu = ReportsMenu(
            self.main_content,
            self.user
        )

        menu.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # CLIENTS
    # =========================================================

    def clients(self):

        self.clear_main_content()

        from add_cli import Client

        menu = Client(
            self.main_content,
            self.user
        )

        menu.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # BILLING & PAYMENTS
    # =========================================================

    def show_outward_part_2b(self):

        self.clear_main_content()

        from outward_part_2b import OutwardPart2BMenu

        menu = OutwardPart2BMenu(
            self.main_content,
            self.user
        )

        menu.pack(
            fill="both",
            expand=True
        )

    # =========================================================
    # ADMIN PANEL
    # =========================================================

    def show_admin_panel(self):

        self.clear_main_content()

        from admin_panel import AdminPanel

        panel = AdminPanel(
            self.main_content
        )

        panel.pack(
            fill="both",
            expand=True
        )

    def show_reassign(self):
    
            self.clear_main_content()
    
            from reassign import AdminReassignWork
    
            menu = AdminReassignWork(
                self.main_content,
                self.user
            )
    
            menu.pack(
                fill="both",
                expand=True
            )

    def show_edit_bill(self):
    
            self.clear_main_content()
    
            from update_bill import AdminBillUpdate
    
            menu = AdminBillUpdate(
                self.main_content,
                self.user
            )
    
            menu.pack(
                fill="both",
                expand=True
            )

    def show_pb(self):
        
                self.clear_main_content()
        
                from pending_bills import PendingBills
        
                menu = PendingBills(
                    self.main_content,
                    self.user
                )
        
                menu.pack(
                    fill="both",
                    expand=True
                )
    def show_pw(self):
        
                self.clear_main_content()
        
                from pending_work import PendingWork
        
                menu = PendingWork(
                    self.main_content,
                    self.user
                )
        
                menu.pack(
                    fill="both",
                    expand=True
                )
    def show_pd(self):
        
                self.clear_main_content()
        
                from pending_dispatch import PendingDispatch
        
                menu = PendingDispatch(
                    self.main_content,
                    self.user
                )
        
                menu.pack(
                    fill="both",
                    expand=True
                )
    def show_update_ts(self):
            
                    self.clear_main_content()
            
                    from UpdateTaskStatus import UpdateTaskStatus
            
                    menu = UpdateTaskStatus(
                        self.main_content,
                        self.user
                    )
            
                    menu.pack(
                        fill="both",
                        expand=True
                    )