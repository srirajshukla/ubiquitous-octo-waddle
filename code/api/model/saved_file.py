import repository.db as db

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, update
from sqlalchemy.orm import relationship


class SavedFile(db.Base):
    __tablename__ = "SavedFile"
    id = Column(Integer, primary_key=True)
    year = Column(String)
    filename = Column(String)
    url = Column(String)
    embed_status = Column(String, default="In Progress")
    type = Column(String)
    user = Column(String)
    trackerid = Column(String)


from sqlalchemy.orm import Session


def create_savedfile(db: Session, year, filename, url, type, user, trackerid):
    db_savedfile = SavedFile(
        year=year, filename=filename, url=url, type=type, user=user, trackerid=trackerid
    )
    db.add(db_savedfile)
    db.commit()
    db.refresh(db_savedfile)
    return db_savedfile


def get_savedfile(db: Session, year, user):
    return (
        db.query(SavedFile).filter(SavedFile.year == year, SavedFile.user == user).all()
    )

def get_taskid_status(db: Session, taskid, user, year):
    return db.query(SavedFile).filter(SavedFile.user == user, SavedFile.trackerid==taskid, SavedFile.year == year).first()


def get_allfiles(db: Session, user):
    return db.query(SavedFile).filter(SavedFile.user == user).all()


def update_savedfile(db: Session, filename, user, year, trackerid, embed_status):
    savedfile = db.query(SavedFile).filter(SavedFile.user == user, SavedFile.year == year, SavedFile.filename==filename, SavedFile.trackerid==trackerid).first()
    savedfile.embed_status = embed_status
    db.add(savedfile)
    db.commit()
    db.refresh(savedfile)
    return savedfile


def get_all_years(db: Session, user):
    years = db.query(SavedFile.year).filter(SavedFile.user == user).distinct().all()
    print(years)
    ans = []
    for year in years:
        ans.append(year[1])
    return ans