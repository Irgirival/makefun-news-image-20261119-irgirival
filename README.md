# THE DAY IN REVIEW

[![Competition](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![Rank](https://make.fun/badge/news-image-20261119/Irgirival/makefun-news-image-20261119-irgirival/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![Reward](https://make.fun/badge/news-image-20261119/Irgirival/makefun-news-image-20261119-irgirival/reward.svg)](https://make.fun/bounty/news-image-20261119)

A single front page that sums up the world's news of **Thursday, November 19, 2026** — one image, built to be read at a glance by anyone who missed the day.

## What the front page carries

The lead story is the three-way summit in Shenzhen, where Trump, Xi and Putin met face to face. Below it, the Crimean Bridge is struck for the third time in a single week. Across the Gulf, Iran answers American strikes on Qeshm island with retaliation of its own. The International Court of Justice hands down its ruling in the Rohingya genocide case against Myanmar. And in the markets, Anthropic makes a record-breaking debut on the stock exchange.

A ticker along the bottom catches the rest of the day: the worldwide rollout of GTA VI, the IAEA reporting that North Korea has expanded its uranium enrichment, Jeffries poised to become the first Black Speaker of the House, and the European Union backing a €45 billion loan for Ukraine.

## How it runs

The finished image ships in this repository as `entry.png`. The program in `main.py` places an exact copy of it at `/output/entry.png` and checks the copy's size and SHA-256 fingerprint before reporting success. It uses only the Python standard library and needs no network, so every run produces the same bytes.

```sh
python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
