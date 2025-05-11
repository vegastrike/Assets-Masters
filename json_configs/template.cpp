/*
 * configuration.cpp
 *
 * Copyright (C) 2021-2025 Daniel Horn, Roy Falk, ministerofinformation,
 * David Wales, Stephen G. Tuggy, and other Vega Strike contributors
 *
 * https://github.com/vegastrike/Vega-Strike-Engine-Source
 *
 * This file is part of Vega Strike.
 *
 * Vega Strike is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 *
 * Vega Strike is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Vega Strike. If not, see <https://www.gnu.org/licenses/>.
 */


#include <iostream>
#include <exception>
#include <boost/json.hpp>
#include <boost/property_tree/json_parser.hpp>

#include "configuration.h"

#ifndef _USE_MATH_DEFINES
#define _USE_MATH_DEFINES
#endif
#include <math.h>
#include <vs_logging.h>
#include <boost/format/format_fwd.hpp>
#include <boost/program_options/errors.hpp>

vega_config::Configuration::Configuration()
= default;

vega_config::Configuration::Configuration(const std::string& json_text) {
    load_config(json_text);
}

vega_config::Configuration::Configuration(const boost::filesystem::path& config_file_path) {
    load_config(config_file_path);
}

void vega_config::Configuration::load_config(const boost::filesystem::path& config_file_path) {
    try {
        std::ifstream config_file(config_file_path.string());
        std::string str;
        std::string file_contents;
        while (std::getline(config_file, str)) {
            file_contents += str;
            file_contents.push_back('\n');
        }
        load_config(file_contents);
    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
    }
}

void vega_config::Configuration::load_config(const std::string& json_text) {
    try {
        if (json_text.empty()) {
            return;
        }
        boost::json::value json_value = boost::json::parse(json_text);
        if (json_value.is_null()) {
            return;
        }
        const boost::json::object & root_object = json_value.get_object();


// JsonStruct
    }
    catch (std::exception const& e)
    {
        std::cerr << e.what() << std::endl;
    }
}

std::shared_ptr<vega_config::Configuration> configuration() {
    static const std::shared_ptr<vega_config::Configuration> kConfiguration = std::make_shared<vega_config::Configuration>();
    return kConfiguration;
}


int main() {
    std::ifstream file("example.json");
    std::string str;
    std::string file_contents;
    while (std::getline(file, str)) {
        file_contents += str;
        file_contents.push_back('\n');
    }

    Config cfg(file_contents);
    std::cout << "string " << cfg.string_key << std::endl;
    std::cout << "int " << cfg.int_key << std::endl;
    std::cout << "double " << cfg.double_key << std::endl;
    std::cout << "bool " << cfg.bool_key << std::endl;

    std::cout << "string " << cfg.inner.string_key << std::endl;
    std::cout << "int " << cfg.inner.int_key << std::endl;
    std::cout << "double " << cfg.inner.double_key << std::endl;
    std::cout << "bool " << cfg.inner.bool_key << std::endl;

    std::cout << "string " << cfg.inner.really_inner.string_key << std::endl;
    std::cout << "int " << cfg.inner.really_inner.int_key << std::endl;
    std::cout << "double " << cfg.inner.really_inner.double_key << std::endl;
    std::cout << "bool " << cfg.inner.really_inner.bool_key << std::endl;

    std::cout << "string " << cfg.inner.really_inner.really_innermost.string_key << std::endl;
    std::cout << "int " << cfg.inner.really_inner.really_innermost.int_key << std::endl;
    std::cout << "double " << cfg.inner.really_inner.really_innermost.double_key << std::endl;
    std::cout << "bool " << cfg.inner.really_inner.really_innermost.bool_key << std::endl;
}
