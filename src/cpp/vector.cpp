#include "vector.hpp"

const char* driver (
    uint flags,
    uint first_doc_filename,
    uint first_theme_filename,
    char*** docsv,   uint docsc,
    char*** themesv, uint themesc,
    char* themes_in,
    char* analyze_in,
    char* final_out
) {
    filemaps files;
    filemaps themes;
    all_keys_t all_keys;
    if (flags == 0b11)
    {
        files = filemaps(docsc);
        themes = filemaps(themesc);

        if (!docsv || !docsc) return "Для первого задания необходим путь к входным файлам и количество файлов не может быть нулевым.";
        if (!themesv || !themesc) return "Для первого задания необходим путь и количество файлов не может быть нулевым.";

        internal::read_from_chars(docsv, docsc, files, all_keys);
        internal::read_from_chars(docsv, docsc, files, all_keys);
    }
    if (flags == 0b10)
    {
        if (!analyze_in) return "При выполнении второго задания отдельно от первого, необходимо предоставить путь до проанализированных файлов";
        if (!themes_in) return "При выполнении второго задания отдельно от первого, необходимо предоставить путь до папки с проанализированными темами";

        internal::read_from_files(analyze_in, files, all_keys);
        internal::read_from_files(themes_in, themes, all_keys);

    }

    internal::normalize_keys(all_keys, files, themes);
    auto [files_parsed, themes_parsed, order] = internal::get_vectors(all_keys, files, themes);

    auto themes_calculated = internal::get_word_costs(themes_parsed, order);
    auto files_calculated = internal::get_word_costs(files_parsed, order);

    auto compare_result = internal::compare_themes(files_calculated, themes_calculated);
    internal::output_data(compare_result, final_out, first_doc_filename, first_theme_filename);
    return "";
}

void print_2d_array(char*** array, uint size)
{
    std::cout << "running test function...\n";
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
    //SFD;
    for (size_t i = 0; i < maps.size(); ++i)
    {
        for (const auto& key : order)
        {
            ret1.at(i).push_back(maps.at(i).at(key));
        }
    }
    for (size_t i = 0; i < themes.size(); ++i)
    {
        for (const auto& key : order)
        {
            ret2.at(i).push_back(themes.at(i).at(key));
        }
    }
    //SFD;
    return std::make_tuple(ret1, ret2, order);
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

    //блять, главное с индексами не запутаться...
    for (size_t i = 0; i < amount_of_words; ++i)
    {
        double idf = 0;
        for(size_t j = 0; j < amount_of_files; ++j)
        {   //amount of files containing that word
            int current_word_count = files.at(j).at(i);
            if (current_word_count /* != 0 */ ) ++idf;
            amounts[j] += current_word_count;
            // calculate amount of words in file
        }
        if (std::abs(idf) > 0.0001)
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
            ret.at(file).at(word) =
                idfs[word] * ( static_cast<double>( files.at(file).at(word) )
                             / static_cast<double>( amounts.at(file)) );
        }
    }
    return ret;
}

void internal::read_from_chars(char ***what, uint how_much, filemaps &where, all_keys_t &all_keys)
{
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
        if (entry.is_directory()) continue;
        std::ifstream current_file(entry.path());
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
        if (!current_file.eof())
        {
            std::cerr << "COULD NOT READ INPUT FILE " << entry << std::endl;
            std::terminate();
        }
    }
}

std::vector<vecd> internal::compare_themes(
    const std::vector<vecd> &costsd,
    const std::vector<vecd> &costst
) {
    size_t nfiles = costsd.size(),
           nthemes = costst.size();
    std::vector<vecd> ret(nfiles);
    for (auto & x : ret)
        x = vecd(nthemes);
    for (size_t i = 0; i < nfiles; ++i)
    {
        for (size_t j = 0; j < nthemes; ++j)
        {
            ret[i][j] = math::angle_cos(costsd[i], costst[j]);
        }
    }
    return ret;
}

void internal::output_data(
    const std::vector<vecd> &docs_themes,
    char* output_path,
    uint doc_index,
    uint theme_index
) {
    auto path_to_files = fs::path{output_path};
    fs::create_directories(path_to_files);

    std::ofstream current_file(path_to_files / "classification");

    if (!current_file.is_open())
    {
        std::cerr << "\e[1;91mcould not write to classification file\e[0m" << std::endl;
        std::terminate();
    }
    for (size_t i = 0; i < docs_themes.size(); ++i)
    {
        SANITY_CHECK(
            std::cerr << "INDEX " << i << '\n';
            for (const auto& x : docs_themes[i])
                std::cerr << x << ' ';
            std::cerr << '\n';
        )

        double min_value = 1000000;
        size_t min_index = 0;
        for (size_t index = 0; index < docs_themes[i].size(); ++index)
        {
            if (min_value >= docs_themes.at(i).at(index))
            {
                min_value = docs_themes.at(i).at(index);
                min_index = index;
            }
        }

        current_file << doc_index + i << '\t' << theme_index + min_index << std::endl;

    }
}
