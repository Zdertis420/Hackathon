#include "vector.hpp"


void driver (
	unsigned int flags, 
	char*** docsv, uint32_t docsc,
	char*** themesv, uint32_t themesc
) {
	filemaps files; // the files will be stored here
	std::unordered_set<std::string_view> all_keys;
}

void print_2d_array(char*** array, size_t size)
{
	std::cout << "tunning test function...\n";
	for(int i = 0; i < size; ++i)
	{
		std::cout << "string " << i << std::endl;
		for(char** p = array[i]; p; ++p)
		{
			std::cout << p << ':' ;
			std::cout.flush();
			std::cout << *p << " | ";
		}
		std::cout << std::endl;
	}
	std::cout << "test function success!\n";
}

