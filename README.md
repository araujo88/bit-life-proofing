# bit-life-proofing

A program that performs life-proof certifications transactions on Bitcoin network using OP_RETURN by combining PGP and hashing

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
