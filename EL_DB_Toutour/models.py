from sqlalchemy import Column, Integer, String, Float, Date, LargeBinary, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base


class Dog(Base):
    __tablename__ = "dogs"  # nom de la table en minuscules et pluriel

    dog_id = Column(String(100), primary_key=True)                      # identifiant unique du chien
    chip_id = Column(String(100), unique=True, nullable=False)          # numéro de puce
    owner_id = Column(String(100), nullable=False)                      # identifiant du propriétaire
    name = Column(String(100), nullable=False)                          # nom du chien
    weight = Column(Integer)                                            # poids en kg
    breed = Column(String(50))                                          # race du chien
    picture = Column(String(100))                                       # path vers la photo
    birth_date = Column(Date)                                           # date de naissance
    optimal_tour_duration = Column(Integer)                             # durée promenade en minutes
    athleticism = Column(Integer)                                       # score de sportivité de 0 à 10


class Owner(Base):
    __tablename__ = "owners"

    owner_id = Column(String(100), primary_key=True)                    # unique ID
    last_name = Column(String(100), nullable=False)                     # nom
    first_name = Column(String(100), nullable=False)                    # prénom
    email = Column(String(150), nullable=False)            # email
    phone = Column(String(20))                                          # numéro de téléphone
    picture = Column(String(100))                                       # path vers la photo
    bio = Column(Text)                                                  # biographie / description


class Walker(Base):
    __tablename__ = "walkers"

    walker_id = Column(String(100), primary_key=True)                   # identifiant unique
    last_name = Column(String(100), nullable=False)                     # nom
    first_name = Column(String(100), nullable=False)                    # prénom
    picture = Column(String(100))                                       # path vers la photo
    bio = Column(Text)                                                  # biographie / description
    verified_profile = Column(Boolean, default=False)                   # profil vérifié
    email = Column(String(150), nullable=False)            # mail
    phone = Column(String(20))                                          # numéro de téléphone
    birth_date = Column(Date)                                           # date de naissance
    rib = Column(String(34))                                            # numéro RIB (IBAN français)


class WalkerAvailability(Base):
    __tablename__ = "walker_availabilities"

    availability_id = Column(String(100), primary_key=True)             # identifiant unique de la dispo
    walker_id = Column(String(100), ForeignKey("walkers.walker_id"), nullable=False)  # lien vers le promeneur
    address = Column(String(255), nullable=False)                             # adresse de disponibilité
    start_datetime = Column(DateTime, nullable=False)                         # début de la disponibilité
    end_datetime = Column(DateTime, nullable=False)                           # fin de la disponibilité

    # Relation SQLAlchemy pour accéder au promeneur
    walker = relationship("Walker", back_populates="availabilities")


class WalkRequest(Base):
    __tablename__ = "walk_requests"

    walk_id = Column(String(100), primary_key=True)  # identifiant unique de la demande
    dog_id = Column(String(100), ForeignKey("dogs.dog_id"), nullable=False)      # lien vers le chien
    address = Column(String(255), nullable=False)                             # adresse de la promenade
    ideal_start_datetime = Column(DateTime, nullable=False)                   # début idéal
    duration_request = Column(Integer, nullable=True)                            # durée souhaitée (en minutes), optionnelle
    distance_request = Column(Float, nullable=True)                            # distance souhaitée (en km), optionnelle
    favorite_walker_id = Column(String(100), ForeignKey("walkers.walker_id"), nullable=True)  # optionnel
    predicted_payment = Column(Float, nullable=True)                           # rémunération prédite, calculée automatiquement

    # Relations SQLAlchemy
    dog = relationship("Dog", back_populates="walk_requests")
    favorite_walker = relationship("Walker")


class PastWalk(Base):
    __tablename__ = "past_walks"

    walk_id = Column(String(100), primary_key=True)             # identifiant unique de la promenade
    dog_id = Column(String(100), ForeignKey("dogs.dog_id"), nullable=False)         # lien vers le chien
    walker_id = Column(String(100), ForeignKey("walkers.walker_id"), nullable=False) # lien vers le promeneur
    distance = Column(Float)                                                     # distance parcourue (en km)
    start_datetime = Column(DateTime)                                           # début de la promenade
    end_datetime = Column(DateTime)                                             # fin de la promenade
    picture = Column(String(100))                                       # path vers la photo
    dog_review_id = Column(String(100), nullable=True)                               # avis du chien (facultatif)
    walker_review_id = Column(String(100), nullable=True)                            # avis du promeneur (facultatif)

    # Relations SQLAlchemy
    dog = relationship("Dog", back_populates="past_walks")
    walker = relationship("Walker", back_populates="past_walks")


class WalkerReview(Base):
    __tablename__ = "walker_reviews"

    review_id = Column(String(100), primary_key=True)                           # identifiant unique de l'avis
    walk_id = Column(String(100), ForeignKey("past_walks.walk_id"), nullable=False) # lien vers la promenade passée
    walker_id = Column(String(100), ForeignKey("walkers.walker_id"), nullable=False) # lien vers le promeneur évalué
    rating = Column(Float, nullable=False)                                     # note (ex: 1 à 5)
    comment = Column(Text, nullable=True)                               # commentaire optionnel

    # Relations SQLAlchemy
    walker = relationship("Walker", back_populates="reviews")
    walk = relationship("PastWalk", back_populates="walker_reviews")
    

class DogReview(Base):
    __tablename__ = "dog_reviews"

    review_id = Column(String(100), primary_key=True)         # identifiant unique de l'avis
    walk_id = Column(String(100), ForeignKey("past_walks.walk_id"), nullable=False) # lien vers la promenade passée
    dog_id = Column(String(100), ForeignKey("dogs.dog_id"), nullable=False)        # lien vers le chien évalué
    rating = Column(Float, nullable=False)                                     # note attribuée au chien
    comment = Column(Text, nullable=True)                               # commentaire optionnel

    # Relations SQLAlchemy
    dog = relationship("Dog", back_populates="reviews")
    walk = relationship("PastWalk", back_populates="dog_reviews")


class OwnerPayment(Base):
    __tablename__ = "owner_payments"

    payment_id = Column(String(100), primary_key=True)        # identifiant unique du paiement
    walk_id = Column(String(100), ForeignKey("past_walks.walk_id"), nullable=False) # lien vers la promenade passée
    amount = Column(Float, nullable=False)                                     # montant calculé automatiquement
    payment_datetime = Column(DateTime, nullable=False)                        # date et heure du paiement
    payment_method = Column(String(50), nullable=False)                        # moyen de paiement (ex: "card", "paypal")
    payment_status = Column(String(50), default="pending", nullable=False)     # statut du paiement (ex: "pending", "completed", "failed")

    # Relation SQLAlchemy
    walk = relationship("PastWalk", back_populates="owner_payment")