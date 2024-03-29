# Aglish

Read in: [العربية](README.ar.md)

---

<img src="./images/logo-256w.png">

[Anki](https://apps.ankiweb.net/) add-on for [YouGlish](https://youglish.com/); a YouTube search engine
for language learning that helps you learn vocabulary in context.

![YouGlish Widget](./images/youglish-widget.png)

YouGlish supports many languages and customizations of the interface. This add-on supports all languages supported by YouGlish and customizations.

## Usage

The add-on integrates YouGlish with Anki through a custom filter you put in your [card templates](https://docs.ankiweb.net/templates/intro.html) (e.g. `{{aglish:Front}}`).

Its usage is quite simple. Let's go through some examples:

-   `{{aglish lang=english accent=uk:Front}}`  
    This will show you video usage examples of the text in your Front field in British English.
-   The video widget will be hidden behind a button by default.
    You can change the text shown on the button via the `label` option (no spaces allowed for now):  
    `{{aglish lang=english accent=uk label=youglish_english_uk:Front}}`
-   Alternatively, You can make the video play automatically by using the `autoplay` option:  
    `{{aglish lang=english accent=uk autoplay:Front}}`  
    Bear in mind that if you review a lot of cards quickly with autoplay enabled, you may get temporarily blocked or
    asked to solve a captcha. It's recommended to enable autoplay only when the main focus of your note type is the YouGlish videos,
    so that you won't go to the next card before watching a clip, or you will be just answering cards without thinking.
-   You can combine Anki's `cloze-only` filter with the `aglish` filter to query only elided sections in cloze note types:  
    `{{aglish lang=english:cloze-only:Text}}`
-   The `cloze-only` filter only works on the back side, so this add-on provides a similar option (`clozeonly`) that works on both sides as a bonus:  
    `{{aglish lang=english clozeonly:Text}}`
-   The `nocaps` option is useful here to hide captions when watching clips containing elided text in the front side:  
    `{{aglish lang=english clozeonly nocaps:Text}}`
-   You can also change the widget theme using the `theme` option:  
    `{{aglish theme=dark:Text}}`  
     Available values are `light`, `dark`, and `anki` (theme used in Anki's interface, the default).
-   The width and height of the widget can be customized using the `width` and `height` options:  
    `{{aglish lang=arabic width=600 height=500:Front}}`  
     The widget will expand to the window size if these options are not specified.
-   You can enable "Restricted mode" to block potentially inappropriate content to be displayed (aka Kids Mode)
    by setting the "restrict" option, like this:
    `{{aglish restrict:Front}}`
-   You can set hotkeys to trigger non-autoplayed widgets using the `hotkey` option:  
    `{{aglish hotkey=k:Front}}`  
    Only single keys work for now. (no combinations like `Ctrl+K`)  
    You can alternatively set a similar `hotkey` config option under _Tools > Add-ons > Config_ to trigger all non-autoplayed widgets without having to specify the hotkey in each filter.

All options have default values so they can be omitted; `{{aglish:Front}}` assumes English in all accents, showing a widget in Anki's theme with captions.

For a list of all supported languages and accents, see [YouGlish documentation](https://youglish.com/api/doc/js-api) (scroll down to the documentation of the `widget.fetch` function).

### Widget Components

You can toggle widget's components like the search bar via the config's `components` key (_Tools > Add-ons > Config_). See [this page](https://youglish.com/api/doc/widget) to experiment with available components. For example to hide the search bar, you can set `search_box` to `false`:

```json
    "components": {
        "search_box": false,
        ...
        ...
    }
```

### Styling

You can style the buttons by targeting the `yg-btn` CSS class in the styling section. E.g.

```css
.yg-btn {
    opacity: 0.8;
    background-color: #c11615;
    color: white;
    border: 1px solid black;
    border-radius: 5px;
}

.yg-btn:hover {
    box-shadow: 1px 1px 1px black;
}
```

## Demo

Watch [this video](https://www.youtube.com/watch?v=aqc98e5ar64) for a demo of the add-on.

## Experimental Support for YouGlish login

I've recently added experimental support to allow users to use their YouGlish account and premium subscription plans in the add-on. This is not tested. I appreciate if someone can test it with their premium plan and tell me about the result.

To use your YouGlish account with the add-on, go to _Tools > Aglish > Log in to YouGlish_.
You'll be presented with the YouGlish login page. After logging in successfully, you can close the window.
The add-on will now use your login information when showing the widget on cards.

## References

YouGlish widget API:

-   https://youglish.com/api/doc/widget
-   https://youglish.com/api/doc/js-api

## YouGlish & YouTube Terms of Service

You may want to read the Privacy & Terms of Service pages of both YouGlish and YouTube:

-   https://youglish.com/terms
-   https://www.youtube.com/t/terms
-   https://policies.google.com/privacy

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes.

## Support & feature requests

Please post any questions, bug reports, or feature requests in the [support page](https://forums.ankiweb.net/t/aglish-youglish-widget-for-anki-official-thread/14503) or the [issue tracker](https://github.com/abdnh/aglish/issues).

If you want priority support for your feature/help request, I'm available for hire.
You can get in touch from the aforementioned pages, via [email](mailto:abdo@abdnh.net) or on [Fiverr](https://www.fiverr.com/abd_nh).

## Support me

Consider supporting me if you like my work:

<a href="https://github.com/sponsors/abdnh"><img height='36' src="https://i.imgur.com/dAgtzcC.png"></a>
<a href="https://www.patreon.com/abdnh"><img height='36' src="https://i.imgur.com/mZBGpZ1.png"></a>
<a href='https://ko-fi.com/abdnh'><img height='36' src='https://cdn.ko-fi.com/cdn/kofi1.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

I'm also available for freelance add-on development on Fiverr:

<a href="https://www.fiverr.com/abd_nh/develop-an-anki-addon"><img height='36' src="https://i.imgur.com/0meG4dk.png"></a>
