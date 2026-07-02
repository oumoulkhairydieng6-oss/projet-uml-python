"""
SUJET 1 : Gestion des projets d'étudiants
==========================================
Implémentation Python (POO) fidèle au diagramme de classes UML.

Classes du diagramme :
    - Formation
    - Etudiant         (association vers Formation)
    - Project          ("Projet")
    - Binôme           (composition : Project "1" -- "1..*" Binôme)
    - NoteSoutenance    (composition : Binôme "1" -- "2" NoteSoutenance, une par membre)

Relations :
    - Etudiant  --(appartient à)-->  Formation        (agrégation, 1..* -- 1)
    - Binôme    --(composé de)-->    Project           (composition, 1..* -- 1)
    - NoteSoutenance --(composé de)--> Binôme          (composition, 2 -- 1)
    - Binôme a un lien direct vers deux Etudiant (etudiant_a, etudiant_b)

Scénario de séquence implémenté : "calculer_note_finale" d'un binôme
    1. calculer_note_finale(penalite_par_jour)
    2. lire _note_rapport
    3. obtenir valeur (étudiant A)
    4. note_soutenance_A
    5. obtenir valeur (étudiant B)
    6. note_soutenance_B
    7. agréger notes et appliquer points_retard
    8. note_finale (non persistée)
"""

from datetime import date


# Classe : Formation
class Formation:
    """Une formation (ex. MIAGE-IF) caractérisée par un numéro, un nom et une promotion."""

    def __init__(self, numero: int, nom: str, promotion: str):
        self.__numero = numero
        self.__nom = nom
        self.__promotion = promotion

    @property
    def numero(self) -> int:
        return self.__numero

    @property
    def nom(self) -> str:
        return self.__nom

    @property
    def promotion(self) -> str:
        return self.__promotion

    def __str__(self) -> str:
        return f"Formation {self.__nom} ({self.__promotion})"

    def __repr__(self) -> str:
        return f"Formation(numero={self.__numero!r}, nom={self.__nom!r}, promotion={self.__promotion!r})"


# Classe : Etudiant
class Etudiant:
    """Un étudiant identifié par un numéro unique, appartenant à une Formation."""

    def __init__(self, numero: int, nom: str, prenom: str, formation: Formation):
        self.__numero = numero
        self.__nom = nom
        self.__prenom = prenom
        self.__formation = formation  

    @property
    def numero(self) -> int:
        return self.__numero

    @property
    def nom(self) -> str:
        return self.__nom

    @property
    def prenom(self) -> str:
        return self.__prenom

    @property
    def formation(self) -> Formation:
        return self.__formation

    def __str__(self) -> str:
        return f"{self.__prenom} {self.__nom} (n°{self.__numero})"

    def __repr__(self) -> str:
        return f"Etudiant(numero={self.__numero!r}, nom={self.__nom!r}, prenom={self.__prenom!r})"


# Classe : Project (Projet)
class Project:
    """Un projet identifié par un numéro, caractérisé par une matière, un sujet
    et une date de remise prévue du rapport."""

    def __init__(self, numero: int, nom_matiere: str, sujet: str, date_remise_prevue: date):
        self.__numero = numero
        self.__nom_matiere = nom_matiere
        self.__sujet = sujet
        self.__date_remise_prevue = date_remise_prevue
        self.__binomes = []  

    @property
    def numero(self) -> int:
        return self.__numero

    @property
    def nom_matiere(self) -> str:
        return self.__nom_matiere

    @property
    def sujet(self) -> str:
        return self.__sujet

    @property
    def date_remise_prevue(self) -> date:
        return self.__date_remise_prevue

    @property
    def binomes(self) -> list:
        return list(self.__binomes)  

    def _ajouter_binome(self, binome: "Binome") -> None:
        """Méthode interne appelée par Binome lors de sa création (composition)."""
        self.__binomes.append(binome)

    def __str__(self) -> str:
        return f"Projet {self.__nom_matiere} (n°{self.__numero}) - {self.__sujet}"

    def __repr__(self) -> str:
        return f"Project(numero={self.__numero!r}, nom_matiere={self.__nom_matiere!r})"


# Classe : Binome
class Binome:
    """Un binôme (groupe de 2 étudiants max) réalisant un Project donné.

    Composition : un Binôme appartient à un seul Project (lien fort).
    Chaque Binôme porte une note de rapport commune et est lié à 2 étudiants.
    """

    def __init__(self, projet: Project, numero_relatif: int, etudiant_a: Etudiant, etudiant_b: Etudiant = None):
        self.__projet = projet
        self.__numero_relatif_projet = numero_relatif
        self.__etudiant_a = etudiant_a
        self.__etudiant_b = etudiant_b  
        self.__date_remise_effective = None
        self.__note_rapport = None
        self.__notes_soutenance = []  
        self.__projet._ajouter_binome(self)

    @property
    def projet(self) -> Project:
        return self.__projet

    @property
    def numero_relatif_projet(self) -> int:
        return self.__numero_relatif_projet

    @property
    def etudiant_a(self) -> Etudiant:
        return self.__etudiant_a

    @property
    def etudiant_b(self) -> Etudiant:
        return self.__etudiant_b

    @property
    def date_remise_effective(self) -> date:
        return self.__date_remise_effective

    @property
    def note_rapport(self) -> float:
        return self.__note_rapport

    def enregistrer_remise_effective(self, date_remise: date) -> None:
        """Enregistre la date à laquelle le rapport a réellement été remis."""
        self.__date_remise_effective = date_remise

    def definir_note_rapport(self, note: float) -> None:
        """Définit la note de rapport, commune aux deux membres du binôme."""
        if not (0 <= note <= 20):
            raise ValueError("La note de rapport doit être comprise entre 0 et 20.")
        self.__note_rapport = note

    def jours_retard(self) -> int:
        """Nombre de jours de retard entre la date prévue et la date effective."""
        if self.__date_remise_effective is None:
            return 0
        delta = (self.__date_remise_effective - self.__projet.date_remise_prevue).days
        return max(0, delta)

    def points_retard(self, penalite_par_jour: float) -> float:
        """Nombre de points à déduire en fonction du nombre de jours de retard."""
        return self.jours_retard() * penalite_par_jour

    def _ajouter_note_soutenance(self, note: "NoteSoutenance") -> None:
        """Méthode interne appelée par NoteSoutenance lors de sa création (composition)."""
        self.__notes_soutenance.append(note)

    def note_soutenance_de(self, etudiant: Etudiant) -> float:
        """Renvoie la valeur de la note de soutenance individuelle d'un étudiant du binôme."""
        for note in self.__notes_soutenance:
            if note.etudiant is etudiant:
                return note.valeur
        raise ValueError(f"Aucune note de soutenance trouvée pour {etudiant}.")

    def calculer_note_finale(self, penalite_par_jour: float) -> dict:
        """Calcule la note finale du projet pour chaque membre du binôme.

        Note finale = moyenne(note_rapport, note_soutenance individuelle) - points_retard
        (la note finale n'est jamais stockée, uniquement calculée à la demande).
        """
        if self.__note_rapport is None:
            raise ValueError("La note de rapport n'a pas encore été définie.")

        retard = self.points_retard(penalite_par_jour)
        resultats = {}

        for etudiant in (self.__etudiant_a, self.__etudiant_b):
            if etudiant is None:
                continue
            note_soutenance = self.note_soutenance_de(etudiant)
            moyenne = (self.__note_rapport + note_soutenance) / 2
            note_finale = moyenne - retard
            resultats[etudiant.nom] = round(min(20, max(0, note_finale)), 2)

        return resultats

    def __str__(self) -> str:
        membres = self.__etudiant_a.nom
        if self.__etudiant_b:
            membres += f" & {self.__etudiant_b.nom}"
        return f"Binôme n°{self.__numero_relatif_projet} ({membres}) - {self.__projet.nom_matiere}"

    def __repr__(self) -> str:
        return f"Binome(projet={self.__projet.numero!r}, numero_relatif={self.__numero_relatif_projet!r})"


# Classe : NoteSoutenance
class NoteSoutenance:
    """Note de soutenance individuelle d'un étudiant pour un binôme donné.

    Composition : une NoteSoutenance appartient à un seul Binôme.
    """

    def __init__(self, etudiant: Etudiant, binome: Binome, valeur: float):
        if not (0 <= valeur <= 20):
            raise ValueError("La note de soutenance doit être comprise entre 0 et 20.")
        self.__etudiant = etudiant
        self.__binome = binome
        self.__valeur = valeur

        self.__binome._ajouter_note_soutenance(self)

    @property
    def etudiant(self) -> Etudiant:
        return self.__etudiant

    @property
    def binome(self) -> Binome:
        return self.__binome

    @property
    def valeur(self) -> float:
        return self.__valeur

    def __str__(self) -> str:
        return f"Note de soutenance de {self.__etudiant.nom} : {self.__valeur}/20"

    def __repr__(self) -> str:
        return f"NoteSoutenance(etudiant={self.__etudiant.nom!r}, valeur={self.__valeur!r})"


# Programme principal de test
if __name__ == "__main__":
    formation = Formation(numero=1, nom="MIAGE-IF", promotion="Initiale")

    alice = Etudiant(numero=101, nom="Diop", prenom="Alice", formation=formation)
    bilal = Etudiant(numero=102, nom="Faye", prenom="Bilal", formation=formation)

    projet_bdd = Project(
        numero=1,
        nom_matiere="Entrepôt de données",
        sujet="Modélisation Merise d'une base scolaire",
        date_remise_prevue=date(2026, 4, 12),
    )

    binome1 = Binome(projet=projet_bdd, numero_relatif=1, etudiant_a=alice, etudiant_b=bilal)

    binome1.enregistrer_remise_effective(date(2026, 4, 14))
    binome1.definir_note_rapport(15.0)

    NoteSoutenance(etudiant=alice, binome=binome1, valeur=16.0)
    NoteSoutenance(etudiant=bilal, binome=binome1, valeur=13.5)

    print(f"Jours de retard : {binome1.jours_retard()}")
    print(f"Points de retard déduits : {binome1.points_retard(penalite_par_jour=0.5)}")

    notes_finales = binome1.calculer_note_finale(penalite_par_jour=0.5)
    print("Notes finales :")
    for nom, note in notes_finales.items():
        print(f"  - {nom} : {note}/20")

    print()
    print(repr(projet_bdd))
    print(repr(binome1))
    print(formation)
    print(alice, "|", bilal)
