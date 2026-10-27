"""Page bodies for the Hardware Security for All site."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def intro(topic, place, materials, papers, videos):
    paper_items = "\n".join(f"<li>{item}</li>" for item in papers)
    cards = []
    for item in videos:
        match = re.search(r'href="([^"]+)"[^>]*>(.*?)</a>(.*)', item, re.S)
        if not match:
            cards.append(item)
            continue
        url, title, rest = match.group(1), match.group(2).strip(), match.group(3).strip()
        rest = re.sub(r"^\.\s*", "", rest).strip()
        cards.append(
            f'<a class="download" href="{url}"><span><b>{title}</b><span>{rest}</span></span><i>Video</i></a>'
        )
    video_cards = "\n".join(cards)
    return f'''<h2>The topic</h2>
<p>{topic}</p>
<h2>Where it belongs</h2>
<div class="callout"><p>{place}</p></div>
<h2>Files and how to use them</h2>
{materials}
<h3>Video lectures</h3>
<p>These are links, not files stored with the module. Play one in class, or send the link to students.</p>
<div class="downloads">
{video_cards}
</div>
<h2>Further reading</h2>
<p>Optional papers for the instructor, or for a student who wants to read past the assignment.</p>
<ul>
{paper_items}
</ul>
'''


def falstad_links():
    assign = (ROOT / r"md\NSF SaTC Education\All modules 2026\Power Side Channel Analysis\Power Side Channel Attack Assignment.md").read_text(encoding="utf-8")
    unknown = re.search(r"\((https://www\.falstad\.com/circuit/[^)]+)\)", assign).group(1)
    notes = (ROOT / r"md\NSF SaTC Education\All modules 2026\Power Side Channel Analysis\Links to other circuits for PSC analysis.md").read_text(encoding="utf-8")
    pairs = re.findall(r"\[([^\]]+)\]\((https://www\.falstad\.com/circuit/[^)]+)\)", notes)
    items = "\n".join(f'<li><a href="{url}">{name}</a></li>' for name, url in pairs)
    return unknown, items


def emit(page, module_page, modules, pills):
    by_id = {m["id"]: m for m in modules}
    unknown, gate_items = falstad_links()

    toc = "\n".join(
        f'<li><a href="modules/{m["slug"]}.html"><span>{m["id"]}</span><b>{m["title"]}</b><em>{m["course_label"]}</em></a></li>'
        for m in modules
    )
    cards = "\n".join(
        f'''<a class="mod-card" href="modules/{m["slug"]}.html">
          <span class="id">{m["id"]}</span>
          <h3>{m["title"]}</h3>
          <p>{m["blurb"]}</p>
          <div class="meta">{pills(m)}</div>
        </a>'''
        for m in modules
    )

    page("index.html", "Hardware Security for All",
         "Nine hands-on hardware security modules for undergraduate embedded systems, digital logic, and computer architecture.",
         "overview", f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow"><span>University of Kansas</span> · University of Florida · Florida International University</p>
      <h1>Hardware security, taught inside the courses students already take.</h1>
      <p class="lede">Most cybersecurity courses still treat the processor and the board as a root of trust. These modules do not add a hardware-security elective. Each one is a lab on a topic the host course already teaches: the instruction set, the stack, the timer, CMOS switching, the adder, the state machine, or the cache.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="catalog.html">Open the nine modules</a>
        <a class="btn btn-ghost" href="framework.html">Read the design rules</a>
      </div>
    </div>
    <ol class="toc">{toc}</ol>
  </div>
</section>
<section class="wrap" aria-label="At a glance">
  <div class="stat-row">
    <div><b>9</b><span>modules across three core courses</span></div>
    <div><b>5</b><span>security topics across the nine modules</span></div>
    <div><b>25</b><span>survey responses from three offerings</span></div>
    <div><b>3</b><span>modules at most in one semester</span></div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>A separate course does not reach the students who need this.</h2>
    </div>
    <div class="cards-3">
      <article class="card">
        <p class="num">Limited reach</p>
        <h3>The elective is taken by a few.</h3>
        <p>At the University of Florida, fewer than 7% of undergraduate electrical and computer engineering students register for the introductory hardware security course in a given year. Students who never enroll in that elective do not see reverse engineering, side-channel analysis, or logic locking.</p>
      </article>
      <article class="card">
        <p class="num">Cost</p>
        <h3>A new course is expensive to keep.</h3>
        <p>A dedicated course needs an instructor who already knows the subject, a lab of special equipment, and a slot in a crowded curriculum. Teaching-focused departments compete for a hire they are unlikely to make. A course taken by a small fraction of the majors is hard to justify.</p>
      </article>
      <article class="card">
        <p class="num">Fragmented view</p>
        <h3>The attack is taught apart from the circuit.</h3>
        <p>Many of these failures start in the implementation. A timing leak comes from data-dependent control flow. A power leak comes from CMOS switching current. Both are properties of the circuit the student is already designing, not topics to postpone until a later elective.</p>
      </article>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="principle">
      <p>A security topic belongs in a core course when the lab requires a design concept already on the syllabus. Running the attack, or building the countermeasure, is how the student practices that concept.</p>
      <span>The selection principle</span>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head">
      <h2>Nine modules</h2>
      <p>Three have survey data from embedded systems. Two more have been taught. Four are written and ready to run. Pick at most three in a term.</p>
    </div>
    <div class="mod-grid">{cards}</div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head">
      <h2>Where they sit</h2>
      <p>Each module is scheduled in the week the host course covers the design topic it uses. The lab keeps the debugger, the vendor tools, and the bench instruments the course already has.</p>
    </div>
    <div class="course-grid">
      <article class="course-card">
        <p class="where">Embedded systems · EECS 388</p>
        <h3>Firmware and the board</h3>
        <ol>
          <li><a href="modules/m1.html">Binary reverse engineering</a></li>
          <li><a href="modules/m2.html">Buffer overflow</a></li>
          <li><a href="modules/m3.html">Timing side channel</a></li>
          <li><a href="modules/m4.html">Board reverse engineering</a></li>
        </ol>
      </article>
      <article class="course-card">
        <p class="where">Digital logic</p>
        <h3>Gates, adders, and state machines</h3>
        <ol>
          <li><a href="modules/m5.html">Power side channel</a></li>
          <li><a href="modules/m6.html">Combinational logic locking</a></li>
          <li><a href="modules/m7.html">Hardware Trojan insertion</a></li>
          <li><a href="modules/m8.html">Sequential logic locking</a></li>
        </ol>
      </article>
      <article class="course-card">
        <p class="where">Computer architecture</p>
        <h3>The memory hierarchy as a channel</h3>
        <ol>
          <li><a href="modules/m9.html">Cache side channel</a></li>
        </ol>
        <p>Each module adds about 30 to 40 minutes of lecture. The rest replaces a lab or homework the course already assigned.</p>
      </article>
    </div>
    <p style="margin-top:1.4rem"><a class="btn btn-ghost" href="courses.html">See the course map</a></p>
  </div>
</section>
''')

    page("framework.html", "Framework · Hardware Security for All",
         "Five design rules for placing a hardware security module inside a core undergraduate design course.",
         "framework", f'''
<div class="page">
  <div class="wrap page-intro">
    <p class="kicker">Method</p>
    <h1>The contextual learning framework</h1>
    <p class="lede">A security module stays in a core course only when the lab requires a concept that course already teaches. A topic that needs a new instrument, a new instruction set, or a cipher the course does not cover belongs in a separate course.</p>
  </div>
  <div class="wrap">
    <figure class="framework-fig">
      <img src="assets/figure1.svg" alt="Diagram of the framework: core design courses connect to security concepts, then to course-specific modules, then to assessment.">
    </figure>
    <p class="note">A core course supplies the design topic. A security topic is attached to that topic, and the result is a module for that course. Only some modules have survey results. M1 through M4 are embedded systems. M5 through M8 are digital logic. M9 is computer architecture.</p>

    <h2>Why integrate, instead of adding an elective</h2>
    <div class="cards-3">
      <article class="card"><p class="num">A1</p><h3>Security education for all</h3><p>Core design courses are required. The material reaches students who would never enroll in a hardware security elective, and it trains the faculty who already teach those courses.</p></article>
      <article class="card"><p class="num">A2</p><h3>The attack next to the implementation</h3><p>An implementation attack is clearer beside the circuit, the instruction set, or the calling convention that produces it.</p></article>
      <article class="card"><p class="num">A3</p><h3>A cost a department can keep</h3><p>There is no new course to staff, equip, and defend in a curriculum committee. The same placement rules can later carry other topics a program needs, such as machine learning at the edge.</p></article>
    </div>

    <h2>Five rules a module has to meet</h2>
    <div class="rule-list">
      <article class="rule"><b>C1</b><div><h3>Concept coupling</h3><p>The security topic is chosen because the lab requires a design concept already on the syllabus. How well known the attack is in the research literature does not decide the choice.</p></div></article>
      <article class="rule"><b>C2</b><div><h3>Instrument reuse</h3><p>The module uses tools the laboratory already owns and the course already teaches: the debugger, the vendor IDE, a logic analyzer, a multimeter. A new instrument is what keeps another department from adopting the module.</p></div></article>
      <article class="rule"><b>C3</b><div><h3>A paired countermeasure, where the target allows one</h3><p>M2 asks the student to repair the overflow on a machine that has no stack canary and no address-space layout randomization. M3 measures a constant-time comparison again on the same logic analyzer. M6 and M8 have the student build the lock. M1, M4, and M5 end with no countermeasure, and the materials say so.</p></div></article>
      <article class="rule"><b>C4</b><div><h3>Sequence alignment</h3><p>The module is placed in the week the course covers the concept the lab uses. A security lab that comes after that unit’s exam no longer reinforces the design topic.</p></div></article>
      <article class="rule"><b>C5</b><div><h3>Split acquisition and analysis</h3><p>Some labs need more time than one period. Keep the measurement in the lab. Identifying parts, reading a trace, and interpreting a waveform can be finished afterward. In every surveyed class, students asked for worked examples and time. They did not ask for new equipment.</p></div></article>
    </div>

    <h2>What the nine modules cover</h2>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Security concept</th><th>Where the threat starts</th><th>Modules</th></tr></thead>
        <tbody>
          <tr><td>Reverse engineering</td><td>Field</td><td>M1, M4</td></tr>
          <tr><td>Side-channel analysis</td><td>Field</td><td>M3, M5, M9</td></tr>
          <tr><td>IP protection and obfuscation</td><td>Supply chain</td><td>M6, M8</td></tr>
          <tr><td>Hardware Trojan</td><td>Supply chain</td><td>M7</td></tr>
          <tr><td>Memory safety</td><td>Outside field and supply chain</td><td>M2</td></tr>
        </tbody>
      </table>
    </div>
    <p>The nine modules do not cover fabrication-time threats, physical unclonable functions, bus snooping, fault injection, or gate-level and device-level reverse engineering. Device-level reverse engineering needs decapsulation and imaging. That needs equipment the course does not already have, so it is out. A semester holds at most three modules. The catalog is a set of choices, not a full syllabus.</p>

    <h2>A topic that fails the test</h2>
    <p>Fault injection on a cryptographic core needs a clock glitcher, a device with a crypto accelerator, and a lecture on the cipher. None of that is in a first embedded-systems course, so the topic stays out of these modules. The same test rejected any module that would require a new instrument.</p>
    <p><a class="btn btn-primary" href="catalog.html">Browse the catalog</a></p>
  </div>
</div>
''')

    filter_cards = "\n".join(
        f'''<a class="mod-card" data-course="{m["course"]}" data-status="{m["status"]}" href="modules/{m["slug"]}.html">
          <span class="id">{m["id"]}</span><h3>{m["title"]}</h3><p>{m["blurb"]}</p>
          <div class="meta">{pills(m)}</div></a>'''
        for m in modules
    )
    rows = "\n".join(
        f'''<tr>
          <td><a href="modules/{m["slug"]}.html">{m["id"]}</a></td>
          <td>{m["title"]}</td>
          <td>{m["course_label"]}</td>
          <td>{m["status_label"]}</td>
          <td>{m["concept"]}</td>
          <td>{m["platform"]}</td>
          <td>{m["evidence"]}</td>
        </tr>'''
        for m in modules
    )
    page("catalog.html", "Module catalog · Hardware Security for All",
         "Nine hardware security modules, the design topic each one uses, and the work a student turns in.",
         "catalog", f'''
<div class="page">
  <div class="wrap">
    <div class="page-intro">
      <p class="kicker">Catalog</p>
      <h1>Nine modules, each tied to a design concept.</h1>
      <p class="lede">Surveyed means students answered a survey. Taught means the module ran, and there was no survey. Written means the lab is ready and has not been graded yet.</p>
    </div>
    <div class="filters" role="group" aria-label="Filter by course">
      <button type="button" data-filter="course" data-value="all" aria-pressed="true">All courses</button>
      <button type="button" data-filter="course" data-value="es" aria-pressed="false">Embedded systems</button>
      <button type="button" data-filter="course" data-value="dl" aria-pressed="false">Digital logic</button>
      <button type="button" data-filter="course" data-value="ca" aria-pressed="false">Computer architecture</button>
    </div>
    <div class="filters" role="group" aria-label="Filter by status">
      <button type="button" data-filter="status" data-value="all" aria-pressed="true">Any status</button>
      <button type="button" data-filter="status" data-value="surveyed" aria-pressed="false">Surveyed</button>
      <button type="button" data-filter="status" data-value="taught" aria-pressed="false">Taught</button>
      <button type="button" data-filter="status" data-value="ready" aria-pressed="false">Written</button>
    </div>
    <div class="mod-grid">{filter_cards}</div>
    <h2>Full record</h2>
    <div class="table-wrap">
      <table>
        <thead><tr><th>#</th><th>Module</th><th>Course</th><th>Status</th><th>Design topic</th><th>Platform</th><th>Student work</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  </div>
</div>
''')

    page("courses.html", "Courses · Hardware Security for All",
         "How the modules attach to embedded systems, digital logic, and computer architecture, and how the suite grew from 2022 to 2024.",
         "courses", '''
<div class="page">
  <div class="wrap page-intro">
    <p class="kicker">Host courses</p>
    <h1>Each module belongs inside a course the department already teaches.</h1>
    <p class="lede">The host course keeps its syllabus, exams, and grading. The security lab replaces an assignment that course would have given anyway, in the week that design topic is taught.</p>
  </div>
  <div class="wrap">
    <div class="course-grid">
      <article class="course-card">
        <p class="where">EECS 388 · University of Kansas</p>
        <h3>Embedded systems</h3>
        <p>Target is the Microchip AT89C51, programmed and debugged in Keil. Spring 2024 ran M1, M2, and M3 as required work, two points each. Spring 2023 ran M1 as homework and M2 as a bonus. M4 is specified for the same course and has not been assigned.</p>
        <ol>
          <li><a href="modules/m1.html">M1 Binary reverse engineering</a></li>
          <li><a href="modules/m2.html">M2 Buffer overflow</a></li>
          <li><a href="modules/m3.html">M3 Timing side channel</a></li>
          <li><a href="modules/m4.html">M4 Board reverse engineering</a></li>
        </ol>
      </article>
      <article class="course-card">
        <p class="where">Digital logic design</p>
        <h3>From gates to a UART</h3>
        <p>M5 began as a circuit-simulator homework. M6, M7, and M8 are VHDL labs adapted from hardware-security lab material and from a published tutorial on obfuscation and logic locking. They use a register-transfer design flow that the microcontroller modules do not. They have not yet been surveyed.</p>
        <ol>
          <li><a href="modules/m5.html">M5 Power side channel</a></li>
          <li><a href="modules/m6.html">M6 Combinational locking</a></li>
          <li><a href="modules/m7.html">M7 Hardware Trojan</a></li>
          <li><a href="modules/m8.html">M8 Sequential locking</a></li>
        </ol>
      </article>
      <article class="course-card">
        <p class="where">Computer architecture · Fall 2024</p>
        <h3>Cache timing</h3>
        <p>M9 ran as two lecture parts with a recorded measurement on a commodity x86 machine. No survey was given, and the source notes do not state a graded assignment.</p>
        <ol>
          <li><a href="modules/m9.html">M9 Cache side channel</a></li>
        </ol>
      </article>
    </div>

    <h2>How the suite grew</h2>
    <div class="timeline">
      <article class="time"><b>Spring 2022</b><p>Side-channel content as a paper and simulator exercise. An early form of the power module.</p></article>
      <article class="time"><b>Spring 2023</b><p>Binary reverse engineering required. Buffer overflow offered as a bonus. Internal survey, 13 responses.</p></article>
      <article class="time"><b>Spring 2024</b><p>M1, M2, and M3 each have a two-part lecture and a required assignment. External evaluation, 8 of 13 students.</p></article>
      <article class="time"><b>Fall 2024</b><p>The same three embedded modules again, plus the cache lecture in computer architecture. External evaluation, 4 responses.</p></article>
      <article class="time"><b>Prepared</b><p>Board reverse engineering, both locking labs, and the Trojan lab. Written, not yet surveyed.</p></article>
    </div>
    <h2>What changed in the grade book</h2>
    <p>In Spring 2023 the reverse-engineering homework was worth 10.5 points and the buffer-overflow bonus was worth 20. In Spring 2024 each of the three assignments was worth 2 points. One student skipped the bonus and then met the calling convention on the final. A module that practices a syllabus topic can be on the exam. Making it optional tells students both that it matters and that they can skip it.</p>
    <p>The cap is three modules in a semester, so the security work does not turn into a second course inside the first.</p>
  </div>
</div>
''')

    page("assessment.html", "Results · Hardware Security for All",
         "Survey results from three offerings of the embedded-systems modules, and what those surveys cannot show.",
         "assessment", '''
<div class="page">
  <div class="wrap page-intro">
    <p class="kicker">Deployment record</p>
    <h1>What 25 students reported, and what that does not prove.</h1>
    <p class="lede">Only M1, M2, and M3 have survey results. The classes were not randomized, and no class ran without the modules. The knowledge ratings are what students said about themselves. These counts are a deployment report. They are not a statistical result.</p>
  </div>
  <div class="wrap">
    <div class="table-wrap">
      <table>
        <thead><tr><th>Cohort</th><th>Term</th><th>Survey</th><th>Modules</th><th>Enrolled</th><th>Responses</th></tr></thead>
        <tbody>
          <tr><td>C1</td><td>Spring 2023</td><td>Internal</td><td>M1, M2</td><td>Not recorded</td><td>13</td></tr>
          <tr><td>C2</td><td>Spring 2024</td><td>External evaluator</td><td>M1, M2, M3</td><td>13</td><td>8 (62%)</td></tr>
          <tr><td>C3</td><td>Fall 2024</td><td>External evaluator</td><td>M1, M2, M3</td><td>Not recorded</td><td>4</td></tr>
        </tbody>
      </table>
    </div>
    <p class="note">C1, C2, and C3 in this table are the three classes. They are not the design rules C1 through C5.</p>
    <p>The survey questions changed between Spring 2024 and Fall 2024, so those two classes should not be compared item by item. A response rate is known only for Spring 2024: 8 of 13 students. Of those eight, five were men, three were women, and six identified as Hispanic or Latino. All four Fall 2024 respondents were men, and one identified as Asian.</p>

    <h2>Self-reported knowledge, Fall 2024</h2>
    <p>Four-point scale. One is no knowledge and four is strong knowledge. These are self-reported ratings. There is no concept inventory behind them.</p>
    <div class="legend"><span><i class="swatch before"></i>Before</span><span><i class="swatch after"></i>After</span></div>
    <div class="bars">
      <div class="bar-row"><span>Binary reverse engineering</span><div class="track"><i class="before" style="--w:32.5"></i><i class="after" style="--w:62.5"></i></div></div>
      <div class="bar-row"><span>Buffer overflow</span><div class="track"><i class="before" style="--w:45"></i><i class="after" style="--w:62.5"></i></div></div>
      <div class="bar-row"><span>Side channel</span><div class="track"><i class="before" style="--w:25"></i><i class="after" style="--w:50"></i></div></div>
    </div>
    <p>Read as 1.3 to 2.5 for binary reverse engineering, 1.8 to 2.5 for buffer overflow, and 1.0 to 2.0 for side channels. Interest in hardware security on a ten-point scale moved from 2.8 to 4.5 in this cohort. Spring 2024 reported 9.1 at the end and has no matching start value, so that figure is a terminal value, not a gain.</p>

    <h2>Spring 2023 usefulness ratings</h2>
    <p>Five-point scale. The midpoint is 3. Means sat below it. Students were not enthusiastic about the early handouts, which is part of why later versions added worked structure.</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Item</th><th>Mean</th><th>SD</th><th>N</th></tr></thead>
        <tbody>
          <tr><td>M1 usefulness for learning binary reverse engineering</td><td>2.77</td><td>1.25</td><td>13</td></tr>
          <tr><td>M1 contribution to assembly and instruction encoding</td><td>2.69</td><td>1.20</td><td>13</td></tr>
          <tr><td>M1 adequacy of materials and lecture</td><td>2.83</td><td>1.14</td><td>12</td></tr>
          <tr><td>M2 usefulness for learning buffer overflow</td><td>2.73</td><td>1.21</td><td>11</td></tr>
          <tr><td>M2 usefulness for a prior understanding of memory layout</td><td>2.36</td><td>1.23</td><td>11</td></tr>
          <tr><td>M2 adequacy of materials and lecture</td><td>2.55</td><td>1.50</td><td>11</td></tr>
        </tbody>
      </table>
    </div>

    <h2>What students said the modules did</h2>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Item</th><th>Spring 2024</th><th>Fall 2024</th></tr></thead>
        <tbody>
          <tr><td>More hands-on work than in other courses</td><td>87% yes</td><td>100% yes</td></tr>
          <tr><td>Modules helped with embedded-systems fundamentals</td><td>87% yes</td><td>25% yes</td></tr>
          <tr><td>Changed interest in a graduate degree</td><td>75% yes</td><td>0% yes</td></tr>
          <tr><td>Sought a hardware-security internship</td><td>100% yes</td><td>Not asked</td></tr>
          <tr><td>Wants a career in hardware security</td><td>50% yes</td><td>Not asked</td></tr>
          <tr><td>Wants more hardware-security modules</td><td>50% yes</td><td>Not asked</td></tr>
          <tr><td>Needs more time to finish the assignments</td><td>75% yes</td><td>25%</td></tr>
          <tr><td>Workload against similar courses</td><td>63% more</td><td>75% about the same</td></tr>
          <tr><td>Overall experience, ten-point scale</td><td>7.6</td><td>Not asked</td></tr>
        </tbody>
      </table>
    </div>
    <p>The split on fundamentals is the result to keep. Spring 2024 agreed that the modules helped them understand embedded systems. Fall 2024 mostly did not. Half of the Fall respondents reported that they did not attempt the assignments. The sample is small. The two cohorts should not be averaged into one success rate.</p>

    <h2>Barriers they named</h2>
    <p>Students chose from a fixed list: worked examples, lecture, study materials, time, and teaching-assistant support. Equipment was not on the list. Their answers are about teaching, not about missing instruments.</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Barrier</th><th>Spring 2023, M1, share of selections</th><th>Spring 2023, M2, share of selections</th><th>Fall 2024, share of respondents</th></tr></thead>
        <tbody>
          <tr><td>Worked examples</td><td>33.3%</td><td>28.6%</td><td>0%</td></tr>
          <tr><td>Class lecture</td><td>29.2%</td><td>33.3%</td><td>25%</td></tr>
          <tr><td>Study materials</td><td>16.7%</td><td>19.0%</td><td>25%</td></tr>
          <tr><td>More time</td><td>12.5%</td><td>14.3%</td><td>25%</td></tr>
          <tr><td>Teaching-assistant support</td><td>8.3%</td><td>4.8%</td><td>50%</td></tr>
        </tbody>
      </table>
    </div>
    <p>The Spring 2023 shares come from 24 selections on M1 and 21 on M2. Fall 2024 is four people. Spring 2024 was not asked this question.</p>

    <h2>Four lessons for the next offering</h2>
    <div class="rule-list">
      <article class="rule"><b>1</b><div><h3>Students wrote most clearly about the repair.</h3><p>One Spring 2023 student called the buffer-overflow assignment among the most interesting work in the program, and described finding where execution had to resume so that later secrets would return in R7. M1 has no countermeasure. Students asked what binary reverse engineering is for.</p></div></article>
      <article class="rule"><b>2</b><div><h3>A desktop mitigation is not on the 8051.</h3><p>The lecture names stack canaries and address-space layout randomization. Neither exists on the AT89C51. The repair has to be in the program, because the platform does not provide one.</p></div></article>
      <article class="rule"><b>3</b><div><h3>Worked examples mattered more than new equipment.</h3><p>The 2024 overflow handout adds partial credit by how far the leak gets, and it adds step-by-step hints. Both match the barrier the surveys recorded: examples, lecture, and time, not instruments.</p></div></article>
      <article class="rule"><b>4</b><div><h3>The toolchain has to run on the machines students have.</h3><p>Free responses include a student who could not run the vendor tools on a personal machine. The three deployed embedded modules share one 8-bit target, the AT89C51, and one vendor IDE, Keil. Whether the same labs carry to a 32-bit core is untested.</p></div></article>
    </div>
  </div>
</div>
''')

    page("adopt.html", "Adopt a module · Hardware Security for All",
         "How an instructor chooses, places, and runs a module without standing up a new hardware security course.",
         "adopt", '''
<div class="page">
  <div class="wrap page-intro">
    <p class="kicker">For instructors</p>
    <h1>Place one module in the week the concept is already taught.</h1>
    <p class="lede">Start from the design topic on your syllabus, then pick the module that makes a student use it. Do not start from a list of famous attacks and look for a week to put them in.</p>
  </div>
  <div class="wrap">
    <div class="rule-list">
      <article class="rule"><b>1</b><div><h3>Choose at most three.</h3><p>That cap is deliberate. Spring 2024 ran binary reverse engineering, buffer overflow, and the timing side channel. A fourth module in the same term starts to feel like a second course.</p></div></article>
      <article class="rule"><b>2</b><div><h3>Budget half a lecture, and reuse a lab slot.</h3><p>Plan 30 to 40 minutes of new lecture for each module. The student work replaces an existing homework or lab, it does not stack on top of one. For embedded systems, the natural slots are the weeks on the toolchain, the calling convention, and the timer and serial port.</p></div></article>
      <article class="rule"><b>3</b><div><h3>Use instruments you already teach.</h3><p>M1 through M3 need Keil and an AT89C51 target or a faithful simulation of it, plus the logic analyzer built into the debugger for M3. M4 needs a populated board and a multimeter, and a logic analyzer only for the optional protocol check. M5 needs a browser. M6 through M8 need a VHDL simulator. M9 needs a student laptop.</p></div></article>
      <article class="rule"><b>4</b><div><h3>Grade the repair when there is one.</h3><p>On M2 and M3 the second half is the point: a bounded copy, and a constant-time comparison measured again. On M6 and M8 the lock itself is the work. If you make the module extra credit, expect some students to skip it and then meet it on the exam.</p></div></article>
      <article class="rule"><b>5</b><div><h3>Keep the bench work and the write-up apart.</h3><p>Taking the board apart needs the lab. Reading datasheets and drawing the block diagram does not. The same split helps M3 when setting up the logic analyzer takes the whole period.</p></div></article>
    </div>

    <h2>A reasonable first adoption</h2>
    <div class="cards-3">
      <article class="card"><p class="num">Embedded systems</p><h3>M1, then M2, then M3</h3><p>This is the sequence that has been taught and surveyed. Run them in that order. M2 assumes the student can already read the memory windows from M1. M3 assumes the timer and the serial port.</p></article>
      <article class="card"><p class="num">Digital logic</p><h3>M6, then M7</h3><p>Students build the adder and lock it, then receive that locked design and add a Trojan without touching the lock. M8 can replace M7 if the course is about to teach state machines. M5 can stand alone in the week on CMOS power.</p></article>
      <article class="card"><p class="num">Computer architecture</p><h3>M9 beside the cache lecture</h3><p>Two parts. The first reads the machine’s own cache geometry. The second treats a hit and a miss as a channel. There is a recorded measurement and no separate graded write-up in the archive.</p></article>
    </div>

    <h2>What this site publishes</h2>
    <p>Student handouts, slide decks, starter VHDL, the C sources for the embedded labs, and the binary used in the reverse-engineering homework. Lab manuals for the three VHDL experiments are included as documents because they carry the figures.</p>
    <div class="callout">
      <strong>Solution archives are not in this bundle.</strong>
      <p>Instructor guides, reference VHDL with completed Trojans and completed locks, and the solved homework from earlier offerings stay in the project archive. Lecture recordings from Spring 2023 are in that archive too. Ask the KU group for the instructor packet.</p>
    </div>
    <p>Two further exclusions. The published tutorial on obfuscation and logic locking is cited from the VHDL labs and is not redistributed here. A gem5 cache configuration script that ships beside the cache slides is third-party teaching code and is not copied onto this site.</p>
    <p><a class="btn btn-primary" href="about.html">Contact the project</a></p>
  </div>
</div>
''')

    page("about.html", "About · Hardware Security for All",
         "The people, institutions, and paper behind the Hardware Security for All modules.",
         "about", '''
<div class="page">
  <div class="wrap page-intro">
    <p class="kicker">Project</p>
    <h1>Hardware Security Education for All</h1>
    <p class="lede">A collaborative curriculum project. The modules let a department teach hardware security inside required design courses, so students who never enroll in a hardware-security elective still meet reverse engineering, side channels, logic locking, and hardware Trojans.</p>
  </div>
  <div class="wrap">
    <h2>People</h2>
    <div class="team">
      <article class="person"><b>Tanvir Hossain</b><span>EECS, University of Kansas · tanvir@ku.edu</span></article>
      <article class="person"><b>Mahmudul Hasan</b><span>EECS, University of Kansas · m.hasan@ku.edu</span></article>
      <article class="person"><b>Kareem El-Araby</b><span>EECS, University of Kansas</span></article>
      <article class="person"><b>Lorenzo R. Godinez</b><span>EECS, University of Kansas</span></article>
      <article class="person"><b>Swarup Bhunia</b><span>ECE, University of Florida · swarup@ece.ufl.edu</span></article>
      <article class="person"><b>Md Tauhidur Rahman</b><span>ECE, Florida International University · mdtrahma@fiu.edu</span></article>
      <article class="person"><b>Tamzidul Hoque</b><span>EECS, University of Kansas · hoque@ku.edu</span></article>
    </div>
    <p class="note">Email addresses follow the author block of the curriculum paper. For an instructor packet, write to the Kansas group.</p>

    <h2>The paper this site follows</h2>
    <p>This site follows the paper <em>Bringing Hardware Security Education to All: A Seamless Curriculum Integration Approach</em>, prepared for ISQED 2027. The paper states the three obstacles, the five design rules, the nine modules, where each one has been taught, and the limits of the survey results.</p>
    <p>If a lab manual and the paper disagree on a step, students follow the manual. This site uses the paper for status, scope, and survey results.</p>
    <p>The paper also states the workforce context. An industry analysis projects growth in the U.S. semiconductor workforce from about 345,000 to about 460,000 positions by 2030, with a large share of new technical roles at risk of going unfilled. Employment of information security analysts is projected to grow much faster than employment overall. The required courses in the programs that train those graduates still skip hardware security.</p>

    <h2>What a department can take</h2>
    <ul>
      <li>The <a href="framework.html">selection principle and the five rules</a>, if you want to write a module of your own.</li>
      <li>The <a href="catalog.html">catalog</a>, if you want to drop an existing module into a course you already teach.</li>
      <li>The <a href="assessment.html">results</a>, if you need to know what has been taught and what is still only written down.</li>
    </ul>
    <p>The site is a set of static pages. Nothing here needs a server-side application.</p>
  </div>
</div>
''')

    module_page(by_id["M1"], intro(
        "Binary reverse engineering recovers what a program does from the machine code when the C source is not available. Many embedded devices ship as a firmware binary only.",
        "<strong>Course:</strong> Embedded systems. At KU this was EECS 388.<br><strong>Teach this after:</strong> compilation, the instruction set, addressing modes, and the difference between code memory and data memory. The last question also uses the stack pointer.",
        '''<p>Use the two slide decks as the class lectures. Then assign the homework and the binary. Older lecture recordings are not posted here.</p>
<ul>
  <li><strong>Lecture, part 1.</strong> Use in class before anyone opens the binary. Motivation, the 8051 instruction set and registers, and a Keil walkthrough.</li>
  <li><strong>Lecture, part 2.</strong> Use in class after part 1 and still before the homework. The memory map, addressing modes, and the disassembly and memory windows.</li>
  <li><strong>Homework handout.</strong> The graded assignment. Spring 2024 scored it at two points. Hand it out after both lectures.</li>
  <li><strong>unknown-1.</strong> The binary named in the handout. Students load it in Keil. Keep the source out of the student bundle.</li>
</ul>
<div class="downloads">
  <a class="download" href="../materials/m1/Module1_RE_part1.pptx"><span><b>Lecture, part 1</b><span>Motivation, 8051, Keil</span></span><i>PPTX</i></a>
  <a class="download" href="../materials/m1/Module1_RE_part2.pptx"><span><b>Lecture, part 2</b><span>Memory map and disassembly</span></span><i>PPTX</i></a>
  <a class="download" href="../materials/m1/Module1_Homework_BRE.pdf"><span><b>Homework handout</b><span>Spring 2024, two points</span></span><i>PDF</i></a>
  <a class="download" href="../materials/m1/unknown-1"><span><b>Binary to analyze</b><span>File name from the handout: unknown-1</span></span><i>BIN</i></a>
</div>''',
        [
            "Rostami, Koushanfar, and Karri, “A Primer on Hardware Security: Models, Methods, and Metrics,” <em>Proceedings of the IEEE</em>, vol. 102, no. 8, pp. 1283–1295, 2014.",
            "Azriel, Speith, Albartus, Ginosar, Shamir, and Paar, “A Survey of Algorithmic Methods in IC Reverse Engineering,” <em>Journal of Cryptographic Engineering</em>, vol. 11, pp. 299–315, 2021. Chip imaging and netlist recovery. This module stops at a firmware binary.",
        ],
        [
            '<a href="https://www.youtube.com/watch?v=9tZmSFjoOm4">Reverse Engineering</a> (Computerphile). What a binary still reveals after compilation. The examples use desktop tools, not the AT89C51.',
            '<a href="https://www.youtube.com/watch?v=a5PwvIRrh9M">Mohammad Tehranipoor on Integrated Circuit Security</a> (UConn). A short faculty talk on why the chip is part of the security problem. Broader than this homework.',
        ],
    ) + '''
<h2>The exercise</h2>
<p>The program behind the binary keeps a hospital room at a stable temperature. It reads a sensor value from external memory six times an hour, folds each sample into a running average with the previous average, compares that average with a threshold, and drives a port pin from the result. Students receive the binary and the part number, the Microchip AT89C51. They do not receive the source.</p>
<div class="outcome"><p class="outcome-title">Outcome</p><p>The student recovers the sampling rate, the stored temperatures and their addresses, the threshold, and the output port, and explains what happens if the conditional jump that returns to the start of the program is replaced by a call.</p></div>
<h2>The ten questions</h2>
<p>The Spring 2024 handout, worth two points, asks the student to work only from the disassembly window.</p>
<ol>
  <li>Address of the <code>START</code> label.</li>
  <li>Initial return address of the first call.</li>
  <li>How many times the program reads external memory.</li>
  <li>Last hour’s temperature, in decimal, before averaging.</li>
  <li>The mean temperature after averaging.</li>
  <li>The threshold, in decimal.</li>
  <li>The temperature values stored in external memory, and their locations.</li>
  <li>Which port carries the output signal.</li>
  <li>Whether that signal is actually driven from the temperatures found in memory.</li>
  <li>At <code>C:0x034D</code> the program returns to <code>START</code> with <code>JNZ</code>. What happens if that opcode is replaced by <code>ACALL</code>.</li>
</ol>
<p>The last question is about the stack. <code>ACALL</code> pushes a return address. This loop never executes a return, so return addresses accumulate in internal RAM until they overwrite other data. The module stops there. It does not teach a countermeasure.</p>
''')

    module_page(by_id["M2"], intro(
        "A buffer overflow writes past the end of a fixed buffer. On the AT89C51 that write can change adjacent internal RAM, including a saved return address.",
        "<strong>Course:</strong> Embedded systems. At KU this was EECS 388, after binary reverse engineering.<br><strong>Teach this after:</strong> the stack frame and the calling convention. Count the homework as required work, not extra credit.",
        '''<p>Use the two slide decks as the class lectures. Then assign the homework. Students build the C file in Keil.</p>
<ul>
  <li><strong>Lecture, part 1.</strong> Use in class after the calling-convention lecture. The stack, the saved return address, and how an overrun reaches them.</li>
  <li><strong>Lecture, part 2.</strong> Use in class before the homework. The 8051 memory map, and how the lab is scored.</li>
  <li><strong>Homework handout.</strong> The graded assignment. Spring 2024 scored it at two points.</li>
  <li><strong>vulnerable_program.c.</strong> The starter students compile. The handout is written against this file.</li>
</ul>
<div class="downloads">
  <a class="download" href="../materials/m2/Module2_BufferOverflow_part1.pptx"><span><b>Lecture, part 1</b><span>Stack, calling convention, the attack</span></span><i>PPTX</i></a>
  <a class="download" href="../materials/m2/Module2_BufferOverflow_part2.pptx"><span><b>Lecture, part 2</b><span>The 8051 memory map and the lab</span></span><i>PPTX</i></a>
  <a class="download" href="../materials/m2/Module1_Homework_BOA.pdf"><span><b>Homework handout</b><span>Spring 2024, two points</span></span><i>PDF</i></a>
  <a class="download" href="../materials/m2/vulnerable_program.c"><span><b>Starter program</b><span>8051 C, Keil</span></span><i>C</i></a>
</div>''',
        [
            '<a href="https://phrack.org/issues/49/14.html">Smashing the Stack for Fun and Profit</a>, Aleph One, <em>Phrack</em>, vol. 7, no. 49, 1996. The classic account of a stack overrun on a desktop. This lab is the same idea on a machine with 256 bytes of internal data memory.',
            "Cowan, Pu, Maier, and others, “StackGuard: Automatic Adaptive Detection and Prevention of Buffer-Overflow Attacks,” USENIX Security Symposium, pp. 63–78, 1998.",
            "Szekeres, Payer, Wei, and Song, “SoK: Eternal War in Memory,” IEEE Symposium on Security and Privacy, pp. 48–62, 2013.",
        ],
        [
            '<a href="https://www.youtube.com/watch?v=1S0aBV-Waeo">Running a Buffer Overflow Attack</a> (Computerphile). A desktop demonstration of an overrun. The repair in this module has to be a property of the program, because the AT89C51 supplies neither a stack canary nor address-space randomization.',
            '<a href="https://www.youtube.com/watch?v=ldq8ZMjoXpM">Buffer overflow: how do cybercriminals take over your computer?</a> (Frank Stajano, security@cambridge). A short classroom explanation of the same idea.',
        ],
    ) + '''
<h2>The exercise</h2>
<p>A lookup routine returns a stored secret when a supplied date matches a record. The copy into the input buffer does not check the buffer length.</p>
<p>On a desktop, a saved frame pointer and a saved return address sit in separate words. On the AT89C51, internal data memory is 256 bytes. The register banks occupy the low addresses, and constants are copied from code memory at startup. This chip has no stack canary and no address-space layout randomization.</p>
<div class="outcome"><p class="outcome-title">Outcome</p><p>The student leaks successive secrets through R7, then rewrites the copy so it cannot leave the buffer, and explains why that rewrite holds on this processor.</p></div>
<h2>What the student does</h2>
<ol class="steps">
  <li>Read the provided C program and find the unbounded copy and the records it is meant to protect.</li>
  <li>Build an input long enough to disturb neighboring memory, and watch the debugger. The handout scores the length of that input, then whether the first secret appears in R7, then the first and second, then more than two.</li>
  <li>Repair the program so data cannot be written past the buffer, and explain in writing how the change prevents the overflow.</li>
</ol>
<p>The lecture names stack canaries and address-space layout randomization, then the lab removes both. The repair has to be a bounds check in this program. Partial credit follows how far the leak gets, so a student who can read the memory map but does not recover every secret still has a score.</p>
<p>In Spring 2023 this assignment was a bonus. From Spring 2024 it is required. Treat it as required if you adopt it. Students who skip a bonus still meet the calling convention on the exam.</p>
''')

    module_page(by_id["M3"], intro(
        "A timing side channel leaks the secret through execution time. This password check returns at the first mismatch, so a wrong first character finishes in fewer cycles than a wrong later character.",
        "<strong>Course:</strong> Embedded systems. At KU this was the third module in EECS 388.<br><strong>Teach this after:</strong> the timer, cycle counting, and the serial port.",
        '''<p>Use the two slide decks as the class lectures. Then assign the homework. Students time the check with the logic analyzer in Keil.</p>
<ul>
  <li><strong>Lecture, part 1.</strong> Use in class after the timer lecture. Five emissions an attacker can measure, the data dependence of CMOS switching energy, and Kocher’s timing attack reduced to a string comparison.</li>
  <li><strong>Lecture, part 2.</strong> Use in class before the homework. How the lab instruments the comparison, and the demonstration cycle counts below.</li>
  <li><strong>Homework handout.</strong> The graded assignment. Spring 2024 scored it at two points. It uses its own password and its own guesses.</li>
  <li><strong>sca_sp24.c.</strong> The starter students build. It contains the early-exit check they measure, then replace.</li>
</ul>
<div class="downloads">
  <a class="download" href="../materials/m3/Module3_TimingSCA_part1.pptx"><span><b>Lecture, part 1</b><span>Emissions, power, Kocher</span></span><i>PPTX</i></a>
  <a class="download" href="../materials/m3/Module3_TimingSCA_part2.pptx"><span><b>Lecture, part 2</b><span>The string comparison, measured</span></span><i>PPTX</i></a>
  <a class="download" href="../materials/m3/Module1_Homework_SCA.pdf"><span><b>Homework handout</b><span>Spring 2024, two points</span></span><i>PDF</i></a>
  <a class="download" href="../materials/m3/sca_sp24.c"><span><b>Starter program</b><span>UART password check</span></span><i>C</i></a>
</div>''',
        [
            "Kocher, “Timing Attacks on Implementations of Diffie–Hellman, RSA, DSS, and Other Systems,” Advances in Cryptology (CRYPTO), pp. 104–113, 1996. The lecture reduces this attack to the string comparison in the lab.",
            "Kocher, Jaffe, and Jun, “Differential Power Analysis,” Advances in Cryptology (CRYPTO), pp. 388–397, 1999. The power channel. This module measures time.",
        ],
        [
            '<a href="https://www.youtube.com/watch?v=p0AuTPmFjTY">Timing Attack on PIN-Protected Hard Drive</a> (Colin O’Flynn). A measured timing leak outside a microcontroller course. Same idea as the early-exit check: a wrong guess can finish early.',
            '<a href="https://www.youtube.com/watch?v=OlX-p4AGhWs">Introduction to Side-Channel Power Analysis</a> (Colin O’Flynn). The power channel named in the first lecture. The graded work in this module is the timer measurement, not a power trace.',
        ],
    ) + '''
<h2>The exercise</h2>
<p>The program grants access when a typed password matches a stored one. The comparison returns at the first mismatch, so the cycle count grows with the length of the correct prefix.</p>
<p>The lecture names five emissions an attacker can measure. One of them is the time this comparison takes. It reduces Kocher’s timing attack on modular exponentiation to that string comparison. The lab measures the comparison with the timer and the logic analyzer.</p>
<div class="outcome"><p class="outcome-title">Outcome</p><p>The student turns in a timing table for the vulnerable check and a second table for a comparison that always walks the whole password, and discusses whether the leak is gone. This is the only module in which the defense is measured on the same instrument as the attack.</p></div>
<h2>How the time is taken</h2>
<ol class="steps">
  <li>Configure the UART. The starter targets 9600 baud on a 12 MHz crystal, Timer 1 in mode 2.</li>
  <li>Set the timer run bit before the password check and clear it after. Read the interval between those edges on the logic analyzer in the debugger. The handout asks for five guesses, terminated with a period.</li>
  <li>Rewrite the comparison so every character is examined regardless of the first mismatch. Repeat the five guesses on the same instrument.</li>
</ol>
<h2>A lecture demonstration, not the graded passwords</h2>
<p>The lecture deck reports eight guesses against a demonstration password. Cycle counts rise as the matching prefix gets longer. The graded assignment uses a different password and a different list of guesses. The figure below is the lecture measurement.</p>
<div class="table-wrap">
  <table>
    <thead><tr><th>Guess</th><th>Machine cycles</th></tr></thead>
    <tbody>
      <tr><td>Howareyou</td><td>122</td></tr>
      <tr><td>Baaaa</td><td>143</td></tr>
      <tr><td>Aaaaa</td><td>152</td></tr>
      <tr><td>Hello</td><td>152</td></tr>
      <tr><td>Iello</td><td>181</td></tr>
      <tr><td>Iaaaa</td><td>188</td></tr>
      <tr><td>Iykpp</td><td>240</td></tr>
      <tr><td>Iykyk</td><td>291</td></tr>
    </tbody>
  </table>
</div>
''')

    module_page(by_id["M4"], intro(
        "Board-level reverse engineering starts from a populated printed circuit board with no schematic. Students identify the parts, write a bill of materials, and draw a block diagram.",
        "<strong>Course:</strong> Embedded systems.<br><strong>Teach this after:</strong> microcontroller interfacing, serial protocols, power distribution, and reading a datasheet. The lab is written and has not been assigned yet. The bench needs a multimeter.",
        '''<p>There is no slide deck. The lab specification is the handout. Read the safety notes before students power the board. The required work fits one lab period.</p>
<ul>
  <li><strong>Lab specification.</strong> Give this to students at the start of the period. It states the required identification work, the optional measurement work, the deliverables, and the evaluation.</li>
  <li>Students need a populated board with no schematic, and a digital multimeter. A logic analyzer is optional and is used only if the course already has one.</li>
</ul>
<div class="downloads">
  <a class="download" href="../materials/m4/Hardware_Reverse_Engineering_Lab_Specification.docx"><span><b>Lab specification</b><span>Required and optional work, deliverables, evaluation</span></span><i>DOCX</i></a>
</div>''',
        [
            "Kleber, Nölscher, and Kargl, “Automated PCB Reverse Engineering,” USENIX Workshop on Offensive Technologies (WOOT), 2017.",
            "Tehranipoor, Guin, and Bhunia, “Invasion of the Hardware Snatchers,” <em>IEEE Spectrum</em>, vol. 54, no. 5, pp. 36–41, 2017. Why a cloned or altered board is a supply-chain problem. This lab stops at identification.",
        ],
        [
            '<a href="https://www.youtube.com/watch?v=BsftxTbs7MA">PCB Reverse Engineering: Eric Schlaepfer</a> (Hackaday). A working engineer walking a board with no schematic.',
            '<a href="https://www.youtube.com/watch?v=O8FQZIPkgZM">Deconstructing the Circuit Board Sandwich</a> (Joe Grand, DEF CON 22). How a multilayer board is taken apart and read.',
            '<a href="https://www.youtube.com/watch?v=18U25M8h7l4">Printed Circuit Board Deconstruction Techniques</a> (USENIX WOOT ’14). A conference talk on the same reconstruction problem.',
        ],
    ) + '''
<h2>The exercise</h2>
<p>The student receives a populated board and no schematic. The required work is identification: a bill of materials and a functional hypothesis for each region of the board. Optional work moves from identification to measurement of the power rails and the serial links.</p>
<div class="outcome"><p class="outcome-title">Outcome</p><p>A bill of materials with part numbers, a high-level block diagram, and a functional hypothesis for each section of the board. The lab specifies no defensive deliverable.</p></div>
<h2>Required</h2>
<ol class="steps">
  <li>Identify components from the ICs down to passives and test points. Capacitor markings can be skipped when the marking is not recoverable.</li>
  <li>Build a bill of materials: description, part number, and value, with datasheets for the ICs.</li>
  <li>Hypothesize what each region does, and write the reason.</li>
  <li>Draw a high-level block diagram once the parts are known.</li>
</ol>
<p>If the board is dense, restrict the required work to one or two chips. The lab period is the constraint the design rule is written for.</p>
<h2>Optional, if the period or a second sitting allows it</h2>
<ul>
  <li>Continuity-map one non-trivial part, such as a sensor or a memory, back to the microcontroller, and redraw that cone in KiCad or a similar tool.</li>
  <li>Power the board and measure rails and regulators. Record what buttons, switches, or sensors do when the board is on.</li>
  <li>Identify a UART, SPI, or I²C link. Confirm it with a logic analyzer when one is on the bench.</li>
</ul>
<h2>What is graded</h2>
<p>Accuracy of the identification, quality of the reconstruction, and whether the reasoning connects a datasheet application circuit to the region of the board in front of the student. Safety notes in the lab specification cover powered measurement. Read them before the section.</p>
''')

    module_page(by_id["M5"], intro(
        "A power side channel reads information from the supply current. In CMOS, a current spike shows that the output switched. The trace does not show whether the output went high or low.",
        "<strong>Course:</strong> Digital logic.<br><strong>Teach this after:</strong> CMOS switching and truth tables. An earlier version was homework in embedded systems in Spring 2022.",
        '''<p>There is no slide deck and no file to download. After the CMOS lecture, students open the unknown circuit in the exercise below. Leave the labeled gates closed until they have an answer.</p>
<ul>
  <li><strong>Unknown circuit.</strong> Use this in class, after the CMOS lecture. Students step the inputs, record the voltage plot, and build the transition table. The link sits with the steps below.</li>
  <li><strong>Labeled gates.</strong> Leave these closed until students have committed to an answer. They are for the discussion afterward.</li>
</ul>''',
        [
            "Kocher, Jaffe, and Jun, “Differential Power Analysis,” Advances in Cryptology (CRYPTO), pp. 388–397, 1999.",
            "Mangard, Oswald, and Popp, <em>Power Analysis Attacks: Revealing the Secrets of Smart Cards</em>, Springer, 2007. The book-length treatment. This lab is one gate and one sense resistor.",
        ],
        [
            '<a href="https://www.youtube.com/watch?v=OlX-p4AGhWs">Introduction to Side-Channel Power Analysis</a> (Colin O’Flynn). What a supply-current measurement can reveal, and the equipment a research lab uses. This module needs only the browser simulator.',
            '<a href="https://www.youtube.com/watch?v=UhEOC3RRBhw">Lecture 48: Side Channel Attacks (Part II)</a> (NPTEL, IIT Kharagpur). A course lecture on side-channel attacks, for an instructor preparing the session.',
        ],
    ) + f'''
<h2>The exercise</h2>
<p>An unknown two-input gate is in a black box. The attacker can see inputs A and B and the supply pin. The output is hidden. A sense resistor between the supply and the source turns switching current into a voltage. A large spike means the output transitioned. A small bump does not. The trace does not encode the direction of the transition.</p>
<div class="outcome"><p class="outcome-title">Outcome</p><p>The transient shows that an output transition happened, not whether it was a rising or a falling edge. A gate and its complement produce the same transition table. The student names both truth tables and explains why the measurement cannot separate them. The module asks for no countermeasure. That ambiguity is the starting point for masking.</p></div>
<h2>The work</h2>
<ol class="steps">
  <li>Open the unknown circuit and step the inputs. Capture the voltage plot for the sequence 00, then 01, then 11, and mark the moments the inputs change.</li>
  <li>For each row of the transition table, stop the simulation, reset, apply the initial input, run about 20 ms, change to the new input, and run about 20 ms. Record whether a real transition occurred.</li>
  <li>From that table, give every truth table that would produce the same transitions, and show the work.</li>
</ol>
<p>The early form of this exercise was a graded homework in embedded systems in Spring 2022, before the module moved to the digital-logic setting the catalog now uses. No survey was collected for it.</p>
<p><a class="btn btn-primary" href="{unknown}">Open the unknown circuit in Falstad</a></p>
<details class="fold">
  <summary>Known gates, for the discussion after students have committed to an answer</summary>
  <p>These circuits are labeled. They are there so a class can compare a trace they already interpreted with a gate whose function is no longer hidden.</p>
  <ul>{gate_items}</ul>
</details>
''')

    module_page(by_id["M6"], intro(
        "Combinational logic locking inserts key gates into a ripple-carry adder. The sum is correct only for the right key. A wrong key inverts a carry, and the error propagates into the higher bits.",
        "<strong>Course:</strong> Digital logic.<br><strong>Teach this after:</strong> the ripple-carry adder, and after students can build a larger circuit from a smaller VHDL part. They should be able to simulate an adder before they add the lock. The lab is written and has not been graded yet.",
        '''<p>There is no slide deck. Give students the manual and the full-adder file after the adder lectures. Use the VHDL tool the course already teaches. The manual is written for Vivado.</p>
<ul>
  <li><strong>Lab manual.</strong> Objectives, figures, and the report checklist. A short in-class introduction can come from those figures, about 30 to 40 minutes, once the unlocked adder works.</li>
  <li><strong>FullAdder.vhdl.</strong> The only source students receive. They build the 4-bit adder from it, simulate, then add the lock.</li>
</ul>
<div class="downloads">
  <a class="download" href="../materials/m6/Combinational_Obfuscation_Lab_Manual.docx"><span><b>Lab manual</b><span>Objectives, figures, report checklist</span></span><i>DOCX</i></a>
  <a class="download" href="../materials/m6/FullAdder.vhdl"><span><b>Full-adder starter</b><span>The only source students receive</span></span><i>VHDL</i></a>
</div>''',
        [
            "Hoque, Chakraborty, and Bhunia, “Hardware Obfuscation and Logic Locking: A Tutorial Introduction,” <em>IEEE Design &amp; Test</em>, vol. 37, no. 3, pp. 59–77, 2020. This lab was adapted from that tutorial. The tutorial PDF is not redistributed here.",
            "Rajendran et al., “Fault Analysis-Based Logic Encryption,” <em>IEEE Transactions on Computers</em>, vol. 64, no. 2, pp. 410–424, 2015.",
        ],
        [
            '<a href="https://www.youtube.com/watch?v=ke7WHIyElkE">Module 2 — Logic Locking Fundamentals</a> (Ozgur Sinanoglu). A course lecture on what a key-controlled circuit is.',
            '<a href="https://www.youtube.com/watch?v=IcsxUS3o_Io">Lec 36: Introduction to Hardware Security</a> (NPTEL, IIT Guwahati). Includes logic locking in a first hardware-security lecture.',
        ],
    ) + '''
<h2>The exercise</h2>
<p>Students receive one file: a full-adder entity. They build a 4-bit ripple-carry adder out of four instances, simulate it, and only then insert a lock on the carries between stages. The adder is correct only for the key they designed. An incorrect key corrupts a carry, and the error ripples into the higher bits.</p>
<div class="outcome"><p class="outcome-title">Outcome</p><p>Under the right key the adder matches binary addition across the input space the testbench covers. Under a wrong key the two lock styles fail differently. XOR and XNOR invert one or more carries. A multiplexer substitutes some other signal into the carry chain. The student compares the styles and says how the key could be made longer.</p></div>
<h2>Part I. The adder, unlocked</h2>
<ol class="steps">
  <li>Read <code>FullAdder.vhdl</code>. Sum is the XOR of the two bits and carry-in. Carry-out is the majority of those three.</li>
  <li>Instantiate four full adders. Connect carry-out of one stage to carry-in of the next.</li>
  <li>Write a testbench, simulate, and confirm ordinary addition. In Vivado, set the radix of A, B, the sum, and carry-out to unsigned decimal before taking the screenshot.</li>
</ol>
<h2>Part II. Lock the carry chain</h2>
<p>Insert key-controlled logic between carry stages. Use either XOR and XNOR gates or multiplexers. Add a 3-bit key input. The design must add correctly for the key the student declares, and it must fail for other keys. The student chooses and documents that key. A reference convention used when this lab is discussed in the paper: a key bit of 0 passes a signal through an XOR and a key bit of 1 passes it through an XNOR.</p>
<h2>Part III. Correct key and wrong key</h2>
<p>Sweep the inputs under the correct key and under at least one incorrect key. Capture A, B, the sum, and carry-out only. The report holds the unlocked sources and schematic, the locked sources and schematic, the testbench, both waveforms, and the discussion questions in the manual. Those questions ask why a carry is a useful place to lock, how the two styles differ, and what would make the key space larger.</p>
<p>Software assumed by the manual is Vivado. Any VHDL simulator that can show a waveform will serve if the course already uses it. The instrument-reuse rule prefers the tool the course already teaches.</p>
''')

    module_page(by_id["M7"], intro(
        "A hardware Trojan is extra logic that stays dormant on almost every input and changes the function on a rare trigger. Students add a combinational trigger and a payload to a locked adder.",
        "<strong>Course:</strong> Digital logic.<br><strong>Teach this after:</strong> detecting one input value and writing a conditional assignment. If you also assign the locking lab, do this lab second. The starter file is already locked. The lab is written and has not been graded yet.",
        '''<p>There is no slide deck. The manual is the assignment. Students change only the marked region of the locked adder.</p>
<ul>
  <li><strong>Lab manual.</strong> The five parts of the report and the questions. Use it as the in-class handout.</li>
  <li><strong>FullAdder.vhdl.</strong> Provided so the design compiles. Students do not modify it.</li>
  <li><strong>4BitAdder_Key.vhdl.</strong> The locked adder. The trigger and the payload go where the file marks the spot. That region is empty in the starter.</li>
  <li><strong>tb_4BitAdder.vhdl.</strong> The testbench students simulate. The manual names the file <code>tb_4BitAdder_Key.vhdl</code>. The file in this bundle is <code>tb_4BitAdder.vhdl</code>.</li>
</ul>
<div class="downloads">
  <a class="download" href="../materials/m7/Hardware_Trojan_Insertion_Lab_Manual.docx"><span><b>Lab manual</b><span>Parts, questions, report checklist</span></span><i>DOCX</i></a>
  <a class="download" href="../materials/m7/FullAdder.vhdl"><span><b>Full adder</b><span>Do not modify</span></span><i>VHDL</i></a>
  <a class="download" href="../materials/m7/4BitAdder_Key.vhdl"><span><b>Locked adder</b><span>Insert the trigger and payload where marked</span></span><i>VHDL</i></a>
  <a class="download" href="../materials/m7/tb_4BitAdder.vhdl"><span><b>Testbench</b><span>Carry-in fixed, key fixed, operands swept</span></span><i>VHDL</i></a>
</div>''',
        [
            "Bhunia, Hsiao, Banga, and Narasimhan, “Hardware Trojan Attacks: Threat Analysis and Countermeasures,” <em>Proceedings of the IEEE</em>, vol. 102, no. 8, pp. 1229–1247, 2014.",
            "Xiao, Forte, Jin, Karri, Bhunia, and Tehranipoor, “Hardware Trojans: Lessons Learned After One Decade of Research,” <em>ACM Transactions on Design Automation of Electronic Systems</em>, vol. 22, no. 1, 2016.",
        ],
        [
            '<a href="https://www.youtube.com/watch?v=YVbvil6LjN0">Hardware Trojans</a> (NPTEL, IIT Madras, Information Security). A course lecture on triggers, payloads, and where a Trojan can sit.',
            '<a href="https://www.youtube.com/watch?v=WLHw8TdIqt4">Hardware Trojans vs. Logic Locking</a> (Dominik Šišejković, hardwear.io). How a Trojan and a lock interact. Useful if this lab follows the locking lab.',
        ],
    ) + '''
<h2>The exercise</h2>
<p>Students receive the adder already locked. They do not modify the full adder and they do not modify the locking equations. The work is a trigger and a payload. The trigger is combinational, looks only at the two operands, and asserts on a single combination the student chooses. The payload runs only while the trigger is asserted and changes at least one bit of the key before that key reaches the locking gates. For every other input the adder still behaves as the lock intends.</p>
<div class="outcome"><p class="outcome-title">Outcome</p><p>The sum is correct everywhere except the trigger combination, where the altered key corrupts the carry chain. The student explains why the Trojan is invisible on every other input, and how a one-bit change in the key becomes a fault that ripples into the higher bits.</p></div>
<h2>The five parts of the report</h2>
<ol class="steps">
  <li><strong>Read the lock.</strong> Explain the key port and both locking styles. The provided architecture uses XOR and XNOR on the masked carries. A multiplexer version is left in comments.</li>
  <li><strong>Design the trigger.</strong> Pick one pair of operand values. Implement it as combinational logic on a signal named <code>trigger</code>. Say why that pair is rare.</li>
  <li><strong>Design the payload.</strong> Build a modified key that differs from the real key only when <code>trigger</code> is 1, and only in at least one bit. Leave the obfuscation equations alone.</li>
  <li><strong>Simulate both cases.</strong> The supplied testbench holds carry-in at 0, drives the key port with <code>010</code>, and walks the operand space. Find the activation in the waveform. Show A, B, the sum, and carry-out in unsigned decimal.</li>
  <li><strong>Explain the hiding.</strong> Which key bit changed, how that change moves through the carry chain, and why every other input still looks like a correct, locked adder.</li>
</ol>
<p>The starter file marks the region where the trigger and payload belong and does not contain them. Completing that region is the lab.</p>
''')

    module_page(by_id["M8"], intro(
        "Sequential logic locking hides the correct behavior in the state machine. The key is applied one byte per clock. A wrong byte sends the UART transmitter into a locked state that it can leave only by reset.",
        "<strong>Course:</strong> Digital logic.<br><strong>Teach this after:</strong> finite-state machines and the UART frame. Students should already be able to simulate a state machine. This lab does not need the adder labs. It is written and has not been graded yet.",
        '''<p>There is no slide deck. The manual is the assignment. Students simulate the transmitter first, then add the lock.</p>
<ul>
  <li><strong>Lab manual.</strong> The frame figure, the report checklist, and the discussion questions. Use it as the in-class handout. It states the verification sequence the testbench has to cover.</li>
  <li><strong>UART.vhdl.</strong> A working transmitter. Idle, start bit, data bits, and stop bit are already there.</li>
  <li><strong>UART_tb.vhdl.</strong> The testbench starter. Students extend it for the correct sequence and a wrong value in each position.</li>
</ul>
<div class="downloads">
  <a class="download" href="../materials/m8/UART_Obfuscation_Lab_Manual.docx"><span><b>Lab manual</b><span>Frame figure, report checklist, discussion questions</span></span><i>DOCX</i></a>
  <a class="download" href="../materials/m8/UART.vhdl"><span><b>Transmitter starter</b><span>Unlocked FSM, task markers in comments</span></span><i>VHDL</i></a>
  <a class="download" href="../materials/m8/UART_tb.vhdl"><span><b>Testbench starter</b><span>Extend it for the four key cases</span></span><i>VHDL</i></a>
</div>''',
        [
            "Chakraborty and Bhunia, “HARPOON: An Obfuscation-Based SoC Design Methodology for Hardware Protection,” <em>IEEE Transactions on Computer-Aided Design</em>, vol. 28, no. 10, pp. 1493–1502, 2009. Sequential obfuscation by adding states. This lab is the UART-sized version of that idea.",
            "Hoque, Chakraborty, and Bhunia, “Hardware Obfuscation and Logic Locking: A Tutorial Introduction,” <em>IEEE Design &amp; Test</em>, vol. 37, no. 3, pp. 59–77, 2020. The tutorial this lab was adapted from. The PDF is not redistributed here.",
        ],
        [
            '<a href="https://www.youtube.com/watch?v=ke7WHIyElkE">Module 2 — Logic Locking Fundamentals</a> (Ozgur Sinanoglu). The combinational case, so the class can see what changes when the key moves into the state machine.',
            '<a href="https://www.youtube.com/watch?v=OtLrM2Y8ecQ">Lec 38: Attacks on RTL Logic Locking</a> (NPTEL, IIT Guwahati). What an attacker does with a locked RTL design. This lab has the student build the lock.',
        ],
    ) + '''
<h2>The exercise</h2>
<p>The starter is a working UART transmitter. Its state machine has idle, start bit, data bits, and stop bit. The line idles high, the start bit pulls it low, eight data bits leave least-significant bit first, and a stop bit returns the line high. There is no parity bit in this lab. Students simulate that machine first. They then add a lock in front of it.</p>
<div class="outcome"><p class="outcome-title">Outcome</p><p>The correct sequence walks three key states and enters idle, and the transmitter runs. Any wrong value enters a locked state that holds the transmit line high and has no exit except reset. The student explains why a key applied over several clocks is different from the single combinational key in the adder lab, and why the locked state has no outgoing transition except reset.</p></div>
<h2>Part I. The unlocked transmitter</h2>
<p>Identify the states, simulate with the provided testbench, and produce a timing diagram of <code>tx_start</code>, <code>tx</code>, <code>state_track</code>, and <code>data_in</code>. Be able to answer why idle is high, why start is low, the order of the data bits, and what makes the machine leave idle.</p>
<h2>Part II. The lock</h2>
<p>Add three key states, S0, S1, and S2, and a <code>LOCKED</code> state. Reset now lands in the first key state, not in idle. Three 8-bit key values must arrive one per clock while <code>key_valid</code> is high, and the comparison runs only then. The manual is explicit that without <code>key_valid</code> the machine would compare on every clock and could lock itself when nobody is entering a key. A wrong value at any position goes to <code>LOCKED</code> and stays there until reset. The original transmitter is reachable only after the sequence succeeds.</p>
<p>The verification sequence specified in the student manual is <code>AA</code>, then <code>BB</code>, then <code>CC</code>. The testbench has to cover that sequence and a wrong value in each of the three positions.</p>
<ul>
  <li>Correct sequence: S0, S1, S2, idle, and a normal frame follows.</li>
  <li>Wrong first key: S0, then locked.</li>
  <li>Wrong second key: S0, S1, then locked.</li>
  <li>Wrong third key: S0, S1, S2, then locked.</li>
</ul>
<p>Waveforms show <code>key_valid</code>, <code>key_seq</code>, <code>state_track</code>, <code>data_in</code>, and <code>tx_start</code>. The starter leaves commented task markers where the states, the key constants, the new ports, and the testbench changes belong. <code>BAUD_DIV</code> is 868 in the starter, which is the divider the supplied transmitter already uses.</p>
''')

    module_page(by_id["M9"], intro(
        "A cache side channel uses the cycle gap between a hit and a miss. On a shared last-level cache, that gap lets one process observe which lines another process touched.",
        "<strong>Course:</strong> Computer architecture. No course number is attached here.<br><strong>Teach this after:</strong> the cache lecture, including hierarchy, associativity, line size, and set indexing. Part 1 can be given in that same week. Part 2 waits until students can explain a hit and a miss. At KU this lecture was given in Fall 2024.",
        '''<p>Use the two slide decks as the class lectures. There is no homework file. Part 2 includes a measurement you can show in class. Students do not turn that measurement in.</p>
<ul>
  <li><strong>Lecture, part 1.</strong> Use with the cache unit, or immediately after it. Hierarchy, the parameters that define a cache, and the geometry of the student’s own machine.</li>
  <li><strong>Lecture, part 2.</strong> Use only after part 1. Flush and reload, prime and probe, and the recorded hit and miss times.</li>
</ul>
<div class="downloads">
  <a class="download" href="../materials/m9/cache_side-channel_Part1.pptx"><span><b>Lecture, part 1</b><span>Hierarchy, geometry of the local machine</span></span><i>PPTX</i></a>
  <a class="download" href="../materials/m9/cache_side-channel_Part2.pptx"><span><b>Lecture, part 2</b><span>Flush and reload, prime and probe, the measurement</span></span><i>PPTX</i></a>
</div>''',
        [
            '<a href="https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-yarom.pdf">FLUSH+RELOAD: A High Resolution, Low Noise, L3 Cache Side-Channel Attack</a>, Yarom and Falkner, USENIX Security Symposium, 2014. The attack the second lecture walks through.',
            "Yan, Fletcher, and Torrellas, “Cache Telepathy: Leveraging Shared Resource Attacks to Learn DNN Architectures,” USENIX Security Symposium, pp. 2003–2020, 2020. A later use of the same kind of shared-cache leak.",
            "Hill, Masters, Ranganathan, Turner, and Hennessy, “On the Spectre and Meltdown Processor Security Vulnerabilities,” <em>IEEE Micro</em>, vol. 39, no. 2, pp. 9–19, 2019.",
        ],
        [
            '<a href="https://www.youtube.com/watch?v=6JpLD3PUAZk">Why do CPUs Need Caches?</a> (Computerphile). A short refresher on the structure the host course has to teach before this module.',
            '<a href="https://www.youtube.com/watch?v=px7Fy6Ehj2s">FLUSH+RELOAD: A High Resolution, Low Noise, L3 Cache Side-Channel Attack</a> (USENIX Security ’14). The conference talk behind the second lecture.',
            '<a href="https://www.youtube.com/watch?v=I5mRwzVvFGE">Spectre and Meltdown</a> (Computerphile). Why a cache timing gap became a processor-security problem.',
        ],
    ) + '''
<h2>The lecture</h2>
<p>The course has already taught the cache as a performance structure: hierarchy, associativity, line size, and set indexing. This module uses the same structure as a side channel. A hit and a miss on a shared last-level line take different numbers of cycles, and that gap is wide enough to observe another process.</p>
<div class="outcome"><p class="outcome-title">Outcome</p><p>The lecture closes on a recorded probe-time series. Across 90 probes, hits fall between 96 and 104 cycles and misses fall between 144 and 168. A threshold at 110 sits in a gap of about 40 cycles. No graded assignment is stated in the materials, and no survey was given.</p></div>
<h2>Part 1. The cache as the course already draws it</h2>
<p>Hierarchy from registers to main memory, the parameters that define a cache, and the three associativity arrangements. Students read the sizes, associativity, and line size of their own machine from the operating system and from a topology tool.</p>
<h2>Part 2. The same structure as a channel</h2>
<p>Flush+Reload needs four things: memory shared with the victim, a cycle counter, an instruction that evicts one cache line, and a last-level cache shared across cores.</p>
<p>The lecture walks the sequence. Flush a shared line. Let the victim run. Reload the line and time the access. The flush is the cache-line flush instruction, with a fence on each side. The reload is timed between two reads of the timestamp counter.</p>
<p>When the attacker and the victim do not share memory, the lecture uses Prime+Probe instead. The attacker fills a cache set, lets the victim run, and times a later access to see whether the victim evicted a line.</p>
<p>Fall 2024 is the offering in which this lecture entered the computer architecture course. The two decks are listed above.</p>
''')
