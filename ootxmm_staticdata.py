import pkgutil
import json

OOTxMMRegionData = json.loads((pkgutil.get_data(__name__, 'raw/GreatWorldJSONdump.json')).decode('utf-8'))
OOTxMMMacroData = json.loads((pkgutil.get_data(__name__, 'raw/GreatMacroJSONdump.json')).decode('utf-8'))
OOTxMMLocationIDs = json.loads((pkgutil.get_data(__name__, 'raw/LocationIDs.json')).decode('utf-8'))
OOTxMMItemData = json.loads((pkgutil.get_data(__name__, 'raw/GreatItemJSONdump.json')).decode('utf-8'))
OOTxMMItemIDs = json.loads((pkgutil.get_data(__name__, 'raw/ItemIDs.json')).decode('utf-8'))
