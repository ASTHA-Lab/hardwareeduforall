#include <reg51.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

void UART_Init()
{
    TMOD |= 0x20;      // Timer1 in mode 2 (auto-reload)
    TH1 = 0xFD;        // Set baud rate to 9600 (for a 12 MHz crystal)
    SCON = 0x50;       // 8-bit UART, enable receiver
    TR1 = 1;           // Start timer1
}

char UART_ReadChar()
{
    while(!RI);        // Wait until character is received
    RI = 0;            // Reset receive interrupt flag
    return SBUF;       // Return received character
}

void UART_SendChar(char c)
{
    SBUF = c;          // Send character via UART
    while(!TI);        // Wait until character is sent
    TI = 0;            // Reset transmit interrupt flag
}

void UART_SendString(char* str)
{
    while(*str != '\0')
    {
        UART_SendChar(*str);    // Send character via UART
        str++;                  // Move to next character in string
    }
}

void main()
{
	char input[10];
	char c;
	int i = 0, len = 0;
	char password[] = "kuastha";
	UART_Init();
	while (1)
	{
		int i = 0, len = 0;
		UART_SendString("Enter password: \n");
		do
		{
			c = UART_ReadChar();    // Read character from UART
			if(c == '\r')           // Ignore carriage returns
				continue;
			if(c == '\b')           // Handle backspaces
			{
				if(i > 0)
				{
					i--;
					UART_SendChar(c);
					UART_SendChar(' ');
					UART_SendChar(c);
				}
				continue;
			}
			input[i] = c;             // Store character in string
			UART_SendChar(c);       // Echo character back to terminal
			i++;
		} while(c != '.');         // Stop when null terminator is received
		input[i-1] = '\0';            // Replace newline with null terminator
		UART_SendString("\r\nYou entered: ");
		UART_SendString(input);
		// Secured password checking algorithm
		len = i - 1;
		
		TR0 = 1;       // End Timer0
		if(len != strlen(password))       // Check length of input string
		{
			// Do something if password is incorrect
			//P1 |= 0x00;
			TR0 = 0;
			UART_SendString("\r\nIncorrect password length :(\r\n");
			//return 0;
		}
		else
		{
			for(i = 0; i < len; i++)      // Compare characters one by one
			{
				if(input[i] != password[i])
				{
					// Do something if password is incorrect
					TR0 = 0;
					UART_SendString("\r\nIncorrect password found!\r\n");
					break;
					//return 0;
				}
			}
			if (i == len)                 // All characters match
			{
				TR0 = 0;
				UART_SendString("\r\nPassword accepted!\r\n");
				// Do something if password is correct
			}	
		}
	}
}



