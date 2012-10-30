#!/bin/bash

export PATH=$PATH:/opt/local/bin

# I like confirming destructive operations.
alias cp="cp -iv"
alias mv="mv -iv"
alias rm="rm -iv"

# Colored output from ls is nice, but the default color choices need
# work for use on a dark/partially transparent background. Directories
# stay blue but get bold, and symbolic links get bold cyan instead of
# magenta.
export CLICOLOR=1
export LSCOLORS="ExGxcxdxbxegedabagacad"

# Color aliases
alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# Define some colors to use in the prompt
NO_COLOR="\[\033[0m\]"
LIGHT_WHITE="\[\033[1;37m\]"
WHITE="\[\033[0;37m\]"
GRAY="\[\033[1;30m\]"
BLACK="\[\033[0;30m\]"

RED="\[\033[0;31m\]"
LIGHT_RED="\[\033[1;31m\]"
GREEN="\[\033[0;32m\]"
LIGHT_GREEN="\[\033[1;32m\]"
YELLOW="\[\033[0;33m\]"
LIGHT_YELLOW="\[\033[1;33m\]"
BLUE="\[\033[0;34m\]"
LIGHT_BLUE="\[\033[1;34m\]"
MAGENTA="\[\033[0;35m\]"
LIGHT_MAGENTA="\[\033[1;35m\]"
CYAN="\[\033[0;36m\]"
LIGHT_CYAN="\[\033[1;36m\]"

# Change the prompt character dpeending on if we're in a repository
function prompt_char {
    git branch >/dev/null 2>/dev/null && echo '±' && return
    hg root >/dev/null 2>/dev/null && echo '☿' && return
    echo '$'
}

## display the current git branch
__git_ps1() {
	local b="$(git symbolic-ref HEAD 2>/dev/null)"
	if [ -n "$b" ]; then
        printf " (git:%s)" "${b##refs/heads/}"
	fi
}

## display the current mercurial branch
__hg_ps1() {
    local branch="$(hg branch 2> /dev/null)"
    if [ -n "$branch" ]; then
        printf " (hg:%s)" "${branch}"
    fi
}

## display the current subversion revision
__svn_ps1() {
    if [[ -d ".svn" ]]; then
        printf " (svn:%s)" `svnversion`
    fi
}

## My super cool prompt
export MY_PROMPT="\[\e]0;\u@\h: \w\a\]"
export MY_PROMPT="$MY_PROMPT${WHITE}[\t] ${LIGHT_GREEN}\u ${LIGHT_WHITE}@ ${LIGHT_RED}\h ${LIGHT_WHITE}in ${LIGHT_CYAN}\w${WHITE}\$(__git_ps1)\$(__hg_ps1)\$(__svn_ps1)\n${LIGHT_WHITE}\$(prompt_char)${NO_COLOR} "

## Basic prompt for everyone else
export BASIC_PROMPT="${WHITE}[\t] ${LIGHT_GREEN}\u@\h${LIGHT_WHITE}:${LIGHT_BLUE}\w${WHITE}\$${NO_COLOR} "

export PS1=$MY_PROMPT

alias basic_prompt="export PS1=\$BASIC_PROMPT"
alias my_prompt="export PS1=\$MY_PROMPT"
alias rmpyc='find . -name "*.pyc" -exec rm {} \;'
alias go_away='sudo poweroff'
#alias chat="/usr/bin/sakura -x \"ssh -t derek@serverbox.dmpayton.com 'screen -dr chat'\""
alias chat="ssh -t derek@serverbox.dmpayton.com 'screen -dr chat'"

# Hooray Nano! *ducks*
export EDITOR=nano

# Env variables and functions for virtualenvwrapper.
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/dev
#. $HOME/bin/virtualenvwrapper.sh
. /usr/local/bin/virtualenvwrapper.sh

# Ruby gems
#export PATH=$PATH:$HOME/bin/:/var/lib/gems/1.8/bin/

# Some useful additional completion.
#. $HOME/bin/django_bash_completion
#. $HOME/bin/hg_completion

### Added by the Heroku Toolbelt
export PATH="/usr/local/heroku/bin:$PATH"
