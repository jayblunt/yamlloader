import sys
import os
from sqlalchemy import Table

from yaml import load
try:
	from yaml import CSafeLoader as SafeLoader
except ImportError:
	from yaml import SafeLoader
	print("Using Python SafeLoader")


def importyaml(connection,metadata,sourcePath,language='en'):
    print("Importing Categories")
    invCategories = Table('invCategories',metadata)
    trnTranslations = Table('trnTranslations',metadata)
    
    trans = connection.begin()
    with open(os.path.join(sourcePath,'fsd','categoryIDs.yaml')) as yamlstream:
        print(f"importing {os.path.basename(yamlstream.name)}")
        categoryids=load(yamlstream,Loader=SafeLoader)
        print(f"{os.path.basename(yamlstream.name)} loaded")
        for categoryid in categoryids:
            connection.execute(invCategories.insert(),
                            categoryID=categoryid,
                            categoryName=categoryids[categoryid].get('name',{}).get(language,''),
                            iconID=categoryids[categoryid].get('iconID'),
                            published=categoryids[categoryid].get('published',0))
            
            if 'name' in categoryids[categoryid]:
                for lang in categoryids[categoryid]['name']:
                    try:
                        connection.execute(trnTranslations.insert(),tcID=6,keyID=categoryid,languageID=lang,text=categoryids[categoryid]['name'][lang])
                    except:                        
                        print(f'{categoryid} {lang} has a category problem')
    trans.commit()
