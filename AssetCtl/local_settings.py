DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',#'django.db.backends.sqlite3', #postgres sql db engine
        'NAME': 'hetal_db', #database name
        'USER': 'asset_user' ,#user name
        'PASSWORD': 'coldfeet1!',#password  coldfeet1!
        'HOST': 'assetmgmt.postgres.database.azure.com',
    }
}

ALLOWED_HOSTS = []