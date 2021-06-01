# original plugin from Uniborg.
# credits to original creator|s.
# ported to ultroid by [eris.]

"""   
**Get Weather Data using OpenWeatherMap API**
✘  Commands Available -
•  {i}weather <Detailed forecast, needs API>
•  {i}wttr <Works without API key, less details> 

Usage: `{i}weather <Location> | {i}wttr <Location>`
"""

import io
import time
from datetime import datetime, tzinfo
import aiohttp

from . import *


@ultroid_cmd(pattern="weather ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    eris = await eor(event, "`Processing...`")
    url = "https://api.openweathermap.org"
    sample_url = "https://api.openweathermap.org/data/2.5/weather?q={}&APPID={}&units=metric"
    x = Redis("OPENWEATHER_API")
    if x == None:
        error = f"No API found. Get One from [Here]({url}) \n"
        error += "And Add it in `OPENWEATHER_API` Redis Key"
        await eris.edit(error)
        return
    input_str = event.pattern_match.group(1)
    if not input_str:
        await eris.edit("`No Location was Given..`")
        return
    async with aiohttp.ClientSession() as session:
        response_api_zero = await session.get(sample_url.format(input_str, x))
    response_api = await response_api_zero.json()
    if response_api["cod"] == 200:
        country_code = response_api["sys"]["country"]
        country_time_zone = int(response_api["timezone"])
        sun_rise_time = int(response_api["sys"]["sunrise"]) + country_time_zone
        sun_set_time = int(response_api["sys"]["sunset"]) + country_time_zone
        await eris.edit(
            """**Weather for {}**\n
• **Temperature :** {}°С
    •  __minimium__ : {}°С
    •  __maximum__ : {}°С
    •  __feels like__ :{}°C \n
• **Humidity :** {}%
• **Wind Speed :** {}m/s
• **Clouds :** {} hpa
• **Pressure :** {}mb
• **Visibility :** {}m \n
• **Sunrise :** {}
• **Sunset :** {}""".format(
                input_str,
                response_api["main"]["temp"],
                response_api["main"]["temp_min"],
                response_api["main"]["temp_max"],
                response_api["main"]["feels_like"],
                response_api["main"]["humidity"],
                response_api["wind"]["speed"],
                response_api["clouds"]["all"],
                response_api["main"]["pressure"],
                response_api["visibility"],
                time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(sun_rise_time)),
                time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(sun_set_time)),
            )
        )
    else:
        await eris.edit(response_api["message"])



@ultroid_cmd(pattern="wttr ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    sample_url = "https://wttr.in/{}.png"
    input_str = event.pattern_match.group(1)
    if not input_str:
        await event.edit("No Location given 🤧")
        return
    async with aiohttp.ClientSession() as session:
        response_api_zero = await session.get(sample_url.format(input_str))
        response_api = await response_api_zero.read()
        with io.BytesIO(response_api) as out_file:
            await event.reply(
                file=out_file
            )
    await event.edit(input_str)


HELP.update({f"{__name__.split('.')[1]}": f"{__doc__.format(i=HNDLR)}"})
