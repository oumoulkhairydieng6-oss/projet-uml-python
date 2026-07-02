"""
SUJET 3 : Gestion de revues et d'articles
============================================
Implémentation Python (POO) fidèle au diagramme de classes UML.

Classes du diagramme :
    - Auteur
    - Revue                  (a un rédacteur en chef = un Auteur)
    - Numero                 (numéro relatif à la revue + à l'année)
    - Article
    - Parution                (classe d'association Article <-> Numero)
    - ContratAuteurRevue      (classe d'association Auteur <-> Revue : l'auteur est "engagé")

Relations principales :
    - Revue "1" --(publie)--> "1..*" Numero                       (composition)
    - Numero "1" --(contient)--> "0..*" Parution                   (composition)
    - Article "1" --(parait dans)--> "1..*" Parution                (composition côté Numero,
      mais un même article peut apparaître dans plusieurs revues -> plusieurs Numero/Parution)
    - Revue "1" --(emploie via)--> "0..*" ContratAuteurRevue
    - Auteur "1" --(engagé par)--> "0..*" ContratAuteurRevue
    - Revue --(rédacteur en chef)--> Auteur (1..1, doit être un auteur engagé par la revue)

Scénarios de séquence implémentés :
    A) "Publier un article dans un numéro" (création Parution + contrainte anti-doublon)
    B) "Auteurs du numéro 3 d'une revue, année 2010" (requête de consultation)
"""


# Classe : Auteur
class Auteur:
    """Un auteur, identifié par son numéro de carte professionnelle."""

    def __init__(self, nom: str, prenom: str, numero_carte_pro: str):
        self.__nom = nom
        self.__prenom = prenom
        self.__numero_carte_pro = numero_carte_pro
        self.__contrats = []  

    @property
    def nom(self) -> str:
        return self.__nom

    @property
    def prenom(self) -> str:
        return self.__prenom

    @property
    def numero_carte_pro(self) -> str:
        return self.__numero_carte_pro

    @property
    def contrats(self) -> list:
        return list(self.__contrats)

    def _ajouter_contrat(self, contrat: "ContratAuteurRevue") -> None:
        self.__contrats.append(contrat)

    def est_engage_par(self, revue: "Revue") -> bool:
        return any(c.revue is revue for c in self.__contrats)

    def __str__(self) -> str:
        return f"{self.__prenom} {self.__nom}"

    def __repr__(self) -> str:
        return f"Auteur(nom={self.__nom!r}, prenom={self.__prenom!r}, carte={self.__numero_carte_pro!r})"


# Classe : Revue
class Revue:
    """Une revue, caractérisée par un nom, avec un rédacteur en chef (un Auteur
    engagé par cette revue) et publiant des numéros."""

    def __init__(self, nom: str):
        self.__nom = nom
        self.__redacteur_en_chef = None
        self.__numeros = []        
        self.__contrats = []       

    @property
    def nom(self) -> str:
        return self.__nom

    @property
    def redacteur_en_chef(self) -> Auteur:
        return self.__redacteur_en_chef

    @property
    def numeros(self) -> list:
        return list(self.__numeros)

    @property
    def auteurs_engages(self) -> list:
        return [c.auteur for c in self.__contrats]

    def engager_auteur(self, auteur: Auteur) -> "ContratAuteurRevue":
        """Engage un auteur pour cette revue (crée le contrat d'association)."""
        contrat = ContratAuteurRevue(auteur=auteur, revue=self)
        return contrat

    def _ajouter_contrat(self, contrat: "ContratAuteurRevue") -> None:
        self.__contrats.append(contrat)

    def definir_redacteur_en_chef(self, auteur: Auteur) -> None:
        """Le rédacteur en chef d'une revue doit être un auteur employé par la revue."""
        if not auteur.est_engage_par(self):
            raise ValueError(
                f"{auteur} doit d'abord être engagé par la revue '{self.__nom}' "
                "avant de pouvoir en être le rédacteur en chef."
            )
        self.__redacteur_en_chef = auteur

    def _ajouter_numero(self, numero: "Numero") -> None:
        self.__numeros.append(numero)

    def nb_numeros_parus_en(self, annee: int) -> int:
        """Répond à : 'Combien de numéros de la revue sont parus en <année> ?'"""
        return sum(1 for n in self.__numeros if n.annee == annee)

    def __str__(self) -> str:
        return f"Revue {self.__nom}"

    def __repr__(self) -> str:
        return f"Revue(nom={self.__nom!r})"


# Classe d'association : ContratAuteurRevue
class ContratAuteurRevue:
    """Association Auteur <-> Revue : un auteur est engagé par une revue
    (un auteur peut être engagé par une seule revue, mais écrire dans plusieurs)."""

    def __init__(self, auteur: Auteur, revue: Revue):
        self.__auteur = auteur
        self.__revue = revue
        self.__auteur._ajouter_contrat(self)
        self.__revue._ajouter_contrat(self)

    @property
    def auteur(self) -> Auteur:
        return self.__auteur

    @property
    def revue(self) -> Revue:
        return self.__revue

    def __str__(self) -> str:
        return f"{self.__auteur} engagé par {self.__revue}"

    def __repr__(self) -> str:
        return f"ContratAuteurRevue(auteur={self.__auteur.nom!r}, revue={self.__revue.nom!r})"


# Classe : Numero
class Numero:
    """Un numéro de revue, identifié par un numéro relatif et une année
    (ex. le n°12 de Linux Magazine en 2009 != le n°12 en 2010)."""

    def __init__(self, revue: Revue, numero_relatif: int, annee: int):
        self.__revue = revue
        self.__numero_relatif = numero_relatif
        self.__annee = annee
        self.__parutions = []  
        self.__revue._ajouter_numero(self)

    @property
    def revue(self) -> Revue:
        return self.__revue

    @property
    def numero_relatif(self) -> int:
        return self.__numero_relatif

    @property
    def annee(self) -> int:
        return self.__annee

    @property
    def parutions(self) -> list:
        return list(self.__parutions)

    def _ajouter_parution(self, parution: "Parution") -> None:
        self.__parutions.append(parution)

    def auteurs_des_articles(self) -> set:
        """Requête : ensemble des auteurs ayant publié dans ce numéro."""
        auteurs = set()
        for parution in self.__parutions:
            auteurs.update(parution.article.auteurs)
        return auteurs

    def __str__(self) -> str:
        return f"N°{self.__numero_relatif} de {self.__revue.nom} ({self.__annee})"

    def __repr__(self) -> str:
        return f"Numero(revue={self.__revue.nom!r}, numero_relatif={self.__numero_relatif!r}, annee={self.__annee!r})"


# Classe : Article
class Article:
    """Un article, écrit par un ou plusieurs auteurs, pouvant apparaître dans
    plusieurs revues différentes (mais jamais 2 fois dans la même revue)."""

    def __init__(self, titre: str, contenu: str, auteurs: list):
        self.__titre = titre
        self.__contenu = contenu
        self.__auteurs = list(auteurs)  
        self.__parutions = []           

    @property
    def titre(self) -> str:
        return self.__titre

    @property
    def contenu(self) -> str:
        return self.__contenu

    @property
    def auteurs(self) -> list:
        return list(self.__auteurs)

    @property
    def parutions(self) -> list:
        return list(self.__parutions)

    def _ajouter_parution(self, parution: "Parution") -> None:
        self.__parutions.append(parution)

    def revues_de_parution(self) -> set:
        """Les différentes revues dans lesquelles cet article est paru."""
        return {p.numero.revue for p in self.__parutions}

    def __str__(self) -> str:
        return f"« {self.__titre} »"

    def __repr__(self) -> str:
        return f"Article(titre={self.__titre!r})"


# Classe d'association : Parution
class Parution:
    """Association Article <-> Numero : place un article dans un numéro précis
    d'une revue. Contrainte : un article ne peut paraître qu'une fois dans
    les différents numéros d'une même revue."""

    def __init__(self, article: Article, numero: Numero):
        self.__verifier_pas_de_doublon(article, numero)
        self.__article = article
        self.__numero = numero
        self.__article._ajouter_parution(self)
        self.__numero._ajouter_parution(self)

    @staticmethod
    def __verifier_pas_de_doublon(article: Article, numero: Numero) -> None:
        """Un même article ne doit jamais apparaître 2 fois dans la même revue."""
        revue_cible = numero.revue
        for parution_existante in article.parutions:
            if parution_existante.numero.revue is revue_cible:
                raise ValueError(
                    f"{article} est déjà paru dans la revue '{revue_cible.nom}' "
                    f"(numéro {parution_existante.numero.numero_relatif})."
                )

    @property
    def article(self) -> Article:
        return self.__article

    @property
    def numero(self) -> Numero:
        return self.__numero

    def __str__(self) -> str:
        return f"{self.__article} paru dans {self.__numero}"

    def __repr__(self) -> str:
        return f"Parution(article={self.__article.titre!r}, numero={self.__numero!r})"


# Service de requêtes
class ServiceRequetes:
    """Requêtes de consultation transverses, illustrant le scénario de séquence
    'auteurs du numéro 3 de la revue X, année 2010'."""

    @staticmethod
    def auteurs_du_numero(revue: Revue, annee: int, numero_relatif: int) -> list:
        for numero in revue.numeros:
            if numero.annee == annee and numero.numero_relatif == numero_relatif:
                return sorted(str(a) for a in numero.auteurs_des_articles())
        return []

    @staticmethod
    def titres_articles_parus_dans_au_moins_deux_revues(articles: list) -> list:
        return [a.titre for a in articles if len(a.revues_de_parution()) >= 2]


# Programme principal de test
if __name__ == "__main__":
    auteur1 = Auteur(nom="Mbaye", prenom="Cheikh", numero_carte_pro="CP-001")
    auteur2 = Auteur(nom="Sow", prenom="Fatou", numero_carte_pro="CP-002")

    linux_mag = Revue(nom="Linux Magazine")
    linux_mag.engager_auteur(auteur1)
    linux_mag.engager_auteur(auteur2)
    linux_mag.definir_redacteur_en_chef(auteur1)

    histoire = Revue(nom="L'Histoire")
    histoire.engager_auteur(auteur2)

    numero3_linux = Numero(revue=linux_mag, numero_relatif=3, annee=2010)
    numero12_linux_2010 = Numero(revue=linux_mag, numero_relatif=12, annee=2010)
    numero3_histoire = Numero(revue=histoire, numero_relatif=3, annee=2010)

    article_python = Article(titre="Python en pratique", contenu="...", auteurs=[auteur1])
    Parution(article=article_python, numero=numero3_linux)

    article_histoire = Article(titre="La chute de l'Empire", contenu="...", auteurs=[auteur2])
    Parution(article=article_histoire, numero=numero3_histoire)

    article_partage = Article(titre="Découvertes croisées", contenu="...", auteurs=[auteur1, auteur2])
    Parution(article=article_partage, numero=numero12_linux_2010)
    Parution(article=article_partage, numero=numero3_histoire)  

    try:
        Parution(article=article_python, numero=numero12_linux_2010)  
    except ValueError as e:
        print(f"Erreur attendue (doublon) : {e}")

    print()
    print(f"Numéros de Linux Magazine parus en 2010 : {linux_mag.nb_numeros_parus_en(2010)}")
    print(f"Auteurs du n°3 de L'Histoire (2010) : "
          f"{ServiceRequetes.auteurs_du_numero(histoire, 2010, 3)}")
    print(f"Articles parus dans au moins 2 revues différentes : "
          f"{ServiceRequetes.titres_articles_parus_dans_au_moins_deux_revues([article_python, article_histoire, article_partage])}")
