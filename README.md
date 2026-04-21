# askgit

An AI-powered Git tutor in your terminal. Ask questions, get unstuck, and build a real understanding of Git — all without leaving the command line.

## Installation

```bash
pip install askgit-tutor
```

## Setup

Add these two lines to your `~/.zshrc`:

```bash
export ASKGIT_SERVER_URL=https://web-production-46e20.up.railway.app
export ASKGIT_TOKEN=your-class-token
```

replace "your-class-token" with token provided

Then reload your shell:

```bash
source ~/.zshrc
```

## Usage

```bash
askgit
```

Type your Git question and press Enter. Type `exit` or `quit` to close.

## Examples

```
You: How do I start a new repository?
You: How do I create a new feature branch?
You: What does git status show me?
You: I made changes on main, how do I move them to a new branch?
You: What's the difference between git add and git commit?
```
