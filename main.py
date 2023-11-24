from recorder import Recorder

if __name__ == "__main__":
    # Usage example
    recorder = Recorder(check_in_interval='1 minute', 
                        pgp_fingerprint="F277A34924BBF522735D912A0F32F636EEB86B44",
                        gpg_passphrase="johndoeINSECURE*")
    recorder.start_monitoring()
