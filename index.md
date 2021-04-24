>> Note: 'final' cleanup/ reformatting of package and this website is underway. 

<span style="text-decoration: underline;">**What is PolyChemPrint3 (PCP3)?**</span> 

_**Short form:** PCP3 functions something like a mix of [Pronterface](https://www.pronterface.com/) and a [GCode Slic(3)r](https://slic3r.org/), but for arbitrary axes/toolhead (extruder/syringe pump/ LASER/ etc.) combinations and streamlined for research of non-thermoplastic materials._ 

This project aims to help bridge the gap between commercially mature FDM 3D-printing and the expanded range of deposition tools and material palette of modern additive manufacturing (AM) research. The centerpiece of this work is the **open source PolyChemPrint3 python package,** available as a [distributable package on PyPi](https://pypi.org/project/polychemprint3/) and (more usefully) from [source code on Github.](https://github.com/BijalBPatel/PolyChemPrint3) A full user manual and software documentation are available via [readthedocs.io](https://polychemprint3.readthedocs.io/en/latest/). PCP3 is essentially the **control software for benchtop additive manufacturing equipment**. It handles **synchronized communication between motion axes and the myriad AM toolheads** (extruders, syringe pumps, Lasers) that are used in modern AM materials research. Along with the software package, this webpage and associated docs describe o**ur research group's hardware implementation**: centered on the Lulzbot Taz 6 3D printer with various print/toolheads that we have used for processing a variety of materials (polymer solutions, thermoplastics, conductive polymers, chocolate, Laser etching of small molecule crystals). <span style="text-decoration: underline;">

**Key Features:**</span>

*   **Free, Open source, object oriented, and excessively documented:** The program is written in an extensible, 'minimum coding required' way. You do not need to be a computer scientist to use and extend this program.
*   **Easy Hardware integration:** New tools and axes need only be capable of two-way serial communication to be integrated: allowing for the use of commercial 3D printers, industrial linear stages, or a (weird) combination to be easily integrated alongside pneumatic extruders, lasers, syringe pumps, etc.
*   **Integration with the mature 3D Slicing Pipeline:** A key functionality of PCP3 is the ability to import 1D/3D GCode sequences prepared by common FDM slicers (Inkscape, Slic3r, Cura, etc) and transcode FDM extruder commands to suitable commands for whichever toolhead is loaded. Essentially: now you can print your fabulous new material into a beautiful hat, chameleon, or arbitrary (useful) object.
*   **Designed for Flexibility:** Designed as a cross-platform tool (Windows and linux), PCP3 can readily switch between control of different toolheads to allow the same printing setup to be switched rapidly between materials and projects.
*   **Streamlined for Research:** Automatic data logging and the (easily extended) library of parameterized sequences (cubes, meanderlines, etc.) improves reproducibility across trials and cuts down wasted time creating 3D models and slicing for minor changes/ parameter sweeps.

<span style="text-decoration: underline;">**Please read and cite this paper if you would like to use or build on the PCP3 code in your work:**</span>

*   <div class="csl-bib-body">

    <div class="csl-entry">

    <div class="csl-right-inline">Patel, B. B.; Chang, Y.; Park, S. K.; Wang, S.; Rosheck, J.; Patel, K.; Walsh, D.; Guironnet, D.; Diao, Y. PolyChemPrint: A Hardware and Software Framework for Benchtop Additive Manufacturing of Functional Polymeric Materials. _Journal of Polymer Science_ [https://doi.org/10.1002/pol.20210086](https://doi.org/10.1002/pol.20210086).</div>

    </div>

    </div>

<span style="text-decoration: underline;">**Other publications making use of PCP3 [by date]:**</span>

*   <div class="csl-bib-body">

    <div class="csl-entry">

    <div class="csl-right-inline">Zhou, K.; Li, W.; Patel, B. B.; Tao, R.; Chang, Y.; Fan, S.; Diao, Y.; Cai, L. Three-Dimensional Printable Nanoporous Polymer Matrix Composites for Daytime Radiative Cooling. _Nano Lett._ **2021**. [https://doi.org/10.1021/acs.nanolett.0c04810](https://doi.org/10.1021/acs.nanolett.0c04810).</div>

    </div>

    </div>

*   <div class="csl-bib-body">

    <div class="csl-entry">

    <div class="csl-right-inline">Park, S. K.; Sun, H.; Chung, H.; Patel, B. B.; Zhang, F.; Davies, D. W.; Woods, T. J.; Zhao, K.; Diao, Y. Super- and Ferroelastic Organic Semiconductors for Ultraflexible Single-Crystal Electronics. _Angewandte Chemie International Edition_ **2020**, _59_ (31), 13004–13012\. [https://doi.org/10.1002/anie.202004083](https://doi.org/10.1002/anie.202004083).</div>

    </div>

    </div>

*   B. B. Patel, D. J. Walsh, D. H. Kim, J. Kwok, B. Lee, D. Guironnet, Y. Diao, Tunable structural color of bottlebrush block copolymers through direct-write 3D printing from solution. Sci. Adv. 6, eaaz7202 (2020).

<span style="text-decoration: underline;">**Funding Sources:**</span>

*   Startup Funds of the [Diao Group](http://diao.scs.illinois.edu/Diao_Lab/Home.html) from the University of Illinois [Department of Chemical and Biomolecular Engineering](https://chbe.illinois.edu/).

*   National Science Foundation DMREF Award No. DMR-1727605