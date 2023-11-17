import tkinter as tk
from tkinter import messagebox
from password_manager import PasswordManager
import os
import string
import random

# Configuration et style de l'interface graphique
root = tk.Tk()
root.title("Gestionnaire de Mots de Passe")
root.geometry("400x300")
root.resizable(width=False, height=False)

# Générer une clé AES256 pour le gestionnaire de mots de passe
key = os.urandom(32)
pm = PasswordManager(key, "passwords.db")

# Fonctions de l'application
def validate_input(site, username, password):
    """ Vérifie que les entrées ne sont pas vides. """
    return bool(site and username and password)

def display_message(message, error=False):
    """ Affiche un message de statut sur l'interface. """
    status_label.config(text=message, fg="red" if error else "green")

def store_password():
    """ Stocke le mot de passe après validation. """
    site, username, password = site_entry.get(), username_entry.get(), password_entry.get()
    if not validate_input(site, username, password):
        display_message("Veuillez remplir tous les champs.", True)
        return

    pm.store_password(site, username, password)
    display_message("Mot de passe enregistré avec succès.")

def check_password():
    """ Vérifie si le mot de passe est correct. """
    site, username, password = site_entry.get(), username_entry.get(), password_entry.get()
    if not validate_input(site, username, password):
        display_message("Veuillez remplir tous les champs.", True)
        return

    if pm.check_password(site, username, password):
        display_message("Mot de passe correct.")
    else:
        display_message("Mot de passe incorrect.", True)

def generate_random_password():
    """ Génère un mot de passe aléatoire. """
    password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(12))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# Interface graphique
site_entry = tk.Entry(root)
username_entry = tk.Entry(root)
password_entry = tk.Entry(root, show="*")
status_label = tk.Label(root, text="", fg="green")

site_entry.pack(pady=5)
username_entry.pack(pady=5)
password_entry.pack(pady=5)

tk.Button(root, text="Stocker le mot de passe", command=store_password).pack(pady=5)
tk.Button(root, text="Vérifier le mot de passe", command=check_password).pack(pady=5)
tk.Button(root, text="Générer un mot de passe aléatoire", command=generate_random_password).pack(pady=5)

status_label.pack(pady=5)

root.mainloop()
