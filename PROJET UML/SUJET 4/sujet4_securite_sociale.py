"""
SUJET 4 : Organisme de sécurité sociale — patients, médecins, remboursements
==============================================================================
Implémentation Python (POO) fidèle au diagramme de classes UML.

Hiérarchie d'héritage :
    Personne (abstraite)
        ├── Assure
        │      └── Patient (un Assuré qui consulte ; a choisi ou non un médecin traitant)
        └── Medecin (un Médecin peut aussi être Assuré -> héritage multiple en Python)
               ├── Generaliste
               └── Specialiste

Classes complémentaires :
    - OrganismeSS
    - Consultation              (Patient consulte un Generaliste à une date donnée)
    - PrescriptionSpecialiste   (un Generaliste peut prescrire une consultation chez un Specialiste)
    - FeuilleMaladie
    - OrdonnanceMedicament
    - Remboursement

Relations principales :
    - Patient hérite de Assure ; Generaliste et Specialiste héritent de Medecin
    - Medecin peut aussi être Assure (héritage multiple, cas d'un médecin malade)
    - Patient "0..1" --(médecin traitant)--> "0..1" Generaliste
    - Consultation "1" --(0..1..*)--> PrescriptionSpecialiste --(oriente vers)--> Specialiste
    - Medecin --(saisit)--> FeuilleMaladie ; Medecin --(prescrit)--> OrdonnanceMedicament
    - OrganismeSS --(traite)--> Remboursement

Scénarios de séquence implémentés :
    A) "Consultation et prescription spécialiste"
    B) "Feuille de maladie et remboursement"
"""

from abc import ABC
from datetime import date


# Classe abstraite : Personne
class Personne(ABC):
    """Classe abstraite de base : toute personne du système a une identité."""

    def __init__(self, identite: str):
        self._identite = identite  

    @property
    def identite(self) -> str:
        return self._identite

    def __str__(self) -> str:
        return self._identite

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(identite={self._identite!r})"


# Classe : Assure
class Assure(Personne):
    """Un assuré de la sécurité sociale."""

    def __init__(self, identite: str, numero_assure: str):
        super().__init__(identite)
        self.__numero_assure = numero_assure

    @property
    def numero_assure(self) -> str:
        return self.__numero_assure

    def __str__(self) -> str:
        return f"Assuré {self._identite} (n°{self.__numero_assure})"


# Classe : Medecin
class Medecin(Personne):
    """Un médecin (généraliste ou spécialiste), identifié par son numéro RPPS.
    Un médecin peut également être assuré (cf. classe Patient pour ce cas)."""

    def __init__(self, identite: str, numero_rpps: str):
        super().__init__(identite)
        self.__numero_rpps = numero_rpps
        self.__feuilles_maladie_saisies = []
        self.__ordonnances_prescrites = []

    @property
    def numero_rpps(self) -> str:
        return self.__numero_rpps

    def saisir_feuille_maladie(self, feuille: "FeuilleMaladie") -> None:
        """Tout médecin peut enregistrer une feuille de maladie."""
        self.__feuilles_maladie_saisies.append(feuille)
        feuille._definir_medecin(self)

    def prescrire_medicament(self, ordonnance: "OrdonnanceMedicament") -> None:
        """Tout médecin peut prescrire des médicaments."""
        self.__ordonnances_prescrites.append(ordonnance)
        ordonnance._definir_medecin(self)

    def __str__(self) -> str:
        return f"{self._identite} (RPPS {self.__numero_rpps})"


# Classe : Generaliste
class Generaliste(Medecin):
    """Un médecin généraliste, pouvant être le médecin traitant de patients
    et réalisant des consultations."""

    def __init__(self, identite: str, numero_rpps: str):
        super().__init__(identite, numero_rpps)
        self.__consultations = []  

    @property
    def consultations(self) -> list:
        return list(self.__consultations)

    def consulter(self, patient: "Patient", date_consultation: date) -> "Consultation":
        """Le généraliste réalise une consultation pour un patient à une date donnée."""
        consultation = Consultation(patient=patient, generaliste=self, date_consultation=date_consultation)
        self.__consultations.append(consultation)
        return consultation

    def __str__(self) -> str:
        return f"{self._identite} (généraliste)"


# Classe : Specialiste
class Specialiste(Medecin):
    """Un médecin spécialiste, caractérisé par sa spécialité."""

    def __init__(self, identite: str, numero_rpps: str, specialite: str):
        super().__init__(identite, numero_rpps)
        self.__specialite = specialite

    @property
    def specialite(self) -> str:
        return self.__specialite

    def __str__(self) -> str:
        return f"{self._identite} (spécialiste en {self.__specialite})"


# Classe : Patient
class Patient(Assure):
    """Un patient, qui est un Assuré ayant choisi ou non un médecin traitant
    (un Generaliste)."""

    def __init__(self, identite: str, numero_assure: str):
        super().__init__(identite, numero_assure)
        self.__medecin_traitant = None  
        self.__a_choisi_medecin_traitant = False
        self.__consultations = []       
        self.__feuilles_maladie = []    

    @property
    def medecin_traitant(self) -> Generaliste:
        return self.__medecin_traitant

    @property
    def a_choisi_medecin_traitant(self) -> bool:
        return self.__a_choisi_medecin_traitant

    def choisir_medecin_traitant(self, generaliste: Generaliste) -> None:
        self.__medecin_traitant = generaliste
        self.__a_choisi_medecin_traitant = True

    def _ajouter_consultation(self, consultation: "Consultation") -> None:
        self.__consultations.append(consultation)

    def _ajouter_feuille_maladie(self, feuille: "FeuilleMaladie") -> None:
        self.__feuilles_maladie.append(feuille)

    @property
    def consultations(self) -> list:
        return list(self.__consultations)

    @property
    def feuilles_maladie(self) -> list:
        return list(self.__feuilles_maladie)

    def __str__(self) -> str:
        return f"Patient {self._identite} (n°{self.numero_assure})"


# Classe : Consultation
class Consultation:
    """Une consultation d'un patient chez un généraliste, à une date donnée."""

    def __init__(self, patient: Patient, generaliste: Generaliste, date_consultation: date):
        self.__patient = patient
        self.__generaliste = generaliste
        self.__date = date_consultation
        self.__prescriptions = []  

        patient._ajouter_consultation(self)

    @property
    def patient(self) -> Patient:
        return self.__patient

    @property
    def generaliste(self) -> Generaliste:
        return self.__generaliste

    @property
    def date(self) -> date:
        return self.__date

    @property
    def prescriptions(self) -> list:
        return list(self.__prescriptions)

    def prescrire_consultation_specialiste(self, specialiste: Specialiste,
                                            date_prescription: date) -> "PrescriptionSpecialiste":
        """Le généraliste peut, lors de la consultation, prescrire une consultation
        chez un ou plusieurs spécialistes."""
        prescription = PrescriptionSpecialiste(
            consultation=self, specialiste=specialiste, date_prescription=date_prescription
        )
        self.__prescriptions.append(prescription)
        return prescription

    def __str__(self) -> str:
        return f"Consultation du {self.__date} : {self.__patient} chez {self.__generaliste}"

    def __repr__(self) -> str:
        return f"Consultation(date={self.__date!r})"


# Classe : PrescriptionSpecialiste
class PrescriptionSpecialiste:
    """Une prescription de consultation chez un spécialiste, émise par un
    généraliste lors d'une consultation."""

    def __init__(self, consultation: Consultation, specialiste: Specialiste, date_prescription: date):
        self.__consultation = consultation
        self.__specialiste = specialiste
        self.__date = date_prescription

    @property
    def consultation(self) -> Consultation:
        return self.__consultation

    @property
    def specialiste(self) -> Specialiste:
        return self.__specialiste

    @property
    def date(self) -> date:
        return self.__date

    def __str__(self) -> str:
        return f"Prescription du {self.__date} vers {self.__specialiste}"

    def __repr__(self) -> str:
        return f"PrescriptionSpecialiste(date={self.__date!r})"


# Classe : FeuilleMaladie
class FeuilleMaladie:
    """Une feuille de maladie, saisie par un médecin pour un patient,
    permettant ensuite un remboursement."""

    def __init__(self, reference: str, patient: Patient):
        self.__reference = reference
        self.__patient = patient
        self.__medecin = None  
        self.__remboursement = None

        patient._ajouter_feuille_maladie(self)

    @property
    def reference(self) -> str:
        return self.__reference

    @property
    def patient(self) -> Patient:
        return self.__patient

    @property
    def medecin(self) -> Medecin:
        return self.__medecin

    @property
    def remboursement(self) -> "Remboursement":
        return self.__remboursement

    def _definir_medecin(self, medecin: Medecin) -> None:
        self.__medecin = medecin

    def _definir_remboursement(self, remboursement: "Remboursement") -> None:
        self.__remboursement = remboursement

    def __str__(self) -> str:
        return f"Feuille de maladie {self.__reference} ({self.__patient})"

    def __repr__(self) -> str:
        return f"FeuilleMaladie(reference={self.__reference!r})"


# Classe : OrdonnanceMedicament
class OrdonnanceMedicament:
    """Une ordonnance de médicament(s), prescrite par un médecin."""

    def __init__(self, patient: Patient, medicaments: list = None):
        self.__patient = patient
        self.__medicaments = list(medicaments) if medicaments else []
        self.__medecin = None  

    @property
    def patient(self) -> Patient:
        return self.__patient

    @property
    def medicaments(self) -> list:
        return list(self.__medicaments)

    @property
    def medecin(self) -> Medecin:
        return self.__medecin

    def _definir_medecin(self, medecin: Medecin) -> None:
        self.__medecin = medecin

    def __str__(self) -> str:
        return f"Ordonnance pour {self.__patient} : {', '.join(self.__medicaments)}"

    def __repr__(self) -> str:
        return f"OrdonnanceMedicament(patient={self.__patient.identite!r})"


# Classe : Remboursement
class Remboursement:
    """Un remboursement calculé par l'organisme de sécurité sociale
    pour une feuille de maladie donnée."""

    def __init__(self, feuille: FeuilleMaladie, montant: float, date_remboursement: date):
        self.__feuille = feuille
        self.__montant = montant
        self.__date = date_remboursement
        feuille._definir_remboursement(self)

    @property
    def feuille(self) -> FeuilleMaladie:
        return self.__feuille

    @property
    def montant(self) -> float:
        return self.__montant

    @property
    def date(self) -> date:
        return self.__date

    def __str__(self) -> str:
        return f"Remboursement de {self.__montant}€ le {self.__date} ({self.__feuille.reference})"

    def __repr__(self) -> str:
        return f"Remboursement(montant={self.__montant!r}, date={self.__date!r})"


# Classe : OrganismeSS
class OrganismeSS:
    """L'organisme de sécurité sociale : point d'entrée des opérations
    administratives (inscription, médecin traitant, feuilles, remboursements)."""

    TAUX_REMBOURSEMENT = 0.70  
    def __init__(self, nom: str):
        self.__nom = nom
        self.__assures = []
        self.__remboursements = []

    @property
    def nom(self) -> str:
        return self.__nom

    def inscrire_assure(self, assure: Assure) -> None:
        self.__assures.append(assure)

    def enregistrer_medecin_traitant(self, patient: Patient, generaliste: Generaliste) -> None:
        patient.choisir_medecin_traitant(generaliste)

    def traiter_feuille_maladie(self, feuille: FeuilleMaladie, montant_facture: float) -> Remboursement:
        """Scénario de séquence 'feuille de maladie et remboursement' :
        valide la feuille, calcule le montant éligible, crée le remboursement."""
        montant_remboursable = round(montant_facture * self.TAUX_REMBOURSEMENT, 2)
        remboursement = Remboursement(
            feuille=feuille, montant=montant_remboursable, date_remboursement=date.today()
        )
        self.__remboursements.append(remboursement)
        return remboursement

    def __str__(self) -> str:
        return f"Organisme {self.__nom}"


# Programme principal de test
if __name__ == "__main__":
    org = OrganismeSS(nom="CSS Sénégal")

    dr_diallo = Generaliste(identite="Dr Diallo", numero_rpps="RPPS-001")
    dr_sarr = Specialiste(identite="Dr Sarr", numero_rpps="RPPS-002", specialite="Cardiologie")

    patient = Patient(identite="Moussa Ba", numero_assure="ASS-12345")
    org.inscrire_assure(patient)
    org.enregistrer_medecin_traitant(patient, dr_diallo)
    print(f"{patient} - médecin traitant choisi ? {patient.a_choisi_medecin_traitant} ({patient.medecin_traitant})")

    consultation = dr_diallo.consulter(patient, date_consultation=date(2026, 6, 10))
    prescription = consultation.prescrire_consultation_specialiste(dr_sarr, date_prescription=date(2026, 6, 10))
    print(consultation)
    print(prescription)

    class MedecinAssure(Medecin, Assure):
        """Un médecin qui est lui-même assuré social (cas explicitement permis par le sujet).
        Illustre l'héritage multiple en Python : la classe hérite à la fois de
        Medecin et d'Assure, chacune apportant ses propres attributs."""

        def __init__(self, identite, numero_rpps, numero_assure):
            Personne.__init__(self, identite)
            self._Medecin__numero_rpps = numero_rpps
            self._Medecin__feuilles_maladie_saisies = []
            self._Medecin__ordonnances_prescrites = []
            self.__numero_assure = numero_assure

        @property
        def numero_assure(self):
            return self.__numero_assure

        def __str__(self) -> str:
            return f"{self.identite} (médecin assuré, RPPS {self.numero_rpps})"

    dr_diallo_assure = MedecinAssure(identite="Dr Diallo", numero_rpps="RPPS-001", numero_assure="ASS-99999")
    print(f"{dr_diallo_assure} est aussi assuré sous le n°{dr_diallo_assure.numero_assure}")

    feuille = FeuilleMaladie(reference="FM-2026-001", patient=patient)
    dr_diallo.saisir_feuille_maladie(feuille)
    remboursement = org.traiter_feuille_maladie(feuille, montant_facture=50.0)
    print(remboursement)
    print(f"Médecin ayant saisi la feuille : {feuille.medecin}")

    ordonnance = OrdonnanceMedicament(patient=patient, medicaments=["Paracétamol", "Vitamine C"])
    dr_diallo.prescrire_medicament(ordonnance)
    print(ordonnance)
