#!/usr/bin/env bash
#
# look-at-the-site.sh  --  open the website from this machine, with no build step
#
# Two ways to run it:
#
#   ./ops/look-at-the-site.sh
#       Plain local viewing on this computer. Prints an address to open in
#       Firefox or Chrome. This is all you need for the flat-screen version.
#
#   ./ops/look-at-the-site.sh headset
#       Same site, but served over https so that a Meta Quest on the same
#       wi-fi can open it. Virtual Reality in a browser REFUSES to start over
#       a plain connection, which is why this mode exists. The certificate is
#       homemade, so the headset will show a scary warning once: tap Advanced,
#       then Proceed. It is your own computer; the warning is only saying that
#       nobody famous vouched for it.
#
# Stop either one with Ctrl+C.
#
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SITE="$HERE/site"
CERTS="$HERE/ops/local-certificate"
PORT_PLAIN=8080
PORT_SECURE=8443

cd "$SITE"

if [[ "${1:-}" != "headset" ]]; then
  echo ""
  echo "Open this on this computer:"
  echo "    http://localhost:$PORT_PLAIN/"
  echo ""
  echo "Stop the server with Ctrl+C."
  echo ""
  exec python3 -m http.server "$PORT_PLAIN" --bind 127.0.0.1
fi

# ---- headset mode -----------------------------------------------------------

mkdir -p "$CERTS"
if [[ ! -f "$CERTS/certificate.pem" ]]; then
  echo "Making a homemade certificate, once. Nothing secret is involved."
  openssl req -x509 -newkey rsa:2048 -nodes -days 3650 \
    -keyout "$CERTS/key.pem" -out "$CERTS/certificate.pem" \
    -subj "/CN=ai-panorama-home" \
    -addext "subjectAltName=DNS:localhost,IP:127.0.0.1,IP:$(hostname -I | awk '{print $1}')" \
    2>/dev/null
fi

ADDRESS="$(hostname -I | awk '{print $1}')"

cat <<EOF

Put the headset on, open its browser, and type this in:

    https://$ADDRESS:$PORT_SECURE/

The headset will warn you that it does not recognise the certificate. That is
expected, because the certificate was made by this computer a moment ago. Tap
Advanced, then Proceed. Then press "Open in Virtual Reality".

Stop the server with Ctrl+C.

EOF

exec python3 - "$PORT_SECURE" "$CERTS" <<'PYTHON'
import http.server, ssl, sys, functools

port = int(sys.argv[1])
certificates = sys.argv[2]

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(f"{certificates}/certificate.pem", f"{certificates}/key.pem")

handler = functools.partial(http.server.SimpleHTTPRequestHandler)
server = http.server.ThreadingHTTPServer(("0.0.0.0", port), handler)
server.socket = context.wrap_socket(server.socket, server_side=True)
server.serve_forever()
PYTHON
