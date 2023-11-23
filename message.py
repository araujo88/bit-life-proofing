import requests
import datetime
import time
import gnupg
import hashlib
import json

class Message:
    def __init__(self, name: str, pgp_fingerprint: str, location: str, personal_statement: str, recent_event: str, purpose: str):
        self.name = name
        self.pgp_fingerprint = pgp_fingerprint
        self.location = location
        self.personal_statement = personal_statement
        self.recent_event = recent_event
        self.purpose = purpose
        self.timestamp = int(time.time())

    def generate_proof_of_life(self) -> dict:
        # Fetch the latest Bitcoin block number
        try:
            response = requests.get('https://blockchain.info/q/getblockcount')
            self.bitcoin_block_number = response.text
        except Exception as e:
            self.bitcoin_block_number = "Error fetching block number: " + str(e)

        # Construct the proof of life message
        proof_of_life_message = {
            "messageType": "Proof of Life",
            "author": {
                "name": self.name,
                "pgpFingerprint": self.pgp_fingerprint
            },
            "timestamp": self.timestamp,
            "location": self.location,
            "personalStatement": self.personal_statement,
            "recentEvent": self.recent_event,
            "additionalInfo": {
                "purpose": self.purpose,
                "bitcoinBlockNumber": self.bitcoin_block_number,
                "otherRelevantInfo": "Automatically generated message"
            }
        }

        return proof_of_life_message

    def sign_and_hash(self, gpg_home: str, passphrase: str) -> (str, str):
        gpg = gnupg.GPG(gnupghome=gpg_home)
        message = json.dumps(self.generate_proof_of_life(), sort_keys=True)

        # Extract long key ID from fingerprint
        long_key_id = self.pgp_fingerprint[-16:]

        # Sign the message
        signed_message = gpg.sign(message, keyid=long_key_id, passphrase=passphrase)

        # Hash the signed message
        message_hash = hashlib.sha256(str(signed_message).encode()).hexdigest()

        return str(signed_message), message_hash

    @staticmethod
    def verify_and_hash(signed_message: str) -> (bool, str):
        gpg = gnupg.GPG()

        # Verify the signed message
        verification = gpg.verify(signed_message)

        # Check if the signature is valid
        if verification:
            # Hash the signed message
            message_hash = hashlib.sha256(signed_message.encode()).hexdigest()
            return verification.valid, message_hash
        else:
            return False, None
