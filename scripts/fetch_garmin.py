# scripts/fetch_garmin.py
import os
import json
import base64
from pathlib import Path

import garth
from garminconnect import Garmin


def write_token_from_env(env_name: str, target_path: Path):
    b64 = os.environ.get(env_name)
    if not b64:
        return False
    raw = base64.b64decode(b64)
    data = json.loads(raw.decode())
    target_path.write_text(json.dumps(data))
    return True


def get_client():
    tmp_dir = Path("/tmp/garth_session")
    tmp_dir.mkdir(parents=True, exist_ok=True)

    # try to reconstruct both token files
    wrote_oauth1 = write_token_from_env("GARMIN_OAUTH1_B64", tmp_dir / "oauth1_token.json")
    wrote_oauth2 = write_token_from_env("GARMIN_OAUTH2_B64", tmp_dir / "oauth2_token.json")

    if wrote_oauth1 or wrote_oauth2:
        # load whatever we have — your dump had both, so this should work
        garth.client.load(str(tmp_dir))
        return Garmin()

    # fallback to username/password
    username = os.environ.get("GARMIN_USERNAME")
    password = os.environ.get("GARMIN_PASSWORD")
    if username and password:
        g = Garmin(username, password)
        g.login()
        return g

    raise RuntimeError("No valid tokens and no username/password available")


def main():
    client = get_client()
    activities = client.get_activities(0, 5)
    for a in activities:
        print(f"{a['startTimeLocal']} - {a['activityName']} - {a.get('distance', 0)}m")


if __name__ == "__main__":
    main()
