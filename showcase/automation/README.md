# Showcase automation

The hosted workflow opens a [ui-test-actions](https://github.com/ui-test-actions/ui-test-actions)
session on the real Android emulator or iOS Simulator. This directory contains
the external-client scripts used to drive and capture it.

## Pinned execution

- Runner scripts: `0c818c5d72e8c30c59bd1287c330a40392bf8e89`
- Captured by `.github/workflows/showcase-ui.yml`; the action itself is not on
  this repository's Actions allowlist, so the workflow clones that exact commit
  and starts `lifecycle.py` directly.
- Client: the `ui_sdk.py` / `agent.py` from the same commit.

## Token handling

The workflow expects the SHA-256 digest of a 256-bit token in
`ci/showcase-android.sha256` and `ci/showcase-ios.sha256`. Generate a fresh token
on the controlling machine and keep it private:

```sh
umask 077
TOKEN=$(openssl rand -hex 32)
printf '%s' "$TOKEN" > /tmp/showcase-token
printf '%s\n' "$(printf '%s' "$TOKEN" | openssl dgst -sha256 | awk '{print $NF}')" \
  > ci/showcase-android.sha256
cp ci/showcase-android.sha256 ci/showcase-ios.sha256
```

Never commit the raw token. The digest is not a secret.

## Download the live connection

```sh
gh api "repos/NativeCmpKit/NativeCmpKit/actions/runs/$RUN_ID/artifacts" \
  --jq '.artifacts[].name'
gh run download "$RUN_ID" --repo NativeCmpKit/NativeCmpKit \
  --name "$ARTIFACT" --dir /tmp/showcase-session
```

## Smoke flow

```sh
python3 showcase/automation/smoke.py \
  --client-dir /path/to/ui-test-actions \
  --connection /tmp/showcase-session/connection.json \
  --token-file /tmp/showcase-token \
  --output screenshots/_smoke/android \
  --platform android
```

The flow captures Home, opens Adaptive Buttons through the searchable index,
taps the production counter button, verifies the visible count, goes back, and
captures Home again.

## Functional checks

`functional.py` drives the real controls and asserts state, not just pixels:

```sh
python3 showcase/automation/functional.py \
  --client-dir /path/to/ui-test-actions \
  --connection live/connection.json --token-file /tmp/showcase-token \
  --platform android --output-root screenshots
```

It writes `screenshots/<platform>/functional.json` with `passed`, `failed` and
`blocked` entries and before/after PNGs under `screenshots/<platform>/functional/`.

## Notes

- Android uses the API 35 Google APIs x86_64 KVM emulator and the debug APK.
- iOS uses one explicitly selected iPhone simulator UDID and the simulator
  `.app`; AXe is installed from the pinned release for semantic elements.
- Screenshots are captured from the live emulator/simulator, never from a
  host-side render.
- Keep failed captures under their unique run/attempt directory; do not
  overwrite an original failure with a later pass.
