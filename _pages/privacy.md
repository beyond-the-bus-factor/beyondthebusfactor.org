---
title: "Privacy"
permalink: /privacy/
eyebrow: "What this site does with you"
standfirst: "Short, because there is not much to say."
---

{% capture analytics_on %}{% include analytics-on.html %}{% endcapture %}
{% if analytics_on == "yes" %}
## What is collected

This site counts page views using {% case site.analytics.provider %}{% when "goatcounter" %}[GoatCounter](https://www.goatcounter.com/){% when "cloudflare" %}[Cloudflare Web Analytics](https://www.cloudflare.com/web-analytics/){% else %}an analytics service{% endcase %}.

That records which pages were viewed, roughly where in the world from, and what kind of browser and device. It sets no cookies, does not follow you between sites, and does not build a profile of you. There is nothing in it that identifies you, and nothing that could be handed over if somebody asked.

It exists so the resources here can be improved based on what people actually read, rather than guesswork.

If you would rather not be counted, a tracker blocker will stop it, and nothing on the site will break.
{% else %}
## What is collected

Nothing. There is no analytics on this site, no cookies, and no third party scripts that watch you.

That means we have no idea which resources are useful, which is a real cost. If something here helped, [saying so]({{ site.repo_resources }}/discussions) is the only way we find out.
{% endif %}

## Fonts

Typefaces are served by Google Fonts, which means your browser fetches them from Google and Google sees the request. If that matters to you, blocking it leaves the site readable in your system font.

## The contact form

If you fill in the [contact form]({{ '/contact/' | relative_url }}), it goes through [Formspree](https://formspree.io/) and arrives as an email. Your message and your address are kept for as long as it takes to reply and to keep a record of the conversation, and are not added to any mailing list or shared with anyone.

## GitHub

The resources live on GitHub, so following a link to them means GitHub's privacy terms apply from that point rather than ours.

## Asking

Any question about this, or a request to delete something you have sent, goes to the [contact form]({{ '/contact/' | relative_url }}).
