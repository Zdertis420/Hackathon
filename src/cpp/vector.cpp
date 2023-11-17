#include "vector.hpp"


const char* driver (
    [[maybe_unused]] uint flags,
    [[maybe_unused]] uint first_filename,
    char*** docsv,   uint docsc,
    char*** themesv, uint themesc,
    [[maybe_unused]] char* themes_in,
    [[maybe_unused]] char* analyze_in,
    [[maybe_unused]] char* final_out
) {

    filemaps files;
    filemaps themes;
    all_keys_t all_keys;
//    std::vector<vec> files_parsed;   // is set differently based on task flags
//    std::vector<vec> themes_parsed;  // is set differently based on task flags

    if (flags == 0xb11)
    {
        files = filemaps(docsc);
        themes = filemaps(themesc);

        // reading docs
        if (!docsv || !docsc) return "Для первого задания необходим путь к входным файлам и количество файлов не может быть нулевым.";
        for (uint i = 0; i < docsc; ++i)
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
        for (uint i = 0; i < themesc; ++i)
        {
            for (char** strarr = themesv[i]; *strarr; ++strarr) // same here
            {
                auto key = std::string_view(*strarr);
                ++themes[i][key];
                all_keys.insert(key);
            }
        }
    }
    if (flags == 0b10)
    {
        if (!analyze_in) return "При выполнении второго задания отдельно от первого, необходимо предоставить путь до проанализированных файлов";
        const fs::path inpath{analyze_in};
        size_t n_elem = 0;
//        for (const auto& entry: fs::directory_iterator{inpath})
//        {
//            if (entry->is_character_file()) ++n_elem;
//        }
        std::cout << n_elem;
    }
    dbg::print_map(files[1]);
    dbg::print_map(themes[0]);
    internal::normalize_keys(all_keys, files, themes);
    auto [files_parsed, themes_parsed, order] = internal::get_vectors(all_keys, files, themes);

    // auto x = internal::get_word_costs(files_parsed, order);


    return "";
}

void print_2d_array(char*** array, uint size)
{
	std::cout << "tunning test function...\n";
    for(uint i = 0; i < size; ++i)
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

std::tuple<std::vector<vec>, std::vector<vec>, axis_order>
internal::get_vectors(const all_keys_t &all_keys, const filemaps &maps, const filemaps &themes)
{
	//construct order array
	axis_order order(all_keys.size());
    int j = 0;
    for(auto i = all_keys.begin(); i != all_keys.end(); ++i, ++j)
		order[j] = *i;

    std::vector<vec> ret1(maps.size());
    std::vector<vec> ret2(themes.size());
    for(size_t i = 0; i < maps.size(); ++i)
	{
        for (const auto& key : order)
        {
            ret1[i].push_back(maps[i].at(key));
            ret2[i].push_back(maps[i].at(key));
        }
	}

    return std::make_tuple(std::move(ret1), std::move(ret2), std::move(order));
}

std::vector<vecd> internal::get_word_costs(const std::vector<vec> &files, const axis_order &ord)
{
    assert(files[0].size() == ord.size());
    //  calvulate varianecs
    /*  tf(X): N/n(X) ~ N/sqrt( n(X)^2 ) [Token frequency]
     *  idf: log(N/D), где
     *      N: files.size()
     *      D: std::accumulate(files, {return | i[j] | <= 10e-6})
     *
     *  W: tf*idf
     */

    std::vector<vecd> ret(files.size());
    for(auto& x : ret) {
        x = vecd(); // TODO ДОПИСАТЬ
    }

    return ret;

}

double math::vector_abs(const vec &v)
{
    return std::sqrt( std::accumulate(v.cbegin(), v.cend(), 0.0, [] (auto acc, auto x) {return acc + x*x;}) );
}


vecd math::normalize(const vec &v)
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

double math::dot_product(const vec &x, const vec &y)
{
    double ret = 0;
    assert(x.size() == y.size());
    for(size_t i = 0; i < x.size(); ++i)
        ret += (x[i]*y[i]);
    return ret;
}
