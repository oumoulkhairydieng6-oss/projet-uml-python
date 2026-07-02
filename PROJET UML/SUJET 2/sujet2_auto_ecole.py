
from datetime import date, time


# Classe : Eleve
class Eleve:
    """Un élève de l'auto-école."""

    def __init__(self, numero: int, nom: str, prenom: str, adresse: str, date_naissance: date):
        self.__numero = numero
        self.__nom = nom
        self.__prenom = prenom
        self.__adresse = adresse
        self.__date_naissance = date_naissance
        self.__participations = []      
        self.__inscriptions_examen = []  
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
    def adresse(self) -> str:
        return self.__adresse

    @property
    def date_naissance(self) -> date:
        return self.__date_naissance

    @property
    def participations(self) -> list:
        return list(self.__participations)

    @property
    def inscriptions_examen(self) -> list:
        return list(self.__inscriptions_examen)

    def _ajouter_participation(self, participation: "ParticipationSeance") -> None:
        self.__participations.append(participation)

    def _ajouter_inscription(self, inscription: "InscriptionExamen") -> None:
        self.__inscriptions_examen.append(inscription)

    def a_echoue_au_moins_une_fois(self) -> bool:
        """Un élève a échoué s'il a une inscription à examen avec plus de 5 fautes."""
        return any(insc.resultat_fautes > 5 for insc in self.__inscriptions_examen)

    def __str__(self) -> str:
        return f"{self.__prenom} {self.__nom} (n°{self.__numero})"

    def __repr__(self) -> str:
        return f"Eleve(numero={self.__numero!r}, nom={self.__nom!r}, prenom={self.__prenom!r})"


# Classe : CdRom
class CdRom:
    """Un CD-ROM de code de la route, composé de 6 séries."""

    NB_SERIES_MAX = 6

    def __init__(self, numero: int, nom_editeur: str):
        self.__numero = numero
        self.__nom_editeur = nom_editeur
        self.__series = []  

    @property
    def numero(self) -> int:
        return self.__numero

    @property
    def nom_editeur(self) -> str:
        return self.__nom_editeur

    @property
    def series(self) -> list:
        return list(self.__series)

    def ajouter_serie(self, serie: "Serie") -> None:
        if len(self.__series) >= self.NB_SERIES_MAX:
            raise ValueError(f"Un CD-ROM ne peut contenir plus de {self.NB_SERIES_MAX} séries.")
        self.__series.append(serie)

    def __str__(self) -> str:
        return f"CD-ROM n°{self.__numero} ({self.__nom_editeur})"

    def __repr__(self) -> str:
        return f"CdRom(numero={self.__numero!r}, nom_editeur={self.__nom_editeur!r})"


# Classe : Serie
class Serie:
    """Une série de 40 questions, numérotée de 1 à 6 au sein d'un CD-ROM."""

    NB_QUESTIONS_MAX = 40

    def __init__(self, numero: int, cdrom: CdRom):
        if not (1 <= numero <= CdRom.NB_SERIES_MAX):
            raise ValueError("Le numéro de série doit être compris entre 1 et 6.")
        self.__numero = numero
        self.__cdrom = cdrom
        self.__questions_dans_serie = []  
        self.__cdrom.ajouter_serie(self)

    @property
    def numero(self) -> int:
        return self.__numero

    @property
    def cdrom(self) -> CdRom:
        return self.__cdrom

    @property
    def questions_dans_serie(self) -> list:
        return list(self.__questions_dans_serie)

    def _ajouter_question(self, qds: "QuestionDansSerie") -> None:
        if len(self.__questions_dans_serie) >= self.NB_QUESTIONS_MAX:
            raise ValueError(f"Une série ne peut contenir plus de {self.NB_QUESTIONS_MAX} questions.")
        self.__questions_dans_serie.append(qds)

    def __str__(self) -> str:
        return f"Série {self.__numero} du {self.__cdrom}"

    def __repr__(self) -> str:
        return f"Serie(numero={self.__numero!r}, cdrom={self.__cdrom.numero!r})"


# Classe : Question
class Question:
    """Une question de code de la route, pouvant apparaître dans plusieurs séries."""

    def __init__(self, intitule: str, reponse: str, niveau_difficulte: str, theme: str):
        self.__intitule = intitule
        self.__reponse = reponse
        self.__niveau_difficulte = niveau_difficulte
        self.__theme = theme

    @property
    def intitule(self) -> str:
        return self.__intitule

    @property
    def reponse(self) -> str:
        return self.__reponse

    @property
    def niveau_difficulte(self) -> str:
        return self.__niveau_difficulte

    @property
    def theme(self) -> str:
        return self.__theme

    def __str__(self) -> str:
        return f"Q: {self.__intitule} [{self.__theme}/{self.__niveau_difficulte}]"

    def __repr__(self) -> str:
        return f"Question(intitule={self.__intitule!r}, theme={self.__theme!r})"


# Classe d'association : QuestionDansSerie
class QuestionDansSerie:
    """Association Question <-> Serie : place une question à un ordre précis
    dans une série donnée. Une même question peut apparaître dans plusieurs
    séries, avec un numéro d'ordre différent dans chacune."""

    def __init__(self, question: Question, serie: Serie, ordre: int):
        if not (1 <= ordre <= Serie.NB_QUESTIONS_MAX):
            raise ValueError("L'ordre doit être compris entre 1 et 40.")
        self.__question = question
        self.__serie = serie
        self.__ordre = ordre
        self.__serie._ajouter_question(self)

    @property
    def question(self) -> Question:
        return self.__question

    @property
    def serie(self) -> Serie:
        return self.__serie

    @property
    def ordre(self) -> int:
        return self.__ordre

    def __str__(self) -> str:
        return f"Question n°{self.__ordre} de la {self.__serie}"

    def __repr__(self) -> str:
        return f"QuestionDansSerie(ordre={self.__ordre!r}, serie={self.__serie!r})"


# Classe : Seance
class Seance:
    """Une séance de code, à une date/heure donnée, projetant une série d'un CD-ROM."""

    def __init__(self, date_seance: date, heure: time, serie: Serie):
        self.__date = date_seance
        self.__heure = heure
        self.__serie = serie  
        self.__participations = []  

    @property
    def date(self) -> date:
        return self.__date

    @property
    def heure(self) -> time:
        return self.__heure

    @property
    def serie(self) -> Serie:
        return self.__serie

    @property
    def cdrom(self) -> CdRom:
        """CD-ROM choisi, déduit de la série projetée."""
        return self.__serie.cdrom

    @property
    def participations(self) -> list:
        return list(self.__participations)

    def _ajouter_participation(self, participation: "ParticipationSeance") -> None:
        self.__participations.append(participation)

    def __str__(self) -> str:
        return f"Séance du {self.__date} à {self.__heure} ({self.__serie})"

    def __repr__(self) -> str:
        return f"Seance(date={self.__date!r}, heure={self.__heure!r})"


# Classe d'association : ParticipationSeance
class ParticipationSeance:
    """Association Eleve <-> Seance : un élève qui assiste à une séance obtient
    un nombre de fautes (note sur 40) pour la série passée."""

    def __init__(self, eleve: Eleve, seance: Seance, nb_fautes: int = None):
        self.__eleve = eleve
        self.__seance = seance
        self.__nb_fautes = None
        if nb_fautes is not None:
            self.fixer_nb_fautes(nb_fautes)

        self.__eleve._ajouter_participation(self)
        self.__seance._ajouter_participation(self)

    @property
    def eleve(self) -> Eleve:
        return self.__eleve

    @property
    def seance(self) -> Seance:
        return self.__seance

    @property
    def nb_fautes(self) -> int:
        return self.__nb_fautes

    def fixer_nb_fautes(self, nb_fautes: int) -> None:
        """Fixe le nombre de fautes (entre 0 et 40)."""
        if not (0 <= nb_fautes <= 40):
            raise ValueError("Le nombre de fautes doit être compris entre 0 et 40.")
        self.__nb_fautes = nb_fautes

    def __str__(self) -> str:
        return f"{self.__eleve.nom} - {self.__seance} : {self.__nb_fautes} fautes"

    def __repr__(self) -> str:
        return f"ParticipationSeance(eleve={self.__eleve.nom!r}, nb_fautes={self.__nb_fautes!r})"


# Classe : ExamenCode
class ExamenCode:
    """Un examen théorique du code de la route, à une date donnée (un seul examen
    par date), avec un nombre maximum de places (8 élèves)."""

    PLACES_MAX_DEFAUT = 8

    def __init__(self, date_examen: date, places_max: int = PLACES_MAX_DEFAUT):
        self.__date = date_examen
        self.__places_max = places_max
        self.__inscriptions = []  

    @property
    def date(self) -> date:
        return self.__date

    @property
    def places_max(self) -> int:
        return self.__places_max

    @property
    def inscriptions(self) -> list:
        return list(self.__inscriptions)

    @property
    def places_restantes(self) -> int:
        return self.__places_max - len(self.__inscriptions)

    def _ajouter_inscription(self, inscription: "InscriptionExamen") -> None:
        if len(self.__inscriptions) >= self.__places_max:
            raise ValueError(f"Examen complet : {self.__places_max} places maximum.")
        self.__inscriptions.append(inscription)

    def __str__(self) -> str:
        return f"Examen du {self.__date} ({len(self.__inscriptions)}/{self.__places_max} places)"

    def __repr__(self) -> str:
        return f"ExamenCode(date={self.__date!r}, places_max={self.__places_max!r})"


# Classe d'association : InscriptionExamen
class InscriptionExamen:
    """Association Eleve <-> ExamenCode, avec le résultat obtenu (nb de fautes)."""

    def __init__(self, eleve: Eleve, examen: ExamenCode):
        self.__eleve = eleve
        self.__examen = examen
        self.__resultat_fautes = None

        self.__examen._ajouter_inscription(self)
        self.__eleve._ajouter_inscription(self)

    @property
    def eleve(self) -> Eleve:
        return self.__eleve

    @property
    def examen(self) -> ExamenCode:
        return self.__examen

    @property
    def resultat_fautes(self) -> int:
        return self.__resultat_fautes

    def enregistrer_resultat(self, nb_fautes: int) -> None:
        if not (0 <= nb_fautes <= 40):
            raise ValueError("Le nombre de fautes doit être compris entre 0 et 40.")
        self.__resultat_fautes = nb_fautes

    def a_reussi(self) -> bool:
        if self.__resultat_fautes is None:
            raise ValueError("Le résultat de l'examen n'a pas encore été saisi.")
        return self.__resultat_fautes <= 5

    def __str__(self) -> str:
        return f"Inscription de {self.__eleve.nom} à l'{self.__examen}"

    def __repr__(self) -> str:
        return f"InscriptionExamen(eleve={self.__eleve.nom!r}, examen={self.__examen.date!r})"


# Service métier : règle d'éligibilité à l'examen
class RegleEligibilite:
    """Implémente la règle : un élève est autorisé à passer l'examen si,
    sur ses 4 dernières séances, il a obtenu au plus 5 fautes à chaque fois."""

    NB_SEANCES_REQUISES = 4
    SEUIL_FAUTES = 5

    @staticmethod
    def peut_passer_examen(eleve: Eleve) -> tuple:
        """Renvoie (booleen, motif) en fonction des 4 dernières participations."""
        participations = eleve.participations
        if len(participations) < RegleEligibilite.NB_SEANCES_REQUISES:
            return False, "Moins de 4 séances suivies."

        dernieres = participations[-RegleEligibilite.NB_SEANCES_REQUISES:]
        fautes = [p.nb_fautes for p in dernieres]

        if any(f is None for f in fautes):
            return False, "Toutes les séances n'ont pas encore été notées."

        if all(f <= RegleEligibilite.SEUIL_FAUTES for f in fautes):
            return True, "Éligible : 4 dernières séances avec au plus 5 fautes."
        return False, f"Non éligible : fautes constatées = {fautes}."

    @staticmethod
    def inscrire_si_eligible(eleve: Eleve, examen: ExamenCode) -> InscriptionExamen:
        """Inscrit l'élève à l'examen s'il est éligible et qu'il reste des places."""
        eligible, motif = RegleEligibilite.peut_passer_examen(eleve)
        if not eligible:
            raise ValueError(f"Inscription refusée : {motif}")
        if examen.places_restantes <= 0:
            raise ValueError("Inscription refusée : examen complet (8 places max).")
        return InscriptionExamen(eleve=eleve, examen=examen)


# Programme principal de test
if __name__ == "__main__":
    cdrom = CdRom(numero=14, nom_editeur="Codes Rousseau")
    serie5 = Serie(numero=5, cdrom=cdrom)

    q1 = Question("Priorité à droite", "Vrai", "facile", "Priorités")
    q2 = Question("Vitesse en agglomération", "50 km/h", "moyen", "Vitesse")
    QuestionDansSerie(question=q1, serie=serie5, ordre=1)
    QuestionDansSerie(question=q2, serie=serie5, ordre=2)

    eleve = Eleve(numero=1, nom="Ndiaye", prenom="Awa",
                  adresse="Mbour", date_naissance=date(2005, 3, 12))

    fautes_obtenues = [4, 3, 5, 2]
    for i, nb_fautes in enumerate(fautes_obtenues, start=1):
        seance = Seance(date_seance=date(2026, 5, i), heure=time(14, 0), serie=serie5)
        ParticipationSeance(eleve=eleve, seance=seance, nb_fautes=nb_fautes)

    eligible, motif = RegleEligibilite.peut_passer_examen(eleve)
    print(f"Éligible à l'examen ? {eligible} ({motif})")

    examen = ExamenCode(date_examen=date(2026, 6, 1))
    if eligible:
        inscription = RegleEligibilite.inscrire_si_eligible(eleve, examen)
        print(inscription)

        inscription.enregistrer_resultat(nb_fautes=4)
        print(f"A réussi l'examen ? {inscription.a_reussi()}")

    print()
    print(examen)
    print(f"A déjà échoué au moins une fois ? {eleve.a_echoue_au_moins_une_fois()}")
