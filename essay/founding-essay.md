# The Day I Watched a Video and Accidentally Started an Infrastructure Project

*By Yusuf Razak — February 26, 2026*

---

Last year I watched a Veritasium video called "The Internet Was Weeks Away From Disaster and No One Knew."

It was a Tuesday evening. I was supposed to be working on something else. But the thumbnail caught me — a Jenga tower with one block about to fall, and text saying the internet almost broke. I clicked.

It's about a compression library called XZ Utils. You've never heard of it. Neither had I. It runs on hundreds of millions of Linux machines. Every time you SSH into a server, every time you update a package, somewhere in that process XZ Utils is probably running. It was maintained by one person — Lasse Collin — who had been doing it for years, largely alone, largely unpaid, and who was burning out.

In 2021, a new contributor appeared. Friendly. Helpful. Patient. They spent two years building trust. Sending good patches. Being kind to Lasse when he was struggling. Slowly they became a co-maintainer. Then in early 2024 they planted a backdoor. Not in a minor utility. In the compression library that ships with OpenSSH — the tool that manages remote access to most of the servers on the internet.

If it had shipped to production systems, someone — probably a nation state — would have had a skeleton key to most of the Linux infrastructure on the planet. Not just a few servers. Most of them. The video has a graphic showing a Jenga tower with one block removed. That's exactly what it felt like watching it. One invisible block holding up everything else.

A Microsoft engineer named Andres Freund noticed something 500 milliseconds slower than expected. He was doing routine benchmarking. He pulled the thread. The backdoor unravelled. We got lucky.

I paused the video and sat there for a while. The Jenga tower image wouldn't leave my head. I had one thought that kept repeating: This is the problem. But it's not the only version of it. The XZ attack was deliberate. What's coming next isn't deliberate. It's just abundance.

The XZ attack was spectacular. State-sponsored, years in the making, nearly catastrophic. But it was also one attack. One bad actor. Three years of patience and social engineering. The thing that keeps me up at night is different. It has no villain. It doesn't need one.

AI made code free. Not cheaper — free. The marginal cost of generating a plausible pull request is now approximately zero. Anybody can do it. Any AI assistant. Any script. Any developer who doesn't understand your codebase but has a suggestion anyway. Any automated system feeding into another automated system. The floodgates aren't just open. They've been removed entirely.

Here's the asymmetry that breaks everything. The marginal cost of reviewing that pull request is the same as it always was. A human. Their attention. Their expertise. Their time. Their capacity to hold a mental model of the codebase while checking for edge cases and unintended consequences and subtle bugs. That hasn't changed. It won't change. It's bounded by the same biological and cognitive limits it always was.

That gap — free to produce, expensive to verify — is not a bug in anyone's design. Nobody planned it. It emerged from the collision of two forces: AI capability and open source culture. And it is crushing the people who hold the Jenga tower up.

The numbers tell part of the story. Pull request volumes are up 40% year over year across major platforms. But here's what the growth charts don't show: the quality distribution has shifted. Industry estimates suggest about 5% of AI-generated PRs meet project standards. That means maintainers are drowning in volume while the signal-to-noise ratio collapses. Every additional PR makes it harder to find the ones worth reading.

Daniel Stenberg built curl. It runs on your phone right now. Probably in a dozen places you don't even know about. In 2025 he had to pause the curl bug bounty program because AI-generated vulnerability reports — confident, detailed, completely fabricated, describing vulnerabilities that don't exist — were eating hundreds of hours of expert time. His team was chasing ghosts while real security work waited. He explained it in a blog post that was quiet and devastating. They had to stop rewarding security researchers because the false positive rate from AI tools had made the program unsustainable.

Mitchell Hashimoto closed his terminal emulator Ghostty to all outside contributors unless personally vouched for by someone inside. Not because he doesn't believe in open source. Because he couldn't verify the flood. He implemented a system where you can only contribute if someone already trusted says you're real. The open door closed.

tldraw, the open source drawing tool, now auto-closes all external pull requests by default. Steve Ruiz, the creator, explained that they were being overwhelmed by low-quality AI submissions. They still welcome contributions. But only after a human has verified the contributor is real and the code is worth looking at. The default changed from trust to distrust.

These aren't antisocial developers rejecting community. These are smart, experienced people making rational decisions in the face of an irrational flood. They're protecting their sanity and their projects the only way they know how. By closing doors that used to be open.

Most people who see this problem conclude we need better security review. More scrutiny. Faster automated response. Better filters. AI detection tools. That's not wrong. It's just not the root cause.

I concluded something different.

The reason Jia Tan succeeded was not a failure of tooling. It was a failure of vocabulary.

Think about it. Lasse Collin accepted this person's contributions because they seemed trustworthy. But "seeming trustworthy" has no standard definition. There was no format for what a trustworthy contribution looks like. No shared language for declaring "this is who I am and this is what I built." No way to verify claims independently. Lasse Collin had to use his gut. His gut was manipulated by three years of careful social engineering.

Now imagine that problem at a million times the scale. Not one sophisticated attacker spending years building fake trust. Millions of contributions — from humans, from AI, from AI-assisted humans, from scripts, from good-faith developers who don't understand the codebase, from automated systems generating PRs to train other automated systems — all arriving with the same empty information envelope.

No declaration. No provenance. No signal about how the code was made or how carefully it was reviewed. Just code, and a hope that someone will read it carefully enough to catch whatever matters.

AI made code free. Trust is still expensive. That gap is what's breaking open source.

This is not the first time technology needed a trust vocabulary at a scaling inflection point.

The web had a trust crisis in the 1990s. You couldn't know if a website was who it claimed to be. Early web users had to manually check certificates or just trust that a site was legitimate. It was a mess. The solution wasn't to check every website manually or build a centralised registry of legitimate sites. It was SSL/TLS — a shared cryptographic infrastructure that any website could implement and any browser could verify. Nobody owns it. Everyone uses it. Its presence is so assumed that its absence is what's alarming. When you see "Not Secure" in your browser, you notice. The absence of the trust layer signals danger.

Creative Commons solved a different version of the same problem. Not by enforcing licensing through legal teams — by creating a vocabulary so clear that using it became easier than not using it. Four icons. Six licenses. A shared language that creators and users both understood. Before Creative Commons, licensing was complicated, expensive, and ambiguous. After, it was a decision you could make in five minutes that would be understood anywhere in the world.

In both cases the pattern was the same. A trust gap at a scaling inflection point. Someone built the vocabulary, gave it away, and it became the assumed layer underneath everything. The thing everyone uses without thinking about because not using it became stranger than using it.

Open source is at that inflection point now. The scaling force is AI. The trust gap is contribution provenance. The vocabulary doesn't exist yet.

I am not the person you'd expect to build this.

I am not a long-time open source contributor with decades of experience maintaining critical infrastructure. I am not someone from Silicon Valley who has watched this problem evolve over years. I am Yusuf Razak, a developer from Nairobi who watched a YouTube video on a weeknight and couldn't stop thinking about it.

I talked through the idea with Claude. I explained what I was seeing and what I thought might solve it. Then I built it with Claude and another AI called Kimi. The entire first version — the specification, the reference implementation, the documentation — was built with AI assistance. I'm telling you this not because I have to, but because the entire point of what I built is that this kind of honesty should be the default. If we're going to solve the trust problem, we have to start by being trustworthy.

What I built is called OCTP — the Open Contribution Trust Protocol.

Here's the simple version. When you finish a contribution and are about to submit a pull request, you run one command: octp sign.

The tool asks you three things. How was this created — human only, AI-assisted, or AI-generated? How carefully was it reviewed — did you glance at it, read it carefully, substantially modify it, or completely rewrite it? What checks has it passed?

You answer honestly. The tool runs your test suite. It checks for security vulnerabilities. It scans for secrets accidentally left in the code. It hashes everything together into a fingerprint. Your private key signs the result. A small JSON file — a trust envelope — travels with your contribution.

The maintainer's tooling reads it. In three seconds they know: this was AI-assisted, substantially reviewed by a human, all checks passed, contributor has 47 prior accepted contributions, self-assessed high confidence, uncertain about thread safety in lines 47-52 so please look there carefully.

Not a verdict. Not a gate. Not an algorithm deciding what gets merged. Just information. The missing information that maintainers have been making decisions without for the last two years. The signal in the noise.

The first OCTP envelope ever generated was created in Nairobi on February 26, 2026. It declares AI assistance. It lists the tools I used — Claude and Kimi. It says substantial human review because I went through every line carefully. My cryptographic signature is on it. If I lied, that signature is evidence of the lie.

That's the point. Not perfection. Accountability. A shared vocabulary for trust that contributor and maintainer can both speak without needing to know each other personally, without needing shared history or institutional context.

Before you get excited — let me be clear about what this is not.

It is not a detection system. You cannot reliably detect AI-generated code and you should stop trying. As models improve, detection becomes harder. You're always one generation behind. And it misses the point anyway. The problem isn't that code is AI-generated. The problem is that we have no way to know what a contribution actually is. OCTP doesn't try to detect anything. It asks contributors to declare.

It is not a gatekeeper. No algorithm decides what gets merged. No score determines what's good or bad. No automated system rejects contributions based on where they fall on some spectrum. That's the maintainer's job. That's always going to be the maintainer's job. OCTP gives them better information to do that job well. It doesn't do the job for them.

It is not centralised. No company owns the standard. No platform controls the infrastructure. No single entity can change the rules or charge for access. The spec lives on GitHub under an open governance model. The tool is MIT licensed. The community governs both through an RFC process. It belongs to everyone who uses it.

It is a vocabulary. A shared language for trust that contributor and maintainer can both speak. The kind of thing that once it exists, everyone wonders how they managed without it.

So what is it for? Here's who I wrote this essay for.

If you're a maintainer drowning in AI-generated pull requests you don't have time to review — this is for you. If you've closed your project to outside contributors not because you want to but because you couldn't handle the volume anymore — this is for you. If you want to reopen that door but need a way to triage effectively — this is for you.

If you're a developer who wants your quality to be legible to the people you're submitting to — this is for you. If you spent three days on a contribution and want maintainers to know that, to see the care you put in, without having to write a novel in the PR description — this is for you.

If you work at OpenSSF or the Linux Foundation and you're trying to solve this at the infrastructure level — this is for you. If you're thinking about software supply chain security and you need a lightweight provenance layer that fits into existing workflows — this is for you.

If you're a builder who wants to implement this standard in Go or Rust or JavaScript — this is for you. The spec is designed to be implementable. The JSON Schema is clear. The cryptographic requirements are standard. You can build this in a weekend.

The spec is live at github.com/openoctp/spec. The reference tool installs with pip install octp-python. It's tested. It works. The first envelope was generated in Nairobi. The project uses its own standard on every commit — every single one declares AI assistance and lists the tools used.

This is v0.1. It is deliberately incomplete. There are open questions I don't know how to answer yet. The key management model needs work — right now it's just local files, and losing your key means losing your ability to sign, and there's no revocation story yet. The reputation layer doesn't exist — there's no formal way to aggregate trust scores across contributions over time. The institutional adoption path is unclear — I don't know how you get from "some guy in Nairobi built a thing" to "this is infrastructure the Linux Foundation co-owns."

I need maintainers who will try this on their real projects and tell me where it breaks. I need developers who will implement it in Go and Rust and JavaScript so it's not just a Python thing. I need critics who will tell me what I got wrong — what's missing, what's unclear, what won't work. I need people from OpenSSF and the Linux Foundation who know how standards actually get adopted to tell me what I'm missing, what I need to do differently, who I need to talk to.

I am Yusuf Razak, a developer from Nairobi. I watched a video about a compression library and couldn't stop thinking about what it meant. I built a thing about it.

The Jenga tower is still wobbling. Not from one deliberate attack by a sophisticated adversary. From a million well-meaning floods. From abundance without structure. From code without context.

Come help me figure out if this is the right piece to stabilise it.

—

*Yusuf Razak is a developer in Nairobi building honest infrastructure for the AI era. OCTP v0.1 is live at octp.dev.*

*The spec: github.com/openoctp/spec*  
*The tool: pip install octp-python*  
*Discussions: github.com/openoctp/community*