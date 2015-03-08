# Robert Cudmore's blog 

## Introduction

This is the Jekyll source code and post data for my blog, the layout is auto generated using [Jekyll](http://jekyllrb.com) and a theme based on [Hyde](http://hyde.getpoole.com) which is based on [Poole](http://getpoole.com).

If you are interested, you can use some of the formatting I have employed.

- I generate a tag list and page by using the [tags.html](https://github.com/cudmore/cudmore.github.io/blob/master/tags.html) file. Each post specifies its tags in its yaml frontmatter like this...

~~~
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
~~~

- I generate an archive page with [archive.md](https://github.com/cudmore/cudmore.github.io/blob/master/archive.md).

- I generate navigation links to pre/next post at the bottom of each blog post using [_layouts/post.html](https://github.com/cudmore/cudmore.github.io/blob/master/_layouts/post.html)


## Authors

**Robert Cudmore**  
- <https://github.com/cudmore>  
- <http://robertcudmore.org>

Hyde was written by **Mark Otto**  
- <https://github.com/mdo>  
- <https://twitter.com/mdo>

## License

Open sourced under the [MIT license](LICENSE.md).
