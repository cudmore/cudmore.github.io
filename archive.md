---
layout: page
title: Archive
---

<ul>
  {% for post in site.posts %}

    {% unless post.next %}
   	   <h3>{{ post.date | date: '%Y' }}</h3>
    {% else %}
      {% capture year %}{{ post.date | date: '%Y' }}{% endcapture %}
      {% capture nyear %}{{ post.next.date | date: '%Y' }}{% endcapture %}
      {% if year != nyear %}
		<div class="archive-group"></div>
        <h3>{{ post.date | date: '%Y' }}</h3>
      {% endif %}
    {% endunless %}

    {{ post.date | date:"%b %d" }} - <a href="{{site.baseurl}}{{ post.url }}">{{ post.title }}</a>
    <BR>
    	
  {% endfor %}
</ul>
