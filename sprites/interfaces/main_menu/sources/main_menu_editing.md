# Editing the Main menu

The source file is menu-main.xcf which has all the layers.

**Before you start, make sure you have the Zekton font installed!**

Now you can make your changes to the main menu and export into the parent folder.

## menu.png

Hide the layers you don't need for your use-case (buttons, version etc.) and export.

## menu_buttons(_hover).png

Select the layer(s) and then use "Export Selected Layers" (in options, select "Export into one image").

To publish the images to production, nvcompress will produce artifacts, ImageMagick does a better job preserving fine details.

```
convert sprites/interfaces/main_menu/menu.png -resize 1024x1024! -define dds:compression=none sprites/interfaces/main_menu/menu.image
convert sprites/interfaces/main_menu/menu_buttons.png -define dds:compression=none sprites/interfaces/main_menu/menu_buttons.image
convert sprites/interfaces/main_menu/menu_buttons_hover.png -define dds:compression=none sprites/interfaces/main_menu/menu_buttons_hover.image
```
