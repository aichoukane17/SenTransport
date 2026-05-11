import './StatReseau.css';

function StatReseau({ lignes }) {
  const totalLignes = lignes.length;
  const totalArrets = lignes.reduce((sum, l) => sum + l.arrets, 0);
  const ligneMax = lignes.reduce((max, l) => l.arrets > max.arrets ? l : max, lignes[0]);

  return (
    <div className="stat-reseau">
      <div className="stat-reseau-item">
        <span className="stat-reseau-chiffre">{totalLignes}</span>
        <span className="stat-reseau-libelle">Lignes</span>
      </div>
      <div className="stat-reseau-item">
        <span className="stat-reseau-chiffre">{totalArrets}</span>
        <span className="stat-reseau-libelle">Arrêts au total</span>
      </div>
      <div className="stat-reseau-item">
        <span className="stat-reseau-chiffre">{ligneMax.numero}</span>
        <span className="stat-reseau-libelle">Ligne avec le plus d'arrêts</span>
      </div>
    </div>
  );
}

export default StatReseau;