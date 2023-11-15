#include <iostream>

extern "C"
void printa(char** arr, int len)
{
	for(int i = 0; i < len; ++i)
		std::cout << arr[i] << std::endl;
}


extern "C" 
void print2d(char*** arr, int len, int max_inner_len)
{
	for(int i = 0; i < len; ++i)
	{
		for(int j = 0; j < max_inner_len && arr[i][j]; ++j)
		{
			std::cout << arr[i][j] << ' ';
			std::cout.flush();
		}
		std::cout.put('\n');
	}
}
