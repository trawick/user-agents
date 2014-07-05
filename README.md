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

The first flavor is useful on Google App Engine, where you get https://appid.appspot.com/ for free, https://foo.customdomain.com/ (SNI only) for free or very cheap, and you pay out the nose for a virtual IP.  You want SSL, of course; redirect SNI-capable clients to your SNI-only custom domain, and redirect non-SNI-capable clients (or those you can't identify) to appspot.com.

