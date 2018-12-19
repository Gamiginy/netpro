import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy.orm import sessionmaker
import codecs

Base = sqlalchemy.ext.declarative.declarative_base()


class Word(Base):
    __tablename__ = 'words'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    english = sqlalchemy.Column(sqlalchemy.String)
    japanese = sqlalchemy.Column(sqlalchemy.String)
    part = sqlalchemy.Column(sqlalchemy.Integer)
    section = sqlalchemy.Column(sqlalchemy.Integer)
    part_section = sqlalchemy.Column(sqlalchemy.String)

    def __init__(self, id, en, jp, part, section, part_section):
        self.id = id
        self.english = en
        self.japanese = jp
        self.part = part
        self.section = section
        self.part_section = part_section


url = 'postgresql+psycopg2://masuda:hogehoge@localhost:5432/netpro'
engine = sqlalchemy.create_engine(url, echo=True)

# スキーマ作成
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def get_session():
    return session


def add_words():
    fin = codecs.open("words.txt", "r", "utf-8")
    counter = 1
    for line in fin:
        print(line)
        word = line.split(",")
        session.add(Word(counter, word[0], word[1], word[2], word[3], word[4]))
        counter += 1
    session.commit()
    fin.close()
