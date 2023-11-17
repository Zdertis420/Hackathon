#include "vector.hpp"


const char* driver (
    uint flags,
    [[maybe_unused]] uint first_doc_filename,
    [[maybe_unused]] uint first_theme_filename,
    char*** docsv,   uint docsc,
    char*** themesv, uint themesc,
    [[maybe_unused]] char* themes_in,
    [[maybe_unused]] char* analyze_in,
    [[maybe_unused]] char* final_out
) {

    filemaps files;
    filemaps themes;
    all_keys_t all_keys;

    if (flags == 0xb11)
    {
        files = filemaps(docsc);
        themes = filemaps(themesc);

        // reading docs
        if (!docsv || !docsc) return "Для первого задания необходим путь к входным файлам и количество файлов не может быть нулевым.";
        if (!themesv || !themesc) return "Для первого задания необходим путь и количество файлов не может быть нулевым.";

        read_from_chars(docsv, docsc, files, all_keys);
        read_from_chars(docsv, docsc, files, all_keys);
    }
    if (flags == 0b10)
    {
        if (!analyze_in) return "При выполнении второго задания отдельно от первого, необходимо предоставить путь до проанализированных файлов";
        if (!themes_in) return "При выполнении второго задания отдельно от первого, необходимо предоставить путь до папки с проанализированными темами";

        read_from_files(analyze_in, files, all_keys);
        read_from_files(themes_in, themes, all_keys);

    }
    dbg::print_map(files[1]);
    dbg::print_map(themes[0]);
    internal::normalize_keys(all_keys, files, themes);
    auto [files_parsed, themes_parsed, order] = internal::get_vectors(all_keys, files, themes);

    auto files_calculated = internal::get_word_costs(files_parsed, order);
    auto themes_calculated = internal::get_word_costs(themes_parsed, order);



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

/*
 *  tf(X): N/n(X) ~ N/sqrt( n(X)^2 ) [Token frequency]
 *  idf: log(N/D), где
 *      N: files.size()
 *      D: std::accumulate(files, {return | i[j] | <= 10e-6})
 *  W: tf*idf
 */

std::vector<vecd> internal::get_word_costs(const std::vector<vec> &files, const axis_order &ord)
{   // TODO: REPLACE ALL .at() METHODS WITH [] AFTER DEBUGGING
    assert(files[0].size() == ord.size());

    size_t  amount_of_words = files.at(0).size(),
            amount_of_files = files.size();
    auto idfs = vecd(amount_of_words);
    auto amounts = vec(amount_of_files);

    // блять, главное с индексами не запутаться...
    for (size_t i = 0; i < amount_of_words; ++i)
    {
        double idf = 0;
        for(size_t j = 0; j < amount_of_files; ++j)
        {   //amount of files containing that word
            int current_word_count = files.at(j).at(i);
            if (current_word_count /* != 0 */ ) ++idf;
            amounts[j] += current_word_count; // calculate amount of words in file
        }
        idf = std::log(amount_of_files/idf); //applyintg the formula
        idfs[i] = idf;
    }

    // calculate W for each word
    std::vector<vecd> ret(amount_of_files);
    for (auto& x : ret) x = vecd(amount_of_words);

    // Надо, блять, духовно расти
    //        Иначе пиздец

    for (size_t file = 0; file < amount_of_files; ++file)
    {   // пожалуйста, заработай с первого раза...
        for (size_t word = 0; word < amount_of_words; ++word)
        {   // я тебя умоляю...
            ret[file][word] = idfs[word] * (files.at(file).at(word) / amounts.at(file));
        }
    }

    return ret;
}

double math::vector_abs(const vec &v)
{
    return std::sqrt(std::accumulate(v.cbegin(), v.cend(), 0.0,
        [] (auto acc, auto x) {
            return acc + x*x;
    }));
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

void internal::read_from_chars(const char ***what, uint how_much, filemaps &where, all_keys_t &all_keys)
{
    // вынести вверх
    //if (!docsv || !docsc) return "Для первого задания необходим путь к входным файлам и количество файлов не может быть нулевым.";
    for (uint i = 0; i < how_much; ++i)
    {
        for (char** strarr = what[i]; *strarr; ++strarr) // read until nullptr
        {
            auto key = std::string(*strarr);
            ++where[i][key];
            all_keys.insert(key);
        }
    }
}

void internal::read_from_files(char *foldername, filemaps &where, all_keys_t &all_keys)
{
    fs::path path{foldername};
    for (const auto & entry: fs::directory_iterator{path})
    {
        if (!entry.is_character_file()) continue;
        std::ifstream current_file(entry);
        if (!current_file.is_open())
        {
            std::cerr << "COULD NOT OPEN INPUT FILE " << entry << std::endl;
            std::terminate();
        }
        where.push_back(filemap());
        std::string key;
        uint amount;
        while (current_file >> key >> amount)
        {
            where.back().insert({key, amount});
            all_keys.insert(key);
        }
        if (!file.eof())
        {
            std::cerr << "COULD NOT READ INPUT FILE " << entry << std::endl;
            std::terminate();
        }
    }
}

vecd math::sub_vector(const vecd &x, const vecd &y)
{
    assers(x.size() == y.size());
    size_t vdim = s.size();
    vecd ret(vdim);
    for (size_t i = 0; i < vdim; ++i)
        ret[i] = x[i]-y[i];
    return ret;
}

double math::angle_cos(const vecd &x, const vecd &y)
{
    // cos(a) = |x * y| / sqrt(|x|*|y|);
    return std::abs( math::dot_product(x, y) )
           / (math::vector_abs(x) * math::vector_abs(y) );
}
