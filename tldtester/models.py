from django.db import models

class TLD(models.Model):
    """
    Model for the TLDs validation
    """
    INET = (( 0 , "IPv4"), ( 1 , "IPv6"), (2, "IPv4 + IPv6"),)
    DNSSECALGOS = (
        ( 0 , "Delete DS"),
        ( 1 , "RSA/MD5"),
        ( 2 , "Diffie-Hellman"),
        ( 3 , "DSA/SHA1"),
        ( 5 , "RSA/SHA-1"),
        ( 6 , "DSA-NSEC3-SHA1"),
        ( 7 , "RSASHA1-NSEC3-SHA1"),
        ( 8 , "RSA/SHA-256"),
        ( 10 , "RSA/SHA-512"),
        ( 12 , "GOST R 34.10-2001"),
        ( 13 , "ECDSA Curve P-256 with SHA-256"),
        ( 14, "ECDSA Curve P-384 with SHA-384"),
        ( 15 , "Ed25519"),
        ( 16 , "Ed448"),
        ( 17 , "SM2 signing algorithm with SM3 hashing algorithm"),
        ( 23 , "GOST R 34.10-2012"),
        ( 252 , "Reserved for Indirect Keys"),
        ( 253 , "private algorithm"),
        ( 254 , "private algorithm OID"),
        ( 300 , "Unknown"),

    )
    tld = models.CharField(max_length=30)
    dnssec = models.CharField(max_length=5, default=300, choices=DNSSECALGOS)
    inet = models.CharField(max_length=1, default=0, choices=INET)
    lastEdition = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.TLD

    class Meta:
        indexes = [
            models.Index(fields=["tld"]),
            models.Index(fields=["dnssec"]),
            models.Index(fields=["inet"]),
        ]
