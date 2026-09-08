---
title: "Scenario card tool"
permalink: /scenarios/cards/
eyebrow: "Draw a card"
standfirst: "Filter by the kind of organisation you are, draw a scenario, and keep a note of what nobody could answer."
body_class: "cards-tool"
---

<div class="tool" id="tool">
  <noscript>
    <p class="tool-fallback">This tool needs JavaScript. All twenty five scenarios are readable without it in
    <a href="{{ site.repo_resources }}/blob/main/resources/scenario-cards.md">the scenario cards document</a>,
    and the <a href="{{ site.repo_resources }}/raw/main/deck/scenario-deck.pdf">printable deck</a> is a PDF.</p>
  </noscript>
</div>

<template id="tool-tpl">
  <div class="tool-filters" role="group" aria-label="Filter scenarios">
    <fieldset>
      <legend>Kind of organisation</legend>
      <div class="chips" data-group="sectors"></div>
    </fieldset>
    <fieldset>
      <legend>Focus</legend>
      <div class="chips" data-group="categories"></div>
    </fieldset>
    <fieldset>
      <legend>Level</legend>
      <div class="chips" data-group="difficulty"></div>
    </fieldset>
    <p class="tool-actions">
      <button type="button" class="btn btn-primary" data-act="draw">Draw a card</button>
      <button type="button" class="btn btn-ghost" data-act="reset">Clear filters</button>
      <span class="tool-count" role="status" aria-live="polite"></span>
    </p>
  </div>

  <div class="tool-stage" aria-live="polite"></div>
</template>

## Running this with a group

There is a [facilitator's guide]({{ site.repo_resources }}/blob/main/resources/facilitator-guide.md) with session formats, timings, and what to do when a group starts arguing with the scenario instead of working it.

For a room, the printed deck works better than a screen. The [PDF]({{ site.repo_resources }}/raw/main/deck/scenario-deck.pdf) is A4, two A5 cards per sheet, with a cover card carrying the instructions.
