import pytest
from app.signature import *

def test_sign():
    # Create a sample document and key for testing
    document = "data/test.xml"
    key = "sample_key"

    # Call the sign method
    result = sign(document, key)

    # Assert that the result is not empty
    assert result is not None

    # Assert that the result is a string
    assert isinstance(result, str)

    # Assert that the result contains the expected signature
    assert "<Signature>" in result
    assert "<SignedInfo>" in result
    assert "<CanonicalizationMethod>" in result
    assert "<SignatureMethod>" in result
    assert "<Reference>" in result
    assert "<DigestMethod>" in result
    assert "<DigestValue>" in result
    assert "<SignatureValue>" in result
    assert "<KeyInfo>" in result

    # Add more assertions as needed for specific requirements of the sign method
