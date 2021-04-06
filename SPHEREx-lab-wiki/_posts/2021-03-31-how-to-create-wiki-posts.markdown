---
layout: post
title:  "How-To Create Wiki Posts in Jekyll"
date:   2021-03-31 09:09:44 -0800
categories: jekyll update
---
Creating new posts in Jekyll is easy, but there are a few rules,
* In the `_drafts` directory create a new file named according to the following
format; date `YEAR-MONTH-DAY-title.md` where title words are separated by dashes
 (.markdown is also ok).
For example, this post is named `2021-03-31-how-to-create-wiki-posts.markdown`
* Posts must begin with "front-matter", consisting of (for lines of) metadata
that make sure the post shows up in the right place in the right format.
It begins and ends with three dashes. The metadata are layout, title, date, and
categories.  For example, this post's metada is
{% highlight jekyll %}
---
layout: post
title:  "How-To Create Wiki Posts in Jekyll"
date:   2021-03-31 09:09:44 -0800
categories: jekyll update
---
{% endhighlight %}
* Text should be written in the kramdown version of Markdown.  For more information [see this cheatsheet](https://kramdown.gettalong.org/quickref.html)
* When posts are completed, move them from `_drafts` to `_posts` directories.

You can rebuild the site in many different ways, but the most common way is to run `jekyll serve`, which launches a web server and auto-regenerates your site when a file is updated.


Jekyll offers powerful support for code snippets:

{% highlight ruby %}
def print_hi(name)
  puts "Hi, #{name}"
end
print_hi('Tom')
#=> prints 'Hi, Tom' to STDOUT.
{% endhighlight %}

Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll Talk][jekyll-talk].

[jekyll-docs]: https://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
