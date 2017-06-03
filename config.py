import os
    
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'postgres://tmfykgvqcxxiiy:b35d2c8219898eb3558d41f5f335142f55f74a39404edc57fc6b3c7061da843f@ec2-23-21-169-238.compute-1.amazonaws.com:5432/d64fq3p9ro085j'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False