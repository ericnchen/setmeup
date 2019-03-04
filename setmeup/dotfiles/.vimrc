" ~/.vimrc
"
" References:
"   [01] http://vimdoc.sourceforge.net/htmldoc/options.html

" By default this option is on and the Vi defaults are used for the options.
" This default was chosen for those people who want to use Vim just like Vi,
" and don't even (want to) know about the 'compatible' option. [01]
set nocompatible

" Insert two spaces after a '.', '?' and '!' with a join command. [01]
set nojoinspaces

" Set 'tabstop' and 'shiftwidth' to whatever you prefer and use 'expandtab'.
" This way you will always insert spaces. The formatting will never be messed
" up when 'tabstop' is changed. [01]
set tabstop=4
set shiftwidth=4
set expandtab

" Highlight the screen line of the cursor with CursorLine. [01]
set cursorline

" Make a backup before overwriting a file. Leave it around after the file has
" been successfully written. If you do not want to keep the backup file, but
" you do want a backup while the file is being written, reset this option and
" set the 'writebackup' option (this is the default). [01]
set nobackup
set writebackup

" Allow backspacing over autoindent, line breaks, and start of inserts. [01]
set backspace=indent,eol,start

" Enable the use of the mouse. [01]
set mouse=a

" When this option is set, the screen will not be redrawn while executing
" macros, registers and other commands that have not been typed. [01]
set lazyredraw

" Change the default horizontal and vertical spitting behavior. [01]
set splitbelow
set splitright

" Do (smart) autoindenting when starting a new line. [01]
set autoindent
set smartindent

" When on, a <Tab> in front of a line inserts blanks according to 'shiftwidth',
" 'tabstop' or 'softtabstop' is used in other places. [01]
set smarttab

" Disable swapfile creation. [01]
set noswapfile

" Default file properties.
set fileformats=unix,mac,dos
set encoding=utf-8

set number
set spelllang=en_us

" Enable the syntax highlighting.
syntax on
