# ~/.bashrc
#
# References:
#   [01] https://www.gnu.org/software/bash/manual/html_node/The-Shopt-Builtin.html
#   [02] https://sanctum.geek.nz/arabesque/better-bash-history/
#   [03] https://superuser.com/a/753948

# If not running interactively, don't do anything.
[[ $- != *i* ]] && return

# Define a function that appends a directory (or several) to $PATH iff it isn't
# already there. [03]
pathappend() {
  for ARG in "$@"
  do
    if [[ -d "$ARG" ]] && [[ ":$PATH:" != *":$ARG:"* ]]; then
        PATH="${PATH:+"$PATH:"}$ARG"
    fi
  done
}

export HISTSIZE=1000
export HISTFILESIZE=2000

# You can prevent commands that start with a space from going into history by
# setting $HISTCONTROL to ignorespace. You can also ignore duplicate commands,
# for example repeated du calls to watch a file grow, by adding ignoredups.
# There’s a shorthand to set both in ignoreboth. [02]
export HISTCONTROL=ignoreboth

# You might also want to remove the use of certain commands from your history,
# whether for privacy or readability reasons. This can be done with the
# $HISTIGNORE variable. It’s common to use this to exclude ls calls, job control
# builtins like bg and fg, and calls to history itself. [02]
export HISTIGNORE='ls:bg:fg:history'

# If set, minor errors in the spelling of a directory component in a cd command
# will be corrected. The errors checked for are transposed characters, a missing
# character, and a character too many. If a correction is found, the corrected
# path is printed, and the command proceeds. [01]
shopt -s cdspell

# If set, the history list is appended to the file named by the value of the
# HISTFILE variable when the shell exits, rather than overwriting the file. [01]
shopt -s histappend

# If set, Bash matches filenames in a case-insensitive fashion when performing
# filename expansion. [01]
shopt -s nocaseglob

# [Linux] If set, Bash attempts spelling correction on directory names during
# word completion if the directory name initially supplied does not exist. [01]
if [[ "${OSTYPE}" == "linux-gnu" ]]; then
  shopt -s dirspell
fi

bind 'set completion-ignore-case on'
export PS1="\[\e[01;32m\]\h\[\033[00m\]:\[\033[01;34m\]\w \$\[\033[00m\] "

# Set an environment variable for the base16 shell color. Doesn't matter if it
# isn't installed since this is just an environment variable.
export BASE16_SHELL="${HOME}/.config/base16-shell"

# Now if base16 shell is installed, then use it.
if [[ -e "${BASE16_SHELL}/profile_helper.sh" ]]; then
  eval "$(${BASE16_SHELL}/profile_helper.sh)"
fi

# Explicitly set umask since it isn't set on WSL.
umask 0022

# Add common personal bin directories to the $PATH.
pathappend "${HOME}/bin" "${HOME}/.local/bin"

# Add the miniconda directory to $PATH
pathappend "${HOME}/miniconda3/bin"

alias qq="exit"
alias clc="clear"

alias dk="docker"
alias dkc="docker-compose"
alias dki="docker images"
alias dkcd="docker-compose down"
alias dkcr="docker-compose restart"
alias dkcu="docker-compose up"

alias grep="grep --color=auto --line-number"

# The color flag is different depending on the OS.
if [[ "${OSTYPE}" == "darwin18" ]]; then
  colorflag="-G"
elif [[ "${OSTYPE}" == "linux-gnu" ]]; then
  colorflag="--color=auto"
fi
alias ls="ls ${colorflag} -F"
alias ll="ls ${colorflag} -Fl"
alias la="ls ${colorflag} -Fla"
alias lt="ls ${colorflag} -Flat"

# Alias to open a file from the terminal.
if [[ "${OSTYPE}" == "darwin18" ]]; then
  alias op="open"
elif [[ "${OSTYPE}" == "linux-gnu" ]]; then
  alias op=""xdg-open""
fi

alias tmls="tmux -2u ls"
alias tmns="tmux -2u new -s"
alias tmat="tmux -2u attach -d -t"

# Anaconda related.
alias sac="source activate"
alias csearch="conda search"
