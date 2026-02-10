# Touch Targets on Touchscreens

Source: https://www.nngroup.com/articles/touch-target-size/

---

8

# Touch Targets on Touchscreens

Aurora Harley

![](https://media.nngroup.com/media/people/photos/Aurora-Harley-20190601SF.jpg.256x256_q75_autocrop_crop-smart_upscale.jpg)

[Aurora Harley](/articles/author/aurora-harley/)

May 5, 2019
2019-05-05

[Share](#)

- [Email article](mailto:?subject=NN/g Article: Touch Targets on Touchscreens&body=https://www.nngroup.com/articles/touch-target-size/)
- [Share on LinkedIn](http://www.linkedin.com/shareArticle?mini=true&url=http://www.nngroup.com/articles/touch-target-size/&title=Touch Targets on Touchscreens&source=Nielsen%20Norman%20Group)
- [Share on Twitter](https://twitter.com/intent/tweet?url=http://www.nngroup.com/articles/touch-target-size/&text=Touch Targets on Touchscreens&via=nngroup)

Summary: 
Interactive elements must be at least 1cm × 1cm (0.4in × 0.4in) to support adequate selection time and prevent fat-finger errors.

As a new parent, I increasingly find myself using my smartphone as my primary computer. Jotting down a note, selecting next week’s meal delivery kits, shopping online, and tracking my child’s eating and sleeping patterns all need to happen one-handed, quickly, while holding this tiny new human. Whether these efforts are successes or failures often comes down to a basic, yet critical detail of mobile design: touch target size and placement.

Adequately sized touch targets are critical for using an interface — let alone ease of use! We’ve all experienced frustration caused by small touch targets: visible, yet unresponsive to our taps — or worse, forcing us to accidentally trigger nearby links. These moments make us feel like gawky giants in a too small world.

Often, this issue is described as a “fat finger” problem because users’ fingers are larger than the desired targets — clumsy cocktail sausages poking at screens. But the **fat fingers are not the real culprit; the blame should lie on the tiny targets.** Designers who prioritize aesthetics over functionally too often forget to create targets that can be easily and accurately selected.

## In This Article:

- [Size Matters](#toc-size-matters-1)
- [Mind the Gap — Crowding Causes Errors](#toc-mind-the-gap-crowding-causes-errors-2)
- [View–Tap Asymmetry](#toc-viewtap-asymmetry-3)
- [When Bigger Is Better](#toc-when-bigger-is-better-4)
- [Conclusion](#toc-conclusion-5)

## Size Matters

Based on a study conducted by Parhi, Karlson and Bederson, for users to quickly and accurately select a touch target, its **minimum size should be 1cm × 1cm (0.4in x 0.4in)**. Note that this is a physical measurement: although our designs may be digital, we use our hands to manipulate these digital elements on a touch screen. Citing dimensions in pixel value doesn’t effectively communicate this physical aspect of touch targets, and quickly becomes meaningless once you consider the vast variety of screen densities for the plethora of devices at our fingertips (pun intended).

A past study from the MIT Touch Lab found that the average person’s fingertips are 1.6–2cm (0.6­­–0.8 in) wide. The impact area of the typical thumb is even larger — an average of 2.5cm (1 inch) wide! **Designing touch targets to account for the physical dimensions of users is basic user-centered design**.

When touch targets are too small, users take longer to tap them. ([Fitts’ law](https://www.nngroup.com/videos/fittss-law/) says that the time to reach a target depends on the distance to the target and the size of the target — thus, smaller targets take longer to reach, because of the added precision required of the user’s movements, than bigger targets placed in the same spot.)

For instance, the Glow Baby app visualized the history of tracked sleeping times, diaper changes, and feeding sessions with various colored bars or icons so users could detect possible patterns in baby’s behavior. Tapping on an individual event displayed detailed information, such as the exact time of a nursing session or when baby fell asleep. Unfortunately, because the visual reflected the length of time the baby was sleeping or nursing, if the session was very short the tap target became too small to easily tap.

![2 screenshots of small tap targets on the history page within the Glow Baby app.](https://media.nngroup.com/media/editor/2019/04/10/glowbaby_mobileapp_history_smalltargets.png)

*Glow Baby: The yellow and purple bars in the tracking history became nearly impossible to select if a nap or nursing session was very short. For example, a nursing session on March 15 was only 5 minutes, which caused the tap target (a thin yellow bar) to be only 6mm (0.2in) wide and not even 1mm (0.04in) tall. It took about 10 tries to select the session to get the right-hand screenshot, in which the selected target is shown in orange.*

## Mind the Gap — Crowding Causes Errors

Not only do small targets take longer to reach, but they also increase the chance of a [slip](https://www.nngroup.com/articles/slips/): accidentally tapping a wrong target that is placed too close to the desired one. Even when an error is avoided, just noticing that an element could be problematic to select adds to the perception that the interface is difficult to use.

[Maps on touchscreens](https://www.nngroup.com/articles/mobile-maps-locations/) often cause touch-target errors. When many locations are presented in a map view, the markers for each location are so small and densely packed that it becomes nearly impossible to precisely select a particular pinpoint. In testing, we often see users immediately make a “focus face” when viewing a map on mobile, as they realize it will require effort to use.

![Screenshot of McDonald's mobile web locator tool, with small, densely placed, map pinpoints.](https://media.nngroup.com/media/editor/2019/04/10/mcdonalds_mobileweb_maptargets.png)

*McDonalds’ mobile site: The locator search-results page presented a map with markers too small and close together. Information about a location was displayed by tapping the corresponding pinpoint. Thankfully, a list view of locations was also available (which ideally should have been the default view).*

Lists of links and stacked buttons also often fall victim to touch-target errors because the spacing between the elements is too small. For example, the stacked thin buttons on the mobile homepage of Kate Spade were too close to each other. More space between them would prevent users from tapping the wrong one. In contrast, the links on the White House Black Market mobile homepage were far enough apart to tap accurately. (Another solution would be to move paired targets to be side-by-side rather than stacked, as the extra width gives more room for error compared with the short line height.)

![Screenshots comparing link placement on Kate Spade's and White House Black Market's mobile homepages.](https://media.nngroup.com/media/editor/2019/04/10/densetargets-katespade_whitehouseblackmarket.png)

*(Left) The links to* Shop Best Selling Gifts *and* Shop the Gift Guide *on Kate Spade’s mobile homepage were too tightly stacked to be accurately tapped. (Right) In comparison, the spacing between the* Shop New Arrivals *and* Find a Boutique *links on the White House Black Market mobile homepage was large enough to support accurate selection of each link.*

Of course, if the targets are too small, adding space between them is likely not going to help. **To avoid accidental taps, targets must first be big enough, and then also spaced well enough**. For example, on Instagram, the buttons to dismiss a follow suggestion were too small (only 2mm — 0.08in — wide), so even though they are far enough from the *Follow* buttons (about 2mm of spacing — the often-recommended minimum), they are still hard to select. Because of this design, it’s easier to simply ignore any bad suggestions rather than risk accidentally following an account when attempting to remove it from the list.

![Screenshot of the Follow page in the Instagram app.](https://media.nngroup.com/media/editor/2019/04/10/instagram_suggestedtofollow_taptargets.jpg)

*Instagram for iOS: The* x *dismiss buttons to the right of the* Follow *buttons are too small, and the small amount of spacing between these opposed actions is not enough to make up for their small size.*

Had the touch target for dismissing a suggestion been wider, the amount of space between the opposing actions would have been sufficient. Although there is plenty of vertical space, the extra width would allow users to tap near the farther edge to avoid potential mistaps.

## View–Tap Asymmetry

Touch targets need to be large enough to (1) discern what the target is, and (2) to accurately acquire them. View–tap asymmetry occurs when **elements are large enough to be seen (e.g., read the label text), but too small or densely packed to select** without struggling. This was a major problem with many designs in our [early studies of the iPad](https://www.nngroup.com/articles/ipad-usability-year-one/). A current common example of view–tap asymmetry is the tiny [iOS-style carousel dot indicators](https://www.nngroup.com/articles/4-ios-rules-break/): you can (sometimes) see that the dots are present, but they are far too small to tap individually to navigate.

View–tap asymmetry is often caused by desktop designs that were not well-adapted for touchscreen use. **Elements that are easily clicked using a mouse cursor are not always accessible by fingers.** For example, the David Yurman jewelry website included small circular swatches under each product photo on product-listing pages, to indicate alternate colors available for each. Clicking each swatch would update the product photo on the page, so users could preview the color without navigating to the detail page. While this design worked well for mouse-based interactions, the small swatches were far too small (only 1mm or 0.04 inches) for tablet users — attempts to tap a color swatch often activated the link to the product-detail page instead. Perhaps they were left visible just so users could see that other colors were available, but the carousel controls to cycle through even more color options were also small-sized and untappable.

![Screenshot of a product-listing page on the David Yurman jewelry website, on a tablet.](https://media.nngroup.com/media/editor/2019/04/10/davidyurman_tab_plp_colorswatchtouchtargets.jpg)

*DavidYurman.com: Alternate color options on product-listing pages were only 1mm (0.04 in) diameter, and thus too small to tap on a touchscreen (here, seen on a tablet).*

## When Bigger Is Better

Of course, 1cm (0.4in) is merely the minimum size for a tap target, and there are many cases where an interactive element should be even larger. For example, **primary calls to action** often deserve great visual prominence and thus deserve a larger tap target.

The **context of use** may also demand tap targets larger than 1cm x 1cm: if an app (or mobile site) is to be used when the user is moving, targets will be harder to hit and thus should be bigger to allow for more room for error. When driving or walking, controls requiring precise manipulation will be difficult, if not impossible to use.

For instance, the Target app prioritized two main features for users who are in a physical store: searching for a product and scanning a product’s barcode to look for a coupon or other product details. These buttons are visibly placed at the top of the page and occupy an area of approximately 2cm × 2cm (0.8in × 0.8in). This design takes into account the fact that many users may be using the app while walking around the store, searching for the aisle which contains a desired item or whether there is a coupon available for a given product.

![Screenshot of the landing screen of the Target mobile app, showing 2 oversized primary tap targets.](https://media.nngroup.com/media/editor/2019/04/10/target_mobileapp_largeprimarybuttons.jpg)

*Buttons to search or scan a barcode for a product on the Target app are oversized (2cm × 2cm, or 0.8in × 0.8in), both to communicate that they are commonly used, primary functions as well as to allow users shopping in the physical stores to easily tap these buttons while in motion.*

**Audience needs** can also be a reason for bigger tap targets. Young [children require large, easy-to-reach controls](https://www.nngroup.com/articles/children-ux-physical-development/) because their physical skills are not as developed as those of adults. Conversely, seniors, whose dexterity has begun to decline, will also benefit from larger controls that are more forgiving of shaky hands. And in my case, new parents need large targets with generous margins of error to support the inevitable juggling act that is now our life.

Limiting the number of elements on the screen can allow key touch targets to be larger and further spaced apart, and thus easier to tap. For instance, the Glow Baby app timer to track how long a baby is nursing dedicated most of the screen to the two touch targets corresponding to the nursing timers (each target measured to 2.3cm, or 0.9in, wide on an iPhone X), with ample white space between them and other, secondary, targets. A large *Finish* button only appeared once a timer had been started, and the *Begin Time* field was then set automatically. All the targets on the screen are fairly far apart from each other to avoid mistaps.

![2 screenshots from the Glow Baby app, showing multiple stages of using the nursing timer function.](https://media.nngroup.com/media/editor/2019/04/10/glowbaby_mobileapp_nursingtimer.png)

*Glow Baby: The touch targets for the nursing timers are oversized and far from other elements on the screen to facilitate easy tapping while users literally have their hands full.*

The **size of the screen** can also influence the size of the touch targets*.* [Very large touchscreens often require larger targets](https://www.nngroup.com/articles/very-large-touchscreen-ux-design/) to be noticeable and to minimize the time to reach them. On the other hand, small touchscreens, such as [smartwatches](https://www.nngroup.com/articles/smartwatch/), shouldn’t just have smaller touch targets — instead consider gestures or voice control as means of interaction.

## Conclusion

Designing usable touch targets is the basis of all touchscreen (and therefore mobile) design. Ensure that all interactive elements are at least 1cm × 1cm (0.4in × 0.4in) in physical, rendered size and positioned with enough space from other competing touch targets to be easily and accurately acquired. Too small targets lead to longer acquisition times and errors, and are bound to cause user frustration.

### References

Parhi, P., Karlson, A. K., and Bederson, B. B. 2006. “Target size study for one- handed thumb use on small touchscreen devices.” In *Proceedings of the 8th Conference on Human-Computer interaction with Mobile Devices and Services*. MobileHCI ‘06. DOI= <http://doi.acm.org/10.1145/1152215.1152260>

Dandekar K., Raju B.I., Srinivasan M.A. (2003). 3-D finite-element models of human and monkey fingertips to investigate the mechanics of tactile sense. *Journal of Biomechanical Engineering*, 125, 682–691. DOI= [10.1115/1.1613673](http://dx.doi.org/10.1115/1.1613673)

## Related Courses

- [#### Mobile User Experience

  Essential UX design principles for small-screen websites and apps

  Interaction](/courses/usability-mobile-websites-apps/?lm=touch-target-size&pt=article)

touch targets,direct manipulation,ios,Mobile & Tablet,mobile navigation,gestures,Interaction Design,ui elements,graphical user interfaces

## Related Topics

- Mobile & Tablet
  [Mobile & Tablet](/topic/mobile-and-tablet-design/)
- [Interaction Design](/topic/interaction-design/)

## Learn More:

- [![](https://media.nngroup.com/media/videos/thumbnails/Teslers_Law-_Shift_Complexity_to_Simplify_UX_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Tesler’s Law: Shift Complexity to Simplify UX

  Lola Famulegun
  ·
  3 min](/videos/teslers-law/?lm=touch-target-size&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Overflow_Menu_Icons_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Overflow Menu Icons

  Kate Kaplan
  ·
  4 min](/videos/overflow-menu-icons/?lm=touch-target-size&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/GenUI_Ai-Generated_Interfaces_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  GenUI: AI-Generated Interfaces

  Kate Moran and Sarah Gibbons
  ·
  4 min](/videos/genui-ai-generated-interfaces/?lm=touch-target-size&pt=article)

## Related Articles:

- [iPhone X: The Rise of Gestures

  Raluca Budiu
  ·
  12 min](/articles/iphone-x/?lm=touch-target-size&pt=article)
- [Slider Design: Rules of Thumb

  Aurora Harley
  ·
  4 min](/articles/gui-slider-controls/?lm=touch-target-size&pt=article)
- [The Apple Watch: User-Experience Appraisal

  Raluca Budiu
  ·
  11 min](/articles/smartwatch/?lm=touch-target-size&pt=article)
- [Shopping Cart or Wishlist? Saving Products for Later in Ecommerce

  Page Laubheimer
  ·
  5 min](/articles/wishlist-or-cart/?lm=touch-target-size&pt=article)
- [Distracted Driving: UX’s Responsibility to Do No Harm

  Page Laubheimer
  ·
  9 min](/articles/distracted-driving-ux/?lm=touch-target-size&pt=article)
- [Banner Blindness Revisited: Users Dodge Ads on Mobile and Desktop

  Kara Pernice
  ·
  9 min](/articles/banner-blindness-old-and-new-findings/?lm=touch-target-size&pt=article)