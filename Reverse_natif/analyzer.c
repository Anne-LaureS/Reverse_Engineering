#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv) {
    const char *name = argc > 1 ? argv[1] : "demo.txt";
    FILE *f = fopen(name, "r");
    if (!f) { perror("fopen"); return EXIT_FAILURE; }
    char buf[128];
    while (fgets(buf, sizeof buf, f)) fputs(buf, stdout);
    fclose(f);
    return EXIT_SUCCESS;
}
