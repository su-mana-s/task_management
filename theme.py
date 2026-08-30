
# theme.py
#
# Central colour/theme settings for the IO System.
# Import these values into every UI screen.
#


# ============================================================
# IO SYSTEM COLOURS
# ============================================================
SIDEBAR = "#0B4008"
SIDEBAR_HOVER = "#7F872E"

GOLD = "#AE8514"

PRIMARY = "#570000"
PRIMARY_HOVER = "#5E6F36"

LOGOUT = "#6D1218"
LOGOUT_HOVER = "#962104"

TEXT_LIGHT = "#F7E7CE"
TEXT_MUTED = "#7F872E"

BACKGROUND = ("#F7E7CE", "#0F172A")


COLORS = {

    # Main application
    "background": ("#F8EAD4", "#0F172A"),
    "toggle" : "#F8EAD4",
    # Cards / forms
    "card": ("#F7E7CE", "#1E293B"),
    "card_alt": ("#F7E7CE"),

    # Sidebar
    # "sidebar": "#172554",
    'sidebar': "#0B4008",
    "sidebar_hover": "#5E6F36",

    # Primary actions
    # "primary": "#637961",
    # 'primary': "#5E0606",
    'primary': "#0B4008",
    'primary_hover': "#5E6F36",
    # "primary_hover": "#9F3F3F",

    # Success
    "success": "#16A34A",
    "success_hover": "#15803D",

    # Warning
    "warning": "#D97706",
    "warning_hover": "#B45309",

    # Danger
    "danger": "#DC2626",
    "danger_hover": "#B91C1C",

    # Dispatch
    "dispatch": "#7C3AED",
    "dispatch_hover": "#6D28D9",

    # Text
    "text": ("#0F172A", "#F7E7CE"),
    "text_secondary": ("#7F872E", "#596300"),

    # Borders
    "border": ("#5E6F36", "#475569"),

    # Input fields
    "input": ("#F7E7CE", "#0F172A"),

    # Placeholder
    "placeholder": ("#7F872E", "#596300")
}

# ============================================================
# STANDARD SIZES
# ============================================================

SIZES = {

    # --------------------------------------------------------
    # Inputs
    # --------------------------------------------------------

    "entry_width": 380,
    "dropdown_width": 380,
    "sidebar_size": 20,
    "entry_height": 46,
    "button_height": 48,
    "button_width": 200,

    # --------------------------------------------------------
    # Containers
    # --------------------------------------------------------

    "corner_radius": 10,
    "large_corner_radius": 14,
    "small_corner_radius": 7,

    # --------------------------------------------------------
    # Fonts
    # --------------------------------------------------------

    "title_size": 30,
    "heading_size": 22,
    "label_size": 16,
    "normal_size": 15,
    "small_size": 13,

    # --------------------------------------------------------
    # Special controls
    # --------------------------------------------------------

    "textbox_width": 600,
    "textbox_height": 140,
}


# ============================================================
# STANDARD PADDING
# ============================================================

PADDING = {

    # Normal form spacing
    "x": 16,
    "y": 12,

    # Form container spacing
    "form_x": 20,
    "form_y": 12,

    # Section spacing
    "section_x": 25,
    "section_y": 20,
}
