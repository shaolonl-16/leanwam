#!/usr/bin/env python3
"""Export the supplied paper assets and tables. Not needed to serve the website.

Usage: python scripts/prepare_paper.py --source ../LeanWAM_arxiv --pdf ../LeanWAM_arxiv.pdf
Requires: PyMuPDF and Pillow. Source files are only read, never modified.
"""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import shutil

import pymupdf
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ("overview", "efficiency", "code_umap", "query_attn")
BENCHMARKS = {
    "libero": {
        "title": "LIBERO",
        "description": "Four 10-task suites, with 500 evaluation episodes per suite. A single model is trained jointly on all four suites.",
        "legend": "PT: large-scale embodied pretraining. Size: number of parameters.",
    },
    "liberoplus": {
        "title": "LIBERO-Plus",
        "description": "Zero-shot evaluation over all 10,030 episodes and seven perturbation types. LeanWAM uses the LIBERO-trained checkpoint without further training.",
        "legend": "PT: large-scale embodied pretraining. Latency: milliseconds per action chunk on an A100, batch size 1. An en dash indicates unmeasured latency. Total follows the benchmark's overall aggregation, not an unweighted mean of the seven columns.",
    },
    "robotwin": {
        "title": "RoboTwin 2.0",
        "description": "The paper's 10 selected bimanual tasks, with 100 episodes per task in each setting. The model is jointly trained on clean and randomized demonstrations.",
        "legend": "Success rates averaged over the selected 10 tasks. Clean and Randomized refer to the two evaluation settings.",
    },
}


def plain_tex(value):
    value = re.sub(r"\\cite\{[^}]+\}", "", value)
    value = re.sub(r"\\rowcolor\{[^}]+\}", "", value)
    value = value.replace(r"\pi_{0.5}", "π₀.₅").replace(r"\pi_0", "π₀")
    value = value.replace(r"\pi", "π").replace(r"\alpha", "α")
    value = value.replace(r"\cmark", "Yes").replace(r"\xmark", "No")
    value = value.replace(r"\times", "×").replace(r"\%", "%")
    value = value.replace(r"\,", " ").replace("~", " ").replace("$", "")
    value = value.replace("--", "–")
    value = re.sub(r"\\(?:textbf|underline|textit)\{([^{}]*)\}", r"\1", value)
    return re.sub(r"\s+", " ", value).strip()


def parse_tables(source):
    tables = {}
    for key, metadata in BENCHMARKS.items():
        match = re.search(r"\\label\{tab:" + key + r"\}.*?\\begin\{tabular\}\{[^}]+\}(.*?)\\end\{tabular\}", source, re.S)
        if not match:
            raise ValueError(f"Missing source table: {key}")
        rows = []
        headers = None
        for line in match[1].splitlines():
            line = line.strip()
            if not line or line.startswith("%") or line in (r"\toprule", r"\midrule", r"\bottomrule"):
                continue
            if line.startswith(r"\multicolumn"):
                group = re.search(r"\\textit\{([^}]+)\}", line)
                if group:
                    rows.append({"group": group[1]})
                continue
            if "&" not in line:
                continue
            cells = [cell.strip() for cell in line.removesuffix(r"\\").split("&")]
            if headers is None:
                headers = [plain_tex(cell) for cell in cells]
                continue
            values = [plain_tex(cell) for cell in cells]
            if len(values) != len(headers):
                raise ValueError(f"Wrong column count in {key}: {line}")
            rows.append({"values": values, "best": [r"\textbf" in cell for cell in cells],
                         "second": [r"\underline" in cell for cell in cells],
                         "ours": "LeanWAM" in values[0]})
        tables[key] = {**metadata, "headers": headers, "rows": rows}
    return tables


def render_tables(tables):
    result = []
    for key, table in tables.items():
        title = html.escape(table["title"])
        result.append(f'<section class="benchmark-panel" id="benchmark-{key}" data-benchmark="{key}" aria-labelledby="heading-{key}">')
        result.append(f'<div class="table-intro"><h3 id="heading-{key}">{title}</h3><p>{html.escape(table["description"])}</p></div>')
        result.append(f'<div class="table-scroll" tabindex="0" role="region" aria-label="{title} results table, scroll horizontally on smaller screens"><table class="table-{key}"><caption class="visually-hidden">{title} success rates (%) from the LeanWAM paper</caption><thead><tr>')
        result.extend(f'<th scope="col">{html.escape(header)}</th>' for header in table["headers"])
        result.append('</tr></thead><tbody>')
        for row in table["rows"]:
            if "group" in row:
                result.append(f'<tr class="group-row"><th colspan="{len(table["headers"])}">{html.escape(row["group"])}</th></tr>')
                continue
            result.append('<tr class="ours">' if row["ours"] else '<tr>')
            for index, value in enumerate(row["values"]):
                content = html.escape(value)
                if index == 0:
                    if row["ours"]:
                        content = 'LeanWAM <span class="ours-label">(ours)</span>'
                    result.append(f'<th scope="row">{content}</th>')
                    continue
                if value in ("Yes", "No"):
                    content = f'<span class="pt-{value.lower()}" role="img" aria-label="{value}" title="{value}">{"✓" if value == "Yes" else "×"}</span>'
                elif row["best"][index]:
                    content = f'<strong>{content}</strong>'
                elif row["second"][index]:
                    content = f'<span class="second">{content}</span>'
                result.append(f'<td>{content}</td>')
            result.append('</tr>')
        result.append('</tbody></table></div>')
        result.append('<p class="table-scroll-hint">Scroll horizontally to see all columns →</p>')
        result.append(f'<p class="table-legend"><strong>Bold</strong>: best. <span class="second">Underline</span>: second best. {html.escape(table["legend"])}</p></section>')
    return "\n          ".join(result)


def replace_block(document, name, content):
    pattern = rf"(<!-- BEGIN PAPER {name} -->).*?(<!-- END PAPER {name} -->)"
    document, count = re.subn(pattern, lambda match: f"{match[1]}\n        {content}\n        {match[2]}", document, flags=re.S)
    if count != 1:
        raise ValueError(f"Expected one {name} block, found {count}")
    return document


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT.parent / "LeanWAM_arxiv")
    parser.add_argument("--pdf", type=Path, default=ROOT.parent / "LeanWAM_arxiv.pdf")
    args = parser.parse_args()
    source = args.source.resolve()
    index = ROOT / "index.html"
    document = index.read_text()
    hashes = {}
    for name in FIGURES:
        path = source / "fig" / f"{name}.pdf"
        hashes[f"fig/{name}.pdf"] = hashlib.sha256(path.read_bytes()).hexdigest()
        shutil.copy2(path, ROOT / "assets" / "figures" / path.name)
        with pymupdf.open(path) as pdf:
            page = pdf[0]
            scale = 2560 / page.rect.width
            pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False)
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        if img.width != 2560:
            img = img.resize((2560, round(img.height * 2560 / img.width)), Image.Resampling.LANCZOS)
        img.save(ROOT / "assets" / "figures" / f"{name}.webp", lossless=True, method=6)
        small = img.resize((1280, round(img.height / 2)), Image.Resampling.LANCZOS)
        small.save(ROOT / "assets" / "figures" / f"{name}-1280.webp", lossless=True, method=6)
        pattern = rf'(<img src="assets/figures/{name}\.webp"[^>]*?width=")\d+(" height=")\d+'
        document = re.sub(pattern, lambda m: f'{m[1]}{img.width}{m[2]}{img.height}', document)
        print(f"Exported {name}: {img.width} × {img.height}")

    experiment_path = source / "sec" / "5_experiments.tex"
    tables = parse_tables(experiment_path.read_text())
    document = replace_block(document, "TABLES", render_tables(tables))
    abstract_path = source / "sec" / "0_abstract.tex"
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", abstract_path.read_text(), re.S)[1]
    document = replace_block(document, "ABSTRACT", f'<p class="abstract-text">{html.escape(plain_tex(abstract))}</p>')
    for path in (experiment_path, abstract_path, source / "main.tex"):
        hashes[str(path.relative_to(source))] = hashlib.sha256(path.read_bytes()).hexdigest()
    hashes["LeanWAM_arxiv.pdf"] = hashlib.sha256(args.pdf.read_bytes()).hexdigest()
    shutil.copy2(args.pdf, ROOT / "assets" / "paper" / "LeanWAM.pdf")
    (ROOT / "data" / "results.json").write_text(json.dumps(tables, ensure_ascii=False, indent=2) + "\n")
    (ROOT / "data" / "sources.json").write_text(json.dumps({
        "paper": "LeanWAM: Learning Latent World Action Models from Frozen Video Models",
        "source_directory": "LeanWAM_arxiv", "sha256": hashes,
        "figures": {"overview": 2, "efficiency": 1, "code_umap": 4, "query_attn": 5},
        "note": "Tables and abstract are exported from the supplied LaTeX. Figures are lossless rasterizations of the original PDFs. No experimental values are recomputed.",
    }, ensure_ascii=False, indent=2) + "\n")
    index.write_text(document)
    print("Exported the original paper, abstract, and all three result tables.")


if __name__ == "__main__":
    main()
