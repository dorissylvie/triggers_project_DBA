import tkinter as tk
from tkinter import ttk, messagebox

from models.audit import AuditModel
from utils.styles import COLORS, FONTS, SIZES


class AuditTab(tk.Frame):
    """Onglet de supervision / audit des opérations."""

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg"])
        self._build_ui()
        self.refresh()

    # ── Construction de l'interface ──────────────────────────────

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=COLORS["bg"])
        header.pack(fill="x", padx=SIZES["padding"], pady=(SIZES["padding"], 0))

        tk.Label(
            header,
            text="Supervision & Audit",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text_dark"],
        ).pack(side="left")

        # Cartes statistiques
        self.stats_frame = tk.Frame(self, bg=COLORS["bg"])
        self.stats_frame.pack(fill="x", padx=SIZES["padding"], pady=SIZES["padding_sm"])

        self.stat_cards = {}
        stats_config = [
            ("ajouts", "Insertions", COLORS["stat_ajout"], "nb_ajouts"),
            ("modifications", "Modifications", COLORS["stat_modif"], "nb_modifications"),
            ("suppressions", "Suppressions", COLORS["stat_suppr"], "nb_suppressions"),
            ("total", "Total opérations", COLORS["primary"], "total"),
        ]
        for key, label, color, _ in stats_config:
            card = self._create_stat_card(self.stats_frame, label, "0", color)
            card.pack(side="left", expand=True, fill="x", padx=6)
            self.stat_cards[key] = card

        # Toolbar filtre
        filter_frame = tk.Frame(self, bg=COLORS["bg"])
        filter_frame.pack(fill="x", padx=SIZES["padding"], pady=(0, SIZES["padding_sm"]))

        tk.Label(filter_frame, text="Filtrer par :", font=FONTS["body_bold"],
                 bg=COLORS["bg"], fg=COLORS["text_dark"]).pack(side="left", padx=(0, 8))

        self.filter_var = tk.StringVar(value="TOUT")
        for text, val in [("Tout", "TOUT"), ("Ajouts", "AJOUT"), ("Modifications", "MODIFICATION"),
                          ("Suppressions", "SUPPRESSION")]:
            rb = tk.Radiobutton(
                filter_frame, text=text, variable=self.filter_var, value=val,
                font=FONTS["body"], bg=COLORS["bg"], fg=COLORS["text_dark"],
                activebackground=COLORS["bg"], selectcolor=COLORS["bg"],
                cursor="hand2", command=self._on_filter_change,
            )
            rb.pack(side="left", padx=6)

        # Bouton rafraîchir
        refresh_btn = tk.Button(
            filter_frame, text="↻  Rafraîchir", font=FONTS["button"],
            bg=COLORS["primary"], fg=COLORS["text_white"],
            activebackground=COLORS["primary_hover"], activeforeground=COLORS["text_white"],
            relief="flat", cursor="hand2", padx=16, pady=4, command=self.refresh,
        )
        refresh_btn.pack(side="right")
        refresh_btn.bind("<Enter>", lambda e: refresh_btn.config(bg=COLORS["primary_hover"]))
        refresh_btn.bind("<Leave>", lambda e: refresh_btn.config(bg=COLORS["primary"]))

        # Card contenant le tableau
        card = tk.Frame(self, bg=COLORS["card_bg"], highlightbackground=COLORS["border"], highlightthickness=1)
        card.pack(fill="both", expand=True, padx=SIZES["padding"], pady=(0, SIZES["padding"]))

        # Treeview audit
        columns = ("id", "type_action", "date", "matricule", "nom", "ancien", "nouveau", "utilisateur")
        self.tree = ttk.Treeview(card, columns=columns, show="headings", style="Custom.Treeview")

        headings = [
            ("id", "ID", 50),
            ("type_action", "Action", 120),
            ("date", "Date", 160),
            ("matricule", "Matricule", 100),
            ("nom", "Nom", 180),
            ("ancien", "Ancien salaire", 140),
            ("nouveau", "Nouveau salaire", 140),
            ("utilisateur", "Utilisateur", 120),
        ]
        for col, text, width in headings:
            self.tree.heading(col, text=text)
            anchor = "w" if col == "nom" else "center"
            self.tree.column(col, width=width, anchor=anchor, minwidth=60)

        scrollbar_y = ttk.Scrollbar(card, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(card, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        card.grid_rowconfigure(0, weight=1)
        card.grid_columnconfigure(0, weight=1)

        # Barre de résumé en bas
        self.summary_var = tk.StringVar(value="")
        tk.Label(
            self, textvariable=self.summary_var, font=FONTS["body_bold"],
            bg=COLORS["bg"], fg=COLORS["text_dark"], anchor="w",
        ).pack(fill="x", padx=SIZES["padding"], pady=(0, 8))

    # ── Carte statistique ────────────────────────────────────────

    @staticmethod
    def _create_stat_card(parent, label, value, color):
        card = tk.Frame(parent, bg=COLORS["card_bg"], highlightbackground=color, highlightthickness=2)

        # Barre de couleur en haut
        tk.Frame(card, bg=color, height=4).pack(fill="x")

        value_label = tk.Label(card, text=value, font=FONTS["stat_number"],
                               bg=COLORS["card_bg"], fg=color)
        value_label.pack(pady=(12, 2))

        tk.Label(card, text=label, font=FONTS["stat_label"],
                 bg=COLORS["card_bg"], fg=COLORS["text_light"]).pack(pady=(0, 12))

        card.value_label = value_label
        return card

    # ── Rafraîchissement ─────────────────────────────────────────

    def refresh(self):
        self._load_stats()
        self._load_table()

    def _load_stats(self):
        try:
            stats = AuditModel.get_stats()
            mapping = {
                "ajouts": "nb_ajouts",
                "modifications": "nb_modifications",
                "suppressions": "nb_suppressions",
                "total": "total",
            }
            for key, db_key in mapping.items():
                val = stats.get(db_key, 0) or 0
                self.stat_cards[key].value_label.config(text=str(val))
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les statistiques :\n{e}")

    def _load_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            filter_val = self.filter_var.get()
            if filter_val == "TOUT":
                rows = AuditModel.get_all()
            else:
                rows = AuditModel.filter_by_action(filter_val)

            for i, row in enumerate(rows):
                ancien = f"{row['salaire_ancien']:,.0f} Ar".replace(",", " ") if row["salaire_ancien"] is not None else "—"
                nouveau = f"{row['salaire_nouv']:,.0f} Ar".replace(",", " ") if row["salaire_nouv"] is not None else "—"
                date_str = row["date_mise_a_jour"].strftime("%d/%m/%Y %H:%M:%S") if row["date_mise_a_jour"] else ""
                tag = "even" if i % 2 == 0 else "odd"
                self.tree.insert(
                    "", "end",
                    values=(
                        row["id"], row["type_action"], date_str,
                        row["matricule"], row["nom"] or "",
                        ancien, nouveau,
                        row["utilisateur"] or "",
                    ),
                    tags=(tag,),
                )
            self.tree.tag_configure("odd", background=COLORS["table_row_alt"])

            self.summary_var.set(
                f"{len(rows)} enregistrement(s) affiché(s)"
            )
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger l'audit :\n{e}")

    def _on_filter_change(self):
        self._load_table()
