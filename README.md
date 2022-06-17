# Loopy and unloopy programming techniques

This repository contains everything you need to follow the "Loopy and unloopy programming techniques" tutorial, presented at the [SciPy conference](https://www.scipy2022.scipy.org/) on [July 11, 2022 at 1:30pm‒5:30pm CDT](https://www.scipy2022.scipy.org/tutorials-schedule).

## How to participate

You don't need to install anything on your computer to participate; I encourage everyone to join on Binder.

<p align="center">
  <a href="https://mybinder.org/v2/gh/jpivarski-talks/2022-07-11-scipy-loopy-tutorial/v1.0?urlpath=lab/tree/narrative.ipynb">
    <img src="https://mybinder.org/badge_logo.svg" alt="Launch Binder" height="40">
  </a>
</p>

Binder tips: if your notebook becomes unresponsive, reconnect to the kernel or restart the kernel from the "Kernel" menu.

While working on exercises, keep a copy of your work-in-progress in a text editor, so that you don't lose them if the web page reloads. "Run → Run All Above Selected Cell" and "Kernel → Restart Kernel and Run up to Selected Cell" will rerun all of the code to get your Python session back to the state it was in before a page reload or kernel restart.

In JupyterLab, the left-bar lets you navigate through files, shut down unnecessary kernels (closing a notebook tab does not shut down its Python kernel), and navigate the table of contents.

<table width="100%"><tr>
  <td style="margin-right: 5px"><img src="img/jupyterlab-files.png"></td>
  <td><img src="img/jupyterlab-kernels.png"></td>
  <td style="margin-left: 5px"><img src="img/jupyterlab-toc.png"></td>
</td></table>

The "intermezzo" demo will be run on [Google Colab](https://research.google.com/colaboratory/) (because it requires a GPU). You can join that as well if you have a Colab account, but you don't have to—none of the exercises require it.

## If you _want_ to install and run on your computer

We use the libraries and versions listed in [requirements.txt](requirements.txt). You also need to install JupyterLab. You don't have to install the libraries with pip (you can use conda, for instance), and you don't need to use the exact versions that this tutorial has been pinned to, but you should probably use _at least_ those versions. Note that `awkward>=1.9.0rc5` is a minimum requirement and a pre-release.

We won't spend any time in the tutorial session on installing libraries. If an installation on your computer doesn't work, switch to Binder by pressing the button above.

