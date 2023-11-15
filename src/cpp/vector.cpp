#include "vector.hpp"


const char* driver (
	unsigned int flags,
	char*** docsv, uint32_t docsc,
	char*** themesv, uint32_t themesc,
	char* path_to_docs,
	char* analyze_out,
	char* analyze_in,
	char* theme_div_in,
	char* theme_div_out,
	char* final_out	
) {

	auto files = filemaps(docsc);
	auto themes = filemaps(themesc);
	std::unordered_set<std::string_view> all_keys;
	if (flags & tasks::task1) {
		if (!docsv || !docsc) return "Для первого задания необходим путь к входным файлам и количество файлов не может быть нулевым.";
		for (int i = 0; i < docsc; ++i)
		{
			for (char** strarr = docsv[i]; *strarr; ++strarr) // read until nullptr
			{
				auto key = std::string_view(*strarr);
				++files[i][key];
				all_keys.insert(key);
			}
		}
		if (!themesv || !themesc) return "Для первого задания необходим путь к файлам тем и количество файлов не может быть нулевым.";
		for (int i = 0; i < themesc; ++i)
		{
			for (char** strarr = themesv[i]; *strarr; ++strarr) // same here
			{
				auto key = std::string_view(*strarr);
				++themes[i][key];
				all_keys.insert(key);
			}
		}
		// сконструировать вектора
		// отфильтровать их
		// вывести в файл
	}
	if (flags & tasks::task2) {
		// прочитать из файла сразу в вектора
		// посчитать по формуле сходство
		// вывести в файлы
	}
	if (flags & tasks::task3) {
		// прочитать из файла сходства 
		// рассортировать по папкам
	}
}

void print_2d_array(char*** array, size_t size)
{
	std::cout << "tunning test function...\n";
	for(int i = 0; i < size; ++i)
	{
		std::cout << "string " << i << std::endl;
		for(char** p = array[i]; *p; ++p)
		{
			std::cout << p << " - " ;
			std::cout.flush();
			std::cout << *p << " | ";
		}
		std::cout << std::endl;
	}
	std::cout << "test function success!\n";
}

