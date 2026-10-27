# Generates the static course site. Run from anywhere: python site/build_site.py
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SITE = Path(__file__).resolve().parent

NAV = [
    ("index.html", "Overview", "overview"),
    ("framework.html", "Framework", "framework"),
    ("catalog.html", "Modules", "catalog"),
    ("courses.html", "Courses", "courses"),
    ("assessment.html", "Evidence", "assessment"),
    ("adopt.html", "Adopt", "adopt"),
    ("about.html", "About", "about"),
]

MODULES = [
    {
        "slug": "m1", "id": "M1", "title": "Binary reverse engineering",
        "course": "es", "course_label": "Embedded systems",
        "status": "surveyed", "status_label": "Delivered, surveyed",
        "origin": "field", "origin_label": "Field",
        "blurb": "Recover a room-temperature controller from an AT89C51 binary that ships with no source.",
        "concept": "Compilation flow, instruction set, addressing modes, code and data spaces, stack pointer",
        "platform": "AT89C51 and Keil µVision",
        "evidence": "Ten answers from the disassembly and the memory windows",
        "defense": "None. The module is a literacy exercise and says so.",
    },
    {
        "slug": "m2", "id": "M2", "title": "Buffer overflow",
        "course": "es", "course_label": "Embedded systems",
        "status": "surveyed", "status_label": "Delivered, surveyed",
        "origin": "field", "origin_label": "Field",
        "blurb": "Overrun a fixed buffer on an 8051, watch a secret return through R7, then repair the copy.",
        "concept": "Stack frame, calling convention, saved return address, constant initialization",
        "platform": "AT89C51, Keil debugger",
        "evidence": "Input length, secrets leaked, and a justified repair",
        "defense": "A bounded copy the student writes for a bare-metal target",
    },
    {
        "slug": "m3", "id": "M3", "title": "Timing side channel",
        "course": "es", "course_label": "Embedded systems",
        "status": "surveyed", "status_label": "Delivered, surveyed",
        "origin": "field", "origin_label": "Field",
        "blurb": "Measure an early-exit password check on the logic analyzer, then make the comparison constant-time.",
        "concept": "Timer peripheral, cycle counting, serial-port setup, data-dependent branching",
        "platform": "AT89C51 and the debugger logic analyzer",
        "evidence": "Timing tables for the vulnerable check and the repaired check",
        "defense": "A comparison that touches every character, re-measured on the same instrument",
    },
    {
        "slug": "m4", "id": "M4", "title": "Board reverse engineering",
        "course": "es", "course_label": "Embedded systems",
        "status": "ready", "status_label": "Written material",
        "origin": "field", "origin_label": "Field",
        "blurb": "Take a populated board with no schematic and produce a bill of materials and a block diagram.",
        "concept": "Microcontroller interfacing, serial protocols, power distribution, datasheets",
        "platform": "Undocumented board and a digital multimeter",
        "evidence": "Bill of materials and block diagram; a schematic and a protocol if time allows",
        "defense": "None specified. The deliverable is the first artifact a cloner produces.",
    },
    {
        "slug": "m5", "id": "M5", "title": "Power side channel",
        "course": "dl", "course_label": "Digital logic",
        "status": "taught", "status_label": "Delivered, no survey",
        "origin": "field", "origin_label": "Field",
        "blurb": "Infer an unknown gate from supply-current spikes, and see what the measurement cannot tell you.",
        "concept": "CMOS switching, output transitions, charge transfer, truth tables",
        "platform": "Browser circuit simulator and a sense resistor",
        "evidence": "Voltage plot, transition table, and the candidate truth tables",
        "defense": "None. The module ends on the ambiguity the measurement leaves.",
    },
    {
        "slug": "m6", "id": "M6", "title": "Combinational logic locking",
        "course": "dl", "course_label": "Digital logic",
        "status": "ready", "status_label": "Written material",
        "origin": "supply", "origin_label": "Supply chain",
        "blurb": "Build a 4-bit ripple-carry adder, then lock the carry chain with a key.",
        "concept": "Ripple-carry addition, carry propagation, hierarchical design, instantiation",
        "platform": "VHDL and an FPGA design suite",
        "evidence": "Locked design, testbench, and waveforms for a correct key and a wrong key",
        "defense": "The student builds the lock.",
    },
    {
        "slug": "m7", "id": "M7", "title": "Hardware Trojan insertion",
        "course": "dl", "course_label": "Digital logic",
        "status": "ready", "status_label": "Written material",
        "origin": "supply", "origin_label": "Supply chain",
        "blurb": "Leave the locked adder alone, and add a trigger and a payload that corrupt it on one input.",
        "concept": "Rare-condition decoding, conditional assignment, behavioral simulation",
        "platform": "VHDL and the locked adder from the locking lab",
        "evidence": "Trigger and payload code, plus waveforms while dormant and while active",
        "defense": "The module teaches the attack. Detection is the analysis half of the report.",
    },
    {
        "slug": "m8", "id": "M8", "title": "Sequential logic locking",
        "course": "dl", "course_label": "Digital logic",
        "status": "ready", "status_label": "Written material",
        "origin": "supply", "origin_label": "Supply chain",
        "blurb": "Lock a UART transmitter in its state machine, so the key arrives over several clocks.",
        "concept": "Finite-state machines, reset and transition behavior, the UART frame",
        "platform": "VHDL UART transmitter",
        "evidence": "Augmented state machine and waveforms for the right sequence and each wrong key",
        "defense": "The student builds the sequential lock.",
    },
    {
        "slug": "m9", "id": "M9", "title": "Cache side channel",
        "course": "ca", "course_label": "Computer architecture",
        "status": "taught", "status_label": "Delivered, no survey",
        "origin": "field", "origin_label": "Field",
        "blurb": "Treat the cache the course already teaches as a channel another process can read.",
        "concept": "Hierarchy, associativity, line size, set indexing, cycle-accurate timing",
        "platform": "A commodity x86 machine and its cycle counter",
        "evidence": "A recorded probe-time series. No graded assignment was stated.",
        "defense": "None in the delivered lecture. The point is that the hit-miss gap is readable.",
    },
]

PILL = {
    "field": "pill-field",
    "supply": "pill-supply",
    "surveyed": "pill-ok",
    "taught": "pill-taught",
    "ready": "pill-ready",
}

MARK = '''<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="6" y="6" width="12" height="12" stroke="#1a1916" stroke-width="1.7"/><path d="M9 3.2v2.6M12 3.2v2.6M15 3.2v2.6M9 18.2v2.6M12 18.2v2.6M15 18.2v2.6M3.2 9H6M3.2 12H6M3.2 15H6M18 9h2.8M18 12h2.8M18 15h2.8" stroke="#1d4ed8" stroke-width="1.7"/></svg>'''


def pills(m):
    return (
        f'<span class="pill {PILL[m["origin"]]}">{m["origin_label"]}</span>'
        f'<span class="pill">{m["course_label"]}</span>'
        f'<span class="pill {PILL[m["status"]]}">{m["status_label"]}</span>'
    )


def header(base, active):
    links = []
    for href, label, pid in NAV:
        current = ' aria-current="page"' if pid == active else ""
        links.append(f'<a href="{base}{href}"{current}>{label}</a>')
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{base}index.html">
      <span class="brand-mark">{MARK}</span>
      <span><strong>Hardware Security for All</strong><em>Core-course modules</em></span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav id="site-nav" class="nav" aria-label="Primary">{''.join(links)}</nav>
  </div>
</header>'''


def footer(base):
    return f'''<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <strong>Hardware Security for All</strong>
      <p>Hands-on hardware security placed inside undergraduate embedded systems, digital logic, and computer architecture. Doing the security work is how the student exercises the design topic.</p>
    </div>
    <div>
      <p>University of Kansas, EECS<br>University of Florida, ECE<br>Florida International University, ECE</p>
    </div>
    <div>
      <a href="{base}catalog.html">Module catalog</a>
      <a href="{base}framework.html">Design rules</a>
      <a href="{base}adopt.html">Adopt a module</a>
      <a href="{base}about.html">People and paper</a>
    </div>
  </div>
  <div class="wrap footer-base"><p>Local course site for later hosting. Instructor solution archives and lecture recordings stay out of this bundle.</p></div>
</footer>'''


def page(filename, title, description, active, body, depth=0):
    base = "../" * depth
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="{base}assets/favicon.svg">
<link rel="stylesheet" href="{base}css/site.css">
</head>
<body>
{header(base, active)}
<main id="main">
{body}
</main>
{footer(base)}
<script src="{base}js/site.js"></script>
</body>
</html>
'''
    path = SITE / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("wrote", path.relative_to(SITE))


def rail(current):
    links = []
    for m in MODULES:
        cur = ' aria-current="page"' if m["slug"] == current else ""
        links.append(f'<a href="{m["slug"]}.html"{cur}><strong>{m["id"]}</strong> {m["title"]}</a>')
    m = next(x for x in MODULES if x["slug"] == current)
    return f'''<aside class="rail">
  <dl class="facts">
    <div><dt>Course</dt><dd>{m["course_label"]}</dd></div>
    <div><dt>Status</dt><dd>{m["status_label"]}</dd></div>
    <div><dt>Threat origin</dt><dd>{m["origin_label"]}</dd></div>
    <div><dt>Platform</dt><dd>{m["platform"]}</dd></div>
    <div><dt>Design concept</dt><dd>{m["concept"]}</dd></div>
    <div><dt>Graded evidence</dt><dd>{m["evidence"]}</dd></div>
    <div><dt>Countermeasure</dt><dd>{m["defense"]}</dd></div>
  </dl>
  <nav class="rail-nav" aria-label="Modules">{''.join(links)}</nav>
</aside>'''


def module_page(m, body):
    inner = f'''<div class="page">
  <div class="wrap">
    <p class="crumb"><a href="../catalog.html">Modules</a> / {m["id"]}</p>
    <p class="pills">{pills(m)}</p>
    <h1>{m["title"]}</h1>
    <p class="lede">{m["blurb"]}</p>
    <div class="layout">
      <article class="prose">{body}</article>
      {rail(m["slug"])}
    </div>
  </div>
</div>'''
    page(
        f'modules/{m["slug"]}.html',
        f'{m["id"]} {m["title"]} · Hardware Security for All',
        m["blurb"],
        "catalog",
        inner,
        depth=1,
    )


def copy_materials():
    pairs = [
        (r"NSF SaTC Education\Past Modules\EECS 388 KU\Spring 2024\Module 1 Binary Rev Eng\Lecture Slides\Module1_RE_part1.pptx", "materials/m1/Module1_RE_part1.pptx"),
        (r"NSF SaTC Education\Past Modules\EECS 388 KU\Spring 2024\Module 1 Binary Rev Eng\Lecture Slides\Module1_RE_part2.pptx", "materials/m1/Module1_RE_part2.pptx"),
        (r"NSF SaTC Education\Past Modules\EECS 388 KU\Spring 2024\Module 1 Binary Rev Eng\Assignment\Module1_Homework_BRE.pdf", "materials/m1/Module1_Homework_BRE.pdf"),
        (r"NSF SaTC Education\Past Modules\EECS 388 KU\Spring 2024\Module 1 Binary Rev Eng\Assignment\unknown-1", "materials/m1/unknown-1"),
        (r"NSF SaTC Education\Past Modules\EECS 388 KU\Spring 2024\Module 2 Buffer Overflow Attack\Lecture Slides\Module2_BufferOverflow_part1.pptx", "materials/m2/Module2_BufferOverflow_part1.pptx"),
        (r"NSF SaTC Education\Past Modules\EECS 388 KU\Spring 2024\Module 2 Buffer Overflow Attack\Lecture Slides\Module2_BufferOverflow_part2.pptx", "materials/m2/Module2_BufferOverflow_part2.pptx"),
        (r"NSF SaTC Education\Past Modules\EECS 388 KU\Spring 2024\Module 2 Buffer Overflow Attack\Assignment\Module1_Homework_BOA.pdf", "materials/m2/Module1_Homework_BOA.pdf"),
        (r"NSF SaTC Education\Past Modules\EECS 388 KU\Spring 2024\Module 2 Buffer Overflow Attack\Assignment\vulnerable_program.c", "materials/m2/vulnerable_program.c"),
        (r"NSF SaTC Education\Past Modules\EECS 388 KU\Spring 2024\Module 3 Timing Side Channel Vulnerability\Lecture Slides\Module3_TimingSCA_part1.pptx", "materials/m3/Module3_TimingSCA_part1.pptx"),
        (r"NSF SaTC Education\Past Modules\EECS 388 KU\Spring 2024\Module 3 Timing Side Channel Vulnerability\Lecture Slides\Module3_TimingSCA_part2.pptx", "materials/m3/Module3_TimingSCA_part2.pptx"),
        (r"NSF SaTC Education\Past Modules\EECS 388 KU\Spring 2024\Module 3 Timing Side Channel Vulnerability\Assignment\Module1_Homework_SCA.pdf", "materials/m3/Module1_Homework_SCA.pdf"),
        (r"NSF SaTC Education\Past Modules\EECS 388 KU\Spring 2024\Module 3 Timing Side Channel Vulnerability\Assignment\sca_sp24.c", "materials/m3/sca_sp24.c"),
        (r"NSF SaTC Education\All modules 2026\PCB Reverse Engineering\Hardware Reverse Engineering Lab Proposal.docx", "materials/m4/Hardware_Reverse_Engineering_Lab_Specification.docx"),
        (r"more modules\Combinational_Obfuscation_Lab\Combinational_Obfuscation_Lab\Starter_Code\FullAdder.vhdl", "materials/m6/FullAdder.vhdl"),
        (r"more modules\Combinational_Obfuscation_Lab\Combinational_Obfuscation_Lab\Combinational_Obfuscation_Lab_Manual.docx", "materials/m6/Combinational_Obfuscation_Lab_Manual.docx"),
        (r"more modules\Hardware_Trojan_Lab\Hardware_Trojan_Lab\Starter_Code\FullAdder.vhdl", "materials/m7/FullAdder.vhdl"),
        (r"more modules\Hardware_Trojan_Lab\Hardware_Trojan_Lab\Starter_Code\4BitAdder_Key.vhdl", "materials/m7/4BitAdder_Key.vhdl"),
        (r"more modules\Hardware_Trojan_Lab\Hardware_Trojan_Lab\Starter_Code\tb_4BitAdder.vhdl", "materials/m7/tb_4BitAdder.vhdl"),
        (r"more modules\Hardware_Trojan_Lab\Hardware_Trojan_Lab\Hardware_Trojan_Insertion_Lab_Manual.docx", "materials/m7/Hardware_Trojan_Insertion_Lab_Manual.docx"),
        (r"more modules\UART_Obfuscation_Lab\UART_Obfuscation_Lab\Starter_Code\UART.vhdl", "materials/m8/UART.vhdl"),
        (r"more modules\UART_Obfuscation_Lab\UART_Obfuscation_Lab\Starter_Code\UART_tb.vhdl", "materials/m8/UART_tb.vhdl"),
        (r"more modules\UART_Obfuscation_Lab\UART_Obfuscation_Lab\UART_Obfuscation_Lab_Manual.docx", "materials/m8/UART_Obfuscation_Lab_Manual.docx"),
        (r"more modules\cache-sidechannel\cache_side-channel_Part1.pptx", "materials/m9/cache_side-channel_Part1.pptx"),
        (r"more modules\cache-sidechannel\cache_side-channel_Part2.pptx", "materials/m9/cache_side-channel_Part2.pptx"),
        (r"ISQED27-paper\Figure1.svg", "assets/figure1.svg"),
    ]
    for src, dest in pairs:
        source = ROOT / src
        target = SITE / dest
        if not source.exists():
            raise SystemExit(f"missing source: {source}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        print("copied", dest)


def main():
    copy_materials()
    from content_pages import emit
    emit(page, module_page, MODULES, pills)


if __name__ == "__main__":
    main()
