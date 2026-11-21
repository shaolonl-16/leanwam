# LeanWAM project page

可直接发布到 GitHub Pages 的英文项目主页，使用 HTML、CSS 和少量原生 JavaScript。无需 Node.js、npm 或构建步骤。字体、图像和论文均保存在本目录，无需依赖外部 CDN。

页面包含论文标题、四位作者、University of Michigan、共同贡献与共同指导说明，PDF / arXiv / Code 入口，完整摘要、overview、图 1、三个 benchmark 的完整结果表、图 4、图 5 和 citation。图像可点击放大，结果表可用鼠标或方向键切换。手机上的宽表可横向滚动，方法名固定在左侧。

## 1. 本地预览

直接用浏览器打开 `index.html` 即可查看，也可以在本目录执行：

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

浏览器访问 <http://localhost:8765/>。如果代码位于远程服务器，在 VS Code 的 **Ports / 端口** 面板转发 `8765`，然后在本机浏览器打开转发地址。停止预览用 `Ctrl+C`。

## 2. 填入个人主页、论文和代码链接

编辑根目录的 `site.config.js`：

```js
links: {
  pdf: "assets/paper/LeanWAM.pdf", // 可保留随网站附带的 PDF，也可改为正式 PDF URL
  arxiv: "",                     // 正式 arXiv abstract 页面 URL
  code: "",                      // 正式 GitHub 代码仓库 URL
},
authors: {
  shaolong: "", // Shaolong Li
  hongze: "",   // Hongze Fu
  yinpei: "",   // Yinpei Dai
  joyce: "",    // Joyce Chai
},
```

把 URL 写在引号内，例如 `"https://your-homepage.example/"`。未填的作者姓名显示为文字，未填的 arXiv / Code 入口显示 `Soon`，不会跳转到无关网址。填入后自动启用链接。PDF 当前已可用。

在同一文件的 `bibtex: String.raw` 后面的一对反引号内粘贴最终 BibTeX。保留 BibTeX 原有的换行和反斜线。填写后页面自动显示引用文本、**Copy BibTeX** 和 **Download .bib**，无需修改 HTML。未填时显示等待 arXiv 发布的说明。

## 3. 注册 GitHub 并发布（推荐的网页操作）

1. 在 <https://github.com/signup> 注册 GitHub 个人账号并验证邮箱。已有账号直接登录。
2. 打开 <https://github.com/new>，新建名为 **`leanwam`** 的仓库，选择 **Public**。推荐将网页放在单独的仓库中。
3. 解压交付的 `leanwam-project-page.zip`。在仓库页面点击 **Add file → Upload files**，上传解压后的文件和目录。空仓库可点击 **uploading an existing file**。**上传内容，而不是 ZIP 文件本身。**
4. 确认 `index.html` 位于仓库根目录，和 `assets/`、`site.config.js` 同级。不要让它落在额外一层 `leanwam-project-page/` 里面。保留 `assets/` 中的目录结构和大小写。提交到 `main` 分支。
5. 进入 **Settings → Pages → Build and deployment**，将 **Source** 设为 **Deploy from a branch**，选择 **`main`** 和 **`/(root)`**，点击 **Save**。
6. 等待部署完成，可在 **Actions** 查看进度，然后回到 **Settings → Pages** 点击 **Visit site**。

你的项目网址会是：

```text
https://你的GitHub用户名.github.io/leanwam/
```

例如，用户名是 `alice`、仓库名是 `leanwam`，网址就是 `https://alice.github.io/leanwam/`。不需要购买域名或单独注册网址。之后修改文件并提交到 `main`，GitHub Pages 会更新页面。

`.nojekyll` 已包含在交付包中，用于跳过 Jekyll。文件管理器可能默认隐藏它，上传时可开启显示隐藏文件。也可以在 GitHub 的 **Add file → Create new file** 中创建名为 `.nojekyll` 的文件。

如果希望得到类似 D4RT 的 **`https://leanwam.github.io/`**，需要拥有名为 `leanwam` 的 GitHub 用户或组织，并在该账号下创建 **`leanwam.github.io`** 仓库。账号/组织名是否可用需要在 GitHub 检查。若 `leanwam` 已被占用，可考虑 `leanwam-paper` 组织及 `leanwam-paper.github.io` 仓库。仅在自己的普通账号下创建 `leanwam.github.io` 仓库不会获得 `https://leanwam.github.io/`。

GitHub 官方说明：[注册账号](https://docs.github.com/en/account-and-profile/how-tos/account-management/creating-an-account-on-github)、[创建 Pages 网站](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)、[设置发布来源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)。

## 4. 用 Git 上传（可选）

在 GitHub 新建空的 `leanwam` 仓库，然后将页面复制到一个独立目录，避免将整个训练仓库提交上去。下面的 `YOUR_USERNAME` 需要替换为你的 GitHub 用户名：

```bash
cp -a /scratch/experiment/shaolong/starVLA_new/leanwam-project-page /scratch/experiment/leanwam-site-publish
cd /scratch/experiment/leanwam-site-publish
git init -b main
git add .
git commit -m "Add LeanWAM project page"
git remote add origin https://github.com/YOUR_USERNAME/leanwam.git
git push -u origin main
```

推送时按 GitHub 的认证方式登录，然后按上一节的 Settings → Pages 步骤启用网站。如果更习惯图形界面，网页上传已经足够。

## 5. 后续维护

| 文件 | 用途 |
| --- | --- |
| `index.html` | 页面结构、文字、完整 HTML 表格 |
| `site.config.js` | 作者链接、资源链接、BibTeX |
| `assets/css/style.css` | 布局、配色、手机适配 |
| `assets/js/main.js` | 表格切换、图片放大、引用复制 |
| `assets/figures/` | 四张论文图的原始 PDF 与两档无损 WebP |
| `assets/paper/LeanWAM.pdf` | PDF 按钮打开的论文 |
| `data/results.json` | 从论文 LaTeX 提取的表格数据，供核对使用 |
| `data/sources.json` | 原始文件的 SHA-256 和图号对应关系 |
| `scripts/prepare_paper.py` | 论文更新后重新导出图片、摘要和表格 |

表格中的数字、加粗与下划线直接沿用论文。RoboTwin 2.0 明确标注为论文选定的 10 个任务。图 1 保留原图的对数坐标和气泡编码，不重新绘制或修改数据。

网站直接使用 `index.html` 中的表格，不会在浏览器中读取 `data/results.json`。因此更新结果时，请修改论文源文件后重新导出，或同步手工修改 HTML，不能只改 JSON。

只有论文内容更新时才需要导出工具。使用独立环境安装 `PyMuPDF` 和 `Pillow` 后，在网站目录执行：

```bash
python scripts/prepare_paper.py --source ../LeanWAM_arxiv --pdf ../LeanWAM_arxiv.pdf
```

导出脚本只读取论文源文件，更新网站中的资源及带 `BEGIN PAPER` 标记的摘要、表格区域。标题、作者、摘要之外的简述和结果卡片需要在论文变化后手工同步。脚本不会改写 `site.config.js`。仅部署或预览网站不需要运行该脚本。

### 常见问题

- **网站 404**：确认仓库为 Public，Pages 选择了实际存在的 `main` 分支与 `/(root)`，`index.html` 在仓库根目录，Actions 部署成功，并使用包含 `/leanwam/` 的完整网址。
- **图片不显示**：确认整个 `assets/` 已上传，且没有改变文件名大小写。当前资源均使用相对路径，可用于仓库子路径部署。
- **修改后未更新**：等待 Pages 部署完成后强制刷新浏览器。GitHub 文档说明发布变化可能需要约 10 分钟。
- **发布后是否还需要本地服务器**：不需要，网站由 GitHub Pages 托管，本地服务器仅用于预览。

## 来源与字体

论文与全部科学图表来自用户提供的 LeanWAM 稿件，未使用生成式图像替代实验结果。页面设计参考 [VPP2](https://robert-gyj.github.io/video-prediction-policy-2/) 与 [D4RT](https://d4rt-paper.github.io/) 的学术项目展示方式，网页代码独立编写。

Inter 字体使用 SIL Open Font License，许可文本位于 `assets/fonts/LICENSE.txt`。论文、图表和页面代码的再分发许可由作者另行确定。
