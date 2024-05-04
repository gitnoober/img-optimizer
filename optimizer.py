import os

from PIL import Image, ImageFilter

from constants import ImageFormat


class ImageOptimizer:
    def __init__(
        self,
        infile: str,
        outfile: str,
        quality: int = 60,
        convert_to: str = ImageFormat.NATIVE.value,
        delta: int = 90,
    ) -> None:
        self.method_map = {
            ImageFormat.JPEG.value: self.convert_to_jpeg,
            ImageFormat.WEBP.value: self.convert_to_webp,
            ImageFormat.NATIVE.value: self.optimize_image,
        }
        self.infile = infile
        self.outfile = outfile
        self.quality = quality
        self.convert_to = convert_to
        self.delta = True

    def convert_to_jpeg(self) -> None:
        f, _ = os.path.splitext(self.infile)
        if not self.outfile:
            outfile = f + ".jpg"
        if self.infile != outfile:
            try:
                with Image.open(self.infile) as im:
                    im.save(outfile)
            except OSError:
                print("cannot convert", self.infile)

    def convert_to_webp(self) -> None:
        """Convert Image to WEBP

        Args:
            infile (str): _description_
        """
        pass

    def optimize_image(self) -> None:
        """Bare bone optimization

        Args:
            infile (str): _description_
        """
        pass

    def optimize(self) -> None:
        image_object = Image(self.infile)
        print(image_object.format, image_object.size, image_object.mode)

        image_object.show()
        return self.method_map[self.convert_to]()

    def indentify_image(self) -> None:
        try:
            with Image.open(self.infile) as im:
                print(self.infile, im.format, f"{im.size}x{im.mode}")
        except OSError:
            pass

    def crop_image(self) -> None:
        box = (100, 100, 400, 400)
        if self.outfile:
            outfile = f"cropped-{self.infile}"
        with Image.open(self.infile) as im:
            region = im.crop(box)
            im.save(outfile, region)

    def roll_image_sideways(self):
        """Roll an image sideways."""
        with Image.open(self.infile) as im:
            xsize, ysize = im.size

            delta = self.delta % xsize
            if delta == 0:
                return im

            part1 = im.crop((0, 0, delta, ysize))
            part2 = im.crop((delta, 0, xsize, ysize))
            im.paste(part1, (xsize - delta, 0, xsize, ysize))
            im.paste(part2, (0, 0, xsize - delta, ysize))

            im.show()
            return im

    def enhance_img(self):
        with Image.open(self.infile) as im:
            out = im.filter(ImageFilter.DETAIL)
            im.show()
            return out
