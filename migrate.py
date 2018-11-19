import peewee
from playhouse.migrate import migrate
from models import Anime, Episodios, db, migrator


try:
    selecao = peewee.BooleanField(default=True)
    migrate(
        migrator.add_column('anime', 'selecao', selecao)
    )
except peewee.OperationalError:
    pass

try:
    migrate(
        #migrator.drop_column('episodios', 'nome')
        migrator.drop_column('episodios', 'video')
    )
except peewee.OperationalError:
    pass

if __name__ == '__main__':
    try:
        Anime.create_table()
    except peewee.OperationalError:
        print('Tabela Anime já existe.')

    try:
        Episodios.create_table()
    except peewee.OperationalError:
        print('Tabela Episodios já existe.')
