
import os
class Config:
    '''
    General configuration parent class
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY')  
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    API_BASE_URL='http://quotes.stormconsultancy.co.uk/random.json'



class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass


class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://khalyz:1234@localhost/log'
    
    
config_options = {
    'development':DevConfig,
    'production':ProdConfig
}