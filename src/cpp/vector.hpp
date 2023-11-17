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
#include <numeric>
#include <utility>
#include <cassert>
#include <vector>
#include <tuple>
#include <cmath>

#ifdef DEBUG
#define SFD \
std::cout << __FILE__ << ':' << __FUNCTION__ << ':' << __LINE__ << std::endl
#define SANITY_CHECK(x) x
#else
#define SFD
#define SANITY_CHECK(x)
#endif


using all_keys_t = std::unordered_set<std::string_view>;
using filemap = std::unordered_map<std::string_view, uint32_t>;
using filemaps = std::vector<filemap>;
using vec = std::vector<uint32_t>;
using vecd = std::vector<double>;
using axis_order = std::vector<std::string>;
using uint = unsigned int;
namespace fs = std::filesystem;


namespace internal {

    std::vector<vecd> get_word_costs(const std::vector<vec> &files, const axis_order &ord);

    void normalize_vectors(std::vector<vec> &vectors);

    std::tuple<std::vector<vec>, std::vector<vec>, axis_order>
    get_vectors(const all_keys_t &all_keys, const filemaps &maps, const filemaps &themes);

    template <typename Key, typename Val>
    void normalize_keys(
            const std::unordered_set<Key> &set,
            std::vector<std::unordered_map<Key, Val>> &maps1,
            std::vector<std::unordered_map<Key, Val>> &maps2
    ) {
        for(const auto& key : set)
        {
            for(auto m1  = maps1.begin(), m2  = maps2.begin();
                     m1 != maps1.end() && m2 != maps2.end();
                     m1++,                m2++ )
            {
                m1->insert({key, 0});
                m2->insert({key, 0});
            }
        }
    }

    std::unordered_set<std::string_view> &&normalize_map_fields(filemap& files);

} // namepsace internal


namespace math {

    double vector_abs(const vec &v);
    vecd normalize(const vec &v);
    double dot_product(const vec &x, const vec &y);
    double angle_cos(const vecd &x, const vecd &y);

}// namespace math


namespace dbg {

    void print_map([[maybe_unused]] const auto& map) {
    #ifdef  DEBUG
        std::cout << "PRINTING INFO |" << __PRETTY_FUNCTION__ << '\n';
        for(const auto& [a, b] : map)
            std::cout << a << " - " << b << std::endl;
    #endif
    }

} // namespace dbg


extern "C" {

    const char* driver (
        uint flags,			// tasks to be done
        uint first_filename,
        char*** docsv, uint docsc,		// array of documents
        char*** themesv, uint themesc,	// array of themes
        char* themes_it,    // Same as in python
        char* analyze_in,	// Same as in python
        char* final_out		// Same as in python
    );
    void analyze_files(char** words, size_t size, char* out_dir_path);
    void calculate_angles();
    void print_2d_array(char*** array, size_t size);

} // extern "C"


#endif // HACKATHON_SRC_CPP_VECTOR_H
