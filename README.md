# LeanWAM

**Learning Latent World Action Models from Frozen Video Models**  
Shaolong Li, Hongze Fu, Yinpei Dai, and Joyce Chai · University of Michigan

The [public project page](https://shaolonl-16.github.io/leanwam/) hosts the paper, the model overview, the success rate versus latency comparison, results on LIBERO, LIBERO-Plus, and RoboTwin 2.0, and visualizations of predictive codes and attention. Visitors can access it without a GitHub account.

## Get a local copy

Run these commands once from the directory on your computer where you keep projects. Open the resulting `leanwam` folder in your editor.

```bash
git clone https://github.com/shaolonl-16/leanwam.git
cd leanwam
```

If you already cloned this repository, open your existing clone and run `git pull --ff-only` before editing. You can check the repository URL with `git remote -v`.

## Update links, citation, and paper

Paths below are relative to the root of the `leanwam` clone.

| To update | Edit | What to enter |
| --- | --- | --- |
| Author homepages | `authors` in `site.config.js` | Set `shaolong`, `hongze`, `yinpei`, and `joyce` to the corresponding authors' full homepage URLs. |
| arXiv button | `links.arxiv` in `site.config.js` | Use the paper's abstract URL, such as `https://arxiv.org/abs/<arXiv-ID>`. |
| Code button | `links.code` in `site.config.js` | Use the URL of the repository containing the model code. |
| PDF button | `links.pdf` in `site.config.js` | Keep `assets/paper/LeanWAM.pdf` to serve the bundled paper, or enter an external PDF URL. |
| Bundled paper | `assets/paper/LeanWAM.pdf` | Replace this file with the new manuscript, keeping the same capitalization and filename. The existing button and direct PDF URL will serve the new version after deployment. |
| Citation | `bibtex` in `site.config.js` | Paste the complete BibTeX entry between the two backticks after `String.raw`. Keep the entry's line breaks, braces, and backslashes. |

Empty author URLs leave the names as plain text. Empty arXiv and Code URLs display **Soon**. Adding a BibTeX entry enables **Copy BibTeX** and **Download .bib** on the page.

## Preview changes

Open `index.html` in your browser, or run the following from the repository root and visit <http://localhost:8765/>. Press `Ctrl+C` to stop the server.

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

When working over VS Code Remote SSH, forward port `8765` in the **Ports** panel. Click each updated link, open the PDF, and check the citation before publishing.

## Publish an update

After saving your changes, run these commands inside your `leanwam` clone. The example stages the link and citation configuration, paper PDF, and README. Include any other files you intentionally edited in the `git add` command.

```bash
git status --short
git add -- site.config.js assets/paper/LeanWAM.pdf README.md
git diff --cached --stat
git commit -m "Update paper, citation, and project links"
git push origin main
```

GitHub Pages deploys updates from `main` using the repository root. Follow the deployment in [Actions](https://github.com/shaolonl-16/leanwam/actions), then open the [project page](https://shaolonl-16.github.io/leanwam/). To check the publishing source, open the repository's [Pages settings](https://github.com/shaolonl-16/leanwam/settings/pages) and look under **Build and deployment** for **Deploy from a branch**, `main`, and `/(root)`.

## Update figures, the abstract, or results tables

`index.html` contains the displayed text and tables. `assets/figures/` holds the original figure PDFs and the WebP images served by the page. `data/results.json` records the exported table values, and `data/sources.json` records the source file hashes and figure numbers.

To refresh these from revised LaTeX sources, install PyMuPDF and Pillow in a Python environment and run the exporter with the paths to the revised source directory and manuscript.

```bash
python scripts/prepare_paper.py --source ../LeanWAM_arxiv --pdf ../LeanWAM_arxiv.pdf
```

The exporter updates the bundled PDF, figure assets, generated abstract and tables, and data files. Review the hand-written figure descriptions and benchmark summary cards in `index.html` when results change. For a PDF-only revision, replacing `assets/paper/LeanWAM.pdf` is sufficient.

## Credits

The figures and results come from the LeanWAM manuscript. The project page design draws on [VPP2](https://robert-gyj.github.io/video-prediction-policy-2/) and [D4RT](https://d4rt-paper.github.io/). The bundled Inter font is distributed under the [SIL Open Font License](assets/fonts/LICENSE.txt).
