---
layout: post
title: "Keeping in sync with github"
category: post
date: 2016-03-26 00:00:00
tags:
- jekyll
- github
---



The cloud is 'just someone else's computer'. And most of it is just 'someone else's fileserver'.

Problems arise when you actually run code in the cloud as you do when you have github autogenerate a static blog using jekyll.

Github recently upgraded to Jekyll 3 and switched their markdown parser to kramdown.

<IMG SRC="/images/thereisnocloud.png" WIDTH="275" ALIGN="RIGHT">

These changes completely broke all my github maintained blogs and documentation sites

- cudmore
- mapmanager
- vacular analysis

### Make sure your local jekyll is the same as the github jekyll

See [Github help][1] to set up your local version of jekyll to match the github version of jekyll

### Add a Gemfile

Make a file named 'Gemfile' in the root directory of your blog and put this text into the file...

    source 'https://rubygems.org'
    gem 'github-pages'

### Update to jekyll 3 and make sure all your gems are up to date

    ruby --version # rube >2.0 is required
    sudo gem install bundler # github suggests using bundler to keep all your gems in sync
    sudo gem install jekyll # this should get jekyll 3.x
    bundle install # run this in the directory with the above Gemfile
    bundle exec jekyll build --safe # run jekyll one to update dependencies

### Put a space in all of the mardown headers

    find . -type f -name '*.md' -exec sed -i '' "s/\()\([a-zA-Z1-9]\)/\1 \2/g" {} +

### Fix links to images

Search and replace

    SRC="../images #search for this
    SRC="images #replace with this
 
### Fix code fences
   
    ~~~ # search for this
    ``` # replace with this
    
### Update _config.yml

Remove all reference to markdown parsers and only specify kramdown 

    markdown: kramdown

### Here is the lame part

'jekyl serve' returns this error:

	roberts-Mac-Pro:cudmore.github.io cudmore$ jekyll serve
	WARN: Unresolved specs during Gem::Specification.reset:
		  jekyll-watch (~> 1.1)
	WARN: Clearing out unresolved specs.
	Please report a bug if this causes problems.
	Configuration file: /Users/cudmore/Sites/cudmore.github.io/_config.yml
	  Dependency Error: Yikes! It looks like you don't have jekyll-paginate or one of its dependencies installed. In order to use Jekyll as currently configured, you'll need to install this gem. The full error message from Ruby is: 'cannot load such file -- jekyll-paginate' If you run into trouble, you can find helpful resources at http://jekyllrb.com/help/! 
	jekyll 3.1.2 | Error:  jekyll-paginate

to run jekyll i need to use

    bundle exec jekyll serve

### Additional junk (20160420)

On OSX 10.10.1 Yosemite I was getting errors in 'nokogiri' not findong 'libxml2' when I did 'gem install'. See [here][2]. In general, follow nokogiri install [documentation][4]

 - Remove macports [following][3].
     sudo port -fp uninstall installed
 - Install homebrew
 - Install gcc (this installed gcc-5.3.0)
     brew install gcc
 - Proceed as normal
    sudo gem install nokogiri
    bundle install
 - **REMEMBER** to run jekyll locally with
    bundle exec jekyll serve

[1]: https://help.github.com/articles/setting-up-your-pages-site-locally-with-jekyll/
[2]: https://github.com/sparklemotion/nokogiri/wiki/What-to-do-if-libxml2-is-being-a-jerk
[3]: https://guide.macports.org/chunked/installing.macports.uninstalling.html
[4]: http://www.nokogiri.org/tutorials/installing_nokogiri.html#mac_os_x
