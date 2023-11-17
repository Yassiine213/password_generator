'''
Ce qui change dans ce code :

Les mots de passe sont directement chiffrés avec AES, au lieu d'être d'abord hachés.
La méthode hash_password a été retirée, car elle n'est plus nécessaire.
La méthode store_password chiffre désormais directement le mot de passe en texte clair.
La méthode check_password compare le mot de passe déchiffré avec celui fourni.

Considérations de Sécurité
Stockage de la Clé AES: La clé AES doit toujours être gérée avec une sécurité maximale. Sa divulgation compromettrait la sécurité de tous les mots de passe stockés.
Sécurité de l'Implémentation de Chiffrement: Bien que le chiffrement AES soit robuste, son implémentation correcte est cruciale. Assurez-vous que les modes de chiffrement, la gestion des IV (vecteurs d'initialisation), et le padding sont correctement gérés.
Utilisation en Production: Comme pour toute application de gestion de mots de passe, une révision et un audit de sécurité par des experts sont recommandés avant toute utilisation en production, surtout si vous prévoyez de gérer des informations sensibles.

'''

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

class PasswordManager:
    def __init__(self, key):
        self.passwords = {}  # Stocke les mots de passe chiffrés
        self.key = key  # Clé AES256

    def _pad(self, data):
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data)
        padded_data += padder.finalize()
        return padded_data

    def _unpad(self, padded_data):
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data)
        data += unpadder.finalize()
        return data

    def _encrypt(self, data):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(self._pad(data)) + encryptor.finalize()
        return iv + encrypted_data

    def _decrypt(self, encrypted_data):
        iv = encrypted_data[:16]
        encrypted_data = encrypted_data[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        return self._unpad(decryptor.update(encrypted_data) + decryptor.finalize())

    def store_password(self, site, username, password):
        data = f"{username}:{password}"
        encrypted_data = self._encrypt(data.encode('utf-8'))
        self.passwords[site] = encrypted_data

    def check_password(self, site, username, password):
        if site in self.passwords:
            encrypted_data = self.passwords[site]
            decrypted_data = self._decrypt(encrypted_data).decode('utf-8')
            stored_username, stored_password = decrypted_data.split(':')
            return stored_username == username and stored_password == password
        return False
