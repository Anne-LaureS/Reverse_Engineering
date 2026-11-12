# TP10 — Ingénierie inverse d'un module WebAssembly

Un logiciel vérifie une **clé de licence** dans un module **WASM**. La clé n'est
stockée nulle part en clair. Une partie de la vérification dépend d'une valeur
fournie par le **JavaScript** : c'est la **frontière JS ↔ WASM**, et c'est elle
qu'on attaque en premier.

## Mise en route
```bash
python3 serve.py tp10
```
Prérequis, à installer **avant la séance** : `wabt` (`sudo apt install wabt`),
qui fournit `wasm2wat`, `wat2wasm`, `wasm-objdump` et `wasm-decompile`.
- Démonstration et variation : http://127.0.0.1:8000/tp10/
- Travail de groupe : http://127.0.0.1:8000/tp10/tp/ (autre module)

## Démonstration (formateur) — script, 15 min
Cible : `/tp10/`, fichier `tp10/license.wasm` du kit. Fil conducteur : *même
méthode qu'au Jour 1, on commence par ce que le module échange avec
l'extérieur*.

### Étape 1 — Triage (2 min)
- **Faire** : `file tp10/license.wasm` puis `strings -n 4 tp10/license.wasm`.
- **Voir** : un binaire WebAssembly ; quelques noms (`seed`, `memory`,
  `buffer`, `check`), aucune clé lisible.
- **Dire** : comme pour un ELF, `strings` donne le vocabulaire du module avant
  toute lecture de code.

> **FAQ**
> - *C'est quoi, WASM ?* Un bytecode pour une machine à pile, exécuté dans le
>   bac à sable du navigateur. Pas d'accès direct au DOM ni au réseau : tout
>   passe par des fonctions que le JS lui fournit.
> - *Pourquoi les noms sont visibles ?* Imports et exports sont toujours en
>   clair, le JS en a besoin. Les autres noms viennent d'une section `name`
>   facultative, présente ici, absente du module de groupe.

### Étape 2 — Imports, exports, données (3 min)
- **Faire** : `wasm-objdump -x tp10/license.wasm`.
- **Voir** : un import `env.seed` ; trois exports (`memory`, `buffer`,
  `check`) ; un segment **Data** de 16 octets chargé à l'adresse `0x10000`.
- **Dire** : l'import est la frontière JS ↔ WASM annoncée dans l'énoncé. Le
  segment Data a exactement la taille d'une table de comparaison.

> **FAQ**
> - *`wasm-objdump` introuvable ?* `sudo apt install wabt`.
> - *Voir seulement les données ?* `wasm-objdump -s -j Data fichier.wasm`.
> - *C'est quoi, `memory` ?* La mémoire linéaire : un seul tableau d'octets,
>   partagé avec le JS (`new Uint8Array(wasm.memory.buffer)`). Les adresses
>   sont de simples indices dans ce tableau.

### Étape 3 — Lire `check` (4 min)
- **Faire** : `wasm-decompile tp10/license.wasm` (ou `wasm2wat` pour le texte
  officiel). Lire `check`, puis ouvrir `tp10/app.js` pour voir ce que renvoie
  l'import `seed`.
- **Voir** : un test de longueur, un appel à `js_seed`, une boucle qui combine
  par XOR un octet saisi, un compteur et le seed, puis compare avec les octets
  du segment Data. Dans `app.js`, le seed est une constante.
- **Dire** : c'est le crackme XOR du Jour 1 (TP05). La seule nouveauté est
  qu'une partie de la clé de transformation vit côté JS.

> **FAQ**
> - *`wasm2wat` ou `wasm-decompile` ?* `wasm2wat` est exact mais verbeux
>   (machine à pile). `wasm-decompile` donne un pseudo-C plus rapide à lire.
> - *La boucle est bizarre, elle avance de 2 ?* Le compilateur l'a déroulée et
>   a replié des constantes. Raisonner sur un tour, pas sur la forme.
> - *Que veut dire `(b + 65461)[0]:ubyte` ?* Lecture d'un octet non signé en
>   mémoire à l'adresse `b + 65461`.
> - *Ghidra, IDA ?* Possible avec des extensions, non nécessaire ici.

### Étape 4 — Vérifier en dynamique (4 min)
- **Faire** : F12 → **Sources** → `license.wasm` (affiché en texte). Poser un
  point d'arrêt sur la première instruction de `$check`. Saisir une clé
  quelconque de 16 caractères, cliquer « Activer ».
- **Voir** : pause dans `$check`. Dans **Scope**, les variables locales et
  `memory` ; clic droit sur `memory` → *Reveal in Memory inspector* : la saisie
  et la table sont visibles à quelques octets d'écart, autour de `0x10000`.
- **Dire** : la lecture statique est une hypothèse, la pause la confirme. On
  avance pas à pas (F9) pour voir la première comparaison échouer.

> **FAQ**
> - *Le module n'apparaît pas dans Sources ?* Recharger DevTools ouverts ; il
>   est listé à côté de `app.js`.
> - *Aller à une adresse ?* Dans le Memory inspector, saisir `0x10000` dans le
>   champ d'adresse.
> - *Firefox ?* Le débogueur affiche aussi le module en texte, sans inspecteur
>   mémoire : utiliser la Console (`new Uint8Array(wasm.memory.buffer)`).

### Étape 5 — Conclure (2 min)
- **Faire** : écrire au tableau la relation lue à l'étape 3, puis l'inverser
  pour obtenir chaque caractère à partir de la table, du compteur et du seed.
  Calculer en Console ou en Python, saisir le résultat sur la page.
- **Voir** : « ✔ Licence valide ».
- **Dire** : XOR est sa propre réciproque. Tout ce qu'il fallait était chez le
  client : la table dans le module, le seed dans le JS.

> **FAQ**
> - *Et si le seed venait du serveur ?* Il arriverait quand même dans le
>   navigateur, donc lisible par un point d'arrêt sur l'import.
> - *Qu'est-ce qui résisterait ?* Envoyer la clé au serveur et vérifier là-bas.

## Variation (un étudiant à l'écran)
Sans lire le module : depuis la Console, écrire des octets dans
`new Uint8Array(wasm.memory.buffer)` à l'adresse `wasm.buffer()`, puis appeler
`wasm.check(longueur)`. Puis parcourez les premiers kilo-octets de la mémoire
linéaire : où se trouvent les octets que `check` compare ?

## Travail de groupe — `/tp10/tp/`
Module compilé sans noms ; il n'est plus exposé dans `window` ; la longueur, la
transformation et la valeur fournie par le JS diffèrent de la démonstration.
1. Retrouvez la longueur attendue, l'opération appliquée à chaque octet, la
   table et la valeur importée depuis le JS.
2. Écrivez un **solveur Python** qui affiche la clé ; validez-la sur la page.

Pistes : la même famille de transformation que le crackme XOR du Jour 1 (TP05).
Pour atteindre le module sans `window.wasm`, un point d'arrêt dans la glue JS
suffit.

### Bonus
- **Patcher** le module (`wasm2wat` → éditer → `wat2wasm`) pour que `check`
  accepte toute clé. Vous servez vous-même le fichier : remplacez
  `tp10/tp/license.wasm` par votre version (gardez une copie de l'original) et
  rechargez la page.
- Expliquer pourquoi seule une vérification **côté serveur** résiste.

## Restitution
Un groupe montre son solveur et, s'il l'a fait, le module patché. Conclusion :
*tout ce qui s'exécute chez le client est lisible et modifiable, WASM compris.*
