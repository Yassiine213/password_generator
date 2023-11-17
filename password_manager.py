import os
import sqlite3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

class PasswordManager:
    """
    Gestionnaire de mots de passe sécurisé utilisant le chiffrement AES.

    Ce gestionnaire stocke les mots de passe de manière sécurisée dans une base de données SQLite.
    Les mots de passe sont chiffrés avec AES avant d'être stockés.

    Args:
        key (bytes): La clé AES utilisée pour le chiffrement.
        db_path (str): Le chemin de la base de données SQLite pour stocker les mots de passe.

    Considérations de sécurité:
        - La clé AES doit être gérée avec une sécurité maximale.
        - Les modes de chiffrement, la gestion des IV et le padding doivent être correctement gérés.
        - Un audit de sécurité est recommandé avant toute utilisation en production.
    """

    def __init__(self, key, db_path):
        """
        Initialise une instance de PasswordManager.
        """
        self.key = key
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """
        Initialise la base de données SQLite si elle n'existe pas encore.
        Crée la table 'accounts' si elle n'existe pas.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS accounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        site TEXT NOT NULL,
                        username TEXT NOT NULL,
                        password BLOB NOT NULL
                    );
                ''')
                conn.commit()
        except sqlite3.Error as e:
            # Log l'erreur (à implémenter)
            print(f"Erreur lors de l'initialisation de la base de données: {e}")

    def _pad(self, data):
        """
        Remplit les données avec un padding PKCS7.
        """
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data)
        padded_data += padder.finalize()
        return padded_data

    def _unpad(self, padded_data):
        """
        Supprime le padding PKCS7 des données.
        """
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data)
        data += unpadder.finalize()
        return data

    def _encrypt(self, data):
        """
        Chiffre les données avec AES en mode CBC.
        """
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(self._pad(data)) + encryptor.finalize()
        return iv + encrypted_data

    def _decrypt(self, encrypted_data):
        """
        Déchiffre les données chiffrées avec AES en mode CBC.
        """
        iv = encrypted_data[:16]
        encrypted_data = encrypted_data[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return self._unpad(decryptor.update(encrypted_data) + decryptor.finalize())

    def store_password(self, site, username, password):
        """
        Stocke un mot de passe chiffré dans la base de données.
        """
        try:
            encrypted_password = self._encrypt(password.encode('utf-8'))
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO accounts (site, username, password) VALUES (?, ?, ?)',
                               (site, username, encrypted_password))
                conn.commit()
        except sqlite3.Error as e:
            # Log l'erreur (à implémenter)
            print(f"Erreur lors de l'enregistrement du mot de passe: {e}")

    def check_password(self, site, username, password):
        """
        Vérifie si un mot de passe correspond à celui stocké dans la base de données.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT password FROM accounts WHERE site = ? AND username = ?',
                               (site, username))
                result = cursor.fetchone()
                if result:
                    stored_password = self._decrypt(result[0])
                    return stored_password.decode('utf-8') == password
                return False
        except sqlite3.Error as e:
            # Log l'erreur (à implémenter)
            print(f"Erreur lors de la vérification du mot de passe: {e}")
            return False
