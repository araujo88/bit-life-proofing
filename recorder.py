from bitcoinlib.wallets import Wallet, WalletError
from bitcoinlib.transactions import Transaction
from bitcoinlib.services.services import Service
import schedule
from datetime import datetime, timedelta
from message import Message

class Recorder:
    def __init__(self,
                 pgp_fingerprint: str,
                 gpg_passphrase: str,
                 gpg_home=None,
                 wallet_name='MyTestnetWallet', 
                 check_in_interval='1 day'):
        self.pgp_fingerprint = pgp_fingerprint
        self.gpg_home = gpg_home
        self.gpg_passphrase = gpg_passphrase

        try:
            # Try to create a new wallet
            self.wallet = Wallet.create(wallet_name, witness_type='segwit', network='testnet')
        except WalletError as e:
            print("Wallet already exists. Loading the existing wallet.")
            self.wallet = Wallet(wallet_name)

        self.wallet.utxos_update()
        self.wallet.info(detail=3)

        # Display the wallet seed and first public key
        #print("Wallet Seed (Mnemonic Phrase):", self.wallet.mnemonic)
        print("First Public Key (Testnet):", self.wallet.get_key().address)

        # Set the check-in interval
        self.check_in_interval = self.parse_check_in_interval(check_in_interval)
        self.reset_check_in_due_date()

    def parse_check_in_interval(self, interval_str):
        interval_mapping = {
            '1 second': timedelta(seconds=1),
            '1 minute': timedelta(minutes=1),
            '1 hour': timedelta(hours=1),
            '1 day': timedelta(days=1),
            '1 week': timedelta(weeks=1),
            '1 month': timedelta(days=30),  # Approximation
            '1 year': timedelta(days=365)   # Approximation
        }
        return interval_mapping.get(interval_str, timedelta(days=1))

    def reset_check_in_due_date(self):
        self.check_in_due_date = datetime.now() + self.check_in_interval

    def record_proof_of_life(self, message_hash: str):
        key = self.wallet.get_key()
        address = key.address
        tx = Transaction(network='testnet')
        tx.add_output(value=1000, address=address)
        # Embed the provided hash in OP_RETURN
        op_return_data = b'\x6a' + len(bytes.fromhex(message_hash)).to_bytes(1, 'little') + bytes.fromhex(message_hash)
        tx.add_output(value=0, lock_script=op_return_data)
        tx.sign()
        print(tx.verify())
        tx.info()
        rawhextx = tx.raw_hex()
        tx = Service().sendrawtransaction(rawhextx)
        #self.wallet.send([(address, 1000)], tx)
        self.reset_check_in_due_date()

    def start_monitoring(self):
        schedule.every().day.at("10:00").do(self.check_in)

        while True:
            if datetime.now() >= self.check_in_due_date:
                self.check_in()
            schedule.run_pending()
            #time.sleep(60)

    def check_in(self):
        # Generate a new message and hash
        message = self.create_and_hash_message()
        self.record_proof_of_life(message)

    def create_and_hash_message(self):
        # Instantiate the Message class (or however you create a new message)
        # Example (replace with actual message creation logic):
        new_message = Message(
            name="John Doe",
            pgp_fingerprint=self.pgp_fingerprint,
            location="New York, USA",
            personal_statement="This is my updated proof of life message.",
            recent_event="Updated recent global event or personal milestone.",
            purpose="To demonstrate the creation of an updated proof of life message."
        )
        message_data = new_message.generate_proof_of_life()
        print(f"Message:\n{message_data}")

        # Sign and hash the message (adjust as needed based on your Message class)
        signed_message, message_hash = new_message.sign_and_hash(
        gpg_home=self.gpg_home, passphrase=self.gpg_passphrase
        )
        print(f"Signed message:\n{signed_message}")
        print(f"Hash: {message_hash}")
        return message_hash