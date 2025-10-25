---
layout: single
title: "Workshops & Sessions"
permalink: /sessions/
---

## Sessions

{% for session in site.sessions %}
<div class="session-card" markdown="1">

### {{ session.title }}

**{{ session.event_name }}**  
📅 {{ session.event_date | date: "%d %B %Y" }}
📍 {{ session.location }}  
⏱️ {{ session.duration }}

{{ session.excerpt }}

[View session materials →]({{ session.url }}){: .btn .btn--primary}

</div>

{% if forloop.last == false %}<hr>{% endif %}

{% endfor %}

---

**Interested in hosting a workshop?** [Get in touch](/contact/) to arrange a session for your conference or organisation.

<style>
.session-card {
  padding: 1.5rem;
  border: 1px solid #e1e4e8;
  border-radius: 8px;
  background: #f8f9fa;
  margin: 1.5rem 0;
}

.session-card h3 {
  margin-top: 0;
  color: #667eea;
}
</style>
