# Optimize Interaction to Next PaintStay organized with collectionsSave and categorize content based on your preferences.

Source: https://web.dev/articles/optimize-inp

---

- [Home](https://web.dev/)
- [Articles](https://web.dev/articles)

# Optimize Interaction to Next Paint Stay organized with collections Save and categorize content based on your preferences.

Learn how to optimize your website's Interaction to Next Paint.

![Jeremy Wagner](https://web.dev/images/authors/jlwagner-v6.jpg)

Jeremy Wagner

![Philip Walton](https://web.dev/images/authors/philipwalton.jpg)

Philip Walton

![Barry Pollard](https://web.dev/images/authors/tunetheweb.jpg)

Barry Pollard

Published: May 19, 2023, Last updated: September 2, 2025

[Interaction to Next Paint (INP)](/articles/inp) is a [stable](/articles/vitals#stable) Core Web Vital metric that assesses a page's overall responsiveness to user interactions by observing the latency of all [qualifying interactions](/articles/inp#whats_in_an_interaction) that occur throughout the lifespan of a user's visit to a page. The final INP value is the longest interaction observed (sometimes ignoring outliers).

To provide a good user experience, websites should strive to have an Interaction to Next Paint of **200 milliseconds or less**. To hit this target for most of your users, a good threshold to measure is the **75th percentile of page loads**, segmented across mobile and desktop devices.

![Good INP values are 200 milliseconds or less, poor values are greater than 500 milliseconds, and anything in between needs improvement.](/static/articles/inp/image/inp-mobile-v2.svg)

INP thresholds

Depending on the website, there may be few to no interactions—such as pages of mostly text and images with few to no interactive elements. Or, in the case of websites such as text editors or games, there could be hundreds—even thousands—of interactions. In either case, where there's a high INP, the user experience is at risk.

It takes time and effort to improve INP, but the reward is a better user experience. In this guide, a path to improving INP will be explored.

## Figure out what's causing poor INP

Before you can fix slow interactions, you'll need data to tell you if your website's INP is poor or needs improvement. Once you have that information, you can move into the lab to begin diagnosing slow interactions, and work your way toward a solution.

### Find slow interactions in the field

Ideally, your journey in optimizing INP will start with [field data](/articles/lab-and-field-data-differences#field_data). At its best, field data from a Real User Monitoring (RUM) provider will give you not only a page's INP value, but also contextual data that highlights what specific interaction was responsible for the INP value itself, whether the interaction occurred during or after page load, the type of interaction (click, keypress, or tap), and other valuable information.

If you're not relying on a RUM provider to get field data, the [INP field data guide](/articles/find-slow-interactions-in-the-field) advises [using PageSpeed Insights to view the Chrome User Experience Report (CrUX) data](/articles/find-slow-interactions-in-the-field#start_with_crux_to_evaluate_your_websites_inp) to help fill in the gaps. CrUX is the Google dataset of the Core Web Vitals program and provides a high-level summary of metrics for millions of websites, including INP. However, CrUX often does not provide the contextual data you'd get from a RUM provider to help you to analyze issues. Because of this, we still recommend that sites use a RUM provider when possible, or implement their own RUM solution to supplement what is available in CrUX.

### Diagnose slow interactions in the lab

Ideally, you'll want to start testing in the lab once you have field data that suggests you have slow interactions. In the absence of field data, there are some strategies for identifying slow interactions in the lab. Such strategies include following common user flows and testing interactions along the way, as well as interacting with the page during load—when the main thread is often busiest—in order to identify slow interactions during that crucial part of the user experience.

## Optimize interactions

Once you've identified a slow interaction and [can manually reproduce it in the lab](/articles/manually-diagnose-slow-interactions-in-the-lab), the next step is to optimize it.

Interactions can be broken down into three subparts:

1. The **input delay**, which starts when the user initiates an interaction with the page, and ends when the event callbacks for the interaction begin to run.
2. The **processing duration**, which consists of the time it takes for event callbacks to run to completion.
3. The **presentation delay**, which is the time it takes for the browser to present the next frame which contains the visual result of the interaction.

![An example interaction on the main thread. The user makes an input while blocking tasks run. The input is delayed until those tasks complete, after which the pointerup, mouseup, and click event handlers run, then rendering and painting work is kicked off until the next frame is presented.](/static/articles/optimize-inp/image/whats-in-an-interaction.svg)

The life of an interaction. An input delay occurs until event handlers start running, possibly caused by factors such as long tasks on the main thread. The interaction's event handler callbacks then run, and a delay occurs before the next frame is presented.

The sum of these three subparts is the total interaction latency. Every single subpart of an interaction contributes some amount of time to total interaction latency, so it's important to know how you can optimize each part of the interaction so it runs for as little time as possible.

### Identify and reduce input delay

When a user interacts with a page, the first part of that interaction is the *input delay*. Depending on other activity on the page, input delays can be considerable in length. This could be due to activity occurring on the main thread (perhaps due to scripts loading, parsing and compiling), fetch handling, timer functions, or even from other interactions that occur in quick succession and overlap with one another.

Whatever the source of an interaction's input delay, you'll want to reduce input delay to a minimum so that interactions can begin running event callbacks as soon as possible.

#### The relationship between script evaluation and long tasks during startup

A critical aspect of interactivity in the page lifecycle is during startup. As a page loads, it will initially render, but it's important to remember that just because a page has *rendered*, doesn't mean that the page is finished *loading*. Depending on how many resources a page requires to become fully functional, it's possible that users may attempt to interact with the page while it's still loading.

One thing that can extend an interaction's input delay while a page loads is script evaluation. After a JavaScript file has been fetched from the network, the browser still has work to do before that JavaScript can run; that work includes parsing a script to check its syntax is valid, compiling it into bytecode, and then finally executing it.

Depending on the size of a script, this work can introduce long tasks on the main thread, which will delay the browser from responding to other user interactions. To keep your page responsive to user input during page load, it's important to understand what you can do to reduce the likelihood of long tasks during page load so the page stays snappy.

### Optimize event callbacks

The input delay is only the first part of what INP measures. You'll also need to make sure that the event callbacks that run in response to a user interaction can complete as quickly as possible.

#### Yield to the main thread often

The best general advice in optimizing event callbacks is to do as little work as possible in them. However, your interaction logic may be complex, and you may only be able to marginally reduce the work they do.

If you find this is the case for your website, the next thing you can try is to break up the work in event callbacks into separate tasks. This prevents the collective work from becoming a long task that blocks the main thread, which allows other interactions that otherwise would be waiting on the main thread to run sooner.

`setTimeout` is one way to break up tasks, because the callback passed to it runs in a new task. You can [use `setTimeout` by itself](/articles/optimize-long-tasks#manually_defer_code_execution) or abstract its use into a separate function [for more ergonomic yielding](/articles/optimize-long-tasks#use_asyncawait_to_create_yield_points).

Yielding indiscriminately is better than not yielding at all—however, there is a more nuanced way of yielding to the main thread, and that involves only yielding immediately after an event callback that updates the user interface so rendering logic can run sooner.

#### Yield to allow rendering work to occur sooner

A more advanced yielding technique involves structuring the code in your event callbacks to limit what gets run to just the logic required to apply visual updates for the next frame. Everything else can be deferred to a subsequent task. This not only keeps callbacks light and nimble, but it also improves rendering time for interactions by not allowing visual updates to block on event callback code.

For example, imagine a rich text editor that formats text as you type, but also updates other aspects of the UI in response to what you've written (such as word count, highlighting spelling mistakes, and other important visual feedback). In addition, the application may also need to save what you've written so that if you leave and return, you haven't lost any work.

In this example, the following four things need to happen in response to characters typed by the user. However, only the first item needs to be done before the next frame is presented.

1. Update the text box with what the user typed and apply any required formatting.
2. Update the part of the UI that displays the current word count.
3. Run logic to check for spelling mistakes.
4. Save the most recent changes (either locally or to a remote database).

The code to do this might look something like the following:

```
textBox.addEventListener('input', (inputEvent) => {
  // Update the UI immediately, so the changes the user made
  // are visible as soon as the next frame is presented.
  updateTextBox(inputEvent);

  // Use `setTimeout` to defer all other work until at least the next
  // frame by queuing a task in a `requestAnimationFrame()` callback.
  requestAnimationFrame(() => {
    setTimeout(() => {
      const text = textBox.textContent;
      updateWordCount(text);
      checkSpelling(text);
      saveChanges(text);
    }, 0);
  });
});
```

The following visualization shows how deferring any non-critical updates until after the next frame can reduce the processing duration and thus the overall interaction latency.

[![A depiction of a keyboard interaction and subsequent tasks in two scenarios. In the top figure, the render-critical task and all subsequent background tasks run synchronously until the opportunity to present a frame has arrived. In the bottom figure, the render-critical work runs first, then yields to the main thread to present a new frame sooner. The background tasks run thereafter.](/static/articles/optimize-inp/image/interaction-latency.png)](https://web.dev/articles/optimize-inp/image/interaction-latency.svg)

Click the figure to see a high-resolution version.

While the use of `setTimeout()` inside a `requestAnimationFrame()` call in the previous code example is admittedly a bit esoteric, it is an effective method that works in all browsers to prevent non-critical code from blocking the next frame.

#### Avoid layout thrashing

Layout thrashing—sometimes called forced synchronous layout—is a rendering performance problem where layout occurs synchronously. It occurs when you update styles in JavaScript, and then read them in the same task—and [there are many properties in JavaScript that can cause layout thrashing](https://gist.github.com/paulirish/5d52fb081b3570c81e3a).

![A visualization of layout thrashing as shown in the performance panel of Chrome DevTools.](/static/articles/optimize-inp/image/a-visualization-layout-t-cefcc10055727.png)

An example of layout thrashing, as shown in the performance panel of Chrome DevTools. Rendering tasks that involve layout thrashing will be noted with a red triangle at the upper right corner of the portion of the call stack, often labeled **Recalculate Style** or **Layout**.

Layout thrashing is a performance bottleneck because by updating styles and then immediately requesting the values of those styles in JavaScript, the browser is forced to do synchronous layout work it otherwise could have waited to perform asynchronously later on after event callbacks have finished running.

### Minimize presentation delay

The *presentation delay* of an interaction marks spans from when an interaction's event callbacks have finished running, up to the point at which the browser is able to paint the next frame that shows the resulting visual changes.

#### Minimize DOM size

When a page's DOM is small, rendering work usually finishes quickly. However, when DOMs get very large, rendering work tends to scale with increasing DOM size. The relationship between rendering work and DOM size isn't a linear one, but large DOMs do require more work to render than small DOMs. A large DOM is problematic in two cases:

1. During the initial page render, where a large DOM requires a lot of work to render the page's initial state.
2. In response to a user interaction, where a large DOM can cause rendering updates to be very expensive, and therefore increase the time it takes for the browser to present the next frame.

Bear in mind that there are instances in which large DOMs can't be significantly reduced. While there are approaches you can take to reduce DOM size, such as [flattening your DOM](/articles/dom-size-and-interactivity#how_can_i_reduce_dom_size) or [add to the DOM during user interactions](/articles/dom-size-and-interactivity#consider_an_additive_approach) to keep your initial DOM size small, those techniques may only go so far.

#### Use `content-visibility` to lazily render off-screen elements

One way you can limit the amount of both rendering work during page load and rendering work in response to user interactions is to lean on the CSS `content-visibility` property, which effectively amounts to lazily rendering elements as they approach the viewport. While `content-visibility` can take some practice to use effectively, it's worth investigating if the result is lower rendering time that can improve your page's INP.

#### Be aware of performance costs when rendering HTML using JavaScript

Where there's HTML, there's HTML parsing, and after the browser has finished parsing HTML into a DOM, it must apply styles to it, perform layout calculations, and subsequently render that layout. This is an unavoidable cost, but *how* you go about rendering HTML matters.

When the server sends HTML, it arrives in the browser as a stream. Streaming means that the HTML response from the server is arriving in chunks. The browser optimizes how it handles a stream by incrementally parsing chunks of that stream as they arrive, and rendering them bit by bit. This is a performance optimization in that the browser implicitly yields periodically and automatically during page load, and you get that for free.

While the first visit to any website will always involve *some* amount of HTML, a common approach starts with a minimal initial bit of HTML, and then JavaScript is used to populate the content area. Subsequent updates to that content area also occur as the result of user interactions. This is usually called the [single-page application (SPA) model](https://en.wikipedia.org/wiki/Single-page_application). One drawback of this pattern is that, by rendering HTML with JavaScript on the client, you not only get the cost of the JavaScript processing to create that HTML, but also the browser will *not* yield until it has finished parsing that HTML, and rendering it.

It's vital to remember though, that even websites that *aren't* SPAs will probably involve some amount of HTML rendering through JavaScript as the result of interactions. This is generally fine, so long as you're not rendering large amounts of HTML on the client, which can delay presentation of the next frame. However, it's important to understand the performance implications of this approach to rendering HTML in the browser, and how it can impact the responsiveness of your website to user input if you are rendering a lot of HTML using JavaScript.

## Conclusion

Improving your site's INP is an iterative process. When you fix a slow interaction in the field, the chances are good that—especially if your website provides lots of interactivity—you'll start to find other slow interactions, and you'll need to optimize them too.

The key to improving INP is persistence. In time, you can get your page's responsiveness to a place where users are happy with the experience you're providing them. The chances are also good that as you develop new features for your users, you may need to go through the same process in optimizing interactions specific to them. It will take time and effort, but it's time and effort well spent.

*Hero image from [Unsplash](https://unsplash.com/), by [David Pisnoy](https://unsplash.com/@davidpisnoy) and modified in accordance with the [Unsplash license](https://unsplash.com/license).*

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-02 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-09-02 UTC."],[],[]]