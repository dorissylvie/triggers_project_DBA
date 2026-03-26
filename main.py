"""
Gestion des Employés — Supervision par Triggers MySQL
Point d'entrée de l'application.
"""

from views.app import App
from views.login_window import LoginWindow


def main():
    login = LoginWindow()
    login.mainloop()

    if not login.authenticated_user:
        return

    app = App(current_user=login.authenticated_user)
    app.mainloop()


if __name__ == "__main__":
    main()