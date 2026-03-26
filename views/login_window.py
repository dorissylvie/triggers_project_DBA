import tkinter as tk
from tkinter import messagebox

from models.utilisateur import UtilisateurModel
from utils.styles import COLORS, FONTS


class LoginWindow(tk.Tk):
    """Fenêtre de connexion avant ouverture de l'application."""

    def __init__(self):
        super().__init__()
        self.title("Connexion")
        self.geometry("460x340")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg"])
        self.authenticated_user = None

        self.update_idletasks()
        x = (self.winfo_screenwidth() - 460) // 2
        y = (self.winfo_screenheight() - 340) // 2
        self.geometry(f"+{x}+{y}")

        self._build_ui()

    def _build_ui(self):
        card = tk.Frame(self, bg=COLORS["card_bg"], highlightbackground=COLORS["border"], highlightthickness=1)
        card.pack(fill="both", expand=True, padx=24, pady=24)

        tk.Label(
            card,
            text="Authentification",
            font=FONTS["title"],
            bg=COLORS["card_bg"],
            fg=COLORS["text_dark"],
        ).pack(pady=(20, 6))

        tk.Label(
            card,
            text="Connectez-vous selon votre rôle",
            font=FONTS["body"],
            bg=COLORS["card_bg"],
            fg=COLORS["text_light"],
        ).pack(pady=(0, 16))

        form = tk.Frame(card, bg=COLORS["card_bg"])
        form.pack(fill="x", padx=40)

        tk.Label(form, text="Username", font=FONTS["body_bold"], bg=COLORS["card_bg"], fg=COLORS["text_dark"], anchor="w").pack(fill="x", pady=(6, 2))
        self.username_entry = tk.Entry(form, font=FONTS["input"], relief="solid", highlightbackground=COLORS["input_border"], highlightthickness=1)
        self.username_entry.pack(fill="x", ipady=8)

        tk.Label(form, text="Mot de passe", font=FONTS["body_bold"], bg=COLORS["card_bg"], fg=COLORS["text_dark"], anchor="w").pack(fill="x", pady=(10, 2))
        self.password_entry = tk.Entry(form, show="*", font=FONTS["input"], relief="solid", highlightbackground=COLORS["input_border"], highlightthickness=1)
        self.password_entry.pack(fill="x", ipady=8)

        btn = tk.Button(
            card,
            text="Se connecter",
            font=FONTS["button"],
            bg=COLORS["primary"],
            fg=COLORS["text_white"],
            activebackground=COLORS["primary_hover"],
            activeforeground=COLORS["text_white"],
            relief="flat",
            cursor="hand2",
            padx=28,
            pady=8,
            command=self._login,
        )
        btn.pack(pady=(22, 12))

        hint = (
            "Comptes par défaut:\n"
            "- user1 / user123 (UTILISATEUR)\n"
            "- super1 / super123 (SUPERVISEUR)"
        )
        tk.Label(card, text=hint, font=FONTS["small"], bg=COLORS["card_bg"], fg=COLORS["text_light"], justify="left").pack(pady=(0, 16))

        self.bind("<Return>", lambda _: self._login())
        self.username_entry.focus_set()

    def _login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Champs manquants", "Renseignez username et mot de passe.", parent=self)
            return

        try:
            user = UtilisateurModel.authenticate(username, password)
            if not user:
                messagebox.showerror("Connexion refusée", "Identifiants invalides.", parent=self)
                return
            self.authenticated_user = user
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de vérifier le compte:\n{e}", parent=self)
