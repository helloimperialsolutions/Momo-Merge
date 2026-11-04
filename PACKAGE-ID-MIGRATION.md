# Package ID migration — 2026-11-04

- Approved package ID: `com.isstudios.momomerge` (user selected the previously proposed value).
- Previous project ID: `com.sukoonstudio.fruitmerge` (legacy).
- User confirmed that no AAB had been uploaded to the previous Play Console app, so local project migration is safe to prepare.
- Updated Capacitor config, Android namespace/applicationId, Java package path, generated Capacitor config, and URL-scheme/package strings.
- `versionCode` remains 2; do not upload until the new package is confirmed/registered in Play Console and the signed build is produced.
- Package availability/registration has not been independently verified.
- No AAB has been built or uploaded in this workspace. GitHub Actions cannot be triggered from this workspace copy because it has no git remote/CLI and the GitHub connector is unsupported here.
