---
title: "Workshops and sessions"
permalink: /sessions/
eyebrow: "Working through it with other people"
standfirst: "Facilitated sessions where teams audit their own exposure and leave with something written down."
---

{% assign today = site.time | date: "%Y-%m-%d" %}
{% assign upcoming = "" | split: "" %}
{% assign past = "" | split: "" %}
{% for s in site.sessions %}{% assign d = s.event_date | date: "%Y-%m-%d" %}{% if d >= today %}{% assign upcoming = upcoming | push: s %}{% else %}{% assign past = past | push: s %}{% endif %}{% endfor %}

{% if upcoming.size > 0 %}
## Coming up

<ul class="sessions">
{% for s in upcoming %}
  <li>
    <p class="card-kind">{{ s.event_date | date: "%-d %B %Y" }} · {{ s.location }} · {{ s.duration }}</p>
    <h3><a href="{{ s.url | relative_url }}">{{ s.title }}</a></h3>
    <p>{{ s.excerpt | strip_html }}</p>
  </li>
{% endfor %}
</ul>
{% else %}
## Coming up

Nothing scheduled at the moment. If you would like a session at your conference, inside your organisation, or for your community group, [get in touch](/contact/).
{% endif %}

## Formats

- **45 minute interactive workshop**, unconference style, for conferences and community days
- **30 minute talk** where a workshop does not fit the programme
- **Half day or full day training** for a team that needs to come out with a finished plan
- **Advisory work** for a transition already underway

Participants leave with their vulnerabilities mapped, templates they can fill in, and one specific commitment for the next thirty days.

{% if past.size > 0 %}
## Previously

<ul class="sessions">
{% for s in past %}
  <li>
    <p class="card-kind">{{ s.event_date | date: "%-d %B %Y" }} · {{ s.location }}</p>
    <h3><a href="{{ s.url | relative_url }}">{{ s.title }}</a></h3>
    <p>{{ s.excerpt | strip_html }}</p>
  </li>
{% endfor %}
</ul>
{% endif %}
