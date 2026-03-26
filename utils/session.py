"""
Session globale de l'application.
Stocke les informations de l'utilisateur connecté.
"""

_session = {
    "current_user": None,
    "username": None,
    "role": None,
}


def set_current_user(user_dict):
    """Définit l'utilisateur connecté."""
    global _session
    _session["current_user"] = user_dict
    _session["username"] = user_dict.get("username")
    _session["role"] = user_dict.get("role")


def get_current_user():
    """Retourne l'utilisateur actuellement connecté."""
    return _session["current_user"]


def get_current_username():
    """Retourne le username de l'utilisateur connecté."""
    return _session["username"]


def get_current_role():
    """Retourne le rôle de l'utilisateur connecté."""
    return _session["role"]


def clear_session():
    """Efface la session (déconnexion)."""
    global _session
    _session = {"current_user": None, "username": None, "role": None}
