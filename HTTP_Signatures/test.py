from hashlib import sha256

import base64
import json

data="""{
    "instructedAmount": {"currency": "EUR", "amount": "123.50"},
    "debtorAccount": {"iban": "DE40100100103307118608"},
    "creditorName": "Merchant123",
    "creditorAccount": {"iban": "DE02100100109307118603"},
    "remittanceInformationUnstructured": "Ref Number Merchant"
    }"""

#json_data=json.dumps(data)

#digest=base64.b64encode(sha256(json_data.encode('utf-8')).digest())

digest=base64.b64encode(sha256(data.encode('utf-8')).digest())
print(digest.decode('utf-8'))