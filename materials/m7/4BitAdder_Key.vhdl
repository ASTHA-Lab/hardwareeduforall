library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity Adder4Bit_Key is
    Port ( A : in STD_LOGIC_VECTOR (3 downto 0);
           B : in STD_LOGIC_VECTOR (3 downto 0);
           Ci : in STD_LOGIC;
           Key : in STD_LOGIC_VECTOR (2 downto 0);
           S : out STD_LOGIC_VECTOR (3 downto 0);
           Co : out STD_LOGIC);
end Adder4Bit_Key;
 
architecture Structure of Adder4Bit_Key is

component FullAdder is
    Port ( X : in STD_LOGIC;
           Y : in STD_LOGIC;
           Cin : in STD_LOGIC;
           Cout : out STD_LOGIC;
           Sum : out STD_LOGIC);
end component;

signal C            : std_logic_vector(3 downto 1);
signal Key_mod      : std_logic_vector(2 downto 0);
signal masked_carry : std_logic_vector(3 downto 1);
signal trigger      : std_logic;

begin

    FA0: FullAdder port map(A(0), B(0), Ci, C(1), S(0));

--------------------------------------------------------------------
-- Task 1: Write the code for the trigger condition and payload below
--------------------------------------------------------------------

    -- XOR/XNOR obfuscation using modified key
    masked_carry(1) <= Key_mod(0) xor C(1);
    masked_carry(2) <= Key_mod(1) xnor C(2);
    masked_carry(3) <= Key_mod(2) xor C(3);
    
-- Combinational Obfuscation using MUXs
--    masked_carry(1) <= C(1) when Key_mod(0)='1' else A(0);
--    masked_carry(2) <= C(2) when Key_mod(1)='0' else B(2);
--    masked_carry(3) <= C(3) when Key_mod(2)='1' else A(0);

    FA1: FullAdder port map(A(1), B(1), masked_carry(1), C(2), S(1));
    FA2: FullAdder port map(A(2), B(2), masked_carry(2), C(3), S(2));
    FA3: FullAdder port map(A(3), B(3), masked_carry(3), Co,   S(3));
    
-- Original Design
--    FA1: FullAdder port map(A(1), B(1), C(1), C(2), S(1));
--    FA2: FullAdder port map(A(2), B(2), C(2), C(3), S(2));
--    FA3: FullAdder port map(A(3), B(3), C(3), Co, S(3));

end Structure;