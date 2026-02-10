# Cards: UI-Component Definition

Source: https://www.nngroup.com/articles/cards-component/

---

8

# Cards: UI-Component Definition

Page Laubheimer

![](https://media.nngroup.com/media/people/photos/2022-portrait-page-3.jpg.256x256_q75_autocrop_crop-smart_upscale.jpg)

Page Laubheimer

November 6, 2016
2016-11-06

[Share](#)

- [Email article](mailto:?subject=NN/g Article: Cards: UI-Component Definition&body=https://www.nngroup.com/articles/cards-component/)
- [Share on LinkedIn](http://www.linkedin.com/shareArticle?mini=true&url=http://www.nngroup.com/articles/cards-component/&title=Cards: UI-Component Definition&source=Nielsen%20Norman%20Group)
- [Share on Twitter](https://twitter.com/intent/tweet?url=http://www.nngroup.com/articles/cards-component/&text=Cards: UI-Component Definition&via=nngroup)

Summary: 
A “card” is a UI design pattern that groups related information in a flexible-size container visually resembling a playing card.

In recent years, we’ve seen a lot of interest towards creating modular UI patterns that work well across a variety of screens and window sizes. One such new UI component is the **card** — a snapshot-like display intended to encourage users to click or tap to view more details.

> **Card:** A container for a few short, related pieces of information. It roughly resembles a playing card in size and shape, and is intended as a linked, short representation of a conceptual unit.

![Wireframed image of a card component](https://media.nngroup.com/media/editor/2016/10/14/card-wireframe-export-unannotated-v3.png)

*This wireframed example of a card component features several different types of information: an image, a title, a short summary, a time stamp, a hashtag, and a secondary call-to-action button for social media sharing. The design (with optional rounded corners) visually resembles a playing card; the card has a visible border, is placed on a contrasting background, and uses a slight drop shadow as a signifier that the entire card is clickable. This card also contains two secondary clickable elements (the hashtag #dayhikes and the Share button), separated from the content area by a horizontal line. (Note that this line doesn't undermine the visual grouping of the entire card.)*

Cards are often associated with [flat design 2.0](https://www.nngroup.com/articles/flat-design/): they retain some aspects of the aesthetic of flat design, but reintroduce visual depth as a [signifier](http://jnd.org/dn.mss/signifiers_not_affordances.html) of clickability. Though the basic concept is older, in the last few years, cards have received a lot of attention in the software-design world, with many high-profile sites and companies (e.g., Google’s Material Design, Twitter's card component) embracing them.

Cards have 4 key properties:

**1.** **Cards are used for grouping information.**

A card [chunks](https://www.nngroup.com/articles/chunking/) several different (but related) pieces of information into one digestible unit — be it an article on a news website, a product on an ecommerce site, or a post on a social app. A single card will typically include a few different types of media, such as an image, a title, a synopsis, sharing icons, or a call-to-action button — all associated with the same concept.

**2.** **Cards present a summary and link to additional details..**

A card is usually short and offers a **linked** **entry point** to further details, rather than the full details themselves. It is intended as a [high–information-scent](https://www.nngroup.com/articles/information-scent/) outline used to entice users to click through to further details contained on a separate page.

**3.** **Cards resemble physical cards.**

Cards use a border around the grouped content, and the background color within the card that differs from background color of the underlying canvas. These visual-design elements create a strong sense that the different bits of information contained within the border are grouped together.

Quite often, cards use a slight drop shadow to show depth, which is a clickability signifier. For most implementations, clicking or tapping *anywhere* on the card link to a details page (though some cards, like the one in our previous example, also include some secondary call-to-action buttons or links in addition to the main link available). This larger touch zone substantially improves usability on both touchscreen devices and mouse-based devices (due to [Fitts’ Law](http://www.asktog.com/columns/022DesignedToGiveFitts.html)).

**4.** **Cards allow for flexible layouts.**

When multiple cards are used together in a layout, they often do not all have the same type of information — some cards might include a text summary, hashtags, or an image whereas other cards on the same page may include totally different details. Cards allow for varying height to accommodate differing amounts or types of content, but typically the width is fixed from one card to the next.

![Pinterest using a card-based layout.](https://media.nngroup.com/media/editor/2016/10/14/pinterest.png)

*Pinterest's use of cards showcases how cards excel at grouping together heterogenous items, where each card features different types and amounts of information and, thus, occupies a different amount of vertical space. Cards include rich media (the thumbnail image), title, secondary calls-to-action (*Like *and*Share *buttons), and attributions. Each card uses visual elements such as background color,border, and shadow to differentiate itself from the background, clearly group the card elements, and indicate clickability. Clicking on a card takes the user to a detail screen for that content. Without the visual style of the card, grouping each item's ingredients together clearly in a way that separates them from other items on the page would require a lot more negative space and would waste valuable screen real estate on mobile phones and tablets.*

## In This Article:

- [UI Cards vs. Hypertext Card Model](#toc-ui-cards-vs-hypertext-card-model-1)
- [Principle of Common Regions Creates Visual Groups](#toc-principle-of-common-regions-creates-visual-groups-2)
- [When Cards Are Useful](#toc-when-cards-are-useful-3)
- [Conclusion](#toc-conclusion-4)

## UI Cards vs. Hypertext Card Model

Seasoned UX pros may recognize the card concept as being related (both in name and in concept) to the [card (or deck-of-cards) model](https://www.nngroup.com/articles/two-basic-hypertext-presentation-models/) of presenting linked information from the dawn of hypertext, in the 1990s. This model refers to splitting content into discrete pages of fixed size and is an alternative to vertical scrolling: navigating through carded content is similar to turning the pages of a book as opposed to unfurling a long paper scroll. This card model saw a revival when the [iPad first came out](https://www.nngroup.com/articles/ipad-usability-first-findings/), when many apps were trying to control the look of each page presented to the user. You are probably familiar with the deck-of-cards paradigm from mobile weather apps — most of them employ it for displaying the weather in different cities.

![iOS weather app uses the deck-of-cards conceptual model](https://media.nngroup.com/media/editor/2016/10/14/iosweather.png)

*The iOS Weather app presents each city's weather forecast in the hypertext deck-of-cards style (rather than the UI-card-component style that is the main subject of this article). Each city is a full-screen* node*, and viewing the weather in other cities is accomplished by swiping to the left or right to see another full-screen* node*, similar to the experience of flipping pages in a book.*

The contemporary card pattern is based on the same idea of grouping content into discrete, completely visible units with controlled information layout and appearance. However, the contemporary card that this article is focused on is not a full-screen item (as in the older card model), but takes up just a small region of the screen, and contemporary cards are often used in a layout with multiple cards per screen.

This goes to remind us two critical things about interface design: 1) everything old is new again, meaning that [new design trends are often not so revolutionary after all](https://www.nngroup.com/articles/roots-minimalism-web-design/), and may be revived with slight variations, and 2) because history repeats itself, [usability guidelines and interaction design principles are durable](https://www.nngroup.com/articles/durability-of-usability-guidelines/) and remain relevant for a long time, even in the rapidly innovating world of user-experience design.

## Principle of Common Regions Creates Visual Groups

Cards take advantage of one of the common-regions principles in cognitive psychology:multiple items contained together within a boundary are more likely to be perceived as being grouped. This principle *can* supersede the powerful [Gestalt law of proximity](https://www.nngroup.com/articles/closeness-of-actions-and-objects-gui/) (where items placed near each are perceived as grouped), allowing items that are further away to be more explicitly visually grouped. The principle of common regions frees designers from using [negative space](https://www.nngroup.com/articles/form-design-white-space/) to create explicit connections among several items. ![](file://localhost/Users/Page/Library/Group%20Containers/UBF8T346G9.Office/msoclip1/01/clip_image004.png)

![triangles demonstrating the law of proximity](https://media.nngroup.com/media/editor/2016/10/14/law-of-proximity.png)

***Top:**The law of proximity creates a strong sense of visual grouping among triangles 2 & 3 and 4 & 5, because they are placed close to one another, and further apart from their neighbors 1 & 6. The designer must use negative space (i.e., empty space between unrelated elements) to convey grouping.*

![triangles demonstrating the common regions principle](https://media.nngroup.com/media/editor/2016/10/14/common-regions.png)

***Bottom:**The common-regions principle trumps the law of proximity: through use of a border and background color (much like the card component uses), the same set of triangles are grouped differently; a strong visual signal is sent that triangles 1 & 2, 3 & 4, and 5 & 6 are grouped, even though the layout is identical with that in the top figure. In the unlikely case that usability testing showed the need for even stronger grouping, each card could be made to have a different background color.*

## When Cards Are Useful

- **Cards are better suited when users browse for information than when they search.**

Multiple-card layouts are frequently used instead of [list views of content](https://www.nngroup.com/articles/list-entries/). Cards are, however, less appropriate than lists when people search for information for three major reasons, all related to their variable size:

**1.** Card layouts typically **deemphasize** the ranking of content. (However, even though they lack the strong hierarchy signals of list views, multicard displays still obey typical page-hierarchy laws: content at the top and on the left of the page is more discoverable and perceived as more important.)

**2.** Card layouts are less scannable than lists. A standard vertical list view (in which each item occupies a new row in the layout, and may still contain mixed media such as an image, title, summary, and so forth) is more scannable than cards because the positioning of the individual elements is fixed in size and more predictable for the eye. Thus, cards are not appropriate when users search for a specific item from a list or look for a particular piece of content.

**3.** Cards take more space. Because cards are bigger than a line of text, any given screen size can’t show as many cards in a single view as would be possible in a list view. The more things are viewable without scrolling, the less demand is placed on users’ [short-term memory](https://www.nngroup.com/articles/short-term-memory-and-web-usability/).

![a card based layout next to a list based layout](https://media.nngroup.com/media/editor/2016/10/14/card-vs-list-v3.png)

***Left**: Scanning products in a card-based list is challenging to quickly find basic information such as price, since the layout is not predictably arranged, and a user can't easily anticipate where to look on the page to find that information.  
**Right**: A vertical list easily supports scanning for price from one product to the next, as this information is placed in a predictable location on each item in the list.*

Cards are also a poor choice when users need to [compare between multiple options](https://www.nngroup.com/articles/explicit-differences/), since cards often aren't structured in a predictable way from item to item; our eyetracking research revealed that users look back and forth multiple times between items when they compare them, so you should facilitate this process by [using a consistent visual treatment of items that will be compared](https://www.nngroup.com/articles/list-entries/).

![Gaze plot of eye tracking on a card-based layout where users looked back and forth](https://media.nngroup.com/media/editor/2016/10/21/cards-heatmap-comparison.png)

*A gaze plot of a user's eyetracking session on a card-based layout. The user was asked to find and read a story that looked interesting to her. The flexible-card layout does not clearly indicate a hierarchy of stories in order, so the user looks around back and forth in a semirandom pattern, looking for any compelling information before deciding which story to click on and read further details. Note that the user looks back and forth between the same stories repeatedly, comparing between options before clicking. The irregular layout makes this comparison behavior a more difficult undertaking than a vertical list, in which similar information would be located in predictable, consistent places for each item.*

- **Cards work best for collections of heterogeneous items** (i.e. not all the content is of the same basic type).

Cards are an excellent choice for dashboard applications and for social or aggregation sites that display a variety of content types at the same time on the same page. In such situations, the card metaphor can help create more obvious differences between items, and each card can accommodate different ingredients, if, for example, not all cards on a page need to include a title, byline, or other specific bit of information.

![Cards used in a dashboard application from Salesforce](https://media.nngroup.com/media/editor/2016/11/08/salesforcedashboard.png)

*Salesforce's dashboard system uses cards effectively to show heterogenous content and media together. Clicking on any card produces a full, detailed report for that item. Items have different sizes and are clearly separated from each other. [Image attribution](http://releasenotes.docs.salesforce.com/en-us/winter16/release-notes/rn_salesforce1_reporting_dashboard_run_read.htm)*

When presenting very homogenous items (such as a list of **similar** blog posts, products, or news stories), consider using a standard vertical list of items (or, in certain cases where the items are similar and are all from a narrowly defined category, [grids of images](https://www.nngroup.com/articles/image-vs-list-mobile-navigation/)) instead of cards to support scannability and also comparisons among items.

For example, placing all the photos in an online photo album on separate cards is not necessary, since they are all of a similar type, are clearly self-contained without the border, background, and shadow, and you don't get *additional* details when you click on it (you simply get a larger version of the same image). A gallery of photos is the type of content better [served by a regular grid](https://www.nngroup.com/articles/image-vs-list-mobile-navigation/).

## Conclusion

Cards are a useful UI component for grouping several related pieces of information together for providing a linked entry point to further details on that content. Cards work especially well in contexts where they provide summaries of many different kinds of content, rather than when simply used as a modern-looking replacement for a list of content.

## Related Courses

- [#### Emerging Patterns in Interface Design

  Trending UX patterns and their impact on the total user experience

  Interaction](/courses/emerging-patterns-interface-design/?lm=cards-component&pt=article)

Visual Design,Design Patterns,graphical user interfaces,web trends,gestalt,minimalism

## Related Topics

- Visual Design
  [Visual Design](/topic/visual-design/)
- [Design Patterns](/topic/design-patterns/)

## Learn More:

- [![](https://media.nngroup.com/media/videos/thumbnails/Grids_101_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Grids 101

  Kelley Gordon
  ·
  4 min](/videos/grids-101/?lm=cards-component&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Visual_Design_Principles_in_Action_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Visual Design Principles in Action

  Rachel Krause
  ·
  6 min](/videos/visual-design-principles-in-action/?lm=cards-component&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/maxresdefault_2.webp.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Why 90’s Designs Are Coming Back

  Megan Chan
  ·
  4 min](/videos/cyclical-design-trends/?lm=cards-component&pt=article)

## Related Articles:

- [Testing Visual Design: A Comprehensive Guide

  Megan Chan
  ·
  10 min](/articles/testing-visual-design/?lm=cards-component&pt=article)
- [5 Principles of Visual Design in UX

  Kelley Gordon
  ·
  8 min](/articles/principles-visual-design/?lm=cards-component&pt=article)
- [AI-Powered Tools for UX Research in 2023: Issues and Limitations

  Feifei Liu and Kate Moran
  ·
  10 min](/articles/ai-powered-tools-limitations/?lm=cards-component&pt=article)
- [The Risks of Imitating Designs (Even from Successful Companies)

  Kathryn Whitenton
  ·
  5 min](/articles/risks-imitating-designs/?lm=cards-component&pt=article)
- [Web UX: Study Guide

  Huei-Hsin Wang
  ·
  15 min](/articles/web-ux-study-guide/?lm=cards-component&pt=article)
- [Executing UX Animations: Duration and Motion Characteristics

  Page Laubheimer
  ·
  9 min](/articles/animation-duration/?lm=cards-component&pt=article)