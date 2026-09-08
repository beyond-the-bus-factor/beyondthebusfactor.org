---
title: "Resources"
permalink: /resources/
eyebrow: "Free to use, free to adapt"
standfirst: "Six resources for finding and reducing key person risk. All released under CC0, so you can copy them, rewrite them and use them internally with no attribution."
body_class: "resources-page"
---

Most people work through these in order. The audit tells you where you are exposed, the checklist covers the immediate risks, and the succession guide is the longer piece of work.

<ul class="resource-list">
{% for r in site.data.resources %}
  <li id="{{ r.slug }}">
    <div class="resource-head">
      {% include icon.html name=r.icon %}
      <div>
        <p class="card-kind">{{ r.kind }} · {{ r.time }}</p>
        <h2>{{ r.title }}</h2>
        <p>{{ r.summary }}</p>
        <p class="use-when"><strong>Use this when:</strong> {{ r.use_when }}</p>
        <p class="resource-actions">
          <a class="btn btn-primary btn-sm" href="{{ site.repo_resources }}/blob/main/resources/{{ r.file }}">Read it</a>
          <a class="btn btn-ghost btn-sm" href="{{ site.repo_resources }}/edit/main/resources/{{ r.file }}">Suggest a change</a>
        </p>
      </div>
    </div>
  </li>
{% endfor %}
</ul>

## Making these fit your organisation

The resources are written in neutral language and then translated. Each one is being given a short overlay for open source projects, for charities and NGOs, and for companies, covering the terms that change and the risks that only show up in that setting.

If your sector is not covered well yet, [tell me what is missing]({{ site.repo_resources }}/issues/new/choose). That is how the rest of it got written.

## Contributing

These improve when more people put their experience into them.

- [Open an issue]({{ site.repo_resources }}/issues/new/choose) to suggest a resource, flag something unclear, or share a scenario
- [Join a discussion]({{ site.repo_resources }}/discussions) about what has worked and what has not
- [Open a pull request]({{ site.repo_resources }}/pulls) to add your expertise directly
