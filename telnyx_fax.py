"""
Telnyx inbound-fax adapter.

Provider-agnostic seam for receiving real faxes: verifies Telnyx webhook
signatures (Ed25519) and downloads the received fax PDF. To support a
different fax provider later, swap this module — the route in demo_server.py
only depends on verify_signature() and download_fax().
"""
import base64
import requests


def verify_signature(payload: bytes, signature_b64: str, timestamp: str, public_key_b64: str) -> bool:
    """Verify a Telnyx Ed25519 webhook signature.

    Telnyx signs ``f"{timestamp}|{raw_body}"`` with its account Ed25519 key and
    sends the signature in the ``telnyx-signature-ed25519`` header (base64) plus
    the ``telnyx-timestamp`` header.

    Returns True when valid. If ``public_key_b64`` is empty, verification is
    SKIPPED (returns True) so local dry-runs work without a key configured —
    always set TELNYX_PUBLIC_KEY in production.
    """
    if not public_key_b64:
        return True  # verification disabled — no key configured (dev/dry-run)
    if not signature_b64 or not timestamp:
        return False
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        from cryptography.exceptions import InvalidSignature
    except ImportError:
        # A key was configured but the lib is missing — fail closed.
        return False
    signed = timestamp.encode() + b"|" + payload
    try:
        key = Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key_b64))
        key.verify(base64.b64decode(signature_b64), signed)
        return True
    except InvalidSignature:
        return False
    except Exception:
        return False


def download_fax(media_url: str, api_key: str = "", timeout: int = 60) -> bytes:
    """Download the received fax PDF from a Telnyx media URL.

    Telnyx media URLs are usually directly downloadable; if the URL requires
    auth (401/403) we retry with the API key as a bearer token.
    """
    r = requests.get(media_url, timeout=timeout)
    if r.status_code in (401, 403) and api_key:
        r = requests.get(media_url, headers={"Authorization": f"Bearer {api_key}"}, timeout=timeout)
    r.raise_for_status()
    return r.content
