# TP07 — Reconnaissance côté client

Tout ce que le navigateur exécute, vous pouvez le lire. Objectif : cartographier
une application depuis son code client, puis **prouver** chaque trouvaille par
une requête rejouée hors navigateur.

## Mise en route

```bash
python3 serve.py tp07
```

- Démonstration et variation : http://127.0.0.1:8000/tp07/
- Travail de groupe : http://127.0.0.1:8000/tp07/tp/ (autre application)

## Outils

DevTools : **Sources** (bouton `{}` pour le pretty-print), **Network**,
**Application** (Local Storage), **Console**. Hors navigateur : `curl`.

## Démonstration (formateur) — script, 12 min

Cible : `/tp07/`. Fil conducteur : *ce que l'interface n'appelle pas existe
quand même*.

### Étape 1 — Ce que l'interface appelle (2 min)

- **Faire** : ouvrir la page, F12, onglet **Network**, recharger (Ctrl+R).
  Cliquer « Mon profil ».
- **Voir** : un seul appel d'API, `GET /api/tp07/status`. Le clic sur le bouton
  n'en ajoute aucun.
- **Dire** : Network montre ce que l'application *fait*, pas ce qu'elle *sait
  faire*.

> **FAQ**
>
> - *Network est vide ?* Il n'enregistre que si les DevTools étaient ouverts au
>   chargement : recharger.
> - *Trop de lignes ?* Filtre **Fetch/XHR**.
> - *Firefox ?* Même onglet, « Réseau » ; filtre **XHR**.

### Étape 2 — Lire le bundle (3 min)

- **Faire** : onglet **Sources** → `127.0.0.1:8000` → `tp07` → `app.min.js`.
  Cliquer `{}` sous l'éditeur (*Pretty print*).
- **Voir** : une ligne illisible devient quelques dizaines de lignes indentées,
  avec des fonctions nommées.
- **Dire** : la minification retire les espaces et raccourcit les variables
  locales, rien de plus. Ce n'est pas une protection.

> **FAQ**
>
> - *Pas de bouton `{}` ?* Il est sous l'éditeur, à gauche de « Line, Column ».
>   Firefox : onglet « Débogueur », même icône.
> - *Le pretty-print modifie le fichier ?* Non, c'est un affichage local.
> - *Je vois un dossier `webpack://` ?* C'est la source map : on la garde pour
>   la variation, on n'y touche pas maintenant.

### Étape 3 — Chercher les routes (3 min)

- **Faire** : dans le fichier, Ctrl+F, chercher `fetch(`. Noter chaque URL.
  La constante `API` (première ligne) donne le préfixe commun.
- **Voir** : trois appels dans le code, contre un seul à l'étape 1.
- **Dire** : deux routes existent dans le code et n'ont jamais été appelées.
  On commence par celle qui ne demande rien de plus qu'une URL.

> **FAQ**
>
> - *Chercher dans tous les fichiers à la fois ?* Ctrl+Shift+F (Chrome et
>   Firefox).
> - *Quoi chercher d'autre que `fetch(` ?* `/api/`, `XMLHttpRequest`, `axios`,
>   `http`, `token`, `key`, `secret`, `role`, `admin`.
> - *Pourquoi l'URL n'apparaît pas en entier ?* Elle est assemblée à partir de
>   la constante `API`. Chercher le morceau fixe.

### Étape 4 — Prouver hors navigateur (4 min)

- **Faire** : dans un terminal, `curl -i` sur la route de configuration
  trouvée à l'étape 3, préfixée par `http://127.0.0.1:8000`.
- **Voir** : `200 OK` et une configuration interne en JSON, sans aucune
  authentification.
- **Dire** : une trouvaille n'est prouvée que rejouée hors navigateur. Cacher
  un lien n'est pas un contrôle d'accès : c'est au serveur de refuser.

> **FAQ**
>
> - *Pourquoi `curl` et pas la barre d'adresse ?* `curl -i` montre le code
>   HTTP, se copie dans un rapport et n'envoie que ce qu'on lui demande.
> - *Ajouter un en-tête ?* `-H "Nom: valeur"`. *Un corps ?*
>   `-X POST -H "Content-Type: application/json" -d '{"a":1}'`.
> - *Depuis Network ?* Clic droit sur une requête → *Copy as cURL*.
> - *Et la troisième route ?* Essayez-la : le code HTTP dit ce qui manque.
>   C'est le réflexe attendu dans le travail de groupe.

## Variation (un étudiant à l'écran)

Même application, mais via la **source map** : dans Sources, retrouvez
l'arborescence d'origine, repérez le **feature flag** piloté côté client et
activez-le (Console ou Application → Local Storage). Un nouveau bouton doit
apparaître.

## Travail de groupe — `/tp07/tp/`

Application différente, minifiée, **sans source map**. Trouvez et prouvez :

1. un **endpoint interne** qu'aucun élément de l'interface n'appelle ;
2. un **secret codé en dur** dans le client, et la ressource qu'il ouvre ;
3. un **contrôle d'accès** que le serveur délègue au client : obtenez la
   ressource réservée aux administrateurs.

Livrable : pour chaque point, la commande `curl` qui obtient un `200`
(et le `401`/`403` sans l'astuce), une phrase sur la **cause** et le
**correctif côté serveur**.

## Restitution

Un étudiant par groupe montre ses trois `curl` et répond à la question :
*où doit vivre un contrôle de sécurité ?*
