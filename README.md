# beyondthebusfactor.org

## Checks

```
python3 script/check-house-style.py       # house style, every file we write prose into
python3 script/check-data.py              # the _data files that drive pages
python3 script/test-check-house-style.py  # that the checkers still work
python3 script/test-check-data.py
python3 script/test-analytics.py          # analytics only loads when configured
npm run a11y                              # WCAG 2 AA across every page
```

All of these run on every pull request. `check-data.py` needs PyYAML; the rest need nothing.

House style rules live in [`.house-style`](.house-style). That file is a copy: the canonical version is in [resilience-resources](https://github.com/beyond-the-bus-factor/resilience-resources/blob/main/.house-style), where most of the writing happens, and a weekly job checks the two still match.

A line that has to contain a banned word carries `house-style: allow` in a comment.

## Analytics

Off by default. Nothing is loaded and nothing is collected until `analytics:` in `_config.yml` names a provider and an id, and even then only on a production build.

Two options are supported, both cookie free and collecting no personal data, so neither needs a consent banner:

- [GoatCounter](https://www.goatcounter.com/), open source, free for non-commercial use
- [Cloudflare Web Analytics](https://www.cloudflare.com/web-analytics/), free, needs a Cloudflare account

The [privacy page](_pages/privacy.md) reads the same config, so it describes whatever is actually switched on rather than drifting from it.
