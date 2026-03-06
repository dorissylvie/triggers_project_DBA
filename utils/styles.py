"""Styles et thème de l'application."""

# Palette de couleurs
COLORS = {
    "bg": "#F5F7FA",
    "sidebar": "#2C3E50",
    "sidebar_active": "#34495E",
    "primary": "#3498DB",
    "primary_hover": "#2980B9",
    "success": "#27AE60",
    "success_hover": "#219A52",
    "warning": "#F39C12",
    "warning_hover": "#D68910",
    "danger": "#E74C3C",
    "danger_hover": "#C0392B",
    "text_dark": "#2C3E50",
    "text_light": "#7F8C8D",
    "text_white": "#FFFFFF",
    "card_bg": "#FFFFFF",
    "border": "#DCE1E8",
    "input_bg": "#FFFFFF",
    "input_border": "#BDC3C7",
    "table_header": "#ECF0F1",
    "table_row_alt": "#F8F9FA",
    "table_selected": "#D4E6F1",
    "stat_ajout": "#27AE60",
    "stat_modif": "#F39C12",
    "stat_suppr": "#E74C3C",
}

# Polices
FONTS = {
    "title": ("Segoe UI", 20, "bold"),
    "subtitle": ("Segoe UI", 14, "bold"),
    "heading": ("Segoe UI", 12, "bold"),
    "body": ("Segoe UI", 11),
    "body_bold": ("Segoe UI", 11, "bold"),
    "small": ("Segoe UI", 9),
    "button": ("Segoe UI", 10, "bold"),
    "stat_number": ("Segoe UI", 28, "bold"),
    "stat_label": ("Segoe UI", 10),
    "sidebar": ("Segoe UI", 12),
    "sidebar_active": ("Segoe UI", 12, "bold"),
    "input": ("Segoe UI", 11),
}

# Dimensions
SIZES = {
    "sidebar_width": 220,
    "padding": 20,
    "padding_sm": 10,
    "padding_xs": 5,
    "border_radius": 8,
    "button_padx": 20,
    "button_pady": 8,
    "entry_padx": 10,
    "entry_pady": 8,
}


def configure_treeview_style(style):
    """Configure le style ttk.Treeview pour un look moderne."""
    style.theme_use("clam")

    style.configure(
        "Custom.Treeview",
        background=COLORS["card_bg"],
        foreground=COLORS["text_dark"],
        rowheight=36,
        fieldbackground=COLORS["card_bg"],
        font=FONTS["body"],
        borderwidth=0,
    )
    style.configure(
        "Custom.Treeview.Heading",
        background=COLORS["table_header"],
        foreground=COLORS["text_dark"],
        font=FONTS["heading"],
        borderwidth=0,
        relief="flat",
        padding=(10, 8),
    )
    style.map(
        "Custom.Treeview",
        background=[("selected", COLORS["table_selected"])],
        foreground=[("selected", COLORS["text_dark"])],
    )
    style.map(
        "Custom.Treeview.Heading",
        background=[("active", COLORS["border"])],
    )

    # Style pour les boutons
    style.configure(
        "Primary.TButton",
        background=COLORS["primary"],
        foreground=COLORS["text_white"],
        font=FONTS["button"],
        padding=(SIZES["button_padx"], SIZES["button_pady"]),
        borderwidth=0,
    )
    style.map(
        "Primary.TButton",
        background=[("active", COLORS["primary_hover"])],
    )
