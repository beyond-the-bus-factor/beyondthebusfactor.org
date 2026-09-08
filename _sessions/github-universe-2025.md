---
title: "Beyond the bus factor, building resilient open source projects"
event_name: "GitHub Universe 2025, Community Day"
event_date: 2025-10-27
location: "San Francisco"
type: "workshop"
duration: "45 minute interactive workshop"
excerpt: "The first outing for this material. Mapping single points of failure, working through crisis scenarios in small groups, and leaving with one commitment for the next thirty days."
---

The session that started this project, run at GitHub Universe Community Day for open source maintainers and community managers.

## What we covered

- Mapping bus factor vulnerabilities across technical systems, governance and community
- Working through crisis scenarios in small groups
- Designing systems that distribute knowledge as a matter of course
- Committing to one concrete action within thirty days

## Materials

The full facilitation guide is published, so anyone can run this session themselves.

<p class="resource-actions">
  <a class="btn btn-primary btn-sm" href="{{ site.repo_resources }}/blob/main/sessions/github-universe-2025.md">Facilitation guide</a>
  <a class="btn btn-ghost btn-sm" href="{{ site.repo_resources }}/blob/main/resources/scenario-cards.md">Scenario cards</a>
</p>

## Resources used

{% assign used = "bus-factor-audit,legacy-checklist,succession-planning-guide,scenario-cards" | split: "," %}
{% for slug in used %}{% assign r = site.data.resources | where: "slug", slug | first %}
- [{{ r.title }}]({{ site.repo_resources }}/blob/main/resources/{{ r.file }})
{%- endfor %}
