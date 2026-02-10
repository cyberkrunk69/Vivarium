# Rendering performanceStay organized with collectionsSave and categorize content based on your preferences.

Source: https://web.dev/articles/rendering-performance

---

- [Home](https://web.dev/)
- [Articles](https://web.dev/articles)

# Rendering performance Stay organized with collections Save and categorize content based on your preferences.

Users notice if sites and apps don't run well, so optimizing rendering performance is crucial!

Paul Lewis

Users of today's web expect that the pages they visit will be interactive and
smooth, and that's where you need to increasingly focus your time and effort.
Pages shouldn't just load quickly, but also respond quickly to user input
throughout their entire lifecycle. In fact, this aspect of the user experience
is precisely what the [Interaction to Next Paint (INP)](/articles/inp) metric measures. A good
INP means that a page was consistently and reliably responsive to the user's
needs.

While a major component of what makes a page feel snappy involves the amount of
JavaScript you execute in response to user interactions, what users are
anticipating are visual changes to the user interface. Visual changes to a user
interface are the result of several types of work, often collectively referred
to as *rendering*, and this work needs to happen as quickly as possible so that
the user experience feels fast and reliable.

To write pages that respond quickly to user interactions, you need to understand
how HTML, JavaScript, and CSS are handled by the browser, and ensure that the
code you write—as well as any other third-party code you include—runs as
efficiently as possible.

## A note on device refresh rates

![A user interacting with a website on a mobile phone.](/static/articles/rendering-performance/image/user-interacting-a-websi-f32989a67c995.jpg)

The refresh rate of a display is an important consideration when it comes to
building websites that feel responsive to user input.

Most devices today refresh their screens **60 times a second**. Each refresh
produces the visual output you see, and is commonly known as a *frame*. In the
following video, the concept of frames is demonstrated:

[

](/static/articles/rendering-performance/video/frames.webm)

Frames as shown in the performance panel of Chrome DevTools. As the cursor
scrubs over the filmstrip near the top, an enlarged representation of each
frame is shown within a tooltip as a mobile navigation menu animates to its
"open" state.

While a device's screen always refreshes at a consistent rate, applications that
run on a device may not necessarily always be able to produce enough frames to
match that refresh rate. For example, if there's an animation or transition
running, the browser needs to match the device's refresh rate to produce one
frame for each time the screen refreshes.

Given that a typical display refreshes 60 times per second, some quick math
would reveal that the browser has 16.66 milliseconds to produce each frame.
In reality, though, the browser has its own overhead for each frame, so all of
your work needs to be completed inside **10 milliseconds**. When you fail to
meet this budget, the frame rate drops, and page contents judder on-screen. This
phenomenon is often called *jank*.

However, your targets change based on the type of work you're trying to do.
Meeting the 10 millisecond threshold is crucial for *animations*, where the
of objects on the screen are interpolated across a series of frames between two
points. When it comes to discrete changes in the user interface—that is,
proceeding from one state to another without any motion in between—it's
recommended that you achieve such changes in a timeframe that *feels* instant to
the user. In cases such as these, 100 milliseconds is an oft-cited figure, but
the INP metric's "good" threshold is 200 milliseconds or lower in order to
accommodate a wider array of devices with varying capabilities.

Whatever your goals are—be they producing the many frames that animations
require in order to avoid jank, or merely producing a discrete visual change in
the user interface as quickly as possible—understanding how the browser's pixel
pipeline works is essential to your work.

## The pixel pipeline

There are five major areas that you need to know about and be mindful of in your
work as a web developer. These five areas are those that you have the most
control over, and each represents a key point in the pixels-to-screen pipeline:

![The full pixel pipeline, containing five steps: JavaScript, Style, Layout, Paint, and Composite.](/static/articles/rendering-performance/image/the-full-pixel-pipeline-45b24543207ea.jpg)

The full pixel pipeline, illustrated.

- **JavaScript:** JavaScript is typically used to handle work that will result
  in visual changes to the user interface. For example, this could be jQuery's
  `animate` function, sorting a dataset, or adding DOM elements to the page.
  JavaScript isn't strictly necessary to trigger visual changes, though: [CSS
  animations](/learn/css/animations), [CSS transitions](/learn/css/transitions), and [the Web Animations API](https://developer.mozilla.org/docs/Web/API/Web_Animations_API) are capable of
  animating page contents.
- **Style calculations:** This is the process of figuring out which CSS rules
  apply to which HTML elements based on matching selectors. For example,
  `.headline` is an example of a CSS selector that applies to any HTML element
  with a `class` attribute value that contains a class of `headline`. From
  there, once rules are known, they are applied, and the final styles for each
  element are calculated.
- **Layout:** Once the browser knows which rules apply to an element it can
  begin to calculate the geometry of the page, such as how much space elements
  take up, and where they appear on the screen. The web's layout model means
  that one element can affect others. For example, the width of the `<body>`
  element typically affects the dimensions of its child elements all the way up
  and down the tree, so the process can be quite involved for the browser.
- **Paint:** Painting is the process of filling in pixels. It involves drawing
  out text, colors, images, borders, shadows, and essentially every visual
  aspect of the elements after their layout on the page has been calculated.
  The drawing is typically done onto multiple surfaces, often called layers.
- **Composite:** Since the parts of the page were potentially drawn onto
  multiple layers, they need to be applied to the screen in the correct order so
  that the page renders as expected. This is especially important for elements
  that overlap another, since a mistake could result in one element appearing
  over the top of another incorrectly.

Each of these parts of the pixel pipeline represents an opportunity to introduce
jank in animations, or delay the painting of frames even for discrete visual
changes to the user interface. It's therefore important to understand exactly
which parts of the pipeline your code triggers, and to investigate if you can
limit your changes to only the parts of the pixel pipeline that are necessary to
render them.

You may have heard the term "rasterize" used in conjunction with "paint". This
is because painting is actually two tasks:

1. Creating a list of draw calls.
2. Filling in the pixels.

The latter is called "rasterization", so whenever you see paint records in
DevTools, you should think of it as including rasterization. In some
architectures, creating the list of draw calls and rasterization are done on
different threads, but that isn't under your control as a developer.

You won't always necessarily touch every part of the pipeline on every frame.
In fact, there are three ways the pipeline *normally* plays out for a given
frame when you make a visual change, either with JavaScript, CSS, or the Web
Animations API.

### 1. JS / CSS > Style > Layout > Paint > Composite

![The full pixel pipeline, with none of the steps omitted.](/static/articles/rendering-performance/image/the-full-pixel-pipeline-8f8a7297e4f77.jpg)

If you change a "layout" property, such as one that changes an element's
geometry like width, height, or its position (such as the `left` or `top` CSS
properties), the browser needs to check all other elements and "reflow" the
page. Any affected areas will need to be repainted, and the final painted
elements will need to be composited back together.

### 2. JS / CSS > Style > Paint > Composite

![The pixel pipeline with the layout step omitted.](/static/articles/rendering-performance/image/the-pixel-pipeline-witho-346f1f6fd4ada.jpg)

If you changed a "paint-only" property for an element in CSS—for example,
properties such as `background-image`, `color`, or `box-shadow`—the layout step
is not necessary to commit a visual update to the page. By omitting the layout
step—where possible—you avoid potentially costly layout work that could have
otherwise contributed significant latency in producing the next frame.

### 3. JS / CSS > Style > Composite

![The pixel pipeline with the layout and paint steps omitted.](/static/articles/rendering-performance/image/the-pixel-pipeline-withou-c9b3dd7e7ab5f.jpg)

If you change a property that requires *neither* layout or paint, the browser
can jump straight to the compositing step. This is the cheapest and most
desirable pathway through the pixel pipeline for high pressure points in a
page's lifecycle, such as animations or scrolling. Fun fact: Chromium optimizes
scrolling of the page so that it occurs solely on the compositor thread where
possible, meaning that even if a page is not responding, you're still able to
scroll the page and see parts of it that were previously drawn to the screen.

Web performance is the art of *avoiding* work, while increasing the efficiency
of any necessary work as much as possible. In many cases, it's about working
with the browser, not against it. It's worth bearing in mind that the work
previously shown in the pipeline differs in terms of computational cost; some
tasks are inherently more expensive than others!

Let’s take a dive into the different parts of the pipeline. We’ll take a look
at the common issues, as well how to diagnose and fix them.

## Browser Rendering Optimizations

[![Udacity course screenshot](/static/articles/rendering-performance/image/udacity-course-screenshot-4c7c3a821e1fa.jpg)](https://www.udacity.com/course/browser-rendering-optimization--ud860)

Performance matters to users, and to build good user experiences, web developers
need to build websites that react quickly to user interactions and render
smoothly. Performance expert Paul Lewis is here to help you destroy jank and
create web apps that maintain 60 frames per second performance. You'll leave
this course with the tools you need to profile apps, and identify the causes of
suboptimal rendering performance. You'll also explore the browser's rendering
pipeline and uncover patterns that make it easier to build fast websites that
users will find delightful to use.

This is a free course offered through [Udacity](https://www.udacity.com), and you can [take it any time](https://www.udacity.com/course/browser-rendering-optimization--ud860).

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2023-12-13 UTC.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2023-12-13 UTC."],[],[]]