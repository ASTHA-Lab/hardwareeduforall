library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity FullAdder is
    Port ( X : in STD_LOGIC;
           Y : in STD_LOGIC;
           Cin : in STD_LOGIC;
           Cout : out STD_LOGIC;
           Sum : out STD_LOGIC);
end FullAdder;

architecture Equations of FullAdder is
begin

Sum <= X xor Y xor Cin;
Cout <= (X and Y) or (X and Cin) or (Y and Cin);

end Equations;
