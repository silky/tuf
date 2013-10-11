"""
<Program Name>
  test_ed25519_keys.py

<Author> 
  Vladimir Diaz 

<Started>
  October 11, 2013. 

<Copyright>
  See LICENSE for licensing information.

<Purpose>
  Test cases for test_ed25519_keys.py.
"""

import unittest
import logging

import tuf
import tuf.log
import tuf.formats
import tuf.ed25519_keys as ed25519 

logger = logging.getLogger('tuf.test_ed25519_keys')

public, private = ed25519.generate_public_and_private()
FORMAT_ERROR_MSG = 'tuf.FormatError raised.  Check object\'s format.'


class TestEd25519_keys(unittest.TestCase):
  def setUp(self):
    pass


  def test_generate_public_and_private(self):
    pub, priv = ed25519.generate_public_and_private()
    
    # Check format of 'pub' and 'priv'.
    self.assertEqual(True, tuf.formats.ED25519PUBLIC_SCHEMA.matches(pub))
    self.assertEqual(True, tuf.formats.ED25519SEED_SCHEMA.matches(priv))

    # Check for invalid argument.
    self.assertRaises(tuf.FormatError,
                      ed25519.generate_public_and_private, 'True')
    
    self.assertRaises(tuf.FormatError,
                      ed25519.generate_public_and_private, 2048)
    

  def test_create_signature(self):
    global public
    global private
    data = 'The quick brown fox jumps over the lazy dog'
    signature, method = ed25519.create_signature(public, private, data)

    # Verify format of returned values.
    self.assertEqual(True,
                     tuf.formats.ED25519SIGNATURE_SCHEMA.matches(signature))
    
    self.assertEqual(True, tuf.formats.NAME_SCHEMA.matches(method))
    self.assertEqual('ed25519-python', method)

    # Check for improperly formatted argument.
    self.assertRaises(tuf.FormatError,
                      ed25519.create_signature, 123, private, data)
    
    self.assertRaises(tuf.FormatError,
                      ed25519.create_signature, public, 123, data)
   
    # Check for invalid 'data'.
    self.assertRaises(tuf.CryptoError,
                      ed25519.create_signature, public, private, 123)


  def test_verify_signature(self):
    global public
    global private
    data = 'The quick brown fox jumps over the lazy dog'
    signature, method = ed25519.create_signature(public, private, data)

    valid_signature = ed25519.verify_signature(public, method, signature, data)
    self.assertEqual(True, valid_signature)

    # Check for improperly formatted arguments.
    self.assertRaises(tuf.FormatError, ed25519.verify_signature, 123, method,
                                       signature, data)
    
    self.assertRaises(tuf.FormatError, ed25519.verify_signature, public, 123,
                                       signature, data)
    
    self.assertRaises(tuf.FormatError, ed25519.verify_signature, method,
                                       '123', data)
    
    
    # Check for invalid signature and data.
    self.assertRaises(tuf.CryptoError, ed25519.verify_signature, public, method,
                                       public_rsa, data)
    
    self.assertRaises(tuf.CryptoError, ed25519.verify_signature, signature,
                                       method, public_rsa, 123)
    
    self.assertEqual(False, ed25519.verify_signature(public, method, signature,
                                                     'mismatched data'))

    mismatched_signature, method = ed25519.create_signature(private_rsa,
                                                             'mismatched data')
    
    self.assertEqual(False, ed25519.verify_signature(mismatched_signature,
                            method, public_rsa, data))



# Run the unit tests.
if __name__ == '__main__':
  unittest.main()