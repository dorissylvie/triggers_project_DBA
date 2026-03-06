import tkinter as tk
from tkinter import ttk, messagebox

from config.database import test_connection
from utils.styles import COLORS, FONTS, SIZES, configure_treeview_style
from views.employe_tab import EmployeTab
from views.audit_tab import AuditTab


class App(tk.Tk):
    """Fenêtre principale avec sidebar de navigation."""

    def __init__(self):
        super().__init__()
        self.title("Gestion des Employés — Supervision par Triggers")
        self.geometry("1200x700")
        self.minsize(900, 550)
        self.configure(bg=COLORS["bg"])

        # Centrer la fenêtre
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 1200) // 2
        y = (self.winfo_screenheight() - 700) // 2
        self.geometry(f"+{x}+{y}")

        # Style global
        self.style = ttk.Style(self)
        configure_treeview_style(self.style)

        # Tester la connexion DB
        if not test_connection():
            messagebox.showerror(
                "Erreur de connexion",
                "Impossible de se connecter à MySQL.\n\n"
                "Vérifiez que :\n"
                "• Le serveur MySQL est démarré\n"
                "• La base 'gestion_employes' existe\n"
                "• Les paramètres dans config/database.py sont corrects\n\n"
                "Exécutez le script sql/schema.sql pour créer la base.",
            )

        self._build_ui()

    def _build_ui(self):
        # ── Sidebar ──────────────────────────────────────────────
        sidebar = tk.Frame(self, bg=COLORS["sidebar"], width=SIZES["sidebar_width"])
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo / titre dans la sidebar
        logo_frame = tk.Frame(sidebar, bg=COLORS["sidebar"])
        logo_frame.pack(fill="x", pady=(25, 30))

        tk.Label(
            logo_frame, text="📊", font=("Segoe UI", 28),
            bg=COLORS["sidebar"], fg=COLORS["text_white"],
        ).pack()
        tk.Label(
            logo_frame, text="GestEmployés", font=("Segoe UI", 15, "bold"),
            bg=COLORS["sidebar"], fg=COLORS["text_white"],
        ).pack()
        tk.Label(
            logo_frame, text="Système d'audit", font=FONTS["small"],
            bg=COLORS["sidebar"], fg="#95A5A6",
        ).pack()

        # Boutons de navigation
        self.nav_buttons = {}
        self.current_tab = None

        nav_items = [
            ("employes", "👥  Employés"),
            ("audit", "📋  Supervision"),
        ]
        for key, text in nav_items:
            btn = tk.Button(
                sidebar, text=text, font=FONTS["sidebar"],
                bg=COLORS["sidebar"], fg=COLORS["text_white"],
                activebackground=COLORS["sidebar_active"],
                activeforeground=COLORS["text_white"],
                relief="flat", anchor="w", padx=20, pady=12,
                cursor="hand2",
                command=lambda k=key: self._switch_tab(k),
            )
            btn.pack(fill="x", padx=8, pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS["sidebar_active"]) if b != self._active_btn() else None)
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS["sidebar"]) if b != self._active_btn() else None)
            self.nav_buttons[key] = btn

        # ── Zone de contenu ──────────────────────────────────────
        self.content = tk.Frame(self, bg=COLORS["bg"])
        self.content.pack(side="left", fill="both", expand=True)

        # Créer les onglets
        self.tabs = {}
        self.tabs["audit"] = AuditTab(self.content)
        self.tabs["employes"] = EmployeTab(self.content, on_data_change=self._on_employee_data_change)

        # Afficher l'onglet par défaut
        self._switch_tab("employes")

    def _active_btn(self):
        if self.current_tab and self.current_tab in self.nav_buttons:
            return self.nav_buttons[self.current_tab]
        return None

    def _switch_tab(self, tab_key):
        if self.current_tab == tab_key:
            return

        # Masquer l'onglet actuel
        for tab in self.tabs.values():
            tab.pack_forget()

        # Afficher le nouveau
        self.tabs[tab_key].pack(fill="both", expand=True)

        # Rafraîchir si c'est l'audit
        if tab_key == "audit":
            self.tabs["audit"].refresh()

        # Mise à jour visuelle de la sidebar
        for key, btn in self.nav_buttons.items():
            if key == tab_key:
                btn.config(bg=COLORS["sidebar_active"], font=FONTS["sidebar_active"])
            else:
                btn.config(bg=COLORS["sidebar"], font=FONTS["sidebar"])

        self.current_tab = tab_key

    def _on_employee_data_change(self):
        """Appelé quand les données employés changent (ajout/modif/suppression)."""
        if "audit" in self.tabs:
            self.tabs["audit"].refresh()
