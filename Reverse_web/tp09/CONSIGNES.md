# TP09 — Obfuscation JavaScript (analyse d'un skimmer simulé)

Un script tiers `analytics.js` se comporte comme un **skimmer de formulaire**
(famille Magecart). Tout est **simulé et inerte** : page factice, données
bidon, collecteur **local** qui écrit seulement dans `collector.log`, à côté de
`serve.py`. Rien ne quitte votre machine.

Objectif défensif : reconnaître ce type de code, le désobfusquer, et produire
une **fiche d'IOC** argumentée.

## Mise en route
```bash
python3 serve.py tp09
```
- Démonstration et variation (niveau 1) : http://127.0.0.1:8000/tp09/
- Travail de groupe (niveau 2) : http://127.0.0.1:8000/tp09/tp/

## Rappel : minification ≠ obfuscation
La minification réduit la taille et reste lisible après pretty-print.
L'obfuscation ajoute de la complexité pour résister à l'analyse : tableau de
chaînes encodé, flot de contrôle aplati, code mort, piège anti-debug.

## Démonstration (formateur) — niveau 1, script, 12 min
Cible : `/tp09/`. Fil conducteur : *on ne lit pas du code obfusqué, on lui fait
dire ce qu'il cache*.

### Étape 1 — Le piège anti-debug (3 min)
- **Faire** : ouvrir la page, F12, recharger.
- **Voir** : l'onglet se fige, Sources affiche une pause sur `debugger` dans un
  script anonyme `VM…`. F8 : la pause revient aussitôt.
- **Faire** : Ctrl+F8 (*Deactivate breakpoints*, panneau Sources actif), puis
  F8.
- **Voir** : la page tourne, et reste libre après un rechargement.
- **Dire** : le piège ne protège rien, il fait perdre du temps. Il nous
  apprend surtout que l'auteur ne voulait pas être observé.

> **FAQ**
> - *Rien ne se fige ?* Le piège part au chargement : DevTools ouverts **puis**
>   recharger.
> - *Ctrl+F8 ne fait rien ?* Le raccourci n'agit que dans le panneau Sources.
>   Sinon, cliquer l'icône de point d'arrêt barré, à droite des boutons de
>   pas à pas.
> - *Mes propres points d'arrêt ?* Ils sont désactivés aussi. C'est le
>   compromis de cette parade.
> - *D'où vient ce script `VM…` ?* Du code créé à l'exécution à partir d'une
>   chaîne ; il n'existe dans aucun fichier.

### Étape 2 — Reconnaître la forme (3 min)
- **Faire** : Sources → `analytics.js` → `{}`. Comparer avec `checkout.js`.
- **Voir** : noms en `_0x…`, nombres en hexadécimal, presque aucune chaîne
  lisible. Deux fonctions `a0_0x…` déclarées au premier niveau (chercher
  `function a0_`, leur place varie) : l'une renvoie un grand tableau, l'autre
  est appelée partout avec un nombre.
- **Dire** : c'est la signature d'un obfuscateur grand public. Les chaînes
  sont rangées dans un tableau encodé ; la fonction appelée partout est le
  guichet qui les rend en clair.

> **FAQ**
> - *Comment trouver le guichet ?* C'est la fonction la plus appelée, toujours
>   avec un nombre : `_0x…(0x1a3)`.
> - *Pourquoi les index ne commencent pas à 0 ?* Le guichet soustrait une
>   constante, visible dans ses premières lignes.
> - *Minifié ou obfusqué ?* Si le pretty-print suffit à lire, c'était minifié.

### Étape 3 — Faire parler le tableau (3 min)
- **Faire** : en Console, appeler le guichet avec un index relevé dans le
  code. Puis boucler sur toute la plage d'index et afficher chaque résultat.
- **Voir** : la liste complète des chaînes : une route d'API, des identifiants
  de champs du formulaire, des noms d'événements, des noms de méthodes.
- **Dire** : on n'a pas décodé l'encodage, on a utilisé le décodeur fourni par
  l'échantillon. La liste suffit à formuler une hypothèse sur son rôle.

> **FAQ**
> - *La fonction est appelable en Console ?* Oui si elle est déclarée au
>   premier niveau du fichier, ce qui est le cas ici.
> - *Est-ce risqué de l'appeler ?* Elle ne fait que rendre une chaîne. On
>   n'appelle rien d'autre, et on reste dans une VM de laboratoire.
> - *Longueur de la plage ?* La taille du tableau renvoyé par l'autre fonction
>   `a0_0x…`, à partir de la constante soustraite.

### Étape 4 — Confirmer par l'observation (3 min)
- **Faire** : onglet **Network**, filtre Fetch/XHR. Cliquer dans un champ du
  formulaire puis en sortir. Recommencer après avoir raccourci le numéro de
  carte factice à quelques chiffres.
- **Voir** : une requête sortante dans le premier cas, vers la route lue à
  l'étape 3, avec un corps illisible. Aucune dans le second.
- **Dire** : l'hypothèse est confirmée et on connaît une condition de
  déclenchement. Ce sont trois lignes de la fiche d'IOC : destination,
  champs, déclencheur. Le corps reste à décoder : c'est votre travail.

> **FAQ**
> - *Où part la requête ?* Vers le collecteur local, sur 127.0.0.1. Rien ne
>   quitte la machine ; il écrit dans `collector.log`.
> - *Voir le corps envoyé ?* Cliquer la requête → onglet *Payload*.
> - *Pourquoi un script légitime ne ferait pas ça ?* Il n'a aucune raison de
>   lire les champs de paiement ni de cacher sa destination.

## Variation (un étudiant à l'écran)
Passer l'échantillon dans un désobfuscateur automatique et comparer avec l'analyse manuelle : qu'est-ce que l'outil a défait, qu'est-ce
qu'il reste à comprendre ?

Outil : `webcrack` (`npm install -g webcrack`, demande **Node.js 22 ou 24**),
à installer avant la séance :
```bash
webcrack tp09/analytics.js -o sortie/     # lire sortie/deobfuscated.js
```

## Travail de groupe — niveau 2
Les outils automatiques sont autorisés. La fiche d'IOC doit contenir, pour
chaque élément, **une preuve que l'outil ne donne pas seul** :
- **endpoint d'exfiltration** : capture de l'onglet Network montrant l'envoi ;
- **champs ciblés** et **déclencheur** : ligne de code désobfusqué + test qui
  le confirme (quand l'envoi part, quand il ne part pas) ;
- **encodage de la charge** : schéma et clé, avec un décodeur écrit par vous ;
- **charge décodée** : la dernière ligne de `collector.log`, en clair ;
- **techniques d'obfuscation** rencontrées, et comment chacune a été défaite.

## Restitution
Un groupe présente sa fiche. Discussion : comment empêcher un script tiers
compromis d'agir (SRI, CSP `script-src` / `connect-src`, inventaire des scripts) ?
