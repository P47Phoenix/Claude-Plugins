# Firmware Interface Documentation Template

This reference defines the firmware interface document structure, content requirements, and best practices for producing documentation that bridges hardware design to firmware development.

## Purpose

The firmware interface document is the primary handoff artifact from the Electrical Engineer to the firmware/software team. It answers: "Given this schematic, what does the firmware engineer need to know to write drivers and bring up the board?"

## Document Sections

### 1. Pin Assignment Table

Capture EVERY MCU/SoC pin and its assigned function. This is the single source of truth for pin-to-function mapping.

**Required columns:**
| Column | Description |
|--------|-------------|
| MCU Pin | Pin number or name as it appears on the MCU datasheet (e.g., PA0, GPIO_12, P1.3) |
| Function | What the pin is used for (e.g., SPI1_SCK, I2C2_SDA, LED_STATUS, BUTTON_1) |
| Direction | IN, OUT, BIDIR, ANALOG, POWER, NC (no connect) |
| Voltage | Logic level voltage (e.g., 3.3V, 1.8V) |
| Net Name | Schematic net name for cross-referencing |
| Alternate Functions | Other available peripheral functions on this pin (helps firmware team understand constraints) |
| Notes | Pull-up/down configuration, drive strength requirements, interrupt capability needed |

**Best practices:**
- Group pins by function (power, digital I/O, analog, communication buses, debug)
- Mark reserved/unused pins with their default configuration (input with pull-down recommended)
- Flag any pins where alternate function conflicts exist (e.g., SPI and I2C share pins)

### 2. Power Domain Map

Document which power rail powers which subsystem and the sequencing dependencies.

**Required columns:**
| Column | Description |
|--------|-------------|
| Domain | Logical name (e.g., CORE, IO, ANALOG, PERIPHERAL) |
| Rail | Net name on schematic (e.g., VCC_3V3, VDD_CORE_1V2) |
| Voltage | Nominal voltage |
| Source | Regulator part number and reference designator |
| Max Current | Maximum current rating of the source |
| Sequencing | Power-on order (e.g., "Must be stable before IO domain") |
| Subsystems | What this rail powers |

**Why firmware needs this:**
- Firmware controls power sequencing via enable pins in some designs
- Power-aware firmware needs to know which peripherals lose power in sleep modes
- Debugging power issues requires understanding which rail feeds which component

### 3. Communication Bus Interfaces

For each communication bus, document everything the firmware engineer needs to configure the peripheral.

#### I2C

| Field | What to Document |
|-------|-----------------|
| Bus instance | Which MCU I2C peripheral (e.g., I2C1, I2C2) |
| SCL/SDA pins | Pin assignments |
| Clock rate | Standard (100kHz), Fast (400kHz), Fast-mode Plus (1MHz) |
| Pull-up value | Resistance and Vcc rail for pull-ups |
| Device address map | Every device on the bus with 7-bit address, description, and datasheet link |
| Address conflicts | Flag any shared addresses (some devices have configurable address pins) |

#### SPI

| Field | What to Document |
|-------|-----------------|
| Bus instance | Which MCU SPI peripheral |
| SCK/MOSI/MISO pins | Pin assignments |
| Clock rate | Maximum SPI clock for the bus (limited by slowest device) |
| Mode (CPOL/CPHA) | SPI mode for each device (modes 0-3) |
| Chip select map | CS pin for each device, active polarity, and description |
| Shared bus concerns | Devices that cannot share the bus (tri-state behavior, clock conflicts) |

#### UART

| Field | What to Document |
|-------|-----------------|
| Interface instance | Which MCU UART peripheral |
| TX/RX pins | Pin assignments |
| Baud rate | Default baud rate |
| Flow control | None, hardware (RTS/CTS pins), software (XON/XOFF) |
| Voltage level | Logic level (important for external connections) |
| Purpose | Debug console, GPS module, Bluetooth module, etc. |

#### Other Interfaces

Document any other communication interfaces (CAN, USB, Ethernet, custom protocols) with equivalent detail.

### 4. Debug Interface Access Points

Document all hardware debug access points so the firmware engineer can connect tools.

**Required information:**
| Field | Description |
|-------|-------------|
| Interface type | SWD, JTAG, UART console, custom |
| Pins | Pin names and assignments |
| Connector | Physical connector reference designator and type |
| Protocol | ARM SWD, JTAG, UART (baud rate + format) |
| Access notes | Header population (populated/unpopulated), test point locations |

**Best practices:**
- Always provide a UART console for text-based debug output
- Document the default debug baud rate and format (e.g., 115200 8N1)
- Note if the debug connector is populated by default or requires hand-soldering headers

### 5. Test Points

Map test points to their net, expected value, and purpose. This helps firmware engineers measure signals during board bring-up.

**Required columns:**
| Column | Description |
|--------|-------------|
| Test Point | Reference designator (e.g., TP1) |
| Net | Schematic net name |
| Expected Value | Voltage, frequency, or signal description |
| Purpose | What the firmware engineer should measure here and when |

## Cross-Referencing

The firmware interface document should cross-reference:
- **Schematic sheets** -- Each pin assignment should reference the schematic sheet where it appears
- **Component datasheets** -- Each device on a communication bus should link to its datasheet
- **Power analysis** -- Power domain map should be consistent with the power analysis artifact

## Common Gaps to Avoid

1. **Missing interrupt pins** -- Document which pins need interrupt capability and the trigger edge (rising, falling, both)
2. **Missing boot configuration** -- Document boot mode pins and their configuration (e.g., STM32 BOOT0 pin)
3. **Missing clock sources** -- Document external oscillator frequencies, load capacitance, and which MCU clock input they connect to
4. **Missing DMA channels** -- If specific DMA channels are allocated by hardware constraints, document them
5. **Missing power mode implications** -- Document which peripherals are available in each low-power mode
6. **Missing GPIO default states** -- Document the required default state of each GPIO during boot (before firmware configures them), especially for safety-critical outputs
