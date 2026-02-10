# Interaction to Next Paint (INP)Stay organized with collectionsSave and categorize content based on your preferences.

Source: https://web.dev/articles/inp

---

- [Home](https://web.dev/)
- [Articles](https://web.dev/articles)

# Interaction to Next Paint (INP) Stay organized with collections Save and categorize content based on your preferences.

![Jeremy Wagner](https://web.dev/images/authors/jlwagner-v6.jpg)

Jeremy Wagner

![Barry Pollard](https://web.dev/images/authors/tunetheweb.jpg)

Barry Pollard

Published: May 06, 2022, Last updated: September 2, 2025

Chrome usage data shows that 90% of a user's time on a page is spent *after* it loads, Thus, careful measurement of responsiveness *throughout* the page lifecycle is important. This is what the INP metric assesses.

Good responsiveness means that a page responds quickly to interactions. When a page responds to an interaction, the browser presents *visual feedback* in the next frame that it paints. Visual feedback tells you if, for example, an item you add to an online shopping cart is indeed being added, whether a mobile navigation menu has opened, if a login form's contents are being authenticated by the server, and so forth.

Some interactions naturally take longer than others, but for especially complex interactions, it's important to quickly present some initial visual feedback to tell the user that something is happening. The next frame that the browser will paint is the earliest opportunity to do this.

Therefore, the intent of INP is not to measure *all* the eventual effects of an interaction—such as network fetches and UI updates from other asynchronous operations)—but the time that the *next* paint is being blocked. By delaying visual feedback, users may get the impression that the page is not responding quickly enough, and INP was developed to help developers measure this part of the user experience.

In the following video, the example on the right gives immediate visual feedback that an accordion is opening. Poor responsiveness is demonstrated in example on the left, and how it can create poor user experiences.

[

](/static/articles/inp/video/jL3OLOhcWUQDnR4XjewLBx4e3PC3/WSmcjiQC4lyLxGoES4dd.mp4)

An example of poor versus good responsiveness. On the left, long tasks block the accordion from opening. This causes the user to click multiple times, thinking the experience is broken. When the main thread catches up, it processes the delayed inputs, resulting in the accordion opening and closing unexpectedly. On the right, a more responsive page opens the accordion quickly and without incident.

This guide explains how INP works, how to measure it, and points to resources for improving it.

## What is INP?

INP is a metric that assesses a page's overall responsiveness to user interactions by observing the latency of all click, tap, and keyboard interactions that occur throughout the lifespan of a user's visit to a page. The final INP value is the longest interaction observed, ignoring outliers.

Details on how INP is calculated

INP is calculated by observing all the interactions made with a page. For most sites the interaction with the worst latency is reported as INP.

However, for pages with large numbers of interactions, random hiccups can result in an unusually high-latency interaction on an otherwise responsive page. The more interactions that occur on a given page, the more likely this is to happen.

To give a better measure of the actual responsiveness for pages with a high number of interactions, we ignore one highest interaction for every 50 interactions. The vast majority of page experiences don't have over 50 interactions, so the worst interaction is most often reported. The 75th percentile of all page views is then reported as usual, which further removes outliers to give a value that the vast majority of users experience or better.

An *interaction* is a group of event handlers that fire during the same logical user gesture. For example, "tap" interactions on a touchscreen device include multiple events, such as `pointerup`, `pointerdown`, and `click`. An interaction can be driven by JavaScript, CSS, built-in browser controls (such as form elements), or a combination thereof.

An interaction's latency consists of the single longest [duration](https://w3c.github.io/event-timing/#ref-for-dom-performanceentry-duration%E2%91%A1:%7E:text=The%20Event%20Timing%20API%20exposes%20a%20duration%20value%2C%20which%20is%20meant%20to%20be%20the%20time%20from%20when%20user%20interaction%20occurs%20(estimated%20via%20the%20Event%27s%20timeStamp)%20to%20the%20next%20time%20the%20rendering%20of%20the%20Event%27s%20relevant%20global%20object%27s%20associated%20Document%E2%80%99s%20is%20updated) of a group of event handlers that drive the interaction, from the time the user begins the interaction to the moment the browser is next able to paint a frame. In rare cases there may be no frame to paint but the interaction ends when the browser would be able to paint a frame.

### What is a good INP score?

Pinning labels such as "good" or "poor" on a responsiveness metric is difficult. On one hand, you want to encourage development practices that prioritize good responsiveness. On the other hand, you must account for the fact that there's considerable variability in the capabilities of devices people use to set achievable development expectations.

To ensure you're delivering user experiences with good responsiveness, a good threshold to measure is the **75th percentile** of page loads recorded in the field, segmented across mobile and desktop devices:

- An INP below or at **200 milliseconds** means a page has **good responsiveness**.
- An INP above **200 milliseconds** and below or at **500 milliseconds** means a page's responsiveness **needs improvement**.
- An INP above **500 milliseconds** means a page has **poor responsiveness**.

![Good INP values are 200 milliseconds or less, poor values are greater than 500 milliseconds, and anything in between needs improvement.](/static/articles/inp/image/inp-mobile-v2.svg)

Good INP values are 200 milliseconds or less. Poor values are greater than 500 milliseconds.

### What's in an interaction?

![A diagram depicting an interaction on the main thread. The user makes an input while blocking tasks run. The input is delayed until those tasks complete, after which the pointerup, mouseup, and click event handlers run, then rendering and painting work is kicked off until the next frame is presented.](/static/articles/inp/image/whats-in-an-interaction.svg)

The life of an interaction. An input delay occurs until event handlers start running, possibly caused by factors such as long tasks on the main thread. The interaction's event handler callbacks then run, and a delay occurs before the next frame is presented.

The primary driver of interactivity is often JavaScript, though browsers do provide interactivity through controls *not* powered by JavaScript, such as checkboxes, radio buttons, and controls powered by CSS.

As the purposes of INP, **only the following interaction types are observed:**

- Clicking with a mouse.
- Tapping on a device with a touchscreen.
- Pressing a key on either a physical or onscreen keyboard.

Interactions happen in the main document or in iframes embedded in the document—for example clicking play on an embedded video. End users won't be aware what is in an iframe or not, therefore, INP within iframes are needed to measure the user experience for the top level page. Because JavaScript Web APIs don't have access to the contents of iframes, this may [show as a difference between CrUX and RUM](/articles/crux-and-rum-differences#iframes)

Interactions can consist of multiple events. For example, a keystroke includes the `keydown`, `keypress`, and `keyup` events. Tap interactions contain `pointerup` and `pointerdown` events. The event with the longest duration within the interaction is what contributes to the interaction's total latency.

![A depiction of more complex interaction containing two interactions. The first is a mousedown event, which produces a frame before the mouse button is let up, which kicks off more work until yet another frame is presented as the result.](/static/articles/inp/image/logical-interaction.svg)

A depiction of an interaction with multiple event handlers. The first part of the interaction receives an input when the user clicks down on a mouse button. However, before they release the mouse button, a frame is presented. When the user releases the mouse button, another series of event handlers must run before the next frame is presented.

As shown in the diagram, the **processing duration** of INP includes all event handler callbacks within that frame. This makes the **input delay** the time before any callback for an interaction is handled, the **processing duration** the time for all the callbacks to execute, and the **presentation delay** the time after the callbacks have been executed until the frame is presented on the user's screen.

The page's INP is calculated when the user leaves the page. The result is a single value that is representative of the page's overall responsiveness throughout its lifecycle. **A low INP means that a page was reliably responsive to user input.**

### How is INP different from First Input Delay (FID)?

INP is the successor metric to [First Input Delay (FID)](/articles/fid). While both are responsiveness metrics, FID only measured the [input delay](/articles/optimize-input-delay#what_is_input_delay) of the *first* interaction on a page. INP improves on FID by observing *all* interactions on a page, beginning from the input delay, to the time it takes to run event handlers, and finally up until the browser has painted the next frame.

These differences mean that both INP and FID are different types of responsiveness metrics. Where FID was a [load responsiveness metric](/articles/user-centric-performance-metrics#types_of_metrics) designed to assess the page's first impression on the user, INP is a more reliable indicator of overall responsiveness, regardless of when in the life of a page interactions occur.

### What if no INP value is reported?

It's possible for a page to return no INP value. This can happen for a number of reasons, including the following:

- The page was loaded, but the user never clicked, tapped, or pressed a key on their keyboard.
- The page loaded, but the user interacted with it using gestures that aren't measured, such as scrolling or hovering over elements.
- The page is being accessed by a bot such as a search crawler or headless browser that has not been scripted to interact with the page.

## How to measure INP

INP can be measured both in [the field](/articles/lab-and-field-data-differences#field_data) and in [the lab](/articles/lab-and-field-data-differences#lab_data), to the extent that you can simulate realistic user interactions.

### In the field

Ideally, your journey in optimizing INP will start with field data. At its best, field data from Real User Monitoring (RUM) will give you not only a page's INP value, but also contextual data that highlights what specific interaction was responsible for the INP value itself, whether the interaction occurred during or after page load, the type of interaction (click, keypress, or tap), and other valuable timings that can help you identify which part of the interaction was affecting responsiveness.

If your website qualifies for inclusion in the [Chrome User Experience Report (CrUX)](https://developer.chrome.com/docs/crux), you can quickly get field data for INP [via CrUX in PageSpeed Insights](/articles/find-slow-interactions-in-the-field#get_field_data_quickly_with_crux) (and other Core Web Vitals). At a minimum, you can get an origin-level picture of your website's INP, but in some cases, you can also get URL-level data.

However, while CrUX can tell you if there *is* a problem, it can't tell you what caused the problem. A RUM solution can help you uncover more details about pages, users, or user interactions that are experiencing responsiveness issues. Being able to attribute INP to individual interactions avoids guesswork and wasted effort.

### In the lab

Optimally, you'll want to start testing in the lab once you have field data that suggests a page has slow interactions. Field data will make the work of reproducing problematic interactions in the lab a much more straightforward task.

It's entirely possible, however, that you don't have field data. While INP *can* be measured in some lab tools, the resulting INP value for a page during lab testing will be dependent on what interactions are performed during the measurement period. User behaviors can be unpredictable and highly variable, meaning that your testing in the lab may not surface problem interactions in the same fashion that field data can. Additionally, some lab tools won't report a page's INP because they only observe the loading of a page without any interactions. In such cases, [Total Blocking Time (TBT)](/articles/tbt) may be a reasonable proxy metric for INP, but it's not a substitute for INP in and of itself.

Even though there are limitations in lab tools when it comes to assessing a page's INP, there are some strategies for reproducing slow interactions in the lab. Strategies include following common user flows and testing interactions along the way, as well as interacting with the page as it loads—when the main thread is often busiest—in order to identify slow interactions during that crucial part of the user experience.

### Measure INP in JavaScript

To measure INP in JavaScript, you need to measure event timings for all
interactions, and then take the 98th percentile across all these interactions on page unload. You can refer to the [`web vitals` JavaScript library source code](https://github.com/GoogleChrome/web-vitals/blob/main/src/onINP.ts) which contains a reference implementation on how INP is calculated.

In most cases, the current INP value at the time the page is being unloaded is the final INP value for that page, but there are a few important exceptions as noted in the next section. The `web vitals` JavaScript library accounts for these as much as possible, within the limitations of the Web APIs.

#### Differences between the metric and the API

- `event` entries below 104 milliseconds don't report by default using performance observers. This default can be changed when a performance observer is registered using the `durationThreshold` parameter but even this has a minimum value of 16 milliseconds. For this reason, it is recommended to also observe the `first-input` entry, which is also an Event Timing entry, but is guaranteed to be observable even when its duration is less than `durationThreshold`. This helps ensure that pages with interactions always report some INP value.
- Calculating percentiles perfectly technically requires keeping all samples in memory, which can be costly. But you can approximate percentiles, especially really high percentiles like p98, by just keeping a small list of the worst-N interactions. 10 is a common choice.
- If a page is restored from the [back/forward cache](/articles/bfcache#impact_on_core_web_vitals), its INP value should be reset to zero since users experience this as a distinct page visit.
- The API does not report `event` entries for interactions that occur within iframes but the metric does as they are part of the user experience of the page. This can [show as a difference between CrUX and RUM](/articles/crux-and-rum-differences#iframes). To properly measure INP you should consider them. Sub-frames can use the API to report their `event-timing` entries to the parent frame.

In addition to these exceptions, INP has some added complexity due to the fact that it measures the entire lifespan of a page:

- Users might keep a tab open for a *very* long time—days, weeks, months. In fact, a user might never close a tab.
- On mobile operating systems, browsers typically don't run page unload callbacks for background tabs, making it difficult to report the "final" value.

To handle such cases, INP should be reported any time a page is background—in addition to any time it's unloaded (the [`visibilitychange` event](https://developer.chrome.com/blog/page-lifecycle-api#event-visibilitychange) covers both of these scenarios). And analytics systems receiving this data will then need to calculate the final INP value on the backend.

Rather than memorizing and grappling with all of these cases yourself, developers can use the [`web-vitals` JavaScript library](https://github.com/GoogleChrome/web-vitals) to measure INP, which accounts for everything mentioned previously, except the iframe case:

```
import {onINP} from 'web-vitals';

// Measure and log INP in all situations
// where it needs to be reported.
onINP(console.log);
```

## How to improve INP

A [collection of guides on optimizing INP](/articles/optimize-inp) is available to guide you through the process of identifying slow interactions in the field, and using lab data to help you identify causes and optimize them.

## Changelog

Occasionally, bugs are discovered in the APIs used to measure metrics, and sometimes in the definitions of the metrics themselves. As a result, changes must sometimes be made, and these changes can show up as improvements or regressions in your internal reports and dashboards.

To help you manage this, all changes to either the implementation or definition of these metrics will be surfaced in this [Changelog](https://chromium.googlesource.com/chromium/src/+/main/docs/speed/metrics_changelog/inp.md).

If you have feedback for these metrics, provide it in the [web-vitals-feedback Google group](https://groups.google.com/g/web-vitals-feedback).

## Test your knowledge

What is the primary goal of the INP metric?

To measure the time it takes for the first content of a page to be displayed.

Incorrect - This describes First Contentful Paint

To quantify the visual stability of a page and minimize unexpected layout shifts.

Incorrect - This describes Cumulative Layout Shift

To assess the time it takes for a page to become fully interactive.

Incorrect - This is related to Time to Interactive, but INP specifically focuses on responsiveness to user input

To minimize the time from when a user initiates an interaction until the next frame is painted, for all or most interactions the user initiates.

Correct!

Which of the following interaction types are observed for the purposes of calculating INP? (Select all that apply.)

Clicking with a mouse.

Correct!

Scrolling the page with a mouse wheel or trackpad.

Incorrect - INP does not consider scrolling

Tapping on a touchscreen.

Correct!

Hovering the mouse cursor over elements.

Incorrect - INP does not consider hovering

Pressing a key on a keyboard.

Correct!

Zooming in or out on the page.

Incorrect - INP does not consider zooming

How is the "latency" of an interaction defined for INP?

The amount of time for the browser to process the event handlers of an interaction.

Incorrect - This only accounts for the processing duration, not the input delay or time to present the next frame

The average time it takes for all interactions on a page to produce a visual response.

Incorrect - INP focuses on the longest interaction, not the average

The time it takes for the browser to start processing the event handlers associated with an interaction.

Incorrect - This only accounts for the input delay, not the processing and rendering time

The time from the start of the interaction to the moment the next frame is fully presented.

Correct!

What is the difference between INP and FID?

INP measures the time it takes for the first content of a page to be displayed, while FID measures the responsiveness to user input.

Incorrect - This describes First Contentful Paint, not INP

INP considers the full duration of all interactions, while FID only measures the input delay of the first interaction.

Correct!

INP and FID measure different timestamps at which a page becomes interactive.

Incorrect - INP and FID are measures of how quickly the page responds to interactions, irrespective of when the interactions occur

There is no difference; INP and FID are just two different names for the same metric.

Incorrect - They do have distinct definitions

Under what circumstances might INP data be unavailable for a page in tools like PageSpeed Insights?

The page is using a custom performance measurement library that doesn't report INP data.

Incorrect - INP is automatically measured using web platform APIs and doesn't rely on pages self-reporting their performance through custom libraries.

There isn't enough interaction data from Chrome users to calculate a meaningful INP value in the CrUX dataset.

Correct!

Users interacted with the page solely through scrolling and hovering, which are not considered for INP.

Correct!

The page is built using a framework that automatically optimizes for INP, so there's no need to report it.

Incorrect - Frameworks can help with INP, but the metric is still relevant and reported if data is available

What is the *most effective* strategy for reproducing slow interactions in a lab environment?

Simulating a high-end device with a slow and unreliable network connection to create challenging conditions.

Incorrect - While network can play a role, device capabilities are more likely to expose slow interactions

Testing interactions only after the page has fully loaded and is idle.

Incorrect - This might miss interactions that are slow during load

Interacting with the page during load and following common user flows to identify potential bottlenecks.

Correct!

Focusing on complex, edge-case interactions that are unlikely to be encountered by most users.

Incorrect - Common user flows are more relevant for identifying typical INP issues

✨ *This quiz was generated by Gemini 1.5 and reviewed by humans. [Share your feedback](https://issuetracker.google.com/issues/new?component=1400680&template=1996170)*

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-02 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-09-02 UTC."],[],[]]