from src import db


class Gene(db.Model):
    __tablename__ = 'gene_autocomplete'

    stable_id = db.Column(db.String(128), primary_key=True)
    species = db.Column(db.String(255))
    display_label = db.Column(db.String(128))
    location = db.Column(db.String(60))
    db = db.Column(db.String(32), default="core", nullable=False)

    def __init__(self, stable_id, species, display_label, location, db=None):
        self.stable_id = stable_id
        self.species = species
        self.display_label = display_label
        self.location = location
        self.db = db
