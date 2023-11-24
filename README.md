# Bitcoin Proof of Life Recorder

A program that performs life-proof certifications transactions on Bitcoin network using OP_RETURN by combining PGP and hashing. Based on the [BitLDC protocol](https://github.com/araujo88/BitLDC).

## Overview

The Bitcoin Proof of Life Recorder is a Python project designed to automate the process of recording a "proof of life" message on the Bitcoin blockchain. This application uses the `bitcoinlib` library to interact with the Bitcoin network, specifically the testnet, and embeds custom messages into the blockchain using `OP_RETURN` transactions.

## Features

- **Automated Proof of Life Messages**: Generates and embeds proof of life messages into the Bitcoin blockchain.
- **PGP Signature**: Integrates GPG for signing messages to ensure authenticity.
- **Flexible Scheduling**: Allows setting custom intervals for message recording.
- **Testnet Support**: Designed to work with Bitcoin's testnet for safe experimentation and testing.

## Requirements

### Python 3.10.12

### GMP development package.

The exact method to do this depends on your operating system. For example:

- **On Ubuntu/Debian-based systems**, you can install GMP using the following command:
  ```bash
  sudo apt-get install libgmp-dev
  ```
- **On Red Hat/CentOS/Fedora systems**, the command would be:
  ```bash
  sudo yum install gmp-devel
  ```
- **For macOS**, if you have Homebrew installed, use:
  ```bash
  brew install gmp
  ```

## Installation

Before running the project, ensure you have Python 3.x installed.

Clone the repository:

```bash
git clone https://github.com/araujo88/bit-life-proofing.git
cd bit-life-proofing
```

Setup the virtualenv and install the required dependencies:

```sh
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

## Usage

1. **Set Up GPG**: Ensure GPG is configured with the necessary keys for signing.
2. **Configuration**: Edit the main script or use environment variables to set the PGP fingerprint, GPG passphrase, and other settings.
3. **Generate some fake coins**: Make sure to generate some coins on a testnet [faucet](https://coinfaucet.eu/en/btc-testnet/) once you have obtained a wallet address for testing.
4. **Run the Recorder**:

```sh
python main.py
```

## Components

- **Recorder**: Manages the creation and broadcasting of transactions with proof of life messages.
- **Message**: Handles the generation, signing, and verification of proof of life messages.

## Customization

- **Message Content**: Customize the content of the proof of life message in `Message` class.
- **Intervals**: Set different check-in intervals in the `Recorder` class.

## Contributing

Contributions to the project are welcome! Please adhere to the following guidelines:

- Fork the repository and create your feature branch.
- Write clear and concise commit messages.
- Ensure your code adheres to the project's coding standards.
- Create a pull request with a detailed description of your changes.

## License

This project is licensed under the GPL License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This project is for educational and testing purposes only. It interacts with the Bitcoin testnet and should not be used for real transactions on the Bitcoin mainnet until the project attains more maturity.

## TODOs

- Integrate with a sidechain/nostr
- Incorporate multisig functionalities
- Write unit tests

## Examples

### Generating a message, signing it and veryfing it

```python
from message import Message

if __name__ == "__main__":
    # Initialize the ProofOfLife instance
    pol = Message(
        name="John Doe",
        pgp_fingerprint="1234ABCD5678EF",  # Replace with your actual PGP fingerprint
        location="New York, USA",
        personal_statement="This is my proof of life message.",
        recent_event="Recent global event or personal milestone.",
        purpose="To demonstrate the creation of a proof of life message."
    )

    # Generate the proof of life message
    message = pol.generate_proof_of_life()
    print("Proof of Life Message:", message)

    # Sign and hash the message
    gpg_home = None  # Replace with your GPG home directory path if not default
    passphrase = "YourPassphrase"  # Replace with your GPG passphrase

    signed_message, message_hash = message.sign_and_hash(
        gpg_home, passphrase
    )
    print("Signed Message:", signed_message)
    print("Message Hash:", message_hash)

    # Verify and hash the signed message
    is_valid, verified_hash = Message.verify_and_hash(signed_message)
    print("Is the signature valid:", is_valid)
    print("Verified Hash:", verified_hash)

    # Compare the verified hash with the original hash
    if is_valid and verified_hash == message_hash:
        print("The message is verified and the hash matches.")
    else:
        print("Verification failed or the hash does not match.")
```
