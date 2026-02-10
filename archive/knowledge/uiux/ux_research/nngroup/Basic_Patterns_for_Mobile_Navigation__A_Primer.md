# Basic Patterns for Mobile Navigation: A Primer

Source: https://www.nngroup.com/articles/mobile-navigation-patterns/

---

6

# Basic Patterns for Mobile Navigation: A Primer

Raluca Budiu

![](https://media.nngroup.com/media/people/photos/2023-04-portraits-raluca.jpg.256x256_q75_autocrop_crop-smart_upscale.jpg)

[Raluca Budiu](/articles/author/raluca-budiu/)

November 15, 2015
2015-11-15

[Share](#)

- [Email article](mailto:?subject=NN/g Article: Basic Patterns for Mobile Navigation: A Primer&body=https://www.nngroup.com/articles/mobile-navigation-patterns/)
- [Share on LinkedIn](http://www.linkedin.com/shareArticle?mini=true&url=http://www.nngroup.com/articles/mobile-navigation-patterns/&title=Basic Patterns for Mobile Navigation: A Primer&source=Nielsen%20Norman%20Group)
- [Share on Twitter](https://twitter.com/intent/tweet?url=http://www.nngroup.com/articles/mobile-navigation-patterns/&text=Basic Patterns for Mobile Navigation: A Primer&via=nngroup)

Summary: 
Mobile navigation must be discoverable, accessible, and take little screen space. Exposing the navigation and hiding it in a hamburger both have pros and cons, and different types of sites have different preferred solutions to the mobile-navigation quandary.

## In This Article:

- [Introduction](#toc-introduction-1)
- [The Navigation Bar and the Tab Bar](#toc-the-navigation-bar-and-the-tab-bar-2)
- [The Hamburger Menu (and Variants)](#toc-the-hamburger-menu-and-variants-3)
- [The Navigation Hub](#toc-the-navigation-hub-4)
- [Conclusion](#toc-conclusion-5)

## Introduction

**[Navigation complements search](http://www.nngroup.com/articles/search-not-enough/)** for several reasons:

- sometimes users don’t know what to search for, and need help figuring out the partitioning of the search space;
- coming up with a good query and typing it requires more mental effort and higher [**interaction cost**](http://www.nngroup.com/articles/interaction-cost-definition/) than [**recognizing**](http://www.nngroup.com/articles/recognition-and-recall/) and tapping a navigation link (and, in fact, [**users are notoriously bad at formulating good queries**](http://www.nngroup.com/articles/incompetent-search-skills/));
- site search often works a lot more poorly than the search-engines users expect it to.

However, on mobile devices, both navigation and search come at a price: they occupy screen space and grab users’ attention, both of which are at an even higher premium on mobile than on desktop. If the screen space is really scarce, a search box or navigation links at the top of the page can interfere with the users’ ability to get to new information fast and may make the user work more. Pay attention to navigation and search, make them accessible and discoverable, but don’t forget one of the basic tenets of [**mobile usability**](http://www.nngroup.com/articles/mobile-ux/): prioritize content over [**chrome**](http://www.nngroup.com/articles/browser-and-gui-chrome/). This is in fact one of the big challenges of implementing navigation on mobile: **how to prioritize content while making navigation accessible and discoverable.** Different approaches sacrifice either content prioritization or the accessibility of the navigation.

## The Navigation Bar and the Tab Bar

### Top Navigation Bar

**The top navigation bar** is essentially inherited from desktop design. It is simply a bar that enumerates the main navigational options across the top of the screen. This is quite efficient, but has two disadvantages: (1) it works well only when there are relatively few navigation options; (2) it takes up valuable [**real estate above the fold**](http://www.nngroup.com/articles/page-fold-manifesto/).

![Washington Post homepage and Google Play Apps Page](//s3.amazonaws.com/media.nngroup.com/media/editor/2015/09/22/nav-bar.png)

*The BBC’s website (left) and Google Play for Android (right) both used a top navigation bar for the main navigation. Google Play was able to fit more items in the navigation bar by using a carousel.*

### The Tab Bar

**The tab bar** is a close relative of the top navigation bar specific to apps. It can appear at the top (Android mostly) or at the bottom of the page (iOS mostly). It is usually present on most pages within an app and has the same disadvantages as the navigation bar. One important difference between tab bars and navigation bars is that tab bars are **persistent,** that is, they are always visible on the screen, whether the user scrolls down the page or not. Navigation bars usually start out being present at the top of the page but disappear once the user has scrolled one or more screens down. (A **sticky version of the navigation** bar stays put at the top of the screen, or as the user starts scrolling up, reappears at the top of the page.)

![Facebook newsfeed on iOS and Android](//s3.amazonaws.com/media.nngroup.com/media/editor/2015/09/22/facebook.png)

*Facebook on iPhone (left) and Android (right) used a tab bar for the main navigation options. The tab was positioned in accordance with official operating-systems guidelines: at the bottom on iPhone and at the top of the page on Android. Note that the icons are labeled on the left screenshot: a recommended best practice in most cases.*

**Tab bars and navigation bars are well suited for sites with relatively few navigation options.** If your site has more than 5 options, it’s hard to fit them in a tab or navigation bar and still keep an optimum [touch-target size](https://www.nngroup.com/articles/touch-target-size/). Solutions such as using a [**carousel**](http://www.nngroup.com/articles/designing-effective-carousels/) navigation bar or tab bar, like in the Google Play example at the beginning of the article, may work but they are not always appropriate. Out of sight is out of mind, and if the categories are widely different (like the case of an older version of Weather Channel illustrated below), it’s likely that users won’t think to scroll to get to those options, simply because the weak information scent from the visible categories may prevent them from guessing what items are hidden.

![Old version of Weather Channel](//s3.amazonaws.com/media.nngroup.com/media/editor/2015/09/22/weather1.png)

*An older version of Weather Channel for Android had a carousel tab bar at the bottom of the screen; the categories in the carousel were not similar or predictable, and thus the ones that were not visible had little discoverability.*

**If you decide to use a navigation bar or a tab bar, they should be the main chrome area of the screen and little extra space should be devoted to other** [**utility-navigation**](http://www.nngroup.com/articles/utility-navigation) **options or to search.** If the site has 4–5 main navigation options, it may make sense to have them all visible on the screen at all times, especially if these are options that will likely be needed. However, keep in mind that navigation needs to be judged in the context of the overall chrome on a page: even if a site may only have a few top-tier categories, if other utility-navigation links (e.g., shopping cart, account information) and search must also be included, the overall chrome may add up wasting too much space on the page.

![Autozone search results page for "sparks"](//s3.amazonaws.com/media.nngroup.com/media/editor/2015/09/22/autozone1.png)

*Autozone.com: Although the site only had 4 main-navigation categories (*Shop, Repair Help, Deals*, and* Find Store*), there were a lot more chrome elements present on the page (logo, shopping cart,* My Zone *link, search box) that all occupied too large an area.*

## The Hamburger Menu (and Variants)

**The navigation menu** is a menu that contains the main navigation options in a manner that usually hides the detailed options but makes them visible upon request. While the hamburger icon is perhaps the most talked-about signifier for a navigation menu, other labels and/or [**icons**](http://www.nngroup.com/articles/icon-usability/) can be used for navigation. (In fact, [**third-party research**](http://exisweb.net/menu-eats-hamburger) seems to suggest that using the word *Menu* instead of the hamburger icon is slightly more popular with users.) The main advantage of the navigation menu is that it can contain a fairly large number of navigation options in a tiny space and can also easily support submenus, if needed; the disadvantage is that it is less discoverable, since, as the old adage says, “out of sight is out of mind.”

![USA Today homepage and menu contents](//s3.amazonaws.com/media.nngroup.com/media/editor/2015/09/22/usatoday.png)

*A hamburger menu was used for the global navigation options on USAToday.com.*

A version of the navigation menu is when the menu has no signifier and is discovered through a gesture. In the Sephora app, on deep pages the menu can be accessed by swiping horizontally on the left edge (a gesture that is problematic in iOS, since, from iOS 7 on, Apple has started pushing the horizontal swipe as *Back*).

![Sephora deep page and content of menu](//s3.amazonaws.com/media.nngroup.com/media/editor/2015/09/22/sephora-swipe.png)

*Sephora for iPhone: There was no visible menu button, but a horizontal swipe on the left edge exposed the menu. Most users would never discover this feature and would restrict themselves to using the visible options*.

**The [navigation menu makes the navigation options least discoverable](https://www.nngroup.com/articles/hamburger-menus/) and is best suited for content-heavy, browse-mostly sites and apps.**

If users rarely care about navigating to specific sections of the site and are mostly content to digest whatever information is presented to them (as is often the case on news sites), then a navigation menu is appropriate. The navigation menu also has the advantage of stealing a minimum amount of space from content, which is the star of browse-mostly sites.

However, keep in mind that when navigation is hidden under a menu, even though that menu as a whole may be salient enough, users will have to make a decision to open it and check whether the individual navigation options are relevant. While the navigation menu is becoming standard and many mobile users are familiar with it, many people still simply don’t think to open it. Even users who tried the navigation menu at some point during a session may not remember to do so later on.

If you decide to use a navigation menu, you need to think seriously about [**supporting navigation in other ways**](http://www.nngroup.com/articles/support-mobile-navigation/), such making the IA structure of your site more discoverable by increasing the cross-section links.

## The Navigation Hub

**The navigation hub** is a page (usually the homepage) that lists all the navigation options. To navigate to a new location, users have to first go back to the hub and then use one of the options listed there. This navigation approach usually devotes the homepage exclusively to navigation (at the expense of content), and incurs an extra step (back to the hub) for each use of the navigation. **It can work well in task-based websites and apps, especially when users tend to limit themselves to using only one branch of the navigation hierarchy during a single session.**

With the homepage as navigation hub, prime real estate will be wasted for chrome and all navigation will have to go through the homepage. While these two may seem as major disadvantages (and they are for most types of sites or apps), they can be less of a problem for those sites and apps used not for browsing and consuming content, but for accomplishing a very specific task (for example, checking in for a flight or changing the settings of the phone). Such sites and apps can take advantage of the homepage-as-navigation-hub pattern, especially if users rarely accomplish more than one task during a single session, and thus they don’t need to traverse the navigation tree often (an action that is relatively difficult and annoying if all navigation must go through the homepage).

![United homepage and flight-search page](//s3.amazonaws.com/media.nngroup.com/media/editor/2015/09/22/united.png)

*United used the homepage as a navigation hub. On deep pages, users had to use the on-page* Home *button to go back to the homepage if they wanted to select a different navigation option.*

In the United example above, most likely you want to *either* buy a ticket *or* check in for a flight, but not do both in a single session. Thus, most users won’t have to return to the hub in this example, meaning that it rather serves as an efficient distribution point.

## Conclusion

Making navigation important and accessible is a challenge on mobile due to the limitations of the small screen and to the need of prioritizing the content over the UI elements. Different basic navigation patterns attempt to solve this challenge in different ways that all suffer from a variety of usability problems. The key is to pick the type of mobile navigation where the (inevitable) downsides will hurt your users the least for the kinds of tasks they are most likely to perform on your site:

- Hamburger menus accommodate a large number of options, but these options are less discoverable. They are particularly well suited for browse-mostly sites.
- Navigation bars and tab bars take space on the page, and work well when the number of navigation options is small.
- Sites that are primarily task oriented can use a homepage-as-navigation-hub pattern.

## Related Courses

- [#### Mobile User Experience

  Essential UX design principles for small-screen websites and apps

  Interaction](/courses/usability-mobile-websites-apps/?lm=mobile-navigation-patterns&pt=article)

mobile navigation,Mobile & Tablet,Navigation,Design Patterns

## Related Topics

- Mobile & Tablet
  [Mobile & Tablet](/topic/mobile-and-tablet-design/)
- [Navigation](/topic/navigation/)
- [Design Patterns](/topic/design-patterns/)

## Learn More:

- [![](https://media.nngroup.com/media/videos/thumbnails/Button_States_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Button States 101

  Kelley Gordon
  ·
  3 min](/videos/button-states-101/?lm=mobile-navigation-patterns&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/2-Factor_Authentication_2-FA_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  2-Factor Authentication (2-FA)

  Tim Neusesser
  ·
  4 min](/videos/2-factor-authentication/?lm=mobile-navigation-patterns&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Card_View_vs_List_View_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Card View vs. List View

  Megan Chan
  ·
  5 min](/videos/card-view-vs-list-view/?lm=mobile-navigation-patterns&pt=article)

## Related Articles:

- [List Thumbnails on Mobile: When to Use Them and Where to Place Them

  Aurora Harley
  ·
  4 min](/articles/mobile-list-thumbnail/?lm=mobile-navigation-patterns&pt=article)
- [Supporting Mobile Navigation in Spite of a Hamburger Menu

  Amy Schade
  ·
  4 min](/articles/support-mobile-navigation/?lm=mobile-navigation-patterns&pt=article)
- [Mobile Login Methods Help Chinese Users Avoid Password Roadblocks

  Xinyi Chen and Yuxuan (Tammy) Zhou
  ·
  10 min](/articles/mobile-login-china/?lm=mobile-navigation-patterns&pt=article)
- [Reading Content on Mobile Devices

  Kate Moran
  ·
  8 min](/articles/mobile-content/?lm=mobile-navigation-patterns&pt=article)
- [Visual Indicators to Differentiate Items in a List

  Aurora Harley
  ·
  6 min](/articles/visual-indicators-differentiators/?lm=mobile-navigation-patterns&pt=article)
- [Mobile User Behavior in India

  Samyukta Sherugar and Raluca Budiu
  ·
  10 min](/articles/mobile-behavior-india/?lm=mobile-navigation-patterns&pt=article)