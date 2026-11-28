# Hosted session runbook

Exact sequence for the remaining verification. Replace `<RUN>` with the
workflow run id and download the matching session artifact. The token file is
private and is never printed or committed.

All sessions use the pinned client `1c0d90debd7319c7580279bcbe2fb5ab19d6feea`
(`--client-dir /tmp/opencode/ui-test-actions`) and the token at
`/tmp/opencode/showcase-token`.

## 1. Android phone (full functional + recapture)

```sh
gh workflow run showcase-ui.yml -R NativeCmpKit/NativeCmpKit \
  --ref feature/showcase-ui-verification \
  -f mode=session -f platform=android -f device_class=phone -f duration_minutes=90
```

```sh
gh run download <RUN> -R NativeCmpKit/NativeCmpKit \
  -n ui-session-android-phone-<attempt>-<session> -D /tmp/opencode/session-android
python3 -u showcase/automation/functional.py \
  --client-dir /tmp/opencode/ui-test-actions \
  --connection /tmp/opencode/session-android/connection.json \
  --token-file /tmp/opencode/showcase-token \
  --platform android --device api35-phone --output-root screenshots
python3 -u showcase/automation/tour.py \
  --client-dir /tmp/opencode/ui-test-actions \
  --connection /tmp/opencode/session-android/connection.json \
  --token-file /tmp/opencode/showcase-token \
  --platform android --device api35-phone --output-root screenshots --continue-on-error
python3 showcase/automation/record_functional.py \
  --functional screenshots/android/functional-api35-phone.json \
  --platform android --run <RUN> --job <JOB>
python3 showcase/automation/record.py --tour screenshots/android/tour.json \
  --platform android --run <RUN> --job <JOB>
python3 showcase/automation/compare.py
python3 showcase/automation/index.py
```

## 2. iOS phone retest

```sh
gh workflow run showcase-ui.yml -R NativeCmpKit/NativeCmpKit \
  --ref feature/showcase-ui-verification \
  -f mode=session -f platform=ios -f device_class=phone -f duration_minutes=60
```

```sh
gh run download <RUN> -R NativeCmpKit/NativeCmpKit \
  -n ui-session-ios-phone-<attempt>-<session> -D /tmp/opencode/session-ios
python3 -u showcase/automation/functional.py ... --platform ios \
  --device iphone-simulator \
  --only clickable,slider,date-bounds,sheet-veto,date-display,webview-js
python3 -u showcase/automation/tour.py ... --platform ios \
  --device iphone-simulator --output-root screenshots --continue-on-error
python3 showcase/automation/record_functional.py \
  --functional screenshots/ios/functional-iphone-simulator.json \
  --platform ios --run <RUN> --job <JOB>
python3 showcase/automation/record.py --tour screenshots/ios/tour.json \
  --platform ios --run <RUN> --job <JOB>
```

The tour must capture `Adaptive Time Picker`; if the condition timeout recurs the
retry pass restarts the app once and retries that screen.

## 3. iPad

```sh
gh workflow run showcase-ui.yml -R NativeCmpKit/NativeCmpKit \
  --ref feature/showcase-ui-verification \
  -f mode=session -f platform=ios -f device_class=tablet -f duration_minutes=90
```

```sh
gh run download <RUN> -R NativeCmpKit/NativeCmpKit \
  -n ui-session-ios-tablet-<attempt>-<session> -D /tmp/opencode/session-ipad
python3 -u showcase/automation/tour.py ... --platform ios \
  --device ipad-simulator --output-root screenshots --continue-on-error
python3 -u showcase/automation/functional.py ... --platform ios \
  --device ipad-simulator --output-root screenshots
python3 showcase/automation/record.py --tour screenshots/ios/tour.json \
  --platform ios --run <RUN> --job <JOB> --tablet
python3 showcase/automation/compare.py --android-device api35-tablet \
  --ios-device ipad-simulator --output screenshots/compare-tablet --label tablet
python3 showcase/automation/index.py
```

`record.py --tablet` writes only the tablet-window rows; phone rows are never
touched. `record_functional.py` refuses `ipad-simulator` without
`--allow-device`; keep tablet functional results as separate evidence rather than
overwriting the canonical phone execution slots.

## 4. Android tablet

```sh
gh workflow run showcase-ui.yml -R NativeCmpKit/NativeCmpKit \
  --ref feature/showcase-ui-verification \
  -f mode=session -f platform=android -f device_class=tablet -f duration_minutes=90
```

```sh
gh run download <RUN> -R NativeCmpKit/NativeCmpKit \
  -n ui-session-android-tablet-<attempt>-<session> -D /tmp/opencode/session-android-tablet
python3 -u showcase/automation/tour.py ... --platform android \
  --device api35-tablet --output-root screenshots --continue-on-error
python3 -u showcase/automation/functional.py ... --platform android \
  --device api35-tablet --output-root screenshots
python3 showcase/automation/record.py --tour screenshots/android/tour.json \
  --platform android --run <RUN> --job <JOB> --tablet
python3 showcase/automation/compare.py --android-device api35-tablet \
  --ios-device ipad-simulator --output screenshots/compare-tablet --label tablet
python3 showcase/automation/index.py
```

## After every session

```sh
python3 showcase/generate_coverage.py
python3 showcase/automation/functional_matrix.py
python3 showcase/automation/check_flows.py
git add showcase screenshots && git commit -m "test(showcase): record <session> evidence"
git push
```

The driver writes results after every flow, so a session cut short still leaves a
usable partial file that `record_functional.py` merges by flow id.
