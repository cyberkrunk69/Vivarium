# CSS in ActionInvisible Content Just for Screen Reader Users

Source: https://webaim.org/techniques/css/invisiblecontent/

---

# CSS in Action Invisible Content Just for Screen Reader Users

You are here: [Home](/) > [Articles](/articles/) > CSS in Action: Invisible Content Just for Screen Reader Users

## Introduction

![A woman hides behind her hands.](media/peekaboo.jpg)There are occasional instances where content should be made available to screen reader users but hidden from sighted users. In the vast majority cases, content that is available visually should be available to screen reader users, and vice versa. Verbose cues or instructions that are only read by screen reader users usually do more harm than good. However, there are a few cases where information or meaning is apparent visually but may not be apparent to screen reader users. In these rare cases, it may be appropriate to cause content to be read by a screen reader, but have the content remain invisible to sighted users.

## Techniques for hiding content

There are several mechanisms that can be used for hiding content. It's important that a technique be implemented that results in the desired outcome and accessibility.

### `display:none` or `visibility: hidden`

These styles will hide content from all users. The content is removed from the visual flow of the page and is ignored by screen readers. **Do not use this CSS if you want the content to be read by a screen reader. But DO use it for content you want hidden from all users.**

### `hidden` attribute

The HTML `hidden` attribute is relatively new and not supported on older browsers like IE11. When supported, it functions the same as CSS `display:none`—elements with this attribute will not be presented to any user.

### `width:0px`, `height:0px` or other 0 pixel sizing techniques (not recommended)

An element with no height or width, whether defined in HTML or CSS, is typically removed from the flow of the page, so most screen readers will not read it. **Do not size content to 0 pixels if you want the content to be read by a screen reader.** Content styled with `font-size:0px` or `line-height:0` may work, though the elements would still take horizontal space on the screen. All these techniques may result in search engine penalties as they may be interpreted as malicious.

### `text-indent: -10000px;`

This approach moves the content to the left 10000 pixels - thus off the visible screen. Screen readers will still read text with this style.

However, if a link, form control, or other focusable element is given this style, the element would be focusable, but not visible on the page—sighted keyboard users would likely be confused. This approach *may* be a viable option if the element does not contain navigable elements, though better techniques are available.

### Absolutely positioning content off-screen

The following are the recommended styles for visually hiding content that will be read by a screen reader.

.sr-only {  
position:absolute;  
left:-10000px;  
top:auto;  
width:1px;  
height:1px;  
overflow:hidden;  
}

The `.sr-only` CSS class ("sr-only" meaning "screen reader only", though the class name does not really matter) should then be referenced from within the tag of the element being hidden, as shown:

<div **class="sr-only"**>This text is hidden.</div>

Sighted users will not see the hidden content at all—it will be hidden well to the left of the visible browser window. Because it is still part of the page content, screen readers will read it.

Let's analyze the styles in detail. `position:absolute;` tells the browser to remove the element from the page flow and to begin positioning it. `left:-10000px;` moves the content 10000 pixels to the left. `top:auto;` tells the browser to position the content vertically at the same location it was originally. `width:1px;`, `height:1px;` and `overflow:hidden;` tell the browser to make the element one pixel in size and to visually hide everything that does not fit into that pixel—this is useful in instances where positioning may be end-user disabled, but all other styles remain enabled.

Note

Navigable elements, such as links and form controls, should not be hidden off-screen. They would still be navigable by sighted keyboard users, but would not be visible to them, unless they are styled to become visible when they receive keyboard focus.

### CSS clip

{clip: rect(1px, 1px, 1px, 1px);  
clip-path: inset(50%);  
height: 1px;  
width: 1px;  
margin: -1px;  
overflow: hidden;  
padding: 0;  
position: absolute;}

This fairly modern technique will hide or clip content that does not fit into a 1-pixel visible area. Like off-screen content, it will be visually hidden but still readable by modern screen readers.

## Examples

Below are examples where off-screen or clipped content might be used to improve accessibility.

Important!

**Use these techniques judiciously!** Keep in mind that many screen reader users have some vision—what they see and what they hear should typically be in harmony. In general, screen reader-only content should be reserved for information is apparent visually but not apparent to blind screen reader users.

### Instructional cues and indicators

One fairly common use case for screen reader-only content is a search text input that is readily identified visually as a search field due to its position on a page and adjacent search button, but for which adjacent text is not provided. A hidden, associated `<label>` element with "Search terms" (or similar) text would ensure that the field is properly identified to screen reader users.

Another use case might be page breadcrumbs (such as the "[Home](/) > [Articles](/articles/) > CSS in Action..." text near the top of this page). These are a common convention due to their visual location and presentation. Because a screen reader accesses the breadcrumb links and content linearly, it may not be readily apparent to them that it is breadcrumbs. As such, hidden text of "You are here:" has been added just prior to the breadcrumbs to provide a cue/indicator to screen reader users about what follows.

### "Skip" links

["Skip to main content" or "Skip navigation" links](/techniques/skipnav/) are one of the few places where accessibility has a potentially negative impact on visual design and usability for some users. To be useful, the "skip" link should be one of the first on the page. Designers may balk at the idea of providing such a prominent link—particularly when that link will not be used by most site visitors. However, hiding the "skip" link visually using a technique above makes it much less usable to sighted keyboard users—a user group that can greatly benefit from this link.

One way to reconcile this conflict is to visually hide the link until the user tabs to it at which point it becomes visible to sighted users.

This technique uses two style definitions—one to visually hide the link, and another using the `a:focus` pseudo-class to visually reveal the link while it has focus.

#skip a  
{   
position:absolute;   
left:-10000px;   
top:auto;   
width:1px;   
height:1px;   
overflow:hidden;  
}   
   
#skip a:focus   
{   
position:static;   
width:auto;   
height:auto;   
}

These styles should then be applied to the "skip" link:

<div id="skip"><a href="#content">Skip to Main Content</a></div>

One possible drawback to this approach is that the sudden appearance of a link that was previously invisible will be unexpected and could potentially confuse the sighted keyboard user. The WebAIM.org site address this by implementing CSS transitions to animate the focused "skip" link from above the top of the page (as opposed to off-screen left) to the top left corner of the page, then back above the page when focus is lost. This ensures that the link is highly visible on screen for a longer period of time. You can see this in action by pressing the "Tab" key with focus at the top of this page.