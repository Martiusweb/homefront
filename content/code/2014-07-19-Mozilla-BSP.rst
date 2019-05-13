I made a patch for Mozilla, and you can do it too
=================================================

:date: 19/07/2014
:slug: Mozilla-BSP
:category: Code
:summary: I will tell how I contributed code to Mozilla during a Bug Squashing Party.


In this article, I will tell how I contributed code to Mozilla during a Bug
Squashing Party. I hope to provide some tips and advice about how to start
contributing to a Mozilla project (or any other open-source project). I will
talk about Firefox and Servo, which, I think, are somehow representative of two
common ways of writing and submitting patches.

The bug squashing party was a two-days events which took place in the Paris
office of Mozilla. We were mentored by experienced contributors (actually,
employees) to fix bugs on Mozilla products. I always felt that contributing to
an open-source project was quite intimidating. I didn't want to bother people
with patches they could have written themselves faster or better. That's why I
decided to join the event, knowing that people would be available to help me.

Getting started
---------------

I wanted to be a bit proactive, and be ready to write code during the event, so
I built Firefox to hack stuff a few days before the event. I wanted to write a
patch that was trivial and that I could sail through once I could find my feet
in this huge codebase.

I started by looking for three things: the code, instructions about how to
build the project, and instructions about how to contribute. For a project as
large as Firefox, it's easy to find a lot of documentation using google, with
the downside that sometimes, it's outdated or slightly incorrect. For smaller
projects, github or bitbucket can be good entry points. Usually we can find a
``README`` or a ``CONTRIBUTING`` file in the repository.

Most of the technical documentation from Mozilla is located on MDN, the Mozilla
Developer Network. I spent around 15 minutes to compare several pages and check
their history (MDN is a wiki) to be sure to read stuff that were up to date.

The build system of Firefox is quite complex, but building firefox is easy
(`look at the build instructions <https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide/Build_Instructions>`_),
and there is plenty of documentation to get started in the `developer guide <https://developer.mozilla.org/en-US/docs/Mozilla/Developer_guide>`_.
It is not always that easy, and can be somewhat frustrating. Knowing that, I
chose to prepare my build a day or two before actually trying to write a patch,
in order not to blow all my motivation away.  It's easy to feel overwhelmed by
all the details I've to get familiar with, from the structure to the coding
style. I believe that managing my motivation when digging into an unknown code
base on my spare time is indeed important.

I wrote a patch that makes Firefox play a sound when the user adds a new
bookmark. It's not really interesting, but trying to do something trivial (even
if useless) allows to have a first "hands-on" experience.

.. admonition:: Take-aways

   * For a small project, start by looking on github, for a larger project,
     look for a wiki, use google, and check the date of the document you are
     reading to be sure it's up to date.
   * This first step takes some time, and building a project can be
     frustrating. Plan to do it something like a day or two before the moment
     when you want to write code, so you don't spend all your motivation on
     this step.
   * Write a first patch to get started, even if what you change is useless.
     For instance, you can change the text displayed somewhere, add a dummy
     button or echo a parameter in the console.

Writing a patch
---------------

I can not add a feature to Firefox as I would have done it to a small project.
For a software of that size, adding a feature is out of my reach while I'm sure
that a patch that fixes a bug can be useful to someone.

Mozilla, as many other projects, centralize everything in a bug tracker.
Experienced contributors often label some bugs as Good first bugs. They are
non-urgent bugs which are easy to solve, and often documented enough so a
newcomer can quickly understand what to do to solve it. Some bugs are also
mentored, which means that an experienced contributor is willing to assist
someone with less experience in solving it. That was the kind of bugs we where
looking for during the bug squashing party.

Now, I could search for such a bug in the big thing that is `bugzilla
<https://bugzilla.mozilla.org/>`_, but it's really messy (maybe even more than
the codebase itself). But thanks to `Bugs Ahoy <http://www.joshmatthews.net/bugsahoy/>`_
(an alternative frontend for bugzilla), finding mentored bugs is now piece of
cake.

I chose to work on Servo, because I had no experience with Rust (a new
programming language) and I was in a room with two of the main contributors. At
home, I would probably have chosen something easier, in a language I knew at
least a bit. I learned something here: whatever the bug you pick, you can be
100% sure that you will dig into code you don't know, that will do things you
have no idea how to implement, and use libraries and APIs you never heard of.
It's a bit intimidating, but it's where the magic happens: with a bit of
method, you will learn a lot! Just think about how rewarding it will be to have
one or two Eureka moments!

Bugs for Servo are not on Bugzilla but on github, along with the code (we can
still use Bugs Ahoy). I spent some time reading the description of most of the
bugs reported as easy. Some bugs were partially fixed by contributors who did
not finish the job, but I chose a fresh new bug.

The description of a bug is usually filled with details about the current
implementation and hints about where to start looking. Unfortunately at this
point I had no clue of what they were talking about, so I chose to read the
definition of the functions and methods they mentioned, then re-read comments
on the ticket 3 or 4 times.

I Used :code:`ag` (aka `the silver searcher <https://github.com/ggreer/the_silver_searcher>`_,
a faster grep) to look for function or class names that are mentioned in the
bug ticket. I sometimes tried to guess the name of a symbol I was looking for
(say :code:`HyperlinkElement` or :code:`AnchorElement` for the type
representing the :code:`<a>` element). Firefox and Servo (as well as many other
open source projects of this size) have dedicated tools that help to search for
symbols in the code. For instance `MXR (Mozilla Cross Reference) <http://mxr.mozilla.org/>`_
allows you to search for files, class or function names so you know where they
are defined and where they are used. If
you happen to work on a bug on mozilla-central, there is also `DXR <http://dxr.mozilla.org/>`_
available to play with. In addition to what can be done with MXR, it will let
you perform structural queries such as "Find all the callers of this function".
Also, instead of using a debugger, I simply printed variables and debug message
on the console (:code:`println!()`) to see if a code path was reached or to see
the value of a given variable.

After that, I *asked questions* to Josh Matthews, a mentor of the bug who was
in the room with us. I knew that I could ask questions on at least two
different channels: the comments of the bug and IRC. The latter is great to ask
questions hoping to get answers quickly.

I find especially useful to asks questions about the purpose of a piece of code
(Why is it here? Why does it do what it does instead of something else? Does it
do what I think it does?) or about features I might need but don't know if they
are available (Is there a code implementing a data structure I'll need? Is
there a method that perform basic checks on data?). At this point, it's not
likely that someone knows exactly how to solve the bug. If there was, the bug
would be solved. It's thus up to me find and try to implement a solution before
proposing it.

Submitting a patch to Servo is easy, since they follow the github
*pull-request* workflow. It's not that easy on Firefox, but now we know that we
can *ask*.

.. admonition:: Take-aways

   * On a large project, look for mentored and good first bugs: they have been
     selected by experienced people for new contributors.
   * If you want to contribute to Mozilla, use `Bugs Ahoy <http://www.joshmatthews.net/bugsahoy/>`_,
     not bugzilla.
   * You are not an expert, and you probably don't know a thing about what you
     will deal with at first. It's okay, that's how you'll learn!
   * Ask questions on IRC about existing code and things you don't understand,
     but try to find solutions by yourself.
   * Use simple command line tools, such as :code:`grep` or a better
     alternative. Large projects often provide a "Cross-reference" website
     (like `MXR <http://mxr.mozilla.org/>`_ or `DXR
     <http://dxr.mozilla.org/>`_). MXR allows to search for a symbol (function
     or class name, for instance) in the code.
   * Use the weapons you master: if you don't know how to use a debugger, use
     :code:`print` statements in the code to understand what's happening.


The Bug Squashing Party was awesome!
------------------------------------

Now, a final word about the Bug Squashing Party.

As far as I know, it's the first event of this kind organized by Mozilla, and
it was both a great and successful idea. Mozillians, ask the `mozilla
francophone community <http://mozfr.org/>`_ about their experience and organize
a bug squashing party in your city.

I enjoyed to discover that anyone can contribute, even those that were not
experienced at all. For instance, a friend of mine who only knew about PHP
added a couple of features to a tool using the API of Bugzilla. The tool was
written in Python, so someone who knew about Python helped him, even if he knew
nothing of bugzilla.

As of me, I don't know if I'll contribute much on mozilla projects on my spare
time. But I'm now more confident in what I can do to contribute to open source
projects, being something as simple as answering a question on a mailing list
or filling a bug. That's part of why I like Mozilla: they can give a lot to
open source, in subtle ways too.

As a final note, Nicholas Nethercote posted a note about `his first contribution to Servo <https://blog.mozilla.org/nnethercote/2014/07/10/dipping-my-toes-in-the-servo-waters/>`_, and it's worth a read.

`Discussion and comments on Hacker News <https://news.ycombinator.com/item?id=8068547>`_

.. admonition:: Acknowledgement

   I would like to thank `Clément Geiger <http://cgg.sexy>`_,
   `Paul Adenot <http://paul.cx>`_,
   `Jan Keromnes <http://jankeromnes.github.io/>`_
   and `Nicolas Silva <https://github.com/nical/>`_ who helped me to write this
   article.

