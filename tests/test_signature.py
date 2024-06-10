import pytest
from app.signature import *
from app.key_generator import read_key_from_file

def test_sign():
    """
    This function tests the sign method.
    """
    # Arrange
    document = "test.txt"
    key = read_key_from_file("priv.bin","123")
    # Act
    sign(document, key)
    # Assert

    # Add more assertions as needed for specific requirements of the sign method

def test_verify():
    """
    This function tests the verify method.
    """
    # Arrange
    xml_signature = "test.txt.xml"
    public_key = read_key_from_file("pub.bin")
    # Act
    result = verify(xml_signature, public_key)
    # Assert
    assert result == True
    # Add more assertions as needed for specific requirements of the verify method