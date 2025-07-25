"""
TODO:
- Filter by empire and claim, add string names to the channel name
"""

import colorsys
import json
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from PIL import Image, ImageEnhance

from bitcraft_explorer.helpers import subscribe_to_query_generator

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

avatar_url_list = [
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306011835797708/spirit_chat_var_01.png?ex=6884e174&is=68838ff4&hm=dfda4c56eedc36d112d39ec0d27eec01e261692d13775f7f22159dcb15c96f18&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306012225736714/spirit_chat_var_02.png?ex=6884e174&is=68838ff4&hm=fc7fa0c9cf24525a32aa4cc77e90dc26f8724b22f3a269f2e74f322b38924499&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306012624326736/spirit_chat_var_03.png?ex=6884e174&is=68838ff4&hm=c2ec6430920b0cebb5a0e860163d5792fac9efe42873cf1c01495caa7c9a4f12&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306013077307542/spirit_chat_var_04.png?ex=6884e174&is=68838ff4&hm=363c7ce1ff500692e3b520172dea104ee803b6d51b66f3565e94839a8d57f5bd&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306013467250759/spirit_chat_var_05.png?ex=6884e174&is=68838ff4&hm=72ba6ae7c971c8c5695ac239b8e5dfd33ff5ca0ce70b2abbbf8dcfbeffc98ee2&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306013815373844/spirit_chat_var_06.png?ex=6884e174&is=68838ff4&hm=54078ad724af55c6e68bf4ac897220f047698e0486411cc044b53b84beb766f6&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306014410834010/spirit_chat_var_07.png?ex=6884e175&is=68838ff5&hm=975fd337d773e198c5680c8939246754cb5dd10c45724407905332f7150c89bc&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306014864080956/spirit_chat_var_08.png?ex=6884e175&is=68838ff5&hm=8fc65ce149c1a39e12b07ee7ecea29a3547110978bf128050b0e98191963cee7&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306015287578634/spirit_chat_var_09.png?ex=6884e175&is=68838ff5&hm=d42f457024f94e9da2880d9637b378a08c34d7c5ce51ee8ca1b078d9a0746530&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306015740694628/spirit_chat_var_10.png?ex=6884e175&is=68838ff5&hm=671259f541ce1071a1e6495fbe21c786f106fb6b0ae7e7f00b620f526a8652fb&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306261086371890/spirit_chat_var_11.png?ex=6884e1af&is=6883902f&hm=67daa9b4c084762223f2d8439566c27cb8d7da145b08e40193e7724bfbdb3057&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306261627306146/spirit_chat_var_12.png?ex=6884e1b0&is=68839030&hm=0f4fb33dc1d723613eb502592d3260bba001f50a12a162661760552357d8a2cb&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306262109655060/spirit_chat_var_13.png?ex=6884e1b0&is=68839030&hm=8f67d030023e84888cb4008989abff88a49c67fd389ec4eb2c442280bb0822d1&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306262537601199/spirit_chat_var_14.png?ex=6884e1b0&is=68839030&hm=ee62b7a64e7b0d8fc3424c700a5a55e7b809acbb2557c9ea4b321c7eefb79b47&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306263044980879/spirit_chat_var_15.png?ex=6884e1b0&is=68839030&hm=8a64107b8c413d99c2d22578e08cbaba38faa6b793f1391e08cdf966a234185b&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306263544238092/spirit_chat_var_16.png?ex=6884e1b0&is=68839030&hm=22cec28c029df6a1e4476dab6124d36a9a407afe7916ca57db811cce7bef1347&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306264076779632/spirit_chat_var_17.png?ex=6884e1b0&is=68839030&hm=28c2955623d3533c07075aa68ea53991c74f08fee16932f42ce5ed1397236e3b&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306264429236395/spirit_chat_var_18.png?ex=6884e1b0&is=68839030&hm=9fadadb7267d3bd0635af90358c8f332e6fa6cf8d781260c311d969e58c52021&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306264831754260/spirit_chat_var_19.png?ex=6884e1b0&is=68839030&hm=78fcca5386fed2b6d42b946cc2e85c23a6ebdc6e44f441a23a2e451da66bfe24&",
    "https://cdn.discordapp.com/attachments/353241001583837191/1398306265238605921/spirit_chat_var_20.png?ex=6884e1b0&is=68839030&hm=ed254aa97f08983fadcbfb3e976583733a82d79cc780cdd30bd73bfe575250fa&",
]

def pick_avatar_url(author: str) -> str:
    return avatar_url_list[hash(author) % len(avatar_url_list)]


def send_webhook(msg: str, author: str, channel: str, avatar_url: str) -> None:
    webhook_data = {
        "content": msg,
        "username": f"{channel} - {author}",
        "avatar_url": avatar_url,
    }

    r = httpx.post(
        DISCORD_WEBHOOK_URL,
        json=webhook_data,
    )
    r.raise_for_status()


def chat_to_discord(channel_id_filters: dict[int, str] | None = None) -> None:
    chat_lookup = {3: "region", 4: "claim", 5: "empire", 2: "local"}
    for msg in subscribe_to_query_generator("select * from chat_message_state where timestamp > 1753422348"):
        if "TransactionUpdate" in msg:
            message_obj = json.loads(msg["TransactionUpdate"]["status"]["Committed"]["tables"][0]["updates"][0]["inserts"][0])

            author = message_obj[1]
            channel_type = message_obj[3]
            channel_id = message_obj[4]
            chat_message = message_obj[5]

            if channel_type == 2 and channel_id_filters and channel_id not in channel_id_filters:
                continue

            if channel_type == 2 and channel_id_filters:
                channel_str = f"[{chat_lookup[channel_type]}:{channel_id_filters[channel_id]}]"
            else:
                channel_str = f"[{chat_lookup[channel_type]}:{channel_id}]"

            print(f"{channel_str} <{author}> {chat_message}")
            send_webhook(chat_message, author, channel_str, avatar_url=pick_avatar_url(channel_str))


def generate_avatar(filename: str, n_variations: int = 5, *, change_background: bool = True, dramatic_differences: bool = True) -> list[str]:
    """
    Generate n different color variations of an image with hue and color changes.

    Args:
        filename: Path to the input image file
        n_variations: Number of color variations to generate (default: 5)
        change_background: Whether to change white background to match hue shifts (default: True)
        dramatic_differences: Whether to use dramatic color differences for easy chat identification (default: True)

    Returns:
        List of generated file paths
    """
    # Load the original image
    original_path = Path(filename)
    if not original_path.exists():
        msg = f"Image file not found: {filename}"
        raise FileNotFoundError(msg)

    image = Image.open(original_path)

    # Convert to RGBA to ensure we can handle transparency
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    generated_files = []
    base_name = original_path.stem
    extension = original_path.suffix
    output_dir = original_path.parent / "output"
    output_dir.mkdir(exist_ok=True)

    for i in range(n_variations):
        # Create a copy to modify
        modified_image = image.copy()

        # Convert to RGB for color manipulation (preserve alpha separately)
        alpha = modified_image.split()[-1] if modified_image.mode == "RGBA" else None
        rgb_image = modified_image.convert("RGB")

        # Apply different modifications for each variation
        variation_factor = i / max(1, n_variations - 1)  # 0 to 1

        if dramatic_differences:
            # More dramatic changes for easy chat identification
            # Calculate hue shift across wider spectrum
            hue_shift = (variation_factor * 300) / 360  # 0 to 300 degrees (full spectrum except back to start)

            # 1. Replace white background with a tinted color that matches the hue shift
            if change_background:
                rgb_image = _replace_white_background(rgb_image, hue_shift)

            # 2. Apply hue shift to the entire image
            rgb_image = _shift_hue(rgb_image, hue_shift)

            # 3. Dramatic saturation changes
            saturation_factor = 0.3 + (variation_factor * 1.5)  # 0.3 to 1.8
            enhancer = ImageEnhance.Color(rgb_image)
            rgb_image = enhancer.enhance(saturation_factor)

            # 4. Significant brightness adjustments
            brightness_factor = 0.6 + (variation_factor * 0.8)  # 0.6 to 1.4
            enhancer = ImageEnhance.Brightness(rgb_image)
            rgb_image = enhancer.enhance(brightness_factor)

            # 5. Notable contrast adjustments
            contrast_factor = 0.7 + (variation_factor * 0.8)  # 0.7 to 1.5
            enhancer = ImageEnhance.Contrast(rgb_image)
            rgb_image = enhancer.enhance(contrast_factor)

            # 6. Add special effects for some variations
            if n_variations > 2:
                special_effect_index = i % 4
                if special_effect_index == 0 and i > 0:
                    # High contrast, desaturated look
                    rgb_image = ImageEnhance.Color(rgb_image).enhance(0.2)
                    rgb_image = ImageEnhance.Contrast(rgb_image).enhance(1.8)
                elif special_effect_index == 1 and i > 0:
                    # Warm tone boost
                    rgb_image = _apply_color_filter(rgb_image, (1.2, 1.1, 0.9))
                elif special_effect_index == 2 and i > 0:
                    # Cool tone boost
                    rgb_image = _apply_color_filter(rgb_image, (0.9, 1.0, 1.3))
                elif special_effect_index == 3 and i > 0:
                    # High saturation, vivid look
                    rgb_image = ImageEnhance.Color(rgb_image).enhance(2.0)
        else:
            # Subtle changes (original behavior)
            hue_shift = (variation_factor * 60 - 30) / 360  # ±30 degrees

            # 1. Replace white background with a tinted color that matches the hue shift
            if change_background:
                rgb_image = _replace_white_background(rgb_image, hue_shift)

            # 2. Apply hue shift to the entire image
            rgb_image = _shift_hue(rgb_image, hue_shift)

            # 3. Subtle saturation changes
            saturation_factor = 0.8 + (variation_factor * 0.4)  # 0.8 to 1.2
            enhancer = ImageEnhance.Color(rgb_image)
            rgb_image = enhancer.enhance(saturation_factor)

            # 4. Slight brightness adjustments
            brightness_factor = 0.9 + (variation_factor * 0.2)  # 0.9 to 1.1
            enhancer = ImageEnhance.Brightness(rgb_image)
            rgb_image = enhancer.enhance(brightness_factor)

            # 5. Minor contrast adjustments
            contrast_factor = 0.95 + (variation_factor * 0.1)  # 0.95 to 1.05
            enhancer = ImageEnhance.Contrast(rgb_image)
            rgb_image = enhancer.enhance(contrast_factor)

        # Restore alpha channel if it existed
        if alpha:
            rgb_image = rgb_image.convert("RGBA")
            rgb_image.putalpha(alpha)

        # Save the variation
        output_filename = f"{base_name}_var_{i+1:02d}{extension}"
        output_path = output_dir / output_filename
        rgb_image.save(output_path)
        generated_files.append(str(output_path))

        mode = "dramatic" if dramatic_differences else "subtle"
        print(f"Generated {mode} variation {i+1}/{n_variations}: {output_path}")

    return generated_files


def _shift_hue(image: Image.Image, hue_shift: float) -> Image.Image:
    """
    Shift the hue of an RGB image.

    Args:
        image: PIL Image in RGB mode
        hue_shift: Hue shift as a fraction (-1 to 1, where 1 = full rotation)

    Returns:
        Image with shifted hue
    """
    # Convert to HSV for hue manipulation
    image_array = image.load()
    width, height = image.size

    for x in range(width):
        for y in range(height):
            r, g, b = image_array[x, y]
            # Convert RGB to HSV
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            # Shift hue and wrap around
            h = (h + hue_shift) % 1.0
            # Convert back to RGB
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            image_array[x, y] = (int(r*255), int(g*255), int(b*255))

    return image


def _apply_color_filter(image: Image.Image, rgb_multipliers: tuple[float, float, float]) -> Image.Image:
    """
    Apply RGB color multipliers to create color filter effects.
    Args:
        image: PIL Image in RGB mode
        rgb_multipliers: Tuple of (red_mult, green_mult, blue_mult) multipliers
    Returns:
        Image with color filter applied
    """
    image_array = image.load()
    width, height = image.size
    red_mult, green_mult, blue_mult = rgb_multipliers

    for x in range(width):
        for y in range(height):
            r, g, b = image_array[x, y]
            # Apply multipliers and clamp to 0-255 range
            new_r = min(255, int(r * red_mult))
            new_g = min(255, int(g * green_mult))
            new_b = min(255, int(b * blue_mult))
            image_array[x, y] = (new_r, new_g, new_b)

    return image


def _replace_white_background(image: Image.Image, hue_shift: float, white_threshold: int = 240) -> Image.Image:
    """
    Replace white/near-white pixels with a tinted color that matches the hue shift.
    Args:
        image: PIL Image in RGB mode
        hue_shift: Hue shift as a fraction (-1 to 1, where 1 = full rotation)
        white_threshold: RGB threshold above which pixels are considered "white" (default: 240)
    Returns:
        Image with white background replaced by tinted color
    """
    # Create a base tinted color for the background
    # Start with a very light gray and apply the hue shift
    base_lightness = 0.95  # Very light background
    base_saturation = 0.15  # Subtle color tint

    # Calculate the target hue (shifted from neutral)
    target_hue = (0.0 + hue_shift) % 1.0  # Start from red (0) and shift

    # Convert to RGB for the background color
    bg_r, bg_g, bg_b = colorsys.hsv_to_rgb(target_hue, base_saturation, base_lightness)
    bg_color = (int(bg_r * 255), int(bg_g * 255), int(bg_b * 255))

    # Process each pixel
    image_array = image.load()
    width, height = image.size

    for x in range(width):
        for y in range(height):
            r, g, b = image_array[x, y]

            # Check if pixel is white/near-white (all RGB values above threshold)
            if r >= white_threshold and g >= white_threshold and b >= white_threshold:
                # Replace with tinted background color
                # Preserve some of the original brightness variation
                brightness_factor = min(r, g, b) / 255.0
                adjusted_bg = (
                    int(bg_color[0] * brightness_factor),
                    int(bg_color[1] * brightness_factor),
                    int(bg_color[2] * brightness_factor),
                )
                image_array[x, y] = adjusted_bg

    return image


def send_webhook_with_generated_avatar(msg: str, author: str, channel: str, base_avatar_path: str, variation_index: int = 0) -> None:
    """
    Send a webhook message using a generated avatar variation.
    Args:
        msg: Message content
        author: Author name
        channel: Channel name
        base_avatar_path: Path to the base avatar image
        variation_index: Which variation to use (0-based index)
    """
    # Generate avatar variations if they don't exist
    generated_files = generate_avatar(base_avatar_path, n_variations=5)

    # Use the specified variation (or first one if index is out of range)
    if variation_index < len(generated_files):
        avatar_file = generated_files[variation_index]
    else:
        avatar_file = generated_files[0]

    # Send webhook with the generated avatar
    send_webhook(msg, author, channel, avatar_file_path=avatar_file)
