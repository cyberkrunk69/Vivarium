# How to Meet WCAG (Quickref Reference)

Source: https://www.w3.org/WAI/WCAG22/quickref/

---

Show Sidebar

Loading Loaded

Selected Filters: **WCAG 2.2:** all success criteria and all techniques. [(What did the filter remove?)](#hiddensc)

Clear filters

Expand **all** sections

Share

Link to this view, with the filters you have selected: Shortcut to copy the link: `ctrl`+`C` *or* `⌘``C`

Close

## **Principle 1** – Perceivable

Information and user interface components must be presentable to users in ways they can perceive.

### Guideline **1.1** – Text Alternatives

Provide text alternatives for any non-text content so that it can be changed into other forms people need, such as large print, braille, speech, symbols or simpler language.

All non-text content that is presented to the user has a text alternative that serves the equivalent purpose, except for the situations listed below.

---

- **Controls, Input:** If non-text content is a control or accepts user input, then it has a name that describes its purpose. (Refer to Success Criterion 4.1.2 for additional requirements for controls and content that accepts user input.)- **Time-Based Media:** If non-text content is time-based media, then text alternatives at least provide descriptive identification of the non-text content. (Refer to Guideline 1.2 for additional requirements for media.)- **Test:** If non-text content is a test or exercise that would be invalid if presented in text, then text alternatives at least provide descriptive identification of the non-text content.- **Sensory:** If non-text content is primarily intended to create a specific sensory experience, then text alternatives at least provide descriptive identification of the non-text content.- **CAPTCHA:** If the purpose of non-text content is to confirm that content is being accessed by a person rather than a computer, then text alternatives that identify and describe the purpose of the non-text content are provided, and alternative forms of CAPTCHA using output modes for different types of sensory perception are provided to accommodate different disabilities.- **Decoration, Formatting, Invisible:** If non-text content is pure decoration, is used only for visual formatting, or is not presented to users, then it is implemented in a way that it can be ignored by assistive technology.

[Understanding 1.1.1](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html)

Show Hide techniques and failures for 1.1.1

##### Sufficient Techniques for Success Criterion 1.1.1

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: If a short description can serve the same purpose and present the same information as the non-text content:

- [G94: Providing short text alternative for non-text content that serves the same purpose and presents the same information as the non-text content](https://www.w3.org/WAI/WCAG22/Techniques/general/G94) using one technique from each group outlined below

Short text alternative techniques for Situation A:

- [ARIA6: Using aria-label to provide labels for objects](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA6)- [ARIA10: Using aria-labelledby to provide a text alternative for non-text content](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA10)- [G196: Using a text alternative on one item within a group of images that describes all items in the group](https://www.w3.org/WAI/WCAG22/Techniques/general/G196)- [H2: Combining adjacent image and text links for the same resource](https://www.w3.org/WAI/WCAG22/Techniques/html/H2)- [H37: Using alt attributes on img elements](https://www.w3.org/WAI/WCAG22/Techniques/html/H37)- [H53: Using the body of the object element](https://www.w3.org/WAI/WCAG22/Techniques/html/H53)- [H86: Providing text alternatives for emojis, emoticons, ASCII art, and leetspeak](https://www.w3.org/WAI/WCAG22/Techniques/html/H86)- [PDF1: Applying text alternatives to images with the Alt entry in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF1)

###### Situation B: If a short description can **not** serve the same purpose and present the same information as the non-text content (e.g., a chart or diagram):

- [G95: Providing short text alternatives that provide a brief description of the non-text content](https://www.w3.org/WAI/WCAG22/Techniques/general/G95) using one technique from each group outlined below

Short text alternative techniques for Situation B:

- [ARIA6: Using aria-label to provide labels for objects](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA6)- [ARIA10: Using aria-labelledby to provide a text alternative for non-text content](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA10)- [G196: Using a text alternative on one item within a group of images that describes all items in the group](https://www.w3.org/WAI/WCAG22/Techniques/general/G196)- [H2: Combining adjacent image and text links for the same resource](https://www.w3.org/WAI/WCAG22/Techniques/html/H2)- [H37: Using alt attributes on img elements](https://www.w3.org/WAI/WCAG22/Techniques/html/H37)- [H53: Using the body of the object element](https://www.w3.org/WAI/WCAG22/Techniques/html/H53)- [H86: Providing text alternatives for emojis, emoticons, ASCII art, and leetspeak](https://www.w3.org/WAI/WCAG22/Techniques/html/H86)- [PDF1: Applying text alternatives to images with the Alt entry in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF1)

Long text alternative techniques for Situation B:

- [ARIA15: Using aria-describedby to provide descriptions of images](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA15)- [G73: Providing a long description in another location with a link to it that is immediately adjacent to the non-text content](https://www.w3.org/WAI/WCAG22/Techniques/general/G73)- [G74: Providing a long description in text near the non-text content, with a reference to the location of the long description in the short description](https://www.w3.org/WAI/WCAG22/Techniques/general/G74)- [G92: Providing long description for non-text content that serves the same purpose and presents the same information](https://www.w3.org/WAI/WCAG22/Techniques/general/G92)- [H53: Using the body of the object element](https://www.w3.org/WAI/WCAG22/Techniques/html/H53)

###### Situation C: If non-text content is a control or accepts user input:

- [G82: Providing a text alternative that identifies the purpose of the non-text content](https://www.w3.org/WAI/WCAG22/Techniques/general/G82) using one technique from each group outlined below

Text alternative techniques for controls and input for Situation C:

- [ARIA6: Using aria-label to provide labels for objects](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA6)- [ARIA9: Using aria-labelledby to concatenate a label from several text nodes](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA9)- [H24: Providing text alternatives for the area elements of image maps](https://www.w3.org/WAI/WCAG22/Techniques/html/H24)- [H30: Providing link text that describes the purpose of a link for anchor elements](https://www.w3.org/WAI/WCAG22/Techniques/html/H30)- [H36: Using alt attributes on images used as submit buttons](https://www.w3.org/WAI/WCAG22/Techniques/html/H36)- [H44: Using label elements to associate text labels with form controls](https://www.w3.org/WAI/WCAG22/Techniques/html/H44)- [H65: Using the title attribute to identify form controls when the label element cannot be used](https://www.w3.org/WAI/WCAG22/Techniques/html/H65)

###### Situation D: If non-text content is time-based media (including live video-only and live audio-only); a test or exercise that would be invalid if presented in text; or primarily intended to create a specific sensory experience:

- Providing a descriptive label using one technique from each group outlined below- [G68: Providing a short text alternative that describes the purpose of live audio-only and live video-only content](https://www.w3.org/WAI/WCAG22/Techniques/general/G68) using one technique from each group outlined below- [G100: Providing a short text alternative which is the accepted name or a descriptive name of the non-text content](https://www.w3.org/WAI/WCAG22/Techniques/general/G100) using one technique from each group outlined below

Short text alternative techniques for Situation D:

- [ARIA6: Using aria-label to provide labels for objects](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA6)- [ARIA10: Using aria-labelledby to provide a text alternative for non-text content](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA10)- [G196: Using a text alternative on one item within a group of images that describes all items in the group](https://www.w3.org/WAI/WCAG22/Techniques/general/G196)- [H2: Combining adjacent image and text links for the same resource](https://www.w3.org/WAI/WCAG22/Techniques/html/H2)- [H37: Using alt attributes on img elements](https://www.w3.org/WAI/WCAG22/Techniques/html/H37)- [H53: Using the body of the object element](https://www.w3.org/WAI/WCAG22/Techniques/html/H53)- [H86: Providing text alternatives for emojis, emoticons, ASCII art, and leetspeak](https://www.w3.org/WAI/WCAG22/Techniques/html/H86)- [PDF1: Applying text alternatives to images with the Alt entry in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF1)

###### Situation E: If non-text content is a CAPTCHA:

- [G143: Providing a text alternative that describes the purpose of the CAPTCHA](https://www.w3.org/WAI/WCAG22/Techniques/general/G143) **AND** [G144: Ensuring that the web page contains another CAPTCHA serving the same purpose using a different modality](https://www.w3.org/WAI/WCAG22/Techniques/general/G144)

###### Situation F: If the non-text content should be ignored by assistive technology:

- Implementing or marking the non-text content so that it will be ignored by assistive technology using one technique from each group outlined below

Techniques to indicate that text alternatives are not required for Situation F:

- [C9: Using CSS to include decorative images](https://www.w3.org/WAI/WCAG22/Techniques/css/C9)- [H67: Using null alt text and no title attribute on img elements for images that assistive technology should ignore](https://www.w3.org/WAI/WCAG22/Techniques/html/H67)- [PDF4: Hiding decorative images with the Artifact tag in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF4)

##### Advisory Techniques for Success Criterion 1.1.1

- [C18: Using CSS margin and padding rules instead of spacer images for layout design](https://www.w3.org/WAI/WCAG22/Techniques/css/C18)

##### Failures for Success Criterion 1.1.1

- [F3: Failure of Success Criterion 1.1.1 due to using CSS to include images that convey important information](https://www.w3.org/WAI/WCAG22/Techniques/failures/F3)- [F13: Failure of Success Criterion 1.1.1 and 1.4.1 due to having a text alternative that does not include information that is conveyed by color differences in the image](https://www.w3.org/WAI/WCAG22/Techniques/failures/F13)- [F20: Failure of Success Criterion 1.1.1 and 4.1.2 due to not updating text alternatives when changes to non-text content occur](https://www.w3.org/WAI/WCAG22/Techniques/failures/F20)- [F30: Failure of Success Criterion 1.1.1 and 1.2.1 due to using text alternatives that are not alternatives (e.g., filenames or placeholder text)](https://www.w3.org/WAI/WCAG22/Techniques/failures/F30)- [F38: Failure of Success Criterion 1.1.1 due to not marking up decorative images in HTML in a way that allows assistive technology to ignore them](https://www.w3.org/WAI/WCAG22/Techniques/failures/F38)- [F39: Failure of Success Criterion 1.1.1 due to providing a text alternative that is not null (e.g., alt="spacer" or alt="image") for images that should be ignored by assistive technology](https://www.w3.org/WAI/WCAG22/Techniques/failures/F39)- [F65: Failure of Success Criterion 1.1.1 due to omitting the alt attribute or text alternative on img elements, area elements, and input elements of type "image"](https://www.w3.org/WAI/WCAG22/Techniques/failures/F65)- [F67: Failure of Success Criterion 1.1.1 and 1.2.1 due to providing long descriptions for non-text content that does not serve the same purpose or does not present the same information](https://www.w3.org/WAI/WCAG22/Techniques/failures/F67)- [F71: Failure of Success Criterion 1.1.1 due to using text look-alikes to represent text without providing a text alternative](https://www.w3.org/WAI/WCAG22/Techniques/failures/F71)- [F72: Failure of Success Criterion 1.1.1 due to using ASCII art without providing a text alternative](https://www.w3.org/WAI/WCAG22/Techniques/failures/F72)

### Guideline **1.2** – Time-based Media

Provide alternatives for time-based media.

For prerecorded audio-only and prerecorded video-only media, the following are true, except when the audio or video is a media alternative for text and is clearly labeled as such:

---

- **Prerecorded Audio-only:** An alternative for time-based media is provided that presents equivalent information for prerecorded audio-only content.- **Prerecorded Video-only:** Either an alternative for time-based media or an audio track is provided that presents equivalent information for prerecorded video-only content.

[Understanding 1.2.1](https://www.w3.org/WAI/WCAG22/Understanding/audio-only-and-video-only-prerecorded.html)

Show Hide techniques and failures for 1.2.1

##### Sufficient Techniques for Success Criterion 1.2.1

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: If the content is prerecorded audio-only:

- [G158: Providing an alternative for time-based media for audio-only content](https://www.w3.org/WAI/WCAG22/Techniques/general/G158)

###### Situation B: If the content is prerecorded video-only:

- [G159: Providing an alternative for time-based media for video-only content](https://www.w3.org/WAI/WCAG22/Techniques/general/G159)- [G166: Providing audio that describes the important video content and describing it as such](https://www.w3.org/WAI/WCAG22/Techniques/general/G166)

##### Advisory Techniques for Success Criterion 1.2.1

- [H96: Using the track element to provide audio descriptions](https://www.w3.org/WAI/WCAG22/Techniques/html/H96)

##### Failures for Success Criterion 1.2.1

- [F30: Failure of Success Criterion 1.1.1 and 1.2.1 due to using text alternatives that are not alternatives (e.g., filenames or placeholder text)](https://www.w3.org/WAI/WCAG22/Techniques/failures/F30)- [F67: Failure of Success Criterion 1.1.1 and 1.2.1 due to providing long descriptions for non-text content that does not serve the same purpose or does not present the same information](https://www.w3.org/WAI/WCAG22/Techniques/failures/F67)

Captions are provided for all prerecorded audio content in synchronized media, except when the media is a media alternative for text and is clearly labeled as such.

[Understanding 1.2.2](https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html)

Show Hide techniques and failures for 1.2.2

##### Sufficient Techniques for Success Criterion 1.2.2

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G93: Providing open (always visible) captions](https://www.w3.org/WAI/WCAG22/Techniques/general/G93)- [G87: Providing closed captions](https://www.w3.org/WAI/WCAG22/Techniques/general/G87) using any of the following techniques:
    - [SM11: Providing captions through synchronized text streams in SMIL 1.0](https://www.w3.org/WAI/WCAG22/Techniques/smil/SM11)- [SM12: Providing captions through synchronized text streams in SMIL 2.0](https://www.w3.org/WAI/WCAG22/Techniques/smil/SM12)- [H95: Using the track element to provide captions](https://www.w3.org/WAI/WCAG22/Techniques/html/H95)- Using any readily available media format that has a video player that supports closed captioning

##### Failures for Success Criterion 1.2.2

- [F8: Failure of Success Criterion 1.2.2 due to captions omitting some dialogue or important sound effects](https://www.w3.org/WAI/WCAG22/Techniques/failures/F8)- [F75: Failure of Success Criterion 1.2.2 by providing synchronized media without captions when the synchronized media presents more information than is presented on the page](https://www.w3.org/WAI/WCAG22/Techniques/failures/F75)- [F74: Failure of Success Criterion 1.2.2 and 1.2.8 due to not labeling a synchronized media alternative to text as an alternative](https://www.w3.org/WAI/WCAG22/Techniques/failures/F74)

An alternative for time-based media or audio description of the prerecorded video content is provided for synchronized media, except when the media is a media alternative for text and is clearly labeled as such.

[Understanding 1.2.3](https://www.w3.org/WAI/WCAG22/Understanding/audio-description-or-media-alternative-prerecorded.html)

Show Hide techniques and failures for 1.2.3

##### Sufficient Techniques for Success Criterion 1.2.3

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G69: Providing an alternative for time based media](https://www.w3.org/WAI/WCAG22/Techniques/general/G69) using one of the following techniques:
  - [G58: Placing a link to the alternative for time-based media immediately next to the non-text content](https://www.w3.org/WAI/WCAG22/Techniques/general/G58)- Linking to the alternative for time-based media using one of the following techniques:
    - [H53: Using the body of the object element](https://www.w3.org/WAI/WCAG22/Techniques/html/H53)- [G78: Providing a second, user-selectable, audio track that includes audio descriptions](https://www.w3.org/WAI/WCAG22/Techniques/general/G78)- [G173: Providing a version of a movie with audio descriptions](https://www.w3.org/WAI/WCAG22/Techniques/general/G173) using one of the following techniques:
        - [SM6: Providing audio description in SMIL 1.0](https://www.w3.org/WAI/WCAG22/Techniques/smil/SM6)- [SM7: Providing audio description in SMIL 2.0](https://www.w3.org/WAI/WCAG22/Techniques/smil/SM7)- [G226: Providing audio descriptions by incorporating narration in the soundtrack](https://www.w3.org/WAI/WCAG22/Techniques/general/G226)- Using any player that supports audio and video- [G8: Providing a movie with extended audio descriptions](https://www.w3.org/WAI/WCAG22/Techniques/general/G8) using one of the following techniques:
          - [SM1: Adding extended audio description in SMIL 1.0](https://www.w3.org/WAI/WCAG22/Techniques/smil/SM1)- [SM2: Adding extended audio description in SMIL 2.0](https://www.w3.org/WAI/WCAG22/Techniques/smil/SM2)- Using any player that supports audio and video- [G203: Using a static text alternative to describe a talking head video](https://www.w3.org/WAI/WCAG22/Techniques/general/G203)

##### Advisory Techniques for Success Criterion 1.2.3

- [H96: Using the track element to provide audio descriptions](https://www.w3.org/WAI/WCAG22/Techniques/html/H96)

Captions are provided for all live audio content in synchronized media.

[Understanding 1.2.4](https://www.w3.org/WAI/WCAG22/Understanding/captions-live.html)

Show Hide techniques and failures for 1.2.4

##### Sufficient Techniques for Success Criterion 1.2.4

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G9: Creating captions for live synchronized media](https://www.w3.org/WAI/WCAG22/Techniques/general/G9) **AND** [G93: Providing open (always visible) captions](https://www.w3.org/WAI/WCAG22/Techniques/general/G93)- [G9: Creating captions for live synchronized media](https://www.w3.org/WAI/WCAG22/Techniques/general/G9) **AND** [G87: Providing closed captions](https://www.w3.org/WAI/WCAG22/Techniques/general/G87)
    - [SM11: Providing captions through synchronized text streams in SMIL 1.0](https://www.w3.org/WAI/WCAG22/Techniques/smil/SM11)- [SM12: Providing captions through synchronized text streams in SMIL 2.0](https://www.w3.org/WAI/WCAG22/Techniques/smil/SM12)- Using any readily available media format that has a video player that supports closed captioning

*Note:* Captions may be generated using real-time text translation service.

Audio description is provided for all prerecorded video content in synchronized media.

[Understanding 1.2.5](https://www.w3.org/WAI/WCAG22/Understanding/audio-description-prerecorded.html)

Show Hide techniques and failures for 1.2.5

##### Sufficient Techniques for Success Criterion 1.2.5

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G78: Providing a second, user-selectable, audio track that includes audio descriptions](https://www.w3.org/WAI/WCAG22/Techniques/general/G78)- [G173: Providing a version of a movie with audio descriptions](https://www.w3.org/WAI/WCAG22/Techniques/general/G173) using one of the following techniques:
    - [SM6: Providing audio description in SMIL 1.0](https://www.w3.org/WAI/WCAG22/Techniques/smil/SM6)- [SM7: Providing audio description in SMIL 2.0](https://www.w3.org/WAI/WCAG22/Techniques/smil/SM7)- [G226: Providing audio descriptions by incorporating narration in the soundtrack](https://www.w3.org/WAI/WCAG22/Techniques/general/G226)- Using any player that supports audio and video- [G8: Providing a movie with extended audio descriptions](https://www.w3.org/WAI/WCAG22/Techniques/general/G8) using one of the following techniques:
      - [SM1: Adding extended audio description in SMIL 1.0](https://www.w3.org/WAI/WCAG22/Techniques/smil/SM1)- [SM2: Adding extended audio description in SMIL 2.0](https://www.w3.org/WAI/WCAG22/Techniques/smil/SM2)- Using any player that supports audio and video- [G203: Using a static text alternative to describe a talking head video](https://www.w3.org/WAI/WCAG22/Techniques/general/G203)

##### Advisory Techniques for Success Criterion 1.2.5

- [H96: Using the track element to provide audio descriptions](https://www.w3.org/WAI/WCAG22/Techniques/html/H96)

##### Failures for Success Criterion 1.2.5

- [F113: Failure of Success Criterion 1.2.5 due to not using available pauses in dialogue to provide audio descriptions of important visual content](https://www.w3.org/WAI/WCAG22/Techniques/failures/F113)

Sign language interpretation is provided for all prerecorded audio content in synchronized media.

[Understanding 1.2.6](https://www.w3.org/WAI/WCAG22/Understanding/sign-language-prerecorded.html)

Show Hide techniques and failures for 1.2.6

##### Sufficient Techniques for Success Criterion 1.2.6

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G54: Including a sign language interpreter in the video stream](https://www.w3.org/WAI/WCAG22/Techniques/general/G54)- [G81: Providing a synchronized video of the sign language interpreter that can be displayed in a different viewport or overlaid on the image by the player](https://www.w3.org/WAI/WCAG22/Techniques/general/G81) using one of the following techniques:
    - [SM13: Providing sign language interpretation through synchronized video streams in SMIL 1.0](https://www.w3.org/WAI/WCAG22/Techniques/smil/SM13)- [SM14: Providing sign language interpretation through synchronized video streams in SMIL 2.0](https://www.w3.org/WAI/WCAG22/Techniques/smil/SM14)

Where pauses in foreground audio are insufficient to allow audio descriptions to convey the sense of the video, extended audio description is provided for all prerecorded video content in synchronized media.

[Understanding 1.2.7](https://www.w3.org/WAI/WCAG22/Understanding/extended-audio-description-prerecorded.html)

Show Hide techniques and failures for 1.2.7

##### Sufficient Techniques for Success Criterion 1.2.7

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G8: Providing a movie with extended audio descriptions](https://www.w3.org/WAI/WCAG22/Techniques/general/G8) using one of the following techniques:
  - [SM1: Adding extended audio description in SMIL 1.0](https://www.w3.org/WAI/WCAG22/Techniques/smil/SM1)- [SM2: Adding extended audio description in SMIL 2.0](https://www.w3.org/WAI/WCAG22/Techniques/smil/SM2)- Using any player that supports audio and video

##### Advisory Techniques for Success Criterion 1.2.7

- [H96: Using the track element to provide audio descriptions](https://www.w3.org/WAI/WCAG22/Techniques/html/H96)

An alternative for time-based media is provided for all prerecorded synchronized media and for all prerecorded video-only media.

[Understanding 1.2.8](https://www.w3.org/WAI/WCAG22/Understanding/media-alternative-prerecorded.html)

Show Hide techniques and failures for 1.2.8

##### Sufficient Techniques for Success Criterion 1.2.8

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: If the content is prerecorded synchronized media:

- [G69: Providing an alternative for time based media](https://www.w3.org/WAI/WCAG22/Techniques/general/G69) using one of the following techniques:
  - [G58: Placing a link to the alternative for time-based media immediately next to the non-text content](https://www.w3.org/WAI/WCAG22/Techniques/general/G58)- Linking to the alternative for time-based media using one of the following techniques:
    - [H53: Using the body of the object element](https://www.w3.org/WAI/WCAG22/Techniques/html/H53)

###### Situation B: If the content is prerecorded video-only:

- [G159: Providing an alternative for time-based media for video-only content](https://www.w3.org/WAI/WCAG22/Techniques/general/G159)

##### Failures for Success Criterion 1.2.8

- [F74: Failure of Success Criterion 1.2.2 and 1.2.8 due to not labeling a synchronized media alternative to text as an alternative](https://www.w3.org/WAI/WCAG22/Techniques/failures/F74)

An alternative for time-based media that presents equivalent information for live audio-only content is provided.

[Understanding 1.2.9](https://www.w3.org/WAI/WCAG22/Understanding/audio-only-live.html)

Show Hide techniques and failures for 1.2.9

##### Sufficient Techniques for Success Criterion 1.2.9

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G151: Providing a link to a text transcript of a prepared statement or script if the script is followed](https://www.w3.org/WAI/WCAG22/Techniques/general/G151)- [G150: Providing text based alternatives for live audio-only content](https://www.w3.org/WAI/WCAG22/Techniques/general/G150)- [G157: Incorporating a live audio captioning service into a web page](https://www.w3.org/WAI/WCAG22/Techniques/general/G157)

### Guideline **1.3** – Adaptable

Create content that can be presented in different ways (for example simpler layout) without losing information or structure.

Information, structure, and relationships conveyed through presentation can be programmatically determined or are available in text.

[Understanding 1.3.1](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html)

Show Hide techniques and failures for 1.3.1

##### Sufficient Techniques for Success Criterion 1.3.1

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: The technology provides semantic structure to make information and relationships conveyed through presentation programmatically determinable:

- [ARIA11: Using ARIA landmarks to identify regions of a page](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA11)- [H101: Using semantic HTML elements to identify regions of a page](https://www.w3.org/WAI/WCAG22/Techniques/html/H101)- [ARIA12: Using role=heading to identify headings](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA12)- [ARIA13: Using aria-labelledby to name regions and landmarks](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA13)- [ARIA16: Using aria-labelledby to provide a name for user interface controls](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA16)- [ARIA17: Using grouping roles to identify related form controls](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA17)- [ARIA20: Using the region role to identify a region of the page](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA20)- [G115: Using semantic elements to mark up structure](https://www.w3.org/WAI/WCAG22/Techniques/general/G115) **AND** [H49: Using semantic markup to mark emphasized or special text](https://www.w3.org/WAI/WCAG22/Techniques/html/H49)- [G117: Using text to convey information that is conveyed by variations in presentation of text](https://www.w3.org/WAI/WCAG22/Techniques/general/G117)- [G140: Separating information and structure from presentation to enable different presentations](https://www.w3.org/WAI/WCAG22/Techniques/general/G140)- [ARIA24: Semantically identifying a font icon with role="img"](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA24)- Making information and relationships conveyed through presentation programmatically determinable using the following techniques:
                        - [G138: Using semantic markup whenever color cues are used](https://www.w3.org/WAI/WCAG22/Techniques/general/G138)- [H51: Using table markup to present tabular information](https://www.w3.org/WAI/WCAG22/Techniques/html/H51)- [PDF6: Using table elements for table markup in PDF Documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF6)- [PDF20: Using Adobe Acrobat Pro's Table Editor to repair mistagged tables](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF20)- [H39: Using caption elements to associate data table captions with data tables](https://www.w3.org/WAI/WCAG22/Techniques/html/H39)- [H63: Using the scope attribute to associate header cells with data cells in data tables](https://www.w3.org/WAI/WCAG22/Techniques/html/H63)- [H43: Using id and headers attributes to associate data cells with header cells in data tables](https://www.w3.org/WAI/WCAG22/Techniques/html/H43)- [H44: Using label elements to associate text labels with form controls](https://www.w3.org/WAI/WCAG22/Techniques/html/H44)- [H65: Using the title attribute to identify form controls when the label element cannot be used](https://www.w3.org/WAI/WCAG22/Techniques/html/H65)- [PDF10: Providing labels for interactive form controls in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF10)- [PDF12: Providing name, role, value information for form fields in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF12)- [H71: Providing a description for groups of form controls using fieldset and legend elements](https://www.w3.org/WAI/WCAG22/Techniques/html/H71)- [H85: Using optgroup to group option elements inside a select](https://www.w3.org/WAI/WCAG22/Techniques/html/H85)- [H48: Using ol, ul and dl for lists or groups of links](https://www.w3.org/WAI/WCAG22/Techniques/html/H48)- [H42: Using h1-h6 to identify headings](https://www.w3.org/WAI/WCAG22/Techniques/html/H42)- [PDF9: Providing headings by marking content with heading tags in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF9)- [PDF11: Providing links and link text using the Link annotation and the /Link structure element in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF11)- [PDF17: Specifying consistent page numbering for PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF17)- [PDF21: Using List tags for lists in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF21)- [H97: Grouping related links using the nav element](https://www.w3.org/WAI/WCAG22/Techniques/html/H97)

###### Situation B: The technology in use does NOT provide the semantic structure to make the information and relationships conveyed through presentation programmatically determinable:

- [G117: Using text to convey information that is conveyed by variations in presentation of text](https://www.w3.org/WAI/WCAG22/Techniques/general/G117)- Making information and relationships conveyed through presentation programmatically determinable or available in text using the following techniques:
    - [T1: Using standard text formatting conventions for paragraphs](https://www.w3.org/WAI/WCAG22/Techniques/text/T1)- [T2: Using standard text formatting conventions for lists](https://www.w3.org/WAI/WCAG22/Techniques/text/T2)- [T3: Using standard text formatting conventions for headings](https://www.w3.org/WAI/WCAG22/Techniques/text/T3)

##### Advisory Techniques for Success Criterion 1.3.1

- [C22: Using CSS to control visual presentation of text](https://www.w3.org/WAI/WCAG22/Techniques/css/C22)- [G162: Positioning labels to maximize predictability of relationships](https://www.w3.org/WAI/WCAG22/Techniques/general/G162)- [ARIA1: Using the aria-describedby property to provide a descriptive label for user interface controls](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA1)- [ARIA2: Identifying a required field with the aria-required property](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA2)- [G141: Organizing a page using headings](https://www.w3.org/WAI/WCAG22/Techniques/general/G141)

##### Failures for Success Criterion 1.3.1

- [F2: Failure of Success Criterion 1.3.1 due to using changes in text presentation to convey information without using the appropriate markup or text](https://www.w3.org/WAI/WCAG22/Techniques/failures/F2)- [F33: Failure of Success Criterion 1.3.1 and 1.3.2 due to using white space characters to create multiple columns in plain text content](https://www.w3.org/WAI/WCAG22/Techniques/failures/F33)- [F34: Failure of Success Criterion 1.3.1 and 1.3.2 due to using white space characters to format tables in plain text content](https://www.w3.org/WAI/WCAG22/Techniques/failures/F34)- [F42: Failure of Success Criteria 1.3.1, 2.1.1, 2.1.3, or 4.1.2 when emulating links](https://www.w3.org/WAI/WCAG22/Techniques/failures/F42)- [F43: Failure of Success Criterion 1.3.1 due to using structural markup in a way that does not represent relationships in the content](https://www.w3.org/WAI/WCAG22/Techniques/failures/F43)- [F46: Failure of Success Criterion 1.3.1 due to using th elements, caption elements, or non-empty summary attributes in layout tables](https://www.w3.org/WAI/WCAG22/Techniques/failures/F46)- [F48: Failure of Success Criterion 1.3.1 due to using the pre element to markup tabular information](https://www.w3.org/WAI/WCAG22/Techniques/failures/F48)- [F90: Failure of Success Criterion 1.3.1 for incorrectly associating table headers and content via the headers and id attributes](https://www.w3.org/WAI/WCAG22/Techniques/failures/F90)- [F91: Failure of Success Criterion 1.3.1 for not correctly marking up table headers](https://www.w3.org/WAI/WCAG22/Techniques/failures/F91)- [F92: Failure of Success Criterion 1.3.1 due to the use of role presentation on content which conveys semantic information](https://www.w3.org/WAI/WCAG22/Techniques/failures/F92)- [F111: Failure of Success Criteria 1.3.1, 2.5.3, and 4.1.2 due to a control with visible label text but no accessible name](https://www.w3.org/WAI/WCAG22/Techniques/failures/F111)

When the sequence in which content is presented affects its meaning, a correct reading sequence can be programmatically determined.

[Understanding 1.3.2](https://www.w3.org/WAI/WCAG22/Understanding/meaningful-sequence.html)

Show Hide techniques and failures for 1.3.2

##### Sufficient Techniques for Success Criterion 1.3.2

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G57: Ordering the content in a meaningful sequence](https://www.w3.org/WAI/WCAG22/Techniques/general/G57) for all the content in the web page- Marking sequences in the content as meaningful using one of the following techniques **AND** [G57: Ordering the content in a meaningful sequence](https://www.w3.org/WAI/WCAG22/Techniques/general/G57) for those sequences
    - [H34: Using a Unicode right-to-left mark (RLM) or left-to-right mark (LRM) to mix text direction inline](https://www.w3.org/WAI/WCAG22/Techniques/html/H34)- [H56: Using the dir attribute on an inline element to resolve problems with nested directional runs](https://www.w3.org/WAI/WCAG22/Techniques/html/H56)- [C6: Positioning content based on structural markup](https://www.w3.org/WAI/WCAG22/Techniques/css/C6)- [C8: Using CSS letter-spacing to control spacing within a word](https://www.w3.org/WAI/WCAG22/Techniques/css/C8)- [C27: Making the DOM order match the visual order](https://www.w3.org/WAI/WCAG22/Techniques/css/C27)- [PDF3: Ensuring correct tab and reading order in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF3)

##### Failures for Success Criterion 1.3.2

- [F34: Failure of Success Criterion 1.3.1 and 1.3.2 due to using white space characters to format tables in plain text content](https://www.w3.org/WAI/WCAG22/Techniques/failures/F34)- [F33: Failure of Success Criterion 1.3.1 and 1.3.2 due to using white space characters to create multiple columns in plain text content](https://www.w3.org/WAI/WCAG22/Techniques/failures/F33)- [F32: Failure of Success Criterion 1.3.2 due to using white space characters to control spacing within a word](https://www.w3.org/WAI/WCAG22/Techniques/failures/F32)- [F49: Failure of Success Criterion 1.3.2 due to using an HTML layout table that does not make sense when linearized](https://www.w3.org/WAI/WCAG22/Techniques/failures/F49)- [F1: Failure of Success Criterion 1.3.2 due to changing the meaning of content by positioning information with CSS](https://www.w3.org/WAI/WCAG22/Techniques/failures/F1)

Instructions provided for understanding and operating content do not rely solely on sensory characteristics of components such as shape, color, size, visual location, orientation, or sound.

*Note:* For requirements related to color, refer to Guideline 1.4.

[Understanding 1.3.3](https://www.w3.org/WAI/WCAG22/Understanding/sensory-characteristics.html)

Show Hide techniques and failures for 1.3.3

##### Sufficient Techniques for Success Criterion 1.3.3

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G96: Providing textual identification of items that otherwise rely only on sensory information to be understood](https://www.w3.org/WAI/WCAG22/Techniques/general/G96)

##### Failures for Success Criterion 1.3.3

- [F14: Failure of Success Criterion 1.3.3 due to identifying content only by its shape or location](https://www.w3.org/WAI/WCAG22/Techniques/failures/F14)- [F26: Failure of Success Criterion 1.3.3 due to using a graphical symbol alone to convey information](https://www.w3.org/WAI/WCAG22/Techniques/failures/F26)

Content does not restrict its view and operation to a single display orientation, such as portrait or landscape, unless a specific display orientation is essential.

*Note:* Examples where a particular display orientation may be essential are a bank check, a piano application, slides for a projector or television, or virtual reality content where content is not necessarily restricted to landscape or portrait display orientation.

[Understanding 1.3.4](https://www.w3.org/WAI/WCAG22/Understanding/orientation.html)

Show Hide techniques and failures for 1.3.4

##### Sufficient Techniques for Success Criterion 1.3.4

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G214: Using a control to allow access to content in different orientations which is otherwise restricted](https://www.w3.org/WAI/WCAG22/Techniques/general/G214)

##### Failures for Success Criterion 1.3.4

- [F97: Failure due to locking the orientation to landscape or portrait view](https://www.w3.org/WAI/WCAG22/Techniques/failures/F97)- [F100: Failure of Success Criterion 1.3.4 due to showing a message asking to reorient device](https://www.w3.org/WAI/WCAG22/Techniques/failures/F100)

The purpose of each input field collecting information about the user can be programmatically determined when:

---

- The input field serves a purpose identified in the Input Purposes for user interface components section; and- The content is implemented using technologies with support for identifying the expected meaning for form input data.

[Understanding 1.3.5](https://www.w3.org/WAI/WCAG22/Understanding/identify-input-purpose.html)

Show Hide techniques and failures for 1.3.5

##### Sufficient Techniques for Success Criterion 1.3.5

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [H98: Using HTML autocomplete attributes](https://www.w3.org/WAI/WCAG22/Techniques/html/H98)

##### Failures for Success Criterion 1.3.5

- [F107: Failure of Success Criterion 1.3.5 due to incorrect autocomplete attribute values](https://www.w3.org/WAI/WCAG22/Techniques/failures/F107)

In content implemented using markup languages, the purpose of user interface components, icons, and regions can be programmatically determined.

[Understanding 1.3.6](https://www.w3.org/WAI/WCAG22/Understanding/identify-purpose.html)

Show Hide techniques and failures for 1.3.6

##### Sufficient Techniques for Success Criterion 1.3.6

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- Programmatically indicating the purpose of icons, regions and user interface components- [ARIA11: Using ARIA landmarks to identify regions of a page](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA11)- Using microdata to markup user interface components (future link)

##### Advisory Techniques for Success Criterion 1.3.6

- Enabling user agents to find the version of the content that best fits their needs- Using semantics to identify important features (e.g., `coga-simplification="simplest"`)- Using `aria-invalid` and `aria-required`

### Guideline **1.4** – Distinguishable

Make it easier for users to see and hear content including separating foreground from background.

Color is not used as the only visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element.

*Note:* This success criterion addresses color perception specifically. Other forms of perception are covered in Guideline 1.3 including programmatic access to color and other visual presentation coding.

[Understanding 1.4.1](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

Show Hide techniques and failures for 1.4.1

##### Sufficient Techniques for Success Criterion 1.4.1

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: If the color of particular words, backgrounds, or other content is used to indicate information:

- [G14: Ensuring that information conveyed by color differences is also available in text](https://www.w3.org/WAI/WCAG22/Techniques/general/G14)- [G205: Including a text cue for colored form control labels](https://www.w3.org/WAI/WCAG22/Techniques/general/G205)- [G182: Ensuring that additional visual cues are available when text color differences are used to convey information](https://www.w3.org/WAI/WCAG22/Techniques/general/G182)- [G183: Using a contrast ratio of 3:1 with surrounding text and providing additional visual cues on hover for links or controls where color alone is used to identify them](https://www.w3.org/WAI/WCAG22/Techniques/general/G183)

###### Situation B: If color is used within an image to convey information:

- [G111: Using color and pattern](https://www.w3.org/WAI/WCAG22/Techniques/general/G111)- [G14: Ensuring that information conveyed by color differences is also available in text](https://www.w3.org/WAI/WCAG22/Techniques/general/G14)

##### Advisory Techniques for Success Criterion 1.4.1

- [C15: Using CSS to change the presentation of a user interface component when it receives focus](https://www.w3.org/WAI/WCAG22/Techniques/css/C15)

##### Failures for Success Criterion 1.4.1

- [F13: Failure of Success Criterion 1.1.1 and 1.4.1 due to having a text alternative that does not include information that is conveyed by color differences in the image](https://www.w3.org/WAI/WCAG22/Techniques/failures/F13)- [F73: Failure of Success Criterion 1.4.1 due to creating links that are not visually evident without color vision](https://www.w3.org/WAI/WCAG22/Techniques/failures/F73)- [F81: Failure of Success Criterion 1.4.1 due to identifying required or error fields using color differences only](https://www.w3.org/WAI/WCAG22/Techniques/failures/F81)

If any audio on a web page plays automatically for more than 3 seconds, either a mechanism is available to pause or stop the audio, or a mechanism is available to control audio volume independently from the overall system volume level.

*Note:* Since any content that does not meet this success criterion can interfere with a user's ability to use the whole page, all content on the web page (whether or not it is used to meet other success criteria) must meet this success criterion. See Conformance Requirement 5: Non-Interference.

[Understanding 1.4.2](https://www.w3.org/WAI/WCAG22/Understanding/audio-control.html)

Show Hide techniques and failures for 1.4.2

##### Sufficient Techniques for Success Criterion 1.4.2

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G60: Playing a sound that turns off automatically within three seconds](https://www.w3.org/WAI/WCAG22/Techniques/general/G60)- [G170: Providing a control near the beginning of the web page that turns off sounds that play automatically](https://www.w3.org/WAI/WCAG22/Techniques/general/G170)- [G171: Playing sounds only on user request](https://www.w3.org/WAI/WCAG22/Techniques/general/G171)

##### Failures for Success Criterion 1.4.2

- [F23: Failure of 1.4.2 due to playing a sound longer than 3 seconds where there is no mechanism to turn it off](https://www.w3.org/WAI/WCAG22/Techniques/failures/F23)- [F93: Failure of Success Criterion 1.4.2 for absence of a way to pause or stop an HTML5 media element that autoplays](https://www.w3.org/WAI/WCAG22/Techniques/failures/F93)

The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following:

---

- **Large Text:** Large-scale text and images of large-scale text have a contrast ratio of at least 3:1;- **Incidental:** Text or images of text that are part of an inactive user interface component, that are pure decoration, that are not visible to anyone, or that are part of a picture that contains significant other visual content, have no contrast requirement.- **Logotypes:** Text that is part of a logo or brand name has no contrast requirement.

[Understanding 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

Show Hide techniques and failures for 1.4.3

##### Sufficient Techniques for Success Criterion 1.4.3

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: text is less than 18 point if not bold and less than 14 point if bold

- [G18: Ensuring that a contrast ratio of at least 4.5:1 exists between text (and images of text) and background behind the text](https://www.w3.org/WAI/WCAG22/Techniques/general/G18)- [G148: Not specifying background color, not specifying text color, and not using technology features that change those defaults](https://www.w3.org/WAI/WCAG22/Techniques/general/G148)- [G174: Providing a control with a sufficient contrast ratio that allows users to switch to a presentation that uses sufficient contrast](https://www.w3.org/WAI/WCAG22/Techniques/general/G174)

###### Situation B: text is at least 18 point if not bold and at least 14 point if bold

- [G145: Ensuring that a contrast ratio of at least 3:1 exists between text (and images of text) and background behind the text](https://www.w3.org/WAI/WCAG22/Techniques/general/G145)- [G148: Not specifying background color, not specifying text color, and not using technology features that change those defaults](https://www.w3.org/WAI/WCAG22/Techniques/general/G148)- [G174: Providing a control with a sufficient contrast ratio that allows users to switch to a presentation that uses sufficient contrast](https://www.w3.org/WAI/WCAG22/Techniques/general/G174)

##### Advisory Techniques for Success Criterion 1.4.3

- [G156: Using a technology that has commonly-available user agents that can change the foreground and background of blocks of text](https://www.w3.org/WAI/WCAG22/Techniques/general/G156)

##### Failures for Success Criterion 1.4.3

- [F24: Failure of Success Criterion 1.4.3, 1.4.6 and 1.4.8 due to specifying foreground colors without specifying background colors or vice versa](https://www.w3.org/WAI/WCAG22/Techniques/failures/F24)- [F83: Failure of Success Criterion 1.4.3 and 1.4.6 due to using background images that do not provide sufficient contrast with foreground text (or images of text)](https://www.w3.org/WAI/WCAG22/Techniques/failures/F83)

Except for captions and images of text, text can be resized without assistive technology up to 200 percent without loss of content or functionality.

[Understanding 1.4.4](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html)

Show Hide techniques and failures for 1.4.4

##### Sufficient Techniques for Success Criterion 1.4.4

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G142: Using a technology that has commonly-available user agents that support zoom](https://www.w3.org/WAI/WCAG22/Techniques/general/G142)- Ensuring that text containers resize when the text resizes **AND** using measurements that are relative to other measurements in the content
    - [C28: Specifying the size of text containers using em units](https://www.w3.org/WAI/WCAG22/Techniques/css/C28)- Techniques for relative measurements
        - [C12: Using percent for font sizes](https://www.w3.org/WAI/WCAG22/Techniques/css/C12)- [C13: Using named font sizes](https://www.w3.org/WAI/WCAG22/Techniques/css/C13)- [C14: Using em units for font sizes](https://www.w3.org/WAI/WCAG22/Techniques/css/C14)- Techniques for text container resizing
          - [SCR34: Calculating size and position in a way that scales with text size](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR34)- [G146: Using liquid layout](https://www.w3.org/WAI/WCAG22/Techniques/general/G146)- [G178: Providing controls on the web page that allow users to incrementally change the size of all text on the page up to 200 percent](https://www.w3.org/WAI/WCAG22/Techniques/general/G178)- [G179: Ensuring that there is no loss of content or functionality when the text resizes and text containers do not change their width](https://www.w3.org/WAI/WCAG22/Techniques/general/G179)

##### Advisory Techniques for Success Criterion 1.4.4

- [C17: Scaling form elements which contain text](https://www.w3.org/WAI/WCAG22/Techniques/css/C17)- [C20: Using relative measurements to set column widths so that lines can average 80 characters or less when the browser is resized](https://www.w3.org/WAI/WCAG22/Techniques/css/C20)- [C22: Using CSS to control visual presentation of text](https://www.w3.org/WAI/WCAG22/Techniques/css/C22)

##### Failures for Success Criterion 1.4.4

- [F69: Failure of Success Criterion 1.4.4 when resizing visually rendered text up to 200 percent causes the text, image or controls to be clipped, truncated or obscured](https://www.w3.org/WAI/WCAG22/Techniques/failures/F69)- [F80: Failure of Success Criterion 1.4.4 when text-based form controls do not resize when visually rendered text is resized up to 200%](https://www.w3.org/WAI/WCAG22/Techniques/failures/F80)- [F94: Failure of Success Criterion 1.4.4 due to incorrect use of viewport units to resize text](https://www.w3.org/WAI/WCAG22/Techniques/failures/F94)

If the technologies being used can achieve the visual presentation, text is used to convey information rather than images of text except for the following:

---

- **Customizable:** The image of text can be visually customized to the user's requirements;- **Essential:** A particular presentation of text is essential to the information being conveyed.

*Note:* Logotypes (text that is part of a logo or brand name) are considered essential.

[Understanding 1.4.5](https://www.w3.org/WAI/WCAG22/Understanding/images-of-text.html)

Show Hide techniques and failures for 1.4.5

##### Sufficient Techniques for Success Criterion 1.4.5

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [C22: Using CSS to control visual presentation of text](https://www.w3.org/WAI/WCAG22/Techniques/css/C22)- [C30: Using CSS to replace text with images of text and providing user interface controls to switch](https://www.w3.org/WAI/WCAG22/Techniques/css/C30)- [G140: Separating information and structure from presentation to enable different presentations](https://www.w3.org/WAI/WCAG22/Techniques/general/G140)- [PDF7: Performing OCR on a scanned PDF document to provide actual text](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF7)

##### Advisory Techniques for Success Criterion 1.4.5

- [C12: Using percent for font sizes](https://www.w3.org/WAI/WCAG22/Techniques/css/C12)- [C13: Using named font sizes](https://www.w3.org/WAI/WCAG22/Techniques/css/C13)- [C14: Using em units for font sizes](https://www.w3.org/WAI/WCAG22/Techniques/css/C14)- [C8: Using CSS letter-spacing to control spacing within a word](https://www.w3.org/WAI/WCAG22/Techniques/css/C8)- [C6: Positioning content based on structural markup](https://www.w3.org/WAI/WCAG22/Techniques/css/C6)

The visual presentation of text and images of text has a contrast ratio of at least 7:1, except for the following:

---

- **Large Text:** Large-scale text and images of large-scale text have a contrast ratio of at least 4.5:1;- **Incidental:** Text or images of text that are part of an inactive user interface component, that are pure decoration, that are not visible to anyone, or that are part of a picture that contains significant other visual content, have no contrast requirement.- **Logotypes:** Text that is part of a logo or brand name has no contrast requirement.

[Understanding 1.4.6](https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html)

Show Hide techniques and failures for 1.4.6

##### Sufficient Techniques for Success Criterion 1.4.6

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: text is less than 18 point if not bold and less than 14 point if bold

- [G17: Ensuring that a contrast ratio of at least 7:1 exists between text (and images of text) and background behind the text](https://www.w3.org/WAI/WCAG22/Techniques/general/G17)- [G148: Not specifying background color, not specifying text color, and not using technology features that change those defaults](https://www.w3.org/WAI/WCAG22/Techniques/general/G148)- [G174: Providing a control with a sufficient contrast ratio that allows users to switch to a presentation that uses sufficient contrast](https://www.w3.org/WAI/WCAG22/Techniques/general/G174)

###### Situation B: text is as least 18 point if not bold and at least 14 point if bold

- [G18: Ensuring that a contrast ratio of at least 4.5:1 exists between text (and images of text) and background behind the text](https://www.w3.org/WAI/WCAG22/Techniques/general/G18)- [G148: Not specifying background color, not specifying text color, and not using technology features that change those defaults](https://www.w3.org/WAI/WCAG22/Techniques/general/G148)- [G174: Providing a control with a sufficient contrast ratio that allows users to switch to a presentation that uses sufficient contrast](https://www.w3.org/WAI/WCAG22/Techniques/general/G174)

##### Advisory Techniques for Success Criterion 1.4.6

- [G156: Using a technology that has commonly-available user agents that can change the foreground and background of blocks of text](https://www.w3.org/WAI/WCAG22/Techniques/general/G156)

##### Failures for Success Criterion 1.4.6

- [F24: Failure of Success Criterion 1.4.3, 1.4.6 and 1.4.8 due to specifying foreground colors without specifying background colors or vice versa](https://www.w3.org/WAI/WCAG22/Techniques/failures/F24)- [F83: Failure of Success Criterion 1.4.3 and 1.4.6 due to using background images that do not provide sufficient contrast with foreground text (or images of text)](https://www.w3.org/WAI/WCAG22/Techniques/failures/F83)

For prerecorded audio-only content that (1) contains primarily speech in the foreground, (2) is not an audio CAPTCHA or audio logo, and (3) is not vocalization intended to be primarily musical expression such as singing or rapping, at least one of the following is true:

---

- **No Background:** The audio does not contain background sounds.- **Turn Off:** The background sounds can be turned off.- **20 dB:** The background sounds are at least 20 decibels lower than the foreground speech content, with the exception of occasional sounds that last for only one or two seconds.

*Note:* Per the definition of "decibel," background sound that meets this requirement will be approximately four times quieter than the foreground speech content.

[Understanding 1.4.7](https://www.w3.org/WAI/WCAG22/Understanding/low-or-no-background-audio.html)

Show Hide techniques and failures for 1.4.7

##### Sufficient Techniques for Success Criterion 1.4.7

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G56: Mixing audio files so that non-speech sounds are at least 20 decibels lower than the speech audio content](https://www.w3.org/WAI/WCAG22/Techniques/general/G56)

For the visual presentation of blocks of text, a mechanism is available to achieve the following:

---

- Foreground and background colors can be selected by the user.- Width is no more than 80 characters or glyphs (40 if CJK).- Text is not justified (aligned to both the left and the right margins).- Line spacing (leading) is at least space-and-a-half within paragraphs, and paragraph spacing is at least 1.5 times larger than the line spacing.- Text can be resized without assistive technology up to 200 percent in a way that does not require the user to scroll horizontally to read a line of text on a full-screen window.

*Note 1:* Content is not required to use these values. The requirement is that a mechanism is available for users to change these presentation aspects. The mechanism can be provided by the browser or other user agent. Content is not required to provide the mechanism.

*Note 2:* Writing systems for some languages use different presentation aspects to improve readability and legibility. If a presentation aspect in this success criterion is not used in a writing system, content in that writing system does not need to use that presentation setting and can conform without it. Authors are encouraged to follow guidance for improving readability and legibility of text in their writing system.

[Understanding 1.4.8](https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html)

Show Hide techniques and failures for 1.4.8

##### Sufficient Techniques for Success Criterion 1.4.8

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### First Requirement: Techniques to ensure foreground and background colors can be selected by the user

- [C23: Specifying text and background colors of secondary content such as banners, features and navigation in CSS while not specifying text and background colors of the main content](https://www.w3.org/WAI/WCAG22/Techniques/css/C23)- [C25: Specifying borders and layout in CSS to delineate areas of a web page while not specifying text and text-background colors](https://www.w3.org/WAI/WCAG22/Techniques/css/C25)- [G156: Using a technology that has commonly-available user agents that can change the foreground and background of blocks of text](https://www.w3.org/WAI/WCAG22/Techniques/general/G156)- [G148: Not specifying background color, not specifying text color, and not using technology features that change those defaults](https://www.w3.org/WAI/WCAG22/Techniques/general/G148)- [G175: Providing a multi color selection tool on the page for foreground and background colors](https://www.w3.org/WAI/WCAG22/Techniques/general/G175)

###### Second Requirement: Techniques to ensure width is no more than 80 characters or glyphs (40 if CJK)

- [G204: Not interfering with the user agent's reflow of text as the viewing window is narrowed](https://www.w3.org/WAI/WCAG22/Techniques/general/G204)- [C20: Using relative measurements to set column widths so that lines can average 80 characters or less when the browser is resized](https://www.w3.org/WAI/WCAG22/Techniques/css/C20)

###### Third Requirement: Techniques to ensure text is not justified (aligned to both the left and the right margins)

- [C19: Specifying alignment either to the left or right in CSS](https://www.w3.org/WAI/WCAG22/Techniques/css/C19)- [G172: Providing a mechanism to remove full justification of text](https://www.w3.org/WAI/WCAG22/Techniques/general/G172)- [G169: Aligning text on only one side](https://www.w3.org/WAI/WCAG22/Techniques/general/G169)

###### Fourth Requirement: Techniques to ensure line spacing (leading) is at least space-and-a-half within paragraphs, and paragraph spacing is at least 1.5 times larger than the line spacing

- [G188: Providing a button on the page to increase line spaces and paragraph spaces](https://www.w3.org/WAI/WCAG22/Techniques/general/G188)- [C21: Specifying line spacing in CSS](https://www.w3.org/WAI/WCAG22/Techniques/css/C21)

###### Fifth Requirement: Techniques to ensure text can be resized without assistive technology up to 200 percent in a way that does not require the user to scroll horizontally to read a line of text on a full-screen window

- [G204: Not interfering with the user agent's reflow of text as the viewing window is narrowed](https://www.w3.org/WAI/WCAG22/Techniques/general/G204)- [G146: Using liquid layout](https://www.w3.org/WAI/WCAG22/Techniques/general/G146) **AND** using measurements that are relative to other measurements in the content
    - [C12: Using percent for font sizes](https://www.w3.org/WAI/WCAG22/Techniques/css/C12)- [C13: Using named font sizes](https://www.w3.org/WAI/WCAG22/Techniques/css/C13)- [C14: Using em units for font sizes](https://www.w3.org/WAI/WCAG22/Techniques/css/C14)- [C24: Using percentage values in CSS for container sizes](https://www.w3.org/WAI/WCAG22/Techniques/css/C24)- [SCR34: Calculating size and position in a way that scales with text size](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR34)- [G206: Providing options within the content to switch to a layout that does not require the user to scroll horizontally to read a line of text](https://www.w3.org/WAI/WCAG22/Techniques/general/G206)

##### Failures for Success Criterion 1.4.8

- [F24: Failure of Success Criterion 1.4.3, 1.4.6 and 1.4.8 due to specifying foreground colors without specifying background colors or vice versa](https://www.w3.org/WAI/WCAG22/Techniques/failures/F24)- [F88: Failure of Success Criterion 1.4.8 due to using text that is justified (aligned to both the left and the right margins)](https://www.w3.org/WAI/WCAG22/Techniques/failures/F88)

Images of text are only used for pure decoration or where a particular presentation of text is essential to the information being conveyed.

*Note:* Logotypes (text that is part of a logo or brand name) are considered essential.

[Understanding 1.4.9](https://www.w3.org/WAI/WCAG22/Understanding/images-of-text-no-exception.html)

Show Hide techniques and failures for 1.4.9

##### Sufficient Techniques for Success Criterion 1.4.9

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [C22: Using CSS to control visual presentation of text](https://www.w3.org/WAI/WCAG22/Techniques/css/C22)- [C30: Using CSS to replace text with images of text and providing user interface controls to switch](https://www.w3.org/WAI/WCAG22/Techniques/css/C30)- [G140: Separating information and structure from presentation to enable different presentations](https://www.w3.org/WAI/WCAG22/Techniques/general/G140)- [PDF7: Performing OCR on a scanned PDF document to provide actual text](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF7)

##### Advisory Techniques for Success Criterion 1.4.9

- [C12: Using percent for font sizes](https://www.w3.org/WAI/WCAG22/Techniques/css/C12)- [C13: Using named font sizes](https://www.w3.org/WAI/WCAG22/Techniques/css/C13)- [C14: Using em units for font sizes](https://www.w3.org/WAI/WCAG22/Techniques/css/C14)- [C8: Using CSS letter-spacing to control spacing within a word](https://www.w3.org/WAI/WCAG22/Techniques/css/C8)- [C6: Positioning content based on structural markup](https://www.w3.org/WAI/WCAG22/Techniques/css/C6)

Content can be presented without loss of information or functionality, and without requiring scrolling in two dimensions for:

---

- Vertical scrolling content at a width equivalent to 320 CSS pixels;- Horizontal scrolling content at a height equivalent to 256 CSS pixels.

Except for parts of the content which require two-dimensional layout for usage or meaning.

*Note 1:* 320 CSS pixels is equivalent to a starting viewport width of 1280 CSS pixels wide at 400% zoom. For web content which is designed to scroll horizontally (e.g., with vertical text), 256 CSS pixels is equivalent to a starting viewport height of 1024 CSS pixels at 400% zoom.

*Note 2:* Examples of content which requires two-dimensional layout are images required for understanding (such as maps and diagrams), video, games, presentations, data tables (not individual cells), and interfaces where it is necessary to keep toolbars in view while manipulating content. It is acceptable to provide two-dimensional scrolling for such parts of the content.

[Understanding 1.4.10](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)

Show Hide techniques and failures for 1.4.10

##### Sufficient Techniques for Success Criterion 1.4.10

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [C32: Using media queries and grid CSS to reflow columns](https://www.w3.org/WAI/WCAG22/Techniques/css/C32)- [C31: Using CSS Flexbox to reflow content](https://www.w3.org/WAI/WCAG22/Techniques/css/C31)- [C33: Allowing for Reflow with Long URLs and Strings of Text](https://www.w3.org/WAI/WCAG22/Techniques/css/C33)- [C38: Using CSS width, max-width and flexbox to fit labels and inputs](https://www.w3.org/WAI/WCAG22/Techniques/css/C38)- [SCR34: Calculating size and position in a way that scales with text size](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR34)- [G206: Providing options within the content to switch to a layout that does not require the user to scroll horizontally to read a line of text](https://www.w3.org/WAI/WCAG22/Techniques/general/G206)- [G224: Accounting for meaningful text indentation and Reflow](https://www.w3.org/WAI/WCAG22/Techniques/general/G224)- [G225: Section panels that scroll horizontally are designed to fit within a width of 320 CSS pixels on a vertically scrolling page](https://www.w3.org/WAI/WCAG22/Techniques/general/G225)- Using PDF/UA when creating PDFs (Potential future technique)

##### Advisory Techniques for Success Criterion 1.4.10

- [C34: Using media queries to un-fixing sticky headers / footers](https://www.w3.org/WAI/WCAG22/Techniques/css/C34)- [C37: Using CSS max-width and height to fit images](https://www.w3.org/WAI/WCAG22/Techniques/css/C37)- CSS, Reflowing simple data tables (Potential future technique)- CSS, Fitting data cells within the width of the viewport (Potential future technique)- Mechanism to allow mobile view at any time (Potential future technique)- Alternate view supporting Reflow for otherwise excepted content (Potential future technique)

##### Failures for Success Criterion 1.4.10

- [F102: Failure of Success Criterion 1.4.10 due to content disappearing and not being available when content has reflowed](https://www.w3.org/WAI/WCAG22/Techniques/failures/F102)

The visual presentation of the following have a contrast ratio of at least 3:1 against adjacent color(s):

---

- **User Interface Components:** Visual information required to identify user interface components and states, except for inactive components or where the appearance of the component is determined by the user agent and not modified by the author;- **Graphical Objects:** Parts of graphics required to understand the content, except when a particular presentation of graphics is essential to the information being conveyed.

[Understanding 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)

Show Hide techniques and failures for 1.4.11

##### Sufficient Techniques for Success Criterion 1.4.11

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: Color is used to identify user interface components or used to identify user interface component states

- [G195: Using an author-supplied, visible focus indicator](https://www.w3.org/WAI/WCAG22/Techniques/general/G195)- [G174: Providing a control with a sufficient contrast ratio that allows users to switch to a presentation that uses sufficient contrast](https://www.w3.org/WAI/WCAG22/Techniques/general/G174)

###### Situation B: Color is required to understand graphical content

- [G207: Ensuring that a contrast ratio of 3:1 is provided for icons](https://www.w3.org/WAI/WCAG22/Techniques/general/G207)- [G209: Provide sufficient contrast at the boundaries between adjoining colors](https://www.w3.org/WAI/WCAG22/Techniques/general/G209)

##### Failures for Success Criterion 1.4.11

- [F78: Failure of Success Criterion 1.4.11, 2.4.7 and 2.4.13 due to styling element outlines and borders in a way that removes or renders non-visible the visual focus indicator](https://www.w3.org/WAI/WCAG22/Techniques/failures/F78)

In content implemented using markup languages that support the following text style properties, no loss of content or functionality occurs by setting all of the following and by changing no other style property:

---

- Line height (line spacing) to at least 1.5 times the font size;- Spacing following paragraphs to at least 2 times the font size;- Letter spacing (tracking) to at least 0.12 times the font size;- Word spacing to at least 0.16 times the font size.

Exception: Human languages and scripts that do not make use of one or more of these text style properties in written text can conform using only the properties that exist for that combination of language and script.

*Note 1:* Content is not required to use these text spacing values. The requirement is to ensure that when a user overrides the authored text spacing, content or functionality is not lost.

*Note 2:* Writing systems for some languages use different text spacing settings, such as paragraph start indent. Authors are encouraged to follow locally available guidance for improving readability and legibility of text in their writing system.

[Understanding 1.4.12](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html)

Show Hide techniques and failures for 1.4.12

##### Sufficient Techniques for Success Criterion 1.4.12

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [C36: Allowing for text spacing override](https://www.w3.org/WAI/WCAG22/Techniques/css/C36)- [C35: Allowing for text spacing without wrapping](https://www.w3.org/WAI/WCAG22/Techniques/css/C35)

##### Advisory Techniques for Success Criterion 1.4.12

- [C8: Using CSS letter-spacing to control spacing within a word](https://www.w3.org/WAI/WCAG22/Techniques/css/C8)- [C21: Specifying line spacing in CSS](https://www.w3.org/WAI/WCAG22/Techniques/css/C21)- [C28: Specifying the size of text containers using em units](https://www.w3.org/WAI/WCAG22/Techniques/css/C28)

##### Failures for Success Criterion 1.4.12

- [F104: Failure of Success Criterion 1.4.12 due to clipped or overlapped content when text spacing is adjusted](https://www.w3.org/WAI/WCAG22/Techniques/failures/F104)

Where receiving and then removing pointer hover or keyboard focus triggers additional content to become visible and then hidden, the following are true:

---

- **Dismissible:** A mechanism is available to dismiss the additional content without moving pointer hover or keyboard focus, unless the additional content communicates an input error or does not obscure or replace other content;- **Hoverable:** If pointer hover can trigger the additional content, then the pointer can be moved over the additional content without the additional content disappearing;- **Persistent:** The additional content remains visible until the hover or focus trigger is removed, the user dismisses it, or its information is no longer valid.

Exception: The visual presentation of the additional content is controlled by the user agent and is not modified by the author.

*Note 1:* Examples of additional content controlled by the user agent include browser tooltips created through use of the HTML title attribute [HTML].

*Note 2:* Custom tooltips, sub-menus, and other nonmodal popups that display on hover and focus are examples of additional content covered by this criterion.

*Note 3:* This criterion applies to content that appears in addition to the triggering component itself. Since hidden components that are made visible on keyboard focus (such as links used to skip to another part of a page) do not present additional content they are not covered by this criterion.

[Understanding 1.4.13](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html)

Show Hide techniques and failures for 1.4.13

##### Sufficient Techniques for Success Criterion 1.4.13

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [SCR39: Making content on focus or hover hoverable, dismissible, and persistent](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR39)- ARIA: Using role="tooltip" (Potential future technique)- CSS: Using hover and focus pseudo classes (Potential future technique)

##### Failures for Success Criterion 1.4.13

- [F95: Failure of Success Criterion 1.4.13 due to content shown on hover not being hoverable](https://www.w3.org/WAI/WCAG22/Techniques/failures/F95)- Failure to make content dismissible without moving pointer hover or keyboard focus (Potential future technique)- Failure to meet by content on hover or focus not remaining visible until dismissed or invalid (Potential future technique)

## **Principle 2** – Operable

User interface components and navigation must be operable.

### Guideline **2.1** – Keyboard Accessible

Make all functionality available from a keyboard.

All functionality of the content is operable through a keyboard interface without requiring specific timings for individual keystrokes, except where the underlying function requires input that depends on the path of the user's movement and not just the endpoints.

*Note 1:* This exception relates to the underlying function, not the input technique. For example, if using handwriting to enter text, the input technique (handwriting) requires path-dependent input but the underlying function (text input) does not.

*Note 2:* This does not forbid and should not discourage providing mouse input or other input methods in addition to keyboard operation.

[Understanding 2.1.1](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html)

Show Hide techniques and failures for 2.1.1

##### Sufficient Techniques for Success Criterion 2.1.1

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G202: Ensuring keyboard control for all functionality](https://www.w3.org/WAI/WCAG22/Techniques/general/G202)- Ensuring keyboard control using one of the following techniques:
    - [H91: Using HTML form controls and links](https://www.w3.org/WAI/WCAG22/Techniques/html/H91)- [PDF3: Ensuring correct tab and reading order in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF3)- [PDF11: Providing links and link text using the Link annotation and the /Link structure element in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF11)- [PDF23: Providing interactive form controls in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF23)- [G90: Providing keyboard-triggered event handlers](https://www.w3.org/WAI/WCAG22/Techniques/general/G90) using one of the following techniques:
      - [SCR20: Using both keyboard and other device-specific functions](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR20)- [SCR35: Making actions keyboard accessible by using the onclick event of anchors and buttons](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR35)- [SCR2: Using redundant keyboard and mouse event handlers](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR2)

##### Advisory Techniques for Success Criterion 2.1.1

- Using WAI-ARIA role, state, and value attributes if repurposing static elements as interactive user interface components (future link) **AND** [SCR29: Adding keyboard-accessible actions to static HTML elements](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR29)

##### Failures for Success Criterion 2.1.1

- [F54: Failure of Success Criterion 2.1.1 due to using only pointing-device-specific event handlers (including gesture) for a function](https://www.w3.org/WAI/WCAG22/Techniques/failures/F54)- [F55: Failure of Success Criteria 2.1.1, 2.4.7, 2.4.13, and 3.2.1 due to using script to remove focus when focus is received](https://www.w3.org/WAI/WCAG22/Techniques/failures/F55)- [F42: Failure of Success Criteria 1.3.1, 2.1.1, 2.1.3, or 4.1.2 when emulating links](https://www.w3.org/WAI/WCAG22/Techniques/failures/F42)

If keyboard focus can be moved to a component of the page using a keyboard interface, then focus can be moved away from that component using only a keyboard interface, and, if it requires more than unmodified arrow or tab keys or other standard exit methods, the user is advised of the method for moving focus away.

*Note:* Since any content that does not meet this success criterion can interfere with a user's ability to use the whole page, all content on the web page (whether it is used to meet other success criteria or not) must meet this success criterion. See Conformance Requirement 5: Non-Interference.

[Understanding 2.1.2](https://www.w3.org/WAI/WCAG22/Understanding/no-keyboard-trap.html)

Show Hide techniques and failures for 2.1.2

##### Sufficient Techniques for Success Criterion 2.1.2

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G21: Ensuring that users are not trapped in content](https://www.w3.org/WAI/WCAG22/Techniques/general/G21)

##### Failures for Success Criterion 2.1.2

- [F10: Failure of Success Criterion 2.1.2 and Conformance Requirement 5 due to combining multiple content formats in a way that traps users inside one format type](https://www.w3.org/WAI/WCAG22/Techniques/failures/F10)

All functionality of the content is operable through a keyboard interface without requiring specific timings for individual keystrokes.

[Understanding 2.1.3](https://www.w3.org/WAI/WCAG22/Understanding/keyboard-no-exception.html)

Show Hide techniques and failures for 2.1.3

##### Sufficient Techniques for Success Criterion 2.1.3

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- No additional techniques exist for this success criterion. Follow [techniques for Success Criterion 2.1.1](https://www.w3.org/WAI/WCAG22/Understanding/keyboard#techniques). If that is not possible because there is a requirement for path-dependent input, then it is not possible to meet this Level AAA success criterion.

If a keyboard shortcut is implemented in content using only letter (including upper- and lower-case letters), punctuation, number, or symbol characters, then at least one of the following is true:

---

- **Turn off:** A mechanism is available to turn the shortcut off;- **Remap:** A mechanism is available to remap the shortcut to include one or more non-printable keyboard keys (e.g., Ctrl, Alt);- **Active only on focus:** The keyboard shortcut for a user interface component is only active when that component has focus.

[Understanding 2.1.4](https://www.w3.org/WAI/WCAG22/Understanding/character-key-shortcuts.html)

Show Hide techniques and failures for 2.1.4

##### Sufficient Techniques for Success Criterion 2.1.4

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G217: Providing a mechanism to allow users to remap or turn off character key shortcuts](https://www.w3.org/WAI/WCAG22/Techniques/general/G217)

##### Failures for Success Criterion 2.1.4

- [F99: Failure of Success Criterion 2.1.4 due to implementing character key shortcuts that cannot be turned off or remapped](https://www.w3.org/WAI/WCAG22/Techniques/failures/F99)

### Guideline **2.2** – Enough Time

Provide users enough time to read and use content.

For each time limit that is set by the content, at least one of the following is true:

---

- **Turn off:** The user is allowed to turn off the time limit before encountering it; or- **Adjust:** The user is allowed to adjust the time limit before encountering it over a wide range that is at least ten times the length of the default setting; or- **Extend:** The user is warned before time expires and given at least 20 seconds to extend the time limit with a simple action (for example, "press the space bar"), and the user is allowed to extend the time limit at least ten times; or- **Real-time Exception:** The time limit is a required part of a real-time event (for example, an auction), and no alternative to the time limit is possible; or- **Essential Exception:** The time limit is essential and extending it would invalidate the activity; or- **20 Hour Exception:** The time limit is longer than 20 hours.

*Note:* This success criterion helps ensure that users can complete tasks without unexpected changes in content or context that are a result of a time limit. This success criterion should be considered in conjunction with Success Criterion 3.2.1, which puts limits on changes of content or context as a result of user action.

[Understanding 2.2.1](https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html)

Show Hide techniques and failures for 2.2.1

##### Sufficient Techniques for Success Criterion 2.2.1

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: If there are session time limits:

- [G133: Providing a checkbox on the first page of a multipart form that allows users to ask for longer session time limit or no session time limit](https://www.w3.org/WAI/WCAG22/Techniques/general/G133)- [G198: Providing a way for the user to turn the time limit off](https://www.w3.org/WAI/WCAG22/Techniques/general/G198)

###### Situation B: If a time limit is controlled by a script on the page:

- [G198: Providing a way for the user to turn the time limit off](https://www.w3.org/WAI/WCAG22/Techniques/general/G198)- [G180: Providing the user with a means to set the time limit to 10 times the default time limit](https://www.w3.org/WAI/WCAG22/Techniques/general/G180)- [SCR16: Providing a script that warns the user a time limit is about to expire](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR16) **AND** [SCR1: Allowing the user to extend the default time limit](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR1)

###### Situation C: If there are time limits on reading:

- [G4: Allowing the content to be paused and restarted from where it was paused](https://www.w3.org/WAI/WCAG22/Techniques/general/G4)- [G198: Providing a way for the user to turn the time limit off](https://www.w3.org/WAI/WCAG22/Techniques/general/G198)- [SCR33: Using script to scroll content, and providing a mechanism to pause it](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR33)- [SCR36: Providing a mechanism to allow users to display moving, scrolling, or auto-updating text in a static window or area](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR36)

##### Failures for Success Criterion 2.2.1

- [F40: Failure due to using meta redirect with a time limit](https://www.w3.org/WAI/WCAG22/Techniques/failures/F40)- [F41: Failure of Success Criterion 2.2.1, 2.2.4, and 3.2.5 due to using meta refresh to reload the page](https://www.w3.org/WAI/WCAG22/Techniques/failures/F41)- [F58: Failure of Success Criterion 2.2.1 due to using server-side techniques to automatically redirect pages after a time-out](https://www.w3.org/WAI/WCAG22/Techniques/failures/F58)

For moving, blinking, scrolling, or auto-updating information, all of the following are true:

---

- **Moving, blinking, scrolling:** For any moving, blinking or scrolling information that (1) starts automatically, (2) lasts more than five seconds, and (3) is presented in parallel with other content, there is a mechanism for the user to pause, stop, or hide it unless the movement, blinking, or scrolling is part of an activity where it is essential; and- **Auto-updating:** For any auto-updating information that (1) starts automatically and (2) is presented in parallel with other content, there is a mechanism for the user to pause, stop, or hide it or to control the frequency of the update unless the auto-updating is part of an activity where it is essential.

*Note 1:* For requirements related to flickering or flashing content, refer to Guideline 2.3.

*Note 2:* Since any content that does not meet this success criterion can interfere with a user's ability to use the whole page, all content on the web page (whether it is used to meet other success criteria or not) must meet this success criterion. See Conformance Requirement 5: Non-Interference.

*Note 3:* Content that is updated periodically by software or that is streamed to the user agent is not required to preserve or present information that is generated or received between the initiation of the pause and resuming presentation, as this may not be technically possible, and in many situations could be misleading to do so.

*Note 4:* An animation that occurs as part of a preload phase or similar situation can be considered essential if interaction cannot occur during that phase for all users and if not indicating progress could confuse users or cause them to think that content was frozen or broken.

[Understanding 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html)

Show Hide techniques and failures for 2.2.2

##### Sufficient Techniques for Success Criterion 2.2.2

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G4: Allowing the content to be paused and restarted from where it was paused](https://www.w3.org/WAI/WCAG22/Techniques/general/G4)- [SCR33: Using script to scroll content, and providing a mechanism to pause it](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR33)- [G11: Creating content that blinks for less than 5 seconds](https://www.w3.org/WAI/WCAG22/Techniques/general/G11)- [G152: Setting animated gif images to stop blinking after n cycles (within 5 seconds)](https://www.w3.org/WAI/WCAG22/Techniques/general/G152)- [SCR22: Using scripts to control blinking and stop it in five seconds or less](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR22)- [G186: Using a control in the web page that stops moving, blinking, or auto-updating content](https://www.w3.org/WAI/WCAG22/Techniques/general/G186)- [G191: Providing a link, button, or other mechanism that reloads the page without any blinking content](https://www.w3.org/WAI/WCAG22/Techniques/general/G191)

##### Failures for Success Criterion 2.2.2

- [F16: Failure of Success Criterion 2.2.2 due to including scrolling content where movement is not essential to the activity without also including a mechanism to pause and restart the content](https://www.w3.org/WAI/WCAG22/Techniques/failures/F16)- [F112: Failure of Success Criterion 2.2.2 due to using blinking content that lasts for more than five seconds without a mechanism to stop it](https://www.w3.org/WAI/WCAG22/Techniques/failures/F112)- [F50: Failure of Success Criterion 2.2.2 due to a script that causes a blink effect without a mechanism to stop the blinking at 5 seconds or less](https://www.w3.org/WAI/WCAG22/Techniques/failures/F50)- [F7: Failure of Success Criterion 2.2.2 due to an object or applet that has blinking content without a mechanism to pause the content that blinks for more than five seconds](https://www.w3.org/WAI/WCAG22/Techniques/failures/F7)

Timing is not an essential part of the event or activity presented by the content, except for non-interactive synchronized media and real-time events.

[Understanding 2.2.3](https://www.w3.org/WAI/WCAG22/Understanding/no-timing.html)

Show Hide techniques and failures for 2.2.3

##### Sufficient Techniques for Success Criterion 2.2.3

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G5: Allowing users to complete an activity without any time limit](https://www.w3.org/WAI/WCAG22/Techniques/general/G5)

Interruptions can be postponed or suppressed by the user, except interruptions involving an emergency.

[Understanding 2.2.4](https://www.w3.org/WAI/WCAG22/Understanding/interruptions.html)

Show Hide techniques and failures for 2.2.4

##### Sufficient Techniques for Success Criterion 2.2.4

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G75: Providing a mechanism to postpone any updating of content](https://www.w3.org/WAI/WCAG22/Techniques/general/G75)- [G76: Providing a mechanism to request an update of the content instead of updating automatically](https://www.w3.org/WAI/WCAG22/Techniques/general/G76)- [SCR14: Using scripts to make nonessential alerts optional](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR14)

##### Failures for Success Criterion 2.2.4

- [F40: Failure due to using meta redirect with a time limit](https://www.w3.org/WAI/WCAG22/Techniques/failures/F40)- [F41: Failure of Success Criterion 2.2.1, 2.2.4, and 3.2.5 due to using meta refresh to reload the page](https://www.w3.org/WAI/WCAG22/Techniques/failures/F41)

When an authenticated session expires, the user can continue the activity without loss of data after re-authenticating.

[Understanding 2.2.5](https://www.w3.org/WAI/WCAG22/Understanding/re-authenticating.html)

Show Hide techniques and failures for 2.2.5

##### Sufficient Techniques for Success Criterion 2.2.5

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- Providing options to continue without loss of data using one of the following techniques:
  - [G105: Saving data so that it can be used after a user re-authenticates](https://www.w3.org/WAI/WCAG22/Techniques/general/G105)- [G181: Encoding user data as hidden or encrypted data in a re-authorization page](https://www.w3.org/WAI/WCAG22/Techniques/general/G181)

*Note:* Refer to Techniques for Addressing Success Criterion 2.2.1 for techniques related to providing notifications about time limits.

##### Failures for Success Criterion 2.2.5

- [F12: Failure of Success Criterion 2.2.5 due to having a session time limit without a mechanism for saving user's input and re-establishing that information upon re-authentication](https://www.w3.org/WAI/WCAG22/Techniques/failures/F12)

Users are warned of the duration of any user inactivity that could cause data loss, unless the data is preserved for more than 20 hours when the user does not take any actions.

*Note:* Privacy regulations may require explicit user consent before user identification has been authenticated and before user data is preserved. In cases where the user is a minor, explicit consent may not be solicited in most jurisdictions, countries or regions. Consultation with privacy professionals and legal counsel is advised when considering data preservation as an approach to satisfy this success criterion.

[Understanding 2.2.6](https://www.w3.org/WAI/WCAG22/Understanding/timeouts.html)

Show Hide techniques and failures for 2.2.6

##### Sufficient Techniques for Success Criterion 2.2.6

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- Setting a session timeout to occur following at least 20 hours of inactivity- Storing user data for more than 20 hours- Providing a warning of the duration of user inactivity at the start of a process

### Guideline **2.3** – Seizures and Physical Reactions

Do not design content in a way that is known to cause seizures or physical reactions.

Web pages do not contain anything that flashes more than three times in any one second period, or the flash is below the general flash and red flash thresholds.

*Note:* Since any content that does not meet this success criterion can interfere with a user's ability to use the whole page, all content on the web page (whether it is used to meet other success criteria or not) must meet this success criterion. See Conformance Requirement 5: Non-Interference.

[Understanding 2.3.1](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html)

Show Hide techniques and failures for 2.3.1

##### Sufficient Techniques for Success Criterion 2.3.1

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G19: Ensuring that no component of the content flashes more than three times in any 1-second period](https://www.w3.org/WAI/WCAG22/Techniques/general/G19)- [G176: Keeping the flashing area small enough](https://www.w3.org/WAI/WCAG22/Techniques/general/G176)- [G15: Using a tool to ensure that content does not violate the general flash threshold or red flash threshold](https://www.w3.org/WAI/WCAG22/Techniques/general/G15)

Web pages do not contain anything that flashes more than three times in any one second period.

[Understanding 2.3.2](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes.html)

Show Hide techniques and failures for 2.3.2

##### Sufficient Techniques for Success Criterion 2.3.2

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G19: Ensuring that no component of the content flashes more than three times in any 1-second period](https://www.w3.org/WAI/WCAG22/Techniques/general/G19)

Motion animation triggered by interaction can be disabled, unless the animation is essential to the functionality or the information being conveyed.

[Understanding 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)

Show Hide techniques and failures for 2.3.3

##### Sufficient Techniques for Success Criterion 2.3.3

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [C39: Using the CSS prefers-reduced-motion query to prevent motion](https://www.w3.org/WAI/WCAG22/Techniques/css/C39)- [SCR40: Using the CSS prefers-reduced-motion query in JavaScript to prevent motion](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR40)- Gx: Allowing users to set a preference that prevents animation

### Guideline **2.4** – Navigable

Provide ways to help users navigate, find content, and determine where they are.

A mechanism is available to bypass blocks of content that are repeated on multiple web pages.

[Understanding 2.4.1](https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html)

Show Hide techniques and failures for 2.4.1

##### Sufficient Techniques for Success Criterion 2.4.1

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- Creating links to skip blocks of repeated material using one of the following techniques:
  - [G1: Adding a link at the top of each page that goes directly to the main content area](https://www.w3.org/WAI/WCAG22/Techniques/general/G1)- [G123: Adding a link at the beginning of a block of repeated content to go to the end of the block](https://www.w3.org/WAI/WCAG22/Techniques/general/G123)- [G124: Adding links at the top of the page to each area of the content](https://www.w3.org/WAI/WCAG22/Techniques/general/G124)- Grouping blocks of repeated material in a way that can be skipped using one of the following techniques:
    - [ARIA11: Using ARIA landmarks to identify regions of a page](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA11)- [H69: Providing heading elements at the beginning of each section of content](https://www.w3.org/WAI/WCAG22/Techniques/html/H69)- [PDF9: Providing headings by marking content with heading tags in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF9)- [H64: Using the title attribute of the iframe element](https://www.w3.org/WAI/WCAG22/Techniques/html/H64)- [SCR28: Using an expandable and collapsible menu to bypass block of content](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR28)

##### Advisory Techniques for Success Criterion 2.4.1

- [C6: Positioning content based on structural markup](https://www.w3.org/WAI/WCAG22/Techniques/css/C6)- [H97: Grouping related links using the nav element](https://www.w3.org/WAI/WCAG22/Techniques/html/H97)

Web pages have titles that describe topic or purpose.

[Understanding 2.4.2](https://www.w3.org/WAI/WCAG22/Understanding/page-titled.html)

Show Hide techniques and failures for 2.4.2

##### Sufficient Techniques for Success Criterion 2.4.2

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G88: Providing descriptive titles for web pages](https://www.w3.org/WAI/WCAG22/Techniques/general/G88) **AND** associating a title with a web page
  - [H25: Providing a title using the title element](https://www.w3.org/WAI/WCAG22/Techniques/html/H25)- [PDF18: Specifying the document title using the Title entry in the document information dictionary of a PDF document](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF18)

##### Advisory Techniques for Success Criterion 2.4.2

- [G127: Identifying a web page's relationship to a larger collection of web pages](https://www.w3.org/WAI/WCAG22/Techniques/general/G127)

##### Failures for Success Criterion 2.4.2

- [F25: Failure of Success Criterion 2.4.2 due to the title of a web page not identifying the contents](https://www.w3.org/WAI/WCAG22/Techniques/failures/F25)

If a web page can be navigated sequentially and the navigation sequences affect meaning or operation, focusable components receive focus in an order that preserves meaning and operability.

[Understanding 2.4.3](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html)

Show Hide techniques and failures for 2.4.3

##### Sufficient Techniques for Success Criterion 2.4.3

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G59: Placing the interactive elements in an order that follows sequences and relationships within the content](https://www.w3.org/WAI/WCAG22/Techniques/general/G59)- Giving focus to elements in an order that follows sequences and relationships within the content using one of the following techniques:
    - [C27: Making the DOM order match the visual order](https://www.w3.org/WAI/WCAG22/Techniques/css/C27)- [PDF3: Ensuring correct tab and reading order in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF3)- Changing a web page dynamically using one of the following techniques:
      - [SCR26: Inserting dynamic content into the Document Object Model immediately following its trigger element](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR26)- [H102: Creating modal dialogs with the HTML dialog element](https://www.w3.org/WAI/WCAG22/Techniques/html/H102)- [SCR27: Reordering page sections using the Document Object Model](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR27)

##### Failures for Success Criterion 2.4.3

- [F44: Failure of Success Criterion 2.4.3 due to using tabindex to create a tab order that does not preserve meaning and operability](https://www.w3.org/WAI/WCAG22/Techniques/failures/F44)- [F85: Failure of Success Criterion 2.4.3 due to using dialogs or menus that are not adjacent to their trigger control in the sequential navigation order](https://www.w3.org/WAI/WCAG22/Techniques/failures/F85)

The purpose of each link can be determined from the link text alone or from the link text together with its programmatically determined link context, except where the purpose of the link would be ambiguous to users in general.

[Understanding 2.4.4](https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-in-context.html)

Show Hide techniques and failures for 2.4.4

##### Sufficient Techniques for Success Criterion 2.4.4

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G91: Providing link text that describes the purpose of a link](https://www.w3.org/WAI/WCAG22/Techniques/general/G91)- [H30: Providing link text that describes the purpose of a link for anchor elements](https://www.w3.org/WAI/WCAG22/Techniques/html/H30)- [H24: Providing text alternatives for the area elements of image maps](https://www.w3.org/WAI/WCAG22/Techniques/html/H24)- Allowing the user to choose short or long link text using one of the following techniques:
        - [G189: Providing a control near the beginning of the web page that changes the link text](https://www.w3.org/WAI/WCAG22/Techniques/general/G189)- [SCR30: Using scripts to change the link text](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR30)- [G53: Identifying the purpose of a link using link text combined with the text of the enclosing sentence](https://www.w3.org/WAI/WCAG22/Techniques/general/G53)- Providing a supplemental description of the purpose of a link using one of the following techniques:
            - [H33: Supplementing link text with the title attribute](https://www.w3.org/WAI/WCAG22/Techniques/html/H33)- [C7: Using CSS to hide a portion of the link text](https://www.w3.org/WAI/WCAG22/Techniques/css/C7)- Identifying the purpose of a link using link text combined with programmatically determined link context using one of the following techniques:
              - [ARIA7: Using aria-labelledby for link purpose](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA7)- [ARIA8: Using aria-label for link purpose](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA8)- [H77: Identifying the purpose of a link using link text combined with its enclosing list item](https://www.w3.org/WAI/WCAG22/Techniques/html/H77)- [H78: Identifying the purpose of a link using link text combined with its enclosing paragraph](https://www.w3.org/WAI/WCAG22/Techniques/html/H78)- [H79: Identifying the purpose of a link in a data table using the link text combined with its enclosing table cell and associated table header cells](https://www.w3.org/WAI/WCAG22/Techniques/html/H79)- [H81: Identifying the purpose of a link in a nested list using link text combined with the parent list item under which the list is nested](https://www.w3.org/WAI/WCAG22/Techniques/html/H81)- [G91: Providing link text that describes the purpose of a link](https://www.w3.org/WAI/WCAG22/Techniques/general/G91) **AND** semantically indicating links
                - [PDF11: Providing links and link text using the Link annotation and the /Link structure element in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF11)- [PDF13: Providing replacement text using the /Alt entry for links in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF13)

##### Advisory Techniques for Success Criterion 2.4.4

- [H2: Combining adjacent image and text links for the same resource](https://www.w3.org/WAI/WCAG22/Techniques/html/H2)- [H80: Identifying the purpose of a link using link text combined with the preceding heading element](https://www.w3.org/WAI/WCAG22/Techniques/html/H80)

##### Failures for Success Criterion 2.4.4

- [F63: Failure of Success Criterion 2.4.4 due to providing link context only in content that is not related to the link](https://www.w3.org/WAI/WCAG22/Techniques/failures/F63)- [F89: Failure of Success Criteria 2.4.4, 2.4.9 and 4.1.2 due to not providing an accessible name for an image which is the only content in a link](https://www.w3.org/WAI/WCAG22/Techniques/failures/F89)

More than one way is available to locate a web page within a set of web pages except where the web page is the result of, or a step in, a process.

[Understanding 2.4.5](https://www.w3.org/WAI/WCAG22/Understanding/multiple-ways.html)

Show Hide techniques and failures for 2.4.5

##### Sufficient Techniques for Success Criterion 2.4.5

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- Using two or more of the following techniques:
  - [G125: Providing links to navigate to related web pages](https://www.w3.org/WAI/WCAG22/Techniques/general/G125)- [G64: Providing a Table of Contents](https://www.w3.org/WAI/WCAG22/Techniques/general/G64)- [G63: Providing a site map](https://www.w3.org/WAI/WCAG22/Techniques/general/G63)- [G161: Providing a search function to help users find content](https://www.w3.org/WAI/WCAG22/Techniques/general/G161)- [G126: Providing a list of links to all other web pages](https://www.w3.org/WAI/WCAG22/Techniques/general/G126)- [G185: Linking to all of the pages on the site from the home page](https://www.w3.org/WAI/WCAG22/Techniques/general/G185)

##### Advisory Techniques for Success Criterion 2.4.5

- [PDF2: Creating bookmarks in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF2)

Headings and labels describe topic or purpose.

[Understanding 2.4.6](https://www.w3.org/WAI/WCAG22/Understanding/headings-and-labels.html)

Show Hide techniques and failures for 2.4.6

##### Sufficient Techniques for Success Criterion 2.4.6

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G130: Providing descriptive headings](https://www.w3.org/WAI/WCAG22/Techniques/general/G130)- [G131: Providing descriptive labels](https://www.w3.org/WAI/WCAG22/Techniques/general/G131)

*Note:* Headings and labels must be programmatically determined, per Success Criterion 1.3.1.

Any keyboard operable user interface has a mode of operation where the keyboard focus indicator is visible.

[Understanding 2.4.7](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html)

Show Hide techniques and failures for 2.4.7

##### Sufficient Techniques for Success Criterion 2.4.7

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G149: Using user interface components that are highlighted by the user agent when they receive focus](https://www.w3.org/WAI/WCAG22/Techniques/general/G149)- [C15: Using CSS to change the presentation of a user interface component when it receives focus](https://www.w3.org/WAI/WCAG22/Techniques/css/C15)- [G165: Using the default focus indicator for the platform so that high visibility default focus indicators will carry over](https://www.w3.org/WAI/WCAG22/Techniques/general/G165)- [G195: Using an author-supplied, visible focus indicator](https://www.w3.org/WAI/WCAG22/Techniques/general/G195)- [C40: Creating a two-color focus indicator to ensure sufficient contrast with all components](https://www.w3.org/WAI/WCAG22/Techniques/css/C40)- [C45: Using CSS :focus-visible to provide keyboard focus indication](https://www.w3.org/WAI/WCAG22/Techniques/css/C45)- [SCR31: Using script to change the background color or border of the element with focus](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR31)

##### Failures for Success Criterion 2.4.7

- [F55: Failure of Success Criteria 2.1.1, 2.4.7, 2.4.13, and 3.2.1 due to using script to remove focus when focus is received](https://www.w3.org/WAI/WCAG22/Techniques/failures/F55)- [F78: Failure of Success Criterion 1.4.11, 2.4.7 and 2.4.13 due to styling element outlines and borders in a way that removes or renders non-visible the visual focus indicator](https://www.w3.org/WAI/WCAG22/Techniques/failures/F78)

Information about the user's location within a set of web pages is available.

[Understanding 2.4.8](https://www.w3.org/WAI/WCAG22/Understanding/location.html)

Show Hide techniques and failures for 2.4.8

##### Sufficient Techniques for Success Criterion 2.4.8

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G65: Providing a breadcrumb trail](https://www.w3.org/WAI/WCAG22/Techniques/general/G65)- [G63: Providing a site map](https://www.w3.org/WAI/WCAG22/Techniques/general/G63)- [G128: Indicating current location within navigation bars](https://www.w3.org/WAI/WCAG22/Techniques/general/G128)- [G127: Identifying a web page's relationship to a larger collection of web pages](https://www.w3.org/WAI/WCAG22/Techniques/general/G127)

##### Advisory Techniques for Success Criterion 2.4.8

- [PDF14: Providing running headers and footers in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF14)- [PDF17: Specifying consistent page numbering for PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF17)

A mechanism is available to allow the purpose of each link to be identified from link text alone, except where the purpose of the link would be ambiguous to users in general.

[Understanding 2.4.9](https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-link-only.html)

Show Hide techniques and failures for 2.4.9

##### Sufficient Techniques for Success Criterion 2.4.9

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [ARIA8: Using aria-label for link purpose](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA8)- [G91: Providing link text that describes the purpose of a link](https://www.w3.org/WAI/WCAG22/Techniques/general/G91)- [H30: Providing link text that describes the purpose of a link for anchor elements](https://www.w3.org/WAI/WCAG22/Techniques/html/H30)- [H24: Providing text alternatives for the area elements of image maps](https://www.w3.org/WAI/WCAG22/Techniques/html/H24)- Allowing the user to choose short or long link text using one of the following techniques:
          - [G189: Providing a control near the beginning of the web page that changes the link text](https://www.w3.org/WAI/WCAG22/Techniques/general/G189)- [SCR30: Using scripts to change the link text](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR30)- Providing a supplemental description of the purpose of a link using one of the following techniques:
            - [C7: Using CSS to hide a portion of the link text](https://www.w3.org/WAI/WCAG22/Techniques/css/C7)- Semantically indicating links using one of the following techniques:
              - [PDF11: Providing links and link text using the Link annotation and the /Link structure element in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF11)- [PDF13: Providing replacement text using the /Alt entry for links in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF13)

##### Advisory Techniques for Success Criterion 2.4.9

- [H2: Combining adjacent image and text links for the same resource](https://www.w3.org/WAI/WCAG22/Techniques/html/H2)- [H33: Supplementing link text with the title attribute](https://www.w3.org/WAI/WCAG22/Techniques/html/H33)

##### Failures for Success Criterion 2.4.9

- [F84: Failure of Success Criterion 2.4.9 due to using a non-specific link such as "click here" or "more" without a mechanism to change the link text to specific text.](https://www.w3.org/WAI/WCAG22/Techniques/failures/F84)- [F89: Failure of Success Criteria 2.4.4, 2.4.9 and 4.1.2 due to not providing an accessible name for an image which is the only content in a link](https://www.w3.org/WAI/WCAG22/Techniques/failures/F89)

Section headings are used to organize the content.

*Note 1:* "Heading" is used in its general sense and includes titles and other ways to add a heading to different types of content.

*Note 2:* This success criterion covers sections within writing, not user interface components. User interface components are covered under Success Criterion 4.1.2.

[Understanding 2.4.10](https://www.w3.org/WAI/WCAG22/Understanding/section-headings.html)

Show Hide techniques and failures for 2.4.10

##### Sufficient Techniques for Success Criterion 2.4.10

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G141: Organizing a page using headings](https://www.w3.org/WAI/WCAG22/Techniques/general/G141)- [H69: Providing heading elements at the beginning of each section of content](https://www.w3.org/WAI/WCAG22/Techniques/html/H69)

When a user interface component receives keyboard focus, the component is not entirely hidden due to author-created content.

*Note 1:* Where content in a configurable interface can be repositioned by the user, then only the initial positions of user-movable content are considered for testing and conformance of this success criterion.

*Note 2:* Content opened by the *user* may obscure the component receiving focus. If the user can reveal the focused component without advancing the keyboard focus, the component with focus is not considered visually hidden due to author-created content.

[Understanding 2.4.11](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html)

Show Hide techniques and failures for 2.4.11

##### Sufficient Techniques for Success Criterion 2.4.11

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [C43: Using CSS scroll-padding to un-obscure content](https://www.w3.org/WAI/WCAG22/Techniques/css/C43)

##### Failures for Success Criterion 2.4.11

- [F110: Failure of Success Criterion 2.4.11 Focus Not Obscured (Minimum) due to a sticky footer or header completely hiding focused elements](https://www.w3.org/WAI/WCAG22/Techniques/failures/F110)

When a user interface component receives keyboard focus, no part of the component is hidden by author-created content.

[Understanding 2.4.12](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-enhanced.html)

Show Hide techniques and failures for 2.4.12

##### Sufficient Techniques for Success Criterion 2.4.12

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [C43: Using CSS scroll-padding to un-obscure content](https://www.w3.org/WAI/WCAG22/Techniques/css/C43)

##### Failures for Success Criterion 2.4.12

- An interaction that causes content to appear over the component with keyboard focus, visually covering part of the focus indicator. This behavior might be encountered with advertising or promotional material meant to provide more information about a product as the user navigates through a catalogue.- A page has a sticky footer (attached to the bottom of the viewport). When tabbing down the page, a focused item is partially obscured by the footer because content in the viewport scrolls without sufficient [scroll padding](https://www.w3.org/TR/css-scroll-snap/#propdef-scroll-padding).

When the keyboard focus indicator is visible, an area of the focus indicator meets all the following:

---

- is at least as large as the area of a 2 CSS pixel thick perimeter of the unfocused component or sub-component, and- has a contrast ratio of at least 3:1 between the same pixels in the focused and unfocused states.

Exceptions:

---

- The focus indicator is determined by the user agent and cannot be adjusted by the author, or- The focus indicator and the indicator's background color are not modified by the author.

*Note 1:* What is perceived as the user interface component or sub-component (to determine the perimeter) depends on its visual presentation. The visual presentation includes the component's visible content, border, and component-specific background. It does not include shadow and glow effects outside the component's content, background, or border.

*Note 2:* Examples of sub-components that may receive a focus indicator are menu items in an opened drop-down menu, or focusable cells in a grid.

*Note 3:* Contrast calculations can be based on colors defined within the technology (such as HTML, CSS, and SVG). Pixels modified by user agent resolution enhancements and anti-aliasing can be ignored.

[Understanding 2.4.13](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html)

Show Hide techniques and failures for 2.4.13

##### Sufficient Techniques for Success Criterion 2.4.13

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G195: Using an author-supplied, visible focus indicator](https://www.w3.org/WAI/WCAG22/Techniques/general/G195)- [C40: Creating a two-color focus indicator to ensure sufficient contrast with all components](https://www.w3.org/WAI/WCAG22/Techniques/css/C40)- [C41: Creating a strong focus indicator within the component](https://www.w3.org/WAI/WCAG22/Techniques/css/C41)

##### Failures for Success Criterion 2.4.13

- [F55: Failure of Success Criteria 2.1.1, 2.4.7, 2.4.13, and 3.2.1 due to using script to remove focus when focus is received](https://www.w3.org/WAI/WCAG22/Techniques/failures/F55)- [F78: Failure of Success Criterion 1.4.11, 2.4.7 and 2.4.13 due to styling element outlines and borders in a way that removes or renders non-visible the visual focus indicator](https://www.w3.org/WAI/WCAG22/Techniques/failures/F78)

### Guideline **2.5** – Input Modalities

Make it easier for users to operate functionality through various inputs beyond keyboard.

All functionality that uses multipoint or path-based gestures for operation can be operated with a single pointer without a path-based gesture, unless a multipoint or path-based gesture is essential.

*Note:* This requirement applies to web content that interprets pointer actions (i.e., this does not apply to actions that are required to operate the user agent or assistive technology).

[Understanding 2.5.1](https://www.w3.org/WAI/WCAG22/Understanding/pointer-gestures.html)

Show Hide techniques and failures for 2.5.1

##### Sufficient Techniques for Success Criterion 2.5.1

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G215: Providing controls to achieve the same result as path based or multipoint gestures](https://www.w3.org/WAI/WCAG22/Techniques/general/G215)- [G216: Providing single point activation for a control slider](https://www.w3.org/WAI/WCAG22/Techniques/general/G216)

##### Failures for Success Criterion 2.5.1

- [F105: Failure of Success Criterion 2.5.1 due to providing functionality via a path-based gesture without simple pointer alternative](https://www.w3.org/WAI/WCAG22/Techniques/failures/F105)

For functionality that can be operated using a single pointer, at least one of the following is true:

---

- **No Down-Event:** The down-event of the pointer is not used to execute any part of the function;- **Abort or Undo:** Completion of the function is on the up-event, and a mechanism is available to abort the function before completion or to undo the function after completion;- **Up Reversal:** The up-event reverses any outcome of the preceding down-event;- **Essential:** Completing the function on the down-event is essential.

*Note 1:* Functions that emulate a keyboard or numeric keypad key press are considered essential.

*Note 2:* This requirement applies to web content that interprets pointer actions (i.e., this does not apply to actions that are required to operate the user agent or assistive technology).

[Understanding 2.5.2](https://www.w3.org/WAI/WCAG22/Understanding/pointer-cancellation.html)

Show Hide techniques and failures for 2.5.2

##### Sufficient Techniques for Success Criterion 2.5.2

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G210: Ensuring that drag-and-drop actions can be cancelled](https://www.w3.org/WAI/WCAG22/Techniques/general/G210)- [G212: Using native controls to ensure functionality is triggered on the up-event.](https://www.w3.org/WAI/WCAG22/Techniques/general/G212)- Touch events are only triggered when touch is removed from a control (Potential future technique)

##### Failures for Success Criterion 2.5.2

- [F101: Failure of Success Criterion 2.5.2 due to activating a control on the down-event](https://www.w3.org/WAI/WCAG22/Techniques/failures/F101)

For user interface components with labels that include text or images of text, the name contains the text that is presented visually.

*Note:* A best practice is to have the text of the label at the start of the name.

[Understanding 2.5.3](https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html)

Show Hide techniques and failures for 2.5.3

##### Sufficient Techniques for Success Criterion 2.5.3

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G208: Including the text of the visible label as part of the accessible name](https://www.w3.org/WAI/WCAG22/Techniques/general/G208)- [G211: Matching the accessible name to the visible label](https://www.w3.org/WAI/WCAG22/Techniques/general/G211)

##### Advisory Techniques for Success Criterion 2.5.3

- [G162: Positioning labels to maximize predictability of relationships](https://www.w3.org/WAI/WCAG22/Techniques/general/G162)- If an icon has no accompanying text, consider using its hover text as its accessible name (Potential future technique)

##### Failures for Success Criterion 2.5.3

- [F96: Failure due to the accessible name not containing the visible label text](https://www.w3.org/WAI/WCAG22/Techniques/failures/F96)- [F111: Failure of Success Criteria 1.3.1, 2.5.3, and 4.1.2 due to a control with visible label text but no accessible name](https://www.w3.org/WAI/WCAG22/Techniques/failures/F111)- Accessible name contains the visible label text, but the words of the visible label are not in the same order as they are in the visible label text (Potential future technique)- Accessible name contains the visible label text, but one or more other words are interspersed in the label (Potential future technique)

Functionality that can be operated by device motion or user motion can also be operated by user interface components and responding to the motion can be disabled to prevent accidental actuation, except when:

---

- **Supported Interface:** The motion is used to operate functionality through an accessibility supported interface;- **Essential:** The motion is essential for the function and doing so would invalidate the activity.

[Understanding 2.5.4](https://www.w3.org/WAI/WCAG22/Understanding/motion-actuation.html)

Show Hide techniques and failures for 2.5.4

##### Sufficient Techniques for Success Criterion 2.5.4

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G213: Provide conventional controls and an application setting for motion activated input](https://www.w3.org/WAI/WCAG22/Techniques/general/G213)- GXXX: Supporting system level features which allow the user to disable motion actuation

##### Failures for Success Criterion 2.5.4

- [F106: Failure due to inability to deactivate motion actuation](https://www.w3.org/WAI/WCAG22/Techniques/failures/F106)- FXXX: Failure of Success Criterion 2.5.4 due to disrupting or disabling system level features which allow the user to disable motion actuation

The size of the target for pointer inputs is at least 44 by 44 CSS pixels except when:

---

- **Equivalent:** The target is available through an equivalent link or control on the same page that is at least 44 by 44 CSS pixels;- **Inline:** The target is in a sentence or block of text;- **User Agent Control:** The size of the target is determined by the user agent and is not modified by the author;- **Essential:** A particular presentation of the target is essential to the information being conveyed.

[Understanding 2.5.5](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html)

Show Hide techniques and failures for 2.5.5

##### Sufficient Techniques for Success Criterion 2.5.5

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- Ensuring that targets are at least 44 by 44 CSS pixels

##### Advisory Techniques for Success Criterion 2.5.5

- Ensuring inline links provide sufficiently large activation target

##### Failures for Success Criterion 2.5.5

- Failure of Success Criterion 2.5.5 due to target being less than 44 by 44 CSS pixels

Web content does not restrict use of input modalities available on a platform except where the restriction is essential, required to ensure the security of the content, or required to respect user settings.

[Understanding 2.5.6](https://www.w3.org/WAI/WCAG22/Understanding/concurrent-input-mechanisms.html)

Show Hide techniques and failures for 2.5.6

##### Sufficient Techniques for Success Criterion 2.5.6

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- Only using high-level, input-agnostic event handlers, such as `focus`, `blur`, `click`, in Javascript (Potential future technique)- Registering event handlers for keyboard/keyboard-like and pointer inputs simultaneously in Javascript; see [Example 1 in Pointer Events Level 2](https://www.w3.org/TR/pointerevents2/#example_1) (Potential future technique)

##### Failures for Success Criterion 2.5.6

- [F98: Failure due to interactions being limited to touch-only on touchscreen devices](https://www.w3.org/WAI/WCAG22/Techniques/failures/F98)

All functionality that uses a dragging movement for operation can be achieved by a single pointer without dragging, unless dragging is essential or the functionality is determined by the user agent and not modified by the author.

*Note:* This requirement applies to web content that interprets pointer actions (i.e., this does not apply to actions that are required to operate the user agent or assistive technology).

[Understanding 2.5.7](https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html)

Show Hide techniques and failures for 2.5.7

##### Sufficient Techniques for Success Criterion 2.5.7

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G219: Ensuring that an alternative is available for dragging movements that operate on content](https://www.w3.org/WAI/WCAG22/Techniques/general/G219)

##### Failures for Success Criterion 2.5.7

- [F108: Failure of Success Criterion 2.5.7 Dragging Movements due to not providing a single pointer method that does not require a dragging movement](https://www.w3.org/WAI/WCAG22/Techniques/failures/F108)

The size of the target for pointer inputs is at least 24 by 24 CSS pixels, except when:

---

- **Spacing:** Undersized targets (those less than 24 by 24 CSS pixels) are positioned so that if a 24 CSS pixel diameter circle is centered on the bounding box of each, the circles do not intersect another target or the circle for another undersized target;- **Equivalent:** The function can be achieved through a different control on the same page that meets this criterion;- **Inline:** The target is in a sentence or its size is otherwise constrained by the line-height of non-target text;- **User Agent Control:** The size of the target is determined by the user agent and is not modified by the author;- **Essential:** A particular presentation of the target is essential or is legally required for the information being conveyed.

*Note 1:* Targets that allow for values to be selected spatially based on position within the target are considered one target for the purpose of the success criterion. Examples include sliders, color pickers displaying a gradient of colors, or editable areas where you position the cursor.

*Note 2:* For inline targets the line-height should be interpreted as perpendicular to the flow of text. For example, in a language displayed vertically, the line-height would be horizontal.

[Understanding 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)

Show Hide techniques and failures for 2.5.8

##### Sufficient Techniques for Success Criterion 2.5.8

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [C42: Using min-height and min-width to ensure sufficient target spacing](https://www.w3.org/WAI/WCAG22/Techniques/css/C42)

## **Principle 3** – Understandable

Information and the operation of the user interface must be understandable.

### Guideline **3.1** – Readable

Make text content readable and understandable.

The default human language of each web page can be programmatically determined.

[Understanding 3.1.1](https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html)

Show Hide techniques and failures for 3.1.1

##### Sufficient Techniques for Success Criterion 3.1.1

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [H57: Using the language attribute on the HTML element](https://www.w3.org/WAI/WCAG22/Techniques/html/H57)- [PDF16: Setting the default language using the /Lang entry in the document catalog of a PDF document](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF16)- [PDF19: Specifying the language for a passage or phrase with the Lang entry in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF19)

##### Advisory Techniques for Success Criterion 3.1.1

- [SVR5: Specifying the default language in the HTTP header](https://www.w3.org/WAI/WCAG22/Techniques/server-side-script/SVR5)

The human language of each passage or phrase in the content can be programmatically determined except for proper names, technical terms, words of indeterminate language, and words or phrases that have become part of the vernacular of the immediately surrounding text.

[Understanding 3.1.2](https://www.w3.org/WAI/WCAG22/Understanding/language-of-parts.html)

Show Hide techniques and failures for 3.1.2

##### Sufficient Techniques for Success Criterion 3.1.2

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [H58: Using language attributes to identify changes in the human language](https://www.w3.org/WAI/WCAG22/Techniques/html/H58)- [PDF19: Specifying the language for a passage or phrase with the Lang entry in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF19)

A mechanism is available for identifying specific definitions of words or phrases used in an unusual or restricted way, including idioms and jargon.

[Understanding 3.1.3](https://www.w3.org/WAI/WCAG22/Understanding/unusual-words.html)

Show Hide techniques and failures for 3.1.3

##### Sufficient Techniques for Success Criterion 3.1.3

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: If the word or phrase has a unique meaning within the web page:

- [G101: Providing the definition of a word or phrase used in an unusual or restricted way](https://www.w3.org/WAI/WCAG22/Techniques/general/G101) for the first occurrence of the word or phrase in a web page using one of the following techniques:
  - [G55: Linking to definitions](https://www.w3.org/WAI/WCAG22/Techniques/general/G55)
    - [H40: Using description lists](https://www.w3.org/WAI/WCAG22/Techniques/html/H40)- [G112: Using inline definitions](https://www.w3.org/WAI/WCAG22/Techniques/general/G112)
      - [H54: Using the dfn element to identify the defining instance of a word](https://www.w3.org/WAI/WCAG22/Techniques/html/H54)- [G101: Providing the definition of a word or phrase used in an unusual or restricted way](https://www.w3.org/WAI/WCAG22/Techniques/general/G101) for each occurrence of the word or phrase in a web page using one of the following techniques:
    - [G55: Linking to definitions](https://www.w3.org/WAI/WCAG22/Techniques/general/G55)
      - [H40: Using description lists](https://www.w3.org/WAI/WCAG22/Techniques/html/H40)- [G62: Providing a glossary](https://www.w3.org/WAI/WCAG22/Techniques/general/G62)- [G70: Providing a function to search an online dictionary](https://www.w3.org/WAI/WCAG22/Techniques/general/G70)

###### Situation B: If the word or phrase means different things within the same web page:

- [G101: Providing the definition of a word or phrase used in an unusual or restricted way](https://www.w3.org/WAI/WCAG22/Techniques/general/G101) for each occurrence of the word or phrase in a web page using one of the following techniques:
  - [G55: Linking to definitions](https://www.w3.org/WAI/WCAG22/Techniques/general/G55)
    - [H40: Using description lists](https://www.w3.org/WAI/WCAG22/Techniques/html/H40)- [G112: Using inline definitions](https://www.w3.org/WAI/WCAG22/Techniques/general/G112)
      - [H54: Using the dfn element to identify the defining instance of a word](https://www.w3.org/WAI/WCAG22/Techniques/html/H54)

A mechanism for identifying the expanded form or meaning of abbreviations is available.

[Understanding 3.1.4](https://www.w3.org/WAI/WCAG22/Understanding/abbreviations.html)

Show Hide techniques and failures for 3.1.4

##### Sufficient Techniques for Success Criterion 3.1.4

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: If the abbreviation has only one meaning within the web page:

- [G102: Providing the expansion or explanation of an abbreviation](https://www.w3.org/WAI/WCAG22/Techniques/general/G102) for the first occurrence of the abbreviation in a web page using one of the following techniques:
  - [G97: Providing the first use of an abbreviation immediately before or after the expanded form](https://www.w3.org/WAI/WCAG22/Techniques/general/G97)- [G55: Linking to definitions](https://www.w3.org/WAI/WCAG22/Techniques/general/G55)- [PDF8: Providing definitions for abbreviations via an E entry for a structure element](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF8)- [G102: Providing the expansion or explanation of an abbreviation](https://www.w3.org/WAI/WCAG22/Techniques/general/G102) for all occurrences of the abbreviation in a web page using one of the following techniques:
    - [G55: Linking to definitions](https://www.w3.org/WAI/WCAG22/Techniques/general/G55)- [G62: Providing a glossary](https://www.w3.org/WAI/WCAG22/Techniques/general/G62)- [G70: Providing a function to search an online dictionary](https://www.w3.org/WAI/WCAG22/Techniques/general/G70)- [PDF8: Providing definitions for abbreviations via an E entry for a structure element](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF8)

###### Situation B: If the abbreviation means different things within the same web page:

- [G102: Providing the expansion or explanation of an abbreviation](https://www.w3.org/WAI/WCAG22/Techniques/general/G102) for all occurrences of abbreviations in a web page using one of the following techniques:
  - [G55: Linking to definitions](https://www.w3.org/WAI/WCAG22/Techniques/general/G55)- [PDF8: Providing definitions for abbreviations via an E entry for a structure element](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF8)

##### Advisory Techniques for Success Criterion 3.1.4

- [H28: Providing definitions for abbreviations by using the abbr element](https://www.w3.org/WAI/WCAG22/Techniques/html/H28)

When text requires reading ability more advanced than the lower secondary education level after removal of proper names and titles, supplemental content, or a version that does not require reading ability more advanced than the lower secondary education level, is available.

[Understanding 3.1.5](https://www.w3.org/WAI/WCAG22/Understanding/reading-level.html)

Show Hide techniques and failures for 3.1.5

##### Sufficient Techniques for Success Criterion 3.1.5

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G86: Providing a text summary that can be understood by people with lower secondary education level reading ability](https://www.w3.org/WAI/WCAG22/Techniques/general/G86)- [G103: Providing visual illustrations, pictures, and symbols to help explain ideas, events, and processes](https://www.w3.org/WAI/WCAG22/Techniques/general/G103)- [G79: Providing a spoken version of the text](https://www.w3.org/WAI/WCAG22/Techniques/general/G79)- [G153: Making the text easier to read](https://www.w3.org/WAI/WCAG22/Techniques/general/G153)- [G160: Providing sign language versions of information, ideas, and processes that must be understood in order to use the content](https://www.w3.org/WAI/WCAG22/Techniques/general/G160)

*Note:* Different sites may address this success criterion in different ways. An audio version of the content may be helpful to some users. For some people who are deaf, a sign language version of the page may be easier to understand than a written language version since sign language may be their first language. Some sites may decide to do both or other combinations. No technique will help all users who have difficulty. So different techniques are provided as sufficient techniques here for authors trying to make their sites more accessible. Any numbered technique or combination above can be used by a particular site and it is considered sufficient by the Working Group.

A mechanism is available for identifying specific pronunciation of words where meaning of the words, in context, is ambiguous without knowing the pronunciation.

[Understanding 3.1.6](https://www.w3.org/WAI/WCAG22/Understanding/pronunciation.html)

Show Hide techniques and failures for 3.1.6

##### Sufficient Techniques for Success Criterion 3.1.6

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G120: Providing the pronunciation immediately following the word](https://www.w3.org/WAI/WCAG22/Techniques/general/G120)- [G121: Linking to pronunciations](https://www.w3.org/WAI/WCAG22/Techniques/general/G121)- [G62: Providing a glossary](https://www.w3.org/WAI/WCAG22/Techniques/general/G62) that includes pronunciation information for words that have a unique pronunciation in the content and have meaning that depends on pronunciation- [G163: Using standard diacritical marks that can be turned off](https://www.w3.org/WAI/WCAG22/Techniques/general/G163)- [H62: Using the ruby element](https://www.w3.org/WAI/WCAG22/Techniques/html/H62)

### Guideline **3.2** – Predictable

Make web pages appear and operate in predictable ways.

When any user interface component receives focus, it does not initiate a change of context.

[Understanding 3.2.1](https://www.w3.org/WAI/WCAG22/Understanding/on-focus.html)

Show Hide techniques and failures for 3.2.1

##### Sufficient Techniques for Success Criterion 3.2.1

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G107: Using "activate" rather than "focus" as a trigger for changes of context](https://www.w3.org/WAI/WCAG22/Techniques/general/G107)

*Note:* A change of content is not always a change of context. This success criterion is automatically met if changes in content are not also changes of context.

##### Advisory Techniques for Success Criterion 3.2.1

- [G200: Opening new windows and tabs from a link only when necessary](https://www.w3.org/WAI/WCAG22/Techniques/general/G200)- [G201: Giving users advanced warning when opening a new window](https://www.w3.org/WAI/WCAG22/Techniques/general/G201)

##### Failures for Success Criterion 3.2.1

- [F55: Failure of Success Criteria 2.1.1, 2.4.7, 2.4.13, and 3.2.1 due to using script to remove focus when focus is received](https://www.w3.org/WAI/WCAG22/Techniques/failures/F55)

Changing the setting of any user interface component does not automatically cause a change of context unless the user has been advised of the behavior before using the component.

[Understanding 3.2.2](https://www.w3.org/WAI/WCAG22/Understanding/on-input.html)

Show Hide techniques and failures for 3.2.2

##### Sufficient Techniques for Success Criterion 3.2.2

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G80: Providing a submit button to initiate a change of context](https://www.w3.org/WAI/WCAG22/Techniques/general/G80) using one of the following techniques:
  - [H32: Providing submit buttons](https://www.w3.org/WAI/WCAG22/Techniques/html/H32)- [H84: Using a button with a select element to perform an action](https://www.w3.org/WAI/WCAG22/Techniques/html/H84)- [PDF15: Providing submit buttons with the submit-form action in PDF forms](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF15)- [G13: Describing what will happen before a change to a form control that causes a change of context to occur is made](https://www.w3.org/WAI/WCAG22/Techniques/general/G13)- [SCR19: Using an onchange event on a select element without causing a change of context](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR19)

*Note:* A change of content is not always a change of context. This success criterion is automatically met if changes in content are not also changes of context.

##### Advisory Techniques for Success Criterion 3.2.2

- [G201: Giving users advanced warning when opening a new window](https://www.w3.org/WAI/WCAG22/Techniques/general/G201)

##### Failures for Success Criterion 3.2.2

- [F36: Failure of Success Criterion 3.2.2 due to automatically submitting a form and presenting new content without prior warning when the last field in the form is given a value](https://www.w3.org/WAI/WCAG22/Techniques/failures/F36)- [F37: Failure of Success Criterion 3.2.2 due to launching a new window without prior warning when the selection of a radio button, check box or select list is changed](https://www.w3.org/WAI/WCAG22/Techniques/failures/F37)

Navigational mechanisms that are repeated on multiple web pages within a set of web pages occur in the same relative order each time they are repeated, unless a change is initiated by the user.

[Understanding 3.2.3](https://www.w3.org/WAI/WCAG22/Understanding/consistent-navigation.html)

Show Hide techniques and failures for 3.2.3

##### Sufficient Techniques for Success Criterion 3.2.3

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G61: Presenting repeated components in the same relative order each time they appear](https://www.w3.org/WAI/WCAG22/Techniques/general/G61)

##### Advisory Techniques for Success Criterion 3.2.3

- [PDF14: Providing running headers and footers in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF14)- [PDF17: Specifying consistent page numbering for PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF17)

##### Failures for Success Criterion 3.2.3

- [F66: Failure of Success Criterion 3.2.3 due to presenting navigation links in a different relative order on different pages](https://www.w3.org/WAI/WCAG22/Techniques/failures/F66)

Components that have the same functionality within a set of web pages are identified consistently.

[Understanding 3.2.4](https://www.w3.org/WAI/WCAG22/Understanding/consistent-identification.html)

Show Hide techniques and failures for 3.2.4

##### Sufficient Techniques for Success Criterion 3.2.4

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G197: Using labels, names, and text alternatives consistently for content that has the same functionality](https://www.w3.org/WAI/WCAG22/Techniques/general/G197) **AND** following the [sufficient techniques for Success Criterion 1.1.1](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content#techniques) and [sufficient techniques for Success Criterion 4.1.2](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value#techniques) for providing labels, names, and text alternatives

*Note:*

Text alternatives that are "consistent" are not always "identical." For instance, you may have a graphical arrow at the bottom of a web page that links to the next web page. The text alternative may say "Go to page 4." Naturally, it would not be appropriate to repeat this exact text alternative on the next web page. It would be more appropriate to say "Go to page 5". Although these text alternatives would not be identical, they would be consistent, and therefore would satisfy this success criterion.

A single non-text-content-item may be used to serve different functions. In such cases, different text alternatives are necessary and should be used. Examples can be commonly found with the use of icons such as check marks, cross marks, and traffic signs. Their functions can be different depending on the context of the web page. A check mark icon may function as "approved", "completed", or "included", to name a few, depending on the situation. Using "check mark" as text alternative across all web pages does not help users understand the function of the icon. Different text alternatives can be used when the same non-text content serves multiple functions.

##### Failures for Success Criterion 3.2.4

- [F31: Failure of Success Criterion 3.2.4 due to using two different labels for the same function on different web pages within a set of web pages](https://www.w3.org/WAI/WCAG22/Techniques/failures/F31)

Changes of context are initiated only by user request or a mechanism is available to turn off such changes.

[Understanding 3.2.5](https://www.w3.org/WAI/WCAG22/Understanding/change-on-request.html)

Show Hide techniques and failures for 3.2.5

##### Sufficient Techniques for Success Criterion 3.2.5

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: If the web page allows automatic updates:

- [G76: Providing a mechanism to request an update of the content instead of updating automatically](https://www.w3.org/WAI/WCAG22/Techniques/general/G76)

###### Situation B: If automatic redirects are possible:

- [SVR1: Implementing automatic redirects on the server side instead of on the client side](https://www.w3.org/WAI/WCAG22/Techniques/server-side-script/SVR1)- [G110: Using an instant client-side redirect](https://www.w3.org/WAI/WCAG22/Techniques/general/G110) using one of the following techniques:
    - [H76: Using meta refresh to create an instant client-side redirect](https://www.w3.org/WAI/WCAG22/Techniques/html/H76)

###### Situation C: If the web page uses pop-up windows:

- Including pop-up windows using one of the following techniques:
  - [H83: Using the target attribute to open a new window on user request and indicating this in link text](https://www.w3.org/WAI/WCAG22/Techniques/html/H83)- [SCR24: Using progressive enhancement to open new windows on user request](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR24)

###### Situation D: If using an onchange event on a select element:

- [SCR19: Using an onchange event on a select element without causing a change of context](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR19)

##### Advisory Techniques for Success Criterion 3.2.5

- [G200: Opening new windows and tabs from a link only when necessary](https://www.w3.org/WAI/WCAG22/Techniques/general/G200)

##### Failures for Success Criterion 3.2.5

- [F60: Failure of Success Criterion 3.2.5 due to launching a new window when a user enters text into an input field](https://www.w3.org/WAI/WCAG22/Techniques/failures/F60)- [F61: Failure of Success Criterion 3.2.5 due to complete change of main content through an automatic update that the user cannot disable from within the content](https://www.w3.org/WAI/WCAG22/Techniques/failures/F61)- [F9: Failure of Success Criterion 3.2.5 due to changing the context when the user removes focus from a form element](https://www.w3.org/WAI/WCAG22/Techniques/failures/F9)- [F22: Failure of Success Criterion 3.2.5 due to opening windows that are not requested by the user](https://www.w3.org/WAI/WCAG22/Techniques/failures/F22)- [F52: Failure of Success Criterion 3.2.5 due to opening a new window as soon as a new page is loaded](https://www.w3.org/WAI/WCAG22/Techniques/failures/F52)- [F40: Failure due to using meta redirect with a time limit](https://www.w3.org/WAI/WCAG22/Techniques/failures/F40)- [F41: Failure of Success Criterion 2.2.1, 2.2.4, and 3.2.5 due to using meta refresh to reload the page](https://www.w3.org/WAI/WCAG22/Techniques/failures/F41)

If a web page contains any of the following help mechanisms, and those mechanisms are repeated on multiple web pages within a set of web pages, they occur in the same order relative to other page content, unless a change is initiated by the user:

---

- Human contact details;- Human contact mechanism;- Self-help option;- A fully automated contact mechanism.

*Note 1:* Help mechanisms may be provided directly on the page, or may be provided via a direct link to a different page containing the information.

*Note 2:* For this success criterion, "the same order relative to other page content" can be thought of as how the content is ordered when the page is serialized. The visual position of a help mechanism is likely to be consistent across pages for the same page variation (e.g., CSS break-point). The user can initiate a change, such as changing the page's zoom or orientation, which may trigger a different page variation. This criterion is concerned with relative order across pages displayed in the same page variation (e.g., same zoom level and orientation).

[Understanding 3.2.6](https://www.w3.org/WAI/WCAG22/Understanding/consistent-help.html)

Show Hide techniques and failures for 3.2.6

##### Sufficient Techniques for Success Criterion 3.2.6

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G220: Provide a contact-us link in a consistent location](https://www.w3.org/WAI/WCAG22/Techniques/general/G220)

##### Failures for Success Criterion 3.2.6

- Inconsistent Help Location

### Guideline **3.3** – Input Assistance

Help users avoid and correct mistakes.

If an input error is automatically detected, the item that is in error is identified and the error is described to the user in text.

[Understanding 3.3.1](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html)

Show Hide techniques and failures for 3.3.1

##### Sufficient Techniques for Success Criterion 3.3.1

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: If a form contains fields for which information from the user is mandatory.

- [G83: Providing text descriptions to identify required fields that were not completed](https://www.w3.org/WAI/WCAG22/Techniques/general/G83)- [ARIA2: Identifying a required field with the aria-required property](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA2)- [ARIA21: Using aria-invalid to Indicate An Error Field](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA21)- [SCR18: Providing client-side validation and alert](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR18)- [PDF5: Indicating required form controls in PDF forms](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF5)

###### Situation B: If information provided by the user is required to be in a specific data format or of certain values.

- [ARIA18: Using aria-alertdialog to Identify Errors](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA18)- [ARIA19: Using ARIA role=alert or Live Regions to Identify Errors](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA19)- [ARIA21: Using aria-invalid to Indicate An Error Field](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA21)- [G84: Providing a text description when the user provides information that is not in the list of allowed values](https://www.w3.org/WAI/WCAG22/Techniques/general/G84)- [G85: Providing a text description when user input falls outside the required format or values](https://www.w3.org/WAI/WCAG22/Techniques/general/G85)- [SCR18: Providing client-side validation and alert](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR18)- [SCR32: Providing client-side validation and adding error text via the DOM](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR32)- [PDF22: Indicating when user input falls outside the required format or values in PDF forms](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF22)

##### Advisory Techniques for Success Criterion 3.3.1

- [G139: Creating a mechanism that allows users to jump to errors](https://www.w3.org/WAI/WCAG22/Techniques/general/G139)- [G199: Providing success feedback when data is submitted successfully](https://www.w3.org/WAI/WCAG22/Techniques/general/G199)

Labels or instructions are provided when content requires user input.

[Understanding 3.3.2](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html)

Show Hide techniques and failures for 3.3.2

##### Sufficient Techniques for Success Criterion 3.3.2

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G131: Providing descriptive labels](https://www.w3.org/WAI/WCAG22/Techniques/general/G131) **AND** one of the following techniques:
  - [ARIA1: Using the aria-describedby property to provide a descriptive label for user interface controls](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA1)- [ARIA9: Using aria-labelledby to concatenate a label from several text nodes](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA9)- [ARIA17: Using grouping roles to identify related form controls](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA17)- [G89: Providing expected data format and example](https://www.w3.org/WAI/WCAG22/Techniques/general/G89)- [G184: Providing text instructions at the beginning of a form or set of fields that describes the necessary input](https://www.w3.org/WAI/WCAG22/Techniques/general/G184)- [G162: Positioning labels to maximize predictability of relationships](https://www.w3.org/WAI/WCAG22/Techniques/general/G162)- [G83: Providing text descriptions to identify required fields that were not completed](https://www.w3.org/WAI/WCAG22/Techniques/general/G83)- [H90: Indicating required form controls using label or legend](https://www.w3.org/WAI/WCAG22/Techniques/html/H90)- [PDF5: Indicating required form controls in PDF forms](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF5)- [H44: Using label elements to associate text labels with form controls](https://www.w3.org/WAI/WCAG22/Techniques/html/H44)- [PDF10: Providing labels for interactive form controls in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF10)- [H71: Providing a description for groups of form controls using fieldset and legend elements](https://www.w3.org/WAI/WCAG22/Techniques/html/H71)- [G167: Using an adjacent button to label the purpose of a field](https://www.w3.org/WAI/WCAG22/Techniques/general/G167)

*Note:* The techniques at the end of the above list should be considered "last resort" and only used when the other techniques cannot be applied to the page. The earlier techniques are preferred because they increase accessibility to a wider user group.

##### Advisory Techniques for Success Criterion 3.3.2

- [G13: Describing what will happen before a change to a form control that causes a change of context to occur is made](https://www.w3.org/WAI/WCAG22/Techniques/general/G13)

##### Failures for Success Criterion 3.3.2

- [F82: Failure of Success Criterion 3.3.2 by visually formatting a set of phone number fields but not including a text label](https://www.w3.org/WAI/WCAG22/Techniques/failures/F82)

If an input error is automatically detected and suggestions for correction are known, then the suggestions are provided to the user, unless it would jeopardize the security or purpose of the content.

[Understanding 3.3.3](https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html)

Show Hide techniques and failures for 3.3.3

##### Sufficient Techniques for Success Criterion 3.3.3

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: If information for a field is required to be in a specific data format:

- [ARIA18: Using aria-alertdialog to Identify Errors](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA18)- [G85: Providing a text description when user input falls outside the required format or values](https://www.w3.org/WAI/WCAG22/Techniques/general/G85)- [G177: Providing suggested correction text](https://www.w3.org/WAI/WCAG22/Techniques/general/G177)- [PDF22: Indicating when user input falls outside the required format or values in PDF forms](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF22)

###### Situation B: Information provided by the user is required to be one of a limited set of values:

- [ARIA18: Using aria-alertdialog to Identify Errors](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA18)- [G84: Providing a text description when the user provides information that is not in the list of allowed values](https://www.w3.org/WAI/WCAG22/Techniques/general/G84)- [G177: Providing suggested correction text](https://www.w3.org/WAI/WCAG22/Techniques/general/G177)- [PDF22: Indicating when user input falls outside the required format or values in PDF forms](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF22)

*Note:* In some cases, more than one of these situations may apply. For example, when a mandatory field also requires the data to be in a specific format.

##### Advisory Techniques for Success Criterion 3.3.3

- [G139: Creating a mechanism that allows users to jump to errors](https://www.w3.org/WAI/WCAG22/Techniques/general/G139)- [G199: Providing success feedback when data is submitted successfully](https://www.w3.org/WAI/WCAG22/Techniques/general/G199)- [SCR18: Providing client-side validation and alert](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR18)- [SCR32: Providing client-side validation and adding error text via the DOM](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR32)

For web pages that cause legal commitments or financial transactions for the user to occur, that modify or delete user-controllable data in data storage systems, or that submit user test responses, at least one of the following is true:

---

- **Reversible:** Submissions are reversible.- **Checked:** Data entered by the user is checked for input errors and the user is provided an opportunity to correct them.- **Confirmed:** A mechanism is available for reviewing, confirming, and correcting information before finalizing the submission.

[Understanding 3.3.4](https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data.html)

Show Hide techniques and failures for 3.3.4

##### Sufficient Techniques for Success Criterion 3.3.4

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: If an application causes a legal transaction to occur, such as making a purchase or submitting an income tax return:

- [G164: Providing a stated time within which an online request (or transaction) may be amended or canceled by the user after making the request](https://www.w3.org/WAI/WCAG22/Techniques/general/G164)- [G98: Providing the ability for the user to review and correct answers before submitting](https://www.w3.org/WAI/WCAG22/Techniques/general/G98)- [G155: Providing a checkbox in addition to a submit button](https://www.w3.org/WAI/WCAG22/Techniques/general/G155)

###### Situation B: If an action causes information to be deleted:

- [G99: Providing the ability to recover deleted information](https://www.w3.org/WAI/WCAG22/Techniques/general/G99)- [G168: Requesting confirmation to continue with selected action](https://www.w3.org/WAI/WCAG22/Techniques/general/G168)- [G155: Providing a checkbox in addition to a submit button](https://www.w3.org/WAI/WCAG22/Techniques/general/G155)

###### Situation C: If the web page includes a testing application

- [G98: Providing the ability for the user to review and correct answers before submitting](https://www.w3.org/WAI/WCAG22/Techniques/general/G98)- [G168: Requesting confirmation to continue with selected action](https://www.w3.org/WAI/WCAG22/Techniques/general/G168)

##### Advisory Techniques for Success Criterion 3.3.4

- [SCR18: Providing client-side validation and alert](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR18)- [G199: Providing success feedback when data is submitted successfully](https://www.w3.org/WAI/WCAG22/Techniques/general/G199)

Context-sensitive help is available.

[Understanding 3.3.5](https://www.w3.org/WAI/WCAG22/Understanding/help.html)

Show Hide techniques and failures for 3.3.5

##### Sufficient Techniques for Success Criterion 3.3.5

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: If a form requires text input:

- [G71: Providing a help link on every web page](https://www.w3.org/WAI/WCAG22/Techniques/general/G71)- [G193: Providing help by an assistant in the web page](https://www.w3.org/WAI/WCAG22/Techniques/general/G193)- [G194: Providing spell checking and suggestions for text input](https://www.w3.org/WAI/WCAG22/Techniques/general/G194)- [G184: Providing text instructions at the beginning of a form or set of fields that describes the necessary input](https://www.w3.org/WAI/WCAG22/Techniques/general/G184)

###### Situation B: If a form requires text input in an expected data format:

- [G89: Providing expected data format and example](https://www.w3.org/WAI/WCAG22/Techniques/general/G89)- [G184: Providing text instructions at the beginning of a form or set of fields that describes the necessary input](https://www.w3.org/WAI/WCAG22/Techniques/general/G184)

##### Advisory Techniques for Success Criterion 3.3.5

- [H89: Using the title attribute to provide context-sensitive help](https://www.w3.org/WAI/WCAG22/Techniques/html/H89)

For web pages that require the user to submit information, at least one of the following is true:

---

- **Reversible:** Submissions are reversible.- **Checked:** Data entered by the user is checked for input errors and the user is provided an opportunity to correct them.- **Confirmed:** A mechanism is available for reviewing, confirming, and correcting information before finalizing the submission.

[Understanding 3.3.6](https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-all.html)

Show Hide techniques and failures for 3.3.6

##### Sufficient Techniques for Success Criterion 3.3.6

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- Following the [sufficient techniques for Success Criterion 3.3.4](https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data#techniques) for all forms that require the user to submit information

Information previously entered by or provided to the user that is required to be entered again in the same process is either:

---

- auto-populated, or- available for the user to select.

Except when:

---

- re-entering the information is essential,- the information is required to ensure the security of the content, or- previously entered information is no longer valid.

[Understanding 3.3.7](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html)

Show Hide techniques and failures for 3.3.7

##### Sufficient Techniques for Success Criterion 3.3.7

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G221: Provide data from a previous step in a process](https://www.w3.org/WAI/WCAG22/Techniques/general/G221)- Not requesting the same information twice (Potential future technique)

A cognitive function test (such as remembering a password or solving a puzzle) is not required for any step in an authentication process unless that step provides at least one of the following:

---

- **Alternative:** Another authentication method that does not rely on a cognitive function test.- **Mechanism:** A mechanism is available to assist the user in completing the cognitive function test.- **Object Recognition:** The cognitive function test is to recognize objects.- **Personal Content:** The cognitive function test is to identify non-text content the user provided to the website.

*Note 1:* "Object recognition" and "Personal content" may be represented by images, video, or audio.

*Note 2:* Examples of mechanisms that satisfy this criterion include:

- support for password entry by password managers to reduce memory need, and- copy and paste to reduce the cognitive burden of re-typing.

[Understanding 3.3.8](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html)

Show Hide techniques and failures for 3.3.8

##### Sufficient Techniques for Success Criterion 3.3.8

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G218: Email link authentication](https://www.w3.org/WAI/WCAG22/Techniques/general/G218)- [H100: Providing properly marked up email and password inputs](https://www.w3.org/WAI/WCAG22/Techniques/html/H100)- Providing WebAuthn as an alternative to username/password (Potential future technique)- Providing a third-party login using OAuth (Potential future technique)- Using two techniques to provide two-factor authentication (Potential future technique)

##### Failures for Success Criterion 3.3.8

- [F109: Failure of Success Criterion 3.3.8 and 3.3.9 due to preventing password or code re-entry in the same format](https://www.w3.org/WAI/WCAG22/Techniques/failures/F109)

A cognitive function test (such as remembering a password or solving a puzzle) is not required for any step in an authentication process unless that step provides at least one of the following:

---

- **Alternative:** Another authentication method that does not rely on a cognitive function test.- **Mechanism:** A mechanism is available to assist the user in completing the cognitive function test.

[Understanding 3.3.9](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-enhanced.html)

Show Hide techniques and failures for 3.3.9

##### Sufficient Techniques for Success Criterion 3.3.9

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

- [G218: Email link authentication](https://www.w3.org/WAI/WCAG22/Techniques/general/G218)- [H100: Providing properly marked up email and password inputs](https://www.w3.org/WAI/WCAG22/Techniques/html/H100)- Providing WebAuthn as an alternative to username/password (Potential future technique)- Providing a third-party login using OAuth (Potential future technique)- Using two techniques to provide two-factor authentication (Potential future technique)

##### Failures for Success Criterion 3.3.9

- [F109: Failure of Success Criterion 3.3.8 and 3.3.9 due to preventing password or code re-entry in the same format](https://www.w3.org/WAI/WCAG22/Techniques/failures/F109)

## **Principle 4** – Robust

Content must be robust enough that it can be interpreted by a wide variety of user agents, including assistive technologies.

### Guideline **4.1** – Compatible

Maximize compatibility with current and future user agents, including assistive technologies.

In content implemented using markup languages, elements have complete start and end tags, elements are nested according to their specifications, elements do not contain duplicate attributes, and any IDs are unique, except where the specifications allow these features.

*Note 1:* This success criterion should be considered as always satisfied for any content using HTML or XML.

*Note 2:*

Since this criterion was written, the HTML Living Standard has adopted specific requirements governing how user agents must handle incomplete tags, incorrect element nesting, duplicate attributes, and non-unique IDs. [HTML]

Although the HTML standard treats some of these cases as non-conforming for authors, it is considered to "allow these features" for the purposes of this success criterion because the specification requires that user agents support handling these cases consistently. In practice, this criterion no longer provides any benefit to people with disabilities in itself.

Issues such as missing roles due to inappropriately nested elements or incorrect states or names due to a duplicate ID are covered by different success criteria and should be reported under those criteria rather than as issues with 4.1.1.

[Understanding 4.1.1](https://www.w3.org/WAI/WCAG22/Understanding/parsing.html)

For all user interface components (including but not limited to: form elements, links and components generated by scripts), the name and role can be programmatically determined; states, properties, and values that can be set by the user can be programmatically set; and notification of changes to these items is available to user agents, including assistive technologies.

*Note:* This success criterion is primarily for web authors who develop or script their own user interface components. For example, standard HTML controls already meet this success criterion when used according to specification.

[Understanding 4.1.2](https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html)

Show Hide techniques and failures for 4.1.2

##### Sufficient Techniques for Success Criterion 4.1.2

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: If using a standard user interface component in a markup language (e.g., HTML):

- [ARIA14: Using aria-label to provide an invisible label where a visible label cannot be used](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA14)- [ARIA16: Using aria-labelledby to provide a name for user interface controls](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA16)- [G108: Using markup features to expose the name and role, allow user-settable properties to be directly set, and provide notification of changes](https://www.w3.org/WAI/WCAG22/Techniques/general/G108) using one or more of the following techniques:
      - [H91: Using HTML form controls and links](https://www.w3.org/WAI/WCAG22/Techniques/html/H91)- [H44: Using label elements to associate text labels with form controls](https://www.w3.org/WAI/WCAG22/Techniques/html/H44)- [H64: Using the title attribute of the iframe element](https://www.w3.org/WAI/WCAG22/Techniques/html/H64)- [H65: Using the title attribute to identify form controls when the label element cannot be used](https://www.w3.org/WAI/WCAG22/Techniques/html/H65)- [H88: Using HTML according to spec](https://www.w3.org/WAI/WCAG22/Techniques/html/H88)

###### Situation B: If using script or code to re-purpose a standard user interface component in a markup language:

- Exposing the names and roles, allowing user-settable properties to be directly set, and providing notification of changes using one of the following techniques:
  - [ARIA16: Using aria-labelledby to provide a name for user interface controls](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA16)

###### Situation C: If using a standard user interface component in a programming technology:

- [G135: Using the accessibility API features of a technology to expose names and roles, to allow user-settable properties to be directly set, and to provide notification of changes](https://www.w3.org/WAI/WCAG22/Techniques/general/G135) using one or more of the following techniques:
  - [PDF10: Providing labels for interactive form controls in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF10)- [PDF12: Providing name, role, value information for form fields in PDF documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF12)

###### Situation D: If creating your own user interface component in a programming language:

- [G10: Creating components using a technology that supports the accessibility API features of the platforms on which the user agents will be run to expose the names and roles, allow user-settable properties to be directly set, and provide notification of changes](https://www.w3.org/WAI/WCAG22/Techniques/general/G10) using one or more of the following techniques:
  - [ARIA4: Using a WAI-ARIA role to expose the role of a user interface component](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA4)- [ARIA5: Using WAI-ARIA state and property attributes to expose the state of a user interface component](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA5)- [ARIA16: Using aria-labelledby to provide a name for user interface controls](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA16)

##### Failures for Success Criterion 4.1.2

- [F59: Failure of Success Criterion 4.1.2 due to using script to make div or span a user interface control in HTML without providing a role for the control](https://www.w3.org/WAI/WCAG22/Techniques/failures/F59)- [F15: Failure of Success Criterion 4.1.2 due to implementing custom controls that do not use an accessibility API for the technology, or do so incompletely](https://www.w3.org/WAI/WCAG22/Techniques/failures/F15)- [F20: Failure of Success Criterion 1.1.1 and 4.1.2 due to not updating text alternatives when changes to non-text content occur](https://www.w3.org/WAI/WCAG22/Techniques/failures/F20)- [F42: Failure of Success Criteria 1.3.1, 2.1.1, 2.1.3, or 4.1.2 when emulating links](https://www.w3.org/WAI/WCAG22/Techniques/failures/F42)- [F68: Failure of Success Criterion 4.1.2 due to a user interface control not having a programmatically determined name](https://www.w3.org/WAI/WCAG22/Techniques/failures/F68)- [F79: Failure of Success Criterion 4.1.2 due to the focus state of a user interface component not being programmatically determinable or no notification of change of focus state available](https://www.w3.org/WAI/WCAG22/Techniques/failures/F79)- [F86: Failure of Success Criterion 4.1.2 due to not providing names for each part of a multi-part form field, such as a US telephone number](https://www.w3.org/WAI/WCAG22/Techniques/failures/F86)- [F89: Failure of Success Criteria 2.4.4, 2.4.9 and 4.1.2 due to not providing an accessible name for an image which is the only content in a link](https://www.w3.org/WAI/WCAG22/Techniques/failures/F89)- [F111: Failure of Success Criteria 1.3.1, 2.5.3, and 4.1.2 due to a control with visible label text but no accessible name](https://www.w3.org/WAI/WCAG22/Techniques/failures/F111)

In content implemented using markup languages, status messages can be programmatically determined through role or properties such that they can be presented to the user by assistive technologies without receiving focus.

[Understanding 4.1.3](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)

Show Hide techniques and failures for 4.1.3

##### Sufficient Techniques for Success Criterion 4.1.3

Note: Other techniques may also be sufficient if they meet the success criterion. See [Understanding Techniques.](https://www.w3.org/WAI/WCAG22/Understanding/understanding-techniques)

###### Situation A: If a status message advises on the success or results of an action, or the state of an application:

- [ARIA22: Using role=status to present status messages](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA22) in combination with any of the following techniques:
  - [G199: Providing success feedback when data is submitted successfully](https://www.w3.org/WAI/WCAG22/Techniques/general/G199)

###### Situation B: If a status message conveys a suggestion, or a warning on the existence of an error:

- [ARIA19: Using ARIA role=alert or Live Regions to Identify Errors](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA19) in combination with any of the following techniques:
  - [G83: Providing text descriptions to identify required fields that were not completed](https://www.w3.org/WAI/WCAG22/Techniques/general/G83)- [G84: Providing a text description when the user provides information that is not in the list of allowed values](https://www.w3.org/WAI/WCAG22/Techniques/general/G84)- [G85: Providing a text description when user input falls outside the required format or values](https://www.w3.org/WAI/WCAG22/Techniques/general/G85)- [G177: Providing suggested correction text](https://www.w3.org/WAI/WCAG22/Techniques/general/G177)- [G194: Providing spell checking and suggestions for text input](https://www.w3.org/WAI/WCAG22/Techniques/general/G194)

*Note:* Not all examples in the preceding general techniques use status messages to convey warnings or errors to users. A role of "alert" is only necessary where a change of context does *not* take place.

###### Situation C: If a status message conveys information on the progress of a process:

- [ARIA23: Using role=log to identify sequential information updates](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA23)- Using `role="progressbar"` (future link)- [ARIA22: Using role=status to present status messages](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA22) **AND** [G193: Providing help by an assistant in the web page](https://www.w3.org/WAI/WCAG22/Techniques/general/G193)

##### Advisory Techniques for Success Criterion 4.1.3

- Using aria-live regions with chat clients (future link)- Using aria-live regions to support [1.4.13 Content on Hover or Focus](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus) (future link)- Using `role="marquee"` (future link)- Using `role="timer"` (future link)- Where appropriate, moving focus to new content with [ARIA18: Using aria-alertdialog to Identify Errors](https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA18)- Supporting personalization with [SCR14: Using scripts to make nonessential alerts optional](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR14)

##### Failures for Success Criterion 4.1.3

- [F103: Failure of Success Criterion 4.1.3 due to providing status messages that cannot be programmatically determined through role or properties](https://www.w3.org/WAI/WCAG22/Techniques/failures/F103)- Using `role="alert"` or `aria-live="assertive"` on content which is not important and time-sensitive (future link)

---

Contribute

We welcome feedback and suggestions:

- This resource — [report bugs](https://github.com/w3c/wai-wcag-quickref/issues/) and contribute directly to the [Github repository](https://github.com/w3c/wai-wcag-quickref)- [Instructions for Commenting on WCAG 2 Documents](https://www.w3.org/WAI/standards-guidelines/wcag/commenting/)