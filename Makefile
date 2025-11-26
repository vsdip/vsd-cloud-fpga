# Simple Makefile for VSDSquadron FPGA Mini (iCE40UP5K)

TOP        := top
SRC_DIR    := src
BUILD_DIR  := build
TOP_V      := $(SRC_DIR)/$(TOP).v
CONSTR     := $(SRC_DIR)/constraints.pcf

YOSYS      := yosys
NEXTPNR    := nextpnr-ice40
ICEPACK    := icepack

DEVICE     := up5k
PACKAGE    := sg48

all: bit

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

json: $(BUILD_DIR) $(TOP_V)
	$(YOSYS) -p "synth_ice40 -top $(TOP) -json $(BUILD_DIR)/$(TOP).json" $(TOP_V)

asc: json
	$(NEXTPNR) --$(DEVICE) --package $(PACKAGE) \
	  --json $(BUILD_DIR)/$(TOP).json \
	  --pcf $(CONSTR) \
	  --asc $(BUILD_DIR)/$(TOP).asc

bit: asc
	$(ICEPACK) $(BUILD_DIR)/$(TOP).asc $(BUILD_DIR)/$(TOP).bin
	@echo "Bitstream generated at $(BUILD_DIR)/$(TOP).bin"

clean:
	rm -rf $(BUILD_DIR)

.PHONY: all json asc bit clean

