"""
Gestion des Employés — Supervision par Triggers MySQL
Point d'entrée de l'application.
"""

from views.app import App


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()