# Genesis Assembly Constants and Definitions

**Source**: Community Genesis assembly reference (GENESIS.EQU)  
**Purpose**: Essential constants for RKA decompilation and analysis  
**Usage**: Assembly code analysis, hardware register mapping, VDP programming

---

## VDP Hardware Registers

### VDP Port Addresses
```assembly
VDPData     EQU $C00000    ; Data port (read/write)
VDPCtrl     EQU $C00004    ; Control port (read/write)
VDPCounter  EQU $C00008    ; HV counter (read only)
PSGPort     EQU $C00011    ; PSG sound port (write only)
```

### VDP Register Definitions
```assembly
; VDP register set format: $8nxx where n=register, xx=value
REG00       EQU $8000      ; Mode Set Register 1
REG01       EQU $8100      ; Mode Set Register 2
REG02       EQU $8200      ; Plane A Name Table Address
REG03       EQU $8300      ; Window Name Table Address
REG04       EQU $8400      ; Plane B Name Table Address
REG05       EQU $8500      ; Sprite Attribute Table Address
REG07       EQU $8700      ; Background Color
REG10       EQU $8A00      ; H Interrupt Counter
REG11       EQU $8B00      ; Mode Set Register 3
REG12       EQU $8C00      ; Mode Set Register 4
REG13       EQU $8D00      ; H Scroll Data Table Address
REG15       EQU $8F00      ; Auto Increment Data
REG16       EQU $9000      ; Scroll Size
REG17       EQU $9100      ; Window H Position
REG18       EQU $9200      ; Window V Position
REG19       EQU $9300      ; DMA Length Lo
REG20       EQU $9400      ; DMA Length Hi
REG21       EQU $9500      ; DMA Source Lo
REG22       EQU $9600      ; DMA Source Mid
REG23       EQU $9700      ; DMA Source Hi
```

### I/O Registers
```assembly
VersionNo   EQU $A10001    ; Version register
Data1       EQU $A10003    ; Controller 1 data
Data2       EQU $A10005    ; Controller 2 data
Ctrl1       EQU $A10009    ; Controller 1 control
Ctrl2       EQU $A1000B    ; Controller 2 control
Z80Ram      EQU $A00000    ; Z80 RAM base (8KB)
Z80BusReq   EQU $A11100    ; Z80 bus request
Z80Reset    EQU $A11200    ; Z80 reset
```

**Credit**: Original GENESIS.EQU from Genesis development community
