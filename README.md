# Humanizer

A Claude Code skill and plugin that removes the tells of AI-generated writing from text you already have. Point it at an email, blog post, cover letter, memo, or doc that "sounds like ChatGPT" and it rewrites the text to sound like a person wrote it, while keeping the meaning and the intended voice.

Based on Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) guide maintained by WikiProject AI Cleanup.

## What it fixes

- AI vocabulary (leverage, foster, pivotal, vibrant, testament, delve, tapestry)
- Promotional and significance inflation
- Rule-of-three padding and parallel-clause filler
- Em-dash and semicolon overuse
- Hollow openers, sign-offs, and "It is important to note" throat-clearing
- Uniform sentence rhythm with no burstiness
- Generic claims with no specifics

It runs a final anti-AI pass on its own output before returning the rewrite.

## Install

### As a plugin (recommended)

```
/plugin marketplace add saurcodes/humanise-claude-skill
/plugin install humanizer@humanizer
```

### As a standalone skill

Copy `skills/humanizer/` into `~/.claude/skills/humanizer/` (user scope) or `.claude/skills/humanizer/` inside a project.

## Usage

The skill triggers automatically when you ask Claude to fix AI-sounding text. Examples:

- "I used ChatGPT to write this email and it sounds too corporate. Fix it."
- "Strip the AI out of this blog post."
- "This cover letter sounds robotic. Humanize it."

You can also invoke it directly with `/humanizer`.

## Repository layout

```
.claude-plugin/
  plugin.json          Plugin manifest
  marketplace.json     Marketplace manifest (lets you install via /plugin)
skills/
  humanizer/
    SKILL.md           The skill itself
evals/
  evals.json           Output quality evals (corporate memo, tech blog, voice matching)
  trigger-eval.json    Trigger accuracy evals (should / should not fire)
  grade.py             Assertion grader for eval outputs
  iteration-1/         Baseline vs. with-skill benchmark run
  iteration-2/         Old skill vs. revised skill benchmark run
```

## Evals

Run the grader against an iteration folder:

```
python3 evals/grade.py
```

Latest benchmark (iteration 2): 100% pass rate with the current skill across 3 evals × 3 runs.

## License

MIT
