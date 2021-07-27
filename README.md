[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/EvanGottschalk/OperateExchangeGUI">
    <img src="logo.png" alt="Logo" width="151" height="80">
  </a>

  <h3 align="center">OperateExchangeGUI</h3>

  <p align="center">
    A GUI that allows the user to easily create, modify, and cancel array orders on cryptocurrency exchanges
    <br />
    <a href="https://github.com/EvanGottschalk/OperateExchangeGUI"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/EvanGottschalk/OperateExchangeGUI">View Demo</a>
    ·
    <a href="https://github.com/EvanGottschalk/OperateExchangeGUI/issues">Report Bug</a>
    ·
    <a href="https://github.com/EvanGottschalk/OperateExchangeGUI/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

`OperateExchangeGUI` displays an intricate, customizable interface for trading cryptocurrencies. Through the help of its partner program `OperateExchange`, users can create or cancel multiple orders with customizable parameters. This saves users the trouble of calculating price and volume related ratios, and then can execute their ideal array of orders with only a few clicks.**

** *Some exchanges have an API rate limit, which means you can only put in so many orders per time. Read the API limit rules for the particular exchange if you want to use `OperateExchangeGUI` or `OperateExchange` to create multiple orders on it.*

### Built With

`Python`

[`CCXT`](https://github.com/ccxt/ccxt) - The fantastic `CCXT` library is critical to this program. Huge thanks to [@kroitor](https://github.com/kroitor) and the many other `CCXT` contributors that made this program possible.

[`OperateExchange`](https://github.com/EvanGottschalk/OperateExchange) - This program is the brains behind `OperateExchangeGUI`. The buttons in the GUI all send commands to `OperateExchange`, which then interprets them, checks them, and finally executes them via `ConnectToExchange`. You can read more about it here: [https://github.com/EvanGottschalk/OperateExchange](https://github.com/EvanGottschalk/OperateExchange)

[`ConnectToExchange`](https://github.com/EvanGottschalk/connecttoexchange) - This program creates the initial connection to a cryptocurrency exchange. You can read more about it here: [github.com/EvanGottschalk/ConnectToExchange](https://github.com/EvanGottschalk/connecttoexchange)

[`GetCurrentTime`](https://github.com/EvanGottschalk/GetCurrentTime) - This program is imported to help collect time data in a legible fashion. It also allows for the translation of time stamps. You can read more about it here: [github.com/EvanGottschalk/GetCurrentTime](https://github.com/EvanGottschalk/GetCurrentTime)

[`AudioPlayer`](https://github.com/EvanGottschalk/AudioPlayer) - This is a simple program for playing custom audio alerts. It can be used with `ConnectToExchange` to warn you if an error occurs. You can read more about it here: [github.com/EvanGottschalk/AudioPlayer](https://github.com/EvanGottschalk/AudioPlayer)

`QuadraticFormula` - This is a simple program for calculating the solutions to a quadratic equation using the quadratic formula.

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Before using `OperateExchangeGUI`, you must first obtain an API key and secret from the cryptocurrency exchange of their choosing. You also need to install the [`CCXT`](https://github.com/ccxt/ccxt) library. If your API key is `view-only`, you can still use `OperateExchangeGUI` to calculate & graph groups of orders with custom ratios. If it has `trade` priveleges, then those orders can be executed and canceled as well.

### Installation

1. Install [`CCXT`](https://github.com/ccxt/ccxt). This can be done in a number of ways. I used `pip`.
   ```sh
   pip install ccxt
   ```
2. Download the `.py` files from this repository (`OperateExchangeGUI.py`,`OperateExchange.py`, `ConnectToExchange.py`, `GetCurrentTime.py`, `QuadraticFormula.py`, and optionally `AudioPlayer.py`)

3. In the same folder as `ConnectToExchange.py`, create a `.txt` file to store your API information. Its name should start with the exchange you are using, followed by an underscore, followed by the name of the account you're using, and ending with `_API.txt`.

  For example, if you are using your **Main** account on **Coinbase**, you would name the `.txt` file **`Coinbase_Main_API.txt`**

  If your API key is `view-only`, you can save your cryptocurrency exchange API key on the 1st line, and your API secret on the 2nd. However, **if your API key has `trade` priveleges, you should save an encrypted version of both your key and secret on those lines instead.**

  To encrypt your API information, I recommend using `CustomEncryptor.py`, which can be downloaded here: [github.com/EvanGottschalk/CustomEncryptor](https://github.com/EvanGottschalk/CustomEncryptor)

4. Run `OperateExchangeGUI.py`

5. Congratulations! You can now use `OperateExchangeGUI` to calculate, graph, create and cancel orders on your chosen cryptocurrency exchange!



<!-- USAGE EXAMPLES -->
## Usage

Users can customize, create & execute orders using the GUI. Here's what it looks like:

<br />
<p align="center">
  <a href="https://github.com/EvanGottschalk/OperateExchangeGUI">
    <img src="screenshots/GUI_with_1_order.PNG" alt="GUI_screenshot">
  </a>
</p>



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/EvanGottschalk/OperateExchangeGUI/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the GNU GPL-3 License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Evan Gottschalk - [@Fort1Evan](https://twitter.com/Fort1Evan) - magnus5557@gmail.com

Project Link: [https://github.com/EvanGottschalk/OperateExchangeGUI](https://github.com/EvanGottschalk/OperateExchangeGUI)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* Huge thanks to [@kroitor](https://github.com/kroitor) and the many other [CCXT](https://github.com/ccxt/ccxt) contributors that made this program possible.
* Thanks to [@bartmassi](https://github.com/bartmassi) for working with me to improve the program's security, and for answering numerous other questions, and also for always being a helpful, available, and informative teacher (and friend).

Thinking about contributing to this project? Please do! Your Github username will then appear here.





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/EvanGottschalk/OperateExchangeGUI.svg?style=for-the-badge
[contributors-url]: https://github.com/EvanGottschalk/OperateExchangeGUI/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/EvanGottschalk/OperateExchangeGUI.svg?style=for-the-badge
[forks-url]: https://github.com/EvanGottschalk/OperateExchangeGUI/network/members
[stars-shield]: https://img.shields.io/github/stars/EvanGottschalk/OperateExchangeGUI.svg?style=for-the-badge
[stars-url]: https://github.com/EvanGottschalk/OperateExchangeGUI/stargazers
[issues-shield]: https://img.shields.io/github/issues/EvanGottschalk/OperateExchangeGUI.svg?style=for-the-badge
[issues-url]: https://github.com/EvanGottschalk/OperateExchangeGUI/issues
[license-shield]: https://img.shields.io/github/license/EvanGottschalk/OperateExchangeGUI.svg?style=for-the-badge
[license-url]: https://github.com/EvanGottschalk/OperateExchangeGUI/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/EvanGottschalk