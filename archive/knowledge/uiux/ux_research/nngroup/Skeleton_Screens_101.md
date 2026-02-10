# Skeleton Screens 101

Source: https://www.nngroup.com/articles/skeleton-screens/

---

5

# Skeleton Screens 101

Samhita Tankala

![](https://media.nngroup.com/media/people/photos/Samhita-portrait-2022-06.jpg.256x256_q75_autocrop_crop-smart_upscale.jpg)

[Samhita Tankala](/articles/author/samhita-tankala/)

June 4, 2023
2023-06-04

[Share](#)

- [Email article](mailto:?subject=NN/g Article: Skeleton Screens 101&body=https://www.nngroup.com/articles/skeleton-screens/)
- [Share on LinkedIn](http://www.linkedin.com/shareArticle?mini=true&url=http://www.nngroup.com/articles/skeleton-screens/&title=Skeleton Screens 101&source=Nielsen%20Norman%20Group)
- [Share on Twitter](https://twitter.com/intent/tweet?url=http://www.nngroup.com/articles/skeleton-screens/&text=Skeleton Screens 101&via=nngroup)

Summary: 
A skeleton screen is used as a placeholder while users wait for a page to load. This progress indicator is used for full page loads and reduces the perception of a long loading time by providing clues for how the page will ultimately look.

A skeleton screen is a design pattern used to indicate that a page is loading while providing users with a [wireframe](https://www.nngroup.com/articles/draw-wireframe-even-if-you-cant-draw/)-like visual that mimics the layout of the page. This specific type of [progress indicator](https://www.nngroup.com/articles/progress-indicators/) is used exclusively for full-page loads.

![LinkedIn uses a skeleton screen to indicate that the page is loading and to give users a sense of how the page will be structured. ](https://media.nngroup.com/media/editor/2023/05/18/linkedin_skeletonscreen.jpg)

*LinkedIn uses a skeleton screen to indicate that the page is loading and to give users a sense of how the page will be structured.*

## In This Article:

- [What Are the Different Types of Skeleton Screens?](#toc-what-are-the-different-types-of-skeleton-screens-1)
- [Static-Content and -Image Skeleton Screens](#toc-static-content-and-image-skeleton-screens-2)
- [Animated Skeleton Screens](#toc-animated-skeleton-screens-3)
- [Frame-Display Skeleton Screens](#toc-frame-display-skeleton-screens-4)
- [Benefits of Using Skeleton Screens](#toc-benefits-of-using-skeleton-screens-5)
- [Are Skeleton Screens Better than Progress Bars or Spinners?](#toc-are-skeleton-screens-better-than-progress-bars-or-spinners-6)
- [Conclusion](#toc-conclusion-7)
- [References](#toc-references-8)

## What Are the Different Types of Skeleton Screens?

There are 3 main types of skeleton screens:

- Static-content and -image skeleton screens
- Animated skeleton screens
- Frame-display skeleton screens

## Static-Content and -Image Skeleton Screens

These are the most common skeleton screens and look like wireframes, in which the light gray boxes represent [content](https://www.nngroup.com/articles/content-strategy/) and images. The structure of the gray boxes mimics the structure of the final page with content. The skeleton screen helps users build a [mental model](https://www.nngroup.com/articles/mental-models/) of what will be on the page and even gives some clues as to the underlying information hierarchy.

![](https://media.nngroup.com/media/editor/2023/05/18/headspace_skeletonscreenfull.png)

*Headspace uses a skeleton screen to build users’ expectations for the structure of the page. This skeleton screen relies on design conventions, with large gray boxes representing images and long rectangle boxes representing text. The thickest gray line at the top (1) implies a page title, with a smaller secondary line underneath that would be descriptive text (2); below that, the page is structured into a sequence map (3) with a card at each step.  In each card there will be a title (4), a bit of accompanying text (5), and an image (6). On the right you can see what the fully loaded page actually looks like.*

## Animated Skeleton Screens

Some skeleton screens include [animations](https://www.nngroup.com/articles/animation-duration/) in the form of a pulsating movement, with the use of gradients or elements fading in and out. These are similar to wait animations (or spinners) and signify that the system is still working and still loading content, decreasing users’ perception of a long loading time by keeping users engaged on the content being loaded.

Note that animations of this sort can potentially be [distracting](https://www.nngroup.com/videos/distracting-animations/), annoying, or even create [accessibility problems](https://www.nngroup.com/articles/animation-purpose-ux/) for some users.

[![ ](https://media.nngroup.com/media/editor/2023/05/18/doordash_thumbnail.jpg)](https://media.nngroup.com/media/editor/2023/05/18/doordash_skeletonscreens.mp4)

*DoorDash uses a short, animated skeleton screen in the form of a shimmer that moves from left to right.*

## Frame-Display Skeleton Screens

One variation that we do not recommend is a skeleton screen that displays only the frame of the application without a content wireframe. These minimal skeleton screens only include the header, footer, and the background. This style doesn’t include placeholders of the content, and as a result, doesn’t give users a sense of the general structure of the page. A frame display is not recommended because, if users are forced to wait for too long, they will assume the page isn’t working because the screen is mostly blank.

[![ ](https://media.nngroup.com/media/editor/2023/05/18/nbc_skeletonscreen.jpg)](https://media.nngroup.com/media/editor/2023/05/18/nbc_skeletonscreen.mp4)

*NBC displays only the frame of the page, with a pulsing background gradient used  to communicate that the page is loading. However, this skeleton screen is essentially equivalent to a [spinner](https://www.nngroup.com/articles/progress-indicators/), since it doesn’t include any information about the page structure.*

## Benefits of Using Skeleton Screens

Skeleton screens help the user understand that the page is loading, while also communicating what the page will look like. Here are a few reasons why you might consider using skeleton screens:

- **Prevent the user from thinking that the site isn’t working.** When a user visits a site or an application and they come across a blank screen while the page is loading, they may assume something is wrong and leave. Skeleton screens help users focus on the content being loaded and give them something to look at while waiting.
- **Create the illusion of a shorter wait time.** [Long loading times](https://www.nngroup.com/articles/website-response-times/) annoy users. Because a skeleton screen looks like a wireframe, it creates the illusion that the page is gradually transitioning into its final format. The indication of progress gives users a sense that it won’t take a long time to load.
- **Reduce users’** [**cognitive load**](https://www.nngroup.com/articles/minimize-cognitive-load/)**.** Instead of overwhelming users by showing them a blank page first and then immediately a full page of content, skeleton screens help users process what the page will look like and give them time to develop mental models of the page structure before they are bombarded with a lot of information at once. For example, when users see a big square with a little box under it, they will know to expect an image with a caption.

## Are Skeleton Screens Better than Progress Bars or Spinners?

Skeleton screens, progress bars, and spinners all show that the system is loading information, but they serve different purposes and work best in different situations. Here are a few guidelines to help you make the decision on when to use each design.

### Waiting-Period Lengths Matter

Spinners or wait animations provide feedback to users that the system is working but don’t give any indication on how long users will have to wait; therefore, they are best used when the page takes 2–10 seconds to load. Similarly, skeleton screens should be used with a wait time that’s under 10 seconds. On the other hand, progress bars are strongly recommended for any page that takes longer that 10 seconds to load because they give users a sense of the state of the system and of how much longer they have to wait. Anything above 10 seconds requires an explicit estimation of duration.

For waiting periods less than 10 seconds, both skeleton screens and spinners could work**.** How do you decide between the two? Spinners are typically best used on a single module, like a video or a card which is on a dashboard. Skeleton screens (with the exception of frame-display ones) are better when the full screen is loading because the wireframe gives users a sense of what the page will look like and, thus, minimizes cognitive load.

### No Skeleton Screens or Spinners for Quick Page Loads

If a page takes [less than 1 second](https://www.nngroup.com/articles/response-times-3-important-limits/) to load, skeleton screens or spinners aren’t necessary, as they likely won’t make a difference to the users’ experience. Using a skeleton screen in such situations can be annoying because the quick flashing page can cause users to feel like they can’t keep up.

### Progress Bars Are Best for Process-Related Indicators

Skeleton screens are used to indicate progress only when the process that the system is performing is a full-page load. Whenever some other process (e.g., download, upload, convert a file) is involved, it does not make sense (and could even be confusing) to show a skeleton screen. Instead, show a progress bar or a [wizard](https://www.nngroup.com/articles/wizards/) that walks the user through the steps of the process.

### Do Not Use a Frame-Display Skeleton Screen

Frame-display skeleton screens display no information about the page layout; they show only a header, footer, and an empty background. They should not be used as a progress indicator because they do not give users any sense that the page is gradually transitioning into its final format. If users end up having to wait for a long time, they will assume the page is not working and abandon it.

## Conclusion

Users generally get impatient by long loading periods. Skeleton screens ease the pain of waiting for medium-length durations by showing the page structure in a gradual manner, through placeholders and subtle animations. While skeleton screens are useful, they do not replace performance-optimization efforts. Skeleton screens are simply one extra tool for improving the wait users sometimes have to experience when content is loading.

## References

Thomas Mejtoft, Arvid Långström, and Ulrik Söderström. 2018. The effect of skeleton screens. *Proceedings of the 36th European Conference on Cognitive Ergonomics* (2018). DOI:http://dx.doi.org/10.1145/3232078.3232086

## Related Courses

- [#### Emerging Patterns in Interface Design

  Trending UX patterns and their impact on the total user experience

  Interaction](/courses/emerging-patterns-interface-design/?lm=skeleton-screens&pt=article)
- [#### Design Systems and Pattern Libraries

  Increase design quality, consistency, and efficiency

  Management](/courses/design-systems/?lm=skeleton-screens&pt=article)
- [#### Application Design for Web and Desktop

  Components, design patterns, workflows, and ways of interacting with complex data

  Interaction](/courses/application-ux/?lm=skeleton-screens&pt=article)

Design Patterns,progress indicators,wireframes,animation,timing,web trends,UI Design

## Related Topics

- Design Patterns
  [Design Patterns](/topic/design-patterns/)

## Learn More:

[![Skeleton Screens vs. Progress Bars vs. Spinners](https://media.nngroup.com/media/videos/thumbnails/Skeleton_Screen.jpg.1300x728_q75_autocrop_crop-smart_upscale.jpg)](https://www.youtube.com/watch?v=4GWqJEfzvmg "Skeleton Screens vs. Progress Bars vs. Spinners on YouTube (new window)")

Enable cookies
 to watch NN/g videos

Skeleton Screens vs. Progress Bars vs. Spinners

 Samhita Tankala
·
4 min

- [![](https://media.nngroup.com/media/videos/thumbnails/Cookie_Permissions-_5_Common_User_Types_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Cookie Permissions: 5 Common User Types

  Samhita Tankala
  ·
  3 min](/videos/cookie-permissions-user-types/?lm=skeleton-screens&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Cookie_Permissions-_6_Design_Guidelines_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Cookie Permissions: 6 Design Guidelines

  Samhita Tankala
  ·
  5 min](/videos/cookie-permissions-guidelines/?lm=skeleton-screens&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Accordions_-_When_to_Avoid_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Accordions: 5 Scenarios to Avoid Them

  Huei-Hsin Wang
  ·
  3 min](/videos/avoid-accordions/?lm=skeleton-screens&pt=article)

## Related Articles:

- [Infinite Scrolling: When to Use It, When to Avoid It

  Tim Neusesser
  ·
  9 min](/articles/infinite-scrolling-tips/?lm=skeleton-screens&pt=article)
- [Hostile Patterns in Error Messages

  Kate Kaplan
  ·
  7 min](/articles/hostile-error-messages/?lm=skeleton-screens&pt=article)
- [Inclusive Design

  Alita Kendrick
  ·
  6 min](/articles/inclusive-design/?lm=skeleton-screens&pt=article)
- [Revisiting Facial-Recognition Payment: Old Problems Still Lingering

  Leeloo Tang
  ·
  12 min](/articles/facial-recognition-payment/?lm=skeleton-screens&pt=article)
- [Executing UX Animations: Duration and Motion Characteristics

  Page Laubheimer
  ·
  9 min](/articles/animation-duration/?lm=skeleton-screens&pt=article)
- [10 Design Guidelines for Reporting Errors in Forms

  Rachel Krause
  ·
  6 min](/articles/errors-forms-design-guidelines/?lm=skeleton-screens&pt=article)