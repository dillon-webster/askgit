# askgit

An AI-powered Git tutor in your terminal. Ask questions, get unstuck, and build a real understanding of Git — all without leaving the command line.

## Installation

```bash
pip install askgit
```

Or install from source:

```bash
git clone https://github.com/yourname/askgit
cd askgit
pip install -e .
```

## Setup

Add your Anthropic API key to `~/.zshrc` (or `~/.bashrc`):

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

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
