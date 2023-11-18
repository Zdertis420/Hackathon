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
#include <string>
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


using all_keys_t = std::unordered_set<std::string>;
using filemap = std::unordered_map<std::string, uint>;
using filemaps = std::vector<filemap>;
using vec = std::vector<uint32_t>;
using vecd = std::vector<double>;
using axis_order = std::vector<std::string>;
using uint = unsigned int;
namespace fs = std::filesystem;


namespace internal {

    std::vector<vecd> get_word_costs(const std::vector<vec> &files, const axis_order &ord);

    void read_from_chars(char*** what, uint how_much, filemaps &where, all_keys_t &all_keys);
    void read_from_files(char* foldername, filemaps &where, all_keys_t &all_keys);

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
            for (auto m1  = maps1.begin(); m1 != maps1.end(); m1++)
                m1->insert({key, 0});
            for (auto m2  = maps2.begin(); m2 != maps2.end(); m2++)
                m2->insert({key, 0});
        }
    } // normalize_keys

    std::vector<vecd> compare_themes(
        const std::vector<vecd> &costsd,
        const std::vector<vecd> &costst
    );

    void output_data(
        const std::vector<vecd> &docs_themes,
        char* output_path,
        uint doc_index,
        uint theme_index
    );

} // namepsace internal


namespace math {

    double vector_abs(const auto &v)
    {
        return std::sqrt(std::accumulate(v.cbegin(), v.cend(), 0.0,
            [] (auto acc, auto x) {
                return acc + x*x;
            }));
    }
    vecd normalize(const auto &v)
    {
        const double abs = vector_abs(v);
        auto ret = vecd();
        ret.reserve(v.size());
        std::for_each(v.cbegin(), v.cend(), [abs, &ret] (auto x) {ret.push_back(x/abs);} );
#ifdef DEBUG
        assert( std::abs(vector_abs(v) - 1) < 0.0001 );
#endif
        return ret;
    }
    double dot_product(const auto &x, const auto &y)
    {
        double ret = 0;
        assert(x.size() == y.size());
        for(size_t i = 0; i < x.size(); ++i)
            ret += (x[i]*y[i]);
        return ret;
    }
    vecd sub_vector(const auto &x, const auto &y)
    {
        assert(x.size() == y.size());
        size_t vdim = x.size();
        decltype(x) ret(vdim);
        for (size_t i = 0; i < vdim; ++i)
            ret[i] = x[i]-y[i];
        return ret;
    }
    double angle_cos(const auto &x, const auto &y)
    {
        // cos(a) = |x * y| / sqrt(|x|*|y|);
        return std::abs( math::dot_product(x, y) )
               / (math::vector_abs(x) * math::vector_abs(y) );
    }

}// namespace math

namespace dbg {

    void print_map(const auto& map) {
    #ifdef  DEBUG
        std::cout << "PRINTING INFO |" << __PRETTY_FUNCTION__ << '\n';
        std::cout << map.size() << std::endl;
        for(const auto& [a, b] : map){
            std::cout << a << " - " << b << std::endl;
        }
    #endif
    }

} // namespace dbg

extern "C" {

    const char* driver (
        uint flags,			// tasks to be done
        uint first_doc_filename,
        uint first_theme_filename,
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
