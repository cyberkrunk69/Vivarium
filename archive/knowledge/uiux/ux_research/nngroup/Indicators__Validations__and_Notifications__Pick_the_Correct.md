# Indicators, Validations, and Notifications: Pick the Correct Communication Option

Source: https://www.nngroup.com/articles/indicators-validations-notifications/

---

9

# Indicators, Validations, and Notifications: Pick the Correct Communication Option

Kim Flaherty

![](https://media.nngroup.com/media/people/photos/Kim-Headshot-2022.jpg.256x256_q75_autocrop_crop-smart_upscale.jpg)

Kim Flaherty

January 17, 2024
2024-01-17

[Share](#)

- [Email article](mailto:?subject=NN/g Article: Indicators, Validations, and Notifications: Pick the Correct Communication Option&body=https://www.nngroup.com/articles/indicators-validations-notifications/)
- [Share on LinkedIn](http://www.linkedin.com/shareArticle?mini=true&url=http://www.nngroup.com/articles/indicators-validations-notifications/&title=Indicators, Validations, and Notifications: Pick the Correct Communication Option&source=Nielsen%20Norman%20Group)
- [Share on Twitter](https://twitter.com/intent/tweet?url=http://www.nngroup.com/articles/indicators-validations-notifications/&text=Indicators, Validations, and Notifications: Pick the Correct Communication Option&via=nngroup)

Summary: 
Status feedback is crucial to the success of any system. Knowing when to use 3 common communication methods is key to supporting users.

In interaction design, a system, whether an application, website, or piece of hardware (anything from a [smartwatch](http://www.nngroup.com/articles/smartwatch/) to a [thermostat](http://www.nngroup.com/articles/emotional-design-fail/)), should always **keep users informed**, by providing appropriate feedback. Ensuring that the state of the system is always visible is one of the [10 usability heuristics for interface design](http://www.nngroup.com/articles/ten-usability-heuristics/). Information about system status, such as error messages and notifications of system activity, allows users to fully understand the current context.

## In This Article:

- [Communicating System Status](#toc-communicating-system-status-1)
- [Indicators](#toc-indicators-2)
- [Validations](#toc-validations-3)
- [Notifications](#toc-notifications-4)
- [Picking the Right Communication Option Is Important](#toc-picking-the-right-communication-option-is-important-5)
- [Conclusion](#toc-conclusion-6)

## Communicating System Status

The best way to communicate system status varies depending on several key factors:

- The **type** of information being communicated
- The **urgency** of the information — how important it is that the user sees it immediately
- Whether the user needs to take **action** as a result of the information

Three common approaches for status communication include validation, notifications, and status indicators. These terms are used sometimes interchangeably in product design, but they stand for different communication methods that should be used in different circumstances. Understanding the differences between them will help you sharpen your feedback to users by choosing the best option for each need.

![system status comparison chart](https://media.nngroup.com/media/editor/2024/01/24/validation-indicators-notifications-comparison.png)

## Indicators

An indicator is a way of making a page element (be it content or part of the user interface) **stand out to inform the user that there is something special** about it that warrants the user’s attention. Often, the indicator will denote that there has been some change to the item represented by that element.

Although, as we’ll see later, indicators are used quite frequently to signal validation errors or notifications, they can also be used on their own.  Indicators are visual cues intended to attract users’ attention to a particular piece of content or UI element that is dynamic in nature.  (If something always looks the same, it’s not an indicator, no matter how flamboyantly it’s designed.)

There are at least three possible ways of implementing indicators:

- Oftentimes, but not always, indicators are implemented as **icons**. Easily [recognizable icons](http://www.nngroup.com/articles/icon-usability/) can make very effective communication tools.
- **Typographical** variations can also be used as indicators; examples include the common convention of boldfacing unread email messages or color-coding stock symbols in an investment account if their price has changed substantially.
- Though less common, enlarged **size** or **animation** (e.g., vibration) can also be used to make certain items stand out from the crowd and thus serve as an indicator.

![yelp app, hot new restaurant flame icon indicator](https://media.nngroup.com/media/editor/2024/01/17/yelp_new_indicator1.jpg)

*Yelp used a red flame icon indicator in the search results to indicate that Paris Banh Mi is a Hot and New restaurant to try out. This indicator communicated additional information about Paris Banh Mi.*

**Characteristics of indicators:**

- Indicators are **contextual**. They are associated with a UI element or with a piece of content, and should be shown in close proximity to that element.
- Indicators are **conditional**— they are not always present, but appear or change depending on certain conditions. For example, a stock-performance indicator, such as the one in the American Century example below, may change to indicate if the stock price is increasing or decreasing.  Additionally, the tag indicator in the Yelp example above only appears if there is a deal at that business.
- Indicators are **passive**.  They do not require that a user take action, but are used as a communication tool to cue the user to something of note.

![Investment stock indicator up arrows](https://media.nngroup.com/media/editor/2024/01/24/american-century-stock-indicators.png)

*American Century Investments used a conditional indicator to provide information regarding a specific stock’s performance. When the daily change was positive, the indicator was a green arrow pointing up. When the daily change was negative, it showed a red arrow pointing down. The condition of the stock performance impacted the indicator that was shown next to the price.*

Indicators can introduce noise and clutter to your overall interface, and may distract users, so it is important to consider how many (if any) indicators to use in your design.

Consider the following when deciding if an indicator is appropriate:

- How important is the information to the user? Is it worth taking up space on the page to inform the user?
  - How often is the information used?
  - Would the user expect to see the information?
  - Would it be missed if it weren’t provided?
- How important is it for the application that the user discovers the information?

## Validations

Validation messages are **error messages** related to users’ inputs: they communicate whether the data just entered was incomplete or incorrect. For example, in e-commerce systems, validation messages often involve information such as name, billing address, and credit-card information.

![newsletter signup email validation red message](https://media.nngroup.com/media/editor/2024/01/17/cobra-golf-validation1.png)

*Cobragolf.com provided a validation message that clearly indicated which field was in error.*

**Characteristics of validation:**

- A user needs to take action to clear the validation message.
- The information in the validation message is contextual and applies to a specific user input that has a problem.

The way in which validation should be implemented varies based on the unique needs of the form.  However, in general, if the user’s input is incorrect, the system should inform the user by providing an identifiable and clear message that aids in correcting the error. Validation messages should follow the [guidelines for error messages](http://www.nngroup.com/articles/error-message-guidelines/) rather than simply identifying the problem, they should tell users how to fix it.  For instance,  don’t  state “Field is blank.” Please enter your street address” is more polite and directs to a solution.

Since validation is contextual, it can be helpful to use an **icon indicator** along with the validation message to help communicate which input(s) are missing or need corrected.

![](//s3.amazonaws.com/media.nngroup.com/media/editor/2015/07/14/bestbuy_validation.png)

*Bestbuy.com provided a helpful validation message telling users how to fix the problem and also used an icon indicator and a different color to attract users’ attention to the field that needed correction.*

## Notifications

Notifications are informational messages that **alert the user of general occurrences within a system**. Unlike validation, notifications may **not be directly tied to user input** or even to the user’s current activity in the system, but they usually inform the user of a change in the system state or of an event that may be of interest. In the case of email, social networks, and mobile-phone applications, notifications can even be delivered while a user is away from the application.

Notifications can be **contextual** —applying to a specific UI element— or **global** —applying to the system as a whole.

![Uniqlo contextual notification about size help tool](https://media.nngroup.com/media/editor/2024/01/17/uniqlo-contextual-notification2.jpg)

*Uniqlo used a contextual notification on their product detail page to bring attention to a tool that helps users find the right size. This notification does not require the user to take action to interact with the page. You could click the X button to close it, but it eventually disappeared after a period of inactivity.*

**Characteristics of notifications:**

- They are not triggered by users’ immediate actions.
- They announce an event that has some significance to the user.

There are two main types of notifications, which differ based on whether the user is required to act upon the notification:

- **Action-required notifications** alert the user of an event that requires a user action. In this sense, they are similar to validation, but since they were not sparked by the user’s own action, they require a different design.

Action-required notifications are often urgent and should be intrusive; for instance, they could be implemented as modal popups that interrupt the user, forcing immediate attention and requiring an action to be dismissed.

![mac OS notification](https://media.nngroup.com/media/editor/2024/01/17/mac-notification002.jpeg)

*The Mac operating system used a notification to inform users that an accessory device needed to be charged. The user could explicitly dismiss it from the screen, by opting to ignore or clicking anywhere outside of the notification. This is an intrusive notification that requires that the user take action.*

- **Passive notifications** are informational; they report a system occurrence that does not require any user action. Many notifications in mobile apps are passive: they usually announce an event of potential interest to the user.

Passive notifications are typically not urgent and should be less intrusive. A typical implementation of a passive notification may be a badge icon or a small nonmodal popover in a corner of a screen. Passive notifications can easily be missed, since they require no user action. When the information provided by the notification is key to the understanding of the system, an easy-to-ignore passive notification can be problematic.

![](//s3.amazonaws.com/media.nngroup.com/media/editor/2015/07/14/creativecloud_notification.png)

*Adobe Creative Cloud used a nonintrusive passive notification to inform the user of an available application update. This notification appeared on screen for several seconds before disappearing. The user did not need to take any action on it.*

![Add to cart notification - green banner top of page](https://media.nngroup.com/media/editor/2024/01/17/shopping-cart-notification.jpg)

*Visual Comfort and Co used a nonintrusive passive notification at the top of the product detail page to provide feedback that an item was added to the shopping cart. Such notifications sometimes cause issues for e-commerce shoppers who do not notice the message due to its location far away from the user's area of focus at the time (the add-to-cart button, which was further down the page). Users who miss the message may respond by adding an item to the cart multiple times or by disrupting their shopping flow to check the cart to see what items were added. No action was necessary to continue interacting with the page, yet it did persist if not dismissed. With its out-of-the-way placement on the page, persisting on the page was not intrusive to the user.*

![Intrusive add to cart notification - takes over screen](https://media.nngroup.com/media/editor/2024/01/17/mango-intrusive-cart-notification2.jpg)

On Mango.com when a user added an item to the cart, a notification appeared in a more intrusive way than Visual Comfort and Co. Taking over a portion of the screen reduces the risk that the user will not see the feedback. This notification was a bit of a hybrid between a passive and action-required notification. It was the direct result of a user action, so it's less important to require the user to take action to acknowledge it. Although it did have buttons to take action, if the user clicked anywhere or continued to interact with the page, the notification dismissed itself.

Notifications have the design challenge that they are not always the immediate and obvious result of a specific user action. In some instances, the user may be in the middle of doing something different and may not be thinking about the issue raised by the notification. This requires notifications to establish more context and provide users with sufficient background information to understand what the notification is about.

(In contrast, with a validation, the user has just done the thing that needs to be corrected. Thus, the validation message doesn’t need to educate users about the task at hand. For example, if an e-commerce checkout form has a field for a credit-card expiration date that was left blank, the validation message doesn’t need to say *“Please provide the expiration date for the credit card you want to have charged $29.90 to pay for the blue sleeveless dress you are in the process of buying on Uniqlo.com.”* However, a notification the following day that the dress has been shipped from the warehouse would need to say more than *“Your package has shipped.”*)

If a notification is contextual and relates to a specific element in the interface, an icon indicator on the element can communicate where that notification applies and catch the user’s attention.  For instance, an indicator badge on a mobile-app icon shows that the user has received a notification from the corresponding app.

![iphone notifications banners and badge](https://media.nngroup.com/media/editor/2024/01/17/iphone-notifications.jpg)

*The iPhone messaging app created a notification to communicate that a new message was received. Along with the notification, an indicator badge was placed on the messaging-app icon to communicate where the notification applied. To clear the indicator, the user had to view the message.*

![](//s3.amazonaws.com/media.nngroup.com/media/editor/2015/07/14/mint_validation.png)

*Mint.com used an indicator together with a notification to communicate that an account needed attention. The warning indicator* (1) *appeared in close proximity to the summary of the account that needed attention, while the notification* (2) *appeared in the central area of the page with other important information. The actual text in the notification message could have been more helpful, though.*

## Picking the Right Communication Option Is Important

Using the wrong communication method can have a negative impact on the users’ experience. Let’s refer back to the scenario above where Yelp utilized a green-tag indicator in the search results to indicate that Tea Market had a special deal running. This information is contextual and important to users who have specifically searched for a place to have tea.

You may think that an alternative way of alerting users of potential tea deals would be to send them a notification when such a deal has become available. Wrong! A notification sent irrespective of the current user goal would likely be ignored, and may even annoy users because it will disrupt their current task and be irrelevant to their current needs.

(In general, [any type of ad tends to be ignored unless it is related to the users’ aims and mindset](http://www.nngroup.com/articles/making-web-advertisements-work/).)

Alternatively, a toast (a small nonmodal popup that disappears after a few seconds, like the *New Stories* one used by the Facebook app), while appropriate for passive notifications, would be a bad way to implement an error message, be it validation or otherwise. In fact, one of our mobile users spent 5 minutes waiting for some content to load only because she hadn’t notice the little error message presented at the bottom of the screen that quickly faded away after 5 seconds.

![](//s3.amazonaws.com/media.nngroup.com/media/editor/2015/07/14/allmodern_notification.png)

*Allmodern.com used an action-required notification to communicate that a product was saved as a favorite.  For a user that is saving a lot of items to their favorites, this can be a bothersome and intrusive way of providing feedback. This may be better communicated by showing a passive nonmodal popover in the corner of the screen that can be seen, but doesn’t require the user to take action to clear it.*

## Conclusion

Remember the key differences between the three communication methods are:

- Indicators provide supplementary information about a dynamic piece of content or UI element. They are conditional —that is, they may appear or change under specific conditions.
- Validations are tied to a user’s action or input.
- Notifications are focused on system-related events.

Understanding when and how to use each of these feedback tools is important in order to build consistency in the communication to users. By assessing the type of information delivered, we can determine the correct mechanism to use.

## Related Courses

- [#### Application Design for Web and Desktop

  Components, design patterns, workflows, and ways of interacting with complex data

  Interaction](/courses/application-ux/?lm=indicators-validations-notifications&pt=article)

Application Design,standards & conventions

## Related Topics

- Application Design
  [Application Design](/topic/applications/)

## Learn More:

- [![](https://media.nngroup.com/media/videos/thumbnails/Icon_Interpretation_vs_Recognizability_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Icon Interpretation vs. Recognizability

  Kate Kaplan
  ·
  4 min](/videos/icon-interpretation-vs-recognizability/?lm=indicators-validations-notifications&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Is_the_Floppy_Disk_Dead_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Is the Floppy Disk Dead?

  Kate Kaplan
  ·
  4 min](/videos/is-the-floppy-disk-dead/?lm=indicators-validations-notifications&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/2-Factor_Authentication_2-FA_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  2-Factor Authentication (2-FA)

  Tim Neusesser
  ·
  4 min](/videos/2-factor-authentication/?lm=indicators-validations-notifications&pt=article)

## Related Articles:

- [Top 10 Application-Design Mistakes

  Jakob Nielsen and Page Laubheimer
  ·
  13 min](/articles/top-10-application-design-mistakes/?lm=indicators-validations-notifications&pt=article)
- [OK-Cancel or Cancel-OK? The Trouble With Buttons

  Jakob Nielsen
  ·
  2 min](/articles/ok-cancel-or-cancel-ok/?lm=indicators-validations-notifications&pt=article)
- [Defeated By a Dialog Box

  Jakob Nielsen
  ·
  6 min](/articles/defeated-by-a-dialog-box/?lm=indicators-validations-notifications&pt=article)
- [Checkboxes vs. Radio Buttons

  Jakob Nielsen
  ·
  6 min](/articles/checkboxes-vs-radio-buttons/?lm=indicators-validations-notifications&pt=article)
- [Apps Within Apps: UX Lessons from WeChat Mini Programs

  Feifei Liu
  ·
  9 min](/articles/wechat-mini-programs/?lm=indicators-validations-notifications&pt=article)
- [Radio Buttons: Select One by Default or Leave All Unselected?

  Kara Pernice
  ·
  12 min](/articles/radio-buttons-default-selection/?lm=indicators-validations-notifications&pt=article)