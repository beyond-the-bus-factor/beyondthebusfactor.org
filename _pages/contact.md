---
title: "Get in touch"
permalink: /contact/
eyebrow: "Workshops, training and advisory"
standfirst: "For a session at your event, training for your team, or support with a transition already underway."
---

<form action="{{ site.contact_form }}" method="POST" class="form">
  <div class="field">
    <label for="name">Name</label>
    <input type="text" id="name" name="name" required>
  </div>
  <div class="field">
    <label for="email">Email</label>
    <input type="email" id="email" name="_replyto" required>
  </div>
  <div class="field">
    <label for="organisation">Organisation</label>
    <input type="text" id="organisation" name="organisation">
  </div>
  <div class="field">
    <label for="sector">What kind of organisation</label>
    <select id="sector" name="sector">
      <option value="">Please select</option>
      <option value="open-source">Open source project or community</option>
      <option value="charity">Charity, NGO or nonprofit</option>
      <option value="company">Company</option>
      <option value="small-team">Small team, collective or volunteer group</option>
      <option value="other">Something else</option>
    </select>
  </div>
  <div class="field">
    <label for="interest">What you are after</label>
    <select id="interest" name="interest" required>
      <option value="">Please select</option>
      <option value="workshop">A workshop at my event</option>
      <option value="talk">A conference talk</option>
      <option value="training">Training for my team</option>
      <option value="advisory">Advisory support for a transition</option>
      <option value="other">Something else</option>
    </select>
  </div>
  <div class="field">
    <label for="message">Message</label>
    <textarea id="message" name="message" rows="6" required></textarea>
  </div>
  <button type="submit" class="btn btn-primary">Send</button>
</form>

## Other ways to reach this work

- [Ask a question or start a discussion]({{ site.repo_resources }}/discussions)
- [Report something unclear or propose a resource]({{ site.repo_resources }}/issues/new/choose)
- [Watch the repository]({{ site.repo_resources }}) for new material
