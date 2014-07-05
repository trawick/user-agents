user-agents
===========

Heuristics to identify capabilities of HTTP user agents

The initial concern is whether or not a user agent supports SNI, in order to support the following
type of server-side logic:

```
    if browser-supports-SNI:
        redirect to https://pretty.com/
    else:
        redirect to https://ugly.com/
```

or

```
    if browser-supports-SNI:
        redirect to https://foo.com/
    else:
        pass
```

The first flavor is useful on Google App Engine, where you get https://appid.appspot.com/ for free, https://foo.customdomain.com/ (SNI only) for free or for very cheap, and you pay $39.00/month or so for a dedicated IP, which allows all browsers to connect to your custom domain over SSL/TLS.  You want SSL/TLS, of course; redirect SNI-capable clients to your SNI-only custom domain, and redirect non-SNI-capable clients (or those you can't identify) to appspot.com.

A bit of a bummer: Some browsers that don't support SNI may not support the signer of your certificate.  E.g., my 1st generation iPod touch with iOS 3.1.3 doesn't support SNI and doesn't support (out of the box) the signer of the *.appspot.com certificate, so it is just plain too old to have a good user experience.

checking for features besides SNI
=================================

Not here.  Another feature I check for in an application I wrote is "mobile" .  I currently use code from here:

```
# from http://detectmobilebrowser.com/
# Ported by Matt Sullivan http://sullerton.com/2011/03/django-mobile-browser-detection-middleware/
```

That would be nice to integrate into the Python class, but I haven't checked the license of that stuff.

permanent concerns
==================

Browsers may let users disable TLS support.  SNI doesn't work without TLS support.  Perhaps some browsers modify user-agent strings, but I don't know about that and the code certainly doesn't handle it.

current status
==============

What did the dog say?  "Ruff, ruff."

The implementation extends only a bit beyond what I can test myself.

It is definitely better than some garbage floating around on the 'net.  But it does not even implement the basic support information outlined in Wikipedia.

so why did you put this garbage on the 'net?
============================================

* There's value in seeing some of the same information as elsewhere with honest caveats.
* You can send me pull requests and make it better for everyone, unlike some closed blog post or Q&A article from 2011.
* Somebody out there can see this and tell me there's already a great implementation that I couldn't find myself, which would be thrilling.  (Being willing to look stupid is a great way to learn.)
