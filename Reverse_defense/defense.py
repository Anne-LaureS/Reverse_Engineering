#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP17 - defenses cote serveur (fichier A COMPLETER).

Deux trous a remplir. Pas besoin de tout coder : on configure des defenses.
Etat initial (trous vides) = application VULNERABLE : l'API fait confiance a un
en-tete fourni par le client, et aucune politique de securite n'est envoyee.
Objectif = deplacer la decision cote serveur et ajouter les en-tetes.

Jeton connu du SERVEUR seulement (le client ne l'a pas) :
"""
SERVER_TOKEN = "srv_tok_7Q2a_9f"


def security_headers():
    """En-tetes de securite ajoutes a chaque reponse."""
    headers = {}
    # TODO(1): politique CSP qui n'autorise que les scripts du MEME origine
    #          (bloque le JS inline injecte). Laisser "" desactive la protection.
    #          Indice : "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
    #          NB : 'unsafe-inline' sur style-src laisse les <style> inline de la
    #          page s'afficher (sinon la page perd sa mise en forme) ; script-src
    #          reste STRICT (pas de 'unsafe-inline') -> le <script> inline est bien bloque.
    csp = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"  # <<< completez la politique CSP
    if csp:
        headers["Content-Security-Policy"] = csp
    headers["X-Content-Type-Options"] = "nosniff"
    return headers


def acces_autorise(request_headers):
    """
    Decide cote SERVEUR si l'export est autorise.

    VULNERABLE (etat initial) : on fait confiance a l'en-tete X-Role envoye par
    le client -> n'importe qui met 'admin' et passe.
    A DURCIR : exiger un jeton que seul le serveur connait, et NE PLUS se fier
    a X-Role.
    """
    # TODO(2): validation cote serveur. Autoriser uniquement si l'en-tete
    #          Authorization vaut exactement "Bearer " + SERVER_TOKEN.
    #          Puis SUPPRIMEZ le bloc "etat vulnerable" ci-dessus.
    auth = request_headers.get("Authorization", "")
    expected = "Bearer " + SERVER_TOKEN  # <<< construisez "Bearer " + SERVER_TOKEN
    if expected and auth == expected:
        return True

    return False
