# VSD Cloud FPGA – VSDSquadron FPGA Mini

This repo lets you:
- Use **GitHub Codespaces** to build bitstreams for VSDSquadron FPGA Mini (iCE40UP5K).
- Program the board on your **local machine** using a tiny agent + ngrok.

## 1. One-time setup on your laptop

(Provided in a separate "VSD Agent" package)

1. Install the VSD Agent and `iceprog` (or openFPGALoader) as per VSD instructions.
2. Plug in your VSDSquadron FPGA Mini board.
3. Start the VSD Agent – it listens on `http://localhost:5000/flash`.
4. In a terminal, run:

   ```bash
   ngrok http 5000
