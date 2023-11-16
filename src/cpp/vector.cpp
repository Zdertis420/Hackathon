#include "vector.hpp"


const char* driver (
	unsigned int flags,
	char*** docsv, uint32_t docsc,
	char*** themesv, uint32_t themesc,
	char* path_to_docs,
	char* analyze_out,
	char* analyze_in,
	char* themes_in,
	char* final_out	
) {

	auto files = filemaps(docsc);
	auto themes = filemaps(themesc);
	std::unordered_set<std::string_view> all_keys;
	std::vector<vec> files_parsed; //is set differently based on task flags
	if (flags & tasks::task1) {
		// reading docs
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
		//reading themes
		if (!themesv || !themesc) return "Для первого задания необходим путь и количество файлов не может быть нулевым.";
		for (int i = 0; i < themesc; ++i)
		{
			for (char** strarr = themesv[i]; *strarr; ++strarr) // same here
			{
				auto key = std::string_view(*strarr);
				++themes[i][key];
				all_keys.insert(key);
			}
		}
		files_parsed = get_vectors(all_keys, files);
		
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

std::vector<vec> &&internal::get_vectors(all_keys_t &all_keys, &filemaps maps)
{
	normalize_keys(all_keys, filemaps);
	//construct order array
	axis_order order(all_keys.size());
	for(auto i = all_keys.begin(), j = 0; i != all_keys.end(); ++i, ++j)
		order[j] = *i;

	std::vector<vec> ret(filemaps.size());
	size_t vec_d = all_keys(size);
	for(auto i  = 0; i < maps.size(); ++i)
	{
		for (const auto& key : order)
			ret[i].push_back(maps[i].at(key));
	}
	// after this loop ret contains a list of word vectors
	return ret;
}
v
void clean_vectors(std::vector<vec> &files)
{
	std::vector<double> variances(files.at(0).size());
	// calvulate varianecs
	for(int i = 0; i < files.at(0).size(); ++i)
	{	// using a 2-pass algorithm
		double mean = 0;
		for (int j = 0; j < files.size(); ++j)
		{
			mean += files[i][j];
		}
		mean /= files.size();
		double variance = 0
		for (int j = 0; j < files.size(); ++j)
		{
			double temp = files[i][j] - mean;
			variance += temp*temp;
		}
		variance /= (files.size() - 1);
		variances[i] = std::sqrt(variance); // is it really needed?
	}
	

}




