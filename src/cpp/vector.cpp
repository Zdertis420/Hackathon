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
    std::vector<vec> files_parsed; //is set differently based on task flags

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
        for (const auto& entry: fs::directory_iterator{inpath})
        {
            if (entry->is_character_file()) ++n_elem;
        }
    }
    dbg::print_map(files[1]);
    dbg::print_map(themes[0]);

    auto [files_parsed, order] = internal::get_vectors(all_keys, files);

    internal::clean_vectors(files_parsed, order);

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

std::pair<std::vector<vec>, axis_order> internal::get_vectors(all_keys_t &all_keys, filemaps &maps)
{

    normalize_keys<std::string_view, uint32_t>(all_keys, maps);
	//construct order array
	axis_order order(all_keys.size());
    int j = 0;
    for(auto i = all_keys.begin(); i != all_keys.end(); ++i, ++j)
		order[j] = *i;

    std::vector<vec> ret(maps.size());
    for(size_t i  = 0; i < maps.size(); ++i)
	{
		for (const auto& key : order)
			ret[i].push_back(maps[i].at(key));
	}
    // after this loop ret contains a list of word vectors

    return std::make_pair(std::move(ret), std::move(order));
}

void internal::clean_vectors(std::vector<vec> &files, axis_order &ord)
{
    assert(files[0].size() == ord.size());
    std::vector<double> variances(files.at(0).size());
    //calvulate varianecs
    /*  tf(X): N/n(X) ~ N/sqrt( n(X)^2 ) [Token frequency]
     *  idf: log(N/D), где
     *      N: files.size()
     *      D: std::accumulate(files, {return | i[j] | <= 10e-6})
     *
     *  W: tf*idf
     */

    for(size_t j = 0; j < files.at(0).size(); ++j)
    {
        uint32_t amount = 0;
        for (size_t i = 0; i < files.size(); ++i)
        {
            if (files.at(i).at(j) != 0) ++amount;
        }
    }

//	for(int i = 0; i < files.at(0).size(); ++i)
//	{	// using a 2-pass algorithm
//		double mean = 0;
//		for (int j = 0; j < files.size(); ++j)
//        {
//            mean += files[j][i];
//        }
//        mean /= files.size();
//        double variance = 0;
//		for (int j = 0; j < files.size(); ++j)
//		{
//            double temp = files[j][i] - mean;
//			variance += temp*temp;
//		}
//		variance /= (files.size() - 1);
//        variances[i] = std::sqrt(variance);
//    }

    //calculating edge variance
    constexpr const double fraction = 1/5;
    auto const [min, max] = std::accumulate(
        variances.cbegin(),
        variances.cend(),
        std::pair<double, double>{},
        [](std::pair<double, double> min_max, double val)
        {
            return std::pair<double, double>{
                std::min(val, min_max.first),
                std::max(val, min_max.second)
            };
        }
    );
    double edge = min + (max-min)*fraction;

    SANITY_CHECK (
        std::printf("min: %f, max: %f, edge: %f\n", min, max, edge);
        for(int i = 0; i < ord.size(); ++i)
            std::printf("word: %s: stddev: %lf\n", ord[i].data(),  variances[i]);
    )

    // constructing new vectors without beyond-edge elements
    std::vector<vec> files_new(files.size());
    axis_order ord_new;
    for (auto& x : files_new) x.reserve( ord.size() * (1-edge) );
    ord_new.reserve( ord.size() * (1-edge) );

    for (size_t i = 0; i < ord.size(); ++i) {
        if (variances[i] < edge) continue;

        ord_new.push_back(ord[i]);
        for (size_t j = 0; j < files.size(); ++j)
        {
            files_new[j].push_back(files[j][i]);
        }
    }

    // reassignment
    files = std::move(files_new);
    ord = std::move(ord_new);
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
