// Logique legitime de la page de paiement (non obfusquee, non piegee).
// Sert de "bruit de fond" realiste autour de l'echantillon a analyser.
document.getElementById("pay").addEventListener("submit", (e) => {
  e.preventDefault();
  alert("Paiement simulé accepté (aucune donnée réelle, aucune transaction).");
});
