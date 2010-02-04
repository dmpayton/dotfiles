#!/bin/bash

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

# Hooray Nano!
export EDITOR=nano

# Prompt is not as complicated as the format string would
# suggest. This one does:
#
# (time) user@host:dir $
#
# with user/host in green and working directory blue.
# The first one sets the terminal title, the second is the prompt.
export PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]"
export PS1="$PS1(\[\e[0;37m\]\A\[\e[0;37m\]) \[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\] \$ "

# Env variables and functions for virtualenvwrapper.
export WORKON_HOME=$HOME/dev/virtualenvs
#. $HOME/bin/virtualenvwrapper_bashrc

# Some useful additional completion.
#. $HOME/dev/django/svn/django/trunk/extras/django_bash_completion
#. $HOME/bin/hg_completion
