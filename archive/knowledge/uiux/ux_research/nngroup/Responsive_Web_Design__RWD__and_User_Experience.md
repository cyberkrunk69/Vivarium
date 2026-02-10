# Responsive Web Design (RWD) and User Experience

Source: https://www.nngroup.com/articles/responsive-web-design-definition/

---

4

# Responsive Web Design (RWD) and User Experience

Amy Schade

![](https://media.nngroup.com/media/people/photos/amy_schade_headshot.jpg.256x256_q75_autocrop_crop-smart_upscale.jpg)

Amy Schade

May 4, 2014
2014-05-04

[Share](#)

- [Email article](mailto:?subject=NN/g Article: Responsive Web Design (RWD) and User Experience&body=https://www.nngroup.com/articles/responsive-web-design-definition/)
- [Share on LinkedIn](http://www.linkedin.com/shareArticle?mini=true&url=http://www.nngroup.com/articles/responsive-web-design-definition/&title=Responsive Web Design (RWD) and User Experience&source=Nielsen%20Norman%20Group)
- [Share on Twitter](https://twitter.com/intent/tweet?url=http://www.nngroup.com/articles/responsive-web-design-definition/&text=Responsive Web Design (RWD) and User Experience&via=nngroup)

Summary: 
Responsive design teams create a single site to support many devices, but need to consider content, design and performance across devices to ensure usability.

## In This Article:

- [Defining Responsive Design](#toc-defining-responsive-design-1)
- [Creating Usable Experiences](#toc-creating-usable-experiences-2)
- [Focusing on Content](#toc-focusing-on-content-3)
- [Considering Performance](#toc-considering-performance-4)
- [Conclusion](#toc-conclusion-5)

## Defining Responsive Design

Responsive web design (RWD) is a web development approach that creates **dynamic changes** to the appearance of a website, **depending on the screen size and orientation** of the device being used to view it. RWD is one approach to the problem of designing for the multitude of devices available to customers, ranging [from tiny phones to huge desktop monitors](http://www.nngroup.com/articles/transmedia-design-for-3-screens/).

RWD uses so-called breakpoints to determine how the layout of a site will appear: one design is used above a breakpoint and another design is applied below that breakpoint. The breakpoints are commonly based on the width of the browser.

[ ](//s3.amazonaws.com/media.nngroup.com/media/editor/2014/04/25/london_700_2.mp4)

*This brief video (0:37) shows the responsive Transport for London website changing as the browser window is narrowed and widened.*

The **same HTML is served to all devices**, using CSS (which determines the layout of webpage) to change the appearance of the page. Rather than creating a separate site and corresponding codebase for wide-screen monitors, desktops, laptops, tablets and phones of all sizes, a single codebase can support users with differently sized viewports.

In responsive design, **page elements reshuffle** as the viewport grows or shrinks. A three-column desktop design may reshuffle to two columns for a tablet and a single column for a smartphone. Responsive design relies on proportion-based grids to rearrange content and design elements.

While responsive design emerged as a way to provide equal access to information regardless of device, it is also possible to hide certain items — such as background images, as in the Transport for London example above, [secondary content](http://www.nngroup.com/articles/defer-secondary-content-for-mobile/) or supplementary navigation — on smaller screens. Decisions about hiding content and functionality or altering appearance for different device types should be based on knowledge about your users and their needs.

RWD has potential advantages over developing separate sites for different device types. The use of a single codebase can make development faster, compared to developing 3 or 4 distinct sites, and makes **maintenance easier over time**, as one set of code and content needs to be updated rather than 3 or 4. RWD is also relatively “future-proof” in that it can support new breakpoints needed at any time. If a 5-inch device or 15-inch device takes off in the market, the code can support the new devices. RWD doesn’t tie design to a particular device.

![](//s3.amazonaws.com/media.nngroup.com/media/editor/2014/04/24/bostonglobe_desktop.png)

![](//s3.amazonaws.com/media.nngroup.com/media/editor/2014/04/25/boston_tab_mob.png)

*The Boston Globe is well-known for using responsive design. The 3-column desktop version (top) changes to a 2-column design on tablets (bottom left) and a single column for mobile (bottom right).*

Because elements need to be able to resize and shuffle, it is often easier to implement a responsive design on a site that is focused on content, rather than functionality. Complex data or interactions can be hard to fit into modular pieces that are easy to shuffle around a page, while preserving clarity and functionality.

## Creating Usable Experiences

Because responsive design relies on shuffling elements around the page, design and development need to work closely together to ensure a usable experience across devices. Responsive design often turns into solving a puzzle — how to reorganize elements on larger pages to fit skinnier, longer pages or vice versa. However, **ensuring that elements fit within a page is not enough**. For a responsive design to be successful, the design must also be usable at all screen resolutions and sizes.

When elements move around the page, the user experience can be completely different from one view of the site to the next. It is important that design and development teams work together not to just determine how the content should be shuffled around, but to also see **what the end result of that shift looks like** and how it affects the user experience.

Many teams look to popular responsive-design frameworks, such as Bootstrap to help create designs. Such frameworks can be a great help in moving development along. However, carefully consider how the framework will work with the content and functionality of your site, rather than how it works in general.

We always recommend [conducting usability testing](http://www.nngroup.com/articles/mobile-usability-testing/) on designs. For responsive designs, we recommend **testing across platforms**. It’s tricky enough to design a website that is usable on a desktop. It is even trickier to design a website that is usable in many rearrangements or configurations of its elements, across various screen sizes and orientations. The same design element that may work swimmingly on a desktop may work horribly on a smartphone, or vice versa.

## Focusing on Content

[Content prioritization](http://www.nngroup.com/articles/responsive-design-intranets) is one key aspect to doing responsive design well. Much [more content is visible](http://www.nngroup.com/articles/scaling-user-interfaces/) without scrolling on a large desktop monitor than on a small smartphone screen. If users don’t instantly see what they want on a desktop monitor, they can easily glance around the page to discover it. On a smartphone, users may have to scroll endlessly to discover the content of interest. Smart content prioritization helps users find what they need more efficiently.

## Considering Performance

[Performance](http://www.nngroup.com/articles/website-response-times/) can also be an issue with responsive design. RWD delivers the **same code to all devices**, regardless if the piece of code applies to that design or not. Changes to the design occur on the client-side, meaning each device — the phone, tablet or computer — receives the full code for all devices and takes what it needs.

A 4-inch smartphone receives the same code as a 24-inch desktop monitor. This can bog down performance on a smartphone, which may be relying on a slower, spottier data connection. (This is why some sites turn to **adaptive design**, where the server hosting the website detects the device that makes the request and delivers different batches of HTML code based on that device.)

To truly assess the user experience of a responsive design, do not test your responsive designs only in the comfort of your own office, on your high-speed connection. Venture out into the wild with your smartphone— between tall buildings in a city, in interior conference rooms or basements, in remote areas with spotty connectivity, in known trouble spots for your own cell-phone’s network connection — and see how your site performs in varied conditions. The goal of many responsive designs is to give equivalent access to information regardless of device. A smartphone user does not have an equivalent experience to a desktop user if download times are intolerable.

## Conclusion

Responsive design is a tool, not a cure-all. While using responsive design has many perks when designing across devices, using the technique does not ensure a usable experience (just as using a gourmet recipe does not ensure the creation of a magnificent meal.) Teams must focus on the details of content, design, and performance in order to support users across all devices.

For more about designing for different devices, see our course [Scaling User Interfaces](http://www.nngroup.com/courses/scaling-responsive-design/).

## Related Courses

- [#### The Human Mind and Usability

  Use psychology to predict and explain how your customers think and act

  Interaction](/courses/human-mind/?lm=responsive-web-design-definition&pt=article)
- [#### Web Page UX Design

  Strategically combine content, visuals, and interactive components to design successful web pages

  Interaction](/courses/web-page-design/?lm=responsive-web-design-definition&pt=article)

Mobile & Tablet,Web Usability,responsive design,performance

## Related Topics

- Mobile & Tablet
  [Mobile & Tablet](/topic/mobile-and-tablet-design/)
- [Web Usability](/topic/web-usability/)

## Learn More:

- [![](https://media.nngroup.com/media/videos/thumbnails/Images_on_Mobile-Script_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Images on Mobile

  Raluca Budiu
  ·
  4 min](/videos/mobile-images/?lm=responsive-web-design-definition&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Passwordless_Accounts.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Passwordless Accounts

  Raluca Budiu
  ·
  5 min](/videos/passwordless-accounts/?lm=responsive-web-design-definition&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Accordions.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Accordions on Mobile

  Raluca Budiu
  ·
  4 min](/videos/accordions-on-mobile/?lm=responsive-web-design-definition&pt=article)

## Related Articles:

- [Visual Indicators to Differentiate Items in a List

  Aurora Harley
  ·
  6 min](/articles/visual-indicators-differentiators/?lm=responsive-web-design-definition&pt=article)
- [Progress in Mobile User Experience

  Raluca Budiu
  ·
  6 min](/articles/mobile-usability-update/?lm=responsive-web-design-definition&pt=article)
- [List Thumbnails on Mobile: When to Use Them and Where to Place Them

  Aurora Harley
  ·
  4 min](/articles/mobile-list-thumbnail/?lm=responsive-web-design-definition&pt=article)
- [Predictions for the Web in Year 2000

  Jakob Nielsen
  ·
  4 min](/articles/predictions-for-the-web-in-year-2000/?lm=responsive-web-design-definition&pt=article)
- [Scan and Shake: A Lesson in Technology Adoption from China’s WeChat

  Yunnuo Cheng and Raluca Budiu
  ·
  13 min](/articles/wechat-qr-shake/?lm=responsive-web-design-definition&pt=article)
- [Mobile Faceted Search with a Tray: New and Improved Design Pattern

  Kathryn Whitenton
  ·
  5 min](/articles/mobile-faceted-search/?lm=responsive-web-design-definition&pt=article)