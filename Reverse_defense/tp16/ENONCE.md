# TP16 — Ingénierie inverse d'un logiciel avec un anti-debug

## Objectif
Analyser un programme qui **refuse d'être débogué** : il détecte le débogueur et
s'arrête avant de révéler son drapeau. Votre but est de **défaire l'anti-debug**
pour obtenir le drapeau **tout en restant attaché** au débogueur.

## Mise en route
Lancez `tp16\tp\protege.exe` **dans** x64dbg (ou attachez-vous à lui) : vous
verrez le blocage. Sans débogueur, le programme va au bout — mais l'exercice est
de l'étudier **sous** débogueur.

## Outils
- **x64dbg** (cible 64 bits) et, si disponible, le greffon **ScyllaHide**.
- **Ghidra** pour repérer les vérifications anti-debug.

## À vous de jouer
Cette cible est coriace : elle ne passe **pas** par `IsDebuggerPresent`
(patcher cette API ne sert à rien). Elle enchaîne **deux** contrôles : la
lecture directe de `BeingDebugged` dans le PEB, **puis** `CheckRemoteDebuggerPresent`.
1. Dans Ghidra, repérez ces **deux contrôles enchaînés** et déterminez lequel
   s'exécute en premier et **court-circuite** l'autre (neutraliser seulement le
   second ne changerait rien).
2. Neutralisez-les : le plus simple est de **forcer la branche de décision**
   (celle qui mène à « Debogueur detecte »), ce qui défait les deux d'un coup ;
   ScyllaHide est une alternative (il masque le PEB **et** couvre
   `CheckRemoteDebuggerPresent`).
3. Obtenez le drapeau `TP16-TP{...}` **tout en restant attaché**.

## Livrable
- La (ou les) vérification(s) identifiée(s).
- La méthode de neutralisation.
- Le drapeau obtenu.

## Bonus
- Rendez la neutralisation **permanente** en patchant le fichier (gardez une
  copie de l'original). Expliquez pourquoi un analyste fait cela quand il doit
  rejouer souvent.

## Restitution
Un anti-debug peut-il vraiment empêcher l'analyse, ou seulement la ralentir ?
