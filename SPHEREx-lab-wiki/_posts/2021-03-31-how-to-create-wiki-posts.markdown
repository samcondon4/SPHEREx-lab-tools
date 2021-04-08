---
layout: post
title:  "How-To Create Wiki Posts in Jekyll"
date:   2021-03-31
categories: [jekyll, update]
---
The wiki is designed with two parts; Posts and Navigation.  Post are notebook-like blog posts that are searchable, grouped by keywords, and displayed chronologically on the first page.
Navigation points to specific information related to hardware, software, schedules, and FAQ.

## New posts
Creating new posts is easy but there are a few unbreakable rules,
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
categories: [jekyll, update]
---
{% endhighlight %}
* Text should be written in the kramdown version of Markdown.  For more information [see this cheatsheet](https://kramdown.gettalong.org/quickref.html)
* When posts are completed, move them from `_drafts` to `_posts` directories.

#### Layout
Layout is the template to use for the document. For standard blog-like documents (90% of our docs) the layout we will use is `post`.  Other templates (or make your own!) can be found in `_posts`.

#### Date
Date format is 2021-03-31 09:09:44 -0800, where the time (in 24 hours) and timezone are optional.

#### Keywords/categories
The addition of keywords (aka catagories) in the front-matter automatically makes the document visible in the "Articles by Category" section.  

### Navigation
The left column of the site links to Navigation.  This is still under construction.  

#### Building the site
You can rebuild the site in many different ways, but the most common way is to run `jekyll serve`, which launches a web server and auto-regenerates your site when a file is updated.

### Markdown Syntax

Posts are written in the [KRAMDOWN](https://kramdown.gettalong.org/quickref.html) version of Markdown.  [This link](https://kramdown.gettalong.org/quickref.html) contains a cheatsheet.

### Hyperlinks
Hyperlinks are easy; in square brackets write the text, immediately followed by round brackets containing the link. E.g., for [Zappos](https://www.zappos.com/) simply write
```
[Zappos](https://www.zappos.com/)
```

Another way is to put all the links in one place (e.g., the bottom) and use square brackets to retrieve them, for example
```
Check out the [Jekyll docs][jekyll-docs] for more info on how to get the most out of Jekyll. File all bugs/feature requests at [Jekyll’s GitHub repo][jekyll-gh]. If you have questions, you can ask them on [Jekyll Talk][jekyll-talk].

# Links
[jekyll-docs]: http://jekyllrb.com/docs/home
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-talk]: https://talk.jekyllrb.com/
```

### Images
Store images in the images directory, and then link to them via
```
![image-title-here](/images/spherex_logo.png){:class="img-responsive"}
```
![Spherex-Logo](/images/spherex_logo.png){:class="img-responsive"}.  Don't forget to put the ! in front or it will just be a hyperlink.  


### Footnotes
You can add footnotes easily, for example, if you want to cite a paper like [Chung et al. 2020][Chung20][^1].

[^1]: [Forecasting [C II] line-intensity mapping measurements between the end of reionization and the epoch of galaxy assembly, Dongwoo T Chung, Marco P Viero, Sarah E Church, Risa H Wechsler 2020, ApJ, 892, 51](https://iopscience.iop.org/article/10.3847/1538-4357/ab798f)
[Chung20]: Forecasting [C II] line-intensity mapping measurements between the end of reionization and the epoch of galaxy assembly, Dongwoo T Chung, Marco P Viero, Sarah E Church, Risa H Wechsler 2020, ApJ, 892, 51](https://iopscience.iop.org/article/10.3847/1538-4357/ab798f

### Code Snippets
Jekyll offers support for code snippets for a wide range of languages, either by starting/ending
a snippet with three back quotes followed by the language name;


```python
import os
import sys
import pdb
import numpy as np
import datetime as datetime

sys.path.append(r'..\pylab')

from pylablib.utils.parameters import *
from pylablib.instruments.powermaxusb import PowermaxUSB
from pylablib.instruments.serial_motor_dpy50601 import DPY50601

class SM:
	startState = 'waiting'
	init = False
	in_queue = False
	ready_to_store = False

	error_status = False

	def start(self):
		self.state = self.startState
		self.init_status = self.init
		self.data_in_queue = self.in_queue
		self.data_ready_to_store = self.ready_to_store
		self.errorStatus = self.error_status
		self.errorDict = {}
		self.metadata = {}


	def step(self, inp):
		(s, o) = self.getNextValues(self.state, inp)

		#pdb.set_trace()
		self.state = s

		return o

	def transduce(self, inputs):
		self.start()
		return [self.step(inp) for inp in inputs]
```
Or by containing code inside curly brackets/percent signs for languages including python

{% highlight python %}
def print_hi(name)
  print("Hi, %s", name)
print_hi('Sam')
#=> prints 'Hi, Tom' to STDOUT.
{% endhighlight %}

or Ruby:

{% highlight ruby %}
def print_hi(name)
  puts "Hi, #{name}"
end
print_hi('Tom')
#=> prints 'Hi, Tom' to STDOUT.
{% endhighlight %}

### Tables
Use | to separate table columns and --- or === or :---: to insert dividing lines.  
```
| Header1 | Header2 | Header3 |
|:--------|:-------:|--------:|
| cell1   | cell2   | cell3   |
| cell4   | cell5   | cell6   |
|----
| cell1   | cell2   | cell3   |
| cell4   | cell5   | cell6   |
|=====
| Foot1   | Foot2   | Foot3
{: rules="groups"}
```


| Header1 | Header2 | Header3 |
|:--------|:-------:|--------:|
| cell1   | cell2   | cell3   |
| cell4   | cell5   | cell6   |
|----
| cell1   | cell2   | cell3   |
| cell4   | cell5   | cell6   |
|=====
| Foot1   | Foot2   | Foot3
{: rules="groups"}

<hr>
