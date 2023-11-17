import tkinter as tk
from tkinter import messagebox, ttk
from password_manager import PasswordManager
import os

# Configuration et style
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12))

# Générer une clé AES256
key = os.urandom(32)  # Cette clé doit être conservée de manière sécurisée
pm = PasswordManager(key)

# Fonctions
def store_password():
    site = site_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    pm.store_password(site, username, password)
    status_label.config(text="Mot de passe enregistré avec succès.", fg="green")

def check_password():
    site = site_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    if pm.check_password(site, username, password):
        status_label.config(text="Le mot de passe est correct.", fg="green")
    else:
        status_label.config(text="Mot de passe incorrect.", fg="red")

def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

# Interface graphique
root = tk.Tk()
root.title("Gestionnaire de Mots de Passe")

# Activer le plein écran
root.attributes("-fullscreen", True)
# Permettre de basculer en mode fenêtré en appuyant sur la touche 'F11'
root.bind("<F11>", toggle_fullscreen)

main_frame = ttk.Frame(root, padding="30")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Widgets
site_label = ttk.Label(main_frame, text="Site/Application :")
site_label.grid(row=0, column=0, sticky=tk.W, pady=5)

site_entry = ttk.Entry(main_frame)
site_entry.grid(row=0, column=1, pady=5, sticky=(tk.W, tk.E))

username_label = ttk.Label(main_frame, text="Nom d'Utilisateur :")
username_label.grid(row=1, column=0, sticky=tk.W, pady=5)

username_entry = ttk.Entry(main_frame)
username_entry.grid(row=1, column=1, pady=5, sticky=(tk.W, tk.E))

password_label = ttk.Label(main_frame, text="Mot de Passe :")
password_label.grid(row=2, column=0, sticky=tk.W, pady=5)

password_entry = ttk.Entry(main_frame, show="*")
password_entry.grid(row=2, column=1, pady=5, sticky=(tk.W, tk.E))

store_button = ttk.Button(main_frame, text="Stocker le mot de passe", command=store_password)
store_button.grid(row=3, column=0, pady=10, sticky=tk.W)

check_button = ttk.Button(main_frame, text="Vérifier le mot de passe", command=check_password)
check_button.grid(row=3, column=1, pady=10, sticky=tk.W)

status_label = ttk.Label(main_frame, text="", font=("Arial", 10))
status_label.grid(row=4, column=0, columnspan=2, pady=5)

# Configuration de la disposition
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)

root.mainloop()
