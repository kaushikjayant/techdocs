# The Technical Writer as Platform Architect: Building Automation That Ships

**Published:** June 2026 | **Category:** Career, Documentation Engineering, Automation

---

The job title says "Technical Writer," but the work is platform architecture. Over
the past two years, I've designed and shipped an automation platform that generates
SoC Reference Manuals from RTL source code, memory map spreadsheets, and AI-assisted
content extraction. The platform serves 40 authors across five product lines, handles
tens of thousands of register descriptions per chip, and eliminated an entire class
of post-release errata that had plagued previous tape-outs.

This isn't a career path that the "technical writer" label prepares you for. Here's
what I learned about bridging the gap between documentation and platform engineering.

## The Moment I Stopped Being Just a Writer

The turning point came during a tape-out crunch. Our team had spent three weeks
manually assembling a SoC Reference Manual — extracting parameter values from
spreadsheets, typing register addresses into XML files, hand-crafting DITA map
references for 80+ IP blocks. Two days before the documentation freeze, the
architecture team updated the memory map. Six base addresses changed. Every one
of those changes had to be manually propagated through the documentation.

I realized I wasn't solving a writing problem. I was solving an automation problem
that happened to produce documentation as its output.

The next morning, instead of fixing those six addresses, I started writing a Python
script that could read the architecture team's memory map spreadsheet and generate
the XML files automatically. That script became the prototype for what is now a
seven-stage automated pipeline.

## Skills That Transfer

Technical writing at the semiconductor level — the kind where you're documenting
register maps, memory hierarchies, and parameter configurations — already requires
many of the skills that platform engineering demands:

**Systems thinking.** You can't document a SoC without understanding how its
components interact. Register documentation isn't a list of independent descriptions;
it's a representation of a hardware state machine. Memory maps aren't tables of
addresses; they're reflections of a physical bus architecture. This systems-level
understanding translates directly to designing automation that respects hardware
constraints.

**Data modeling.** Every documentation format is a data model. DITA maps represent
hierarchical relationships. Register databases represent structured hardware
descriptions. Parameter definition files represent typed configuration with
constraints. Designing these formats requires the same thinking as designing a
database schema or an API contract — what are the entities, what are the
relationships, what are the validation rules, how does data flow between layers.

**Process automation.** Technical writers spend a lot of time thinking about
repetition. When you document the same type of content (a register, a parameter,
an IP instance) a hundred times over, you naturally start thinking about templates,
macros, and automation. The jump from "I'll write a FrameMaker template" to
"I'll write a Python script that generates the entire chapter from a JSON file"
is incremental in concept but transformative in outcome.

**Toolchain integration.** Semiconductor documentation relies on complex toolchains:
DITA-OT, XSLT transforms, PDF renderers, XML editors, version control systems.
Understanding how these tools connect — where the handoffs happen, what formats
are exchanged, how errors propagate — is exactly the skill needed to design
automation pipelines.

## What I Had to Learn

Some skills didn't transfer and had to be learned from scratch:

**RTL fundamentals.** I didn't need to become a hardware designer, but I needed
to understand enough SystemVerilog to trace parameter declarations, recognize
generate blocks, and understand hierarchy. I spent evenings working through
Verilog tutorials and asking design engineers to walk me through their module
hierarchies.

**API integration.** Connecting VS Code's extension API to a local Python backend
over JSON-RPC, integrating Claude's API for content generation, building Flask
endpoints for the documentation explorer — none of this was in the technical
writing toolkit. I learned it by building it, one integration at a time.

**CI/CD pipeline design.** The automation platform runs in CI, triggered by RTL
commits. Designing the pipeline — what triggers a build, what constitutes a
failure, how artifacts flow between stages, how results are reported — required
understanding GitLab CI configuration, artifact management, and build notification
patterns.

**The most difficult skill: earning cross-functional trust.** When a technical
writer shows up at an architecture meeting with a proposal for an automated
documentation pipeline, the initial reaction is scepticism. Overcoming that
required demonstrating technical competence — not just talking about automation
but showing working prototypes that produced correct documentation faster than
the manual process.

## The Career Argument

The title "Technical Writer" under-sells what many of us actually do. At the
senior level in semiconductor documentation, you're doing systems design, data
modeling, process automation, toolchain integration, and cross-functional
coordination. You're making architectural decisions that affect how tens of
thousands of pages of documentation are produced across multiple product lines.

The industry needs a better way to recognize this. "Documentation Engineer" or
"Documentation Platform Architect" more accurately describes the work of designing
and building the systems that produce documentation, as distinct from the work
of authoring individual documents.

For technical writers who want to move in this direction: start automating
something repetitive. Find the task that you do the most often — generating a
register table, assembling a DITA map, extracting values from a spreadsheet —
and write a script that does it for you. The first script will be rough. The
tenth script will be production-quality. By the twentieth, you'll have become
the person who designs the systems that other writers use, and your job title
won't matter anymore.

---

*This article reflects personal experience in documentation engineering.
All technical details have been generalized.*