postgresql = {'host': '127.0.0.1',
         'user': 'postgres',
         'passwd': 'postgres',
         'db': 'flask_db'}

postgresqlConfig = "postgresql+psycopg2://{}:{}@{}/{}".format(postgresql['user'], postgresql['passwd'], postgresql['host'], postgresql['db'])