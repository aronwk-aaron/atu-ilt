# atu-ilt
Interior Least Tern Data Colletion Tool for Carice Godbey's ATU Master's Project

# Docker
Needs:
 * Vairables
    * APP_SECRET_KEY: SECRETE_KEY
    * SQLALCHEMY_DATABASE_URI: APP_DATABASE_URI
 * Ports
    * Expose container port 8000

# Notes

## Predator table
 * classification and type names should be switch
 Can't do it in the db cause that's not fun (probably can, but ugh)
 So if any tables are made straight from the db, threat the names inversely
