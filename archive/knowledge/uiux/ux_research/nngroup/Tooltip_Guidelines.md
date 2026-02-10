# Tooltip Guidelines

Source: https://www.nngroup.com/articles/tooltip-guidelines/

---

5

# Tooltip Guidelines

Alita Kendrick

![](https://media.nngroup.com/media/people/photos/alita-kendrick.jpg.256x256_q75_autocrop_crop-smart_upscale.jpg)

[Alita Kendrick](/articles/author/alita-kendrick/)

January 27, 2019
2019-01-27

[Share](#)

- [Email article](mailto:?subject=NN/g Article: Tooltip Guidelines&body=https://www.nngroup.com/articles/tooltip-guidelines/)
- [Share on LinkedIn](http://www.linkedin.com/shareArticle?mini=true&url=http://www.nngroup.com/articles/tooltip-guidelines/&title=Tooltip Guidelines&source=Nielsen%20Norman%20Group)
- [Share on Twitter](https://twitter.com/intent/tweet?url=http://www.nngroup.com/articles/tooltip-guidelines/&text=Tooltip Guidelines&via=nngroup)

Summary: 
Tooltips are user-triggered messages that provide additional information about a page element or feature. Although tooltips aren’t new to the web, they are often incorrectly implemented.

Tooltips aren’t new, but they’re often misused.

## In This Article:

- [Defining Tooltips](#toc-defining-tooltips-1)
- [Tooltips vs. Popup Tips](#toc-tooltips-vs-popup-tips-2)
- [Tooltip-Usage Guidelines](#toc-tooltip-usage-guidelines-3)
- [Additional Recommendations](#toc-additional-recommendations-4)
- [Conclusion](#toc-conclusion-5)

## Defining Tooltips

> Definition: A **tooltip** is a brief, informative message that appears when a user interacts with an element in a graphical user interface (GUI). Tooltips are usually initiated in one of two ways: through a mouse-hover gesture or through a keyboard-hover gesture.

(In case you’re wondering what keyboard hover is: to access the active elements on a page, users can usually move the mouse to them or tab through them using the keyboard. Keyboard hover refers to maintaining the keyboard focus on the same element for a longer time.)

Tooltips can be attached to any active element (icons, text links, buttons, etc.) on a page. They provide descriptions or explanations for their paired element. Thus, tooltips are highly contextual and specific and don’t explain the bigger picture or entire task flow.

One important aspect of tooltips is that they are user-triggered. Therefore, tips that pop up on pages to inform users about new features or [how to use a specific functionality](https://www.nngroup.com/videos/just-in-time-help/) are not tooltips.

Because tooltips are initiated by a hover gesture, they can be used only on devices with a mouse or keyboard. They are not normally available on touchscreens. (In the future, tooltips could be initiated on eyetracking-enabled devices when the user’s gaze dwells on a GUI element for a certain duration.)

## Tooltips vs. Popup Tips

Although tooltips are mainly limited to desktop computers and laptops, they do have a sister element that is common on touchscreen devices: popup tips. Both tooltips and popup tips have the same goal: to provide helpful, additional content. The following table shows the key similarities and differences between popup tips and tooltips.

|  |  |  |
| --- | --- | --- |
|  | **Tooltips** | **Popup tips** |
| Type of site | Desktop | Any |
| Initiated by | Hover (mouse or keyboard) | Touch/click |
| Terminated when | User leaves predefined interaction area | User taps to close or clicks another area of the screen |
| Paired element | Icon, text link, button, image | “?” or “i” icon |
| Content type | Microcontent | Microcontent |

This article will focus on tooltips and their use on desktop sites.

## Tooltip-Usage Guidelines

### **1. Don’t use tooltips for information that is vital to task completion.**

Users shouldn’t need to find a tooltip in order to complete their task. Tooltips are best when they provide additional explanation for a form field unfamiliar to some users or reasoning for what may seem like an unusual request. Remember that tooltips disappear, so instructions or other directly actionable information, like field requirements, shouldn’t be in a tooltip. (If it is, people will have to commit it to their working memory in order to be able to act upon it.)

![Screenshot of a form on Amtrak.com, where hovering over an icon triggers a tooltip explaining a field.](https://media.nngroup.com/media/editor/2018/11/19/amtrak.png)

*❌ **Don't:**The Amtrak website put password requirements into a tooltip (accessed via a mouse hover). This type of information is essential to a user successfully completing the Create an Account process and therefore should always be present on the screen.*

![Screenshot from the FedEx website where a tooltip contains content explaining why a field was listed.](https://media.nngroup.com/media/editor/2018/11/19/fedex.png)

*✅ **Do:**FedEx used tooltips to provide additional information for the shipping-form fields. For example, the Email field had a tooltip explaining why that field was listed. (This tooltip was accessed via a mouse hover. )*

### **2. Provide brief and helpful content inside the tooltip.**

Tooltips with obvious or [redundant text](https://www.nngroup.com/articles/reduce-redundancydecrease-duplicated-design-decisions/) are not beneficial to users. If you can’t think of particularly helpful content, don’t offer a tooltip. Otherwise, you’ll just add [information pollution](https://www.nngroup.com/articles/information-pollution/) to your UI and waste the time of any users unlucky enough to activate that tooltip.

Additionally, lengthy content is no longer a ‘tip’, so keep it brief. Tooltips are [microcontent](https://www.nngroup.com/articles/microcontent-how-to-write-headlines-page-titles-and-subject-lines/), — short text fragments intended to be self-sufficient. Your copy can be single- or multiple-line long as long as it’s relevant and it does not block related content.

![Sprint.com screenshot with redundant tooltip and button copy.](https://media.nngroup.com/media/editor/2018/11/19/sprint.png)

*❌ **Don't:**On the Sprint website, a button with the label Add**new line also had a tooltip with the text Add new line. This tooltip is repetitive and unnecessary.*

![Alibaba screenshot with a tooltip describing an unlabeled icon](https://media.nngroup.com/media/editor/2018/11/19/alibaba.png)

*✅ **Do:**Alibaba had a search bar with an unlabeled camera icon. When users hovered over this icon, a tooltip that read**Search by image appeared. This functionality was likely unfamiliar to many users, and therefore a tooltip describing its purpose was helpful.*

### **3. Support *both* mouse *and* keyboard hover.**

Tooltips that appear only on mouse hover are inaccessible for users that rely on [keyboards](https://www.nngroup.com/articles/keyboard-accessibility/) to navigate. Be inclusive in your design and ensure that your tooltips are accessible via keyboards.

![McDonalds screenshot showing lack of keyboard tooltip support.](https://media.nngroup.com/media/editor/2018/11/19/1mcdonalds-combined.png)

*❌ **Don't:**The McDonalds website did not support tooltips via keyboard triggers. A mouse-hover–initiated tooltip (top) was not available when the user tabbed through the same page (bottom).*

![Wikipedia screenshot showing tooltip trigger via keyboard.](https://media.nngroup.com/media/editor/2018/11/19/wikipedia.png)

*✅ **Do:**Wikipedia supported keyboard triggers for tooltips. The same tooltips appeared on mouse hover and keyboard hover.*

### **4. Use tooltip arrows when multiple elements are nearby.**

Arrows are beneficial to clearly identify to which element the tooltip is associated. When there are several nearby elements, these arrows help avoid confusion.

![PowerPoint screenshot showing lack of tooltip arrows in a somewhat crowded area of the screen.](https://media.nngroup.com/media/editor/2018/11/19/powerpoint-online.png)

*❌ **Don't:**PowerPoint had several icons in close proximity to one another. Without the tooltip arrows, it was difficult to know which tooltips correspond to which element.*

![Screenshot of Witeboard using tooltip arrows.](https://media.nngroup.com/media/editor/2018/11/19/witeboard.png)

*✅ **Do:**Witeboard used tooltip arrows to signify which icon the tip is for. Although the icons are fairly spaced out, the arrows provide additional clarity with minimal visual noise.*

### **5. Use tooltips consistently throughout your site.**

Tooltips are hard to discover because they often lack visual cues. If tooltips are erratically displayed throughout your site, people may never discover them. It’s important to be consistent and provide tooltips for all the elements in your design rather than just for some. If only some of the elements need additional explanation, use popup tips for these elements instead.

![Business Insider screenshot showing inconsistent use of tooltips.](https://media.nngroup.com/media/editor/2018/11/19/business-insider.png)

*❌ **Don't:**The Business Insider website used tooltips for 2 of 3 icons in its navigation menu. (Note: on the homepage of the Business Insider website, the globe icon did have a tooltip that read Globe Icon. However, the label was not helpful, nor indicative of its functionality: a language selector.) In general, we advise against using icons without labels and hiding labels inside tooltips, but this offense is even graver when the tooltip labels are inconsistently deployed.*

![Todoist screenshot showing consistent use of tooltips.](https://media.nngroup.com/media/editor/2018/11/19/1to-do-ist.png)

*✅ **Do:**Todoist used tooltips consistently. All three icons in the main section have tooltips. Consistency instills confidence in users by meeting their expectations.*

## Additional Recommendations

**Provide Tooltips for Unlabeled Icons**

Most icons have some level of ambiguity, which is why we recommend text labels for all **[icons](https://www.nngroup.com/articles/icon-usability/)**. If you’re too stubborn to provide text labels for the icons on your site, the least you can do is provide your users with a descriptive tooltip.

**Ensure Tooltips Have Moderate Against the Background**

Users generally look where they click (or hover). However, since tooltips lack, a moderate **[contrast](https://www.nngroup.com/articles/low-contrast/)** is important to ensure users see the text in the tooltip. Additionally, for users with visual impairments, a white page with light-grey tooltips is especially difficult to read.

**Position Tooltips So They Don’t Block Related Content**

When tooltips block the content they’re related to, they cause users to repeat steps (i.e. move their mouse to close the tooltip, read the information or field again, hover to reveal tooltip). Test your tooltip positioning to ensure that the content does not block other information pertinent to the user’s goal.

## Conclusion

Tooltips are often a fail-safe for users when they can’t understand a feature. Many of today’s use cases for tooltips could be omitted if people followed other design guidelines (for example, labeling icons). Important information should always be on the page; therefore, tooltips shouldn’t be essential for the tasks users need to accomplish on your site.

The more we strive for extreme [minimalism](https://www.nngroup.com/articles/roots-minimalism-web-design/), the more tooltips we’ll need, and the more work for our users. The next time you consider a tooltip, ask: is the information in the tooltip necessary for users in order to complete a task? If the answer is no, a tooltip is well-suited. Otherwise, the information should be present on the screen.

![Graphic explaining when to use a tooltip. If the information is necessary for a user to complete a task, always keep the information on the screen and not in a tooltip.](https://media.nngroup.com/media/editor/2018/11/19/v2tooltipsasset-9.png)

## Related Courses

- [#### Application Design for Web and Desktop

  Components, design patterns, workflows, and ways of interacting with complex data

  Interaction](/courses/application-ux/?lm=tooltip-guidelines&pt=article)

help and user assistance,popups,Interaction Design,Application Design

## Related Topics

- Interaction Design
  [Interaction Design](/topic/interaction-design/)
- [Application Design](/topic/applications/)

## Learn More:

- [![](https://media.nngroup.com/media/videos/thumbnails/Teslers_Law-_Shift_Complexity_to_Simplify_UX_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Tesler’s Law: Shift Complexity to Simplify UX

  Lola Famulegun
  ·
  3 min](/videos/teslers-law/?lm=tooltip-guidelines&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Overflow_Menu_Icons_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Overflow Menu Icons

  Kate Kaplan
  ·
  4 min](/videos/overflow-menu-icons/?lm=tooltip-guidelines&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Usability_Heuristic_10_Help_and_Documentation_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Usability Heuristic 10: Help and Documentation

  Maria Rosala
  ·
  3 min](/videos/help-and-documentation/?lm=tooltip-guidelines&pt=article)

## Related Articles:

- [Mobile Tutorials: Wasted Effort or Efficiency Boost?

  Alita Kendrick
  ·
  6 min](/articles/mobile-tutorials/?lm=tooltip-guidelines&pt=article)
- [Instructional Overlays and Coach Marks for Mobile Apps

  Aurora Harley
  ·
  6 min](/articles/mobile-instructional-overlay/?lm=tooltip-guidelines&pt=article)
- [Onboarding Tutorials vs. Contextual Help

  Page Laubheimer
  ·
  7 min](/articles/onboarding-tutorials/?lm=tooltip-guidelines&pt=article)
- [Web UX: Study Guide

  Huei-Hsin Wang
  ·
  15 min](/articles/web-ux-study-guide/?lm=tooltip-guidelines&pt=article)
- [Overlay Overload: Competing Popups Are an Increasing Menace

  Kate Moran
  ·
  6 min](/articles/overlay-overload/?lm=tooltip-guidelines&pt=article)
- [Pop-ups and Adaptive Help Get a Refresh

  Katie Sherwin
  ·
  6 min](/articles/pop-up-adaptive-help/?lm=tooltip-guidelines&pt=article)