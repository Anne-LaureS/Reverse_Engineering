# TP08 — Analyse dynamique dans le navigateur (requête signée)

Le client signe chaque virement avec un HMAC-SHA256. Le serveur refuse toute
requête mal signée ou trop ancienne (±30 s). Le code est minifié, **sans source
map**.

## Mise en route
```bash
python3 serve.py tp08
```
- Démonstration et variation : http://127.0.0.1:8000/tp08/
- Travail de groupe : http://127.0.0.1:8000/tp08/tp/ (signature construite autrement)

## Démonstration (formateur)
1. Rejouer la requête avec un autre montant → **401**. Firefox : Network →
   *Edit and Resend*. Chrome n'a pas cette fonction : clic droit → *Copy as
   fetch* (à coller dans la Console) ou *Copy as cURL*.
2. Point d'arrêt sur la requête : Sources → *XHR/fetch Breakpoints* → `transfer`.
3. Remonter la **pile d'appels** jusqu'à la fonction qui calcule la signature.
4. **Pendant la pause**, appeler cette fonction depuis la Console. Le script est
   un module ES : ses fonctions ne sont pas globales, elles ne sont accessibles
   qu'en étant arrêté dans sa portée.

## Variation (un étudiant à l'écran)
Récupérer la clé **sans arrêter l'exécution** : *logpoint* (clic droit sur un
numéro de ligne → *Add logpoint*) qui affiche la valeur reconstituée.

## Travail de groupe — `/tp08/tp/`
La clé, le message signé, l'encodage de la signature et les en-têtes diffèrent
de la démonstration. Écrivez **`forge.py`** : un script Python qui envoie un
virement d'un montant de votre choix et obtient un **200**, sans navigateur.

À établir par l'analyse : la clé, la composition exacte du message, l'encodage
de la signature, les noms d'en-têtes.

## Restitution
Démonstration de `forge.py` → `200`. Discussion : que protège une signature
calculée par le client ? Que changerait un secret qui ne quitte jamais le
serveur ?
