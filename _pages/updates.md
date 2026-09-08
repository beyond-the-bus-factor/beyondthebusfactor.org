---
title: "Updates"
permalink: /updates/
eyebrow: "What has changed"
standfirst: "New resources, sessions run, and what is being worked on."
---

<ul class="sessions">
{% for post in site.posts %}
  <li>
    <p class="card-kind"><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%-d %B %Y" }}</time></p>
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    <p>{{ post.excerpt | strip_html | strip_newlines | truncate: 200 }}</p>
  </li>
{% endfor %}
</ul>
