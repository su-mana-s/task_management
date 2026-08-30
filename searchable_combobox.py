
import customtkinter as ctk


class SearchableComboBox(ctk.CTkFrame):

    def __init__(
        self,
        master,
        values=None,
        variable=None,
        command=None,
        width=400,
        height=40,
        font=None,
        dropdown_font=None,
        fg_color=None,
        border_color=None,
        button_color=None,
        button_hover_color=None,
        text_color=None,
        dropdown_fg_color=None,
        dropdown_text_color=None,
        dropdown_hover_color=None,
        corner_radius=10,
        **kwargs
    ):

        super().__init__(
            master,
            fg_color="transparent"
        )

        self.values = list(values or [])
        self.filtered_values = self.values.copy()

        self.variable = (
            variable
            if variable is not None
            else ctk.StringVar()
        )

        self.command = command

        self.width = width
        self.height = height

        self.font = font
        self.dropdown_font = dropdown_font or font

        self.fg_color = fg_color
        self.border_color = border_color
        self.button_color = button_color
        self.button_hover_color = button_hover_color
        self.text_color = text_color
        self.dropdown_fg_color = dropdown_fg_color
        self.dropdown_text_color = dropdown_text_color
        self.dropdown_hover_color = dropdown_hover_color
        self.corner_radius = corner_radius

        self.is_open = False

        # =====================================================
        # MAIN ENTRY
        # =====================================================

        self.entry = ctk.CTkEntry(
            self,
            width=width - 45,
            height=height,
            textvariable=self.variable,
            font=font,
            fg_color=fg_color,
            border_color=border_color,
            text_color=text_color,
            **kwargs
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        # =====================================================
        # DROPDOWN BUTTON
        # =====================================================

        self.button = ctk.CTkButton(
            self,
            text="▼",
            width=45,
            height=height,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            fg_color=button_color,
            hover_color=button_hover_color,
            text_color=text_color,
            corner_radius=0,
            command=self.toggle_dropdown
        )

        self.button.pack(
            side="right"
        )

        # =====================================================
        # EVENTS
        # =====================================================

        self.entry.bind(
            "<KeyRelease>",
            self.on_type
        )

        self.entry.bind(
            "<FocusIn>",
            self.on_focus
        )

        self.entry.bind(
            "<Down>",
            self.open_dropdown_event
        )

        # =====================================================
        # DROPDOWN
        # =====================================================

        self.dropdown = None

    # =========================================================
    # SET VALUES
    # =========================================================

    def configure_values(self, values):

        self.values = list(values or [])
        self.filtered_values = self.values.copy()

    # =========================================================
    # FILTER
    # =========================================================

    def on_type(self, event=None):

        search_text = self.variable.get().strip().lower()

        if not search_text:

            self.filtered_values = self.values.copy()

        else:

            self.filtered_values = [
                value
                for value in self.values
                if search_text in str(value).lower()
            ]

        self.show_dropdown()

    # =========================================================
    # FOCUS
    # =========================================================

    def on_focus(self, event=None):

        self.show_dropdown()

    # =========================================================
    # TOGGLE
    # =========================================================

    def toggle_dropdown(self):

        if self.is_open:

            self.hide_dropdown()

        else:

            self.filtered_values = self.values.copy()

            self.show_dropdown()

            self.entry.focus_set()

    # =========================================================
    # OPEN FROM KEYBOARD
    # =========================================================

    def open_dropdown_event(self, event=None):

        self.show_dropdown()

        return "break"

    # =========================================================
    # SHOW DROPDOWN
    # =========================================================

    def show_dropdown(self):

        if self.dropdown is not None:

            self.dropdown.destroy()

        # -----------------------------------------------------
        # Position below the entry
        # -----------------------------------------------------

        self.update_idletasks()

        x = self.winfo_rootx()

        y = (
            self.winfo_rooty()
            + self.winfo_height()
        )

        # -----------------------------------------------------
        # Dropdown window
        # -----------------------------------------------------

        self.dropdown = ctk.CTkToplevel(
            self
        )

        self.dropdown.overrideredirect(
            True
        )

        self.dropdown.geometry(
            f"{self.width}x300+{x}+{y}"
        )

        self.dropdown.configure(
            fg_color=(
                self.dropdown_fg_color
                or self.fg_color
                or "white"
            )
        )

        self.dropdown.lift()

        # -----------------------------------------------------
        # List frame
        # -----------------------------------------------------

        list_frame = ctk.CTkScrollableFrame(
            self.dropdown,
            width=self.width - 20,
            height=280,
            fg_color=(
                self.dropdown_fg_color
                or self.fg_color
                or "white"
            )
        )

        list_frame.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # -----------------------------------------------------
        # No results
        # -----------------------------------------------------

        if not self.filtered_values:

            label = ctk.CTkLabel(
                list_frame,
                text="No matching records",
                font=self.dropdown_font,
                text_color=(
                    self.dropdown_text_color
                    or self.text_color
                )
            )

            label.pack(
                fill="x",
                padx=5,
                pady=8
            )

        # -----------------------------------------------------
        # Results
        # -----------------------------------------------------

        else:

            for value in self.filtered_values:

                btn = ctk.CTkButton(
                    list_frame,
                    text=str(value),
                    anchor="w",
                    height=38,
                    font=self.dropdown_font,
                    fg_color="transparent",
                    hover_color=(
                        self.dropdown_hover_color
                        or self.button_hover_color
                    ),
                    corner_radius=self.corner_radius,
                    text_color=(
                        self.dropdown_text_color
                        or self.text_color
                    ),
                    command=lambda v=value: (
                        self.select_value(v)
                    ),
                    
                )

                btn.pack(
                    fill="x",
                    padx=2,
                    pady=1
                )

        self.is_open = True

        # -----------------------------------------------------
        # Close when focus leaves
        # -----------------------------------------------------

        self.dropdown.bind(
            "<FocusOut>",
            self.on_dropdown_focus_out
        )

    # =========================================================
    # SELECT
    # =========================================================

    def select_value(self, value):

        self.variable.set(
            str(value)
        )

        self.hide_dropdown()

        self.entry.focus_set()

        if self.command:

            self.command(
                str(value)
            )

    # =========================================================
    # HIDE
    # =========================================================

    def hide_dropdown(self):

        if self.dropdown is not None:

            try:
                self.dropdown.destroy()
            except Exception:
                pass

            self.dropdown = None

        self.is_open = False

    # =========================================================
    # FOCUS OUT
    # =========================================================

    def on_dropdown_focus_out(self, event=None):

        self.after(
            100,
            self.check_focus
        )

    def check_focus(self):

        try:

            focused = self.focus_get()

            if focused != self.entry:

                self.hide_dropdown()

        except Exception:

            self.hide_dropdown()

    # =========================================================
    # SET
    # =========================================================

    def set(self, value):

        self.variable.set(
            str(value)
        )

    # =========================================================
    # GET
    # =========================================================

    def get(self):

        return self.variable.get()

    # =========================================================
    # DELETE
    # =========================================================

    def delete(self, first=0, last="end"):

        self.entry.delete(
            first,
            last
        )

    # =========================================================
    # INSERT
    # =========================================================

    def insert(self, index, string):

        self.entry.insert(
            index,
            string
        )

    # =========================================================
    # FOCUS
    # =========================================================

    def focus_set(self):

        self.entry.focus_set()
