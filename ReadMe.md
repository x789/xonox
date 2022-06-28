# xonox
In June 2022, Noxon(tm) decided to discontinue the infrastructure-services for legacy iRadio series devices.

`xonox` is an alternative for these infrastructure-services that you can easily host at home.

You need a device that is always-on, reachable by your iRadios and capable to run Python-scripts. Additionally, you need to redirect DNS entries to the device that runs `xonox`.

Because `xonox` is available via PyPi, the installation is rather easy.
But to configure its environment, you should have some basic knowledge of Internet technologies. You can find a configuration guide at `xonox`'s PyPI page.

- [`xonox` at PyPI](https://pypi.org/project/xonox)

## Note to developers
Make sure that your development environment has [Flask](https://pypi.org/project/Flask/) installed. The unit-tests require [pyfakefs](https://pypi.org/project/pyfakefs/).

(c) 2022 TillW - Licensed to you under the AGPL v3.0