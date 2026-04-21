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
You: How do I undo my last commit but keep the changes?
You: What's the difference between git merge and git rebase?
You: I accidentally committed to main, how do I move it to a new branch?
You: My merge has conflicts, walk me through fixing them
```
