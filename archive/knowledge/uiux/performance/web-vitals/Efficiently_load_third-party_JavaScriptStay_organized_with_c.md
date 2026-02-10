# Efficiently load third-party JavaScriptStay organized with collectionsSave and categorize content based on your preferences.

Source: https://web.dev/articles/efficiently-load-third-party-javascript

---

- [Home](https://web.dev/)
- [Articles](https://web.dev/articles)

# Efficiently load third-party JavaScript Stay organized with collections Save and categorize content based on your preferences.

![Milica Mihajlija](https://web.dev/images/authors/mihajlija.jpg)

Milica Mihajlija

If a third-party script is [slowing down](/articles/third-party-javascript) your
page load, you have two options to improve performance:

- Remove it if it doesn't add clear value to your site.
- Optimize the loading process.

This post explains how to optimize the loading process of third-party scripts
with the following techniques:

- Using the `async` or `defer` attribute on `<script>` tags
- Establishing early connections to required origins
- Lazy loading
- Optimizing how you serve third-party scripts

## Use `async` or `defer`

Because [synchronous scripts](/articles/third-party-javascript) delay DOM
construction and rendering, you should always load third-party scripts
asynchronously unless the script has to run before the page can be rendered.

The `async` and `defer` attributes tell the browser that it can go on parsing
the HTML while loading the script in the background, then execute the script
after it loads. This way, script downloads don't block DOM construction or page
rendering, letting the user see the page before all scripts have finished
loading.

```
<script async src="script.js">

<script defer src="script.js">
```

The difference between `async` and `defer` attributes is when the browser
executes the scripts.

### `async`

Scripts with the `async` attribute execute at the first opportunity after they
finish downloading and before the window's
[load](https://developer.mozilla.org/docs/Web/Events/load) event. This means
it's possible (and likely) that `async` scripts won't run in the order in which
they appear in the HTML. It also means they can interrupt DOM building if they
finish downloading while the parser is still at work.

![Diagram of parser blocking script with async attribute](/static/articles/efficiently-load-third-party-javascript/image/diagram-parser-blocking-020263bc7658c.png)

Scripts with `async` can still block
HTML parsing.

### `defer`

Scripts with the `defer` attribute execute after HTML parsing is completely
finished, but before the
[`DOMContentLoaded`](https://developer.mozilla.org/docs/Web/Events/DOMContentLoaded)
event. `defer` ensures that scripts run in the order they appear in the HTML and
don't block the parser.

![Diagram of parser flow with a script with defer attribute](/static/articles/efficiently-load-third-party-javascript/image/diagram-parser-flow-a-s-f9a9ef751f974.png)

Scripts with `defer` wait to run until
the browser is done parsing the HTML.

- Use `async` if it's important to have the script run earlier in the loading
  process.
- Use `defer` for less critical resources, such as a video player that's below
  the fold.

Using these attributes can significantly speed up page load. For example,
[Telegraph deferred all their scripts](https://medium.com/p/a0a1000be5#4123),
including ads and analytics, and improved the ad loading time by an average of
four seconds.

## Establish early connections to required origins

You can save 100–500 ms by
[establishing early connections](/articles/preconnect-and-dns-prefetch) to
important third-party origins.

Two [`<link>`](https://developer.mozilla.org/docs/Web/HTML/Element/link) types,
`preconnect` and `dns-prefetch`, can help here:

### `preconnect`

`<link rel="preconnect">` tells the browser that your page wants to establish a
connection to another origin, and that you'd like the process to start as soon
as possible. When the browser requests a resource from the pre-connected origin,
the download starts immediately.

```
<link rel="preconnect" href="https://cdn.example.com">
```

### `dns-prefetch`

`<link rel="dns-prefetch>` handles a small subset of what
`<link rel="preconnect">` handles. Establishing a connection involves the DNS
lookup and TCP handshake, and for secure origins, TLS negotiations.
`dns-prefetch` tells the browser to only resolve the DNS of a specific domain before it has been explicitly called.

The `preconnect` hint is best used for only the most critical connections. For
less important third-party domains, use `<link rel=dns-prefetch>`.

```
<link rel="dns-prefetch" href="http://example.com">
```

[Browser support for `dns-prefetch`](https://caniuse.com/#search=dns-prefetch)
is slightly different from [`preconnect` support](https://caniuse.com/#search=preconnect),
so `dns-prefetch` can serve as a fallback for browsers that don't support
`preconnect`. Use separate link tags to implement this safely:

```
<link rel="preconnect" href="http://example.com">
<link rel="dns-prefetch" href="http://example.com">
```

## Lazy-load third-party resources

Embedded third-party resources can significantly slow down page loading if
they're constructed poorly. If they aren't critical, or are below the fold
(that is, if users have to scroll to view them), lazy loading is a good way to
improve page speed and paint metrics. This way, users get the main page content
faster and have a better experience.

![A diagram of a webpage shown on a mobile device with scrollable content extending beyond the screen. The content that's below-the-fold is desaturated because it's not loaded yet.](/static/articles/efficiently-load-third-party-javascript/image/a-diagram-a-webpage-show-0c848a2212482.png)

Lazy load content below the fold.

One effective approach is to lazy-load third-party content after the main page
content loads. Ads are a good candidate for this approach.

Ads are an important source of income for many sites, but users come for the
content. By lazy loading ads and delivering the main content faster, you can
increase the overall viewability percentage of an ad. For example, MediaVine
switched to [lazy-loading ads](https://www.mediavine.com/lazy-loading-ads-mediavine-ads-load-200-faster/)
and saw a 200% improvement in page load speed. Google Ad Manager has documentation
on how to [lazy load ads](https://developers.google.com/publisher-tag/reference#googletag.PubAdsService_enableLazyLoad).

You can also set third-party content to load only when users first scroll to
that section of the page.

[Intersection Observer](https://developer.chrome.com/blog/intersectionobserver)
is a browser API that efficiently detects when an element enters or exits the
browser's viewport, and you can use it to implement this technique.
[lazysizes](/use-lazysizes-to-lazyload-images) is a popular JavaScript library
for lazy loading images and [`iframes`](http://afarkas.github.io/lazysizes/#examples).
It supports YouTube embeds and
[widgets](https://github.com/aFarkas/lazysizes/tree/gh-pages/plugins/unveilhooks).
It also has [optional support](https://github.com/aFarkas/lazysizes/blob/097a9878817dd17be3366633e555f3929a7eaaf1/src/lazysizes-intersection.js)
for Intersection Observer.

Using the [`loading` attribute for lazy loading images and iframes](/articles/browser-level-image-lazy-loading)
is a great alternative to JavaScript techniques, and it has recently become
available in Chrome 76!

## Optimize how you serve third-party scripts

The following are some recommended strategies for optimizing your use of
third-party scripts.

### Third-party CDN hosting

It's common for third-party vendors to provide URLs for JavaScript files they
host, usually on a [content delivery network (CDN)](https://en.wikipedia.org/wiki/Content_delivery_network).
The benefits of this approach are that you can get started quickly—just
copy and paste the URL—and there's no maintenance overhead. The
third-party vendor handles server configuration and script updates.

But because they aren't on the same origin as the rest of your resources,
loading files from a public CDN comes with a network cost. The browser needs to
perform a DNS lookup, establish a new HTTP connection, and, on secure origins,
perform an SSL handshake with the vendor's server.

When you use files from third-party servers, you rarely have control over
caching. Relying on someone else's caching strategy might cause scripts to be
unnecessarily re-fetched from the network too often.

### Self-host third-party scripts

Self-hosting third-party scripts is an option that gives you more control over a
script's loading process. By self-hosting you can:

- Reduce DNS lookup and round-trip times.
- Improve [HTTP caching](/articles/http-cache) headers.
- Take advantage of [HTTP/2](/articles/performance-http2), or the newer HTTP/3.

For example, Casper managed to [shave 1.7 seconds](https://medium.com/caspertechteam/we-shaved-1-7-seconds-off-casper-com-by-self-hosting-optimizely-2704bcbff8ec)
off load times by self-hosting an A/B testing script.

Self-hosting comes with one big downside though: scripts can go out of date and
won't get automatic updates when there's an API change or a security fix.

### Use service workers to cache scripts from third-party servers

You can use [service workers to cache scripts from third-party servers](https://developer.chrome.com/docs/workbox/caching-resources-during-runtime#cross-origin-considerations)
as an alternative to self-hosting. This gives you greater control over caching,
while retaining the benefits of third-party CDNs.

You can control how often scripts are re-fetched from the network and
create a loading strategy that throttles requests for non-essential,
third-party resources until a user arrives at a key interaction on the page.
With `preconnect`, you can establish early connections and also help
mitigate the network costs.

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2019-08-14 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2019-08-14 UTC."],[],[]]