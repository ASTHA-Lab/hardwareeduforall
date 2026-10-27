library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

--------------------------------------------------------------------
-- Task 4: Add "key_valid" and "key_seq" as Inputs
--------------------------------------------------------------------

entity uart_tx is
    Port (
        clk       : in  std_logic;
        reset     : in  std_logic;
        tx_start  : in  std_logic;
        data_in   : in  std_logic_vector(7 downto 0);
        tx        : out std_logic
    );
end uart_tx;

architecture Behavioral of uart_tx is

constant BAUD_DIV : integer := 868;
--------------------------------------------------------------------
-- Task 3: Add Constant Values of the 8-bit Keys
--------------------------------------------------------------------

--------------------------------------------------------------------
-- Task 1: Add additional obfuscation states S0, S1, and S2
--------------------------------------------------------------------
type state_type is (
    IDLE,
    START_BIT,
    DATA_BITS,
    STOP_BIT
);

signal state : state_type := IDLE;

-- Signal to keep track of current state on timing diagram
signal state_track : integer := 0;

signal baud_counter : integer range 0 to BAUD_DIV := 0;
signal baud_tick : std_logic := '0';

signal shift_reg : std_logic_vector(7 downto 0) := (others => '0');
signal bit_counter : integer range 0 to 7 := 0;

signal tx_reg : std_logic := '1';

begin

tx <= tx_reg;

--------------------------------------------------------------------
-- DEBUG STATE DISPLAY
--------------------------------------------------------------------
with state select
state_track <=
    3 when IDLE,
    4 when START_BIT,
    5 when DATA_BITS,
    6 when STOP_BIT;

--------------------------------------------------------------------
-- BAUD GENERATOR
--------------------------------------------------------------------
process(clk, reset)
begin
if reset = '1' then
    baud_counter <= 0;
    baud_tick <= '0';
elsif rising_edge(clk) then
    if baud_counter = BAUD_DIV - 1 then
        baud_counter <= 0;
        baud_tick <= '1';
    else
        baud_counter <= baud_counter + 1;
        baud_tick <= '0';
    end if;
end if;
end process;


process(clk, reset)
begin
if reset = '1' then
    state <= IDLE;
    tx_reg <= '1';
    bit_counter <= 0;
    shift_reg <= (others => '0');

elsif rising_edge(clk) then
case state is

--------------------------------------------------------------------
-- Task 1: Add additional obfuscation states S0, S1, and S2 Below
--------------------------------------------------------------------


--------------------------------------------------------------------
-- UART
--------------------------------------------------------------------
when IDLE =>
    tx_reg <= '1';
    if tx_start = '1' then
        shift_reg <= data_in;
        bit_counter <= 0;
        state <= START_BIT;
    end if;

when START_BIT =>
    tx_reg <= '0';
    if baud_tick='1' then
        tx_reg <= shift_reg(0);
        shift_reg <= '0' & shift_reg(7 downto 1);
        bit_counter <= 0; 
        state <= DATA_BITS;
    end if;

when DATA_BITS =>
    if baud_tick='1' then
        tx_reg <= shift_reg(0);
        shift_reg <= '0' & shift_reg(7 downto 1);

        if bit_counter = 7 then
            bit_counter <= 0;
            tx_reg <= '1';
            state <= STOP_BIT;
        else
            bit_counter <= bit_counter+1;
        end if;
    end if;

when STOP_BIT =>
    tx_reg <= '1';
    if baud_tick = '1' then
        state <= IDLE; 
    end if;
--------------------------------------------------------------------
-- Task 2: Add the "LOCKED" State Below
--------------------------------------------------------------------

end case;
end if;
end process;

end Behavioral;