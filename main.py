import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("Gestion des employés")
root.geometry("1000x600")

# ===============================
# FONCTIONS
# ===============================

def ouvrir_formulaire(mode="ajout"):
    form = tk.Toplevel(root)
    form.title("Formulaire Employé")
    form.geometry("400x300")
    form.grab_set()  # bloque fenêtre principale

    tk.Label(form, text="Matricule").pack(pady=5)
    entry_matricule = tk.Entry(form)
    entry_matricule.pack()

    tk.Label(form, text="Nom").pack(pady=5)
    entry_nom = tk.Entry(form)
    entry_nom.pack()

    tk.Label(form, text="Salaire").pack(pady=5)
    entry_salaire = tk.Entry(form)
    entry_salaire.pack()

    # Mode modification → pré-remplir
    if mode == "modification":
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Sélectionnez un employé")
            form.destroy()
            return

        values = tree.item(selected)["values"]
        entry_matricule.insert(0, values[0])
        entry_nom.insert(0, values[1])
        entry_salaire.insert(0, values[2])

    def valider():
        matricule = entry_matricule.get()
        nom = entry_nom.get()
        salaire = entry_salaire.get()

        if not matricule or not nom or not salaire:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires")
            return

        if mode == "ajout":
            tree.insert("", "end", values=(matricule, nom, salaire))
            messagebox.showinfo("Succès", "Employé ajouté avec succès")

        else:
            selected = tree.selection()
            tree.item(selected, values=(matricule, nom, salaire))
            messagebox.showinfo("Succès", "Employé modifié avec succès")

        form.destroy()

    tk.Button(
        form,
        text="Enregistrer",
        bg="#4CAF50",
        fg="white",
        command=valider
    ).pack(pady=15)


def supprimer_employe():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Attention", "Sélectionnez un employé")
        return

    confirm = messagebox.askyesno(
        "Confirmation",
        "Voulez-vous vraiment supprimer cet employé ?"
    )

    if confirm:
        tree.delete(selected)
        messagebox.showinfo("Succès", "Employé supprimé")


# ===============================
# BOUTON AJOUTER EN HAUT
# ===============================

top_frame = tk.Frame(root)
top_frame.pack(fill="x", padx=20, pady=10)

tk.Button(
    top_frame,
    text="➕ Ajouter Employé",
    bg="#2196F3",
    fg="white",
    command=lambda: ouvrir_formulaire("ajout")
).pack(side="right")

# ===============================
# TITRE
# ===============================

tk.Label(
    root,
    text="Liste des Employés",
    font=("Arial", 18, "bold")
).pack(pady=10)

# ===============================
# TABLEAU
# ===============================

frame_table = tk.Frame(root)
frame_table.pack(fill="both", expand=True, padx=20)

tree = ttk.Treeview(
    frame_table,
    columns=("Matricule", "Nom", "Salaire"),
    show="headings"
)

tree.heading("Matricule", text="Matricule")
tree.heading("Nom", text="Nom")
tree.heading("Salaire", text="Salaire")

tree.column("Matricule", width=150, anchor="center")
tree.column("Nom", width=250, anchor="center")
tree.column("Salaire", width=150, anchor="center")

tree.pack(fill="both", expand=True)

# ===============================
# BOUTONS MODIFIER / SUPPRIMER
# ===============================

bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

tk.Button(
    bottom_frame,
    text="✏ Modifier",
    bg="#FFC107",
    command=lambda: ouvrir_formulaire("modification")
).pack(side="left", padx=10)

tk.Button(
    bottom_frame,
    text="🗑 Supprimer",
    bg="#F44336",
    fg="white",
    command=supprimer_employe
).pack(side="left", padx=10)

# ===============================
# DONNÉE EXEMPLE
# ===============================

tree.insert("", "end", values=("1001", "Rakoto Jean", "500000"))
tree.insert("", "end", values=("1002", "Rasoana Marie", "650000"))

root.mainloop()