---
title: "Sector overlays"
permalink: /sectors/
eyebrow: "Four doors into the same library"
standfirst: "The audit is deliberately neutral. Each overlay translates it into the language of your setting and adds the risks it cannot know about."
---

The underlying failure is the same everywhere. One person holds something, nobody else can pick it up, and nothing goes wrong until it does.

The vocabulary is not the same, and neither are the specifics. A charity has statutory roles it must fill. A company has a continuity plan that covers the building and not the people. An open source project can lose the ability to publish while the code stays perfectly safe.

So the [bus factor audit]({{ '/resources/' | relative_url }}#bus-factor-audit) is written to work anywhere, and each overlay adds four things: a map of what the terms are called in your setting, the audit rows a neutral document cannot carry, the failure that setting most often turns out to have, and a worked example.

<ol class="cards">
{% for s in site.data.sectors %}
  <li class="card">
    <span class="card-icon">{% include icon.html name=s.icon %}</span>
    <p class="card-kind">Overlay</p>
    <h3><a href="{{ '/sectors/' | append: s.slug | append: '/' | relative_url }}">{{ s.name }}</a></h3>
    <p>{{ s.blurb }}</p>
    <p class="card-failure"><strong>The usual failure:</strong> {{ s.failure }}</p>
  </li>
{% endfor %}
</ol>

## How to use one

Read the overlay first, which takes a few minutes, then work through the [audit]({{ '/resources/bus-factor-audit/' | relative_url }}) with its extra rows added to yours. The overlay ends by naming the [scenario cards]({{ '/scenarios/' | relative_url }}) worth running first for that setting.

If you sit across two of these, and plenty of organisations do, read both. They overlap less than you would expect.

## If none of them fit

The overlays cover the settings the material has been tested against so far. If yours is missing, or one of them nearly fits but gets something wrong, [say so]({{ site.repo_resources }}/issues/new/choose). That is how the existing four got written.
