#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VERSION="${1:-}"
DISPLAY_VERSION="${VERSION#review-}"
SIGNING_IDENTITY="${PAMALYTICS_CODESIGN_IDENTITY:-}"
NOTARY_PROFILE="${PAMALYTICS_NOTARY_PROFILE:-}"

APP="$ROOT/dist-review/PAMalytics Review.app"
ICON="$ROOT/packaging/macos/PAMalytics.icns"
RELEASE_DIR="$ROOT/release-review"
DMG_ROOT="$RELEASE_DIR/dmg-root"
DMG_OUT="$RELEASE_DIR/PAMalytics-review-${DISPLAY_VERSION}-macOS-arm64.dmg"
CHECKSUM_OUT="$DMG_OUT.sha256"

if [[ -z "$VERSION" ]]; then
  echo "Usage: bash packaging/review/macos/build_dmg.sh <version>" >&2
  echo "Example: bash packaging/review/macos/build_dmg.sh review-v1.0.2" >&2
  exit 1
fi

if [[ -z "$SIGNING_IDENTITY" ]]; then
  echo "PAMALYTICS_CODESIGN_IDENTITY must be set." >&2
  exit 1
fi

if [[ -z "$NOTARY_PROFILE" ]]; then
  echo "PAMALYTICS_NOTARY_PROFILE must be set." >&2
  exit 1
fi

if [[ ! -d "$APP" ]]; then
  echo "Missing review app bundle: $APP" >&2
  echo "Run: python3.12 packaging/review/macos/build_app.py" >&2
  exit 1
fi

if [[ ! -f "$ICON" ]]; then
  echo "Missing volume icon: $ICON" >&2
  exit 1
fi

security find-identity -v -p codesigning | grep -Fq "$SIGNING_IDENTITY" || {
  echo "Signing identity not found: $SIGNING_IDENTITY" >&2
  exit 1
}

codesign --verify --deep --strict --verbose=2 "$APP"

mkdir -p "$RELEASE_DIR"
rm -rf "$DMG_ROOT"
rm -f "$DMG_OUT" "$CHECKSUM_OUT"
mkdir -p "$DMG_ROOT"

ditto "$APP" "$DMG_ROOT/PAMalytics Review.app"
cp "$ICON" "$DMG_ROOT/.VolumeIcon.icns"
ln -s /Applications "$DMG_ROOT/Applications"

if command -v SetFile >/dev/null 2>&1; then
  SetFile -a C "$DMG_ROOT"
else
  echo "Warning: SetFile is unavailable; the custom volume icon may not display." >&2
fi

hdiutil create \
  -volname "PAMalytics Review" \
  -srcfolder "$DMG_ROOT" \
  -ov \
  -format UDZO \
  "$DMG_OUT"

codesign \
  --force \
  --timestamp \
  --sign "$SIGNING_IDENTITY" \
  "$DMG_OUT"

codesign --verify --strict --verbose=2 "$DMG_OUT"

xcrun notarytool submit "$DMG_OUT" \
  --keychain-profile "$NOTARY_PROFILE" \
  --wait

xcrun stapler staple "$DMG_OUT"
xcrun stapler validate "$DMG_OUT"
hdiutil verify "$DMG_OUT"
spctl --assess --type open --context context:primary-signature --verbose=4 "$DMG_OUT"

shasum -a 256 "$DMG_OUT" | tee "$CHECKSUM_OUT"

rm -rf "$DMG_ROOT"

echo
echo "Signed, notarised and stapled reviewer release created:"
echo "$DMG_OUT"
echo "$CHECKSUM_OUT"
