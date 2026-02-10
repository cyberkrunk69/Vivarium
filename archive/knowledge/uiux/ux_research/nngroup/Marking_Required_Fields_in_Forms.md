# Marking Required Fields in Forms

Source: https://www.nngroup.com/articles/required-fields/

---

6

# Marking Required Fields in Forms

Raluca Budiu

![](https://media.nngroup.com/media/people/photos/2023-04-portraits-raluca.jpg.256x256_q75_autocrop_crop-smart_upscale.jpg)

[Raluca Budiu](/articles/author/raluca-budiu/)

June 16, 2019
2019-06-16

[Share](#)

- [Email article](mailto:?subject=NN/g Article: Marking Required Fields in Forms&body=https://www.nngroup.com/articles/required-fields/)
- [Share on LinkedIn](http://www.linkedin.com/shareArticle?mini=true&url=http://www.nngroup.com/articles/required-fields/&title=Marking Required Fields in Forms&source=Nielsen%20Norman%20Group)
- [Share on Twitter](https://twitter.com/intent/tweet?url=http://www.nngroup.com/articles/required-fields/&text=Marking Required Fields in Forms&via=nngroup)

Summary: 
Using an asterisk to mark required fields is an easy way to improve the usability of your forms. Only marking optional fields makes it difficult for people to fill out the form.

A common question in many of our [UX Conference](https://www.nngroup.com/ux-conference/) classes is: should you mark the **required** fields in a form? If most fields in the form are required, should we still mark them? (That’s a lot of marks, after all.) The short answer is **yes**. And I’ll spend the rest of the article explaining why.

## In This Article:

- [The Temptation to Not Mark the Required Fields](#toc-the-temptation-to-not-mark-the-required-fields-1)
- [How to Mark the Required Fields?](#toc-how-to-mark-the-required-fields-2)
- [Should You Mark the Optional Fields, Too?](#toc-should-you-mark-the-optional-fields-too-3)
- [How About Login Forms?](#toc-how-about-login-forms-4)
- [Conclusion](#toc-conclusion-5)
- [A Note on Accessibility](#toc-a-note-on-accessibility-6)

## The Temptation to Not Mark the Required Fields

Often designers feel that the having a marker for every single required field is repetitive, ugly, takes too much space, and, with longer forms, may even seem oppressive (the form requires so much from the user!).  So, they usually adopt one or both of the following strategies:

1. They show instructions at the top of the form saying *All fields are required* or *All fields are required unless otherwise indicated.*
2. They mark the optional fields, since they are usually fewer.

(In some rare situations, they don’t do anything: they simply assume users will magically know what fields are required; if they don’t, then they will just have to deal with the resulting error.)

![Left: The form titled Tell Us About Yourself includes fields such as First Name, Middle Initial (opt.), Last Name, Suffix (opt), Date of Birth: Month, Day. Right: The fields are Full Name, Name on card, email address, and phone number.](https://media.nngroup.com/media/editor/2019/06/04/citi-amex.png)

*Citicards’ credit-card application (left) included small-font italic instructions*All fields are required unless specified optional *at the top of its form; American Express’s form (right) had no instructions at all. In both forms, only optional fields were marked: in the case of Citibank with the somewhat unclear abbreviation*opt*.*

What’s wrong with these approaches? There are a few problems:

- **People don’t read instructions at the top of forms.**

  It’s well known that users don’t read instructions, and they are particularly less likely to read instructions at the top of a form. Form fields seem self-sufficient — after all, each field has a specific instruction — its label, why would you need to read anything else to fill it in?
- **Even if people read instructions, they may forget them.**

  You may think: if users read the instruction at the top, how could they forget it — it’s such a simple thing? Well, they do forget — especially if the form is long or if they get interrupted while filling it out (a situation that is common on mobile). And even if people don’t forget the instruction, you’re increasing their [cognitive load](https://www.nngroup.com/articles/minimize-cognitive-load/) by having them commit it to their [working memory](https://www.nngroup.com/articles/working-memory-external-memory/). In other words, you’re making it harder for them to do their task. Filling in the form itself is quite challenging for your users — why would you want to make it even more so?
- **People have to scan the form to determine if the field is required.**

  We’ve seen that, whether you include instructions at the top of the form or not, the result is likely to be the same — people will ignore or forget them. So, what happens when the user fills out the form? How do they know whether a field is required? Well, the more-diligent users will look around trying to figure it out — they will scan the form and find a field that is marked *optional* (sometimes scrolling the page, like in the American Express example above, where the first optional field appears below the mobile fold); if they do find one, they will assume that anything not marked is required. But that takes time and [interaction cost](https://www.nngroup.com/articles/interaction-cost-definition/) — and, again, why would you make it harder for your users to fill in the form?

  Most users, however, will not bother to look around — they will simply make assumptions. They will say – “Well, phone number – they don’t really need my phone number, do they? Maybe I’ll leave this blank”. And even if they don’t leave it blank, having to pause to decide whether a field needs to be completed slows down the interaction and makes the process seem longer and more tedious. (Remember, as much as you’d like to think otherwise, nobody wants to fill out a form — whether on a small screen or on a large one.) The result will be a form-submission error, which will mean even more time spent addressing it.

The solution is simple: **mark all the required fields**. Be as explicit and transparent as possible: for every single field that must be completed, mark it as required.

## How to Mark the Required Fields?

There are at least two options here: an asterisk (whether red or not) and the word “required”.

![Form titled Card details with two fields: Name and Card Number](https://media.nngroup.com/media/editor/2019/06/04/2019-05-31-121132.png)

*The iOS Wallet app used the placeholder*Required*to indicate the required fields. (In general, especially with longer forms, it’s better to have the word* Required*outside the field instead of inside it, to make it easy to identify the fields that still need to be filled in.)*

The asterisk has become very common on the web and users are familiar with its meaning. Its main advantage is that it does not take up much space and looks different enough from the label text, so use it.

**Should the asterisk precede or follow the field label?** That is unlikely to make a practical difference, but one reason to put it just before the field description is to help the eyes easily locate which fields are required by scanning just the left-most character of the label.

![Left: Where are you shipping from form; Right: Registration form ](https://media.nngroup.com/media/editor/2019/06/04/ups0usps.PNG)

*Both these sites used the asterisk to mark required fields: UPS (left) displayed the asterisk at the end of the label and USPS (right) showed it at the beginning, in red. Showing it at the beginning in a different color makes it slightly easier to identify the required fields, which may prove useful when the form is longer. (However, we don’t recommend using as small a font size as the one used for the USPS asterisk.)*

**Should the asterisk be red?** Not necessarily, but red has become the expected required-marker color on the web, which is a reason in its own right to stick with this choice (according to [Jakob’s Law](https://www.nngroup.com/videos/jakobs-law-internet-ux/)). In any case, there is some value to using different colors for the asterisk and for the field label: it allows users to quickly separate the two and focus on the field label while trying to decode what the field means. While red is somewhat recommended, we have a strong recommendation to [avoid pale grays or low-contrast colors](https://www.nngroup.com/articles/low-contrast/) for the asterisk. Slightly muted colors can have aesthetic benefits, but truly low contrast symbols constitute an accessibility problem for low-vision or elderly users and slow down visual processing of the form for everybody.

## Should You Mark the Optional Fields, Too?

While it’s not obligatory, **marking the optional fields does lighten the user’s cognitive load**: in the absence of that word, the user must look around and infer that the field is optional based on the other fields being marked as required. If the word *optional* is next to the field descriptor, that task becomes a tad easier.

Not specifying that a field is optional is not a deal breaker, but doing so is a nice perk.

![Form for adding a new address to your sephora account](https://media.nngroup.com/media/editor/2019/06/04/both-required-and-optional.png)

*Sephora’s iOS app marked both the required and the optional fields.*

## How About Login Forms?

Login forms are short and traditionally composed of two fields: the username and the password, both of which are always required. If you’re using the asterisk, the cost of marking these fields as required should be minimal, so you cannot go wrong. However, most users have encountered many, many login forms and they do know that to login you need to enter an email or username and a password. So, if you absolutely hate the asterisk, it’s okay to leave it out in this type of form.

![](https://media.nngroup.com/media/editor/2019/06/04/usps-login-kayak.PNG)

*USPS’s login form (left) marked the two fields as required. Kayak (right) did not mark them. Either design is acceptable for login forms.*

It is, however, dangerous to not mark the required fields in a [registration](https://www.nngroup.com/articles/checklist-registration-login/) form. Registration forms vary a lot across sites — different companies require different types of information when creating an account. If your registration form looks like a login form, it’s safe to leave the required information out. But if it does include more than the username and the password fields, mark all required fields (including the username and password ones).

![registratin forms includes fields First name, last name, email address, password (all marked with an asterisk)](https://media.nngroup.com/media/editor/2019/06/04/sephora-register.png)

*Sephora’s registration form (on desktop) marked the required fields (included the email and password). (Unfortunately, the site violated other usability guidelines — in particular, it showed  [field labels inside the fields](https://www.nngroup.com/articles/form-design-placeholders/) and it had the*Subscribe*checkbox automatically selected.)*

## Conclusion

Forms are no fun. They require users to do a lot of work. In fact, many forms end up being abandoned because filling them in is too hard or too tedious. To increase the chance that your form will get completed, minimize the effort that your users will have to put in and the information that they need to remember. There are many aspects that contribute to these, but marking the required fields (and, optionally, the optional ones) is an easy one to address.

## A Note on Accessibility

After this article was published, we received a few questions about the accessibility of the asterisk as a required-field marker. In HTML 5, it is possible to [add markup to the form field to instruct screen readers to say the word "required"](https://dequeuniversity.com/tips/identify-required-elements) whenever they encounter an asterisk next to the field label.

## Related Courses

- [#### Web Page UX Design

  Strategically combine content, visuals, and interactive components to design successful web pages

  Interaction](/courses/web-page-design/?lm=required-fields&pt=article)
- [#### The Human Mind and Usability

  Use psychology to predict and explain how your customers think and act

  Interaction](/courses/human-mind/?lm=required-fields&pt=article)

forms,Web Usability

## Related Topics

- Web Usability
  [Web Usability](/topic/web-usability/)

## Learn More:

[![Marking Required Fields in Online Forms](https://media.nngroup.com/media/videos/thumbnails/Marking_Required_Fields_in_Online_Forms_Thumbnail.jpg.1300x728_q75_autocrop_crop-smart_upscale.jpg)](https://www.youtube.com/watch?v=h8qL5ToR6oY "Marking Required Fields in Online Forms on YouTube (new window)")

Enable cookies
 to watch NN/g videos

Marking Required Fields in Online Forms

 Raluca Budiu
·
3 min

- [![](https://media.nngroup.com/media/videos/thumbnails/Semantic_Differential_Scales-_Measure_User_Attitudes_with_Nuance_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Semantic Differential Scales: Measure User Attitudes with Nuance

  Rachel Banawa
  ·
  4 min](/videos/semantic-differential-scales/?lm=required-fields&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Checkbox_Design_8_Guidelines_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Checkbox Design: 8 Guidelines

  Maddie Brown
  ·
  3 min](/videos/checkbox-design-guidelines/?lm=required-fields&pt=article)
- [![](https://media.nngroup.com/media/videos/thumbnails/Better_Forms_Through_Visual_Organization_Thumbnail.jpg.650x364_q75_autocrop_crop-smart_upscale.jpg)

  Better Forms Through Visual Organization

  Kathryn Whitenton
  ·
  3 min](/videos/better-forms-visual-organization/?lm=required-fields&pt=article)

## Related Articles:

- [Website Forms Usability: Top 10 Recommendations

  Kathryn Whitenton
  ·
  6 min](/articles/web-form-design/?lm=required-fields&pt=article)
- [Reset and Cancel Buttons

  Jakob Nielsen
  ·
  5 min](/articles/reset-and-cancel-buttons/?lm=required-fields&pt=article)
- [Placeholders in Form Fields Are Harmful

  Katie Sherwin
  ·
  6 min](/articles/form-design-placeholders/?lm=required-fields&pt=article)
- [Date-Input Form Fields: UX Design Guidelines

  Angie Li
  ·
  5 min](/articles/date-input/?lm=required-fields&pt=article)
- [Popups: 10 Problematic Trends and Alternatives

  Anna Kaley
  ·
  12 min](/articles/popups/?lm=required-fields&pt=article)
- [Zigzag Image–Text Layouts Make Scanning Less Efficient

  Kim Flaherty
  ·
  11 min](/articles/zigzag-page-layout/?lm=required-fields&pt=article)