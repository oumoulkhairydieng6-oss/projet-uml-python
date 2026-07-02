"""
SUJET 5 : Gestion des masters, enseignants et cours
Hiérarchie d'héritage :
    Enseignant
        ├── Professeur          (titre HDR, peut diriger un Laboratoire)
        └── MaitreDeConferences (titre de thèse)

Classes complémentaires :
    - Laboratoire
    - Master                   (dirigé par un Enseignant)
    - Cours
    - AffiliationCoursMaster   (classe d'association Cours <-> Master, avec obligatoire/optionnel)

Relations principales :
    - Professeur "0..1" --(dirige)--> "0..1" Laboratoire
    - Master "1" --(directeur)--> "1" Enseignant
    - Master "1" --(0..*)--> AffiliationCoursMaster <--(0..*)-- "1" Cours
      (un cours obligatoire pour un master peut être optionnel dans un autre)

Scénarios de séquence implémentés :
    A) "Professeur et laboratoire" (assignation d'un directeur de labo)
    B) "Rattacher un cours à un master" (création d'une affiliation, avec règle d'unicité)
"""


# Classe : Enseignant
class Enseignant:
    """Un enseignant, identifié par son NUMEN (transmis par l'Éducation Nationale)."""

    def __init__(self, numen: str, nom: str, prenom: str):
        self.__numen = numen
        self.__nom = nom
        self.__prenom = prenom
        self.__masters_diriges = []  
    @property
    def numen(self) -> str:
        return self.__numen

    @property
    def nom(self) -> str:
        return self.__nom

    @property
    def prenom(self) -> str:
        return self.__prenom

    @property
    def masters_diriges(self) -> list:
        return list(self.__masters_diriges)

    def _ajouter_master_dirige(self, master: "Master") -> None:
        self.__masters_diriges.append(master)

    def __str__(self) -> str:
        return f"{self.__prenom} {self.__nom}"

    def __repr__(self) -> str:
        return f"Enseignant(numen={self.__numen!r}, nom={self.__nom!r}, prenom={self.__prenom!r})"


# Classe : Professeur
class Professeur(Enseignant):
    """Un professeur, titulaire d'une HDR, pouvant diriger un laboratoire."""

    def __init__(self, numen: str, nom: str, prenom: str, titre_hdr: str):
        super().__init__(numen, nom, prenom)
        self.__titre_hdr = titre_hdr
        self.__laboratoire_dirige = None  

    @property
    def titre_hdr(self) -> str:
        return self.__titre_hdr

    @property
    def laboratoire_dirige(self) -> "Laboratoire":
        return self.__laboratoire_dirige

    def assigner_laboratoire(self, laboratoire: "Laboratoire") -> None:
        """Scénario de séquence 'professeur et laboratoire' :
        le professeur devient directeur du laboratoire."""
        self.__laboratoire_dirige = laboratoire
        laboratoire._definir_directeur(self)

    def __str__(self) -> str:
        return f"Pr {super().__str__()} (HDR : {self.__titre_hdr})"


# Classe : MaitreDeConferences
class MaitreDeConferences(Enseignant):
    """Un maître de conférences, titulaire d'une thèse."""

    def __init__(self, numen: str, nom: str, prenom: str, titre_these: str):
        super().__init__(numen, nom, prenom)
        self.__titre_these = titre_these

    @property
    def titre_these(self) -> str:
        return self.__titre_these

    def __str__(self) -> str:
        return f"Dr {super().__str__()} (thèse : {self.__titre_these})"


# Classe : Laboratoire
class Laboratoire:
    """Un laboratoire de recherche, dirigé par un Professeur (0..1)."""

    def __init__(self, nom: str):
        self.__nom = nom
        self.__directeur = None  

    @property
    def nom(self) -> str:
        return self.__nom

    @property
    def directeur(self) -> Professeur:
        return self.__directeur

    def _definir_directeur(self, professeur: Professeur) -> None:
        self.__directeur = professeur

    def __str__(self) -> str:
        dir_str = self.__directeur.nom if self.__directeur else "aucun directeur"
        return f"Laboratoire {self.__nom} (directeur : {dir_str})"

    def __repr__(self) -> str:
        return f"Laboratoire(nom={self.__nom!r})"


# Classe : Master
class Master:
    """Un master, caractérisé par un nom et dirigé par un Enseignant."""

    def __init__(self, nom: str, directeur: Enseignant):
        self.__nom = nom
        self.__directeur = directeur
        self.__affiliations = []  
        directeur._ajouter_master_dirige(self)

    @property
    def nom(self) -> str:
        return self.__nom

    @property
    def directeur(self) -> Enseignant:
        return self.__directeur

    @property
    def affiliations(self) -> list:
        return list(self.__affiliations)

    def _ajouter_affiliation(self, affiliation: "AffiliationCoursMaster") -> None:
        self.__affiliations.append(affiliation)

    def cours_obligatoires(self) -> list:
        return [aff.cours for aff in self.__affiliations if aff.obligatoire]

    def cours_optionnels(self) -> list:
        return [aff.cours for aff in self.__affiliations if not aff.obligatoire]

    def __str__(self) -> str:
        return f"Master {self.__nom} (dirigé par {self.__directeur})"

    def __repr__(self) -> str:
        return f"Master(nom={self.__nom!r})"


# Classe : Cours
class Cours:
    """Un cours, caractérisé par un intitulé, pouvant être obligatoire dans un
    Master et optionnel dans un ou plusieurs autres Masters."""

    def __init__(self, intitule: str):
        self.__intitule = intitule
        self.__affiliations = []  

    @property
    def intitule(self) -> str:
        return self.__intitule

    @property
    def affiliations(self) -> list:
        return list(self.__affiliations)

    def _ajouter_affiliation(self, affiliation: "AffiliationCoursMaster") -> None:
        self.__affiliations.append(affiliation)

    def masters_ou_il_est_obligatoire(self) -> list:
        return [aff.master for aff in self.__affiliations if aff.obligatoire]

    def __str__(self) -> str:
        return f"Cours « {self.__intitule} »"

    def __repr__(self) -> str:
        return f"Cours(intitule={self.__intitule!r})"


# Classe d'association : AffiliationCoursMaster
class AffiliationCoursMaster:
    """Association Cours <-> Master : précise si le cours est obligatoire ou
    optionnel pour ce master donné. Un même cours peut être obligatoire dans
    un master et optionnel dans un autre."""

    def __init__(self, cours: Cours, master: Master, obligatoire: bool):
        self.__verifier_unicite(cours, master)
        self.__cours = cours
        self.__master = master
        self.__obligatoire = obligatoire

        cours._ajouter_affiliation(self)
        master._ajouter_affiliation(self)

    @staticmethod
    def __verifier_unicite(cours: Cours, master: Master) -> None:
        """Un cours ne peut être rattaché qu'une seule fois à un même master."""
        for affiliation in cours.affiliations:
            if affiliation.master is master:
                raise ValueError(
                    f"{cours} est déjà rattaché au master '{master.nom}'."
                )

    @property
    def cours(self) -> Cours:
        return self.__cours

    @property
    def master(self) -> Master:
        return self.__master

    @property
    def obligatoire(self) -> bool:
        return self.__obligatoire

    def __str__(self) -> str:
        statut = "obligatoire" if self.__obligatoire else "optionnel"
        return f"{self.__cours} {statut} pour {self.__master.nom}"

    def __repr__(self) -> str:
        return f"AffiliationCoursMaster(cours={self.__cours.intitule!r}, master={self.__master.nom!r}, obligatoire={self.__obligatoire!r})"


if __name__ == "__main__":
    pr_gueye = Professeur(numen="NUM001", nom="Gueye", prenom="Mamadou", titre_hdr="HDR Informatique")
    mc_diop = MaitreDeConferences(numen="NUM002", nom="Diop", prenom="Aïssatou", titre_these="Thèse en IA")

    labo = Laboratoire(nom="LIA - Laboratoire d'Intelligence Artificielle")
    pr_gueye.assigner_laboratoire(labo)
    print(labo)

    master_info = Master(nom="MIAGE-IF", directeur=pr_gueye)
    master_data = Master(nom="Data Science", directeur=mc_diop)

    cours_poo = Cours(intitule="Programmation Orientée Objet")
    cours_uml = Cours(intitule="Modélisation UML")

    AffiliationCoursMaster(cours=cours_poo, master=master_info, obligatoire=True)
    AffiliationCoursMaster(cours=cours_poo, master=master_data, obligatoire=False)  # optionnel ailleurs
    AffiliationCoursMaster(cours=cours_uml, master=master_info, obligatoire=True)

    try:
        AffiliationCoursMaster(cours=cours_poo, master=master_info, obligatoire=False)
    except ValueError as e:
        print(f"Erreur attendue (doublon) : {e}")

    print()
    for enseignant in (pr_gueye, mc_diop):
        print(enseignant)

    print()
    print(master_info, "- cours obligatoires :", [c.intitule for c in master_info.cours_obligatoires()])
    print(master_data, "- cours optionnels :", [c.intitule for c in master_data.cours_optionnels()])

    print()
    print(f"'{cours_poo.intitule}' est obligatoire dans : "
          f"{[m.nom for m in cours_poo.masters_ou_il_est_obligatoire()]}")
