# Mobile First Is NOT Mobile Only

Source: https://www.nngroup.com/articles/mobile-first-not-mobile-only/

---

9

# Mobile First Is NOT Mobile Only

Raluca Budiu, Kara Pernice

![](https://media.nngroup.com/media/people/photos/2023-04-portraits-raluca.jpg.256x256_q75_autocrop_crop-smart_upscale.jpg)
![](https://media.nngroup.com/media/people/photos/kara-2025.jpg.256x256_q75_autocrop_crop-smart_upscale.jpg)

[Raluca Budiu](/articles/author/raluca-budiu/) and
[Kara Pernice](/articles/author/kara-pernice/)

July 24, 2016
2016-07-24

[Share](#)

- [Email article](mailto:?subject=NN/g Article: Mobile First Is NOT Mobile Only &body=https://www.nngroup.com/articles/mobile-first-not-mobile-only/)
- [Share on LinkedIn](http://www.linkedin.com/shareArticle?mini=true&url=http://www.nngroup.com/articles/mobile-first-not-mobile-only/&title=Mobile First Is NOT Mobile Only &source=Nielsen%20Norman%20Group)
- [Share on Twitter](https://twitter.com/intent/tweet?url=http://www.nngroup.com/articles/mobile-first-not-mobile-only/&text=Mobile First Is NOT Mobile Only &via=nngroup)

Summary: 
Mobile-navigation patterns make navigation unusable on the desktop and decrease the use of this important UI element. Porting an unchanged UI to a different platform hurts UX.

In a [recent study](https://www.nngroup.com/articles/hamburger-menus/), we found that hiding navigation under a menu significantly decreases the use of the navigation and also degrades the overall user experience both on desktop and on mobile.

While hiding navigation under an expandable menu can be a necessity on a small mobile device, it is not a practice that is native to the desktop; rather, it is a trend inspired by mobile and reinforced by [responsive design](https://www.nngroup.com/articles/responsive-web-design-definition/), a technology that allows the same content and functionality to be present on different screen sizes, but rearranged in layouts that are appropriate to the available screen spaces. Many responsive sites use a mobile-first approach to designing for multiple devices: they start with a design that is optimized for mobile and then port it to the desktop, under the assumption that simple is better across all devices, and a design that is simple and condensed enough so that it works for small screens will also provide a good user experience on large ones.

In this article we examine the consequences of porting mobile-first designs to the desktop, with a focus on navigation.

## In This Article:

- [About Our Study](#toc-about-our-study-1)
- [Navigation Usage: More on Mobile than on Desktop?](#toc-navigation-usage-more-on-mobile-than-on-desktop-2)
- [Design Patterns Borrowed from Mobile](#toc-design-patterns-borrowed-from-mobile-3)
- [Optimize for Each Device](#toc-optimize-for-each-device-4)
- [Porting User Interfaces Creates Terrible User Experience](#toc-porting-user-interfaces-creates-terrible-user-experience-5)

## About Our Study

NN/g partnered with international remote-usability-testing firm, [WhatUsersDo](http://whatusersdo.com/?utm_campaign=nng_hamburger_sidebar&utm_medium=referral&utm_source=ext_article), to test 3 different types of navigation: hidden, visible, and a combination of hidden and visible navigation. As described in the [study methodology](https://www.nngroup.com/articles/hidden-navigation-methodology/), 179 users participated in our study; they completed tasks on 6 different websites, on desktops and smartphones:

- 7digital (music, e-commerce)
- BBC (news)
- Bloomberg Business (business news)
- Business Insider UK (business news)
- Supermarket HQ (e-commerce)
- Slate (news)

For each site, we designed two types of tasks that involved finding specific content:

1. **A navigation-optional task,** which could be accomplished without using the navigation or search on the site, by simply selecting an item on the homepage
2. **A navigation-required task,** which could only be accomplished through the use of navigation (or search — so even these tasks could be done without navigation)

All the sites in our study were responsive, with the exception of Business Insider UK. By looking at the patterns that all of these sites employed, whether responsive or not, (e.g., the use of hidden navigation, repeating the navigation at the bottom of the page, using a search icon instead of a search box), we also surmise that most if not all of these sites were designed using mobile-first principles.

As discussed in our other articles, we collected several metrics; here, we focus on one of them: navigation use. This measure captured whether participants clicked on the navigation options during their tasks.

## Navigation Usage: More on Mobile than on Desktop?

When we look at the differences between mobile and desktop navigation use, it is highly surprising that, on the sites that we included in our study, the **[navigation was used a lot more on mobile](https://www.nngroup.com/articles/find-navigation-mobile-even-hamburger) [than on desktop](https://www.nngroup.com/articles/find-navigation-desktop-not-hamburger/)**. (This difference was statistically significant with a paired t-test, p <0.05.) Not only that, but comparing the navigation use on each site, on 5 out of the 6 sites, the navigation was used significantly more on mobile than on the desktop. (These differences were significant by N-1 2 proportion tests.) The exception was 7Digital, where we also recorded more navigation use on mobile but the difference was not statistically significant, and thus may just have been random.

![](https://media.nngroup.com/media/editor/2016/07/11/navuse.PNG)

*Navigation usage was higher on the mobile versions of the sites than on the desktop versions of the sites.*

This result is unexpected for several reasons:

- Making navigation **easy to access** is a notoriously hard task on mobile. Mobile pages are long and often as soon as users scroll down the first screenful, navigation placed at the top of the page is no longer visible. If they want to access it, they have to scroll back. (Sticky navigation or back-to-top buttons are sometimes used to alleviate this problem, but they often get ignored by users.)
- Making navigation **discoverable** is also notoriously difficult on mobile. Lucky sites that only have 4–5 options in their main navigation can afford to make these options visible at the top of the screen, but the majority of sites must hide at least some of the navigation under an expandable menu. Because these menus hide a wide variety of items, by necessity, they have vague labels such as *Menu* or *Browse* with low [information scent](https://www.nngroup.com/articles/information-scent/). Users must actively think about turning to them as a problem-solving strategy when they are in trouble; they are not [primed](https://www.nngroup.com/articles/priming/) by a label that resembles the content that they are looking for. As a result, people often ignore these menus, and sometimes they forget about them even after they’ve used them once within the same session.

So how is it possible that on this platform with hard-to-use navigation, the navigation is still used a lot more than on the desktop? Did the mobile sites in our sample have exceptionally good navigation designs? If you look at the individual sites, you’ll see that they were not much different from the many navigation implementations on countless other mobile sites: either the much reviled hamburger menu or an homologue, plus, in some cases, a number of visible navigation links.

No. The proper way of describing our findings is not that these sites had discovered the secret of [mobile navigation](https://www.nngroup.com/articles/mobile-navigation-patterns/) or that there was more navigation on mobile (in fact, the overall navigation usage on mobile was only a modest 63%), but, rather, that there was **less navigation on the desktop**. While these two statements are logically the same, the twist in perspective allocates the guilt where it belongs: to the desktop user interfaces, which were not up to the demands of this platform.

And why were the desktop designs worse? Because they were ported from a different platform — mobile. In other words, all of these sites were likely built to be mobile-first: they were optimized for mobile, and as a result the desktop user experience suffered significantly.

You can perhaps think of another possible explanation for why the navigation was used more on mobile. Because the mobile screen is too small and shows only a little content at the time, users have to scroll more to get the same amount of content that is displayed on a desktop screen. (That is indeed, a consequence of the fact that the [mobile–user communication channel is narrower in capacity](https://www.nngroup.com/articles/scaling-user-interfaces), and it’s also the reason why [comprehension is poorer on mobile](https://www.nngroup.com/articles/mobile-content-is-twice-as-difficult/)). So maybe mobile users got tired of scrolling, so they decided to use navigation instead of fishing around for information on the page. That may be true; however, remember that our study included both navigation-required and navigation-optional tasks. If people were simply tired of scrolling on mobile, you’d expect to see more navigation use on mobile for the navigation-optional tasks that could be accomplished by clicking on a link on the homepage. But there should be no difference between mobile and desktop for the navigation-required tasks, that required the use of navigation to be completed.

But our data says otherwise: we found statistically significant differences for mobile and desktops for each type of tasks, both navigation-dependent and navigation independent. In other words, the reason why people used navigation less on the desktop was *not* that they didn’t need it; even in those situations where they couldn’t accomplish the task without the navigation, they used it in only 54% of the times, compared to 77% on mobile.

![](https://media.nngroup.com/media/editor/2016/07/11/bytask.PNG)

*Navigation usage was higher on mobile irrespective of task type. Navigation-dependent tasks that required the use of navigation to be completed had an overall higher rate of navigation use. However, the navigation usage was still higher on mobile than on desktop even for these tasks.*

## Design Patterns Borrowed from Mobile

Which were some of the more important mobile-design patterns that the sites in our study borrowed for the desktop?

**Hidden navigation**. Perhaps the expandable navigation menu (such as the hamburger menu) was the biggest offender and certainly the mobile-inspired pattern most relevant to our study. We’ve seen from many qualitative studies that [it doesn’t work on the desktop](https://www.nngroup.com/articles/killing-global-navigation-one-trend-avoid/), but sites still insist on using it.

**Repeated navigation at the bottom of the screen.** One of the sites (7Digital) in our study has an expandable navigation menu at the top of the page and also repeats the navigation options at the bottom of the screen. This practice is often used on mobile to prevent users from having to scroll back to the top of the page to access the navigation positioned there.

**Sticky navigation at the top of the page.** Some desktop sites (e.g., Bloomberg, Business Insider UK) chose to make the navigation sticky: that is, it remained present at the top of the page as users scrolled down or when they started to scroll up.

**Navigation in the top right corner.** One of the desktop sites (Slate) placed the navigation in a highly nonstandard position for the desktop: the top right corner. This placement for the hamburger menu is a lot more common on mobile (where, in apps, the top left corner is often reserved for the *Back* button).

**Search icon instead of search box.** Many of the sites also got rid of the search box on the desktop and preferred to use a search icon instead. We generally [recommend against this practice on the desktop](https://www.nngroup.com/articles/magnifying-glass-icon/); we’ve heard countless users complaining about having to locate a tiny icon on a large screen.

![](https://media.nngroup.com/media/editor/2016/07/11/slate-better-res.png)

*Slate desktop (left) and mobile (right): the desktop site used a hamburger menu at the top of the right rail, in the top right corner of the page, a position highly nonstandard for desktop but fairly common on mobile. It also displayed a search icon instead of the traditional search box that people expect on the desktop.*

![](https://media.nngroup.com/media/editor/2016/07/11/bbc.png)

*BBC desktop (left) and mobile (right): The desktop site used a navigation bar with a* More *tab — similar with the* More *tab used to fit extra tabs in the iOS tab bar.*

![](https://media.nngroup.com/media/editor/2016/07/11/businessins.png)

*Business Insider desktop (left) and mobile (right): The desktop site used a hamburger menu for the desktop global navigation. The top blue bar was sticky: it stayed at the top of the page as the user scrolled down. Other mobile-inspired featured were the image-based, information-depleted layout and the search icon instead of a search box.*

None of these patterns are either common or particularly usable or useful on desktop, yet they often work or are necessary on mobile. These sites found them valuable for their small-screen designs, and thought they should apply them to the desktop. Little did they know that they were throwing the baby out with the bath water: the desktop user experience suffered, and they created unnecessary problems.

## Optimize for Each Device

In our world of many interconnected devices, it is imperative to design for all of them. Agreed, it seems wasteful to have separate designs for every single device. But, different devices have different capabilities of interaction and different screen sizes. The amount of information that can be displayed on each of these devices at a time varies wildly and the same design will have a very different [content-to-chrome ratio](https://www.nngroup.com/articles/content-chrome-ratio) on two different devices. For example, on a small mobile screen, a hamburger icon may be noticeable enough, but if you move the same icon to a large 27” screen, it will easily get lost.

Granted, you could make the hamburger bigger, like in the image below, which shows Slate’s homepage if the hamburger icon were sized to take the same fraction of the desktop screen as it does on an iPhone 6S. But we don’t advise you to use a design like this for several reasons:

1. [Right-aligned logos work worse than left-aligned logos](https://www.nngroup.com/articles/logo-placement-brand-recall/) (but we retained the right-alignment here for the sake of comparison).
2. Icons this huge may still be overlooked due to [banner blindness](https://www.nngroup.com/articles/banner-blindness-old-and-new-findings/).
3. If you do allocate this much space to navigation, you might as well show the links.

![Mockup of desktop homepage, magnifying the navigation icons to take up the same proportion of screen space on a 27-inch desktop monitor as they do on a smartphone screen](https://media.nngroup.com/media/editor/2016/07/11/slate-big-icons-both.png)

*Slate desktop homepage, as tested (left) and with icons resized to take up the same percentage of the screen on a 27-inch monitor as they do on an iPhone 6 screen (right). Since a good 27-inch monitor costs $180, it’s currently a typical purchase for business users.*

We cannot ignore these differences when scaling user interfaces. We must take advantage of individual device strengths in order to produce designs that work across all screen sizes.

## Porting User Interfaces Creates Terrible User Experience

The history of user interface design has many examples of people replying on the shortcut of porting a UI from one platform to another. It never works:

- 1980s: Taking a DOS program and porting it to Windows translates into a miserable user experience, as the resulting software doesn’t integrate GUI direct-manipulation features properly.
- 1990s: Taking a Windows program and porting it to Macintosh results in a substandard user experience, as the application doesn’t feel like a native Mac program. The look-and-feel is simply wrong, and the Apple magazines of the day rightfully savaged such ports in their reviews.
- 2000s: Taking a brochure or other print collateral and making it into a website results in a sluggish user experience, with little use of interactive features and impoverished navigation. Porting print content to online by making it into a [PDF blob](https://www.nngroup.com/articles/pdf-unfit-for-human-consumption/) is even worse.
- Late 2000s: Taking a website optimized for desktop use and offering it to mobile users results in an almost unusable user experience, as people get lost in overly elaborate menus and content that doesn’t fit the small screen.
- 2010: Taking a magazine designed for paper and [porting it to the iPad](https://www.nngroup.com/articles/ipad-usability-first-findings/) results in a dreadful user experience, with users stuck into a nonhyperlinked world and crushed by the print metaphor.
- Late 2010s: Taking a website optimized for mobile use and offering it to desktop users results in a degraded user experience, as we have seen in this article.
- 2020? Taking a mobile app and cramming it onto a [watch will also be terrible](https://www.nngroup.com/articles/smartwatch/). Let’s hope that history won’t repeat itself, though it surely will.

Tempting as it may be to design once and use twice, it can result in a subpar user experience for one of the platforms, and maybe for both of them. Providing content and feature parity across devices is a great goal, but it doesn’t mean that all the UI elements and the design must also stay exactly the same. Each UI platform has different capabilities leading to different design requirements for an optimized user experience. Serving users on multiple platforms requires a multiplatform design strategy.

### Other Articles Related to the NN/g Hidden-Navigation Study

[Hamburger Menus and Hidden Navigation Hurt UX Metrics](https://www.nngroup.com/articles/hamburger-menus/)

[Hidden- and Visible-Navigation Study: Methodology](https://www.nngroup.com/articles/hidden-navigation-methodology/)

[How to Make Navigation (Even Hamburger) Discoverable on Mobile](http://www.nngroup.com/articles/find-navigation-mobile-even-hamburger/)

[Beyond the Hamburger: How to Make Navigation Discoverable on Desktops](http://www.nngroup.com/articles/find-navigation-desktop-not-hamburger/)

Learn more about scaling user interfaces across different devices in our full-day [course](https://www.nngroup.com/courses/scaling-responsive-design/).

## Related Courses

- [#### Mobile User Experience

  Essential UX design principles for small-screen websites and apps

  Interaction](/courses/usability-mobile-websites-apps/?lm=mobile-first-not-mobile-only&pt=article)
- [#### Web Page UX Design

  Strategically combine content, visuals, and interactive components to design successful web pages

  Interaction](/courses/web-page-design/?lm=mobile-first-not-mobile-only&pt=article)
- [#### The Human Mind and Usability

  Use psychology to predict and explain how your customers think and act

  Interaction](/courses/human-mind/?lm=mobile-first-not-mobile-only&pt=article)

hamburger,mobile navigation,Mobile & Tablet,Navigation,Web Usability

## Related Topics

- Mobile & Tablet
  [Mobile & Tablet](/topic/mobile-and-tablet-design/)
- [Navigation](/topic/navigation/)
- [Web Usability](/topic/web-usability/)

## Learn More:

- [![](https://media.nngroup.com/media/videos/thumbnails/Grids_101_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Grids 101

  Kelley Gordon
  ·
  4 min](/videos/grids-101/?lm=mobile-first-not-mobile-only&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Hamburger_Menu_Icon_Update_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Hamburger Menu Icon Update

  Kate Kaplan
  ·
  3 min](/videos/hamburger-menu-icon-update/?lm=mobile-first-not-mobile-only&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/2-Factor_Authentication_2-FA_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  2-Factor Authentication (2-FA)

  Tim Neusesser
  ·
  4 min](/videos/2-factor-authentication/?lm=mobile-first-not-mobile-only&pt=article)

## Related Articles:

- [Hamburger Menus and Hidden Navigation Hurt UX Metrics

  Kara Pernice and Raluca Budiu
  ·
  12 min](/articles/hamburger-menus/?lm=mobile-first-not-mobile-only&pt=article)
- [Supporting Mobile Navigation in Spite of a Hamburger Menu

  Amy Schade
  ·
  4 min](/articles/support-mobile-navigation/?lm=mobile-first-not-mobile-only&pt=article)
- [List Thumbnails on Mobile: When to Use Them and Where to Place Them

  Aurora Harley
  ·
  4 min](/articles/mobile-list-thumbnail/?lm=mobile-first-not-mobile-only&pt=article)
- [Basic Patterns for Mobile Navigation: A Primer

  Raluca Budiu
  ·
  7 min](/articles/mobile-navigation-patterns/?lm=mobile-first-not-mobile-only&pt=article)
- [Don’t Use Split Buttons for Navigation Menus

  Raluca Budiu
  ·
  9 min](/articles/split-buttons-navigation/?lm=mobile-first-not-mobile-only&pt=article)
- [Visual Indicators to Differentiate Items in a List

  Aurora Harley
  ·
  6 min](/articles/visual-indicators-differentiators/?lm=mobile-first-not-mobile-only&pt=article)