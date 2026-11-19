# EuroMillions Number Picker

A free, single-page app for choosing EuroMillions numbers from the full draw history (every draw since 13 Feb 2004), with your own hot / cold / overdue notes.

**Live app:** `https://<your-username>.github.io/euromillions-picker/` (after you turn on GitHub Pages)

> Every combination has the same 1 in 139,838,160 chance of winning the jackpot. Past draws don't change future ones. This app can't raise your odds; it helps you avoid popular combinations (so a win is less likely to be shared), spread several tickets, and test any ticket against every past draw.

## Features

- **Number board**: green = drawn more often, red = less often; switch to "draws since last seen".
- **Analysis window**: Hybrid (last 2 years + 5 years + all-time, like LotoIA), all-time, last 5 / 2 years, last 700 / 500 / 200 / 100 draws.
- **Strategies**: My notes, Hot, Cold, Overdue, Balanced, Pure random.
- **Filters**: avoid birthday tickets, balanced odd/even and low/high, typical total, no runs, dodge the crowd, spread tickets.
- **Share-risk score** (0–100) for every ticket.
- **Backtest**: test any ticket against all past draws.
- **Saved tickets**, automatic check against the latest draw, odds table for all 13 prize tiers.
- **Auto-update**: a GitHub Action adds each new draw on Wednesday and Saturday mornings.

## Files

| File | What it is |
| --- | --- |
| `index.html` | The whole app (HTML, CSS and JavaScript in one file) |
| `draws.csv` | Every draw: `date,n1,n2,n3,n4,n5,s1,s2` |
| `meta.json` | Last update date and (optional) jackpot text |
| `scripts/update_draws.py` | Adds new draws to `draws.csv` (standard library only) |
| `.github/workflows/update-draws.yml` | Runs the update script twice a week |
| `.nojekyll` | Tells GitHub Pages to serve the files as they are |

## Run it locally

The page loads `draws.csv` with `fetch`, so open it through a small web server, not by double-clicking:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Data and credits

- Draw history: public EuroMillions results archive by [dev-baris/lottery-archive](https://github.com/dev-baris/lottery-archive), cross-checked against the all-time totals on lottery.co.uk.
- Ideas: Suetens, Galbo-Jørgensen & Tyran, *Predicting Lotto Numbers*; Stömmer, *Tackling the 6/49 Lottery*; Abrams & Garibaldi, *Finding good bets in the lottery, and why you shouldn't take them*; Bărboianu, *The Mathematics of Lottery*; [LotoIA generator](https://lotoia.fr/en/euromillions/generator).

Play only what you can afford to lose. France: Joueurs Info Service, 09 74 75 13 13.
