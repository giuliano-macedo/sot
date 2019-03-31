[bits 16]
[org 0x7c00]

 main:
  mov si, msg
  call print_msg
  call print_endl

  xor ax,ax
  mov bx,1
  
  mov cx,1
  mov dx,[fibn]
  .l1: 
    cmp cx,dx
    jne .noarrow
    mov si,arrow
    call print_msg

    .noarrow:
      xchg cx,ax
      call print_int

      mov si,comma
      call print_msg

      xchg cx,ax
      call print_int

      call print_endl

      add ax,bx
      xchg ax,bx

      add cx,1
      cmp cx,14
      jne .l1

done:
  hlt
print_msg:
  push ax
.l1:
  lodsb     
  cmp al, 0 
  je .return
  mov ah, 0x0e 
  int 0x10  
  jmp .l1 
.return:
  pop ax
  ret
print_endl:
  mov si,endl
  call print_msg
  ret
print_int:
  push ax
  push bx
  push dx
  xor dx,dx
  mov bx,10
  div bx
  test ax,ax
  je .l1
  call print_int
.l1:
    mov ax,dx
    add al,'0'
    mov ah,0x0e
    int 0x10
    pop dx
    pop bx
    pop ax
    ret

arrow: db "numero escolhido  --> ",0
comma: db " , ",0
endl:db 10,13,0
fibn: dw 13
msg: db "Hello world",0

times 510-($-$$) db 0
dw 0xaa55