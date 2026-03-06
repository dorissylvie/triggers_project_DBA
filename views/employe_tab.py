import tkinter as tk
from tkinter import ttk, messagebox

from models.employe import EmployeModel
from utils.styles import COLORS, FONTS, SIZES


class EmployeTab(tk.Frame):
    """Onglet de gestion des employés."""

    def __init__(self, parent, on_data_change=None):
        super().__init__(parent, bg=COLORS["bg"])
        self.on_data_change = on_data_change
        self._build_ui()
        self.refresh_table()

    # ── Construction de l'interface ──────────────────────────────

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=COLORS["bg"])
        header.pack(fill="x", padx=SIZES["padding"], pady=(SIZES["padding"], 0))

        tk.Label(
            header,
            text="Gestion des Employés",
            font=FONTS["title"],
            bg=COLORS["bg"],
            fg=COLORS["text_dark"],
        ).pack(side="left")

        # Toolbar
        toolbar = tk.Frame(self, bg=COLORS["bg"])
        toolbar.pack(fill="x", padx=SIZES["padding"], pady=SIZES["padding_sm"])

        # Recherche
        search_frame = tk.Frame(toolbar, bg=COLORS["card_bg"], highlightbackground=COLORS["border"],
                                highlightthickness=1)
        search_frame.pack(side="left")

        tk.Label(search_frame, text=" 🔍 ", bg=COLORS["card_bg"], font=FONTS["body"]).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._on_search())
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=FONTS["input"],
            bg=COLORS["card_bg"],
            fg=COLORS["text_dark"],
            relief="flat",
            width=25,
        )
        search_entry.pack(side="left", ipady=6, padx=(0, 8))

        # Boutons d'action
        btn_frame = tk.Frame(toolbar, bg=COLORS["bg"])
        btn_frame.pack(side="right")

        self._make_button(btn_frame, "＋  Ajouter", COLORS["success"], COLORS["success_hover"],
                          self._on_add).pack(side="left", padx=4)
        self._make_button(btn_frame, "✎  Modifier", COLORS["warning"], COLORS["warning_hover"],
                          self._on_edit).pack(side="left", padx=4)
        self._make_button(btn_frame, "✕  Supprimer", COLORS["danger"], COLORS["danger_hover"],
                          self._on_delete).pack(side="left", padx=4)
        self._make_button(btn_frame, "↻  Rafraîchir", COLORS["primary"], COLORS["primary_hover"],
                          self.refresh_table).pack(side="left", padx=4)

        # Card contenant le tableau
        card = tk.Frame(self, bg=COLORS["card_bg"], highlightbackground=COLORS["border"], highlightthickness=1)
        card.pack(fill="both", expand=True, padx=SIZES["padding"], pady=(0, SIZES["padding"]))

        # Treeview
        columns = ("matricule", "nom", "salaire")
        self.tree = ttk.Treeview(card, columns=columns, show="headings", style="Custom.Treeview")

        self.tree.heading("matricule", text="Matricule")
        self.tree.heading("nom", text="Nom de l'employé")
        self.tree.heading("salaire", text="Salaire (Ar)")

        self.tree.column("matricule", width=150, anchor="center")
        self.tree.column("nom", width=300, anchor="w")
        self.tree.column("salaire", width=200, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", lambda _: self._on_edit())

        # Barre de statut
        self.status_var = tk.StringVar(value="")
        tk.Label(
            self, textvariable=self.status_var, font=FONTS["small"],
            bg=COLORS["bg"], fg=COLORS["text_light"], anchor="w"
        ).pack(fill="x", padx=SIZES["padding"], pady=(0, 8))

    # ── Composant bouton réutilisable ────────────────────────────

    @staticmethod
    def _make_button(parent, text, bg_color, hover_color, command):
        btn = tk.Button(
            parent,
            text=text,
            font=FONTS["button"],
            bg=bg_color,
            fg=COLORS["text_white"],
            activebackground=hover_color,
            activeforeground=COLORS["text_white"],
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=6,
            command=command,
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
        return btn

    # ── Rafraîchissement du tableau ──────────────────────────────

    def refresh_table(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            rows = data if data is not None else EmployeModel.get_all()
            for i, row in enumerate(rows):
                tag = "even" if i % 2 == 0 else "odd"
                self.tree.insert(
                    "", "end",
                    values=(row["matricule"], row["nom"], f"{row['salaire']:,.0f} Ar".replace(",", " ")),
                    tags=(tag,),
                )
            self.tree.tag_configure("odd", background=COLORS["table_row_alt"])
            self.status_var.set(f"{len(rows)} employé(s) trouvé(s)")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger les données :\n{e}")

    # ── Recherche ────────────────────────────────────────────────

    def _on_search(self):
        keyword = self.search_var.get().strip()
        try:
            if keyword:
                rows = EmployeModel.search(keyword)
            else:
                rows = EmployeModel.get_all()
            self.refresh_table(data=rows)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    # ── Formulaire (Ajout / Modification) ────────────────────────

    def _open_form(self, mode="ajout", values=None):
        form = tk.Toplevel(self)
        form.title("Ajouter un employé" if mode == "ajout" else "Modifier un employé")
        form.geometry("500x420")
        form.resizable(False, False)
        form.configure(bg=COLORS["bg"])
        form.grab_set()
        form.focus_set()

        # Centrer la fenêtre
        form.update_idletasks()
        x = (form.winfo_screenwidth() - 500) // 2
        y = (form.winfo_screenheight() - 420) // 2
        form.geometry(f"+{x}+{y}")

        # Titre
        title_text = "Nouvel employé" if mode == "ajout" else "Modifier employé"
        tk.Label(form, text=title_text, font=FONTS["subtitle"], bg=COLORS["bg"],
                 fg=COLORS["text_dark"]).pack(pady=(20, 15))

        # Champs
        fields_frame = tk.Frame(form, bg=COLORS["bg"])
        fields_frame.pack(padx=40, fill="x")

        entries = {}
        for label_text, key in [("Matricule", "matricule"), ("Nom", "nom"), ("Salaire", "salaire")]:
            tk.Label(fields_frame, text=label_text, font=FONTS["body_bold"],
                     bg=COLORS["bg"], fg=COLORS["text_dark"], anchor="w").pack(fill="x", pady=(8, 2))
            entry = tk.Entry(
                fields_frame, font=FONTS["input"], bg=COLORS["input_bg"],
                fg=COLORS["text_dark"], relief="solid",
                highlightbackground=COLORS["input_border"], highlightthickness=1,
            )
            entry.pack(fill="x", ipady=8)
            entries[key] = entry

        # Pré-remplissage en mode modification
        if mode == "modification" and values:
            entries["matricule"].insert(0, values[0])
            entries["matricule"].config(state="disabled")
            entries["nom"].insert(0, values[1])
            salaire_str = str(values[2]).replace(",", "").replace(" ", "").replace("Ar", "").strip()
            entries["salaire"].insert(0, salaire_str)

        # Boutons
        btn_row = tk.Frame(form, bg=COLORS["bg"])
        btn_row.pack(pady=25)

        def valider():
            matricule = entries["matricule"].get().strip()
            nom = entries["nom"].get().strip()
            salaire_str = entries["salaire"].get().strip()

            if not matricule or not nom or not salaire_str:
                messagebox.showwarning("Champs manquants", "Tous les champs sont obligatoires.", parent=form)
                return
            try:
                salaire = float(salaire_str)
            except ValueError:
                messagebox.showerror("Erreur", "Le salaire doit être un nombre.", parent=form)
                return

            try:
                if mode == "ajout":
                    EmployeModel.insert(matricule, nom, salaire)
                    messagebox.showinfo("Succès", "Employé ajouté avec succès.", parent=form)
                else:
                    EmployeModel.update(matricule, nom, salaire)
                    messagebox.showinfo("Succès", "Employé modifié avec succès.", parent=form)
                form.destroy()
                self.refresh_table()
                if self.on_data_change:
                    self.on_data_change()
            except Exception as e:
                messagebox.showerror("Erreur", str(e), parent=form)

        self._make_button(btn_row, "  Enregistrer  ", COLORS["success"], COLORS["success_hover"],
                          valider).pack(side="left", padx=12, ipady=4)
        self._make_button(btn_row, "    Annuler    ", COLORS["text_light"], COLORS["border"],
                          form.destroy).pack(side="left", padx=12, ipady=4)

    # ── Actions ──────────────────────────────────────────────────

    def _on_add(self):
        self._open_form("ajout")

    def _on_edit(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Sélectionnez un employé à modifier.")
            return
        values = self.tree.item(selected[0])["values"]
        self._open_form("modification", values)

    def _on_delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Sélectionnez un employé à supprimer.")
            return
        values = self.tree.item(selected[0])["values"]
        confirm = messagebox.askyesno(
            "Confirmation",
            f"Supprimer l'employé {values[1]} (matricule: {values[0]}) ?",
        )
        if confirm:
            try:
                EmployeModel.delete(str(values[0]))
                self.refresh_table()
                messagebox.showinfo("Succès", "Employé supprimé.")
                if self.on_data_change:
                    self.on_data_change()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
