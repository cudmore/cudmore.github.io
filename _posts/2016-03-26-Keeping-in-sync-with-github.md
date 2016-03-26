---
layout: post
title: "Keeping in sync with github"
category: post
date: 2016-03-26 22:01:06
tags:
- jekyll
- github
---

The cloud is 'just someone else's computer'. And most of it is just 'someone else's fileserver'.

Problems arise when you actually run code in the cloud as you do when you have github autogenerate a static blog using jekyll.

Github recently upgraded to Jekyll 3 and switched their markdown parser to kramdown.

These changes completely broke all my github maintained blogs and documentation sites

- cudmore
- mapmanager
- vacular analysis

### Make sure your local jekyll is the same as the github jekyll

See [Github help][1] to set up your local version of jekyll to match the github version of jekyll

- make a Gemfile

    source 'https://rubygems.org'
    gem 'github-pages'

- run some commands

    ruby --version # rube >2.0 is required
    sudo gem install bundler # github suggests using bundler to keep all your gems in sync
    sudo gem install jekyll # this should get jekyll 3.x
    bundle install # run this in the directory with the above Gemfile
    bundle exec jekyll build --safe # run jekyll one to update dependencies

### put a space in all of the mardown headers

>> find . -type f -name '*.md' -exec sed -i '' "s/\()\([a-zA-Z1-9]\)/\1 \2/g" {} +

### Fix links to images

Search and replace

    SRC="../images #search for this
    SRC="images #replace with this
 
### Fix code fences
   
    ~~~ # search for this
    ``` # replace with this
    
### Update _config.yml

Remove all reference to markdown parsers and only specify kramdown 

>> markdown: kramdown

[1]: https://help.github.com/articles/setting-up-your-pages-site-locally-with-jekyll/