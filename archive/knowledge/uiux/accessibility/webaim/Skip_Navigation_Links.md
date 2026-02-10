# Skip Navigation Links

Source: https://webaim.org/techniques/skipnav/

---

# Skip Navigation Links

You are here: [Home](/) > [Articles](/articles/) > "Skip Navigation" Links

## Overview

On most pages, keyboard and screen reader users must navigate a long list of navigation links and other elements before ever arriving at the main content. This can be particularly difficult for users with some forms of motor disabilities. Consider users with no or limited arm movement who navigate a web page by tapping their heads on a switch or that use a stick in their mouth to press keyboard keys. Requiring users to perform any action numerous times before reaching the main content poses an accessibility barrier.

Of course, sighted people who use their mouse do not have any trouble with web pages like this. They can almost immediately scan over the page and identify where the main content is. Skip navigation links are useful to give screen reader and keyboard users the same capability of navigating directly to the main content.

## Creating "Skip Navigation" Links

The idea is simple enough: provide a link at the top of the page that, when activated, jumps the user to the beginning of the main content area.

### Visible skip links

The easiest method of creating a skip navigation link is to put it at or near the top of the page in regular text. The key is to **make sure the link is one of the first items** that screen readers hear and that keyboard users navigate to using the keyboard (typically by pressing the Tab key). Otherwise, users may not realize there is a skip navigation link there and may waste time navigating through extraneous links. The link must also be apparent to be helpful.

Example

The link is the first item in the page. The anchor or target for the link (where the link will jump the user to) is the main content region.

<body>  
<a href="#maincontent">Skip to main content</a>
  
...  
**<main id="maincontent">**  
<h1>Heading</h1>  
<p>This is the first paragraph</p>

The target is identified by its `id` attribute value matching the `href` value (minus the "#") of the skip link. When the skip link is activated, keyboard focus will go to the `<main>` element. Navigation and reading will proceed from this location in the page.

Alternatively, you can use a named anchor to identify the target for the link, though named anchors are no longer conforming in HTML5.

<h1>**<a name="maincontent" id="maincontent"></a>** Heading</h1>  
<p>This is the first paragraph</p>

### Temporarily hidden skip links

Many designers worry about the aesthetic impact of visible skip navigation links. They may think these links are unattractive or confusing to users who do not need them, so they may decide to make them invisible. A very small or hidden link does not benefit the audience that most needs skip links—sighted keyboard users. While screen readers have many mechanisms to jump around the page (e.g., headings and regions/landmarks), other keyboard users do not.

To address the concerns that a visible skip link can be intrusive, but still create a skip link that is useful for sighted keyboard users, **we recommend creating a link that is hidden until to the user navigates to it with a keyboard**.

To be usable by all keyboard users, particularly sighted keyboard users, the link must:

- be hidden by default
- be accessible to keyboard navigation
- become prominently visible when it is focused
- properly set focus to the main content area when activated

Probably the most accessible method for visually hiding a skip link is to hide it off screen with CSS, then cause it to be positioned on screen when it receives keyboard focus. Because the link is still part of the accessible content on the page, keyboard and screen reader users can navigate it, and the link will become visible when accessed.

Some techniques, such as hiding the skip link with CSS `display:none` or the `hidden` attribute, will remove the link from keyboard navigation making it inaccessible to all users. Making the link the same color as the background or fully transparent, sizing the link to 0 pixels, or placing it on a one-pixel transparent image can also pose accessibility issues.

Important

Review the article on [Invisible Content Just for Screen Reader Users](/techniques/css/invisiblecontent/) for details on using CSS to hide skip links off-screen.

One potential issue with this approach is that if the user navigates very quickly using the Tab key, the link may be visible on the page for only a fraction of a second and may be overlooked. This can be partially addressed by ensuring that the skip link is very visually distinctive at the top of the page when visible. Additionally, one could use scripting or CSS transitions to cause the link to animate so it remains visible on screen for more time.

Note

Navigate the links at the beginning of this page using the Tab key to see an example of a hidden skip link that becomes visible on keyboard focus using CSS transitions to make it visually distinctive and persistent on screen for at least a moment.

### Which wording is best?

There are multiple ways that the skip link could be worded:

- Skip navigation
- Skip main navigation
- Skip navigation links
- Skip to main content
- Skip to content

Any of these may be sufficient so long as the purpose of the link is clearly described. In general, we prefer "Skip to main content" as it explains where the user is navigating to versus what they are navigating past.

### Multiple skip links are usually unnecessary

What if a page has multiple sections or multiple levels of navigational links? Should developers provide a skip navigation link to each of these sections or to skip over each level of navigational?

**In most cases, a single skip link is sufficient.** For pages that have very few navigable items preceding the main content, a skip link may not be necessary at all. On the other hand, a very complex page with several repeated elements may necessitate additional skip links. Remember, the purpose of skip navigation links is to make keyboard navigation more efficient. Adding more links increases link-clutter. At what point will you need to add a "Skip the skip links" link?!

In-page links elsewhere in a page can also be used to allow users to jump to or jump over other types of page content. The "Article Contents" at the top of this page, for example, includes in-page links to facilitate navigation to major page sections. A skip link could also be used to allow the user to quickly bypass confusing or potentially inaccessible content, such as ASCII art, complex tables, or complex social media feeds.

## Other In-page Navigation Options

### WCAG conformance

[WCAG 2.4.1 (Bypass Blocks - Level A)](/standards/wcag/checklist#sc2.4.1) states, "A mechanism is available to bypass blocks of content that are repeated on multiple Web pages." This does not necessarily require that a skip link be present. Beginning the main content with an `<h1>` or using a `<main>` region would be a sufficient "mechanism". However because neither of these techniques are highly useful for sighted keyboard users absent a screen reader or specialized software, a skip link is strongly recommended for optimal accessibility on pages with repeated navigation.

### Headings and regions

Implementing proper [heading structures](/techniques/semanticstructure/#headings) (especially starting the main content with an `<h1>`) and [regions](/techniques/semanticstructure/#regions) (especially `<nav>` and `<main>`) is a vital aspect of keyboard accessibility. Unfortunately, browsers do not yet natively support this type of navigation without the use of extensions or a screen reader. Even though skip navigation links are a rather clumsy and obtrusive solution to a real-world problem, they are still often necessary to best meet the needs of all keyboard users.

Within web pages and applications, focus management may be necessary to ensure that keyboard focus is set on content elements when they are presented or activated. When a dialog pop-up appears, for example, focus will likely need to be set to it using JavaScript.

### Alternate reading orders

Some web sites use CSS to change page layouts so that the main content is presented before the navigation in the underlying source code (which is what determines the screen reader reading and keyboard navigation order), but it comes after the navigation visually. Because the navigation is encountered first for keyboard and screen reader users, this method may make a skip navigation link unnecessary.

When the visual order does not align with the navigation and reading order, sighted keyboard or screen reader users may be confused when what they are seeing or navigating to seemingly jumps around the visual page. These types of layouts are not recommended.