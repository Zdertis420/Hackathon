#ifndef HACKATHON_SRC_CPP_VECTOR_H
#define HACKATHON_SRC_CPP_VECTOR_H


#include <unordered_map>
#include <unordered_set>
#include <string_view>
#include <algorithm>
#include <filsystem>
#include <fstream>
#include <vector>

using filemap = std::unordered_map<std::string_view, uint32_t>;
using filemaps = std::vector<filemap>;

enum struct Flags {
	
}

namespace internal {
	std::unordered_set &&normalize_map_fields(filemap& files); 
	
	
	

} // namepsace internal

extern "C" {
// питухон передаёт argc и argv, но не все, а только с путями
// питон может передать nullptr
void driver (
	unsigned int flags
	char*** docsv, uint32_t docsc,
	char*** themesv, uint32_t themesc
);
void analyze_files(char** words, int size, char* out_dir_path);
void calculate_angles();

} // exterm "C"


#endif // HACKATHON_SRC_CPP_VECTOR_H
