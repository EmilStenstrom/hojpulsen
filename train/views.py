import os
import math
import random
from urllib.parse import quote, urlencode

from django.http import Http404
from django.shortcuts import redirect, render

NUM_BLOCKS = 4
NUM_TIMESTEPS = 11
IMAGES = {
    "snake": {
        "src": "https://s7.orientaltrading.com/is/image/OrientalTrading/PDP_VIEWER_THUMB$&$NOWA/inflatable-snake~13675186",
        "base_path": "static/images/snake/",
    },
    # "spider": {
    #     "src": "https://cdn.shopify.com/s/files/1/1787/3171/products/Remote-Control-11-4CH-Realistic-RC-Spider-Scary-Toy-Prank-Holiday-Gift-Model-Hot-Sale_e1ace6fe-16b1-475f-8548-f58a8587133a_small.jpg",
    #     "base_path": "static/images/spider/",
    # },
}

def startpage(request):
    seconds = None
    if request.GET.get("seconds"):
        try:
            seconds = int(request.GET.get("seconds"))
        except ValueError:
            pass

    for image_name in IMAGES.keys():
        if request.POST.get(image_name + ".x"):
            blocks = sorted([
                (int(key[len("block"):]), value.replace("%", ""))
                for key, value in request.POST.items()
                if key.startswith("block")]
            )
            params = {
                "seconds": seconds,
                "image": image_name,
                "pace": ",".join(list(dict(blocks).values())),
            }
            return redirect("/slideshow?" + urlencode(params, safe=','))

    return render(request, "startpage.html", {
        "seconds": seconds,
        "timesteps": range(NUM_TIMESTEPS),
        "num_timesteps": NUM_TIMESTEPS - 1,
        "blocks": range(1, NUM_BLOCKS),
        "num_blocks": NUM_BLOCKS - 1,
        "images": IMAGES,
    })

def slideshow(request):
    try:
        seconds = int(request.GET.get("seconds", 0))
        if not seconds:
            raise Http404("Missing seconds")
    except ValueError:
        raise Http404("Missing seconds")

    image = request.GET.get("image", None)
    if (
        not image or
        image not in IMAGES.keys()
    ):
        raise Http404("Missing image")

    try:
        pace_list = [pace for pace in request.GET.get("pace", "").split(",")]
        if (
            not pace_list or
            not len(pace_list) == NUM_TIMESTEPS or
            not set(pace_list).issubset(set(["33", "67", "100"]))
        ):
            raise Http404("Missing pace")
    except ValueError:
        raise Http404("Missing pace")

    base_path = IMAGES[image]["base_path"]
    image_paths = {
        directory.replace(base_path, ""): images
        for directory, _, images in list(os.walk(base_path))[1:]
    }

    paths = []
    pace_per_second = []
    for second in range(seconds):
        pace = pace_list[math.floor((NUM_TIMESTEPS) * second / seconds)]
        paths.append(os.path.join("/", base_path, pace, random.choice(image_paths[pace])))
        pace_per_second.append(pace)

    return render(request, "slideshow.html", {
        "seconds": seconds,
        "start_minutes": ("0" if math.floor(seconds/60) < 9 else "") + str(math.floor(seconds/60)),
        "start_seconds": ("0" if seconds % 60 < 9 else "") + str(seconds % 60),
        "paths": paths,
        "pace_per_second": pace_per_second,
    })
