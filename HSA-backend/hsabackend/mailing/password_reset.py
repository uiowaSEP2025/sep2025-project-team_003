from django.core.mail import send_mail
import os


def send_password_reset(reset_token):
    send_mail(
        subject='Hello from Django',
        message='This is a test email sent from Django!',
        from_email=os.environ.get('EMAIL_HOST_USER',None),
        recipient_list=['alex.t.guo@gmail.com'],
        fail_silently=False,
    )

import socket
import ssl
from pprint import pprint

import os
import socket
import ssl
from pprint import pprint

def getCert():
    hostname = os.environ.get('EMAIL_HOST', None)
    port = 465
    
    # Create a context that doesn't verify the cert (to prevent SSLCertVerificationError)
    context = ssl.create_default_context()
    context.check_hostname = False  # Disable hostname verification
    context.verify_mode = ssl.CERT_NONE  # Disable certificate verification
    
    try:
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                print(f"\n🔍 SSL Certificate Details for {hostname}:{port}")
                print("\n📜 Certificate Subject:")
                subject = dict(x[0] for x in cert.get('subject', []))
                pprint(subject)
                
                print("\n🔎 Subject Alternative Names (SANs):")
                sans = cert.get('subjectAltName', [])
                if sans:
                    for san_type, san_value in sans:
                        print(f"  - {san_type}: {san_value}")
                else:
                    print("  ❌ No SANs found (certificate may be invalid for hostname verification)")
                
                # Check if the hostname/IP matches any SAN or CN
                is_valid = False
                expected_names = set()
                
                # Check SANs first
                if sans:
                    for san_type, san_value in sans:
                        expected_names.add(san_value.lower())
                
                # Fallback to Common Name (CN) if no SANs
                if not sans and 'commonName' in subject:
                    expected_names.add(subject['commonName'].lower())
                
                # Check if hostname matches any expected name
                hostname_lower = hostname.lower()
                is_valid = hostname_lower in expected_names
                
                if not is_valid:
                    print(f"\n❌ MISMATCH DETECTED: The certificate is NOT VALID for '{hostname}'")
                    print("\n   Expected (from certificate):")
                    for name in expected_names:
                        print(f"   - {name}")
                    print("\n   Possible fixes:")
                    print("   - Connect using one of the names listed above")
                    print("   - Get a new certificate that includes this hostname/IP in SANs")
                else:
                    print("\n✅ VALID: The hostname/IP matches the certificate.")
                
                print("\n📜 Full Certificate Details:")
                pprint(cert)
                
    except Exception as e:
        print(f"\n❌ Connection Error: {e}")