# snips-clock: An interactive audible clock

This is a very simple [snips](https://snips.ai/) skill to announce the current time.
Two modes of operation are supported:

* You can ask for the current date / time,
* Regular announcements via `cron` jobs,
* Clock chimes, either plain or a full set of Big Ben chimes.
* An example [crontab](clock.contab) is included.

## Basic usage

For simple time announcements (in English or German) run `setup.sh`,
activate the virtual environment and then call:

    ./action-clock.py --site <site-name>

The language is automatically selected according to the system locale.

To ring an hourly churchbell chime:

    ./action-clock.py --site <site-name> --chime DEFAULT

To ring an the hours:

    ./action-clock.py --site <site-name> --chime chimes

## Big Ben

Call the following at :59, :00, :15, :30 and :45 minutes:

    ./action-clock.py --site <site-name> --chime bigben_intro  # :59
    ./action-clock.py --site <site-name> --chime bigben_full   # :00
    ./action-clock.py --site <site-name> --chime bigben_15     # :15
    ./action-clock.py --site <site-name> --chime bigben_30     # :30
    ./action-clock.py --site <site-name> --chime bigben_45     # :45

## Configuration

See [config.ini.default](config.ini.default) for all possible values.
The configuration consists of site (`--site`) and chime (`--chime`) sections.
Default values for both are given in the `[DEFAULT]` section.

### Site sections:

* `volume`: Percentage value to lower the volume,
* `presence_topic`: MQTT topic to gather presence announcements. Announcements or chimes will play only if any of the message payloads evaluates to `true` in JSON,
* `presence_pattern`: Regex to filter  presence announcements, defaults to `.*`.

### Chime sections

* `chime`: Path to `.wav` audio file, defaults to a plain churchbell sound,
* `hours`: Boolean to ring the number of hours, using a 12 hour clock,
* `delay`: Integer, wait as many seconds before starting to chime,
* `spacing`: Float, wait as many seconds between chimes.

## Credits

* The hourly Big Ben chimes are courtesy of [UK Parliament](https://old.parliament.uk/about/living-heritage/building/palace/big-ben/anniversary-year/downloads/),
* the default clock chime is courtesy of [Daniel Simion](http://soundbible.com/2170-Clock-Chimes-4x.html).
