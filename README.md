# internet-speed-log

Track your internet speed over time.

-----

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Logging](#logging)
  - [Plotting](#plotting)
- [License](#license)

## Installation

Bash (Linux):

```bash
python3 venv env
source env/bin/activate
pip3 install -r requirements.txt
```

PowerShell (Windows):

```powershell
python venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
```

CMD (Windows):

```cmd
python venv env
.\env\Scripts\activate.bat
pip install -r requirements.txt
```

## Usage

Bash (Linux):

```bash
source env/bin/activate
internet-speed-log
```

PowerShell (Windows):

```powershell
.\env\Scripts\Activate.ps1
internet-speed-log
```

CMD (Windows):

```cmd
.\env\Scripts\activate.bat
internet-speed-log
```

### Logging

```console
internet-speed-log log
```

### Plotting

```console
internet-speed-log plot
```

Or to plot a specific renamed log file:

```console
internet-speed-log plot log-file.txt
```

## License

`internet-speed-log` is distributed under the terms detailed in [the LICENCE file](LICENCE.txt).  
Here is a (non-binding) summary:

What you can do:

- Read, download, and enjoy the source code.
- Modify it privately for yourself, your household, or family.
- Submit improvements or ideas via pull requests to the official GitHub repository.

What you cannot do (without written permission):

- Redistribute the code outside of your household, or family (modified or unmodified) outside this repository.
- Publish or share your modified versions publicly.
- Use the code commercially unless you have received explicit written approval.

About contributions:

- Pull requests are welcome.
- Attribution is given at the author’s discretion for contributions that are accepted and retained in a release.
- Contributions confer no ownership of the project.

Other notes:

- The author may change the license in future versions.
- The author is the final arbiter of any uncertainties.
- All rights not expressly granted remain reserved.
