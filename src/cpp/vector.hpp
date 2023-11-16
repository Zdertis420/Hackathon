#ifndef HACKATHON_SRC_CPP_VECTOR_H
#define HACKATHON_SRC_CPP_VECTOR_H


#include <unordered_map>
#include <unordered_set>
#include <string_view>
#include <filesystem>
#include <functional>
#include <algorithm>
#include <iostream>
#include <optional>
#include <fstream>
#include <vector>

using all_keys_t = std::unordered_set<std::string_view>;
using filemap = std::unordered_map<std::string_view, uint32_t>;
using filemaps = std::vector<filemap>;
using vec = std::vector<uint32_t>;
using axis_order = std::vector<std::string>;

enum struct tasks {
	task1 = 0x01,
	task2 = 0x02,
};

namespace internal {

void clean_vectors(std::vector<vec> &files);

void normalize_vectors(std::vector<vec> &vectors);

std::vector<vec> &&get_vectors(all_keys_t &all_keys, &filemaps maps);

template <typename Key, typename Val>
void normalize_keys(
		const std::unordered_set<Key> &set,
		std::unordered_map<Key, Val> &map1,
//		std::unordered_map<Key, Val> &map2
) {
	for(const auto& key : set)
	{
		map1.insert({key, 0});
//		map2.insert({key, 0});
	}
}

std::unordered_set<std::string_view> &&normalize_map_fields(filemap& files); 

} // namepsace internal

extern "C" {
void driver (
	unsigned int flags,			// tasks to be done
	char*** docsv, uint32_t docsc,		// array of documents
	char*** themesv, uint32_t themesc,	// array of themes
	//int first_index	// first file name
	char* path_to_docs,	// Same as in python
	char* analyze_out,	// Same as in python
	char* analyze_in,	// Same as in python
	char* themes_in,	// Same as in python
	char* final_out		// Same as in python
);
void analyze_files(char** words, size_t size, char* out_dir_path);
void calculate_angles();
void print_2d_array(char*** array, size_t size);

} // extern "C"


#endif // HACKATHON_SRC_CPP_VECTOR_H
