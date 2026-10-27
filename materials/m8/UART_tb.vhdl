library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity tb_uart_tx is
end tb_uart_tx;

architecture sim of tb_uart_tx is

--------------------------------------------------------------------
-- Task 5: Edit Ports based on New Obfuscated UART Design
--------------------------------------------------------------------

component uart_tx
Port (
    clk       : in  std_logic;
    reset     : in  std_logic;
    tx_start  : in  std_logic;
    data_in   : in  std_logic_vector(7 downto 0);
    tx        : out std_logic
);
end component;

signal clk      : std_logic := '0';
signal reset    : std_logic := '1';
signal tx_start : std_logic := '0';

signal data_in  : std_logic_vector(7 downto 0) := "10101010";
signal tx       : std_logic;

--------------------------------------------------------------------
-- Task 6: Add Constant Key Values you want to Enter
--------------------------------------------------------------------

-- 100 MHz clock
constant CLK_PERIOD : time := 10 ns;

begin

--------------------------------------------------------------------
-- Task 5: Edit Ports based on New Obfuscated UART Design
--------------------------------------------------------------------

uut : uart_tx
port map(
    clk      => clk,
    reset    => reset,
    tx_start => tx_start,
    data_in  => data_in,
    tx       => tx
);

clk <= not clk after CLK_PERIOD/2;

process
begin

reset <= '1';
wait for 50 ns;
reset <= '0';

wait for 100 ns;

--------------------------------------------------------------------
-- Task 7: Enter Each Key Sequence
--------------------------------------------------------------------

wait until rising_edge(clk);
tx_start <= '1';

wait until rising_edge(clk);
tx_start <= '0';

wait for 200us;

assert false report "SIM DONE" severity failure;
    
end process;

end sim;