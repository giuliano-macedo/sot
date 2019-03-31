.PHONY:boot.bin
boot.bin:boot.asm
	nasm boot.asm -o boot.bin
	dd if=boot.bin of=baseboot.bin bs=1 count=140 status=none
clean:
	rm -f boot.bin baseboot.bin