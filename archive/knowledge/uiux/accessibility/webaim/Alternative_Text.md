# Alternative Text

Source: https://webaim.org/techniques/alttext/

---

# Alternative Text

You are here: [Home](/) > [Articles](/articles/) > Alternative Text

## Introduction

Alternative text is a textual substitute for non-text content in web pages. This article is focused on [images](/techniques/images), but its principles also apply to multimedia and other non-text content.

Alternative text serves several functions:

- Screen readers announce alternative text in place of images, helping users with visual or certain cognitive disabilities perceive the content and function of the images.
- If an image fails to load or the user has blocked images, the browser will present the alternative text visually in place of the image.
- Search engines use alternative text and factor it into their assessment of the page purpose and content.

Although technology is getting better at recognizing what an image **depicts**, algorithms alone cannot understand what an image **means** within the context of the overall page. A maple leaf might represent Canada, or it might just illustrate the leaf of a tree. Web page authors must provide alternative text that represents the **content** and **function** of their images.

Alternative text can be presented in two ways:

- within the `alt` attribute of the `<img>` element
- within visible body text near the image, or when the text equivalent cannot be presented succinctly, alternative text can be presented on a separate page, linked from either the image or a text link adjacent to the image

Thus, alternative text is about more than just the `alt` attribute.

**Every** image should have an `alt` attribute, even if it's `alt=""` (sometimes called "null" alternative text).

## Context is Everything

Consider this image of Ellen Ochoa:

![example image](media/ellen-ochoa.jpg)

This image may need vastly different alternative text depending on how it is used.

Note

To best present these principles of alternative text, most images within this article have been given `alt="example image"`. However, the content of the images is typically presented within page context.

### Example 1

![example image](media/ellen-ochoa.jpg)

As the first Hispanic woman to go to space, and, later, the first Hispanic director of Johnson Space Center, Ellen Ochoa is widely regarded as a role model.

What would you choose as `alt` text for the image in Example 1?

- "Astronaut Ellen Ochoa"
- "Image of Ellen Ochoa, Astronaut"
- "Ellen Ochoa, the first Hispanic woman to go into space"
- Empty `alt` attribute (`alt=""` )

First, consider its **content** and **function**. An image only has a function if it is linked (or has an `<area>` within a `<map>`), or if it's in a `<button>` . In this case, the image does not have a function.

Assessing and summarizing an image's content can be more difficult. If the image's content is presented within the surrounding text, then `alt=""` may be all that's needed.

In the example above, the image content informs the user that this is Ellen Ochoa. Her mode of dress further conveys that she is an astronaut—which is meaningful, given her achievements.

**Based on this, we recommend `alt="Astronaut Ellen Ochoa"`.**

"Image of Ellen Ochoa, Astronaut" redundantly describes the image as an image.

"Ellen Ochoa, the first Hispanic woman to go into space" includes information that is not part of the image, and is also redundant with the body text.

An empty `alt` attribute is not appropriate either. Even though the body text names Ellen Ochoa, visual users can tell this directly from the content of the image—and so, since the image conveys content, it needs more than an empty `alt` attribute.

Important

The `alt` attribute should **typically**:

- **be accurate and equivalent** in representing content and function.
- **be succinct.** Content (if any) and function (if any) should be presented as succinctly as possible, without sacrificing accuracy. Typically, only a few words are necessary, though rarely a short sentence or two may be appropriate.
- **not be redundant** or provide the same information as text near the image.
- **not include phrases like "image of ..." or "graphic of ...", etc.** This would be redundant since screen readers already announce "graphic" along with the `alt` text. If the fact that an image is a photograph or illustration, etc. is important content, it may be useful to include this in alternative text.

### Example 2

![](media/ellen-ochoa.jpg)  
**Ellen Ochoa, Astronaut**

As the first Hispanic woman to go to space, and, later, the first Hispanic director of Johnson Space Center, Ellen Ochoa is widely regarded as a role model.

What `alt` text would you choose for the image in Example 2?

- "Image"
- "Ellen Ochoa"
- empty `alt` attribute (`alt=""` )

**In this case, the content of the image is presented in adjacent text, so `alt=""` is the best choice.**

"Ellen Ochoa" would be redundant. "Image" provides no useful information.

## Functional Images

Images are often used not only to provide content, but to provide important functions, such as navigation.

### Example 3

[![example image](media/ellen-ochoa.jpg)](//en.wikipedia.org/wiki/Ellen_Ochoa)  
**Ellen Ochoa, Astronaut**

Note that this image is linked (and is the only content within that link). What `alt` text would you choose here?

- "Read More"
- "Astronaut Ellen Ochoa"
- "Wikipedia entry for Ellen Ochoa, Astronaut"
- empty `alt` attribute (`alt=""` )

The image is also a link, so it has a function. Since no adjacent text **within the link** describes the link's function, it must be conveyed within the image `alt` attribute.

**So, `alt="Astronaut Ellen Ochoa"` is the best choice.** A screen reader would typically read "Link, Image, Astronaut Ellen Ochoa. Ellen Ochoa, Astronaut". The redundancy is necessary to adequately describe the function of the linked image, especially if it were to be accessed in isolation from the adjacent text, such as if a screen reader user were navigating by links.

"Wikipedia entry for Ellen Ochoa, Astronaut" provides content other than that conveyed by the image—the fact the link goes to Wikipedia.

"Read More" does not provide enough information, especially out of context.

Empty `alt` text would never be appropriate here. When an image is the **only** content inside a link or button, `alt` text is all that a screen reader has to go on. If it's empty or missing, screen readers might read the image filename or the URL of the linked page in hopes that this may be helpful to the user, but this is not always the case.

This example would be more accessible for all users if both the image and the text caption were contained within one link:

[![example image](media/ellen-ochoa.jpg)  
**Ellen Ochoa, Astronaut**](//en.wikipedia.org/wiki/Ellen_Ochoa)

Now, both the content and function of the linked image are presented as text within the link, so the image would have `alt=""` to avoid redundancy. A screen reader would typically read, "Link, Ellen Ochoa, Astronaut"—much more efficient than above.

When possible, avoid using "link to...", "click here for...", etc. in the `alt` attribute. Screen readers already announce links as links.

### Example 4

[Download the employment application ![example image](media/pdf.gif)](https://webaim.org/techniques/alttext/media/generic_link.htm)

What `alt` text would you choose for the icon image in Example 4? Note that the icon is within the link.

- "Employment application"
- "PDF"
- "PDF icon"
- The content of the image is presented in context, so `alt=""` is appropriate.

**"PDF" is the best choice. This conveys the content of the icon—no more, no less.**

"Employment application" would be redundant. The function ("Download the employment application") is presented within the text of the link, so it does not need to be included again within the `alt` attribute.

"PDF icon" describes what the image looks like, but it is not the most appropriate for this context—"icon" is redundant here. (If this icon were used in a different context, it may be important that the user know that it is an icon.)

Empty `alt` text would omit the important information that the image presents—that the link is to a PDF document.

If the icon alone was linked without the adjacent text, then the `alt` text would need to fully convey the content and function of the link/image combination: `alt="Download the employment application in PDF format"`. "PDF format" alone would not be sufficient for the linked icon, especially if the page includes many PDF links and icons—a screen reader user navigating through the linked icons would hear, "PDF format, PDF format, PDF format..."

## Decorative Images

A "decorative" image is one that...

- does not present important content,
- is used for layout or non-informative purposes, and
- does not have a function (e.g., is not a link).

Decorative images should have `alt=""` .

### Example 5

![example image](media/separator.gif)

What `alt` text would you choose for the horizontal separator image in Example 5?

- "Decorative line"
- "Beginning of footer"
- "Separator"
- `alt=""`

While this image conveys a separation between document sections, it is just a visual reinforcement of a structure that is already presented in text.

**Because the image does not convey additional content, `alt=""` is the most appropriate choice.**

Note

When an image is used only for decorative purposes, it is best to remove the image from the page content and instead define it as a CSS background image. This will remove the need for alternative text entirely, and will remove the image from the semantic and structural flow of the page.

### Example 6

![example image](media/handshake.jpg)Our business promises the best service you will find on the planet. Our team is professionally trained to offer excellent customer service throughout the contract negotiation process.

Customer satisfaction is our top priority and is guaranteed, or your money back.

What would be the appropriate `alt` attribute for the image in Example 6?

- "Handshake"
- "Businessmen shake hands to complete a contract"
- `alt=""`
- "We guarantee our professional services"

**Because the image does not convey relevant or important content, empty `alt` text is best here.** Consider: If the image were deleted, would important content be lost? In this case, probably not. Many images like this force meaningless, redundant, verbose `alt` text on screen reader users even though they don't provide useful content visually.

"Handshake" and "businessmen shake hands to complete a contract" describe the image, but this is superfluous information.

"We guarantee our professional services" is not correct. This is another mistake too commonly seen across the web—using `alt` to inject extraneous information (or information directed to search engines) that doesn't "fit" anywhere else. The coder's rationale may be to err on the side of verbosity—but why err at all?

Note

In many cases you can ask, "if I could not use this image, what would I put in its place?" If the answer is "nothing," then `alt=""` is probably sufficient.

## Advanced Images

In some cases, determining `alt` text is more subjective. User testing—with and without a screen reader—can help you generate some ideas.

### Form image buttons

Form image buttons that merely present rasterized text should be replaced with true text, styled with CSS as desired. If an image cannot be avoided, the image needs an `alt` attribute that describes the function of the button. The `alt` text should describe what the button will do when activated, such as "Search", "Submit", "Register", "Place your order", etc. For instance, `<input type="image" alt="Submit Search">` might be appropriate for an image button on a site search form.

### Image maps

When using a client-side image `<map>` , the main image's `alt` attribute must convey the content that is presented within the image, but that is not presented with the image map hot spots. For instance, a State of New York map that has an `<area>` for each county might have `alt="Counties of New York"`. If the main image does not convey content, but is primarily just a container for the hot spots, then `alt=""` is appropriate.

Each `<area>` *must* also have an equivalent `alt` attribute, because each `<area>` provides a function. For a New York counties image map, each `<area alt>` would contain the name of the county.

By contrast, **server-side** image maps (which pass mouse click coordinates back to the server for interpretation) are not perceivable by screen readers, and are inoperable by keyboard and screen reader users. Server-side image maps should be replaced by client-side image maps.

### CSS images

CSS images should be used for decorative images which do not need alternative text. Images that convey content should not generally be defined in CSS. They should be within the page content. It is not possible to add alternative text directly to CSS or other background images, so when background images do present content, that content must be made accessible within the page markup. If the PDF icon image in Example 4 above were instead presented via a CSS background image, you could use a text replacement technique to present the content within the link:

<a href="application.pdf">Download the Employment Application<span class="pdficon"> (PDF)</span></a>

You would then use CSS to position the "(PDF)" text (the `span class="pdficon"` element) [off-screen](/techniques/css/invisiblecontent/). Sighted users would see the PDF background image and screen reader users would hear the off-screen "(PDF)" text.

### Logos

Many websites link the main branding logo to the home page. Providing alternative text for the image, such as your company name (`alt="Acme Company"`), will usually suffice. The word "logo" (`alt="Acme Company Logo"`) is usually not an important part of the image's content or function. Similarly, it is usually not necessary to indicate that the image links to the home page (`alt="Acme Company home page"`) because this is a common convention—hearing "Link, Graphic, Acme Company" at the top of a web page is sufficient for a screen reader user to know that it is a logo linked to the home page.

### Complex images

When an equivalent alternative for a complex image (chart, graph, map, etc.) will not fit inside a succinct `alt` attribute (perhaps a couple sentences in length), then the alternative must be provided elsewhere. This might be an adjacent data table on the same page, or it might be on a separate web page, linked from the page with the image. The link can be adjacent to the image, or the image itself could be linked to the description page. The alternative text for the image should still describe the general content of the image.

<img src="sales.jpg" alt="Line chart of annual sales data"><br>  
<a href="salesdata.htm">View sales data</a>

Note on `longdesc`

The `longdesc` attribute is deprecated and should not be used. It was an HTML4 attribute that created a reference to a long description page, but was never well supported in screen readers.

#### Example 7

![example image](media/gw2.jpg)

In this painting, the artist Emanuel Leutze used light, color, form, perspective, proportion, and motion to create the composition.

What `alt` text would you choose for the image in Example 7?

- "George Washington"
- "Painting of George Washington"
- "Painting of George Washington crossing the Delaware River"
- "A classic painting demonstrating the use of light and color to create composition."
- "Painting of George Washington crossing the Delaware River. Swirling waves surround the boat where the majestic George Washington looks forward out of the storm and into the rays of light across the river as he leads his wary troops to battle."

The image is not linked, so there is no function. We should then determine if the content of the image is presented in the surrounding text. In this case, it is not (at least not entirely). But this image is more challenging.

"George Washington" is probably inadequate.

"Painting of George Washington" is better, but in this case, it is appropriate to describe the image as a painting, as opposed to a photograph or other image type, but it does not provide enough content to be considered equivalent.

"Painting of George Washington crossing the Delaware River" provides more information that may help the user identify the content itself. Remember that alternative text is not just for users who are blind. Many sighted users would be able to identify the specific painting in question given this description, whereas "George Washington" alone would not be descriptive enough.

The final (verbose) option might be appropriate if the art technique is more important than the subject. It may also be appropriate if a detailed examination of the painting is in order, but this level of detail would probably be better within the body text.

There is no **one** right answer here. The best alternative text will depend on the context and intended content of the image.

### Figure and figcaption

The `<figure>` element, designed to contain an `<img>` and a `<figcaption>`, is self-contained and typically referenced as a single unit from the main flow of the document. A `<figure>` can be separated from the main flow of the document without affecting the document's meaning.

A `<figure>` creates a semantic association with its contained `<figcaption>`, which may provide a summary of or additional information about the figure and/or relate the figure back to the containing document. However, the `<img>` still needs `alt` text—and to prevent redundancy, this information should not be conveyed via the `<figcaption>` .

## Conclusion

Despite being one of the biggest issues affecting web accessibility, we continue to see still divergent and incorrect methods for implementing alternative text on the web. If the development community could fully embrace equivalent alternative text, the web would be a much more accessible place!

*Ellen Ochoa Image Credit: NASA, Public domain, via Wikimedia Commons.*