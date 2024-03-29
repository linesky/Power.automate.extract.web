printf "\x1bc\x1b[44;37masm file name ? "
read g
nasm $g -o /tmp/my.o
objdump -M intel -D -b binary -mi386  -Maddr16,data16 /tmp/my.o
