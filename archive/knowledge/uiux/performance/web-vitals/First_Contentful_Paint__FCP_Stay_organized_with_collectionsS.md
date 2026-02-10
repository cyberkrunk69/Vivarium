# First Contentful Paint (FCP)Stay organized with collectionsSave and categorize content based on your preferences.

Source: https://web.dev/articles/fcp

---

- [Home](https://web.dev/)
- [Articles](https://web.dev/articles)

# First Contentful Paint (FCP) Stay organized with collections Save and categorize content based on your preferences.

![Philip Walton](https://web.dev/images/authors/philipwalton.jpg)

Philip Walton

## What is FCP?

First Contentful Paint (FCP) measures the time from when the user first navigated to the page to when any part of the page's content is rendered on the screen. For this metric, "content" refers to text, images (including background images), `<svg>` elements, or non-white `<canvas>` elements.

![FCP timeline from google.com](/static/articles/fcp/image/fcp-timeline-googlecom.png)

In this load timeline, FCP happens in the second frame, because that's when the first text and image elements are rendered to the screen.

In the loading timeline depicted in the preceding image, FCP happens in the second frame, as that's when the first text and image elements are rendered to the screen.

You'll notice that though some of the content has rendered, not all of it has rendered. This is an important distinction to make between *First* Contentful Paint and [*Largest* Contentful Paint (LCP)](/articles/lcp)—which aims to measure when the page's main contents have finished loading.

### What is a good FCP score?

To provide a good user experience, sites should strive to have a First Contentful Paint of **1.8 seconds** or less. To ensure you're hitting this target for most of your users, a good threshold to measure is the **75th percentile** of page loads, segmented across mobile and desktop devices.

![Good FCP values are 1.8 seconds or less, poor values are greater than 3.0 seconds, and anything in between needs improvement](/static/articles/fcp/image/good-fcp-values-are-18-s-421f9e1a2cc56.svg)

Good FCP values are 1.8 seconds or less. Poor values are greater than 3.0 seconds

## How to measure FCP

FCP can be measured [in the lab](/articles/user-centric-performance-metrics#lab) or [in the field](/articles/user-centric-performance-metrics#field), and it's available in the following tools:

### Field tools

- [PageSpeed Insights](https://pagespeed.web.dev/)
- [Chrome User Experience
  Report](https://developer.chrome.com/docs/crux)
- [Search Console (Speed
  Report)](https://webmasters.googleblog.com/2019/11/search-console-speed-report.html)
- [`web-vitals` JavaScript library](https://github.com/GoogleChrome/web-vitals)

### Lab tools

- [Lighthouse](https://developer.chrome.com/docs/lighthouse/overview)
- [Chrome DevTools](https://developer.chrome.com/docs/devtools)
- [PageSpeed Insights](https://pagespeed.web.dev/)

### Measure FCP in JavaScript

To measure FCP in JavaScript, you can use the [Paint Timing API](https://w3c.github.io/paint-timing/). The following example shows how to create a [`PerformanceObserver`](https://developer.mozilla.org/docs/Web/API/PerformanceObserver) that listens for a `paint` entry with the name `first-contentful-paint` and logs it to the console.

```
new PerformanceObserver((entryList) => {
  for (const entry of entryList.getEntriesByName('first-contentful-paint')) {
    console.log('FCP candidate:', entry.startTime, entry);
  }
}).observe({type: 'paint', buffered: true});
```

In the previous code snippet, the logged `first-contentful-paint` entry will tell you when the first contentful element was painted. However, in some cases this entry is not valid for measuring FCP.

The following section lists the differences between what the API reports and how the metric is calculated.

#### Differences between the metric and the API

- The API will dispatch a `first-contentful-paint` entry for pages loaded in a background tab, but those pages should be ignored when calculating FCP (first paint timings should only be considered if the page was in the foreground the entire time).
- The API does not report `first-contentful-paint` entries when the page is restored from the [back/forward cache](/articles/bfcache#impact_on_core_web_vitals), but FCP should be measured in these cases since users experience them as distinct page visits.
- The API [may not report paint timings from cross-origin iframes](https://w3c.github.io/paint-timing/#:%7E:text=cross-origin%20iframes), but to properly measure FCP you should consider all frames. Sub-frames can use the API to report their paint timings to the parent frame for aggregation.
- The API measures FCP from navigation start, but for [prerendered pages](https://developer.chrome.com/docs/web-platform/prerender-pages) FCP should be measured from [`activationStart`](https://developer.mozilla.org/docs/Web/API/PerformanceNavigationTiming/activationStart) since that corresponds to the FCP time as experienced by the user.

Rather than memorizing all these subtle differences, developers can use the [`web-vitals` JavaScript library](https://github.com/GoogleChrome/web-vitals) to measure FCP, which handles these differences for you (where possible—note the iframe issue is not covered):

```
import {onFCP} from 'web-vitals';

// Measure and log FCP as soon as it's available.
onFCP(console.log);
```

You can refer to [the source code for `onFCP()`](https://github.com/GoogleChrome/web-vitals/blob/main/src/onFCP.ts) for a complete example of how to measure FCP in JavaScript.

## How to improve FCP

To learn how to improve FCP for a specific site, you can run a Lighthouse performance audit and pay attention to any specific [opportunities](https://developer.chrome.com/docs/lighthouse/performance/#opportunities) or [diagnostics](https://developer.chrome.com/docs/lighthouse/performance/#diagnostics) the audit suggests.

To learn how to improve FCP in general (for any site), refer to the following performance guides:

- [Eliminate render-blocking resources](https://developer.chrome.com/docs/lighthouse/performance/render-blocking-resources)
- [Minify CSS](https://developer.chrome.com/docs/lighthouse/performance/unminified-css)
- [Remove unused CSS](https://developer.chrome.com/docs/lighthouse/performance/unused-css-rules)
- [Remove unused JavaScript](https://developer.chrome.com/docs/lighthouse/performance/unused-javascript)
- [Preconnect to required origins](https://developer.chrome.com/docs/lighthouse/performance/uses-rel-preconnect)
- [Reduce server response times (TTFB)](/articles/ttfb)
- [Avoid multiple page redirects](https://developer.chrome.com/docs/lighthouse/performance/redirects)
- [Preload key requests](https://developer.chrome.com/docs/lighthouse/performance/uses-rel-preload)
- [Avoid enormous network payloads](https://developer.chrome.com/docs/lighthouse/performance/total-byte-weight)
- [Serve static assets with an efficient cache policy](https://developer.chrome.com/docs/lighthouse/performance/uses-long-cache-ttl)
- [Avoid an excessive DOM size](https://developer.chrome.com/docs/lighthouse/performance/dom-size)
- [Minimize critical request depth](https://developer.chrome.com/docs/lighthouse/performance/critical-request-chains)
- [Ensure text remains visible during webfont load](https://developer.chrome.com/docs/lighthouse/performance/font-display)
- [Keep request counts low and transfer sizes small](https://developer.chrome.com/docs/lighthouse/performance/resource-summary)

## Changelog

Occasionally, bugs are discovered in the APIs used to measure metrics, and sometimes in the definitions of the metrics themselves. As a result, changes must sometimes be made, and these changes can show up as improvements or regressions in your internal reports and dashboards.

To help you manage this, all changes to either the implementation or definition of these metrics will be surfaced in this [Changelog](https://chromium.googlesource.com/chromium/src/+/main/docs/speed/metrics_changelog/fcp.md).

If you have feedback for these metrics, you can provide it in the [web-vitals-feedback Google group](https://groups.google.com/g/web-vitals-feedback).

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2023-12-06 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2023-12-06 UTC."],[],[]]