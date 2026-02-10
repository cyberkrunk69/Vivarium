# The Role of Animation and Motion in UX

Source: https://www.nngroup.com/articles/animation-purpose-ux/

---

8

# The Role of Animation and Motion in UX

Page Laubheimer

![](https://media.nngroup.com/media/people/photos/2022-portrait-page-3.jpg.256x256_q75_autocrop_crop-smart_upscale.jpg)

Page Laubheimer

January 12, 2020
2020-01-12

[Share](#)

- [Email article](mailto:?subject=NN/g Article: The Role of Animation and Motion in UX&body=https://www.nngroup.com/articles/animation-purpose-ux/)
- [Share on LinkedIn](http://www.linkedin.com/shareArticle?mini=true&url=http://www.nngroup.com/articles/animation-purpose-ux/&title=The Role of Animation and Motion in UX&source=Nielsen%20Norman%20Group)
- [Share on Twitter](https://twitter.com/intent/tweet?url=http://www.nngroup.com/articles/animation-purpose-ux/&text=The Role of Animation and Motion in UX&via=nngroup)

Summary: 
Animation in UX must be unobtrusive, brief, and subtle. Use it for feedback, state-change and navigation metaphors, and to enhance signifiers.

In UX, motion and animation can be helpful and communicative, if used with restraint. Motion is most often appropriate as a form of *subtle* [feedback](https://www.nngroup.com/articles/indicators-validations-notifications/) for [microinteractions](https://www.nngroup.com/articles/microinteractions/), rather than to induce delight or entertain users. In this article, we explore the purposes of useful, unobtrusive feedback animation. In a second (forthcoming) article, we will discuss the details in timing and movement to make these animations appear smooth and natural.

The big advantage (and also drawback) of UI motion is that it [attracts user attention](https://www.nngroup.com/articles/animation-usability/). Our peripheral vision (specifically, through the rod-shaped photoreceptors in the human retina) is responsible for detecting motion.  Evolutionarily, the fact that we can detect a movement outside the center of our field of vision is, of course, an advantage: we can discern danger and protect ourselves. But that means that we are sensitive and prone to be [distracted](https://www.nngroup.com/videos/distracting-animations/) by any type of motion (meaningful or not). That’s why motion in user interfaces can easily become annoying: it’s hard to stop attending to it, and, if irrelevant to the task at hand, it can substantially degrade the user experience (as any web user who has encountered a moving [advertisement](https://www.nngroup.com/articles/most-hated-advertising-techniques/) can attest).

Although animations *can* be useful and can build [user expectation](https://www.nngroup.com/videos/mental-models/)s about the UI, they should be used with a light touch — primarily as a tool for providing users with easily noticeable, smooth feedback.

## In This Article:

- [Purpose of UI Animations](#toc-purpose-of-ui-animations-1)
- [Motion to Communicate State Change](#toc-motion-to-communicate-state-change-2)
- [Attention Grabbing and Attention Hijacking](#toc-attention-grabbing-and-attention-hijacking-3)
- [References](#toc-references-4)

## Purpose of UI Animations

When animation is used in a subtle way, it can help users build mental models about how the system works and how they can interact with it.  Animations are less critical for user experience when they are simply time-filling visual stimulations during moments of transition (in fact, it’s these down-time animations that often frustrate participants in usability testing).  Instead of using animations to provide [surface-level delight](https://www.nngroup.com/articles/theory-user-delight/) (that quickly sours), animations can be leveraged for usability: as clues about what is currently happening with the system, as signifiers for how UI elements will behave, and as easily understandable spatial metaphors for the user’s location in the information space.

### Motion for Feedback

Animations are often helpful as a form of noticeable feedback that an action has been recognized by the system.  A ubiquitous example is the animation of a navigation menu sliding over the page when a [hamburger](https://www.nngroup.com/articles/hamburger-menus/) icon is tapped.  Because our visual systems are so attuned to motion, a short animation can ensure that users see the feedback.

[Your browser does not support the video tag.](https://media.nngroup.com/media/editor/2020/01/06/museumnathistory-accordion-trimmed.mp4)

*American Museum of Natural History: When clicking the*Exhibitions*menu icon in the middle of the page, a menu panel slides over from the left side on top of the page’s content, rather than appearing suddenly like a new page.*

[Your browser does not support the video tag.](https://media.nngroup.com/media/editor/2020/01/06/epicurious-shopping-list.mov)

*Epicurious for iPhone: A shopping-list feature shows a subtle animated feedback when the user adds a new item to the list: upon hitting the* Done *button on the keyboard, the word that was just typed (*Coffee, *in this case) instantly becomes light gray, and then quickly changes to black to show that it has been accepted. At the same time, the input field both fades in and slides down below, signaling that it is waiting for new input.*

Sometimes, static visual feedback is ignored due to c[hange blindness](https://www.nngroup.com/videos/change-blindness/). For example, people may not notice the shopping-cart–badge update after clicking the *Add to cart* button in the Cuisinart example below. An animation increases the chance of noticing that feedback. (Another alternative would be to make the static feedback more prominent — e.g., through a dialog box or using a bigger badge. Both solutions would likely be more intrusive than a simple animation.)

![An ecommerce product page that features no animated feedback when adding an item to the cart](https://media.nngroup.com/media/editor/2020/01/06/cuisinart.png)

*Cuisinart.com: After the user clicks*Add to cart, *the cart badge simply updates, with no animation. Because the badge is small and far away from the*Add to cart *button (which is likely where the user is looking), it’s easy to miss this change. The result could be that the user adds the same product to the cart multiple times.*

And animations can also be used as a form of feedback *before* the user commits to an action, such as previewing the new location of an item when using drag-and-drop to reorder a list.

[Your browser does not support the video tag.](https://media.nngroup.com/media/editor/2020/01/06/drag-and-drop-preview.mov)

*Airtable: When drag-and-drop is used to reorder columns in a table, a subtle animation gives a preview of the new order before the user lets go and commits to the action.*

## Motion to Communicate State Change

Motion can be used to indicate that the interface switched to a different state — for example, because of a mode change. [Modes](https://www.nngroup.com/articles/modes/) are often a difficult concept to communicate to users, but animation can help in two ways: (1) by making the mode change noticeable; and (2) by providing a conceptual metaphor of the mode transition. For example, morphing a pencil icon into a disk after it was clicked on signals the transition from *Edit* to *Save* mode more clearly than swapping one icon out for the other instantly.

[Your browser does not support the video tag.](https://media.nngroup.com/media/editor/2020/01/06/material-button-transform.mov)

*Material Design: A pencil icon that transforms into a + icon helps to communicate the difference between the*Edit*mode and the*Add new*mode.*

In addition to showing a transition between modes or views of data, animations are also helpful for communicating state changes that are not triggered by users’ actions. For example, loading indicators show that the system is not yet ready to accept input.  One form of this is a “skeleton screen” (a placeholder UI that looks like a wireframe of the loading page, with no content) that is animated by a light glare moving across it.

[Your browser does not support the video tag.](https://media.nngroup.com/media/editor/2020/01/06/hipmunk-loading.mov)

*Hipmunk: While loading flight-search results, Hipmunk offers several animated cues. First, there is an animated chipmunk pretending to fly. (While cute, the chipmunk is not essential for feedback, but is helpful to establish the [brand tone.](http://www.nngroup.com/articles/interaction-branding/)) However, at the same time, other, more-communicative animations occur: the number of flight results climbs steadily from 0 to 754, indicating that the system is performing multiple federated searches concurrently. Also, a placeholder shows where content will appear as flight results load.  A [progress bar](http://www.nngroup.com/articles/progress-indicators/), along with two animated ellipses, indicates that results are still loading.  Finally, as new results are loaded and the relevance order changes, a subtle animation shows new results appearing within the list and is meant to communicate that the order of the search results is changing dynamically.  However, the number of simultaneous animations is overwhelming: the power of any of these animations to pull the user’s attention is diminished by competition from all the others.*

### Motion for Spatial Metaphors and Navigation

The structure of a complex information space is often challenging to communicate to users without taxing their cognitive resources or taking up too much screen space. Scanning through navigation menus, tree diagrams, or even [breadcrumbs](https://www.nngroup.com/articles/breadcrumbs/) to figure out where one is in the information hierarchy is a complex type of cognitive work. While animation alone is not a suitable substitute for visible navigation with clear, unbranded labels, it can signal to users the direction in which they are moving within a process or hierarchy; this **supplemental** **cue** can make navigation through a complex IA more intuitive and understandable.

Zooming animations can help users understand the direction of their journey into a hierarchical information space without looking at a tree diagram. Zooming out shows less detail, but more objects, thus suggesting that the user travels up into the hierarchy, whereas zooming in shows more detail, but fewer objects, creating the impression of going deeper into the hierarchy.

[Your browser does not support the video tag.](https://media.nngroup.com/media/editor/2020/01/06/apple-photos-zoom.mp4)

*iOS Photos uses a zoom metaphor to show the user’s location in the information space (in this case, represented by my endless library of photos of my dog, Daphne). Going between*Years, Months*, and*Days*has a subtle zoom-in or zoom-out animation that helps users understand whether they are going up or down in the hierarchy of photos. This approach helps keep the user’s attention on content (cute dog photos), and not on the navigation [chrome](http://www.nngroup.com/articles/browser-and-gui-chrome/).*

Likewise, a slide-over animation helps to establish that a user is moving forward or backward within a process such as checkout.

[Your browser does not support the video tag.](https://media.nngroup.com/media/editor/2020/01/06/amtrak-process.mov)

*Amtrak shows a subtle slide-over animation to indicate that the user is moving forward through the process of booking a train.*

Animations can also prevent disorientation and telling people if they are on the same page or have moved on — particularly on mobile, where context can be lost due to the small screen size.  [Accordions](https://www.nngroup.com/articles/mobile-accordions/), [anchor links](https://www.nngroup.com/articles/in-page-links/), and menu overlays can be disorienting or confusing if the change appears instantaneously; since a menu overlay fills the entire screen, the relationship between the overlay and the underlying page (e.g., “is this content a new page, or is it something else?”) is hard to understand without an animated cue. (Why does it matter if users know where they are? If they think they are on a new page, they are often tempted to use the *Back* button to navigate to the previous view; unfortunately, in the case of overlays or accordions, that action will take them away from the page instead of simply closing the element.)

[Your browser does not support the video tag.](https://media.nngroup.com/media/editor/2020/01/06/webmd-accordions.mov)

*WebMD: When opening an accordion on the page, the associated content immediately shows up at the top of the screen (with no animation). The user may think that the new content is on a brand new page. A scrolling animation (showing how the page is moved so that the accordion is at the top of the screen), followed by a moving expansion could help the user to understand that this is not a completely new page, but an accordion within the page’s content.*

[Your browser does not support the video tag.](https://media.nngroup.com/media/editor/2020/01/06/metmuseum-anchor-link.mov)

*MetMuseum: [Anchor links](http://www.nngroup.com/articles/in-page-links/) are often confusing or disorienting for users, but in this case, the anchor links use a smooth scrolling animation to show (1) that the content is all contained on a single page and  (2) where it is on that page.*

### Motion as a Signifier

Animations help users understand how to interact with UI elements. The direction (or other attributes) of the motion signifies the type of acceptable actions. For example, a [card](https://www.nngroup.com/articles/cards-component/) that expands from the bottom of the screen towards the top signals to the user that it can be closed by pulling down. A new card that comes from the right of the screen signals that it can be closed by swiping it to the right.

[Your browser does not support the video tag.](https://media.nngroup.com/media/editor/2020/01/06/apple-music-card.mp4)

*Apple Music for iPhone: the*Now Playing *card animates up into place in a manner that helps the user understand that this view can be dismissed by pulling down, rather than swiping left or right on the edge.*

[Your browser does not support the video tag.](https://media.nngroup.com/media/editor/2020/01/06/car2goedited.mp4)

*Car2Go for iPhone: A short bounce animation is a signifier that [swiping](http://www.nngroup.com/articles/contextual-swipe/) across the list item reveals options.*

## Attention Grabbing and Attention Hijacking

Because the human visual system is very sensitive to motion (particularly, to motion that appears to have [animacy](https://www.nngroup.com/articles/animation-usability/)), animation can be used to grab users’ attention, for better or worse. On the one hand, it can make a subtle signifier obvious, but on the other hand, gratuitous animations distract and annoy the user. Further, using animation to hijack the users’ attention or create a [fear of loss](https://www.nngroup.com/articles/prospect-theory/) is a [dark pattern](https://www.nngroup.com/videos/shame-users-to-convert/): an unethical application of user-experience principles and cognitive psychology to get users to do something they ordinarily wouldn’t.

[Your browser does not support the video tag.](https://media.nngroup.com/media/editor/2020/01/06/action-button.mov)

*Benign: Refinery29 embeds a poll in the middle of a story about social media’s mental health effects and shows a radiating halo on the slider’s knob to reinforce the signifier and catch the user’s attention. This limited use of animation is a relatively benign (though mostly unhelpful) way of catching the user’s attention. Were animations widespread throughout the site, this animation would be a distracting usability problem.*

[Your browser does not support the video tag.](https://media.nngroup.com/media/editor/2020/01/06/the-outline-gratiutious.mov)

*Distracting: The moving squiggle on Outline’s content pages adds no benefit, but needlessly draws the attention of the user away from the content.*

[Your browser does not support the video tag.](https://media.nngroup.com/media/editor/2020/01/06/warmly-decor.MP4)

*Dark pattern: A flashing countdown clock on warmlydecor.com indicates that a sale is about to end (by a puzzling coincidence, in just under an hour for every single product on the site, no matter when you visit). The clock activates the powerful loss-aversion instinct in users, and the flashing (with a subtle enlarging of the digits as they flash) is very difficult to avoid attending to.*

In summary, when UI animations are subtle, unobtrusive, and brief, they can improve the user experience and can communicate feedback and state changes, prevent disorientation, and strengthen signifiers. But they should not be overused, as they can easily become overwhelming and distract users.

## References

Head, V. (2016) [*Designing Interface Animation*](https://www.amazon.com/Designing-Interface-Animation-Meaningful-Experience/dp/1933820322/?tag=useitcomusablein). Rosenfeld Media.

Saffer, D. (2014). *[Microinteractions](https://www.amazon.com/dp/1491945923?tag=useitcomusablein).* O’Reilly Media.

Pratt, J., Radulescu, P., Guo, R.M., & Abrams, R.A. (2010). [It's Alive! Animate motion captures visual attention](http://abrams.wustl.edu/artsci/reprints/PrattRadulescuGuoAbrams2010.pdf). *Psychological Science*, 21, 1724–1730

animation,signifiers,Design Patterns,gestures

## Related Topics

- Design Patterns
  [Design Patterns](/topic/design-patterns/)

## Learn More:

- [![](https://media.nngroup.com/media/videos/thumbnails/Button_States_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Button States 101

  Kelley Gordon
  ·
  3 min](/videos/button-states-101/?lm=animation-purpose-ux&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/2-Factor_Authentication_2-FA_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  2-Factor Authentication (2-FA)

  Tim Neusesser
  ·
  4 min](/videos/2-factor-authentication/?lm=animation-purpose-ux&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/UX_Animations_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  UX Animations

  Page Laubheimer
  ·
  4 min](/videos/ux-animations/?lm=animation-purpose-ux&pt=article)

## Related Articles:

- [What Parallax Lacks

  Katie Sherwin
  ·
  7 min](/articles/parallax-usability/?lm=animation-purpose-ux&pt=article)
- [Change Blindness in UX: Definition

  Raluca Budiu
  ·
  8 min](/articles/change-blindness-definition/?lm=animation-purpose-ux&pt=article)
- [Animation for Attention and Comprehension

  Aurora Harley
  ·
  8 min](/articles/animation-usability/?lm=animation-purpose-ux&pt=article)
- [Design-Pattern Guidelines: Study Guide

  Samhita Tankala and Alita Kendrick
  ·
  6 min](/articles/design-pattern-guidelines/?lm=animation-purpose-ux&pt=article)
- [Scroll-Triggered Text Animations Delay Users

  Aurora Harley
  ·
  4 min](/articles/scroll-animations/?lm=animation-purpose-ux&pt=article)
- [Timing Guidelines for Exposing Hidden Content

  Aurora Harley
  ·
  6 min](/articles/timing-exposing-content/?lm=animation-purpose-ux&pt=article)