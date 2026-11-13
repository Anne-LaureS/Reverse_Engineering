/*
 * TP18 - version A DURCIR (fichier a completer).
 *
 * Reprenez vulnerable.c et corrigez les deux defauts en completant les TODO.
 * Pas de reecriture complete : deux changements ciblés suffisent. La version
 * corrigee, compilee AVEC protections (voir CONSIGNES), resiste au ret2win du
 * Jour 3.
 */
#include <stdio.h>
#include <string.h>

void win(void)
{
    puts("");
    puts(">>> Execution detournee vers win().");
    puts(">>> Drapeau : TP18{code_a_durcir}");
    fflush(stdout);
}

static void traiter(void)
{
    char secret[32];
    char buf[64];
    size_t len;
    int c;

    strcpy(secret, "cle-temporaire-en-clair");
    printf("Entrez le code d'acces : ");
    fflush(stdout);

    /* TODO(1) : lecture BORNEE. fgets ne lit jamais plus que sizeof(buf)
       octets, contrairement a scanf("%s", buf) qui ignore la taille du
       tampon et peut l'ecraser (debordement exploitable, voir TP14/TP15).
       On verifie aussi la valeur de retour : si fgets echoue (EOF, flux
       ferme), buf n'est jamais rempli et il ne faut pas le lire. */
    if (fgets(buf, sizeof(buf), stdin) == NULL) {
        printf("Erreur de lecture.\n");
        memset(secret, 0, sizeof(secret));
        return;
    }

    len = strcspn(buf, "\r\n");

    /* Bonus : validation de longueur explicite. Si fgets n'a trouve aucune
       fin de ligne alors que le tampon est totalement rempli, l'entree
       depassait sizeof(buf) et a ete tronquee : on le signale proprement
       plutot que de traiter silencieusement une entree coupee, et on vide
       le reste de la ligne dans stdin pour ne pas polluer une lecture
       suivante. */
    if (buf[len] == '\0' && len == sizeof(buf) - 1) {
        while ((c = getchar()) != '\n' && c != EOF) {
            /* vide le reste de la ligne trop longue */
        }
        printf("Erreur : entree trop longue (%zu caracteres max).\n",
               sizeof(buf) - 1);
        memset(secret, 0, sizeof(secret));
        return;
    }

    buf[len] = '\0';
    printf("Code recu : %s\n", buf);

    /* TODO(2) : effacer le secret de la memoire avant de quitter la
       fonction -- sur TOUS les chemins de sortie (voir aussi ci-dessus),
       pas seulement celui-ci. */
    memset(secret, 0, sizeof(secret));
}

int main(void)
{
    printf("=== Controle d'acces (simulation TP18 - durci) ===\n");
    traiter();
    printf("Fin normale du programme.\n");
    return 0;
}
