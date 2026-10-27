library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.std_logic_unsigned.all;

entity tb_4BitAdder is
end tb_4BitAdder;

architecture testbench of tb_4BitAdder is

component Adder4Bit_Key is
    Port ( A : in STD_LOGIC_VECTOR (3 downto 0);
           B : in STD_LOGIC_VECTOR (3 downto 0);
           Ci : in STD_LOGIC;
           Key : in STD_LOGIC_VECTOR (2 downto 0);
           S : out STD_LOGIC_VECTOR (3 downto 0);
           Co : out STD_LOGIC);
end component;

signal x_in, y_in : STD_LOGIC_VECTOR(3 downto 0);
signal c_in : STD_LOGIC;
signal key_in : STD_LOGIC_VECTOR(2 downto 0);
signal s_out : STD_LOGIC_VECTOR(3 downto 0);
signal c_out : STD_LOGIC;

begin

    DUT: Adder4Bit_Key port map(x_in, y_in, c_in, key_in, s_out, c_out);
    
    process
    begin
        c_in <= '0';     -- Assume Carry_in is Always Zero
        key_in <= "010"; -- Key Input Vector
        x_in <= "0000";
        y_in <= "0000";
        wait for 1ns;
        
        -- Iterate over all possible input valuations
        for i in 0 to 15 loop
            for j in 0 to 15 loop
                y_in <= y_in + "0001";
                wait for 1ns;
            end loop;
            x_in <= x_in + "0001";
        end loop;
        
     end process;
end testbench;
