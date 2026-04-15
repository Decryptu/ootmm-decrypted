import pkgutil
import json

OOTxMMRegionData = json.loads((pkgutil.get_data(__name__, 'raw/GreatWorldJSONdump.json')).decode('utf-8'))
OOTxMMMacroData = json.loads((pkgutil.get_data(__name__, 'raw/GreatMacroJSONdump.json')).decode('utf-8'))