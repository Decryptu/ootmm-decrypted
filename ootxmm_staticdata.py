import pkgutil
import json

OOTxMMRegionData = json.loads((pkgutil.get_data(__name__, 'raw/GreatWorldJSONdump.json')).decode('utf-8'))
OOTxMMLocationIDs = json.loads((pkgutil.get_data(__name__, 'raw/LocationIDs.json')).decode('utf-8'))
OOTxMMItemData = json.loads((pkgutil.get_data(__name__, 'raw/GreatItemJSONdump.json')).decode('utf-8'))
OOTxMMItemIDs = json.loads((pkgutil.get_data(__name__, 'raw/ItemIDs.json')).decode('utf-8'))
OOTxMMCheckItems = json.loads((pkgutil.get_data(__name__, 'raw/GreatCheckItemJSONdump.json')).decode('utf-8'))
OOTxMMLogic = json.loads((pkgutil.get_data(__name__, 'raw/GreatLogicJSONdump.json')).decode('utf-8'))
