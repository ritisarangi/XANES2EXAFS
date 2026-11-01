#!/usr/bin/env python3
"""Renews the Globus login that driver.py uses to copy results between ALCF and NERSC.

ALCF's collection (alcf#dtn_flare) accepts only a recent login with an alcf.anl.gov identity; when
that session lapses, transfers fail with "None of your authenticated identities are from domains
allowed by resource policies". The login needs a person (browser, ALCF MFA), in two steps:

    ../venv/bin/python globus_login.py url           # prints a link: open it, log in with ALCF
    ../venv/bin/python globus_login.py code <CODE>   # paste the code shown after login

The second step replaces ~/.globus/transfer_tokens.json (the old file is kept as .bak). Then restart
the driver (screen zn_nersc) so it picks up the new tokens; the watchdog restarts it if you just quit it.
"""
import json, os, secrets, sys, time
import globus_sdk

CLIENT = "fae5c579-490a-4d76-b6eb-d78f65caeb63"
ALCF, NERSC = "f39a7a0f-5bfc-46ce-9615-ba9f8592814f", "6bdc7956-fc0f-4ad2-989c-7aa5ee643a79"
SCOPES = ("openid profile email urn:globus:auth:scope:transfer.api.globus.org:all"
          "[*https://auth.globus.org/scopes/%s/data_access *https://auth.globus.org/scopes/%s/data_access]"
          % (NERSC, ALCF))
G = os.path.expanduser("~/.globus")
VERIFIER, TOKENS = os.path.join(G, "login_verifier"), os.path.join(G, "transfer_tokens.json")


def flow(verifier):
    c = globus_sdk.NativeAppAuthClient(CLIENT)
    c.oauth2_start_flow(SCOPES, verifier=verifier, refresh_tokens=True)
    return c


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "url":
        v = secrets.token_urlsafe(64)[:80]
        with open(VERIFIER, "w") as f:
            f.write(v)
        os.chmod(VERIFIER, 0o600)
        print(flow(v).oauth2_get_authorize_url(session_required_single_domain="alcf.anl.gov", prompt="login"))
    elif len(sys.argv) >= 3 and sys.argv[1] == "code":
        c = flow(open(VERIFIER).read().strip())
        tok = c.oauth2_exchange_code_for_tokens(sys.argv[2].strip()).by_resource_server
        if "transfer.api.globus.org" not in tok:
            sys.exit("no transfer token in the reply; nothing changed")
        if os.path.exists(TOKENS):
            os.replace(TOKENS, TOKENS + ".bak")
        with open(TOKENS + ".new", "w") as f:
            json.dump(tok, f)
        os.chmod(TOKENS + ".new", 0o600)
        os.replace(TOKENS + ".new", TOKENS)
        os.remove(VERIFIER)
        print("new tokens written %s; restart the NERSC driver (screen zn_nersc)" % time.strftime("%F %T"))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
