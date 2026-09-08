# beyondthebusfactor.org

## Checks

```
python3 script/check-house-style.py       # house style, every file we write prose into
python3 script/test-check-house-style.py  # that the checker still works
npm run a11y                              # WCAG 2 AA across every page
```

The first two run on every pull request, alongside the accessibility check.

House style rules live in [`.house-style`](.house-style). That file is a copy: the canonical version is in [resilience-resources](https://github.com/beyond-the-bus-factor/resilience-resources/blob/main/.house-style), where most of the writing happens, and a weekly job checks the two still match.

A line that has to contain a banned word carries `house-style: allow` in a comment.
