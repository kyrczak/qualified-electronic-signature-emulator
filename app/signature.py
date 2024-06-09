from xml.etree import ElementTree as ET
from datetime import datetime
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from xml.dom.minidom import parseString
import os

def sign(document, key):
    with open(document, 'r') as f:
        document_content = f.read()

    document_name = document.split('/')[-1]
    document_name = document_name.split('.')[0]
    document_extension = document.split('.')[-1]
    file_modification_time = datetime.fromtimestamp(os.path.getmtime(document)).isoformat()
    rsa_key = RSA.import_key(key)

    sigining_key = pkcs1_15.new(rsa_key)
    signature = sigining_key.sign(SHA256.new(document_content.encode('utf-8')))
    signature = signature.hex()
    
    root = ET.Element('Signature')
    doc_info = ET.SubElement(root, 'FileInfo')
    xml_document_name = ET.SubElement(doc_info, 'FileName')
    xml_document_name.text = document_name
    xml_document_extension = ET.SubElement(doc_info, 'FileExtension')
    xml_document_extension.text = document_extension
    xml_document_modification_time = ET.SubElement(doc_info, 'FileModificationTime')
    xml_document_modification_time.text = file_modification_time
    xml_user_info = ET.SubElement(root, 'UserInfo')
    xml_username = ET.SubElement(xml_user_info, 'Username')
    xml_username.text = os.getlogin()
    xml_signature = ET.SubElement(root, 'SignatureValue')
    xml_signature.text = signature
    xml_signature_timestamp = ET.SubElement(root, 'SignatureTimestamp')
    xml_signature_timestamp.text = datetime.now().isoformat()

    pretty_xml = parseString(ET.tostring(root)).toprettyxml()
    
    with open(document + '.xml', 'w') as f:
        f.write(pretty_xml)    

def verify(xml_signature, public_key):
    print(public_key)
    tree = ET.parse(xml_signature)
    root = tree.getroot()
    rsa_public_key = RSA.import_key(public_key)
    document_name = root.find('FileInfo/FileName').text
    document_extension = root.find('FileInfo/FileExtension').text
    signature = root.find('SignatureValue').text

    with open(document_name + '.' + document_extension, 'r') as f:
        document_content = f.read()

    try:
        pkcs1_15.new(rsa_public_key).verify(SHA256.new((document_content.encode('utf-8'))), bytes.fromhex(signature))
    except (ValueError, TypeError) as e:
        print(e)
        return False

    return True
