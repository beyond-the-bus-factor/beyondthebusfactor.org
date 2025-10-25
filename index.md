---
layout: splash
title: "Beyond the Bus Factor"
header:
  overlay_color: "#2c3e50"
  overlay_filter: "0.5"
  overlay_image: /assets/images/header-bg.jpg
  actions:
    - label: "View Resources"
      url: "/resources/"
    - label: "GitHub"
      url: "https://github.com/beyond-the-bus-factor/resilience-resources"
excerpt: "Building resilient projects and organisations that survive beyond any individual contributor"
intro: 
  - excerpt: 'Most projects are one key person away from crisis. We provide practical resources, workshops, and community support to help you build genuine resilience.'
feature_row:
  - image_path: /assets/images/audit.svg
    alt: "Bus Factor Audit"
    title: "Audit Your Vulnerabilities"
    excerpt: "Identify single points of failure across technical systems, governance, and community relationships"
    url: "https://github.com/beyond-the-bus-factor/resilience-resources/blob/main/resources/bus-factor-audit.md"
    btn_label: "Use the Framework"
    btn_class: "btn--primary"
  - image_path: /assets/images/checklist.svg
    alt: "Legacy Checklist"
    title: "Prepare for the Unexpected"
    excerpt: "The uncomfortable but essential checklist for what happens if you die or become suddenly incapacitated"
    url: "https://github.com/beyond-the-bus-factor/resilience-resources/blob/main/resources/legacy-checklist.md"
    btn_label: "Get the Checklist"
    btn_class: "btn--primary"
  - image_path: /assets/images/succession.svg
    alt: "Succession Planning"
    title: "Plan for Transitions"
    excerpt: "Templates for technical handoffs, governance changes, and building sustainable leadership"
    url: "https://github.com/beyond-the-bus-factor/resilience-resources/blob/main/resources/succession-planning-guide.md"
    btn_label: "Start Planning"
    btn_class: "btn--primary"
---

{% include feature_row id="intro" type="center" %}

{% include feature_row %}

## Upcoming Events

<div class="events-list">
  {% for session in site.sessions %}
    <div class="event-card">
      <h3><a href="{{ session.url }}">{{ session.title }}</a></h3>
      <p class="event-meta">
        <strong>{{ session.event_name }}</strong><br>
        📅 {{ session.event_date | date: "%d %B %Y" }}<br>
        📍 {{ session.location }}
      </p>
      <p>{{ session.excerpt }}</p>
      <a href="{{ session.url }}" class="btn btn--primary">Learn More</a>
    </div>
  {% endfor %}
</div>

[View all sessions →](/sessions/){: .btn .btn--primary}

---

## Why This Matters

Most open source projects fail not because the technology is bad, but because key people leave and nobody knows how to continue.

The 'bus factor' is a polite term for a harsh reality: most projects are one burnout, one new job, or one life event away from collapsing.

**This doesn't have to be your story.**

These resources emerged from real experience preparing for transitions, navigating crises, and building projects that survive beyond individuals.

[Read the origin story →](/about/){: .btn .btn--inverse}

---

## Community Contributors

<div id="contributors-grid">
  <p>Loading contributors...</p>
</div>

<script>
// Fetch contributors from GitHub API
fetch('https://api.github.com/repos/beyond-the-bus-factor/resilience-resources/contributors')
  .then(response => response.json())
  .then(contributors => {
    const grid = document.getElementById('contributors-grid');
    grid.innerHTML = contributors.map(contributor => `
      <a href="${contributor.html_url}" class="contributor-card" target="_blank" rel="noopener">
        <img src="${contributor.avatar_url}" alt="${contributor.login}" loading="lazy">
        <span>${contributor.login}</span>
        <small>${contributor.contributions} contributions</small>
      </a>
    `).join('');
  })
  .catch(error => {
    document.getElementById('contributors-grid').innerHTML = '<p>Unable to load contributors. <a href="https://github.com/beyond-the-bus-factor/resilience-resources/graphs/contributors">View on GitHub</a></p>';
  });
</script>

<style>
.events-list {
  display: grid;
  gap: 2rem;
  margin: 2rem 0;
}

.event-card {
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  padding: 1.5rem;
  background: #f6f8fa;
}

.event-card h3 {
  margin-top: 0;
}

.event-meta {
  color: #586069;
  font-size: 0.9rem;
  margin: 0.5rem 0 1rem;
}

#contributors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
}

.contributor-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1rem;
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s;
}

.contributor-card:hover {
  border-color: #0366d6;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transform: translateY(-2px);
}

.contributor-card img {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  margin-bottom: 0.5rem;
}

.contributor-card span {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.contributor-card small {
  font-size: 0.8rem;
  color: #586069;
}
</style>
<style>
/* Resize feature row icons */
.feature__item .archive__item-teaser img {
  max-width: 150px;
  max-height: 150px;
  width: auto;
  height: auto;
  margin: 0 auto 1rem;
}

.feature__item .archive__item-teaser {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 180px;
}
</style>
