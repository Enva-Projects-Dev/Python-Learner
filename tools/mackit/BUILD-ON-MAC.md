# Build Python Learner on your Mac

This kit builds a real Python Learner.app and a DMG on an Apple
Silicon Mac (M1/M2/M3/M4). Takes about 3-5 minutes, ~40 MB download.

## Steps

1. Copy this folder to your Mac, e.g. onto the Desktop.
2. Open Terminal and check `python3 --version`. If it's below 3.10 or
   missing, install Python from
   <https://www.python.org/downloads/macos/> first.
3. Double-click `Build Python Learner.command`.
   (First time macOS may say it "can't be opened", so right-click the
   file, choose Open, click Open once.)
4. Wait. The script fetches a standalone Python runtime, builds the
   app, signs it ad-hoc, smoke-tests it, and creates the DMG.
5. When it says DONE, open the DMG next to this folder and drag
   Python Learner into Applications.

The first launch may warn "unidentified developer", so right-click the
app and choose Open once.

## Troubleshooting

- "Python 3.10+ was not found" -> install Python from
  python.org (link above), then run the .command again.
- "This kit builds for Apple Silicon only" -> Intel Macs aren't
  supported by this kit.
- "could not download a runtime" -> check your internet connection.
- "BUILD FAILED at step: X" -> note the step name and re-run in
  Terminal to see the full error: `bash build_mac_app.sh`
- No space -> the build needs ~300 MB free temporarily.

Your progress is stored in
`~/Library/Application Support/PythonLearner/progress.json`,
delete that file to reset everything.
