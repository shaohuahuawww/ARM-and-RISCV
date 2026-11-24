module retire_mon();
  reg active;
  reg [63:0] total_cycles;
  reg [63:0] cycles;
  reg [63:0] instret;

  initial begin
    active       = 1'b0;
    total_cycles = 64'd0;
    cycles       = 64'd0;
    instret      = 64'd0;
  end

  always @(posedge tb.clk or negedge tb.rst_b) begin
    if (!tb.rst_b) begin
      active       <= 1'b0;
      total_cycles <= 64'd0;
      cycles       <= 64'd0;
      instret      <= 64'd0;
    end else begin
      total_cycles <= total_cycles + 64'd1;
      if (total_cycles != 0 && (total_cycles % 100000) == 0) begin
        $display("[E902-HB] total_cyc=%0d active=%0d win_cyc=%0d win_inst=%0d pc=%08h",
                 total_cycles, active, cycles, instret, tb.x_soc.x_cpu_sub_system_ahb.biu_pad_retire_pc);
      end
      if (tb.cpu_trans == 2'b10 && tb.cpu_addr == 32'h6000fff4 && tb.cpu_write) begin
        if (tb.cpu_wdata == 32'd1 && !active) begin
          active  <= 1'b1;
          cycles  <= 64'd0;
          instret <= 64'd0;
        end else if (tb.cpu_wdata == 32'd2 && active) begin
          active <= 1'b0;
          $display("[E902-MON] cycles=%0d instret=%0d", cycles, instret);
        end
      end
      if (active) begin
        cycles <= cycles + 64'd1;
        if (tb.x_soc.x_cpu_sub_system_ahb.biu_pad_retire) begin
          instret <= instret + 64'd1;
        end
      end
    end
  end
endmodule
