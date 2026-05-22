import { useState, useEffect } from 'react';
import DetailLigne from './DetailLigne';
import './App.css';
import Header from './Header';
import Recherche from './Recherche';
import LigneBus from './LigneBus';
import Footer from './Footer';
import Carte from './Carte'; // Importation validée (Étape 7)

function App() {
  // ==========================================
  // 1. Déclaration de tous les états (Lab 5)
  // ==========================================
  const [lignes, setLignes] = useState([]); 
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur] = useState(null);
  const [recherche, setRecherche] = useState("");
  const [ligneSelectionnee, setLigneSelectionnee] = useState(null);
  const [compteurRecherche, setCompteurRecherche] = useState(0);

  // ==========================================
  // MODIFICATION EXO 1 : Fonction de chargement isolée
  // ==========================================
  const chargerDonnees = () => {
    setChargement(true);
    setErreur(null); 
    
    fetch("http://127.0.0.1:5000/lignes")
      .then(response => {
        if (!response.ok) {
          throw new Error("Erreur serveur : " + response.status);
        }
        return response.json();
      })
      .then(data => {
        setLignes(data);
        setChargement(false);
      })
      .catch(error => {
        setErreur(error.message);
        setChargement(false);
      });
  };

  // 2. Charger les données au démarrage
  useEffect(() => {
    chargerDonnees();
  }, []);

  // Logique du "Debounce" (Lab 4)
  useEffect(() => {
    if (recherche === "") return;

    const handler = setTimeout(() => {
      setCompteurRecherche(prev => prev + 1);
    }, 800);

    return () => clearTimeout(handler);
  }, [recherche]);

  const handleChangementRecherche = (valeur) => {
    setRecherche(valeur);
  };

  // Filtrage dynamique des lignes
  const lignesFiltrees = lignes.filter(l =>
    l.depart.toLowerCase().includes(recherche.toLowerCase()) ||
    l.arrivee.toLowerCase().includes(recherche.toLowerCase()) ||
    l.numero.includes(recherche)
  );

  // ==========================================
  // MODIFICATION EXO 3 : Récupération par ID au clic
  // ==========================================
  function handleClickLigne(ligne) {
    if (ligneSelectionnee && ligneSelectionnee.id === ligne.id) {
      setLigneSelectionnee(null);
      return;
    }

    fetch(`http://127.0.0.1:5000/lignes/${ligne.id}`)
      .then(response => {
        if (!response.ok) {
          throw new Error("Impossible de charger les détails de cette ligne.");
        }
        return response.json();
      })
      .then(data => {
        setLigneSelectionnee(data);
      })
      .catch(error => {
        alert(error.message);
      });
  }

  // ==========================================
  // Écrans conditionnels (Chargement / Erreur)
  // ==========================================
  if (chargement) {
    return (
      <div className="App">
        <Header />
        <main className="contenu">
          <p className="message-chargement">Chargement des lignes...</p>
        </main>
      </div>
    );
  }

  if (erreur) {
    return (
      <div className="App">
        <Header />
        <main className="contenu">
          <div className="message-erreur">
            <p>Impossible de charger les lignes.</p>
            <p className="erreur-detail">{erreur}</p>
            <p style={{ marginBottom: "15px" }}>Vérifiez que le serveur Flask est lancé (python api/app.py).</p>
            <button onClick={chargerDonnees} className="bouton-recharger">
              🔄 Tenter de recharger
            </button>
          </div>
        </main>
      </div>
    );
  }

  // Écran normal rendu si (!chargement && !erreur)
  return (
    <div className="App">
      <Header />
      <main className="contenu">
        
        {/* BOUTON RECHARGER (EXERCICE 1) */}
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '15px' }}>
          <button onClick={chargerDonnees} className="bouton-recharger">
            🔄 Recharger les données
          </button>
        </div>

        <p style={{ fontStyle: 'italic', color: '#666' }}>
          Vous avez effectué {compteurRecherche} recherche(s)
        </p>

        <div className="zone-recherche" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Recherche 
            valeur={recherche} 
            onChange={handleChangementRecherche} 
          />
          
          {recherche !== "" && (
            <button onClick={() => setRecherche("")} className="bouton-effacer">
              Effacer
            </button>
          )}
        </div>

        <p className="resultat-recherche">
          {lignesFiltrees.length} ligne{lignesFiltrees.length > 1 ? 's' : ''} trouvée{lignesFiltrees.length > 1 ? 's' : ''}
        </p>

        {lignesFiltrees.length === 0 && (
          <div className="message-erreur">
            <p>Aucune ligne trouvée pour votre recherche.</p>
          </div>
        )}

        {lignesFiltrees.map((ligne) => (
          <LigneBus
            key={ligne.id}
            numero={ligne.numero}
            depart={ligne.depart}
            arrivee={ligne.arrivee}
            arrets={ligne.arrets}
            estSelectionnee={ligneSelectionnee && ligneSelectionnee.id === Math.abs(ligne.id)}
            onClick={() => handleClickLigne(ligne)}
          />
        ))}

        {/* Détails de la ligne sélectionnée */}
        {ligneSelectionnee && (
          <DetailLigne ligne={ligneSelectionnee} />
        )}

        {/* ========================================== */}
        {/* 🗺️ INTÉGRATION DE LA CARTE (Étape 7)         */}
        {/* ========================================== */}
        <Carte />

      </main>
      <Footer />
    </div>
  );
}

export default App;