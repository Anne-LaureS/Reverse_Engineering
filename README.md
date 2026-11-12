# 🧩 Reverse Engineering

![Python](https://img.shields.io/badge/Python-3670A0?logo=python&logoColor=white)
![C](https://img.shields.io/badge/C-00599C?logo=c&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)
![Windows](https://img.shields.io/badge/Windows-0078D6?logo=windows&logoColor=white)
![Ghidra](<https://img.shields.io/badge/Ghidra-reverse%20engineering-CC3333>)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)
![WebAssembly](https://img.shields.io/badge/WebAssembly-654FF0?logo=webassembly&logoColor=white)
[![Licence MIT](https://img.shields.io/badge/licence-MIT-green)](LICENSE)

## 📌 Description

Travaux pratiques du module **Reverse Engineering**

14 TP répartis sur trois terrains : binaires natifs Linux (statique), applications web côté client (JS/WASM/HTTP), et analyse mémoire/débogage live sur une VM Windows isolée.

## 🎯 Objectifs

- ✅ Désassembler et décompiler des binaires (ELF et PE, Ghidra/GDB/binutils)
- ✅ Contourner des contrôles d'accès posés côté client (jamais une vraie protection)
- ✅ Désobfusquer du JavaScript et lire du WebAssembly
- ✅ Lire et **modifier** la mémoire d'un processus vivant (Cheat Engine, x64dbg)
- ✅ Retrouver un secret dans un dump mémoire
- ✅ Exploiter un débordement de tampon pour détourner l'exécution (ret2win)

## 📁 Structure du dépôt

```text
Reverse_Engineering/
├── Reverse_natif/              # Binaires ELF Linux — Ghidra, GDB, binutils
│   ├── login_rapport/          # login_O0 : désactivation/contournement, -O0 vs -O2
│   ├── suspicious_rapport/     # Analyse d'un binaire au comportement suspect
│   ├── xor_stripped_rapport/   # Binaire strippé : mot de passe XOR, binutils puis Ghidra
│   └── exo2_rapport/           # ELF 64 bits PIE strippé : reconstruction du code
│
├── Reverse_web/                 # Reverse engineering web côté client (TP07–TP10)
│   ├── tp07/                    # Reconnaissance côté client (endpoint caché, secret en dur, contrôle d'accès délégué)
│   ├── tp08/                    # Requête signée : clé HMAC lisible dans le client, forge.py
│   ├── tp09/                    # Obfuscation JS — skimmer simulé, fiche d'IOC
│   └── tp10/                    # WebAssembly : clé de licence, frontière JS↔WASM
│
└── Reverse_windows/              # VM Windows isolée — analyse mémoire & débogage live (TP11–TP14)
    ├── tp11/                     # Cheat Engine : extraction d'un secret en RAM
    ├── tp12/                     # Dump mémoire (System Informer + HxD), secret XOR masqué
    ├── tp13/                     # x64dbg attaché à un process actif, vérification XOR à clé glissante
    └── tp14/                     # Buffer overflow 32 bits — ret2win (x32dbg + payload.py)
```

Chaque dossier de TP contient son énoncé, un rapport (`RAPPORT.md` ou équivalent) avec captures d'écran à l'appui, et les scripts/preuves produits (`.py`, `curl`, etc.).

## 🛠️ Outils utilisés

| Domaine                 | Outils                                                                          |
| ----------------------- | ------------------------------------------------------------------------------- |
| Binaires natifs (Linux) | Ghidra, GDB, `objdump`, `strings`, `file`                                 |
| Web côté client       | DevTools (Network/Sources), `curl`, `webcrack`, `wasm2wat`                |
| Windows (VM isolée)    | Cheat Engine, System Informer, HxD, x64dbg/x32dbg, Ghidra                       |
| Scripts de preuve       | Python 3 (stdlib uniquement : `hmac`, `hashlib`, `struct`, `base64`...) |

## ⚠️ Précautions

- Les TP11–TP14 se déroulent dans une **VM Windows isolée, sans réseau sortant** une fois les outils installés — les cibles manipulées (débordement de tampon, process patché en mémoire) ne doivent jamais tourner sur une machine connectée.
- Toutes les cibles (binaires, pages web, scripts serveur) sont **fournies par le formateur dans un cadre pédagogique**, simulées et inertes — aucune donnée réelle, aucune communication externe.

## 📚 Détail des TP

| TP           | Sujet                                              | Rapport                                                                                         |
| ------------ | -------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Login        | Contournement de vérification, `-O0` vs `-O2` | [`Reverse_natif/login_rapport/README.md`](Reverse_natif/login_rapport/README.md)               |
| Suspicious   | Analyse d'un binaire au comportement suspect       | [`Reverse_natif/suspicious_rapport/README.md`](Reverse_natif/suspicious_rapport/README.md)     |
| XOR strippé | Mot de passe XOR, binaire sans symboles            | [`Reverse_natif/xor_stripped_rapport/README.md`](Reverse_natif/xor_stripped_rapport/README.md) |
| exo2         | Reconstruction de code, ELF PIE strippé           | [`Reverse_natif/exo2_rapport/README.md`](Reverse_natif/exo2_rapport/README.md)                 |
| TP07         | Reconnaissance côté client                       | [`Reverse_web/tp07/RAPPORT.md`](Reverse_web/tp07/RAPPORT.md)                                   |
| TP08         | Requête signée (HMAC lisible côté client)      | [`Reverse_web/tp08/RAPPORT.md`](Reverse_web/tp08/RAPPORT.md)                                   |
| TP09         | Obfuscation JS — skimmer simulé                  | [`Reverse_web/tp09/FICHE_IOC.md`](Reverse_web/tp09/FICHE_IOC.md)                               |
| TP10         | WebAssembly — clé de licence                     | [`Reverse_web/tp10/RAPPORT.md`](Reverse_web/tp10/RAPPORT.md)                                   |
| TP11         | Secret en RAM (Cheat Engine)                       | [`Reverse_windows/tp11/RAPPORT.md`](Reverse_windows/tp11/RAPPORT.md)                           |
| TP12         | Dump mémoire, secret masqué                      | [`Reverse_windows/tp12/RAPPORT.md`](Reverse_windows/tp12/RAPPORT.md)                           |
| TP13         | Débogueur sur process actif                       | [`Reverse_windows/tp13/RAPPORT.md`](Reverse_windows/tp13/RAPPORT.md)                           |
| TP14         | Buffer overflow — ret2win                         | [`Reverse_windows/tp14/RAPPORT.md`](Reverse_windows/tp14/RAPPORT.md)                           |
