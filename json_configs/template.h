/*
 * configuration.h
 *
 * Copyright (C) 2021-2025 Daniel Horn, Roy Falk, ministerofinformation,
 * David Wales, Stephen G. Tuggy, Benjamen R. Meyer, and other Vega Strike contributors
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


#ifndef VEGA_STRIKE_ENGINE_CONFIG_CONFIGURATION_H
#define VEGA_STRIKE_ENGINE_CONFIG_CONFIGURATION_H

#include <string>
#include <memory>
#include <boost/filesystem/path.hpp>

#include "components/energy_consumer.h"

namespace vega_config {
	struct Configuration {
	    Configuration();
		explicit Configuration(const std::string& json_text);
	    explicit Configuration(const boost::filesystem::path& config_file_path);

		void load_config(const std::string& json_text);
		void load_config(const boost::filesystem::path & config_file_path);

// JsonStruct
    };

	// extern std::shared_ptr<Config> config;
}

extern std::shared_ptr<vega_config::Configuration> configuration();

#endif //VEGA_STRIKE_ENGINE_CONFIG_CONFIGURATION_H
