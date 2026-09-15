# Contributing

Issues are welcome. Specialist additions are curated by the maintainer.

## Pull requests

A pull request must pass:

```bash
npm run format:check
npm test
npm run validate
```

Published versions are immutable. A change to an already published Specialist ships as a new
SemVer version directory, never an edit to an existing one.

See [specialists/README.md](specialists/README.md) for the authoring layout and
[example/README.md](example/README.md) for a copyable walkthrough.
