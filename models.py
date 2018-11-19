import peewee
from playhouse.migrate import SqliteMigrator


db = peewee.SqliteDatabase('anime.db')
migrator = SqliteMigrator(db)


class baseModel(peewee.Model):
    class Meta:
        database = db


class Anime(baseModel):
    nome = peewee.CharField()
    genero = peewee.CharField()
    numeroEpisodio = peewee.DecimalField(max_digits=5, decimal_places=0)
    imagem = peewee.CharField()
    link = peewee.CharField()
    status = peewee.DecimalField(max_digits=1, decimal_places=0)


class Episodios(baseModel):
    anime = peewee.ForeignKeyField(Anime)
    nome = peewee.CharField()
    episodio = peewee.CharField()
    link = peewee.CharField()
    video = peewee.CharField()
