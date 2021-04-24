>> Note: 'final' cleanup/ reformatting of package and this website is underway. <<

What is PolyChemPrint3 (PCP3)?

Short form: PCP3 functions something like a mix of Pronterface and a GCode Slic(3)r, but for arbitrary axes/toolhead (extruder/syringe pump/ LASER/ etc.) combinations and streamlined for research of non-thermoplastic materials.

This project aims to help bridge the gap between commercially mature FDM 3D-printing and the expanded range of deposition tools and material palette of modern additive manufacturing (AM) research.

The centerpiece of this work is the open source PolyChemPrint3 python package, available as a distributable package on PyPi and (more usefully) from source code on Github. A full user manual and software documentation are available via readthedocs.io.

PCP3 is essentially the control software for benchtop additive manufacturing equipment. It handles synchronized communication between motion axes and the myriad AM toolheads (extruders, syringe pumps, Lasers) that are used in modern AM materials research.

Along with the software package, this webpage and associated docs describe our research group's hardware implementation: centered on the Lulzbot Taz 6 3D printer with various print/toolheads that we have used for processing a variety of materials (polymer solutions, thermoplastics, conductive polymers, chocolate, Laser etching of small molecule crystals).

Key Features:

Free, Open source, object oriented, and excessively documented: The program is written in an extensible, 'minimum coding required' way. You do not need to be a computer scientist to use and extend this program.
Easy Hardware integration: New tools and axes need only be capable of two-way serial communication to be integrated: allowing for the use of commercial 3D printers, industrial linear stages, or a (weird) combination to be easily integrated alongside pneumatic extruders, lasers, syringe pumps, etc.
Integration with the mature 3D Slicing Pipeline: A key functionality of PCP3 is the ability to import 1D/3D GCode sequences prepared by common FDM slicers (Inkscape, Slic3r, Cura, etc) and transcode FDM extruder commands to suitable commands for whichever toolhead is loaded. Essentially: now you can print your fabulous new material into a beautiful hat, chameleon, or arbitrary (useful) object.
Designed for Flexibility: Designed as a cross-platform tool (Windows and linux), PCP3 can readily switch between control of different toolheads to allow the same printing setup to be switched rapidly between materials and projects.
Streamlined for Research: Automatic data logging and the (easily extended) library of parameterized sequences (cubes, meanderlines, etc.) improves reproducibility across trials and cuts down wasted time creating 3D models and slicing for minor changes/ parameter sweeps.

Please read and cite this paper if you would like to use or build on the PCP3 code in your work:

Patel, B. B.; Chang, Y.; Park, S. K.; Wang, S.; Rosheck, J.; Patel, K.; Walsh, D.; Guironnet, D.; Diao, Y. PolyChemPrint: A Hardware and Software Framework for Benchtop Additive Manufacturing of Functional Polymeric Materials. Journal of Polymer Science https://doi.org/10.1002/pol.20210086.

Other publications making use of PCP3 [by date]:

Zhou, K.; Li, W.; Patel, B. B.; Tao, R.; Chang, Y.; Fan, S.; Diao, Y.; Cai, L. Three-Dimensional Printable Nanoporous Polymer Matrix Composites for Daytime Radiative Cooling. Nano Lett. 2021. https://doi.org/10.1021/acs.nanolett.0c04810.
Park, S. K.; Sun, H.; Chung, H.; Patel, B. B.; Zhang, F.; Davies, D. W.; Woods, T. J.; Zhao, K.; Diao, Y. Super- and Ferroelastic Organic Semiconductors for Ultraflexible Single-Crystal Electronics. Angewandte Chemie International Edition 2020, 59 (31), 13004–13012. https://doi.org/10.1002/anie.202004083.
B. B. Patel, D. J. Walsh, D. H. Kim, J. Kwok, B. Lee, D. Guironnet, Y. Diao, Tunable structural color of bottlebrush block copolymers through direct-write 3D printing from solution. Sci. Adv. 6, eaaz7202 (2020).

Funding Sources:

National Science Foundation DMREF Award No. DMR-1727605
Startup Funds of the Diao Group from the University of Illinois Department of Chemical and Biomolecular Engineering.
## Welcome to GitHub Pages

You can use the [editor on GitHub](https://github.com/BijalBPatel/PolyChemPrint3/edit/gh-pages/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/BijalBPatel/PolyChemPrint3/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
