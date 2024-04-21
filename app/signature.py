import xmlsig
from xmlsig import algorithms
from xml.etree import ElementTree as ET
from datetime import datetime
import hashlib
import xades

def sign(document, key):
    with open(document, 'r') as f:
        document_content = f.read()
    
    hash_algorithm = hashlib.sha256()  # You can choose the hash algorithm according to your requirements
    hash_algorithm.update(document_content.encode())
    document_hash = hash_algorithm.digest()

    timestamp = datetime.now().isoformat()

    root = ET.Element('XAdESSignature')
    document_info = ET.SubElement(root, 'DocumentInfo')

    ET.SubElement(document_info, 'Size').text = str(len(document_content))
    ET.SubElement(document_info, 'Extension').text = document.split('.')[-1]
    ET.SubElement(document_info, 'DateOfModification').text = timestamp
    ET.SubElement(root, 'SigningUser').text = 'User A'
    ET.SubElement(root, 'EncryptedHash').text = str(document_hash)
    ET.SubElement(root, 'Timestamp').text = timestamp

    xml_signature = ET.tostring(root,encoding='utf-8')

    signature = xmlsig.Xades(
        key = key,
        data = xml_signature,
        signed_info_params={
            'canonicalization_method': algorithms.C14N_EXCLUSIVE,
            'signature_method': algorithms.RSA_SHA256,
            'digest_method': algorithms.SHA256
        },
        key_info=xmlsig.KeyInfo(include_x509_data=True)
    )

    signed_document = signature.sign()

    with open(f'signed_{document.split('.')[0]}.xml', 'wb') as f:
        f.write(signed_document)

