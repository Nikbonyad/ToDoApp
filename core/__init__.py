from decouple import config

DB_ENGINE = config('DB_ENGINE', default='sqlite')

if DB_ENGINE == 'mysql':
    import pymysql
    pymysql.install_as_MySQLdb()
