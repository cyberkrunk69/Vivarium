# Time to First Byte (TTFB)Stay organized with collectionsSave and categorize content based on your preferences.

Source: https://web.dev/articles/ttfb

---

- [Home](https://web.dev/)
- [Articles](https://web.dev/articles)

# Time to First Byte (TTFB) Stay organized with collections Save and categorize content based on your preferences.

![Barry Pollard](https://web.dev/images/authors/tunetheweb.jpg)

Barry Pollard

![Jeremy Wagner](https://web.dev/images/authors/jlwagner-v6.jpg)

Jeremy Wagner

Published: October 26, 2021, Last updated: November 18, 2025

## What is TTFB?

TTFB is a metric that measures the time between starting navigating to a page and when the first byte of a response begins to arrive.

![A visualization of network request timings. The timings from left to right are Redirect, Service Worker Init, Service Worker Fetch event, HTTP Cache, DNS, TCP, Request, Early Hints (103), Response (which overlaps with Prompt for Unload), Processing, and Load. The associated timings are redirectStart and redirectEnd, fetchStart, domainLookupStart, domainLookupEnd, connectStart, secureConnectionStart, connectEnd, requestStart, interimResponseStart, responseStart, unloadEventStart, unloadEventEnd, responseEnd, domInteractive, domContentLoadedEventStart, domContentLoadedEventEnd, domComplete, loadEventStart, and loadEventEnd.](/static/articles/ttfb/image/performance-navigation-timing-timestamp-diagram.svg)

A diagram of network request phases and their associated timings. TTFB measures the elapsed time between `startTime` and `responseStart`.

TTFB is the sum of the following request phases:

- Redirect time
- Service worker startup time (if applicable)
- DNS lookup
- Connection and TLS negotiation
- Request, up until the point at which the first byte of the response has arrived

Reducing latency in connection setup time and on the backend can lower your TTFB.

### TTFB and Early Hints

The introduction of [103 Early Hints](https://developer.chrome.com/docs/web-platform/early-hints) causes some confusion as to what "first byte" TTFB measures. The 103 Early Hints counts as the "first bytes". The [`finalResponseHeadersStart`](https://developer.mozilla.org/docs/Web/API/PerformanceResourceTiming/finalResponseHeadersStart) is an additional timing entry to `responseStart` that measures the the start of the final document response (typically an HTTP 200 response) to be measured.

Early Hints is just a newer example of responding early. Some servers allow early flushing of the document response to happen before the main body is available—either with just the HTTP headers, or with the `<head>` element, both of which could be considered similar in effect to Early Hints. This is another reason why all these are measured as `reponseStart` and so TTFB.

There is real value in sending back data early if the full response is going to take some more time. However, this does make it difficult to compare TTFB across different platforms or technologies depending on what features they use, and how that impacts the TTFB measurement being used. What is most important is to understand what the measure the tool you are using measures and how that is affected by the platform being measured.

### What is a good TTFB score?

Because TTFB precedes [user-centric metrics](/articles/user-centric-performance-metrics) such as [First Contentful Paint (FCP)](/articles/fcp) and [Largest Contentful Paint (LCP)](/articles/lcp), it's recommended that your server responds to navigation requests quickly enough so that the **75th percentile** of users experience an [FCP within the "good" threshold](/articles/fcp#what_is_a_good_fcp_score). As a rough guide, most sites should strive to have a TTFB of **0.8 seconds** or less.

![Good TTFB values are 0.8 seconds or less, poor values are greater than 1.8 seconds, and anything in between needs improvement](/static/articles/ttfb/image/good-ttfb-values-are-08-ca73d93f5df2d.svg)

Good TTFB values are 0.8 seconds or less, and poor values are greater than 1.8 seconds.

## How to measure TTFB

TTFB can be measured in [the lab](/articles/user-centric-performance-metrics#in_the_lab) or in [the field](/articles/user-centric-performance-metrics#in_the_field) in the following ways.

### Field tools

- [Chrome User Experience Report](https://developer.chrome.com/docs/crux)
- [`web-vitals` JavaScript library](https://github.com/GoogleChrome/web-vitals)

### Lab tools

- In the [network panel](https://developer.chrome.com/docs/devtools/network) of Chrome's DevTools
- [WebPageTest](https://www.webpagetest.org/)

### Measure TTFB in JavaScript

You can measure the TTFB of [navigation requests](https://developer.mozilla.org/docs/Web/API/Request/mode) in the browser with the [Navigation Timing API](https://developer.mozilla.org/docs/Web/API/Navigation_timing_API). The following example shows how to create a [`PerformanceObserver`](https://developer.mozilla.org/docs/Web/API/PerformanceObserver) that listens for a `navigation` entry and logs it to the console:

```
new PerformanceObserver((entryList) => {
  const [pageNav] = entryList.getEntriesByType('navigation');

  console.log(`TTFB: ${pageNav.responseStart}`);
}).observe({
  type: 'navigation',
  buffered: true
});
```

The [`web-vitals` JavaScript library](https://github.com/GoogleChrome/web-vitals) can also measure TTFB in the browser more succinctly:

```
import {onTTFB} from 'web-vitals';

// Measure and log TTFB as soon as it's available.
onTTFB(console.log);
```

### Measure resource requests

TTFB can also be measured on *all* requests, not just navigation requests. In particular, resources hosted on cross-origin servers can introduce latency due to the need to set up connections to those servers.

To measure TTFB for resources in the field, use the [Resource Timing API](https://developer.mozilla.org/docs/Web/API/Resource_Timing_API/Using_the_Resource_Timing_API) within a `PerformanceObserver`:

```
new PerformanceObserver((entryList) => {
  const entries = entryList.getEntries();

  for (const entry of entries) {
    // Some resources may have a responseStart value of 0, due
    // to the resource being cached, or a cross-origin resource
    // being served without a Timing-Allow-Origin header set.
    if (entry.responseStart > 0) {
      console.log(`TTFB: ${entry.responseStart}`, entry.name);
    }
  }
}).observe({
  type: 'resource',
  buffered: true
});
```

The previous code snippet is similar to the one used to measure the TTFB for a navigation request, except instead of querying for `'navigation'` entries, you query for `'resource'` entries instead. It also accounts for the fact that some resources loaded from the primary origin may return a value of `0`, since the connection is already open, or a resource is instantaneously retrieved from a cache.

## How to improve TTFB

For guidance on improving your site's TTFB, see our in-depth guide to [optimizing TTFB](/articles/optimize-ttfb).

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-11-28 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-11-28 UTC."],[],[]]