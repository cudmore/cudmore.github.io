# Robert Cudmore's blog 

## Introduction

This is the Jekyll source code and post data for my blog, the layout is auto generated using Jekyll and a theme based on Hyde which is based on Poole.

If you are interested, you can use some of the formatting I have employed.

- I generate a tag list and page by using the [tags.html](https://github.com/cudmore/cudmore.github.io/blob/master/tags.html) file. This requires each post to have some yaml front matter:

	---
	layout: post
	title: "Use OpenCV to acquire video"
	category: post
	date: 2015-03-07 22:01:06
	tags:
	- video  
	- acquisition  
	- opencv  
	---  

- I generate an archive page with [archive.md](https://github.com/cudmore/cudmore.github.io/blob/master/archive.md) and it looks like this:

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

	    {{ post.date | date:"%b %d" }}, <a href="{{site.baseurl}}{{ post.url }}">{{ post.title }}</a>
	    <BR>
	    	
	  {% endfor %}
	</ul>


## Authors

**Robert Cudmore**  
- <https://github.com/cudmore>  
- <http://robertcudmore.org>

Hyde was written by **Mark Otto**  
- <https://github.com/mdo>  
- <https://twitter.com/mdo>

## License

Open sourced under the [MIT license](LICENSE.md).
