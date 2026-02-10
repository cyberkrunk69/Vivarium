# Links and HypertextIntroduction to Links and Hypertext

Source: https://webaim.org/techniques/hypertext/

---

# Links and Hypertext Introduction to Links and Hypertext

You are here: [Home](/) > [Articles](/articles/) > Links and Hypertext

## Overview

![](media/link_code.jpg) Hypertext links are one of the most basic elements of HTML, as its name implies (HTML stands for *HyperText* Markup Language). As such, making hypertext links accessible is one of the most basic and most important aspects of web accessibility. For the most part, this is an easy task. Standard hypertext links work with all technologies and platforms and users of all abilities can access them, whether directly or through the use of some sort of assistive technology. As might be expected though, there is more to hypertext link accessibility than simply creating a link. Some types of links are more accessible than others, and some types of links are completely inaccessible to people with certain types of disabilities. Because links are so basic to the functionality of web content, inaccessible links are one of the most severe barriers to overall accessibility.

## Keyboard Accessibility of Links

Users must be able to navigate to and select each link using the keyboard alone. In most browsers, the Tab key allows users to jump from link to link, and the Enter key allows users to select a link. If the only way to access a link is with a mouse, the link is unusable by people who cannot use a mouse. How is it even possible to create a link that is inaccessible by keyboard? The most common method is by using JavaScript event handlers that do not permit keyboard access (see the article on [JavaScript Event Handlers](/techniques/javascript/eventhandlers)).

Important

Links must have a non-empty `href` attribute in order to be considered true links and to be accessible to keyboard users.

One of the most serious barriers is to create links that go nowhere. Developers sometimes use JavaScript to create dynamic menus that drop down when the user hovers over certain links with the mouse. In some cases, the link itself goes nowhere at all, and its only purpose is to expose the links in the drop-down menu, which do have real destinations. Links like this often have a pound sign as the link destination, which means that the link destination is the same page; clicking on the link accomplishes nothing. Both keyboard users and mouse users will experience nothing at all when attempting to activate the link.

Bad Example

The link in this example goes nowhere. Its only purpose is to activate a JavaScript function.

`<a href="#" onmouseover="dropdownmenu()">Products</a>`

Mouse users will at least be able to click on the links in the drop-down menu, but keyboard users cannot access the drop-down menu, so the link is completely useless and all of the link destinations in the drop-down menu are completely inaccessible to them. One solution is to abandon the drop-down menu and instead use standard hypertext links. Another solution is to specify a real link destination (e.g. `href="products.htm"`) which would list the same links that are available via the drop-down menu. For more information see example 2 in [`onMouseOver` section of the JavaScript Event Handlers article](/techniques/javascript/eventhandlers#onmouseover).

## Screen Readers and Links

### Screen readers generally inform users that a piece of text (or a graphic) is a link

Most screen readers say "link" before each link. For example, a "products" link would be read as "link products" by JAWS.

**Implication:** Links do not need to include "link" in the link text, because all users already know that the link is a link. This is more of an issue with graphics used as links. The `alt` text for a graphic does not need to say "link" or "link to." Otherwise, JAWS users will hear "link graphic link to Products," which is redundant.

### Screen reader users often navigate from link to link, skipping the text in between

Tabbing from link to link is a way of skimming web content, especially if users are trying to find a particular section of a web site.

**Implication 1:** Links should make sense out of context. Phrases such as "click here," "more," "click for details," and so on are ambiguous when read out of context. At the same time, it would be overkill to ensure that every detail about a link destination is discernible by listening to the link context. Users wouldn't want to hear "Products page on which a list of all of our products are presented, including software products and training products, with a list of prices and availability by region (this page uses the same navigation template as the page you are now on)." Perhaps a better alternative would be a link that simply says "Products."

**Implication 2:** Place the distinguishing information of links at the beginning of a link. Don't put extra information first, For example, don't say "Link opens in a new window: Products." Instead, say "Products (opens in a new window)" (or something along those lines). This is especially important in this example if several links open in a new window. With the explanatory information first instead of the main information, screen reader users would have to listen to the phrase "link opens in a new window" over and over again. They will have a harder time distinguishing between different links, or at least it will take them
longer.

### Screen reader users sometimes obtain an alphabetically-organized list of links

Screen readers allow users to view the list all links present on the page, using a keyboard shortcut. This is especially useful if they are searching for a particular link.

**Implication:** Use link words and phrases that are unambiguous and that can be intuitively organized regardless of order (the screen reader might sort them in order of appearance or alphabetically). For example, the phrase "contact us" is a common one that users may want to access. If the link says "you can contact us," or "how to contact us," or some other phrase that is less intuitive, users may have a more difficult time finding the link.

[Next](link_text)